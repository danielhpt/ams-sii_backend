from django.shortcuts import get_object_or_404, HttpResponse, render, redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response, status

from .serializers import *


def userDetails(request, user_id):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    user = get_object_or_404(User, pk=user_id)
    context = {
         'user': user

    }
    return render(request, 'userDetails.html', context=context)


def occurrenceListByNumber(request, occurrence_number):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    context = {

    }

    return render(request, 'occurrenceListByNumber.html', context=context)


def occurrenceDetails(request, occurrence_id):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    context = {

    }

    return render(request, 'occurrenceDetails.html', context=context)


def occurrenceVictimsList(request, occurrence_id):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    context = {

    }

    return render(request, 'occurrenceVictimsList.html', context=context)


def occurrenceStateList(request, occurrence_id):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    context = {

    }

    return render(request, 'occurrenceStateList.html', context=context)


def victimDetails(request, victim_id):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    context = {

    }

    return render(request, 'victimDetails.html', context=context)
