from decimal import Decimal

from rest_framework import generics

from . import models
from events.models import Event
from . import serializers

class UserListView(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    
    def total_distance_travelled(self):
        total_distance_query = Event.object.filter(custom_user=self.id)
        total_distance = Decimal(0.)
        total_distance = sum([obj.distance_travelled 
            for obj in total_distance_query])
        
        return sum(total_distance)
