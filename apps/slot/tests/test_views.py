from django.urls import reverse

from rest_framework import status

from apps.base.tests.utils import BaseTestUtils


class SlotRetrieveViewTests(BaseTestUtils):
    """
    SlotRetrieveViewTests to test slot retrieval
    """

    def setUp(self):
        """
        Creating slot and tickets for tests
        """
        super().setUp()
        self.create_slot()
        self.create_ticket()
        self.create_ticket(data={"seat_row": 2, "seat_column": 5})

    def test_retrieve_slot_returns_slot(self):
        """
        Slot view must be return slot data
        """
        response = self.client.get(
            reverse("slot-ticket-detail", kwargs={"id": self.slot_object.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.slot_object.id)
        self.assertIn("movie", response.data)
        self.assertIn("cinema", response.data)
        self.assertIn("tickets", response.data)
        self.assertEqual(len(response.data["tickets"]), 2)


class CreateBookingViewTests(BaseTestUtils):

    def setUp(self):
        super().setUp()
        self.create_user()
        self.create_slot()
        self.create_ticket()
        self.create_ticket(data={"seat_row": 2, "seat_column": 5})

    def test_create_booking(self):
        """
        Authenticated user is able to create booking
        """
        self.authenticate()
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id}),
            {"seats": [{"seat_row": 11, "seat_column": 13}]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_booking_unauthorised_user(self):
        """
        Unauthenticated user cannot create booking
        """
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_empty_body(self):
        """
        Authenticated user cannot create booking without seats
        """
        self.authenticate()
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_empty_seats(self):
        """
        Authenticated user cannot create booking with empty seats
        """
        self.authenticate()
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id}),
            {"seats": []},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_duplicate_seats(self):
        """
        Authenticated user cannot create booking with duplicate seats
        """
        self.authenticate()
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id}),
            {
                "seats": [
                    {"seat_row": 11, "seat_column": 13},
                    {"seat_row": 11, "seat_column": 13},
                ]
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_seats_exceed_the_cinema_capacity(self):
        """
        Authenticated user cannot create booking with seats that exceeds cinema capacity
        """
        self.authenticate()
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id}),
            {
                "seats": [
                    {"seat_row": 11, "seat_column": 13},
                    {"seat_row": 11, "seat_column": 13},
                ]
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_seats_already_booked(self):
        """
        Authenticated user cannot create booking of seats that are already booked
        """
        self.authenticate()
        self.create_ticket(data={"seat_row": 11, "seat_column": 13})
        response = self.client.post(
            reverse("slot-booking", kwargs={"id": self.slot_object.id}),
            {
                "seats": [
                    {"seat_row": 11, "seat_column": 13},
                ]
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
