from django.db import models


class Genre(models.Model):
    """
    Represents a movie category.

    Attributes:
        name (str) : The name of the genre (e.g., Action, Horror).
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Represents the language of the movie content.

    Attributes:
        name (str) : The name of the language (e.g., English, Hindi).
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
        Represents a cinematic film available for booking.

    Attributes:
        name (str) : The title of the movie.
        description (str) : A brief summary of the movie.
        duration (timedelta) : Total running time of the movie.
        release_date (date) : The official date the movie was released.
        generes (ManyToManyField) : The genres associated with the movie.
        language (ForeignKey) : The primary language of the movie.
    """

    name = models.CharField(max_length=50)
    description = models.TextField()
    duration = models.DurationField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
