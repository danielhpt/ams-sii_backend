from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden

from .serializers import *


def userDetails(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.id != user_id:
        return HttpResponseForbidden()

    user = get_object_or_404(User, pk=user_id)

    context = {
        'user': user,
        'user_id': request.user.id
    }

    return render(request, 'userDetails.html', context=context)


def occurrenceListByNumber(request, occurrence_number):
    if not request.user.is_authenticated:
        return redirect('login')

    occurrences = Occurrence.objects.filter(occurrence_number=occurrence_number)

    context = {
        'occurrences': occurrences,
        'user_id': request.user.id

    }

    return render(request, 'occurrenceListByNumber.html', context=context)


def occurrenceDetails(request, occurrence_id):
    if not request.user.is_authenticated:
        return redirect('login')

    occurrence = get_object_or_404(Occurrence, pk=occurrence_id)

    context = {
        'occurrence': occurrence,
        'user_id': request.user.id

    }

    return render(request, 'occurrenceDetails.html', context=context)


def victimDetails(request, victim_id):
    if not request.user.is_authenticated:
        return redirect('login')

    victim = get_object_or_404(Victim, pk=victim_id)

    context = {
        'victim': victim,
        'user_id': request.user.id
    }

    return render(request, 'victimDetails.html', context=context)
