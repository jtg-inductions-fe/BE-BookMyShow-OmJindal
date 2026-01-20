from datetime import date as date_class

from django.db.models import Prefetch
from django.utils import timezone

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError

from apps.movie.models import Movie
from apps.slot.models import Slot
from apps.movie.serializers import (
    MovieSerializer,
    MovieDetailSerializer,
)
from apps.movie.filter import MovieFilter
from apps.movie.pagination import MoviePagination


class MovieViewSet(ReadOnlyModelViewSet):
    """
    View Set to fetch paginated list of movie and particular
    movie based on filters
    """

    pagination_class = MoviePagination
    filterset_class = MovieFilter

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSerializer

        return MovieDetailSerializer

    def get_queryset(self):
        raw_date = self.request.query_params.get("date")
        try:
            if raw_date:
                parsed_date = date_class.fromisoformat(raw_date)
            else:
                parsed_date = timezone.now().date()
        except ValueError:
            raise ValidationError({"date": "Invalid date format. Use YYYY-MM-DD."})

        if self.action == "retrieve":
            city = self.request.query_params.get("city")
            slots_qs = Slot.objects.filter(
                start_time__gt=timezone.now(), start_time__date=parsed_date
            ).select_related("cinema", "cinema__city", "language")

            if city:
                slots_qs = slots_qs.filter(cinema__city_id=city)

            return Movie.objects.prefetch_related(
                Prefetch("slots_by_movie", queryset=slots_qs), "genres", "languages"
            )

        qs = Movie.objects.all()

        if raw_date:
            qs = qs.filter(slots_by_movie__start_time__date=raw_date)

        return qs.prefetch_related("genres", "languages")
