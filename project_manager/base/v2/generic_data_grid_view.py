from django.views.generic import TemplateView

from django.core.exceptions import ImproperlyConfigured

from django.conf import settings

from django.contrib import messages

from django.shortcuts import HttpResponseRedirect

from django.utils.safestring import mark_safe
from django.utils import timezone

import django_tables2 as tables
from django_tables2 import RequestConfig
from django_tables2.utils import AttributeDict, A

from base.forms import DateRangeForm

import logging
logger = logging.getLogger(__name__)

try:
    generic_table_attr = settings.GENERIC_TABLE_ATTRS
except:
    raise ImproperlyConfigured(
        "GENERIC_TABLE_ATTRS requires a defined in "
        "django settings"
    )


class CustomCheckBoxColumn(tables.CheckBoxColumn):

    @property
    def header(self):
        default = {
            'type': 'checkbox',
            'class': "tableflat",
            'id': "checkboxall",
            'name': 'for_action',
        }
        general = self.attrs.get('input')
        specific = self.attrs.get('th__input')
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe('<input %s/>' % attrs.as_html())

    def render(self, value, bound_column, record):
        default = {
            'type': 'checkbox',
            'name': 'for_action',
            'value': value
        }
        if self.is_checked(value, record):
            default.update({
                'checked': 'checked',
            })

        general = self.attrs.get('input')
        specific = self.attrs.get('td__input')
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe('<input %s/>' % attrs.as_html())


class GenericDataTableView(TemplateView):

    """
    Required Params:

    - 'model' is django model class whose data is rendered into table

    - 'list_display' is python list, containing all the
    fields to be displayed as table columns

    - 'detail_page' is url string expressed in django url reverse format
        Ex: 'jobcard:detail'

    - 'template_name' is template path which is used by TemplateView

    Optional Params:

    - 'per_page_count' is number of objs to be shown per page
        warning >> Changing this may affect the page loading speed
    - 'checkbox' is bool if assigned True checkbox column added
    """

    per_page_count = 25
    model = None
    list_display = None
    detail_page = None
    checkbox = False
    title = 'Your title goes here'
    sub_title = 'Your sub-title goes here'
    date_query_attr = 'created_at'
    action_dict = {}
    accessor_attr = 'pk'

    def get(self, request, *args, **kwargs):
        if 'go' in self.request.GET:
            print "GO"
            dispatch = request.GET.get('action')
            self.for_action_keys = request.GET.getlist('for_action')
            print "lenght {0}".format(len(self.for_action_keys))
            try:
                method = getattr(self, dispatch)
            except:
                raise AttributeError(
                    "GenericDataGridView has no method '{0}' defined."
                    "Please define method '{0}'".format(dispatch)
                )
            if len(self.for_action_keys) == 0:
                messages.error(
                    request,
                    "Error! Select atlest one item for action"
                )
                return HttpResponseRedirect(
                    self.request.META['PATH_INFO'])
            else:
                return method()
        else:
            return super(GenericDataTableView, self).get(
                request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.model is None and self.list_display is None:
            raise ImproperlyConfigured(
                "GenericDataTableView requires a definition of "
                "'model' and 'list_display' ")
        context = super(
            GenericDataTableView, self).get_context_data(**kwargs)
        query = self.get_queryset()
        if self.request.GET.get('start_date') \
                and self.request.GET.get('end_date'):
            logger.debug("I am date ranging")
            query = self.query_date(query)
        table = self.table_on_the_fly()
        table = table(query)
        RequestConfig(
            self.request, paginate={
                'per_page': self.per_page_count}).configure(table)
        context['table'] = table
        context['title'], context['sub_title'] = self.get_titles()
        context['date_range'] = True
        if self.action_dict:
            context['action_dict'] = self.action_dict
        return context

    def query_date(self, query):
        form = DateRangeForm(self.request.GET)
        if form.is_valid():
            logger.debug('DateRangeForm is valid')
            to_date = form.cleaned_data['end_date']
            from_date = form.cleaned_data['start_date']
            logger.info(
                "Form is valid with {0}-{1}".format(from_date, to_date))
            if to_date <= timezone.now().date() or from_date <= timezone.now().date() or self.date_query_attr is not 'created_at':
                if to_date == from_date:
                    to_date = timezone.datetime.strptime(
                        self.request.GET["start_date"], "%m/%d/%Y")
                    dynamic_args = dict()
                    dynamic_args['{0}__year'.format(
                        self.date_query_attr)] = to_date.year
                    dynamic_args['{0}__month'.format(
                        self.date_query_attr)] = to_date.month
                    dynamic_args['{0}__day'.format(
                        self.date_query_attr)] = to_date.day
                    object_list = query.filter(
                        **dynamic_args).order_by(
                        '-{0}'.format(self.date_query_attr))
                    return object_list
                else:
                    # some weired stuff need to add 24hr or day
                    date_range = [from_date,
                                  to_date + timezone.timedelta(hours=24)]
                    dynamic_args = dict()
                    dynamic_args["{0}__range".format(
                        self.date_query_attr)] = date_range
                    object_list = query.filter(**dynamic_args).order_by(
                        '-{0}'.format(self.date_query_attr))
                    return object_list
                logger.debug(
                    "Date filtered objects: {0}".format(object_list))
            else:
                logger.debug("Improper Date Range")
                messages.warning(self.request,
                                 "Improper dates try other dates")
        else:
            logger.debug("Improper Date Range")
            messages.warning(self.request,
                             "Improper dates try other dates")

    # To do get_titles overriding not working
    def get_titles(self):
        """
        Override this method to return custom titles
        """
        if self.title and self.sub_title:
            return self.title, self.sub_title

    def get_queryset(self):
        """
        Override this method to pass
        custom queryset
        """
        return self.model.objects.all()

    def table_on_the_fly(self):
        OnTheFlyTable = type(
            'OnTheFlyTable',
            (tables.Table,),
            self.get_properties()
        )
        return OnTheFlyTable

    def get_properties(self):
        """
        Returns a dict containing table meta obj and properties
        for generating on the fly table
        """
        properties_dict = dict()
        Meta = type(
            'Meta',
            (object,),
            {
                'model': self.model,
                'fields': self.get_list_display(),
                'attrs': generic_table_attr,
                'template': 'django_tables2/bootstrap.html',
            }
        )
        properties_dict['Meta'] = Meta
        if (self.checkbox or self.action_dict) \
                and not properties_dict.get('selection'):
            properties_dict['selection'] = CustomCheckBoxColumn(
                accessor='pk', orderable=True, attrs={'name': 'for_action'})
        if self.detail_page and not properties_dict.get('action'):
            properties_dict['action'] = tables.LinkColumn(
                self.detail_page, args=[A(self.accessor_attr)], text='More')
        return properties_dict

    def get_list_display(self):
        """
        Returns a tuple
        Mutates the list, inserts default columns
        """
        if (self.checkbox or self.action_dict) \
                and 'selection' not in self.list_display:
            self.list_display.insert(0, 'selection')
        if self.detail_page and 'action' not in self.list_display:
            self.list_display.insert(-1, 'action')
        return tuple(self.list_display)
