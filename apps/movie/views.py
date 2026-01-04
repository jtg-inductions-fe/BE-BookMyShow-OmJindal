from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Prefetch

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


class MovieDetailAPIView(RetrieveAPIView):
    """
    API to fetch a single movie by ID
    """

    serializer_class = MovieDetailSerializer

    def get_queryset(self):
        return Movie.objects.prefetch_related("languages", "genres")


class MovieCinemasAPIView(RetrieveAPIView):
    """
    API to fetch a movie's cinema and slot details
    """

    serializer_class = MovieCinemasSerializer

    def get_queryset(self):
        location_id = self.request.query_params.get("location_id")

        slots_qs = Slot.objects.select_related(
            "cinema",
            "cinema__city",
        )

        if location_id:
            slots_qs = slots_qs.filter(cinema__city_id=location_id)

        return Movie.objects.prefetch_related(
            Prefetch(
                "slots_by_movie",
                queryset=slots_qs,
            )
        )
