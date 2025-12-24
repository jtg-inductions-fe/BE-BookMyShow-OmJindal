from django.db import models
from django.core.validators import MinValueValidator


class City(models.Model):
    """
    Represents a city in which the cinema is located.

    Attributes:
        name (str) : The name of the city.
    """

    name = models.CharField(max_length=50)

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
    address = models.CharField(max_length=70)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    seats_per_row = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name
