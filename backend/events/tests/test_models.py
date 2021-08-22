from django.test import TestCase
import pytest

from events.models import Event


class TestEventModel(TestCase):
    @classmethod
    def set_up(cls):
        cls.user = "test_user"
        cls.transport_type = "Bike"
        cls.distance_travelled = 10.00
        cls.description = "test description"

        cls.test_event = Event.objects.create(
            user=cls.user,
            transport_type=cls.transport_type,
            distance_travelled=cls.distance_travelled,
            description=cls.description,
        )

    def test_user(self):
        assert Event.objects.get(pk=0) == "test_user"
