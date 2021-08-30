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
        CustomUser.objects.create(**register_data_1)  # ** - keyword arguments
        CustomUser.objects.create(**register_data_2)
        self.user = CustomUser.objects.get(username=register_data_1["username"])
        return super().setUp()


# def tearDown(self):
#     return super.tearDown()
