from rest_framework import permissions


class IsOwnerAndPrivateEvent(permissions.BasePermission):
    """
    Custom permission to allow users to see own private events
    """

    message = "You do not have permission to view this event"

    def has_object_permission(self, request, view, obj):
        """
        Owner of event can see/edit/delete their event
        """
        __import__("pdb").set_trace()
        if obj.is_private == False:
            # Public Events
            return True
        elif obj.is_private == True and obj.custom_user == request.user.id:
            # Grant access since owner
            return True
        else:
            # Decline access to private events
            return False
