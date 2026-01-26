from rest_framework import serializers as rest_serializers

from apps.booking import constants as booking_constants
from apps.booking import models as booking_models
from apps.cinema import models as cinema_models
from apps.slot import models as slot_models


class SeatSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for individual booked seats.

    Provides the specific coordinates of a seat within
    the cinema's grid layout.
    """

    class Meta:
        model = cinema_models.Seat
        fields = ["row_number", "seat_number"]


class CinemaLayoutSerializer(rest_serializers.ModelSerializer):
    """
    Serializer to provide the physical layout of a
    cinema with basic information.
    """

    city = rest_serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = cinema_models.Cinema
        fields = ["name", "city", "rows", "seats_per_row"]


class SlotDetailSerializer(rest_serializers.ModelSerializer):
    """
    Detailed serializer for a Movie Slot and its occupancy.

    Provides showtime data and a list of all seats already
    booked.

    Attributes:
        tickets (SerializerMethodField): A flattened list of all booked seats.
        cinema (CinemaLayoutSerializer): The physical details of the venue.
        movie (SlugRelatedField): The title of the movie being screened.
        language (SlugRelatedField): The name of the language in which the show is screened.
    """

    seats = rest_serializers.SerializerMethodField()
    cinema = CinemaLayoutSerializer()
    movie = rest_serializers.SlugRelatedField(read_only=True, slug_field="name")
    language = rest_serializers.SlugRelatedField(read_only=True, slug_field="name")

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
        Calculates availability for every seat in the cinema for this specific slot.
        """
        # 1. Get IDs of all seats already booked for this slot
        booked_seat_ids = set(
            booking_models.Ticket.objects.filter(
                booking__slot=slot, booking__status=booking_constants.BookingStatus.BOOKED
            ).values_list("cinema_seat_id", flat=True)
        )

        # 2. Fetch all physical seats for this cinema
        all_cinema_seats = slot.cinema.seats.all()

        # 3. Combine data into a flat list for the frontend
        return [
            {
                "id": seat.id,
                "row_number": seat.row_number,
                "seat_number": seat.seat_number,
                "is_available": seat.id not in booked_seat_ids,
            }
            for seat in all_cinema_seats
        ]
