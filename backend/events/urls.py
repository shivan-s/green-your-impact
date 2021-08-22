from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListEvent.as_view()),
    path("<int:pk>/", views.DetailEvent.as_view()),
]
