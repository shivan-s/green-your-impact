from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "is_private",
            "custom_user",
            "transport_type",
            "distance_travelled",
            "description",
        )
        model = Event


class CreateEventSerializer(EventSerializer):
    custom_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
