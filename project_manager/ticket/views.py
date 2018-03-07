from django.views.generic import TemplateView, View, DetailView
from .models import Ticket, MileStone
from django.http import HttpResponse


class DashboardView(TemplateView):

    template_name = 'ticket/dashbord.html'


# def testing(request):
#   return HttpRespose("hello")


class TicketListView(TemplateView):
    #ticket = Ticket.objects.all()
    template_name = 'ticket/ticket_list.html'
    '''
    context_object_name = 'ticket_list'
    def get_queryset(self):
        return Ticket.objects.all ()
    '''
    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        ticket_list = Ticket.objects.all ()
        context['ticket_list'] = ticket_list
        return context

# MilestoneListView
class TicketDetailView(TemplateView):
    template_name = 'ticket/detail_user.html'
    # detail_list = MileStone.objects.all()

    def get_context_data(self, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        detail_list = MileStone.objects.filter(ticket__id=ticket_id)
        ticket = Ticket.objects.get (pk=ticket_id)
        context['ticket'] = ticket
        context['detail_list'] = detail_list
        return context




class TicketCreateView():
    pass


class MilestoneCreateView():
    pass