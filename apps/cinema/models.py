from django.db import models

from apps.base.models import City, TimeStampedModel


class Cinema(TimeStampedModel):
    """
    Represents a cinema hall within a specific city.

    Attributes:
        name (str) : The name of the cinema.
        address (str) : The physical address of the cinema.
        city (Foreign Key) : References to the City where the cinema is located.
        rows (int) : The total number of rows in the cinema hall.
        seats_per_row (int) : The number of seat available in each row.
    """

    name = models.CharField(max_length=50)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="cinemas")
    rows = models.PositiveSmallIntegerField()
    seats_per_row = models.PositiveSmallIntegerField()
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.city} at {self.address}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "address"], name="unique_cinema_at_each_address"
            )
        ]
