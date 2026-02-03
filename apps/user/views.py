from rest_framework import generics as rest_generics
from rest_framework import permissions as rest_permissions

from apps.user import serializers as user_serializers


class SignupView(rest_generics.CreateAPIView):
    """
    API endpoint for registering new users and issuing authentication tokens.

    HTTP Method: POST
        Request Body:
                - name: User's full name.,
                - email: User's email address.
                - password: User's password.
                - confirm_password: User's confirm password.
        Response (201 Created):
                - name: User's full name.,
                - email: User's email address.
                - access: "<jwt_access_token>",
                - refresh: "<jwt_refresh_token>"
        Error :
            400 Bad Request:
                - user with this email already exists.
                - This password is too common.
                - This password is too short. It must contain at least 8 characters.
                - Passwords do not match.
    """

    serializer_class = user_serializers.SignUpSerializer


class ProfileView(rest_generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the authenticated user's profile.

    This view allows authenticated users to fetch their profile details
    and update allowed profile fields using partial updates.

    Authentication: JWTAuthentication:
        Requires a valid JWT access token.

    Permissions: IsAuthenticated:
        Only authenticated users can access this endpoint.

    Methods Allowed:
        GET:
            Retrieves the authenticated user's profile details.
                Response:
                    200 OK:
                        - name (str | null)
                        - email (str)
                        - phone_number (str | null)
                        - profile_picture (Image | null): User's profile image url.
                        - city (City | null): User's city reference id.
        PATCH
            Update specific profile fields.
                Request Body:
                    - name: User's full name.,
                    - profile_picture: User's profile picture.
                    - phone_number: User's phone number.
                    - city: User's city id.
                Response:
                    200 OK:
                        - name (str | None)
                        - email (str)
                        - phone_number (str | None):
                        - profile_picture (Image | None): User's profile image url.
                        - city (City | None): User's city reference id.
                Error:
                    401 Unauthorized:
                        - Token is expired
                        - Authentication credentials were not provided
                    400 Bad Request:
                        - Phone number should be exactly 10 numeric digits
    """

    serializer_class = user_serializers.UserSerializer
    permission_classes = [rest_permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        """
        Overrides the default behavior to return the currently logged-in user.
        """
        return self.request.user
