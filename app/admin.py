from django.contrib import admin

from .models import *

admin.site.site_header = "Sireph Administrator Page"


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


class VictimAdmin(admin.ModelAdmin):
    inlines = [
        ProcedureRCPInline,
        ProcedureVentilationInline,
        ProcedureCirculationInline,
        ProcedureProtocolInline,
        ProcedureScaleInline,
        SymptomInline,
        PharmacyInline,
    ]


class OccurrenceAdmin(admin.ModelAdmin):
    pass


class OccurrenceStateAdmin(admin.ModelAdmin):
    pass


class StateAdmin(admin.ModelAdmin):
    pass


class NonTransportReasonAdmin(admin.ModelAdmin):
    pass


class TypeOfTransportAdmin(admin.ModelAdmin):
    pass


class EvaluationAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Victim, VictimAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(OccurrenceState, OccurrenceAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Pharmacy)
admin.site.register(ProcedureScale)
admin.site.register(ProcedureCirculation)
admin.site.register(ProcedureProtocol)
admin.site.register(ProcedureVentilation)
admin.site.register(ProcedureRCP)
admin.site.register(NonTransportReason, NonTransportReasonAdmin)
admin.site.register(TypeOfTransport, TypeOfTransportAdmin)
admin.site.register(Symptom)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Team, TeamAdmin)
