from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from apps.slot.models import Slot, Booking, Ticket
from apps.base.tests.utils import BaseTestUtils


class SlotModelTests(BaseTestUtils):
    """
    SlotModelTests to test Slot model
    """

    def setUp(self):
        """
        Creating cinema and movie for slot tests
        """
        super().setUp()
        self.create_cinema()
        self.create_movie()

    def test_create_valid_slot(self):
        """
        Slot should be valid when correct details are provided
        """
        slot = Slot(**self.slot, cinema=self.cinema_object, movie=self.movie_object)

        slot.full_clean()
        slot.save()

        self.assertEqual(slot.start_time, self.slot.get("start_time"))

    def test_missing_cinema_or_movie(self):
        """
        Missing cinema or movie raise ObjectDoesNotExist error
        """
        slot = Slot(**self.slot)

        with self.assertRaises(ObjectDoesNotExist):
            slot.full_clean()

    def test_missing_required_fields(self):
        """
        Missing slot details raise ValueError
        """
        slot = Slot(cinema=self.cinema_object, movie=self.movie_object)

        with self.assertRaises(ValueError):
            slot.full_clean()

    def test_slot_must_be_unique(self):
        """
        Duplicate slot raise IntegrityError
        """
        self.create_slot()

        with self.assertRaises(IntegrityError):
            self.create_slot()

    def test_invalid_start_time_type(self):
        """
        start_time should have a valid format
        """
        slot = Slot(
            **{**self.slot, "start_time": "abc"},
            cinema=self.cinema_object,
            movie=self.movie_object
        )

        with self.assertRaises(ValidationError):
            slot.full_clean()

    def test_invalid_end_time_type(self):
        """
        end_time should have a valid format
        """
        slot = Slot(
            **{**self.slot, "end_time": "abc"},
            cinema=self.cinema_object,
            movie=self.movie_object
        )

        with self.assertRaises(ValidationError):
            slot.full_clean()

    def test_invalid_price_type(self):
        """
        Negative price should raise ValidationError
        """
        slot = Slot(
            **{**self.slot, "price": -100},
            cinema=self.cinema_object,
            movie=self.movie_object
        )

        with self.assertRaises(ValidationError):
            slot.full_clean()


class BookingModelTests(BaseTestUtils):
    """
    BookingModelTests to test Booking model
    """

    def setUp(self):
        """
        Creating slot and user for booking tests
        """
        super().setUp()
        self.create_slot()
        self.create_user()

    def test_create_valid_booking(self):
        """
        Booking should be valid when correct details are provided
        """
        booking = Booking(
            slot=self.slot_object,
            user=self.user_object,
            status=Booking.BookingStatus.CONFIRMED,
        )

        booking.full_clean()
        booking.save()

        self.assertEqual(booking.status, Booking.BookingStatus.CONFIRMED)

    def test_missing_booking_or_user(self):
        """
        Booking should raise ValidationError in case of missing slot or user
        """
        booking = Booking(
            status=Booking.BookingStatus.CONFIRMED,
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_invalid_status(self):
        """
        Booking should raise ValidationError in case of invalid status
        """
        booking = Booking(
            slot=self.slot_object,
            user=self.user_object,
            status="PENDING",
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()


class TicketModelTests(BaseTestUtils):
    """
    TicketModelTests to test Ticket model
    """

    def setUp(self):
        """
        Creating booking for ticket tests
        """
        super().setUp()
        self.create_booking()

    def test_create_valid_ticket(self):
        """
        Ticket should be valid when correct details are provided
        """
        ticket = Ticket(booking=self.booking_object, **self.ticket)

        ticket.full_clean()
        ticket.save()

        self.assertEqual(ticket.seat_row, self.ticket.get("seat_row"))

    def test_missing_booking(self):
        """
        Ticket should be invalid when booking is not provided
        """
        ticket = Ticket(**self.ticket)

        with self.assertRaises(ObjectDoesNotExist):
            ticket.full_clean()

    def test_missing_required_fields(self):
        """
        Ticket should be invalid when seat_row or seat_column is not provided
        """
        ticket = Ticket(booking=self.booking_object)

        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_invalid_seat_row(self):
        """
        Ticket should be invalid when seat_row is negative
        """
        ticket = Ticket(booking=self.booking_object, **{**self.ticket, "seat_row": -1})

        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_invalid_seat_column(self):
        """
        Ticket should be invalid when seat_column is negative
        """
        ticket = Ticket(
            booking=self.booking_object, **{**self.ticket, "seat_column": -1}
        )

        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_limit_seat_row(self):
        """
        Ticket should be invalid when seat_row exceeds cinema row capacity
        """
        ticket = Ticket(booking=self.booking_object, **{**self.ticket, "seat_row": 51})

        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_limit_seat_column(self):
        """
        Ticket should be invalid when seat_column exceeds cinema seats_per_row capacity
        """
        ticket = Ticket(
            booking=self.booking_object, **{**self.ticket, "seat_column": 51}
        )

        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_ticket_must_be_unique(self):
        """
        Duplicate tickets should raise IntegrityError
        """
        self.create_ticket()

        with self.assertRaises(IntegrityError):
            self.create_ticket()
