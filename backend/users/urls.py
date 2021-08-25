from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.UserListView.as_view()),
    path("<str:username>/", views.UserDetailView.as_view()),
]
