from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r"events", views.EventViewSet, "events")

# /api/v1/events/events
urlpatterns = [
    path("", include(router.urls)),
]
