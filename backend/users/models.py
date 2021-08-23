from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    total_carbon_saved = models.IntegerField(default=0)

    def __str__(self):
        return self.email
