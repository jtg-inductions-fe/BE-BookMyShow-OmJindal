from django.db import models as db_models

from apps.base import constants as base_constants


class TimeStampedModel(db_models.Model):
    """
    Abstract base model that provides self-managed
    creation and modification timestamps.

    Attributes:
        created_at (DateTimeField) : Timestamp when the record is created.
        updated_at (DateTimeField) : Timestamp when the record is updated.
    """

    created_at = db_models.DateTimeField(auto_now_add=True)
    updated_at = db_models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for TimeStampedModel.

        Specifies that this model is abstract and should not create
        its own database table.
        """

        abstract = True


class City(TimeStampedModel):
    """
    Represents a city in which the cinema is located. (e.g., Mumbai, Delhi).

    Attributes:
        name (str): Unique name of the city.
    """

    name = db_models.CharField(max_length=base_constants.BaseConstants.NAME_MAX_LENGTH, unique=True)

    class Meta:
        """
        Meta options for City.
        """

        verbose_name_plural = "Cities"
        ordering = ["name"]

    def __str__(self):
        """
        The string representation of the City.

        Returns:
            str: The city name.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Normalizes the city name to lowercase before saving.
        """
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)


class Genre(TimeStampedModel):
    """
    Represents a movie genre (e.g., Action, Sci-Fi, Drama).

    Attributes:
        name (str): Unique name of the genre.
    """

    name = db_models.CharField(max_length=base_constants.BaseConstants.NAME_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        The string representation of the Genre.

        Returns:
            str: The genre name.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Normalizes the genre name to lowercase before saving.
        """
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)


class Language(TimeStampedModel):
    """
    Represents the language available for a movie (e.g., English, Hindi).

    Attributes:
        name (str): Unique name of the language.
    """

    name = db_models.CharField(max_length=base_constants.BaseConstants.NAME_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        The string representation of the Language.

        Returns:
            str: The language name.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Normalizes the language name to lowercase before saving.
        """
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)
