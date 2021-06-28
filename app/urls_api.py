from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views_api import *

urlpatterns = [
    # API
    path('token/', obtain_auth_token),

    path('users/', UserList.as_view(), name="user_list"),  # admin only
    path('users/<int:user_id>/', UserDetail.as_view(), name="user_detail"),
    path('users/<int:user_id>/teams/', UserTeamList.as_view(), name="user_team_list"),
    path('users/<int:user_id>/occurrences/', UserOccurrenceList.as_view(), name="user_occurrences_list"),

    path('teams/', TeamList.as_view(), name="team_list"),  # admin only
    path('teams/<int:team_id>/', TeamDetail.as_view(), name="team_detail"),
    path('teams/<int:team_id>/occurrences/', TeamOccurrencesList.as_view(), name="team_occurrences_list"),

    path('occurrences/', OccurrenceList.as_view(), name="occurrence_list"),  # admin only
    path('occurrences/<int:occurrence_id>/', OccurrenceDetails.as_view(), name="occurrence_detail"),
    path('occurrences/<int:occurrence_id>/victims/', OccurrenceVictimsList.as_view(), name="occurrence_victims_list"),
    path('occurrences/<int:occurrence_id>/states/', OccurrenceStateList.as_view(), name="occurrence_states_list"),

    path('victims/<int:victim_id>/', VictimDetails.as_view(), name="victim_detail"),
    path('victims/<int:victim_id>/pharmacies/', VictimPharmacyList.as_view(), name="victim_pharmacy_list"),
    path('victims/<int:victim_id>/pharmacies/<int:pharmacy_id>/', VictimPharmacyDetail.as_view(), name="victim_pharmacy_detail"),
    path('victims/<int:victim_id>/evaluations/', VictimEvaluationList.as_view(), name="victim_evaluation_list"),
    path('victims/<int:victim_id>/evaluations/<int:evaluation_id>/', VictimEvaluationDetail.as_view(), name="victim_evaluation_detail"),
    path('victims/<int:victim_id>/symptom/', VictimSymptomList.as_view(), name="victim_symptom"),
    path('victims/<int:victim_id>/procedure_rcp/', VictimProcedureRCPList.as_view(), name="victim_procedure_rcp"),
    path('victims/<int:victim_id>/procedure_ventilation/', VictimProcedureVentilationList.as_view(), name="victim_procedure_ventilation"),
    path('victims/<int:victim_id>/procedure_protocol/', VictimProcedureProtocolList.as_view(), name="victim_procedure_protocol"),
    path('victims/<int:victim_id>/procedure_circulation/', VictimProcedureCirculationList.as_view(), name="victim_procedure_circulation"),
    path('victims/<int:victim_id>/procedure_scale/', VictimProcedureScaleList.as_view(), name="victim_procedure_scale"),
]
