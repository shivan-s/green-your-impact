from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)
import pytest

from events.models import Event
from events.hello.test_setup import TestSetUp
from events.views import EventViewSet

# TODO: Test if Events can be created
class TestEvent(TestSetUp):
    def test_create_event(self):
        """
        Ensure event can only be created by an authenticated user
        """
        # factory = APIRequestFactory()
        view = EventViewSet.as_view({"post": "list"})
        url = reverse("events-list")
        data = {
            "is_private": "false",
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test",
        }
        request = self.client.post(url, data, format="json")
        # unauthenticated user
        assert request.status_code == status.HTTP_403_FORBIDDEN
        # authenticated user
        self.client.force_authenticate(user=self.user_1)
        request = self.client.post(url, data, format="json")
        assert request.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1
        assert Event.objects.get().description == data["description"]

    def test_list_event(self):
        """
        Ensure public events can be viewed 

    # Test unauthenticated user


# TODO: Test if the event can viewed

# TODO: check if the event is private

# TODO: check if the event can be deleted by the user ONLY

# class TestEventModel(TestCase):
#    @classmethod
#    def set_up(cls):
#        cls.user = "test_user"
#        cls.transport_type = "Bike"
#        cls.distance_travelled = 10.00
#        cls.description = "test description"
#
#        cls.test_event = Event.objects.create(
#            user=cls.user,
#            transport_type=cls.transport_type,
#            distance_travelled=cls.distance_travelled,
#            description=cls.description,
#        )
#
#    def test_user(self):
#        assert Event.objects.get(pk=0) == "test_user"
