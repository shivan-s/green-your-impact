from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "user",
            "transport_type",
            "distance_travelled",
            "description",
        )
        model = Event
