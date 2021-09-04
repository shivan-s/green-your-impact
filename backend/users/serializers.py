from rest_framework import serializers

from events.models import Event
from .models import CustomUser


class UserEventSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="events-detail", read_only=True
    )

    class Meta:
        fields = (
            "url",
            "is_private",
            "transport_type",
            "distance_travelled",
            "description",
        )
        model = Event


# TODO: Combine this with UserSerializer so not violating DRY
class UserDetailSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="users-detail", read_only=True)
    event_set = UserEventSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "url",
            "email",
            "username",
            "total_carbon_saved",
            "event_set",
        )


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="users-detail", read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "url",
            "email",
            "username",
            "total_carbon_saved",
        )
