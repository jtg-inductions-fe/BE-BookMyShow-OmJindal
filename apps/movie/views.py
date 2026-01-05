from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.movie.models import Movie
from apps.movie.serializers import MovieSerializer, MovieCinemasSerializer
from apps.movie.filter import MovieFilter
from apps.movie.pagination import MoviePagination


class MovieListAPIView(ListAPIView):
    """
    API to fetch list of movies with filters & pagination
    """

    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.prefetch_related("languages", "genres").order_by(
            "-release_date"
        )


class MovieDetailAPIView(RetrieveAPIView):
    """
    API to fetch a single movie by ID
    """

    serializer_class = MovieSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Movie.objects.prefetch_related("languages", "genres")
