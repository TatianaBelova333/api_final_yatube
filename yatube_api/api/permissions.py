from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsObjAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow authors of an object
    to edit/delete it. Assumes the model instance has an `author` attribute.
    Nonauthor users must be authenticated to able to view an object
    or a list of objects.

    """
    message = ("Editing or deleting other users'"
               "posts or comments is not allowed")

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
        )
