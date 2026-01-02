import django_filters
from django.utils import timezone
from datetime import timedelta

from apps.movie.models import Movie
from apps.base.models import Genre, Language


class MovieFilter(django_filters.FilterSet):
    genres = django_filters.ModelMultipleChoiceFilter(
        field_name="genres",
        queryset=Genre.objects.all(),
    )

    languages = django_filters.ModelMultipleChoiceFilter(
        field_name="languages",
        queryset=Language.objects.all(),
    )

    latest_days = django_filters.NumberFilter(method="filter_latest_movies")

    class Meta:
        model = Movie
        fields = ["genres", "languages"]

    def filter_latest_movies(self, queryset, name, value):
        """
        value = number of days
        """
        days = int(value)
        date_from = timezone.now().date() - timedelta(days=days)
        return queryset.filter(release_date__gt=date_from)
