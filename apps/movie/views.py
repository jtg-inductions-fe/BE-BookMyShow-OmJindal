from django.db.models import Prefetch
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
        if self.action == "list":
            return Movie.objects.all()

        city = self.request.query_params.get("city")

        slots_qs = Slot.objects.select_related("cinema")

        if city:
            slots_qs = slots_qs.filter(cinema__city_id=city)

        return Movie.objects.prefetch_related(
            Prefetch(
                "slots_by_movie",
                queryset=slots_qs,
            )
        )
