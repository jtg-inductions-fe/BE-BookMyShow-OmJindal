from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Prefetch

from apps.cinema.models import Cinema
from apps.slot.models import Slot
from apps.cinema.serializers import CinemaSerializer, CinemaDetailSerializer
from apps.cinema.filter import CinemaFilter
from apps.cinema.pagination import CinemaPagination


class CinemaListAPIView(ListAPIView):
    """
    List all cinemas.

    - Supports filtering by city
    - Paginated response
    """

    serializer_class = CinemaSerializer
    queryset = Cinema.objects.select_related("city")
    filterset_class = CinemaFilter
    pagination_class = CinemaPagination


class CinemaDetailAPIView(RetrieveAPIView):
    """
    Retrieve a single cinema with slots and movies.
    """

    serializer_class = CinemaDetailSerializer

    def get_queryset(self):
        return Cinema.objects.select_related("city").prefetch_related(
            Prefetch(
                "slots_by_cinema",
                queryset=Slot.objects.select_related("movie"),
            )
        )
