from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListEvent.as_view()),
    path('<uuid:pk>/', views.DetailEvent.as_view()),
]
