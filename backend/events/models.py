from django.db import models


class Event(models.Model):
    user = models.CharField(max_length=200)

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
    # carbon_saved = models.DecimalField()
    description = models.TextField()

    def __str__(self):
        return self.user
