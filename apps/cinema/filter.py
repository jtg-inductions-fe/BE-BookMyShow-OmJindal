import django_filters
from apps.cinema.models import Cinema


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class CinemaFilter(django_filters.FilterSet):
    """
    FilterSet for Cinema model.

    Filter cinemas on the basis of cities
    """

    cities = NumberInFilter(field_name="city_id", lookup_expr="in")

    class Meta:
        model = Cinema
        fields = ["cities"]
