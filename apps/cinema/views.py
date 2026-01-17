from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "city__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return CinemaSerializer

        return CinemaDetailSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            date = self.request.query_params.get("date")
            slots_qs = Slot.objects.filter(
                start_time__gt=timezone.now()
            ).select_related("movie")
            if date:
                slots_qs = slots_qs.filter(start_time__date=date)
            else:
                slots_qs = slots_qs.filter(start_time__date=timezone.now().date())
            return Cinema.objects.select_related("city").prefetch_related(
                Prefetch("slots_by_cinema", queryset=slots_qs)
            )

        return Cinema.objects.select_related("city")
