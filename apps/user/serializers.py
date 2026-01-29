from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers as rest_serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user import constants as user_constants

User = get_user_model()


class SignUpSerializer(rest_serializers.ModelSerializer):
    """
    Serializer responsible for user registration and
    initial authentication token generation.

    Fields:
        name (str): Full name of the user.
        email (str): Unique email address used for authentication. Email is normalized
            (lowercased and trimmed) before validation.
        password (str): User password, validated using Django's password validator.
        confirm_password (str): Must match the password field for successful registration.
        access (str): JWT access token used for authenticated API requests.
        refresh (str): JWT refresh token used to obtain new access tokens.

    Responsibilities:
    - Normalizes email to lowercase and validates password strength
    - Ensures password and confirm_password match
    - Creates user using the custom create_user method of UserManager
    - Generates JWT refresh and access tokens
    - Returns tokens in response
    """

    confirm_password = rest_serializers.CharField(write_only=True)
    access = rest_serializers.CharField(read_only=True)
    refresh = rest_serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password", "confirm_password", "access", "refresh"]
        extra_kwargs = {
            "name": {"write_only": True},
            "email": {"write_only": True},
            "password": {"write_only": True},
        }

    def to_internal_value(self, data):
        """
        Normalize the email address before any validation occurs.
        """
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return super().to_internal_value(data)

    def validate_password(self, value):
        """
        Validation for password strength.
        """
        validate_password(value)
        return value

    def validate(self, attrs):
        """
        Validation for cross-field checks.
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError({"password": user_constants.ErrorMessages.PASSWORD_MISMATCH})
        return attrs

    def create(self, validated_data):
        """
        Creates a new User instance using the custom UserManager
        and add JWT tokens.
        """
        validated_data.pop("confirm_password")
        # Create the user using the manager to ensure password hashing
        user = User.objects.create_user(**validated_data)

        # Generate refresh token
        refresh = RefreshToken.for_user(user)
        user.access = str(refresh.access_token)
        user.refresh = str(refresh)

        return user


class UserSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user profile information.

    This serializer is used to return authenticated user profile data and
    allows partial updates to editable profile fields. The email field is
    read-only and cannot be modified.

    Fields:
        name (str): Full name of the user.
        email (str): Unique email address of the user. This field is
            read-only and cannot be updated.
        phone_number (str): Phone number of the user.
            Must follow valid phone number format.
        profile_picture (Image): Profile image uploaded by the user.
        city (City): Reference to the City model.
    """

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "profile_picture", "city"]
        read_only_fields = ["email"]


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token serializer for JWT-based authentication.

    Extends the standard SimpleJWT TokenObtainPairSerializer to ensure
    that email casing does not prevent a successful login.
    """

    def to_internal_value(self, data):
        """
        Normalize the email address before any validation occurs.
        """
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return super().to_internal_value(data)
