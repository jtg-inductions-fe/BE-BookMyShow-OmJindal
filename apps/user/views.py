from rest_framework import generics as rest_generics
from rest_framework import permissions as rest_permissions

from apps.user import serializers as user_serializers


class SignupView(rest_generics.CreateAPIView):
    """
    Register a new user and receive authentication tokens.

    This endpoint creates a new user record in the database. Upon successful
    registration, it automatically generates and returns a JSON Web Token (JWT)
    pair (access and refresh), allowing the user to be logged in immediately.
    """

    serializer_class = user_serializers.SignUpSerializer


class ProfileView(rest_generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update authenticated user's profile.

    Permissions:
        - IsAuthenticated: Only users with a valid JWT token can access this view.

    Methods Allowed:
        - GET: Retrieve profile details.
        - PATCH: Update specific profile fields.
    """

    serializer_class = user_serializers.UserSerializer
    permission_classes = [rest_permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        """
        Overrides the default behavior to return the currently logged-in user.
        """
        return self.request.user
