from datetime import timedelta

import django_filters
from django.utils import timezone

from apps.movie.models import Movie


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class MovieFilter(django_filters.FilterSet):
    """
    FilterSet for Movie model.

    Provides filtering for:
    - Multiple genres (ManyToMany relationship)
    - Multiple languages (ManyToMany relationship)
    - Latest movies based on release date (last N days)
    - Multiple Cinemas in which movie is available
    - Slot on a particular Date
    """

    genres = NumberInFilter(field_name="genres__id", lookup_expr="in")

    languages = NumberInFilter(field_name="languages__id", lookup_expr="in")

    cinemas = NumberInFilter(field_name="slots_by_movie__cinema_id", lookup_expr="in")

    latest_days = django_filters.NumberFilter(method="filter_latest_movies")

    class Meta:
        model = Movie
        fields = ["genres", "languages", "cinemas", "latest_days"]

    def filter_latest_movies(self, queryset, name, value):
        try:
            days = int(value)
        except (TypeError, ValueError):
            return queryset

        if days <= 0:
            return queryset

        date_from = timezone.now().date() - timedelta(days=days)
        return queryset.filter(release_date__gte=date_from)
