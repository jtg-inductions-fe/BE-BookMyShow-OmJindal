from rest_framework import viewsets
from django.db.models import Prefetch

from apps.cinema.models import Cinema
from apps.slot.models import Slot
from apps.cinema.serializers import CinemaSerializer, CinemaDetailSerializer
from apps.cinema.filter import CinemaFilter
from apps.cinema.pagination import CinemaPagination


class CinemaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Set to fetch paginated list of cinema and particular
    cinema based on filters
    """

    filterset_class = CinemaFilter
    pagination_class = CinemaPagination

    def get_serializer_class(self):
        if self.action == "list":
            return CinemaSerializer

        return CinemaDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return Cinema.objects.select_related("city")

        return Cinema.objects.select_related("city").prefetch_related(
            Prefetch(
                "slots_by_cinema",
                queryset=Slot.objects.select_related("movie"),
            )
        )
