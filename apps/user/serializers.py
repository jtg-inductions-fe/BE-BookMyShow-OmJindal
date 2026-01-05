from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles validation and creation of a new user account.
    The password field is write-only and is properly hashed
    using Django's `create_user` method.
    """

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            phone_number=validated_data["phone_number"],
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Validates user credentials using Django's authentication
    system and returns the authenticated user instance.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile information.

    Used to return non-sensitive user details such as
    name, email, and phone number.
    """

    class Meta:
        model = User
        fields = ["name", "email", "phone_number"]


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
        fields = ["name", "phone_number"]
