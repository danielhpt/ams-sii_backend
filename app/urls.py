from django.urls import path

from .views import *

urlpatterns = [
    # API
    path('api/users/', UserList.as_view(), name="user_list"),  # admin only?
    path('api/users/<int:user_id>/', UserDetail.as_view(), name="user_detail"),
    path('api/users/<int:user_id>/teams/', UserTeamList.as_view(), name="user_team_list"),
    path('api/users/<int:user_id>/occurrences/', UserOccurrenceList.as_view(), name="user_occurrences_list"),

    path('api/teams/', TeamList.as_view(), name="team_list"),  # admin only?
    path('api/teams/<int:team_id>/', TeamDetail.as_view(), name="team_detail"),
    # path('api/teams/<int:team_id>/occurrences/', None, name="team_occurrences_list"),

    path('api/occurrences/', OccurrenceList.as_view(), name="occurrence_list"),  # admin only?
    path('api/occurrences/<int:occurrence_id>/', OccurrenceDetails.as_view(), name="occurrence_detail"),
    path('api/occurrences/<int:occurrence_id>/victims/', OccurrenceVictimsList.as_view(), name="occurrence_victims_list"),

    path('api/victims/<int:victim_id>/', VictimDetails.as_view(), name="victim_detail"),
    path('api/victims/<int:victim_id>/pharmacies/', VictimPharmacyList.as_view(), name="victim_pharmacy_list"),
    path('api/victims/<int:victim_id>/pharmacies/<int:pharmacy_id>/', VictimPharmacyDetail.as_view(), name="victim_pharmacy_detail"),
    path('api/victims/<int:victim_id>/evaluations/', VictimEvaluationList.as_view(), name="victim_evaluation_list"),
    path('api/victims/<int:victim_id>/evaluations/<int:evaluation_id>/', VictimEvaluationDetail.as_view(), name="victim_evaluation_detail"),
    # path('api/victims/<int:victim_id>/symptom/', None, name="victim_symptom"),
    # path('api/victims/<int:victim_id>/procedure_rcp/', None, name="victim_procedure_rcp"),
    # path('api/victims/<int:victim_id>/procedure_ventilation/', None, name="victim_procedure_ventilation"),
    # path('api/victims/<int:victim_id>/procedure_protocol/', None, name="victim_procedure_protocol"),
    # path('api/victims/<int:victim_id>/procedure_circulation/', None, name="victim_procedure_circulation"),
    # path('api/victims/<int:victim_id>/procedure_scale/', None, name="victim_procedure_scale"),

    # WEB
    # path('', views.index, name="index"),
]
