from rest_framework import permissions

class IsRecipient(permissions.BasePermission):
    """
    Permission class to check if the requesting user is the recipient of the object.

    This permission class inherits from `permissions.BasePermission` and overrides
    the `has_object_permission` method to ensure that the user making the request
    is the recipient of the object.

    Methods:
        has_object_permission(request, view, obj): Checks if the recipient of the
        object is the same as the user making the request.

        Args:
            request (HttpRequest): The HTTP request object.
            view (View): The view that is being accessed.
            obj (Model): The object being accessed.

        Returns:
            bool: True if the user is the recipient of the object, False otherwise.
    """
    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user