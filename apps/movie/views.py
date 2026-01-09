from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.movie.models import Movie
from apps.movie.serializers import MovieSerializer, MovieDetailSerializer
from apps.movie.filter import MovieFilter
from apps.movie.pagination import MoviePagination


class MovieListAPIView(ListAPIView):
    """
    API to fetch list of movies with filters & pagination
    """

    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    filterset_class = MovieFilter
    queryset = Movie.objects.all()
