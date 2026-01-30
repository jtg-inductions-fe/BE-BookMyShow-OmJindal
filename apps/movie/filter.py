from datetime import timedelta

import django_filters
from django.utils import timezone

from apps.movie import models as movie_models


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """
    Custom filter to allow comma-separated numeric IDs in a query string.

    Example:
        /api/movies/?genres=1,2,3
    """

    pass


class MovieFilter(django_filters.FilterSet):
    """
    FilterSet for Movie model.

    Attributes:
        genres (NumberInFilter): Filter by multiple genre IDs.
        languages (NumberInFilter): Filter by multiple language IDs.
        cinemas (NumberInFilter): Filter by multiple cinema IDs.
        latest_days (NumberFilter): Custom filter for recently released movies.
    """

    genres = NumberInFilter(field_name="genres__id", lookup_expr="in")
    languages = NumberInFilter(field_name="languages__id", lookup_expr="in")
    cinemas = NumberInFilter(field_name="slots__cinema_id", lookup_expr="in")
    latest_days = django_filters.NumberFilter(method="filter_latest_movies")

    class Meta:
        model = movie_models.Movie
        fields = ["genres", "languages", "cinemas", "latest_days"]

    def filter_latest_movies(self, queryset, name, value):
        """
        Filters the queryset to return movies released within the last N days.
        """
        try:
            days = int(value)
        except (TypeError, ValueError):
            return queryset

        if days <= 0:
            return queryset

        date_from = timezone.now().date() - timedelta(days=days)
        return queryset.filter(release_date__gte=date_from)
