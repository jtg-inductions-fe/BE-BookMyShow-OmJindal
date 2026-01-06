from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.slot.models import Booking
from apps.slot.models import Slot
from apps.movie.models import Movie
from apps.cinema.models import Cinema

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
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password do not match"}
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


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "name", "duration", "poster", "description"]


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ["id", "name", "image", "city", "address"]


class SlotSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer()
    movie = MovieSerializer()

    class Meta:
        model = Slot
        fields = ["movie", "cinema", "start_time"]


class BookingHistorySerializer(serializers.ModelSerializer):
    slot = SlotSerializer()

    class Meta:
        model = Booking
        fields = ["slot", "status"]


class BookingCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = []

    def update(self, instance, validated_data):
        if instance.status == Booking.BookingStatus.CANCELLED:
            raise serializers.ValidationError(
                {"detail": "Booking is already cancelled."}
            )

        instance.status = Booking.BookingStatus.CANCELLED
        instance.save()
        return instance
