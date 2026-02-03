from django.core.exceptions import ValidationError
from django.db import models as db_models
from django.db import transaction as db_transaction
from django.dispatch import receiver

from apps.base import models as base_models
from apps.cinema import constants as cinema_constants


class Cinema(base_models.TimeStampedModel):
    """
    Represents a cinema model.

    Attributes:
        name (str): The name of the cinema.
        city (ForeignKey): Reference to the City model where cinema is located.
        address (str): The complete physical address of cinema.
        rows (int): Total count of horizontal seating rows.
        seats_per_row (int): Total count of vertical seating columns per row.
        image (ImageField): Image of the cinema hall.
    """

    name = db_models.CharField(
        max_length=cinema_constants.CinemaConstants.NAME_MAX_LENGTH
    )
    city = db_models.ForeignKey(
        base_models.City, on_delete=db_models.CASCADE, related_name="cinemas"
    )
    address = db_models.TextField()
    rows = db_models.PositiveSmallIntegerField()
    seats_per_row = db_models.PositiveSmallIntegerField()
    image = db_models.ImageField(
        upload_to=cinema_constants.CinemaConstants.CINEMA_IMAGE_DIR,
        null=True,
        blank=True,
    )

    class Meta:
        # Unique constraint for cinema
        constraints = [
            db_models.UniqueConstraint(
                fields=["name", "city", "address"],
                name="unique_cinema_location",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.city.name})"

    def clean(self):
        """
        Prevents modification of cinema seating layout after creation.
        """
        if self.pk:
            original = Cinema.objects.get(pk=self.pk)
            if (
                original.rows != self.rows
                or original.seats_per_row != self.seats_per_row
            ):
                raise ValidationError(cinema_constants.ErrorMessages.NOT_ALLOWED)

        super().clean()


class Seat(base_models.TimeStampedModel):
    """
    Represents an individual physical seat within a Cinema.

    Seats are generated automatically based on the Cinema's grid layout.

    Attributes:
        cinema (ForeignKey): The cinema hall this seat belongs to.
        row_number (int): The numeric identifier for the row.
        seat_number (int): The numeric identifier for the seat in a row.
    """

    cinema = db_models.ForeignKey(
        Cinema, on_delete=db_models.CASCADE, related_name="seats"
    )
    row_number = db_models.PositiveSmallIntegerField()
    seat_number = db_models.PositiveSmallIntegerField()

    class Meta:
        # Unique constraint for the Seat
        constraints = [
            db_models.UniqueConstraint(
                fields=["cinema", "row_number", "seat_number"],
                name="unique_seat_per_cinema",
            )
        ]

    def __str__(self):
        return f"{self.cinema.name} - R{self.row_number} S{self.seat_number}"

    def clean(self):
        """
        Validates that the seat coordinates do not exceed the cinema hall's capacity.
        """
        if hasattr(self, "cinema"):
            if self.row_number > self.cinema.rows:
                raise ValidationError(
                    {
                        "row_number": f"Row number {self.row_number} exceeds this cinema's capacity of {self.cinema.rows} rows."
                    }
                )

            if self.seat_number > self.cinema.seats_per_row:
                raise ValidationError(
                    {
                        "seat_number": f"Seat number {self.seat_number} exceeds this cinema's capacity of {self.cinema.seats_per_row} seats per row."
                    }
                )

        super().clean()


@receiver(db_models.signals.post_save, sender=Cinema)
def create_cinema_seats(sender, instance, created, **kwargs):
    """
    Automatically generates a grid of Seat objects upon Cinema creation.

    This signal iterates through the defined rows and seats_per_row of the
    cinema instance and performs a bulk insertion for efficiency.

    Args:
        sender (Model): The model class (Cinema).
        instance (Cinema): The actual instance being saved.
        created (bool): Boolean indicating if a new record was created.
    """
    if created:
        with db_transaction.atomic():
            seats_to_create = [
                Seat(cinema=instance, row_number=row, seat_number=seat)
                for row in range(1, instance.rows + 1)
                for seat in range(1, instance.seats_per_row + 1)
            ]
            Seat.objects.bulk_create(seats_to_create)
