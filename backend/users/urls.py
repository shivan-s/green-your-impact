from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet, "users")

# /api/v1/users/users
urlpatterns = [
    path("", include(router.urls)),
    path(
        "<str:username>/", views.UserNameView.as_view(), name="username_view"
    ),
]
