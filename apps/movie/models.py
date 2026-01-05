from django.db import models

from apps.base.models import Genre, Language, TimeStampedModel


class Movie(TimeStampedModel):
    """
        Represents a cinematic film available for booking.

    Attributes:
        name (str) : The title of the movie.
        description (str) : A brief summary of the movie.
        duration (timedelta) : Total running time of the movie.
        release_date (date) : The official date the movie was released.
        genres (ManyToManyField) : The genres associated with the movie.
        languages (ForeignKey) : The primary language of the movie.
    """

    name = models.CharField(max_length=125, unique=True)
    description = models.TextField()
    duration = models.DurationField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name="movies_by_genre")
    languages = models.ManyToManyField(Language, related_name="movies_by_language")
    poster = models.CharField(max_length=255)

    def __str__(self):
        return self.name
