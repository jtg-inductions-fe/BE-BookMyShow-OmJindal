from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework import serializers as rest_serializers

from apps.booking import constants as booking_constants
from apps.booking import models as booking_models
from apps.cinema import serializers as cinema_serializers


class BookingCreateSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for creating movie seat bookings for a specific showtime slot.

    Business Rules Enforced:
        - Prevents booking if showtime has already started.
        - Prevents empty seat selection.
        - Prevents duplicate seat selection.
        - Ensures seats belong to the cinema hosting the show.
        - Prevents booking already reserved seats.

    Context Requirements:
        - slot: Slot instance for which booking is being created.
        - request.user: Authenticated user creating the booking.

    Fields:
        id(int): Unique identifier of the booking.
        status(str): Current status of the booking.
        seats(list): List of seat IDs to be booked for the selected slot.
    """

    seats = rest_serializers.ListField(child=rest_serializers.IntegerField(), write_only=True)

    class Meta:
        model = booking_models.Booking
        fields = ["id", "status", "seats"]

    def _validate_showtime(self, slot):
        """
        Check if the show has already started
        """
        if timezone.now() >= slot.start_time:
            raise rest_serializers.ValidationError(booking_constants.ErrorMessages.SLOT_CLOSED)

    def _validate_empty_selection(self, seats):
        """
        Check if the seats is empty
        """
        if not seats:
            raise rest_serializers.ValidationError(booking_constants.ErrorMessages.EMPTY_SEATS)

    def _validate_duplicate_seats(self, seats):
        """
        Check if seats are duplicate
        """
        if len(seats) != len(set(seats)):
            raise rest_serializers.ValidationError(booking_constants.ErrorMessages.DUPLICATE_SEATS)

    def _validate_cinema_seats(self, slot, seats):
        """
        Check for invalid seats that does not belong to the cinema
        """
        cinema_seat_ids = [seat.id for seat in slot.cinema.seats.all()]
        invalid_seats = [seat for seat in seats if seat not in cinema_seat_ids]

        if invalid_seats:
            raise rest_serializers.ValidationError(
                {"seats": f"Seats {(invalid_seats)} do not belong to the cinema hosting this show."}
            )

    def _validate_seat_occupancy(self, slot, seats):
        """
        Check for seats if already booked
        """
        booked_seat_ids = [
            seat.id
            for seat in slot.cinema.seats.all()
            for booking in seat.bookings.all()
            if booking.status == booking_constants.BookingStatus.BOOKED
            and booking.slot_id == slot.id
        ]

        occupied_seats = [seat for seat in seats if seat in booked_seat_ids]

        if occupied_seats:
            raise rest_serializers.ValidationError(
                {"seats": f"Seats {(occupied_seats)} are already occupied."}
            )

    def validate(self, attrs):
        """
        Performs business logic validation for new bookings.

        Checks:
            1. Showtime: Prevents booking if the movie has already started.
            2. Selection: Ensures at least one seat is provided.
            3. Duplication: Prevents creation of duplicate seats.
            3. Cinema Check: If the seats belong to the cinema or not.
            4. Occupancy: Checks if the seats are already booked.
        """
        slot = self.context["slot"]
        seats = attrs.get("seats", [])

        self._validate_showtime(slot)
        self._validate_empty_selection(seats)
        self._validate_duplicate_seats(seats)
        self._validate_cinema_seats(slot, seats)
        self._validate_seat_occupancy(slot, seats)

        return attrs

    def create(self, validated_data):
        """
        Creates a booking and assigns selected seats atomically.
        """
        slot = self.context["slot"]
        user = self.context["request"].user
        seats = validated_data.pop("seats")

        with db_transaction.atomic():
            booking = booking_models.Booking.objects.create(
                user=user,
                slot=slot,
                status=booking_constants.BookingStatus.BOOKED,
            )
            booking.seats.add(*seats)
        return booking


class BookingHistorySerializer(rest_serializers.ModelSerializer):
    """
    Serializer used to represent booking history details for a user.

    Fields:
        id(int): Unique identifier of the booking.
        movie(str): Name of the movie associated with the booking.
        language(str): Language in which the movie is screened.
        cinema_name(str): Name of the cinema where the show is scheduled.
        cinema_address(str): Address of the cinema.
        cinema_city(str): City in which the cinema is located.
        start_time(datetime): Scheduled start time of the movie show.
        status(str): Current status of the booking (Booked / Cancelled).
        seats(list): List of seats associated with the booking containing
            row and seat number details.
    """

    movie = rest_serializers.CharField(source="slot.movie.name", read_only=True)
    cinema_name = rest_serializers.CharField(source="slot.cinema.name", read_only=True)
    cinema_city = rest_serializers.CharField(source="slot.cinema.city.name", read_only=True)
    start_time = rest_serializers.DateTimeField(source="slot.start_time", read_only=True)
    seats = cinema_serializers.SeatSerializer(many=True, read_only=True)

    class Meta:
        model = booking_models.Booking
        fields = [
            "id",
            "movie",
            "cinema_name",
            "cinema_city",
            "start_time",
            "status",
            "seats",
        ]


class BookingCancelSerializer(rest_serializers.ModelSerializer):
    """
    Serializer used to validate and process booking cancellation requests.

    Fields:
        id (int): Unique identifier of the booking.
        status (str): Current booking status. Updated to cancelled
            after successful validation.
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

    def update(self, instance, validated_data):
        """
        Applies the cancellation status during a PATCH request.
        """
        instance.status = booking_constants.BookingStatus.CANCELLED
        instance.save()
        return instance
