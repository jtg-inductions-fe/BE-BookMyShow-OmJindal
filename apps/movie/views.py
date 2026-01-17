from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import viewsets

from apps.movie.models import Movie
from apps.slot.models import Slot
from apps.movie.serializers import (
    MovieSerializer,
    MovieCinemasSerializer,
)
from apps.movie.filter import MovieFilter
from apps.movie.pagination import MoviePagination


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Set to fetch paginated list of movie and particular
    movie based on filters
    """

    pagination_class = MoviePagination
    filterset_class = MovieFilter

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSerializer

        return MovieCinemasSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        if self.action == "retrieve":
            city = self.request.query_params.get("city")
            slots_qs = Slot.objects.filter(
                start_time__gt=timezone.now()
            ).select_related("cinema", "cinema__city")
            if city:
                slots_qs = slots_qs.filter(cinema__city_id=city)
            if date:
                slots_qs = slots_qs.filter(start_time__date=date)
            else:
                slots_qs = slots_qs.filter(start_time__date=timezone.now().date())
            return Movie.objects.prefetch_related(
                Prefetch("slots_by_movie", queryset=slots_qs),
                "genres",
            )
        qs = Movie.objects.all()
        if date:
            qs = qs.filter(slots_by_movie__start_time__date=date)
        return qs.prefetch_related("genres", "languages").distinct()
