from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import pytest

from users.models import CustomUser
from events.models import Event


class TestSetUp(APITestCase):
    """
    Setting up 2 test users each with 1 event. 1 event is public and 1 is private
    """

    def setUp(self):
        # Setting up test users
        register_url = reverse("rest_register")
        # First Test User
        register_data_1 = {
            "username": "TestUser_1",
            "email": "test@testemail.com",
            "password": "tEsT1234@!",
        }
        # Second Test User
        register_data_2 = {
            "username": "TestUser_2",
            "email": "test@testemail.com",
            "password": "tEsT1234@!",
        }
        # ** - keyword arguments
        self.user_1 = CustomUser.objects.create(**register_data_1)
        self.user_2 = CustomUser.objects.create(**register_data_2)
        event_data_1_private = {
            "is_private": True,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Private",
        }
        event_data_2_public = {
            "is_private": False,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Public",
        }
        self.event_1_private = Event.objects.create(
            custom_user=self.user_1, **event_data_1_private
        )
        self.event_2_public = Event.objects.create(
            custom_user=self.user_2, **event_data_2_public
        )
        return super().setUp()

    def tearDown(self):
        self.user_1.delete()
        self.user_2.delete()
        self.event_1_private.delete()
        self.event_2_public.delete()
        return super().tearDown()


class TestEvent(TestSetUp):
    def test_create_event(self):
        """
        Ensure event can only be created by an authenticated user
        """
        url = reverse("events-list")
        data = {
            "is_private": False,
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
        __import__("pdb").set_trace()
        assert request.status_code == status.HTTP_201_CREATED
        filtered_query = Event.objects.filter(id=request.data["id"])
        assert filtered_query.count() == 1
        assert filtered_query[0].description == data["description"]

    # TODO: Build more tests
    def test_list_event(self):
        """
        Ensure public events can be viewed and not private events unless by the owner
        """
        # Unauthenticated user can see public events and not private event
        # Authenticated user 1 can see it's own private event
        # Authenticated user 2 cannot see user 1's private events
        pass

    def test_retrieve_event(self):
        """
        Ensure public events can be viewed and not private events unless by the owners
        """
        pass

    def test_edit_event(self):
        """
        Ensure event can only be edited by the owner
        """
        pass

    def test_delete_event(self):
        """
        Ensure event can only be deleted by the owner
        """
        pass
