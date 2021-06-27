from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status

from .models import *
from .serializers import *


# API
class UserList(APIView):
    """List all Users"""

    def get(self, request):  # working
        users = User.objects.all()
        serializer = UserSimplifiedSerializer(users, many=True)

        return Response(serializer.data)


# todo UserDetail
# todo UserTeamList
# todo UserOccurrenceList


class TeamList(APIView):
    """List all Teams"""

    def get(self, request):  # working
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)

        return Response(serializer.data)

    def post(self, request):  # working
        serializer = TeamSerializer(data=request.data.copy())

        if serializer.is_valid():
            serializer.save()
            result = TeamSerializer(Team.objects.get(pk=serializer.instance.id))
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# todo TeamDetail
# todo TeamOccurrencesList


class OccurrenceList(APIView):
    """List all Occurrences"""

    def get(self, request):  # working
        occurrences = Occurrence.objects.all()
        serializer = OccurrenceSerializer(occurrences, many=True)

        return Response(serializer.data)


class OccurrenceDetails(APIView):
    """List the details of an Occurrence"""

    def get(self, request, occurrence_id):  # working
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
        serializer = OccurrenceDetailSerializer(occurrence)

        return Response(serializer.data)

    def put(self, request, occurrence_id):  # working
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
        data = request.data.copy()
        serializer = OccurrenceDetailSerializer(occurrence, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


# todo OccurrenceVictimsList


class StateList(APIView):
    """List all States"""

    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)

        return Response(serializer.data)


class OccurrenceStateList(APIView):
    """List all Occurrence States"""

    def get(self, request):
        occurrence_states = OccurrenceState.objects.all()
        serializer = OccurrenceStateSerializer(occurrence_states, many=True)

        return Response(serializer.data)

    def post(self, request, occurrence_id):
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
        data = request.data.copy()
        state = State.objects.get(pk=data.state.id)

        occurrenceState = OccurrenceState()
        occurrenceState.occurrence = occurrence
        occurrenceState.state = state

        serializer = OccurrenceStateSerializer(occurrenceState)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TypeOfTransportList(APIView):
    """List all Type of transports"""

    def get(self, request, victim_pk):
        transports_type = TypeOfTransport.objects.all()
        serializer = TypeOfTransportSerializer(transports_type, many=True)

        return Response(serializer.data)


class NonTransportReasonList(APIView):
    """List all non transport reasons"""

    def get(self, request, victim_id):
        victim = get_object_or_404(Victim, pk=victim_id)
        non_transport_reason = NonTransportReason.objects.all().filter(victim=victim)
        serializer = NonTransportReasonSerializer(non_transport_reason)

        return Response(serializer.data)


class VictimList(APIView):
    """List all victims"""

    def get(self, request, occurrence_id):
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
        victim = Victim.objects.all().filter(occurrence=occurrence)
        serializer = VictimSerializer(victim)

        return Response(serializer.data)

    def post(self, request, occurrence_id):
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
        data = request.data.copy()
        data["occurrence"] = occurrence.id
        serializer = VictimDetailsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimDetails(APIView):
    """List the details of a Victim"""

    def get(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        serializer = VictimDetailsSerializer(victim)

        return Response(serializer.data)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        serializer = VictimDetailsSerializer(victim, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)