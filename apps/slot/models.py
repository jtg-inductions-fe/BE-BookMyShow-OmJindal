from django.db import models
from django.core.validators import MinValueValidator

from apps.movie.models import Movie
from apps.cinema.models import Cinema
from apps.user.models import User


class Slot(models.Model):
    """
    Represents a specific movie screening time in a cinema hall.

    Attributes:
        price (int) : The ticket price for this specific show.
        start_time (datetime) : The date and time when the movie starts.
        end_time (datetime) : The date and time when the movie ends.
        movie (ForeignKey) : The movie being screened.
        cinema (ForeignKey) : The cinema hall where the movie is screened.
    """

    price = models.IntegerField(validators=[MinValueValidator(1)])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return f"Slot of {self.movie} in {self.cinema} between {self.start_time} and {self.end_time}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")


class Booking(models.Model):
    """
    Represents a reservation made by a user for a specific movie slot.

    Attributes:
        user (ForeignKey) : The user who is making the booking.
        slot (ForeignKey) : The specific showtime slot being booked.
        status (str) : The current state of the booking (Confirmed or Cancelled)
    """

    class BookingStatus(models.TextChoices):
        CONFIRMED = "CO", ("CONFIRMED")
        CANCELLED = "CA", ("CANCELLED")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=BookingStatus.choices)

    def __str__(self):
        return f"Booking of {self.user} for {self.slot}"


class Ticket(models.Model):
    """
    Represents an individual seat reserved under a booking.

    Attributes:
        seat_row (int) : The row number of the reserved seat.
        seat_column (int) : The column number in that specific row.
        booking (ForeignKey) : The booking to which this ticket belongs.
    """

    seat_row = models.IntegerField(validators=[MinValueValidator(1)])
    seat_column = models.IntegerField(validators=[MinValueValidator(1)])
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket of {self.booking} for seat {self.seat_row}-{self.seat_column}"

    def clean(self):
        from django.core.exceptions import ValidationError

        cinema = self.booking.slot.cinema
        if self.seat_row > cinema.rows:
            raise ValidationError(
                f"Seat row {self.seat_row} exceeds cinema capacity of {cinema.rows} rows."
            )
        if self.seat_column > cinema.seats_per_row:
            raise ValidationError(
                f"Seat column {self.seat_column} exceeds cinema capacity of {cinema.seats_per_row} seats per row."
            )
