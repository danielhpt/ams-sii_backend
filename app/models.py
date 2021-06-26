from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    team_leader = models.ForeignKey(
        User,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.team_leader.username


class TeamTechnician(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        related_name="team_technicians"
    )
    technician = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="technician_teams"
    )
    active = models.BooleanField()

    models.UniqueConstraint(
        fields=['team', 'technician'],
        name='unique1'
    )

    def __str__(self):
        return self.team.team_leader.username + self.technician.username + str(self.active)


class Occurrence(models.Model):
    occurrence_number = models.IntegerField()
    entity = models.CharField(max_length=50)
    mean_of_assistance = models.CharField(max_length=50)
    motive = models.CharField(max_length=50)
    number_of_victims = models.IntegerField()
    local = models.CharField(max_length=100)
    parish = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    team = models.ForeignKey(
        Team,
        related_name="occurrences",
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return str(self.id) + '' + str(self.occurrence_number)


class State(models.Model):
    state = models.CharField(max_length=25)

    def __str__(self):
        return self.state


class OccurrenceState(models.Model):
    occurrence = models.ForeignKey(
        Occurrence,
        on_delete=models.RESTRICT,
        related_name="occurrence_states"
    )
    state = models.ForeignKey(
        State,
        on_delete=models.RESTRICT,
        related_name="state_occurrences"
    )
    longitude = models.DecimalField(max_digits=15, decimal_places=7)
    latitude = models.DecimalField(max_digits=15, decimal_places=7)
    date_time = models.DateTimeField()

    models.UniqueConstraint(fields=['occurrence', 'state'], name='unique2')

    def __str__(self):
        return str(self.occurrence.id) + self.state.state


class TypeOfTransport(models.Model):
    type_of_transport = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type_of_transport


class NonTransportReason(models.Model):
    non_transport_reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.non_transport_reason


class Victim(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=25, null=True, blank=True)
    identity_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    circumstances = models.CharField(max_length=100, null=True, blank=True)
    disease_history = models.CharField(max_length=200, null=True, blank=True)
    allergies = models.CharField(max_length=100, null=True, blank=True)
    last_meal = models.CharField(max_length=50, null=True, blank=True)
    last_meal_time = models.DateTimeField(null=True, blank=True)
    usual_medication = models.CharField(max_length=100, null=True, blank=True)
    risk_situation = models.CharField(max_length=50, null=True, blank=True)
    medical_followup = models.BooleanField()
    health_unit_origin = models.CharField(max_length=100, null=True, blank=True)
    health_unit_destination = models.CharField(max_length=100, null=True, blank=True)
    episode_number = models.PositiveIntegerField()
    comments = models.CharField(max_length=400, null=True, blank=True)
    type_of_emergency = models.CharField(max_length=100, null=True, blank=True)
    SIV_SAV = models.DateTimeField(null=True, blank=True)
    type_of_transport = models.ForeignKey(
        TypeOfTransport,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    non_transport_reason = models.ForeignKey(
        NonTransportReason,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    occurrence = models.ForeignKey(
        Occurrence,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return str(self.id) + '-' + self.name


class Pharmacy(models.Model):
    victim = models.ForeignKey(
        Victim,
        on_delete=models.RESTRICT,
        related_name="pharmacies"
    )
    time = models.TimeField(null=True, blank=True)
    pharmacy = models.CharField(max_length=50, null=True, blank=True)
    dose = models.CharField(max_length=50, null=True, blank=True)
    route = models.CharField(max_length=50, null=True, blank=True)
    adverse_effect = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.pharmacy + '' + str(self.victim.id)


class ProcedureScale(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True
    )
    cincinatti = models.PositiveSmallIntegerField(null=True, blank=True)
    PROACS = models.PositiveSmallIntegerField(null=True, blank=True)
    RTS = models.PositiveSmallIntegerField(null=True, blank=True)
    MGAP = models.PositiveSmallIntegerField(null=True, blank=True)
    RACE = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.victim.id) + ' - Scale procedures'


class ProcedureCirculation(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True
    )
    temperature_monitoring = models.BooleanField()
    compression = models.BooleanField()
    tourniquet = models.BooleanField()
    pelvic_belt = models.BooleanField()
    venous_access = models.BooleanField()
    patch = models.BooleanField()
    ecg = models.BooleanField()

    def __str__(self):
        return str(self.victim.id) + '- Circulation procedures'


class Evaluation(models.Model):
    victim = models.ForeignKey(
        Victim,
        on_delete=models.RESTRICT,
        related_name="victim_evaluations"
    )
    hours = models.DateTimeField(),
    avds = models.IntegerField(null=True, blank=True)
    ventilation = models.PositiveSmallIntegerField(null=True, blank=True)
    spo2 = models.PositiveSmallIntegerField(null=True, blank=True)
    o2 = models.PositiveSmallIntegerField(null=True, blank=True)
    etco2 = models.PositiveSmallIntegerField(null=True, blank=True)
    pulse = models.PositiveSmallIntegerField(null=True, blank=True)
    ecg = models.BooleanField()
    skin = models.CharField(max_length=50, null=True, blank=True)
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    systolic_blood_pressure = models.PositiveSmallIntegerField(null=True, blank=True)
    diastolic_blood_pressure = models.PositiveSmallIntegerField(null=True, blank=True)
    pupils = models.CharField(max_length=50, null=True, blank=True)
    pain = models.PositiveSmallIntegerField(null=True, blank=True)
    glycemia = models.PositiveSmallIntegerField(null=True, blank=True)
    news = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.victim.id) + '' + str(self.hours)


class Symptom(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True
    )
    comments = models.CharField(max_length=400, null=True, blank=True)
    image_path = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.victim.id) + '- Symptoms'


class ProcedureRCP(models.Model):
    witnessed = models.BooleanField()
    SBV_DAE = models.DateTimeField(null=True, blank=True)
    first_rhythm = models.CharField(max_length= 25, null=True, blank=True)
    nr_shocks = models.PositiveIntegerField(null=True, blank=True)
    recovery = models.DateTimeField(null=True, blank=True)
    downtime = models.DateTimeField(null=True, blank=True)
    mechanical_compressions = models.PositiveIntegerField(null=True, blank=True)
    performed = models.BooleanField()
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True
    )

    def __str__(self):
        return str(self.victim.id) + '- RCP procedures'


class ProcedureVentilation(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True
    )
    clearance = models.BooleanField(null=True, blank=True)
    oropharyngeal = models.BooleanField(null=True, blank=True)
    laryngeal_tube = models.BooleanField(null=True, blank=True)
    endotracheal = models.BooleanField(null=True, blank=True)
    laryngeal_mask = models.BooleanField(null=True, blank=True)
    mechanical_ventilation = models.BooleanField(null=True, blank=True)
    cpap = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.victim.id) + '- Ventilation procedures'


class ProcedureProtocol(models.Model):
    immobilization = models.BooleanField()
    TEPH = models.BooleanField()
    SIV = models.BooleanField()
    VV_AVC = models.BooleanField()
    VV_coronary = models.BooleanField()
    VV_sepsis = models.BooleanField()
    VV_trauma = models.BooleanField()
    VV_PCR = models.BooleanField()
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True
    )

    def __str__(self):
        return str(self.victim.id) + '- Protocol procedures'
