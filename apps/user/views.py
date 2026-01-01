from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.user.serializers import (
    SignUpSerializer,
    UserProfileSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
)

from apps.user.models import User

from apps.user.utils import generate_refresh_token, set_refresh_cookie


class SignupView(APIView):
    """
    API view to handle user registration.

    This view validates user signup data, creates a new user,
    generates JWT access and refresh tokens, and returns the
    access token along with user profile details.

    The refresh token is stored securely in an HTTP-only cookie.
    """

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = generate_refresh_token(user)

        response = Response(
            {
                "message": "Signup successfully",
                "access": str(tokens["access"]),
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

        set_refresh_cookie(response, tokens["refresh"])
        return response


class LoginView(APIView):
    """
    API view to handle user authentication (login).

    This view validates user credentials, generates JWT tokens,
    and returns an access token with user profile information.

    The refresh token is stored in an HTTP-only cookie.
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        tokens = generate_refresh_token(user)

        response = Response(
            {
                "message": "Login successfully",
                "access": str(tokens["access"]),
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

        set_refresh_cookie(response, tokens["refresh"])
        return response


class ProfileView(APIView):
    """
    API view to retrieve and update the authenticated user's profile.

    Access is restricted to authenticated users only.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "user": UserProfileSerializer(request.user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    API view to handle user logout.

    This view removes the refresh token stored in cookies,
    effectively logging the user out.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("refresh")
        return response


class CookieTokenRefreshView(APIView):
    """
    API view to generate new access and refresh token.

    It also blacklist the previous refresh token.
    """

    def post(self, request):
        old_refresh_token = request.COOKIES.get("refresh")

        if not old_refresh_token:
            return Response(
                {"error": "Refresh token not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(old_refresh_token)

            user_id = refresh["user_id"]
            user = User.objects.get(id=user_id)

            refresh.blacklist()

            tokens = generate_refresh_token(user)

            response = Response(
                {
                    "access": str(tokens["access"]),
                },
                status=status.HTTP_200_OK,
            )

            set_refresh_cookie(response, tokens["refresh"])
            return response

        except TokenError as e:
            return Response(
                {"error": "Token expired or invalid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
