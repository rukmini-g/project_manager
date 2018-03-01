"""Djangomon url"""
import views

from django.conf.urls import url

from .views import *

urlpatterns = [
	# url(r'^test/$', views.testing, name='dashboard'),
    url(r'^dashboard/$', views.DashboardView, name='dashboard'),
]
