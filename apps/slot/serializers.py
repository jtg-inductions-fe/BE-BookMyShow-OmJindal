from rest_framework import serializers as rest_serializers

from apps.booking import constants as booking_constants
from apps.cinema import serializers as cinema_serializers
from apps.slot import models as slot_models


class SlotDetailSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for detailed slot information along with movie
    and cinema including seat availability.

    Attributes:
        price(int): Ticket price for the slot.
        start_time(datetime): Show start date and time.
        language(str): Language of the movie screening.
        movie(str): Name of the movie being screened.
        cinema(CinemaLayoutSerializer): Cinema layout details including seating structure.
        seats(SerializerMethodField): List of all seats with availability status.
    """

    language = rest_serializers.SlugRelatedField(read_only=True, slug_field="name")
    movie = rest_serializers.SlugRelatedField(read_only=True, slug_field="name")
    cinema = cinema_serializers.CinemaLayoutSerializer()
    seats = rest_serializers.SerializerMethodField()

    class Meta:
        model = slot_models.Slot
        fields = [
            "price",
            "start_time",
            "language",
            "movie",
            "cinema",
            "seats",
        ]

    def get_seats(self, slot):
        """
        Computes seat availability for all seats in the cinema
        for the given slot.
        """
        booked_seat_ids = {
            seat.id
            for seat in slot.cinema.seats.all()
            for booking in seat.bookings.all()
            if booking.status == booking_constants.BookingStatus.BOOKED
            and booking.slot_id == slot.id
        }

        return cinema_serializers.SeatAvailabilitySerializer(
            slot.cinema.seats.all(),
            many=True,
            context={
                "booked_seat_ids": booked_seat_ids,
            },
        ).data
