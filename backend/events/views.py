from rest_framework import permissions
from rest_framework import viewsets

from .models import Event
from .permissions import IsOwnerAndPrivateEvent
from .serializers import EventSerializer, CreateEventSerializer


# class EventViewSet(viewsets.ModelViewSet):
#    # TODO:Set up permissions
#    # Need to check about editing events (patch), only by user
#
#    def get_serializer_class(self):
#        if self.action == "create":
#            return CreateEventSerializer
#        else:
#            return EventSerializer
#
#    def get_queryset(self):
#        if self.action == "list":
#            if self.request.user.is_authenticated:
#                qs1 = Event.objects.filter(is_private=False)
#                qs2 = Event.objects.filter(custom_user=self.request.user.id)
#                qs = qs1.union(qs2).order_by("created")
#                return qs
#            else:
#                return Event.objects.filter(is_private=False)
#        if self.action == "retrieve":
#            if self.request.user.is_authenticated:
#                qs = Event.objects.filter(custom_user=self.request.user.id)
#                return qs
#            else:
#                return Event.objects.filter(is_private=False)
#        return Event.objects.filter(is_private=False)
#


class EventViewSet(viewsets.ModelViewSet):
    """
    # Viewset for events
        - Public events can be viewed by everyone including NONAUTHENTICATED USERS. But only editable by the owner.
        - Private events can only be viewed by the OWNER.
    """

    def get_queryset(self):
        if self.request.user.get("id"):
            qs1 = Event.objects.filter(is_private=False)
            qs2 = Event.objects.filter(custom_user=self.request.user.id)
            qs = qs1.union(qs2).order_by("created")
            return qs
        return Event.objects.filter(is_private=False)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEventSerializer
        else:
            return EventSerializer

    queryset = Event.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerAndPrivateEvent,
    ]
