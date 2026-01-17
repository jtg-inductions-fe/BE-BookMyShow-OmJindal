from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.cinema.models import Cinema
from apps.base.tests.utils import BaseTestUtils


class CinemaModelTests(BaseTestUtils):
    """
    CinemaModelTests to test cinema model
    """

    def setUp(self):
        super().setUp()
        self.create_city()

    def test_create_valid_cinema(self):
        """
        Cinema should be valid when correct data is provided
        """
        cinema = Cinema(**self.cinema, city=self.city_object)

        cinema.full_clean()
        cinema.save()

        self.assertEqual(cinema.name, self.cinema.get("name"))
        self.assertEqual(cinema.city.name, self.city.get("name"))

    def test_cinema_must_be_unique(self):
        """
        Duplicate cinema with same name in same city at same address
        should throw error
        """
        self.create_cinema()

        with self.assertRaises(IntegrityError):
            self.create_cinema()

    def test_invalid_rows(self):
        """
        Cinema rows could not be negative
        """
        cinema = Cinema(**{**self.cinema, "rows": -1}, city=self.city_object)

        with self.assertRaises(ValidationError):
            cinema.full_clean()

    def test_invalid_columns(self):
        """
        Cinema seats_per_row should not be negative
        """
        cinema = Cinema(**{**self.cinema, "seats_per_row": -1}, city=self.city_object)

        with self.assertRaises(ValidationError):
            cinema.full_clean()

    def test_missing_required_fields(self):
        """
        Cinema will be invalid if some fields are missing
        """
        cinema = Cinema(name="Incomplete Cinema")

        with self.assertRaises(ValidationError):
            cinema.full_clean()
