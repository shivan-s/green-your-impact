from rest_framework import serializers

from events.models import Event
from .models import CustomUser


class UserEventSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="events-detail", read_only=True
    )

    # TODO Need to some how filter the nested serializer

    class Meta:
        fields = (
            "id",
            "url",
            "is_private",
            "transport_type",
            "distance_travelled",
            "description",
        )
        model = Event


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="users-detail", read_only=True
    )

    class Meta:
        lookup_field = "username"
        model = CustomUser
        fields = (
            "id",
            "url",
            "email",
            "username",
            "total_carbon_saved",
            "date_joined",
        )


class UserDetailSerializer(UserSerializer):
    # Ensures the event set is only present in the detail view for a user
    event_set = UserEventSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("event_set",)
