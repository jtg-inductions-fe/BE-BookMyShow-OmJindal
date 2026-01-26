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

    def __str__(self):
        """
        Returns a string representation including user and slot details.
        """

        return f"Booking {self.id} by {self.user.email} for {self.slot}"


class Ticket(base_models.TimeStampedModel):
    """
    Represents an individual seat reserved under a booking.

    Attributes:
        booking (ForeignKey) : The booking to which this ticket belongs.
        cinema_seat (ForeignKey) : The specific physical seat assigned to this ticket.
    """

    booking = db_models.ForeignKey(Booking, on_delete=db_models.CASCADE, related_name="tickets")
    cinema_seat = db_models.ForeignKey(
        cinema_models.Seat,
        on_delete=db_models.CASCADE,
        related_name="tickets",
    )

    class Meta:
        constraints = [
            db_models.UniqueConstraint(
                fields=["booking", "cinema_seat"],
                name="unique_ticket_per_booking",
            )
        ]

    def __str__(self):
        """
        Returns a string representation showing specific seat coordinates,
        """

        return f"Ticket of {self.booking} for seat {self.cinema_seat.row_number}-{self.cinema_seat.seat_number}"

    def clean(self):
        """
        Performs cross-field validation for seat availability and location.

        Validates:
            1. That the chosen seat actually belongs to the cinema hosting the slot.
            2. That the seat is not already associated with another 'Booked'
               transaction for the same showtime slot.

        Raises:
            ValidationError: If seat is in the wrong cinema or already occupied.
        """

        # Validation to ensure the seat belongs to the cinema where the slot is hosted
        if self.cinema_seat.cinema != self.booking.slot.cinema:
            raise ValidationError(booking_constants.ErrorMessages.INVALID_CINEMA_SEAT)

        # Check if this seat is already taken for this specific slot
        occupied = Ticket.objects.filter(
            booking__slot=self.booking.slot,
            cinema_seat=self.cinema_seat,
            booking__status=Booking.BookingStatus.BOOKED,
        ).exclude(booking=self.booking)

        if occupied.exists():
            raise ValidationError(booking_constants.ErrorMessages.SEAT_ALREADY_OCCUPIED)
