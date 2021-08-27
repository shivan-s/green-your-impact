from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "custom_user")
    list_display = (
        "custom_user",
        "is_private",
        "id",
        "created",
        "last_edited",
        "distance_travelled",
    )
