from django.db import models as db_models


class BookingStatus(db_models.TextChoices):
    """
    Defines the possible states of a booking.
    """

    BOOKED = "B", "Booked"
    CANCELLED = "C", "Cancelled"


class ErrorMessages:
    """
    Constants for defining errors.
    """

    # Creation Errors
    SLOT_CLOSED = "Booking is closed for this showtime as it has already started or ended."
    EMPTY_SEATS = "Please select at least one seat to proceed with the booking."
    SEAT_ALREADY_OCCUPIED = "One or more selected seats are already booked for this show."
    INVALID_CINEMA_SEAT = (
        "One or more selected seats do not belong to the cinema hosting this show."
    )

    # Cancellation Errors
    ALREADY_CANCELLED = "This booking has already been cancelled."
    PAST_SHOW_CANCEL = "Cannot cancel a booking for a show that has already started or finished."


class BookingConstants:
    """
    Database configuration for the Booking app.
    """

    STATUS_MAX_LENGTH = 1
