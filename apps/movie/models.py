from django.db import models as db_models

from apps.base import models as base_models
from apps.movie import constants as movie_constants


class Movie(base_models.TimeStampedModel):
    """
    Represents a movie model.

    Attributes:
        name (str): The unique title of the movie.
        description (str): A brief summary of the movie.
        duration (timedelta): Total running time (e.g., 02:30:00).
        release_date (date): The release date of the movie indexed for perfomance.
        genres (ManyToManyField): Genres associated with the movie.
        languages (ManyToManyField): Languages associated with the movie.
        poster (ImageField): Movie poster image.
    """

    name = db_models.CharField(
        max_length=movie_constants.MovieConstants.NAME_MAX_LENGTH,
        unique=True,
    )
    description = db_models.TextField()
    duration = db_models.DurationField(help_text="Format: HH:MM:SS")
    release_date = db_models.DateField(db_index=True)
    genres = db_models.ManyToManyField(base_models.Genre, related_name="movies")
    languages = db_models.ManyToManyField(base_models.Language, related_name="movies")
    poster = db_models.ImageField(
        upload_to=movie_constants.MovieConstants.MOVIE_POSTER_DIR,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-release_date"]

    def __str__(self):
        """
        The string representation of the movie.

        Returns:
            str: The movie name.
        """
        return self.name
