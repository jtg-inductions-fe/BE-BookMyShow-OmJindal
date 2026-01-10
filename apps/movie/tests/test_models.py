from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.movie.models import Movie
from apps.base.tests.utils import BaseTestUtils


class MovieModelTests(BaseTestUtils):
    """
    MovieModelTests to test Movie model
    """

    def setUp(self):
        """
        Creating language and genre for movie tests
        """
        super().setUp()
        self.create_language()
        self.create_genre()

    def test_create_valid_movie(self):
        """
        Movie should be valid when correct details are provided
        """
        movie = Movie(**self.movie)

        movie.full_clean()
        movie.save()

        movie.genres.add(self.genre_object)
        movie.languages.add(self.language_object)

        self.assertEqual(movie.name, self.movie.get("name"))

    def test_movie_name_must_be_unique(self):
        """
        Movie with same name should raise IntegrityError
        """
        self.create_movie()

        with self.assertRaises(IntegrityError):
            self.create_movie()

    def test_invalid_duration_type(self):
        """
        Movie should be invalid in case of wrong duration type
        """
        movie = Movie(**{**self.movie, "duration": "abc"})

        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_invalid_release_date_type(self):
        """
        Movie should be invalid in case of wrong release_date type
        """
        movie = Movie(**{**self.movie, "release_date": "20-01-01"})

        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_movie_genres_and_languages(self):
        """
        Movie should be valid when correct language and genres are added
        """
        self.genre1 = self.create_genre(data={"name": "Actionable"})
        self.genre2 = self.create_genre(data={"name": "Scientific"})
        self.language1 = self.create_language(data={"name": "Spanish"})
        self.language2 = self.create_language(data={"name": "French"})

        self.create_movie()

        self.movie_object.genres.add(self.genre1, self.genre2)
        self.movie_object.languages.add(self.language1, self.language2)

        self.assertEqual(self.movie_object.genres.count(), 2)
        self.assertEqual(self.movie_object.languages.count(), 2)

    def test_missing_required_fields(self):
        """
        Movie should be invalid in case of missing details
        """
        movie = Movie(name="Incomplete Movie")

        with self.assertRaises(ValidationError):
            movie.full_clean()
