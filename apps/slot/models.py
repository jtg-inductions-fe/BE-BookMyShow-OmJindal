from django.db import models
from django.core.exceptions import ValidationError

from apps.movie.models import Movie
from apps.cinema.models import Cinema
from apps.user.models import User
from apps.base.models import TimeStampedModel


class Slot(TimeStampedModel):
    """
    Represents a specific movie screening time in a cinema hall.

    Attributes:
        price (int) : The ticket price for this specific show.
        start_time (datetime) : The date and time when the movie starts.
        end_time (datetime) : The date and time when the movie ends.
        movie (ForeignKey) : The movie being screened.
        cinema (ForeignKey) : The cinema hall where the movie is screened.
    """

    price = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="slots_by_movie"
    )
    cinema = models.ForeignKey(
        Cinema, on_delete=models.CASCADE, related_name="slots_by_cinema"
    )

    def __str__(self):
        return f"Slot of {self.movie} in {self.cinema} between {self.start_time} and {self.end_time}"

    def clean(self):
        overlapping_slots = Slot.objects.exclude(pk=self.pk).filter(
            movie=self.movie,
            cinema=self.cinema,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if overlapping_slots.exists():
            raise ValidationError(
                "This slot overlaps with an existing slot for the same movie in this cinema."
            )

        running_time = self.end_time - self.start_time
        if running_time < self.movie.duration:
            raise ValidationError(
                "The running time of the slot must be greater than or equal to duration of the movie."
            )

        slot_start_date = self.start_time.date()
        if self.movie.release_date > slot_start_date:
            raise ValidationError(
                "The movie start_time cannot be set before movie release date."
            )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F("start_time")),
                name="slot_end_after_start",
            ),
            models.UniqueConstraint(
                fields=["movie", "cinema", "start_time"],
                name="unique_slot_per_cinema_and_movie",
            ),
        ]


class Booking(TimeStampedModel):
    """
    Represents a reservation made by a user for a specific movie slot.

    Attributes:
        user (ForeignKey) : The user who is making the booking.
        slot (ForeignKey) : The specific showtime slot being booked.
        status (str) : The current state of the booking (Confirmed or Cancelled)
    """

    class BookingStatus(models.TextChoices):
        CONFIRMED = "CONFIRMED", ("Confirmed")
        CANCELLED = "CANCELLED", ("Cancelled")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings_by_user"
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, related_name="bookings_by_slot"
    )
    status = models.CharField(
        max_length=20, choices=BookingStatus.choices, default=BookingStatus.CONFIRMED
    )

    def __str__(self):
        return f"Booking of {self.user} for {self.slot}"


class Ticket(TimeStampedModel):
    """
    Represents an individual seat reserved under a booking.

    Attributes:
        seat_row (int) : The row number of the reserved seat.
        seat_column (int) : The column number in that specific row.
        booking (ForeignKey) : The booking to which this ticket belongs.
    """

    seat_row = models.PositiveSmallIntegerField()
    seat_column = models.PositiveSmallIntegerField()
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="tickets_by_booking"
    )

    def __str__(self):
        return f"Ticket of {self.booking} for seat {self.seat_row}-{self.seat_column}"

    def clean(self):
        cinema = self.booking.slot.cinema
        if self.seat_row > cinema.rows:
            raise ValidationError(
                f"Seat row {self.seat_row} exceeds cinema capacity of {cinema.rows} rows."
            )
        if self.seat_column > cinema.seats_per_row:
            raise ValidationError(
                f"Seat column {self.seat_column} exceeds cinema capacity of {cinema.seats_per_row} seats per row."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["seat_row", "seat_column", "booking"],
                name="unique_seat_per_booking",
            )
        ]
