from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.urls import path

from .views_web import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),


]
