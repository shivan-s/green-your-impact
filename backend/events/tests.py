from django.urls import reverse
from rest_framework import status
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


# TODO: Build more tests: retrieve, edit, delete - also reorder
# TODO reorder list, detail, create, edit, delete
class TestEvent(TestSetUp):
    def test_create_event(self):
        """
        Ensure event can only be created by an authenticated user
        """
        # https://www.django-rest-framework.org/api-guide/routers/
        # on reverse names
        url = reverse("events-list")
        data = {
            "is_private": False,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test",
        }

        # Unauthenticated user cannot create an event
        request = self.client.post(url, data, format="json")
        assert request.status_code == status.HTTP_403_FORBIDDEN

        # Authenticated user can create an event
        self.client.force_authenticate(user=self.user_1)
        request = self.client.post(url, data, format="json")
        assert request.status_code == status.HTTP_201_CREATED
        filtered_query = Event.objects.filter(id=request.data["id"])
        assert filtered_query.count() == 1
        assert filtered_query[0].description == data["description"]

    def test_list_event(self):
        """
        Ensure public events can be viewed and not private events unless by the owner
        """
        url = reverse("events-list")

        # Unauthenticated user can see public events and not private events
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data) == 1
        assert request.data[0]["description"] == self.event_2_public.description

        # Authenticated user 1 can see their own private event
        self.client.force_authenticate(user=self.user_1)
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data) == 2
        # set is used to ignore order
        user_1_description_set = {obj["description"] for obj in request.data}
        assert user_1_description_set == {
            self.event_2_public.description,
            self.event_1_private.description,
        }

        # Authenticated user 2 cannot see user 1's private events
        self.client.force_authenticate(user=self.user_2)
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data) == 1
        user_2_description_set = {obj["description"] for obj in request.data}
        assert user_2_description_set != {
            self.event_2_public.description,
            self.event_1_private.description,
        }
        assert request.data[0]["description"] == self.event_2_public.description

    def test_retrieve_event(self):
        """
        Ensure public events can be viewed and not private events unless by the owners
        """
        # Unauthenticated user can see public events and not private events
        # - public event
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_2_public.description
        # - private event
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url)
        # private event is not forbidden, it is hidden due to search query nature
        assert request.status_code == status.HTTP_404_NOT_FOUND

        # Authenticated user 1 can see their own private event
        self.client.force_authenticate(user=self.user_1)
        # - user 1 private event
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_1_private.description

        # - public event
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_2_public.description

        # Authenticated user 2 cannot see user 1's private events
        self.client.force_authenticate(user=self.user_2)
        # - user 1 private event
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_404_NOT_FOUND

        # - public event
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_2_public.description

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
