from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone_number", "password"]

        def create(self, validated_data):
            return User.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                name=validated_data["name"],
                phone_number=validated_data["phone_number"],
            )


class LoginSerializer(serializers.Serializer):
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
    class Meta:
        model = User
        fields = {"id", "name", "email", "phone_number"}


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {"name", "phone_number"}
