from rest_framework.serializers import ModelSerializer

from .models import *


class UserSimplifiedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'firstname', 'lastname', 'email']


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'team_leader']


class TeamTechnicianSerializer(ModelSerializer):
    class Meta:
        model = TeamTechnician
        fields = ['id', 'team', 'technician', 'active']

    def to_representation(self, instance):
        self.fields['team'] = TeamSerializer(read_only=True)
        self.fields['technician'] = UserSimplifiedSerializer(read_only=True)
        return super(TeamTechnicianSerializer, self).to_representation(instance)


class OccurrenceSerializer(ModelSerializer):
    class Meta:
        model = Occurrence
        fields = ['occurrence_number', 'entity', 'mean_of_assistance', 'motive', 'number_of_victims', 'local', 'parish',
                  'municipality', 'team']

    def to_representation(self, instance):
        self.fields['team'] = TeamSerializer(read_only=True)
        return super(OccurrenceSerializer, self).to_representation(instance)


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'state']


class OccurrenceStateSerializer(ModelSerializer):
    class Meta:
        model = OccurrenceState
        fields = ['id', 'occurrence', 'state', 'longitude', 'latitude', 'date_time']

    def to_representation(self, instance):
        self.fields['occurrence'] = OccurrenceSerializer(read_only=True)
        self.fields['state'] = StateSerializer(read_only=True)
        return super(OccurrenceStateSerializer, self).to_representation(instance)


class TypeOfTransportSerializer(ModelSerializer):
    class Meta:
        model = TypeOfTransport
        fields = ['id', 'type_of_transport']


class NonTransportReasonSerializer(ModelSerializer):
    class Meta:
        model = NonTransportReason
        fields = ['id', 'non_transport_reason']


class VictimSerializer(ModelSerializer):
    class Meta:
        model = Victim
        fields = ['id', 'name', 'birthdate', 'age', 'gender', 'identity_number', 'address', 'circumstances',
                  'disease_history', 'allergies', 'last_meal', 'last_meal_time', 'usual_medication', 'risk_situation',
                  'medical_followup', 'health_unit_origin', 'health_unit_destination', 'episode_number', 'comments',
                  'type_of_emergency', 'type_of_transport', 'non_transport_reason', 'occurrence']

    def to_representation(self, instance):
        self.fields['type_of_transport'] = TypeOfTransportSerializer(read_only=True)
        self.fields['non_transport_reason'] = NonTransportReasonSerializer(read_only=True)
        self.fields['occurrence'] = OccurrenceSerializer(read_only=True)
        return super(VictimSerializer, self).to_representation(instance)


class PharmacySerializer(ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['id', 'victim', 'time', 'pharmacy', 'dose', 'route', 'adverse_effect']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(PharmacySerializer, self).to_representation(instance)


class ProcedureScaleSerializer(ModelSerializer):
    class Meta:
        model = ProcedureScale
        fields = ['id', 'victim', 'cincinatti', 'PROACS', 'RTS', 'MGAP', 'RACE']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(ProcedureScaleSerializer, self).to_representation(instance)


class ProcedureCirculationSerializer(ModelSerializer):
    class Meta:
        model = ProcedureCirculation
        fields = ['id', 'victim', 'temperature_monitoring', 'compression', 'tourniquet', 'pelvic_belt', 'venous_access',
                  'patch', 'ecg']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(ProcedureCirculationSerializer, self).to_representation(instance)


class EvaluationSerializer(ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'victim', 'hours', 'avds', 'ventilation', 'spo2', 'o2', 'etco2', 'pulse', 'ecg', 'skin',
                  'temperature', 'systolic_blood_pressure', 'diastolic_blood_pressure', 'pupils', 'pain', 'glycemia',
                  'news']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(EvaluationSerializer, self).to_representation(instance)


class SymptomSerializer(ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'victim', 'comments', 'image_path']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(SymptomSerializer, self).to_representation(instance)


class ProcedureRCPSerializer(ModelSerializer):
    class Meta:
        model = ProcedureRCP
        fields = ['id', 'witnessed', 'SBV_DAE', 'SIV_SAV', 'first_rhythm', 'nr_shocks', 'recovery', 'downtime',
                  'mechanical_compressions', 'performed', 'victim']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(ProcedureRCPSerializer, self).to_representation(instance)


class ProcedureVentilationSerializer(ModelSerializer):
    class Meta:
        model = ProcedureVentilation
        fields = ['id', 'victim', 'clearance', 'oropharyngeal', 'laryngeal_tube', 'endotracheal', 'laryngeal_mask',
                  'mechanical_ventilation', 'cpap']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(ProcedureVentilationSerializer, self).to_representation(instance)


class ProcedureProtocolSerializer(ModelSerializer):
    class Meta:
        model = ProcedureProtocol
        fields = ['id', 'immobilization', 'TEPH', 'SIV', 'VV_AVC', 'VV_coronary', 'VV_sepsis', 'VV_trauma', 'VV_PCR',
                  'victim']

    def to_representation(self, instance):
        self.fields['victim'] = VictimSerializer(read_only=True)
        return super(ProcedureProtocolSerializer, self).to_representation(instance)
