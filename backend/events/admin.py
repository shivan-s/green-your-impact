from django.contrib import admin

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
            'custom_user',
            'created',
            'last_edited',
            'distance_travelled',
            )
