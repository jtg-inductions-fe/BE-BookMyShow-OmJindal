from django.core.exceptions import ValidationError
from django.db import models as db_models

from apps.base import models as base_models
from apps.booking import constants as booking_constants
from apps.cinema import models as cinema_models
from apps.slot import models as slot_models
from apps.user import models as user_models


class Booking(base_models.TimeStampedModel):
    """
    Represents a reservation made by a user for a specific movie slot.

    Attributes:
        user (ForeignKey) : The user who is making the booking.
        slot (ForeignKey) : The specific showtime (slot) being booked.
        status (str) : The current state of the booking (Booked or Cancelled).
    """

    user = db_models.ForeignKey(
        user_models.User, on_delete=db_models.CASCADE, related_name="bookings"
    )
    slot = db_models.ForeignKey(
        slot_models.Slot, on_delete=db_models.CASCADE, related_name="bookings"
    )
    status = db_models.CharField(
        max_length=booking_constants.BookingConstants.STATUS_MAX_LENGTH,
        choices=booking_constants.BookingStatus.choices,
        default=booking_constants.BookingStatus.BOOKED,
    )
    seats = db_models.ManyToManyField(cinema_models.Seat, related_name="bookings")

    def __str__(self):
        return f"Booking {self.id} by {self.user.email} for {self.slot}"

    def clean(self):
        """
        Validates seat availability for the booking.

        Ensures that none of the selected seats are already booked for the same
        showtime slot in another active booking.
        """

        if not self.pk:
            return

        # Check if this seat is already taken for this specific slot
        occupied = Booking.objects.filter(
            slot=self.slot,
            status=booking_constants.BookingStatus.BOOKED,
            seats__in=self.seats.all(),
        ).exclude(id=self.id)

        if occupied.exists():
            raise ValidationError(booking_constants.ErrorMessages.SEAT_ALREADY_OCCUPIED)
