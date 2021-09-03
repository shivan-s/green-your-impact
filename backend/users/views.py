from rest_framework import viewsets
from rest_framework import generics

from .models import CustomUser
from events.models import Event
from .permissions import PrivateIsOwner
from .serializers import UserSerializer
from events.serializers import EventSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()


class UserEventListView(generics.ListAPIView):
    lookup_field = "uuid"
    serializer_class = EventSerializer
    permission_classes = [PrivateIsOwner]

    # TODO: Hide private events
    def get_queryset(self):
        #        qs_public = Event.objects.filter(is_private=False)
        #        qs_owner = Event.objects.filter(custom_user=self.request.user.id)
        #        qs_url = Event.objects.filter(custom_user=self.kwargs.get("pk"))
        #        qs = qs_public | qs
        return Event.objects.filter(custom_user=self.kwargs.get("pk"))
