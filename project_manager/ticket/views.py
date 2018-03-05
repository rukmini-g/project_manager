from django.views.generic import TemplateView, View
from .models import Ticket, MileStone
from django.http import HttpResponse


class DashboardView(TemplateView):

    template_name = 'ticket/dashbord.html'


# def testing(request):
#   return HttpRespose("hello")


class TicketListView(TemplateView):
    #ticket = Ticket.objects.all()
    template_name = 'ticket/list.html'
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
class TicketDetailView(TicketListView):
    ticket = Ticket.objects.filter()



class TicketCreateView():
    pass


class MilestoneCreateView():
    pass