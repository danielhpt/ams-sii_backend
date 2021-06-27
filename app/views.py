from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from .serializers import *


# API
class UserList(APIView):
    """List all Users"""

    def get(self, request):  # working
        users = User.objects.all()
        serializer = UserSimplifiedSerializer(users, many=True)

        return Response(serializer.data)


class UserDetail(APIView):
    """List the details of an User"""

    def get(self, request, user_id):  # working
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSimplifiedSerializer(user)

        return Response(serializer.data)


class UserTeamList(APIView):
    """List the teams of an User"""

    def get(self, request, user_id):  # working
        user = get_object_or_404(User, pk=user_id)
        teams = Team.objects.filter(team_technicians__technician=user)
        serializer = TeamSerializer(teams, many=True)

        return Response(serializer.data)


class UserOccurrenceList(APIView):
    """List the occurrences of an User"""

    def get(self, request, user_id):  # working
        user = get_object_or_404(User, pk=user_id)
        occurrences = Occurrence.objects.filter(team__team_technicians__technician=user)
        serializer = OccurrenceSerializer(occurrences, many=True)

        return Response(serializer.data)


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


class TeamDetail(APIView):
    """List the details of a Team"""

    def get(self, request, team_id):  # working
        team = get_object_or_404(Team, pk=team_id)
        serializer = TeamSerializer(team)

        return Response(serializer.data)

    def put(self, request, team_id):  # todo update and test
        team = get_object_or_404(Team, pk=team_id)
        data = request.data.copy()
        serializer = TeamSerializer(team, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class TeamOccurrencesList(APIView):
    """List all Ocurrences for a specific Team"""

    def get(self, request, team_id):  # working
        team = get_object_or_404(Team, pk=team_id)
        occurrence = get_object_or_404(Occurrence, team=team)
        serializer = OccurrenceSerializer(occurrence)

        return Response(serializer.data)

    def post(self, request, team_id):  # working
        team = get_object_or_404(Team, pk=team_id)

        data = request.data.copy()
        data['team'] = team

        serializer = OccurrenceSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = OccurrenceSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class OccurrenceVictimsList(APIView):
    """List all Victims of an Occurrence"""

    def get(self, request, occurrence_id):  # todo test
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
        victim = Victim.objects.filter(occurrence=occurrence)
        serializer = VictimSerializer(victim, many=True)

        return Response(serializer.data)

    # todo
    def post(self, request, occurrence_id):
        occurrence = get_object_or_404(Occurrence, pk=occurrence_id)

        victim = Victim()
        victim.occurrence = occurrence
        serializer = VictimSerializer(victim, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class VictimPharmacyList(APIView):
    """List the pharmacies of a Victim"""

    def get(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        pharmacies = Pharmacy.objects.filter(victim=victim)
        serializer = PharmacySerializer(pharmacies, many=True)

        return Response(serializer.data)

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = PharmacyDetailSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = PharmacySerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimPharmacyDetail(APIView):
    """List the details of a pharmacies of a Victim"""

    def get(self, request, victim_id, pharmacy_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        pharmacy = get_object_or_404(Pharmacy, pk=pharmacy_id, victim=victim)
        serializer = PharmacySerializer(pharmacy)

        return Response(serializer.data)


class VictimEvaluationList(APIView):
    """List the evaluations of a Victim"""

    def get(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        evaluations = Evaluation.objects.filter(victim=victim)
        serializer = EvaluationSerializer(evaluations, many=True)

        return Response(serializer.data)

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = EvaluationDetailSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = EvaluationSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimEvaluationDetail(APIView):
    """List the details of an evaluation of a Victim"""

    def get(self, request, victim_id, evaluation_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        evaluation = get_object_or_404(Evaluation, pk=evaluation_id, victim=victim)
        serializer = EvaluationSerializer(evaluation)

        return Response(serializer.data)


class VictimSymptomList(APIView):
    """List the Symptons of a Victim"""

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = SymptomSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = SymptomSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        symptom = get_object_or_404(Symptom, pk=victim)
        data = request.data.copy()
        serializer = SymptomSerializer(symptom, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimProcedureRCPList(APIView):
    """List the RCP Procedures of a Victim"""

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = ProcedureRCPSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = ProcedureRCPSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        procedureRCP = get_object_or_404(ProcedureRCP, pk=victim)
        data = request.data.copy()
        serializer = ProcedureRCPSerializer(procedureRCP, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimProcedureVentilationList(APIView):
    """List the Ventilation Procedures of a Victim"""

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = ProcedureVentilationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = ProcedureVentilationSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        procedureVentilation = get_object_or_404(ProcedureVentilation, pk=victim)
        data = request.data.copy()
        serializer = ProcedureVentilationSerializer(procedureVentilation, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimProcedureProtocolList(APIView):
    """List the Protocol Procedures of a Victim"""

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = ProcedureProtocolSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = ProcedureProtocolSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        procedureProtocol = get_object_or_404(ProcedureProtocol, pk=victim)
        data = request.data.copy()
        serializer = ProcedureProtocolSerializer(procedureProtocol, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimProcedureCirculationList(APIView):
    """List the Circulation Procedures of a Victim"""

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = ProcedureCirculationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = ProcedureCirculationSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        procedureCirculation = get_object_or_404(ProcedureCirculation, pk=victim)
        data = request.data.copy()
        serializer = ProcedureCirculationSerializer(procedureCirculation, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VictimProcedureScaleList(APIView):
    """List the Scale Procedures of a Victim"""

    def post(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        data = request.data.copy()
        data['victim'] = victim
        serializer = ProcedureScaleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            result = ProcedureScaleSerializer(serializer.instance)
            return Response(result.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, victim_id):  # working
        victim = get_object_or_404(Victim, pk=victim_id)
        procedureScale = get_object_or_404(ProcedureScale, pk=victim)
        data = request.data.copy()
        serializer = ProcedureScaleSerializer(procedureScale, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
