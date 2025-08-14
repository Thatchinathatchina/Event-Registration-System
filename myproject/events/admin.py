from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'capacity', 'cancelled', 'registrations_count')
    list_filter = ('cancelled',)
    search_fields = ('name',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'event', 'created_at')
    search_fields = ('full_name', 'email', 'event__name')
