from django.urls import include, path

urlpatterns = [
    # local apps
    path('users/', include('users.urls')),
    path('', include('events.urls')),

    # REST
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
