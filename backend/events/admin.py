from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "custom_user",
        "id",
        "created",
        "last_edited",
        "distance_travelled",
    )
