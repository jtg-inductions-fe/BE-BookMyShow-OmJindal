from datetime import date as date_class

from django.db.models import Prefetch
from django.utils import timezone

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.cinema.models import Cinema
from apps.slot.models import Slot
from apps.cinema.serializers import CinemaSerializer, CinemaDetailSerializer
from apps.cinema.filter import CinemaFilter
from apps.cinema.pagination import CinemaPagination


class CinemaViewSet(ReadOnlyModelViewSet):
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
            raw_date = self.request.query_params.get("date")

            try:
                if raw_date:
                    parsed_date = date_class.fromisoformat(raw_date)
                else:
                    parsed_date = timezone.now().date()
            except ValueError:
                raise ValidationError({"date": "Invalid date format. Use YYYY-MM-DD."})

            slots_qs = (
                Slot.objects.filter(
                    start_time__gt=timezone.now(), start_time__date=parsed_date
                )
                .select_related("movie", "language")
                .prefetch_related("movie__genres", "movie__languages")
            )

            return Cinema.objects.select_related("city").prefetch_related(
                Prefetch("slots_by_cinema", queryset=slots_qs)
            )

        return Cinema.objects.select_related("city")
