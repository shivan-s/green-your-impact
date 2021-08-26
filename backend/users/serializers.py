from rest_framework import serializers

from events.models import Event

# from events.serializers import EventSerializer
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = (
            "email",
            "username",
            "total_carbon_saved",
            # "total_distance_travelled",
        )


# class UserEventListSerializer(EventSerializer):
