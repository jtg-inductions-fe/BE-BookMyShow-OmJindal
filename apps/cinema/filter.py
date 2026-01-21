import django_filters
from apps.cinema.models import Cinema


class CinemaFilter(django_filters.FilterSet):
    """
    FilterSet for Cinema model.

    Provides filtering for a particular city
    """

    city = django_filters.NumberFilter(field_name="city__id")

    class Meta:
        model = Cinema
        fields = ["city"]
