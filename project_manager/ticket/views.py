from django.views.generic import TemplateView
from .models import Ticket, MileStone
from forms import TaskForm
from base.views import GenericModalCreateView
from base.mixin import  GeneralContextMixin, ForActionMixin

from django.shortcuts import HttpResponseRedirect, HttpResponse


class DashboardView(GeneralContextMixin, TemplateView):

    template_name = 'ticket/dashbord.html'


# def testing(request):
#   return HttpRespose("hello")


class TicketListView(ForActionMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/ticket_list.html'
    model = Ticket
    app_url = 'ticket'
    page_url = 'ticket_list'
    object_name = 'Ticket'

    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        ticket_list = Ticket.objects.all()
        context['ticket_list'] = ticket_list
        context['form'] = TaskForm()
        return context

    def do_action(self, objects):
        print objects
        return HttpResponseRedirect(self.get_success_url())



# MilestoneListView
class TicketDetailView(GeneralContextMixin, TemplateView):
    template_name = 'ticket/detail_user.html'

    def get_context_data(self, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        detail_list = MileStone.objects.filter(ticket__id=ticket_id)
        ticket = Ticket.objects.get(pk=ticket_id)
        context['ticket'] = ticket
        context['detail_list'] = detail_list
        return context


class TicketCreateView (GenericModalCreateView):
    form_class = TaskForm
    success_url = '/ticket/ticket_list/'

def delete_ticket(request):
    delete_ids = request.GET.getlist('for_action')
    print delete_ids
    # tickets = Ticket.objects.filter(id__in=delete_ids )

    return HttpResponse('/ticket/ticket_list')
'''
class MilestoneCreateView():
    pass
'''