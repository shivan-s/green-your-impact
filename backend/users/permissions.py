from rest_framework import permissions


class PrivateIsOwner(permissions.BasePermission):
    """
    Custom permission to allow owner to view events from user view
    """

    message = "You do not have permission to view this event"

    def has_permission(self, request, view):
        return request.method == "GET"

    def has_object_permission(self, request, view, obj):
        __import__("pdb").set_trace()
        if obj.is_private:
            return obj.custom_user == request.user
        else:
            return True
