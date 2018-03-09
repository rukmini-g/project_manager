"""Djangomon url"""
import views

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^dashboard/$',
    	views.DashboardView.as_view(), name='dashboard'),
    url(r'^create/$',
        TicketCreateView.as_view(), name='create'),
    url(r'^ticket_list/$',
    	views.TicketListView.as_view(), name='ticket_list'),
    url(r'^(?P<ticket_id>[^/]+)/$',
        TicketDetailView.as_view(), name='details')

]
