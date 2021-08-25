from decimal import Decimal

from rest_framework import serializers

from events.models import Event
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def total_distance_travelled():
        total_distance_query = Event.objects.all()
        total_distance = Decimal(0.0)
        total_distance = sum([obj.distance_travelled for obj in total_distance_query])
        return sum(total_distance)

    # total_distance = total_distance_travelled()

    class Meta:
        model = models.CustomUser
        fields = (
            "email",
            "username",
            "total_carbon_saved",
        )
