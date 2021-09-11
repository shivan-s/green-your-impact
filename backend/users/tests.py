from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import pytest

from events.models import Event
from users.models import CustomUser


class TestSetUp(APITestCase):
    """
    Setting up 2 test users each with 1 event. 1 event is public and 1 is
    private
    """

    def setUp(self):
        # Setting up test users
        # - First Test User
        register_data_1 = {
            "username": "TestUser_1",
            "email": "test@testemail.com",
            "password": "tEsT1234@!",
        }
        # - Second Test User
        register_data_2 = {
            "username": "TestUser_2",
            "email": "test@testemail.com",
            "password": "tEsT1234@!",
        }
        # ** - keyword arguments
        self.user_1 = CustomUser.objects.create(**register_data_1)
        self.user_2 = CustomUser.objects.create(**register_data_2)

        # Setting up test events
        # - Private event liked to First Test User
        event_data_1_private = {
            "is_private": True,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Private",
        }
        # - Public event linked to Second Test User
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
        self.client.force_authenticate(user=None)
        self.user_1.delete()
        self.user_2.delete()
        self.event_1_private.delete()
        self.event_2_public.delete()
        return super().tearDown()


class TestCustomUser(TestSetUp):
    def test_create_account(self):
        """
        Ensure an account can be created
        """
        url = reverse("rest_register")
        data = {
            "username": "TestUser",
            "email": "test_x@testemail.com",
            "password1": "tEsT1234@!",
            "password2": "tEsT1234@!",
        }
        request = self.client.post(url, data, format="json")
        filtered_query = CustomUser.objects.filter(username=data["username"])
        assert request.status_code == status.HTTP_201_CREATED
        assert filtered_query.count() == 1
        assert filtered_query[0].username == data["username"]

    def test_detail_user_event_set_own_user(self):
        """
        Ensure the user can see all their events in the event_set, which is a
        nested serializer
        If this test passes then unauthenticated should be able to see public
        events in the event set
        """
        url = reverse("users-detail", args=[self.user_1.id])
        self.client.force_authenticate(user=self.user_1)
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data["event_set"]) == 1

    def test_detail_user_event_set_not_own_user(self):
        """
        Ensure private events cannot be viewed in the event set of a user
        User is authenticated as other user, so if this test passes, it should
        also be the case for an unauthenticated user
        """
        url = reverse("users-detail", args=[self.user_1.id])
        self.client.force_authenticate(user=self.user_2)
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data["event_set"]) == 0
