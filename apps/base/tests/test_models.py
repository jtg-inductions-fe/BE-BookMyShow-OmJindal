from django.db import IntegrityError

from apps.base.models import Language, City, Genre
from apps.base.tests.utils import BaseTestUtils


class LanguageModelTests(BaseTestUtils):
    """
    LanguageModelTests to test language model
    """

    def setUp(self):
        super().setUp()

    def test_create_valid_language(self):
        """
        Language should be valid with correct details
        """
        language = Language(**self.language)

        language.full_clean()
        language.save()

        self.assertEqual(language.name, self.language.get("name"))

    def test_language_must_be_unique(self):
        """
        Duplicate language should raise IntegrityError
        """
        self.create_language()

        with self.assertRaises(IntegrityError):
            self.create_language()


class GenreModelTests(BaseTestUtils):
    """
    GenreModelTests to test Genre model
    """

    def setUp(self):
        super().setUp()

    def test_create_valid_genre(self):
        """
        Genre should be valid when correct details are provided
        """
        genre = Genre(**self.genre)

        genre.full_clean()
        genre.save()

        self.assertEqual(genre.name, self.genre.get("name"))

    def test_genre_must_be_unique(self):
        """
        Duplicate genre should raise IntegrityError
        """
        self.create_genre()

        with self.assertRaises(IntegrityError):
            self.create_genre()


class CityModelTests(BaseTestUtils):
    """
    CityModelTests to test City model
    """

    def setUp(self):
        super().setUp()

    def test_create_valid_city(self):
        """
        City should be valid when correct details are provied
        """
        city = City(**self.city)

        city.full_clean()
        city.save()

        self.assertEqual(city.name, self.city.get("name"))

    def test_city_must_be_unique(self):
        """
        Duplicate city should raise IntegrityError
        """
        self.create_city()

        with self.assertRaises(IntegrityError):
            self.create_city()
