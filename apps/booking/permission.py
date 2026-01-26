from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.

    This permission assumes the model instance has a 'user' attribute
    that references a User instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Ensure the object has a 'user' attribute
        if not hasattr(obj, "user"):
            return False

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user
