from rest_framework import viewsets

from apps.movie.models import Movie
from apps.movie.serializers import MovieSerializer
from apps.movie.filter import MovieFilter
from apps.movie.pagination import MoviePagination


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Set to fetch list of movie and particular
    movie based on filters
    """

    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.prefetch_related("languages", "genres").order_by(
            "-release_date"
        )
