from django.views.generic import TemplateView, View

# from django.shortcuts import HttpRespose


class DashboardView(TemplateView):

    template_name = 'ticket/dashboard.html'

# def testing(request):
#   return HttpRespose("hello")


class TicketListView():
    pass

# MilestoneListView
class TicketDetailView():
    pass


class TicketCreateView():
    pass


class MilestoneCreateView():
    pass