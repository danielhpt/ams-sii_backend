from rest_framework import serializers

from .models import *


class UserSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TechnicianSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='technician.id')
    username = serializers.ReadOnlyField(source='technician.username')
    first_name = serializers.ReadOnlyField(source='technician.first_name')
    last_name = serializers.ReadOnlyField(source='technician.last_name')

    class Meta:
        model = TeamTechnician
        fields = ['id', 'username', 'first_name', 'last_name', 'active', 'team_leader']


class TeamSerializer(serializers.ModelSerializer):
    technicians = TechnicianSerializer(many=True, source='team_technicians')

    class Meta:
        model = Team
        fields = ['id', 'technicians']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        technicians_data = validated_data.pop('technicians')
        team = Team.objects.create()
        for technician_data in technicians_data:
            user = User.objects.get(pk=technician_data['id'])
            teamTechnician = TeamTechnician()
            teamTechnician.team = team
            teamTechnician.technician = user
            teamTechnician.active = technician_data['active']
            teamTechnician.team_leader = technician_data['team_leader']
            teamTechnician.save()
        return team


class OccurrenceSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Occurrence
        fields = ['id', 'occurrence_number', 'entity', 'mean_of_assistance', 'motive', 'number_of_victims', 'local',
                  'parish', 'municipality', 'team']


class VictimSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = ['id', 'name']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'state']


class OccurrenceStateSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = OccurrenceState
        fields = ['id', 'state', 'longitude', 'latitude', 'date_time']


class OccurrenceSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = ['id', 'occurrence_number']


class OccurrenceDetailSerializer(serializers.ModelSerializer):
    victims = VictimSimplifiedSerializer(many=True, read_only=True)
    states = OccurrenceStateSerializer(many=True, read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Occurrence
        fields = ['id', 'occurrence_number', 'entity', 'mean_of_assistance', 'motive', 'number_of_victims', 'local',
                  'parish', 'municipality', 'team', 'victims', 'states']


class TypeOfTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfTransport
        fields = ['id', 'type_of_transport']


class NonTransportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonTransportReason
        fields = ['id', 'non_transport_reason']


class VictimSerializer(serializers.ModelSerializer):
    type_of_transport = TypeOfTransportSerializer(read_only=True)
    non_transport_reason = NonTransportReasonSerializer(read_only=True)
    occurrence = OccurrenceSimplifiedSerializer(read_only=True)

    class Meta:
        model = Victim
        fields = ['id', 'name', 'birthdate', 'age', 'gender', 'identity_number', 'address', 'circumstances',
                  'disease_history', 'allergies', 'last_meal', 'last_meal_time', 'usual_medication', 'risk_situation',
                  'medical_followup', 'health_unit_origin', 'health_unit_destination', 'episode_number', 'comments',
                  'type_of_emergency', 'type_of_transport', 'non_transport_reason', 'occurrence']


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['id', 'time', 'pharmacy', 'dose', 'route', 'adverse_effect']


class ProcedureScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureScale
        fields = ['id', 'cincinatti', 'PROACS', 'RTS', 'MGAP', 'RACE']


class ProcedureCirculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureCirculation
        fields = ['id', 'temperature_monitoring', 'compression', 'tourniquet', 'pelvic_belt', 'venous_access', 'patch',
                  'ecg']


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'hours', 'avds', 'ventilation', 'spo2', 'o2', 'etco2', 'pulse', 'ecg', 'skin', 'temperature',
                  'systolic_blood_pressure', 'diastolic_blood_pressure', 'pupils', 'pain', 'glycemia', 'news']


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'comments', 'image_path']


class ProcedureRCPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureRCP
        fields = ['id', 'witnessed', 'SBV_DAE', 'SIV_SAV', 'first_rhythm', 'nr_shocks', 'recovery', 'downtime',
                  'mechanical_compressions', 'performed']


class ProcedureVentilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureVentilation
        fields = ['id', 'clearance', 'oropharyngeal', 'laryngeal_tube', 'endotracheal', 'laryngeal_mask',
                  'mechanical_ventilation', 'cpap']


class ProcedureProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureProtocol
        fields = ['id', 'immobilization', 'TEPH', 'SIV', 'VV_AVC', 'VV_coronary', 'VV_sepsis', 'VV_trauma', 'VV_PCR']


class VictimDetailsSerializer(serializers.ModelSerializer):
    type_of_transport = serializers.ReadOnlyField(source='type_of_transport.type_of_transport')
    non_transport_reason = serializers.ReadOnlyField(source='non_transport_reason.non_transport_reason')
    occurrence = OccurrenceSimplifiedSerializer(read_only=True)
    symptom = SymptomSerializer(read_only=True)
    evaluations = EvaluationSerializer(many=True, read_only=True)
    procedure_rcp = ProcedureRCPSerializer(read_only=True)
    procedure_ventilation = ProcedureVentilationSerializer(read_only=True)
    procedure_protocol = ProcedureProtocolSerializer(read_only=True)
    procedure_circulation = ProcedureCirculationSerializer(read_only=True)
    procedure_scale = ProcedureScaleSerializer(read_only=True)
    pharmacy = PharmacySerializer(many=True, read_only=True)

    class Meta:
        model = Victim
        fields = ['id', 'name', 'birthdate', 'age', 'gender', 'identity_number', 'address', 'circumstances',
                  'disease_history', 'allergies', 'last_meal', 'last_meal_time', 'usual_medication', 'risk_situation',
                  'medical_followup', 'health_unit_origin', 'health_unit_destination', 'episode_number', 'comments',
                  'type_of_emergency', 'type_of_transport', 'non_transport_reason', 'occurrence', 'symptom',
                  'evaluations', 'procedure_rcp', 'procedure_ventilation', 'procedure_protocol',
                  'procedure_circulation', 'procedure_scale', 'pharmacy']
