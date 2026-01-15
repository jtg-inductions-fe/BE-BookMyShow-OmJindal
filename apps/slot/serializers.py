from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

from apps.slot.models import Slot, Booking, Ticket
from apps.cinema.models import Cinema


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for individual movie tickets.

    Represents a booked seat using its row and column
    inside a cinema hall.
    """

    class Meta:
        model = Ticket
        fields = ["seat_row", "seat_column"]


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cinema information.
    """

    city = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Cinema
        fields = ["name", "city", "rows", "seats_per_row"]


class SlotTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for a movie slot along with its booked tickets.

    Includes:
    - Slot details (time and price)
    - Related movie and cinema information
    - All tickets booked under CONFIRMED bookings for the slot
    """

    tickets = serializers.SerializerMethodField()
    cinema = CinemaSerializer()
    movie = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Slot
        fields = [
            "id",
            "price",
            "start_time",
            "movie",
            "cinema",
            "tickets",
        ]

    def get_tickets(self, slot):
        tickets = []
        for booking in slot.bookings_by_slot.all():
            tickets.extend(booking.tickets_by_booking.all())

        return TicketSerializer(tickets, many=True).data


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to handle booking creation.

    Accepts seat details, validates seat uniqueness,
    checks availability, and creates a confirmed booking
    along with its tickets atomically.
    """

    seats = TicketSerializer(many=True, write_only=True)

    class Meta:
        model = Booking
        fields = ["seats", "id", "status"]

    def validate(self, attrs):
        seats = attrs["seats"]

        slot = self.context["slot"]
        cinema = slot.cinema

        if timezone.now() >= slot.start_time:
            raise serializers.ValidationError(
                {"detail": "Cannot book a slot that has already started or ended."}
            )

        if len(seats) == 0:
            raise serializers.ValidationError({"seats": "Cannot be empty."})

        seat_keys = [(s["seat_row"], s["seat_column"]) for s in seats]

        if len(seat_keys) != len(set(seat_keys)):
            raise serializers.ValidationError(
                {"seats": "Duplicate seats are not allowed"}
            )

        booked_seats = set(
            Ticket.objects.filter(
                booking__slot=slot,
                booking__status=Booking.BookingStatus.CONFIRMED,
            ).values_list("seat_row", "seat_column")
        )

        invalid_seats = booked_seats & set(seat_keys)

        conflict = []

        for row, column in seat_keys:
            if (row > cinema.rows) or (column > cinema.seats_per_row):
                conflict.append(
                    f"seat_row:{row}, seat_column:{column} exceeds cinema capacity of {cinema.rows} rows and {cinema.seats_per_row} columns"
                )
            if (row, column) in invalid_seats:
                conflict.append(
                    f"seat_row:{row}, seat_column:{column} is already booked."
                )

        if conflict:
            raise serializers.ValidationError({"seats": conflict})

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        slot = self.context["slot"]
        user = request.user
        seats = validated_data.pop("seats")

        requested_seats = {(s["seat_row"], s["seat_column"]) for s in seats}

        with transaction.atomic():
            booking = Booking.objects.create(
                user=user,
                slot=slot,
                status=Booking.BookingStatus.CONFIRMED,
            )

            Ticket.objects.bulk_create(
                [
                    Ticket(
                        booking=booking,
                        seat_row=row,
                        seat_column=col,
                    )
                    for row, col in requested_seats
                ]
            )

        return booking
