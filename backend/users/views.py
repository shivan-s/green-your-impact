from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import generics

from . import models
from . import serializers


class UserListView(generics.ListAPIView):
    """
    Lists all users
    """

    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    """
    Retieves detailed view of a user by username
    """

    # lookup_field = "username"  # using username in the url, and not pk
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


#  def get(self, request, *args, **kwargs):
#      """
#      Return the total distance travelled based on user events
#      """
#      user_id = get_object_or_404(models.CustomUser, pk=kwargs.get("id"))
#      total_distance_query = Event.objects.filter(custom_user_id=user_id)
#      total_distance = Decimal(0.0)
#      total_distance = sum([obj.distance_travelled for obj in total_distance_query])
#      return Response(total_distance)
