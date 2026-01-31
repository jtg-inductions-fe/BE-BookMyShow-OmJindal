from django.db import models as db_models


class BookingConstants:
    """
    Centralized database-related constants for the Booking app.
    """

    STATUS_MAX_LENGTH = 1


class BookingStatus(db_models.TextChoices):
    """
    Defines the possible states of a booking.
    """

    BOOKED = "B", "Booked"
    CANCELLED = "C", "Cancelled"


class ErrorMessages:
    """
    Centralized error message constants for the Booking app.
    """

    # Creation Errors
    SLOT_CLOSED = "Booking is closed for this showtime as it has already started or ended."
    EMPTY_SEATS = "Please select at least one seat to proceed with the booking."
    DUPLICATE_SEATS = "Duplicate seats are not allowed for booking"

    # Cancellation Errors
    ALREADY_CANCELLED = "This booking has already been cancelled."
    PAST_SHOW_CANCEL = "Cannot cancel a booking for a show that has already started or finished."
