import uuid

from django.db import models

from users.models import CustomUser

class Event(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            )
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    BIKE = "BIKE"
    PUBLIC_TRANSPORT = "PUBL"
    WALK = "WALK"
    TRANSPORT_CHOICES = [
        (BIKE, "Bike"),
        (PUBLIC_TRANSPORT, "Public Transport"),
        (WALK, "Walk"),
    ]
    transport_type = models.CharField(
        max_length=4, choices=TRANSPORT_CHOICES, default=WALK
    )

    distance_travelled = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'{self.custom_user}'
