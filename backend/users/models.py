import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(blank=True, max_length=255)
    total_carbon_saved = models.IntegerField(default=0)

    def __str__(self):
        return self.username
