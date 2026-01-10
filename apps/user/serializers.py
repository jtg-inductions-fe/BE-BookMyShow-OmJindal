from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles validation and creation of a new user account.
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "password", "confirm_password"]

    def validate(self, attrs):
        email = attrs.get("email")
        email = email.lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Already exist"})

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )

        validate_password(password)
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile information.

    Used to return non-sensitive user details such as
    name, email, and phone number.
    """

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "profile_picture"]
        read_only_fields = fields


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile details.

    Allows partial updates to user attributes such as
    name and phone number.
    """

    def to_internal_value(self, data):
        unknown_fields = set(data.keys()) - set(self.fields.keys())
        if unknown_fields:
            raise serializers.ValidationError(
                {field: "This field is not allowed" for field in unknown_fields}
            )
        return super().to_internal_value(data)

    class Meta:
        model = User
        fields = ["name", "phone_number", "profile_picture"]
