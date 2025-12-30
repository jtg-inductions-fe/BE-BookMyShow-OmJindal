from django.db import models


class City(models.Model):
    """
    Represents a city in which the cinema is located.

    Attributes:
        name (str) : The name of the city.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Cinema(models.Model):
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
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="cinemas_by_city"
    )
    rows = models.PositiveSmallIntegerField()
    seats_per_row = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "address"], name="unique_cinema_at_each_address"
            )
        ]
