from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.user.serializers import (
    SignUpSerializer,
    UserProfileSerializer,
    ProfileUpdateSerializer,
)


class SignupView(CreateAPIView):
    """
    API view to create user's profile.
    """

    serializer_class = SignUpSerializer


class ProfileView(RetrieveUpdateAPIView):
    """
    API view to retrieve and update authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_serializer_class(self):
        """
        Return serializer based on HTTP method.
        """
        if self.request.method == "PATCH":
            return ProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        """
        Return the currently authenticated user.
        """
        return self.request.user
