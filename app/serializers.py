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

    def update(self, instance, validated_data):
        validated_data = self.data.serializer.initial_data
        teamTechniciansOld = TeamTechnician.objects.filter(team_id=instance.id)
        teamTechniciansNew = validated_data.pop('technicians')

        for ttOld in teamTechniciansOld:
            for ttNew in teamTechniciansNew:
                if ttOld.technician_id == ttNew['id']:
                    if ttNew['active'] is not None:
                        ttOld.active = ttNew['active']
            ttOld.save()

        return instance


class OccurrenceSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Occurrence
        fields = ['id', 'occurrence_number', 'entity', 'mean_of_assistance', 'motive', 'number_of_victims', 'local',
                  'parish', 'municipality', 'team']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        del validated_data['id']
        del validated_data['states']
        del validated_data['victims']
        occurrence = Occurrence.objects.create(**validated_data)
        return occurrence


class VictimIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = ['id']


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

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        del validated_data['id']
        occurrenceState = OccurrenceState.objects.create(**validated_data)
        return occurrenceState


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
                  'type_of_emergency', 'type_of_transport', 'non_transport_reason', 'occurrence', 'SIV_SAV']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        del validated_data['id']
        if validated_data['type_of_transport']:
            validated_data['type_of_transport'] = TypeOfTransport.objects.get(
                pk=validated_data['type_of_transport']['id'])
        if validated_data['non_transport_reason']:
            validated_data['non_transport_reason'] = NonTransportReason.objects.get(
                pk=validated_data['non_transport_reason']['id'])
        victim = Victim.objects.create(**validated_data)
        return victim


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['id', 'time', 'pharmacy', 'dose', 'route', 'adverse_effect']


class PharmacyDetailSerializer(serializers.ModelSerializer):
    victim = VictimIdSerializer(read_only=True)

    class Meta:
        model = Pharmacy
        fields = ['id', 'time', 'pharmacy', 'dose', 'route', 'adverse_effect', 'victim']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        del validated_data['id']
        pharmacy = Pharmacy.objects.create(**validated_data)
        return pharmacy


class ProcedureScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureScale
        fields = ['cincinatti', 'PROACS', 'RTS', 'MGAP', 'RACE']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        procedureScale = ProcedureScale.objects.create(**validated_data)
        return procedureScale

    def update(self, instance, validated_data):
        instance.cincinatti = validated_data.get('cincinatti', instance.cincinatti)
        instance.PROACS = validated_data.get('PROACS', instance.PROACS)
        instance.RTS = validated_data.get('RTS', instance.RTS)
        instance.MGAP = validated_data.get('MGAP', instance.MGAP)
        instance.RACE = validated_data.get('RACE', instance.RACE)

        instance.save()

        return instance


class ProcedureCirculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureCirculation
        fields = ['temperature_monitoring', 'compression', 'tourniquet', 'pelvic_belt', 'venous_access', 'patch',
                  'ecg']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        procedureCirculation = ProcedureCirculation.objects.create(**validated_data)
        return procedureCirculation

    def update(self, instance, validated_data):
        instance.temperature_monitoring = validated_data.get('temperature_monitoring', instance.temperature_monitoring)
        instance.compression = validated_data.get('compression', instance.compression)
        instance.tourniquet = validated_data.get('tourniquet', instance.tourniquet)
        instance.pelvic_belt = validated_data.get('pelvic_belt', instance.pelvic_belt)
        instance.venous_access = validated_data.get('venous_access', instance.venous_access)
        instance.patch = validated_data.get('patch', instance.patch)
        instance.ecg = validated_data.get('ecg', instance.ecg)

        instance.save()

        return instance


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'hours', 'avds', 'ventilation', 'spo2', 'o2', 'etco2', 'pulse', 'ecg', 'skin', 'temperature',
                  'systolic_blood_pressure', 'diastolic_blood_pressure', 'pupils', 'pain', 'glycemia', 'news']


class EvaluationDetailSerializer(serializers.ModelSerializer):
    victim = VictimIdSerializer(read_only=True)

    class Meta:
        model = Evaluation
        fields = ['id', 'hours', 'avds', 'ventilation', 'spo2', 'o2', 'etco2', 'pulse', 'ecg', 'skin', 'temperature',
                  'systolic_blood_pressure', 'diastolic_blood_pressure', 'pupils', 'pain', 'glycemia', 'news', 'victim']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        del validated_data['id']
        evaluation = Evaluation.objects.create(**validated_data)
        return evaluation


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['comments', 'image_path']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        symptom = Symptom.objects.create(**validated_data)
        return symptom

    def update(self, instance, validated_data):
        instance.comments = validated_data.get('comments', instance.comments)
        instance.image_path = validated_data.get('image_path', instance.image_path)
        instance.save()

        return instance


class ProcedureRCPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureRCP
        fields = ['witnessed', 'SBV_DAE', 'first_rhythm', 'nr_shocks', 'recovery', 'downtime',
                  'mechanical_compressions', 'performed']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        procedureRCP = ProcedureRCP.objects.create(**validated_data)
        return procedureRCP

    def update(self, instance, validated_data):
        instance.witnessed = validated_data.get('witnessed', instance.witnessed)
        instance.SBV_DAE = validated_data.get('SBV_DAE', instance.SBV_DAE)
        instance.first_rhythm = validated_data.get('first_rhythm', instance.first_rhythm)
        instance.nr_shocks = validated_data.get('nr_shocks', instance.nr_shocks)
        instance.recovery = validated_data.get('recovery', instance.recovery)
        instance.downtime = validated_data.get('downtime', instance.downtime)
        instance.nr_shocks = validated_data.get('mechanical_compressions', instance.nr_shocks)
        instance.performed = validated_data.get('performed', instance.performed)

        instance.save()

        return instance


class ProcedureVentilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureVentilation
        fields = ['clearance', 'oropharyngeal', 'laryngeal_tube', 'endotracheal', 'laryngeal_mask',
                  'mechanical_ventilation', 'cpap']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        procedureVentilation = ProcedureVentilation.objects.create(**validated_data)
        return procedureVentilation

    def update(self, instance, validated_data):
        instance.clearance = validated_data.get('clearance', instance.clearance)
        instance.oropharyngeal = validated_data.get('oropharyngeal', instance.oropharyngeal)
        instance.laryngeal_tube = validated_data.get('laryngeal_tube', instance.laryngeal_tube)
        instance.endotracheal = validated_data.get('endotracheal', instance.endotracheal)
        instance.laryngeal_mask = validated_data.get('laryngeal_mask', instance.laryngeal_mask)
        instance.mechanical_ventilation = validated_data.get('mechanical_ventilation', instance.mechanical_ventilation)
        instance.cpap = validated_data.get('cpap', instance.cpap)

        instance.save()

        return instance


class ProcedureProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureProtocol
        fields = ['immobilization', 'TEPH', 'SIV', 'VV_AVC', 'VV_coronary', 'VV_sepsis', 'VV_trauma', 'VV_PCR']

    def create(self, validated_data):
        validated_data = self.data.serializer.initial_data
        procedureProtocol = ProcedureProtocol.objects.create(**validated_data)
        return procedureProtocol

    def update(self, instance, validated_data):
        instance.immobilization = validated_data.get('immobilization', instance.immobilization)
        instance.TEPH = validated_data.get('TEPH', instance.TEPH)
        instance.SIV = validated_data.get('SIV', instance.SIV)
        instance.VV_AVC = validated_data.get('VV_AVC', instance.VV_AVC)
        instance.VV_coronary = validated_data.get('VV_coronary', instance.VV_coronary)
        instance.VV_sepsis = validated_data.get('VV_sepsis', instance.VV_sepsis)
        instance.VV_trauma = validated_data.get('VV_trauma', instance.VV_trauma)
        instance.VV_PCR = validated_data.get('VV_PCR', instance.VV_PCR)

        instance.save()

        return instance


class VictimDetailsSerializer(serializers.ModelSerializer):
    type_of_transport = serializers.ReadOnlyField(source='type_of_transport.type_of_transport')
    non_transport_reason = serializers.ReadOnlyField(source='non_transport_reason.non_transport_reason')
    occurrence = OccurrenceSimplifiedSerializer(read_only=True)
    evaluations = EvaluationSerializer(read_only=True, many=True)
    pharmacies = PharmacySerializer(many=True, read_only=True)
    procedure_rcp = ProcedureRCPSerializer(read_only=True)
    procedure_ventilation = ProcedureVentilationSerializer(read_only=True)
    procedure_protocol = ProcedureProtocolSerializer(read_only=True)
    procedure_circulation = ProcedureCirculationSerializer(read_only=True)
    procedure_scale = ProcedureScaleSerializer(read_only=True)
    symptom = SymptomSerializer(read_only=True)

    class Meta:
        model = Victim
        fields = ['id', 'name', 'birthdate', 'age', 'gender', 'identity_number', 'address', 'circumstances',
                  'disease_history', 'allergies', 'last_meal', 'last_meal_time', 'usual_medication', 'risk_situation',
                  'medical_followup', 'health_unit_origin', 'health_unit_destination', 'episode_number', 'comments',
                  'type_of_emergency', 'type_of_transport', 'non_transport_reason', 'occurrence', 'evaluations',
                  'symptom', 'procedure_rcp', 'procedure_ventilation', 'procedure_protocol',
                  'procedure_circulation', 'procedure_scale', 'pharmacies']
