from django.core.exceptions import ValidationError
from django.db import models as db_models
from django.utils import timezone

from apps.base import models as base_models
from apps.cinema import models as cinema_models
from apps.movie import models as movie_models
from apps.slot import constant as slot_constants


class Slot(base_models.TimeStampedModel):
    """
    Represents a specific movie screening time in a cinema hall.

    Attributes:
        price (int): The ticket price for this specific show.
        start_time (datetime): The date and time when the movie starts.
        end_time (datetime): The date and time when the movie ends.
        movie (ForeignKey): Reference to the Movie being screened.
        cinema (ForeignKey): Reference to the Cinema hosting the show.
        language (ForeignKey): The specific language version for this screening.
    """

    price = db_models.PositiveIntegerField()
    start_time = db_models.DateTimeField()
    end_time = db_models.DateTimeField()
    movie = db_models.ForeignKey(
        movie_models.Movie, on_delete=db_models.CASCADE, related_name="slots"
    )
    cinema = db_models.ForeignKey(
        cinema_models.Cinema,
        on_delete=db_models.CASCADE,
        related_name="slots",
    )
    language = db_models.ForeignKey(
        base_models.Language,
        on_delete=db_models.CASCADE,
        related_name="slots",
    )

    class Meta:
        """
        Meta options for Slot.
        """

        constraints = [
            # Checks end_time should be greater than start_time
            db_models.CheckConstraint(
                check=db_models.Q(end_time__gt=db_models.F("start_time")),
                name="slot_end_after_start",
            ),
            db_models.UniqueConstraint(
                fields=["cinema", "start_time"],
                name="unique_slot_per_cinema_time",
            ),
        ]

    def __str__(self):
        """
        Returns a string representation of the showtime slot.
        """
        return f"{self.movie.name} at {self.cinema.name} in {self.language}"

    def clean(self):
        """
        Validates the slot's business logic before saving.

        Checks for language availability, cinema hall overlaps,
        movie duration alignment, and release date consistency.

        Raises:
            ValidationError: If any business rule is violated.
        """
        # 1. Validate Language availability for the Movie
        if self.movie and self.language:
            if not self.movie.languages.filter(id=self.language.id).exists():
                raise ValidationError({slot_constants.ErrorMessages.INVALID_LANGUAGE})

        # 2. Prevent overlapping slots in the SAME CINEMA (any movie)
        overlapping_slots = Slot.objects.exclude(pk=self.pk).filter(
            cinema=self.cinema,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if overlapping_slots.exists():
            raise ValidationError(slot_constants.ErrorMessages.OVERLAPPING_SCHEDULE)

        # 3. Ensure duration is sufficient
        if self.movie and (self.end_time - self.start_time) < self.movie.duration:
            raise ValidationError(slot_constants.ErrorMessages.DURATION_TOO_SHORT)

        # 4. Check against Release Date
        if self.movie and self.start_time.date() < self.movie.release_date:
            raise ValidationError(slot_constants.ErrorMessages.BEFORE_RELEASE_DATE)

        # 5. Prevent creation of slot in past
        if self.start_time < timezone.now():
            raise ValidationError(slot_constants.ErrorMessages.PAST_START_TIME)
