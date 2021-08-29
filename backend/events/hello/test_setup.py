from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import pytest

from users.models import CustomUser


class TestSetUp(APITestCase):
    """
    Test cases
    """

    def setUp(self):
        """
        Setting up test data
        """
        register_url = reverse("rest_register")
        # First Test User
        register_data_1 = {
            "username": "TestUser_1",
            "email": "test@testemail.com",
            "password1": "tEsT1234@!",
            "password2": "tEsT1234@!",
        }
        # Second Test User
        register_data_2 = {
            "username": "TestUser_2",
            "email": "test@testemail.com",
            "password1": "tEsT1234@!",
            "password2": "tEsT1234@!",
        }
        CustomUser.objects.create(register_data_1)
        CustomUser.objects.create(register_data_2)
        # self.user = CustomUser.objects.get(username=register_data["username"])
        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        return super().setUp()


# def tearDown(self):
#     return super.tearDown()
