from rest_framework import permissions
from rest_framework import viewsets

from .models import Event
from .permissions import IsOwner
from .serializers import EventSerializer, CreateEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    # Viewset for events
    - Public events can be viewed by everyone including unauthenticated users. But only editable by the owner.
    - Private events can only be viewed by the owner.
    """

    def get_queryset(self):
        qs = Event.objects.filter(is_private=False) | Event.objects.filter(
            custom_user=self.request.user.id
        )
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEventSerializer
        else:
            return EventSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
