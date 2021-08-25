from decimal import Decimal

from rest_framework import generics

from . import models
from . import serializers


class UserListView(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    lookup_field = "username"  # using username in the url, and not pk
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
