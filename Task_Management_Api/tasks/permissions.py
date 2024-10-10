from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to access it.

    Methods:
        has_object_permission(request, view, obj):
            Returns True if the requesting user is the author of the object, False otherwise.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
    
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    Read-only permissions are allowed for any request.
    Methods:
        has_object_permission(request, view, obj): Checks if the request method is safe (read-only) or if the user is the author of the object.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    