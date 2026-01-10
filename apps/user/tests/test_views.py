from django.urls import reverse

from rest_framework import status

from apps.base.tests.utils import BaseTestUtils
from apps.slot.models import Booking


class SignupViewTests(BaseTestUtils):
    """
    SignupViewTests class to test user Signup
    """

    def test_user_can_signup(self):
        """
        User can signup with valid details
        """
        response = self.client.post(reverse("signup"), self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_password_mismatch(self):
        """
        User cannot signup incase of password and confirm_password mismatch
        """
        response = self.client.post(
            reverse("signup"),
            {**self.user, "confirm_password": "WrongPass"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_validate_password(self):
        """
        User cannot signup incase of weak or common password
        """
        response = self.client.post(
            reverse("signup"),
            {
                **self.user,
                "password": "123",
                "confirm_password": "123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_validate_phone_number(self):
        """
        User cannot signup with invalid phone_number
        """
        response = self.client.post(
            reverse("signup"),
            {**self.user, "phone_number": "123"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_user(self):
        """
        User with same email cannot exist
        """
        response = self.client.post(reverse("signup"), self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(reverse("signup"), self.user)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(BaseTestUtils):
    """
    LoginViewTests class to test user Login
    """

    def setUp(self):
        """
        Creating user for login
        """
        super().setUp()
        self.create_user()

    def test_login_success(self):
        """
        User can login with correct credentials
        """
        response = self.client.post(
            reverse("login"),
            self.user,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        """
        User cannot login with incorrect credentials
        """
        response = self.client.post(
            reverse("login"),
            {**self.user, "password": "WrongPass"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileViewTests(BaseTestUtils):
    """
    ProfileViewTests class to test user profile fetching and updation
    """

    def setUp(self):
        """
        Creating user for profile view
        """
        super().setUp()
        self.create_user()

    def test_get_profile(self):
        """
        Authenticated users can fetch their profile details
        """
        self.authenticate()
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_object.email)

    def test_get_profile_authorization(self):
        """
        Unauthenticated users cannot fetch their profile details
        """
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile(self):
        """
        Authenticated users can update their allowed profile details
        """
        self.authenticate()
        response = self.client.patch(
            reverse("profile"),
            {"name": "Updated Name"},
        )
        self.user_object.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_object.name, "Updated Name")

    def test_patch_profile_authorization(self):
        """
        Unauthenticated users cannot update their profile details
        """
        response = self.client.patch(
            reverse("profile"),
            {"name": "Updated Name"},
        )
        self.user_object.refresh_from_db()

    def test_patch_invalid_field(self):
        """
        Authenticated users cannot update unallowed profile detals like 'email'
        """
        self.authenticate()
        response = self.client.patch(
            reverse("profile"),
            {"email": "hack@test.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PurchaseHistoryViewTests(BaseTestUtils):
    """
    PurchaseHistoryViewTests class to test user booking history
    """

    def setUp(self):
        """
        Creating user and booking for tests
        """
        super().setUp()
        self.create_user()
        self.create_booking()

    def test_purchase_history_with_booking(self):
        """
        Authenticated user can fetch their purchase history
        """
        self.authenticate()
        response = self.client.get(reverse("user-purchase-history"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.booking_object.id)

    def test_purchase_history_with_booking_authorization(self):
        """
        Unauthenticated user cannot fetch their purchase history
        """
        response = self.client.get(reverse("user-purchase-history"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingCancelViewTests(BaseTestUtils):
    """
    BookingCancelViewTests to test user booking cancellation
    """

    def setUp(self):
        """
        Creating user and booking for the tests
        """
        super().setUp()
        self.create_user()
        self.create_booking()

    def test_cancel_booking(self):
        """
        Authenticated user can cancel their booking
        """
        self.authenticate()
        response = self.client.patch(
            reverse("booking-cancel", kwargs={"pk": self.booking_object.id})
        )
        self.booking_object.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.booking_object.status,
            Booking.BookingStatus.CANCELLED,
        )

    def test_cancel_booking_authorization(self):
        """
        Unauthenticated user cannot cancel their booking
        """
        response = self.client.patch(
            reverse("booking-cancel", kwargs={"pk": self.booking_object.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_cancel_twice(self):
        """
        Authenticated user cannot cancel their booking twice
        """
        self.authenticate()
        self.booking_object.status = Booking.BookingStatus.CANCELLED
        self.booking_object.save()

        response = self.client.patch(
            reverse("booking-cancel", kwargs={"pk": self.booking_object.id})
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
