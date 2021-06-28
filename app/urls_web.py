from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.urls import path

from . import views_web

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/<int:user_id>/', views_web.userDetails, name='user_detail'),
    path('occurrences/<int:occurrence_id>/', views_web.occurrenceDetails, name="occurrence_detail"),
    path('occurrences/<int:occurrence_id>/victims/', views_web.occurrenceVictimsList, name="occurrence_victims_list"),
    path('occurrences/<int:occurrence_id>/states/', views_web.occurrenceStateList, name="occurrence_states_list"),
    path('victims/<int:victim_id>/', views_web.victimDetails, name="victim_detail"),
    path('occurrences/<int:occurrence_number>/', views_web.occurrenceListByNumber, name="occurrence_list_by_number"),



]
