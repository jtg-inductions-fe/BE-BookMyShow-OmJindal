import django_filters

from apps.cinema import models as cinema_models


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """
    A custom filter that allows for comma-separated numeric values.

    This enables filtering across multiple IDs in a single query parameter.
    Example: `/api/cinemas/?cities=1,2,3`
    """

    pass


class CinemaFilter(django_filters.FilterSet):
    """
    FilterSet for Cinema model.

    Attributes:
        cities (NumberInFilter): A filter allowing multiple city IDs to be
            passed as a comma-separated string.
    """

    cities = NumberInFilter(field_name="city_id", lookup_expr="in")

    class Meta:
        """
        Configuration for the CinemaFilter.
        """

        model = cinema_models.Cinema
        fields = ["cities"]
