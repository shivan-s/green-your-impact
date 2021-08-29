from django.urls import include, path

urlpatterns = [
    # local apps
    path("users/", include("users.urls")),
    path("events/", include("events.urls")),
    # rest_auth, no longer maintained
    # path("rest-auth/", include("rest_auth.urls")),
    # path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
