from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.base.tests.utils import BaseTestUtils

User = get_user_model()


class UserModelTests(BaseTestUtils):
    """
    UserModelTests class to test user Model
    """

    def test_valid_user_creation(self):
        """
        User should be valid when correct details are provided
        """
        user = User(
            name="Om",
            email="om@test.com",
            phone_number="9999999999",
        )

        user.set_password("StrongPass@123")
        user.full_clean()
        user.save()

        self.assertEqual(user.email, "om@test.com")
        self.assertEqual(user.name, "Om")
        self.assertEqual(user.phone_number, "9999999999")
        self.assertTrue(user.check_password("StrongPass@123"))

    def test_invalid_email(self):
        """
        Invalid email format should raise ValidationError
        """
        user = User(
            name="Om",
            email="invalid-email",
            phone_number="9999999999",
            password="StrongPass@123",
        )

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number(self):
        """
        Phone number not matching regex should raise ValidationError
        """
        user = User(
            name="Om",
            email="om@test.com",
            phone_number="12345",
        )

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_create_superuser(self):
        """
        Superuser should have correct flags
        """
        self.create_superuser()

        self.assertTrue(self.superuser_object.is_staff)
        self.assertTrue(self.superuser_object.is_superuser)
        self.assertTrue(self.superuser_object.is_active)

    def test_duplicate_email_not_allowed(self):
        """
        Duplicate email should raise IntegrityError
        """
        self.create_user(data={"name": "Raghav"})

        with self.assertRaises(IntegrityError):
            self.create_user()

    def test_missing_required_fields(self):
        """
        Missing field should raise ValidationError
        """
        user = User(
            name="Incomplete Movie",
            password="StrongPass@123",
        )

        with self.assertRaises(ValidationError):
            user.full_clean()
