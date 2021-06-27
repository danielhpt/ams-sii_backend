from django.urls import path

from .views import *

urlpatterns = [
    # # API
    path('api/users/', UserList.as_view(), name="user_list"),  # admin only?
    # path('api/users/<int:user_id>/', None, name="user_detail"),
    # path('api/users/<int:user_id>/teams/', None, name="user_team_list"),
    # path('api/users/<int:user_id>/occurrences/', None, name="user_occurrences_list"),
    path('api/teams/', TeamList.as_view(), name="team_list"),  # admin only?
    # path('api/teams/<int:team_id>/', None, name="team_detail"),
    # path('api/teams/<int:team_id>/occurrences/', None, name="team_occurrences_list"),
    path('api/occurrences/', OccurrenceList.as_view(), name="occurrence_list"),  # admin only?
    path('api/occurrences/<int:occurrence_id>/', OccurrenceDetails.as_view(), name="occurrence_detail"),
    # path('api/occurrences/<int:occurrence_id>/victims/', None, name="occurrence_victims_list"),
    path('api/victims/<int:victim_id>', VictimDetails.as_view(), name="victim_detail"),

    # WEB
    # path('', views.index, name="index"),
]
