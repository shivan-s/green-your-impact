from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.UserListView.as_view()),
    path("<uuid:id>/", views.UserDetailView.as_view()),
]
