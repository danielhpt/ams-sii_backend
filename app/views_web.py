from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden

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
    if not request.user.is_authenticated:
        return redirect('login')

    occurrence = get_object_or_404(Occurrence, pk=occurrence_id)

    context = {

    }

    return render(request, 'occurrenceDetails.html', context=context)


def victimDetails(request, victim_id):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    context = {
        'victim': victim,
        'user_id': request.user.id
    }

    return render(request, 'victimDetails.html', context=context)
