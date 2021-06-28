from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Team(models.Model):
    def __str__(self):
        if self.team_technicians.filter(team_leader=True)[0]:
            return str(self.id) + ' - ' + self.team_technicians.filter(team_leader=True)[0].technician.get_username()
        return str(self.id)


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
    active = models.BooleanField(default=True)
    team_leader = models.BooleanField(default=False)

    models.UniqueConstraint(
        fields=['team', 'technician'],
        name='unique1'
    )

    def __str__(self):
        if self.active:
            active = ' active: 1'
        else:
            active = ' active: 0'
        if self.team_leader:
            team_leader = ' leader: 1'
        else:
            team_leader = ' leader: 0'
        return str(self.team.id) + ' - ' + self.technician.get_username() + active + team_leader


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
        return str(self.id) + ' - ' + str(self.occurrence_number)


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
        return str(self.occurrence.id) + ' - ' + self.state.state


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
        on_delete=models.RESTRICT,
        related_name='victims'
    )

    def __str__(self):
        if self.name:
            return str(self.id) + ' - ' + self.name
        return str(self.id)


class Pharmacy(models.Model):
    victim = models.ForeignKey(
        Victim,
        on_delete=models.RESTRICT,
        related_name="pharmacies"
    )
    time = models.TimeField(null=True, blank=True)
    pharmacy = models.CharField(max_length=50)
    dose = models.CharField(max_length=50, null=True, blank=True)
    route = models.CharField(max_length=50, null=True, blank=True)
    adverse_effect = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Pharmacies"

    def __str__(self):
        return str(self.victim.id) + ' - ' + self.pharmacy


class ProcedureScale(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True,
        related_name='procedure_scale'
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
        primary_key=True,
        related_name='procedure_circulation'
    )
    temperature_monitoring = models.BooleanField()
    compression = models.BooleanField()
    tourniquet = models.BooleanField()
    pelvic_belt = models.BooleanField()
    venous_access = models.BooleanField()
    patch = models.BooleanField()
    ecg = models.BooleanField()

    def __str__(self):
        return str(self.victim.id) + ' - Circulation procedures'


class Evaluation(models.Model):
    victim = models.ForeignKey(
        Victim,
        on_delete=models.RESTRICT,
        related_name="evaluations"
    )
    hours = models.DateTimeField()
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
    pain = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    glycemia = models.PositiveSmallIntegerField(null=True, blank=True)
    news = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.victim.id) + ' - ' + str(self.hours)


class Symptom(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True,
        related_name='symptom'
    )
    comments = models.CharField(max_length=400, null=True, blank=True)
    image_path = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.victim.id) + ' - Symptoms'


class ProcedureRCP(models.Model):
    witnessed = models.BooleanField(default=False)
    SBV_DAE = models.DateTimeField(null=True, blank=True, default=datetime.now)
    first_rhythm = models.CharField(max_length=25, null=True, blank=True)
    nr_shocks = models.PositiveIntegerField(null=True, blank=True)
    recovery = models.DateTimeField(null=True, blank=True)
    downtime = models.DateTimeField(null=True, blank=True)
    mechanical_compressions = models.PositiveIntegerField(null=True, blank=True)
    performed = models.BooleanField(default=False)
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True,
        related_name='procedure_rcp'
    )

    def __str__(self):
        return str(self.victim.id) + ' - RCP procedures'


class ProcedureVentilation(models.Model):
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True,
        related_name='procedure_ventilation'
    )
    clearance = models.BooleanField(default=False)
    oropharyngeal = models.BooleanField(default=False)
    laryngeal_tube = models.BooleanField(default=False)
    endotracheal = models.BooleanField(default=False)
    laryngeal_mask = models.BooleanField(default=False)
    mechanical_ventilation = models.BooleanField(default=False)
    cpap = models.BooleanField(default=False)

    def __str__(self):
        return str(self.victim.id) + ' - Ventilation procedures'


class ProcedureProtocol(models.Model):
    immobilization = models.BooleanField(default=False)
    TEPH = models.BooleanField(default=False)
    SIV = models.BooleanField(default=False)
    VV_AVC = models.BooleanField(default=False)
    VV_coronary = models.BooleanField(default=False)
    VV_sepsis = models.BooleanField(default=False)
    VV_trauma = models.BooleanField(default=False)
    VV_PCR = models.BooleanField(default=False)
    victim = models.OneToOneField(
        Victim,
        on_delete=models.RESTRICT,
        primary_key=True,
        related_name='procedure_protocol'
    )

    def __str__(self):
        return str(self.victim.id) + ' - Protocol procedures'
