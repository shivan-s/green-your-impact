from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import pytest

from users.models import CustomUser
from events.models import Event

# TODO: Date range?
# TODO: Set and Tear down isn't necessary
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
# TODO reorder list, detail/retrieve, create, edit, delete
class TestEvent(TestSetUp):
    def test_create_event_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot create an event
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
        request = self.client.post(url, data, format="json")
        filtered_query = Event.objects.filter(id=request.data.get("id"))
        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert filtered_query.count() == 0

    def test_create_event_authenticated(self):
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
        self.client.force_authenticate(user=self.user_1)
        request = self.client.post(url, data, format="json")
        filtered_query = Event.objects.filter(id=request.data["id"])
        assert request.status_code == status.HTTP_201_CREATED
        assert filtered_query.count() == 1
        assert filtered_query[0].description == data["description"]

    def test_list_event_public_unauthenticated(self):
        """
        Ensure public events can be viewed by an unauthenticated user
        """
        url = reverse("events-list")
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data) == 1
        assert request.data[0]["description"] == self.event_2_public.description

    def test_list_event_authenticated_user_1(self):
        """
        Authenticated user 1 can see their own private event and public events
        """
        url = reverse("events-list")
        self.client.force_authenticate(user=self.user_1)
        request = self.client.get(url)
        # set is used to ignore order
        user_1_description_set = {obj["description"] for obj in request.data}
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data) == 2
        assert user_1_description_set == {
            self.event_2_public.description,
            self.event_1_private.description,
        }

    def test_list_event_authenticated_user_2(self):
        """
        Authenticated user 2 cannot see user 1's private events but can see public events
        """
        url = reverse("events-list")
        self.client.force_authenticate(user=self.user_2)
        request = self.client.get(url)
        user_2_description_set = {obj["description"] for obj in request.data}
        assert request.status_code == status.HTTP_200_OK
        assert len(request.data) == 1
        assert user_2_description_set != {
            self.event_2_public.description,
            self.event_1_private.description,
        }
        assert request.data[0]["description"] == self.event_2_public.description

    def test_retrieve_event_unauthenticated_public(self):
        """
        Ensure public events are visible to an unauthenticated user
        """
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_2_public.description

    def test_retrieve_event_unauthenticated_private(self):
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url)
        # private event is not forbidden, it is hidden due to search query nature
        assert request.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_event_user_1_private(self):
        """
        Ensure User 1 can see their own private event
        """
        self.client.force_authenticate(user=self.user_1)
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_1_private.description

    def test_retrieve_event_user_1_public(self):
        """
        Ensure User 1 can see User 2's public event
        """
        self.client.force_authenticate(user=self.user_1)
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_2_public.description

    def test_retrieve_event_user_2_private(self):
        """
        Ensure User 2 cannot see User 1's private event
        """
        self.client.force_authenticate(user=self.user_2)
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_event_user_2_public(self):
        """
        Ensure User 2 cannot their own public event
        """
        self.client.force_authenticate(user=self.user_2)
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == self.event_2_public.description

    def test_edit_event_unauthenticated_public(self):
        """
        Unauthenicated user cannot edit a public event
        """
        data = {
            "is_private": False,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Change",
        }
        url = reverse("events-detail", args=[self.event_2_public.id])
        request = self.client.put(url, data, format="json")
        filtered_query = Event.objects.filter(id=self.event_2_public.id)
        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert filtered_query[0].description != data["description"]

    def test_edit_event_unauthenticated_private(self):
        """
        Unauthenticated user cannot edit a private event
        """
        data = {
            "is_private": False,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Change",
        }
        url = reverse("events-detail", args=[self.event_1_private.id])
        request = self.client.get(url, data, format="json")
        filtered_query = Event.objects.filter(id=self.event_1_private.id)
        # 404 instead of 403 since query does not show private events
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert filtered_query[0].description != data["description"]

    def test_edit_event_user_1_own_and_change_privacy(self):
        """
        User 1 can edit their own event and can change privacy from private to public
        """
        data = {
            "is_private": False,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Change",
        }
        url = reverse("events-detail", args=[self.event_1_private.id])
        self.client.force_authenticate(user=self.user_1)
        request = self.client.put(url, data, format="json")
        filtered_query = Event.objects.filter(id=self.event_1_private.id)
        assert request.status_code == status.HTTP_200_OK
        assert filtered_query[0].description == data["description"]
        # check public with unauthenticated user
        self.client.force_authenticate(user=None)
        self.client.get(url)
        assert request.status_code == status.HTTP_200_OK
        assert request.data["description"] == data["description"]

    def test_edit_event_user_1_other(self):
        """
        User 1 cannot edit User 2's event
        """
        data = {
            "is_private": True,
            "transport_type": "BIKE",
            "distance_travelled": 10.00,
            "description": "Test - Change",
        }
        url = reverse("events-detail", args=[self.event_2_public.id])
        self.client.force_authenticate(user=self.user_1)
        request = self.client.put(url, data, format="json")
        filtered_query = Event.objects.filter(id=self.event_2_public.id)
        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert filtered_query[0].description != data["description"]

    def test_delete_event(self):
        """
        Ensure event can only be deleted by the owner
        """
        pass
