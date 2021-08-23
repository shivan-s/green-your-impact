from django.urls import path

from . import views

urlpatterns = [
    path("events/", views.ListEvent.as_view()),
    path("events/<int:pk>/", views.DetailEvent.as_view()),
]
