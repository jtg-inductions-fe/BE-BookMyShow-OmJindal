import django_filters

from apps.cinema import models as cinema_models


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """
    Custom filter to allow comma-separated numeric IDs in a query string.

    Example:
        /api/cinemas/?cities=1,2,3
    """

    pass


class CinemaFilter(django_filters.FilterSet):
    """
    FilterSet for Cinema model.

    Attributes:
        cities (NumberInFilter): Filter by multiple City IDs.
    """

    cities = NumberInFilter(field_name="city_id", lookup_expr="in")

    class Meta:
        model = cinema_models.Cinema
        fields = ["cities"]
