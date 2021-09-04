from rest_framework import viewsets
from rest_framework import generics

from .models import CustomUser
from events.models import Event
from .permissions import PrivateIsOwner
from .serializers import UserSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    # Viewset for users
    - List view shows users
    - Detail views of user will also their events
    """

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        else:
            return UserSerializer
