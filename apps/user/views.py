from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from apps.user.serializers import (
    SignUpSerializer,
    UserProfileSerializer,
    ProfileUpdateSerializer,
)


class SignupView(CreateAPIView):
    """
    API view to create user's profile and return
    JWT refresh and access tokens
    """

    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


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
