from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


from .models import *


admin.site.site_header = "Sireph Administrator Page"


TokenAdmin.raw_id_fields = ['user']


class TokenInline(admin.StackedInline):
    model = Token


class UserAdmin(AuthUserAdmin):
    inlines = [TokenInline]


class TeamTechnicianInline(admin.TabularInline):
    model = TeamTechnician


class ProcedureScaleInline(admin.StackedInline):
    model = ProcedureScale


class ProcedureCirculationInline(admin.StackedInline):
    model = ProcedureCirculation


class ProcedureProtocolInline(admin.StackedInline):
    model = ProcedureProtocol


class ProcedureVentilationInline(admin.StackedInline):
    model = ProcedureVentilation


class ProcedureRCPInline(admin.StackedInline):
    model = ProcedureRCP


class SymptomInline(admin.StackedInline):
    model = Symptom


class PharmacyInline(admin.TabularInline):
    model = Pharmacy


class EvaluationInline(admin.TabularInline):
    model = Evaluation


class VictimAdmin(admin.ModelAdmin):
    inlines = [
        EvaluationInline,
        SymptomInline,
        ProcedureRCPInline,
        ProcedureVentilationInline,
        ProcedureCirculationInline,
        ProcedureProtocolInline,
        ProcedureScaleInline,
        PharmacyInline,
    ]


class OccurrenceStateInline(admin.TabularInline):
    model = OccurrenceState


class OccurrenceAdmin(admin.ModelAdmin):
    inlines = [
        OccurrenceStateInline
    ]


class TeamAdmin(admin.ModelAdmin):
    inlines = [
        TeamTechnicianInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Victim, VictimAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(State)
admin.site.register(NonTransportReason)
admin.site.register(TypeOfTransport)
admin.site.register(Team, TeamAdmin)
