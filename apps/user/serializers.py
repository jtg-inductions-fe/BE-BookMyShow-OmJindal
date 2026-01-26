from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import serializers as rest_serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user import constants as user_constants

User = get_user_model()


class SignUpSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for handling new user registration.

    This serializer manages the creation of new user accounts, ensuring
    password security through Django's standard validation framework and
    automated JWT token generation upon successful creation.
    """

    password = rest_serializers.CharField(write_only=True)
    confirm_password = rest_serializers.CharField(write_only=True)
    access = rest_serializers.CharField(read_only=True)
    refresh = rest_serializers.CharField(read_only=True)

    class Meta:
        """
        Meta options for SignUpSerializer.
        """

        model = User
        fields = ["name", "email", "password", "confirm_password", "access", "refresh"]

    def to_internal_value(self, data):
        """
        Normalize the email address before any validation occurs.
        """
        resource_data = data.copy()
        if "email" in resource_data:
            resource_data["email"] = resource_data["email"].lower().strip()
        return super().to_internal_value(resource_data)

    def validate_password(self, value):
        """
        Validation for password strength.
        """
        django_validate_password(value)
        return value

    def validate(self, attrs):
        """
        Validation for cross-field checks.
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError(user_constants.ErrorMessages.PASSWORD_MISMATCH)
        return attrs

    def create(self, validated_data):
        """
        Creates a new User instance using the custom UserManager
        and add JWT tokens.
        """
        validated_data.pop("confirm_password")
        try:
            # Create the user using the manager to ensure password hashing
            user = User.objects.create_user(**validated_data)
            # Generate refresh token
            refresh = RefreshToken.for_user(user)
            user.access = str(refresh.access_token)
            user.refresh = str(refresh)
            return user
        except IntegrityError:
            raise rest_serializers.ValidationError({user_constants.ErrorMessages.EMAIL_EXISTS})


class UserSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for user profile retrieval and updates with
    email as a read-only field.
    """

    class Meta:
        """
        Meta options for UserSerializer.
        """

        model = User
        fields = ["name", "email", "phone_number", "profile_picture", "city"]
        read_only_fields = ["email"]

    def to_internal_value(self, data):
        """
        Strictly enforces the defined field set.
        Raises:
            ValidationError: If fields not present in the serializer are provided.
        """
        unknown_fields = set(data.keys()) - set(self.fields.keys())
        if unknown_fields:
            raise rest_serializers.ValidationError(
                {field: user_constants.ErrorMessages.FIELD_NOT_ALLOWED for field in unknown_fields}
            )
        return super().to_internal_value(data)


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
        resource_data = data.copy()

        if "email" in resource_data:
            resource_data["email"] = resource_data["email"].lower().strip()

        return super().to_internal_value(resource_data)
