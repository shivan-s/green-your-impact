from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to see own private events
    """

    message = "You do not have permission to edit/delete this  event"

    def has_object_permission(self, request, view, obj):
        """
        Owner can only edit/delete the event
        """
        if request.method in permissions.SAFE_METHODS:
            # private events should be stopped at the level of the query but
            # this is here for extra security
            if obj.is_private == True:
                if obj.custom_user == request.user:
                    return True
                else:
                    return False
            else:
                return True
        else:
            if obj.custom_user == request.user:
                return True
            else:
                return False
