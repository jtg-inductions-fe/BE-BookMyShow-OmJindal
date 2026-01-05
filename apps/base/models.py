from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-managed
    creation and modification timestamps.

    Attributes:
        created_at (DateTimeField) : Timestamp when the record is created.
        updated_at (DateTimeField) : Timestamp when the record is updated.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(TimeStampedModel):
    """
    Represents a city in which the cinema is located.

    Attributes:
        name (str) : The name of the city.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(TimeStampedModel):
    """
    Represents a movie category.

    Attributes:
        name (str) : The name of the genre (e.g., Action, Horror).
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Language(TimeStampedModel):
    """
    Represents the language of the movie content.

    Attributes:
        name (str) : The name of the language (e.g., English, Hindi).
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
