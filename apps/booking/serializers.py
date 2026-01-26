from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework import serializers as rest_serializers

from apps.booking import constants as booking_constants
from apps.booking import models as booking_models
from apps.cinema import models as cinema_models


class BookingCreateSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for handling atomic creation of movie bookings.
    """

    seats = rest_serializers.ListField(child=rest_serializers.IntegerField(), write_only=True)

    class Meta:
        model = booking_models.Booking
        fields = ["id", "status", "seats"]

    def validate(self, attrs):
        """
        Performs business logic validation for new bookings.

        Checks:
            1. Showtime: Prevents booking if the movie has already started.
            2. Selection: Ensures at least one seat is provided.
            3. Cinema Check: If the seats belong to the cinema or not.
            4. Occupancy: Verifies that none of the requested seats are
               already booked by another user for this specific slot.
        """
        slot = self.context["slot"]
        seats = attrs.get("seats", [])

        # 1. Check if the show has already started
        if timezone.now() >= slot.start_time:
            raise rest_serializers.ValidationError(booking_constants.ErrorMessages.SLOT_CLOSED)

        # 2. Check for empty selection
        if not seats:
            raise rest_serializers.ValidationError(booking_constants.ErrorMessages.EMPTY_SEATS)

        # 3. Check for invalid seats
        valid_seats = cinema_models.Seat.objects.filter(cinema_id=slot.cinema_id, id__in=seats)

        if len(valid_seats) != len(seats):
            raise rest_serializers.ValidationError(
                booking_constants.ErrorMessages.INVALID_CINEMA_SEAT
            )

        # 4. Check for seat overlap (Occupancy Check)
        occupied_seats = booking_models.Ticket.objects.filter(
            booking__slot=slot,
            booking__status=booking_constants.BookingStatus.BOOKED,
            cinema_seat__in=seats,
        ).values_list("cinema_seat_id", flat=True)

        if occupied_seats:
            raise rest_serializers.ValidationError(
                {"seats": f"Seats {list(occupied_seats)} are already occupied."}
            )

        return attrs

    def create(self, validated_data):
        """
        Persists the booking and associated tickets atomically.

        Uses an atomic transaction to ensure that if ticket creation fails
        (e.g., due to a database constraint), the booking record is not created.
        """
        slot = self.context["slot"]
        user = self.context["request"].user
        seats = validated_data.pop("seats")

        with db_transaction.atomic():
            # Create the booking
            booking = booking_models.Booking.objects.create(
                user=user,
                slot=slot,
                status=booking_constants.BookingStatus.BOOKED,
            )
            # Create all tickets
            booking_models.Ticket.objects.bulk_create(
                [booking_models.Ticket(booking=booking, cinema_seat_id=seat) for seat in seats]
            )
        return booking


class TicketSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for representing individual ticket seat info.
    """

    row = rest_serializers.SlugRelatedField(
        source="cinema_seat", read_only=True, slug_field="row_number"
    )
    column = rest_serializers.SlugRelatedField(
        source="cinema_seat", read_only=True, slug_field="seat_number"
    )

    class Meta:
        model = booking_models.Ticket
        fields = ["row", "column"]


class BookingHistorySerializer(rest_serializers.ModelSerializer):
    """
    Detailed serializer for user booking history.
    """

    movie = rest_serializers.SlugRelatedField(
        source="slot.movie", read_only=True, slug_field="name"
    )
    language = rest_serializers.SlugRelatedField(
        source="slot.language", read_only=True, slug_field="name"
    )
    cinema_name = rest_serializers.SlugRelatedField(
        source="slot.cinema", read_only=True, slug_field="name"
    )
    cinema_address = rest_serializers.SlugRelatedField(
        source="slot.cinema", read_only=True, slug_field="address"
    )
    cinema_city = rest_serializers.SlugRelatedField(
        source="slot.cinema.city", read_only=True, slug_field="name"
    )
    start_time = rest_serializers.DateTimeField(source="slot.start_time", read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = booking_models.Booking
        fields = [
            "id",
            "movie",
            "language",
            "cinema_name",
            "cinema_address",
            "cinema_city",
            "start_time",
            "status",
            "tickets",
        ]


class BookingCancelSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for booking cancellation.
    """

    class Meta:
        model = booking_models.Booking
        fields = ["id", "status"]

    def validate(self, attrs):
        """
        Verifies that the booking is eligible for cancellation.
        """
        # Ensure Booking is not already in cancelled state.
        if self.instance.status == booking_constants.BookingStatus.CANCELLED:
            raise rest_serializers.ValidationError(
                booking_constants.ErrorMessages.ALREADY_CANCELLED
            )

        # Ensure cancellation request is not made after shows start.
        if self.instance.slot.start_time <= timezone.now():
            raise rest_serializers.ValidationError(booking_constants.ErrorMessages.PAST_SHOW_CANCEL)

        return attrs
