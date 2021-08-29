from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import pytest

from users.models import CustomUser


class TestCustomUser(APITestCase):
    def test_create_account(self):
        """
        Ensure an account can be created
        """
        url = reverse("rest_register")
        data = {
            "username": "TestUser",
            "email": "test@testemail.com",
            "password1": "tEsT1234@!",
            "password2": "tEsT1234@!",
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.count() == 1
        assert CustomUser.objects.get().username == data["username"]


# TODO:  test listing user
# class TestCustomUser:
#    factor = APIRequestFactory()
#    request = factory.get("/users/users")


# TODO:  test retrieve users

# TODO: testing updating users if authenticated

# TODO: testing is user is set to private
