from rest_framework import serializers

from .models import Event


class CustomUserNameField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.custom_user}"


class EventSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="events-detail", read_only=True
    )
    custom_user = serializers.HyperlinkedRelatedField(
        view_name="users-detail", read_only=True
    )
    custom_user_name = CustomUserNameField(source="*", read_only=True)

    class Meta:
        fields = (
            "id",
            "url",
            "custom_user",
            "custom_user_name",
            "is_private",
            "transport_type",
            "distance_travelled",
            "description",
        )
        model = Event


class CreateEventSerializer(EventSerializer):
    custom_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
