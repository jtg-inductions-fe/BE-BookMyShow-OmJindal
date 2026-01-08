import django_filters
from django.utils import timezone
from datetime import timedelta

from apps.movie.models import Movie
from apps.base.models import Genre, Language


class MovieFilter(django_filters.FilterSet):
    """
    FilterSet for Movie model.

    Provides filtering for:
    - Multiple genres (ManyToMany relationship)
    - Multiple languages (ManyToMany relationship)
    - Latest movies based on release date (last N days)
    """

    genres = django_filters.CharFilter(method="filter_genres")

    languages = django_filters.CharFilter(method="filter_languages")

    latest_days = django_filters.NumberFilter(method="filter_latest_movies")

    class Meta:
        model = Movie
        fields = ["genres", "languages"]

    def filter_genres(self, queryset, name, value):
        genre_ids = value.split(",")
        return queryset.filter(genres__id__in=genre_ids).distinct()

    def filter_languages(self, queryset, name, value):
        language_ids = value.split(",")
        return queryset.filter(languages__id__in=language_ids).distinct()

    def filter_latest_movies(self, queryset, name, value):
        """
        value = number of days
        """
        days = int(value)
        date_from = timezone.now().date() - timedelta(days=days)
        return queryset.filter(release_date__gte=date_from)
