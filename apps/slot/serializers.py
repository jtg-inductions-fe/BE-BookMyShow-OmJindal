from rest_framework import serializers
from django.db import transaction

from apps.slot.models import Slot, Booking, Ticket
from apps.cinema.serializers import CinemaSerializer
from apps.movie.serializers import MovieSerializer


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["seat_row", "seat_column"]


class SlotTicketSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()
    cinema = CinemaSerializer()
    movie = MovieSerializer()

    class Meta:
        model = Slot
        fields = [
            "id",
            "price",
            "start_time",
            "end_time",
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
    seats = TicketSerializer(many=True, write_only=True)

    class Meta:
        model = Booking
        fields = ["seats", "id", "status"]

    def validate(self, attrs):
        seats = attrs["seats"]

        seat_keys = [(s["seat_row"], s["seat_column"]) for s in seats]

        if len(seat_keys) != len(set(seat_keys)):
            raise serializers.ValidationError(
                {"seats": "Duplicate seats are not allowed"}
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        slot = self.context["slot"]
        user = request.user
        seats = validated_data.pop("seats")

        requested_seats = {(s["seat_row"], s["seat_column"]) for s in seats}

        with transaction.atomic():
            booked_seats = set(
                Ticket.objects.filter(
                    booking__slot=slot,
                    booking__status=Booking.BookingStatus.CONFIRMED,
                ).values_list("seat_row", "seat_column")
            )

            conflict = booked_seats & requested_seats
            if conflict:
                raise serializers.ValidationError(
                    {"seats": [f"{row}{col}" for row, col in conflict]}
                )

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
