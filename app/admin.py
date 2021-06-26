from django.contrib import admin

from .models import *


class UserInline(admin.TabularInline):
    model = User


class TeamInLine(admin.TabularInline):
    model = Team


class TechnicianAdmin(admin.ModelAdmin):
    inlines = [
        UserInline
    ]

