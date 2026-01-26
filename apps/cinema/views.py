from datetime import date as date_class

from django.db.models import Prefetch
from django.utils import timezone
from django_filters import rest_framework as df_filters
from rest_framework import exceptions as rest_exceptions
from rest_framework import filters as rest_filters
from rest_framework import viewsets as rest_viewsets

from apps.cinema import constants as cinema_constants
from apps.cinema import filter as cinema_filters
from apps.cinema import models as cinema_models
from apps.cinema import pagination as cinema_paginations
from apps.cinema import serializers as cinema_serializers
from apps.slot import models as slot_models


class CinemaViewSet(rest_viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for cinema listings and detailed cinema showtimes.

    This ViewSet provides endpoints to browse the cinemas and check
    specific showtime availability across different movies.

    Actions:
        list:
            Returns a paginated list of cinemas. Supports filtering by
            cities and search filter.

        retrieve:
            Returns full data for a single cinema along with
            nested 'movies' containing showtime slots, filtered
            by 'date' query parameters.

    Attributes:
        filterset_class: Custom CinemaFilter for city-based filtering.
        pagination_class: Cursor-based pagination for stable scrolling.
        search_fields: Enables searching by cinema name or city name.
    """

    filterset_class = cinema_filters.CinemaFilter
    pagination_class = cinema_paginations.CinemaPagination
    filter_backends = [df_filters.DjangoFilterBackend, rest_filters.SearchFilter]
    search_fields = ["name", "city__name"]

    def get_serializer_class(self):
        """
        Selects the serializer based on the current action.

        Returns:
            list: CinemaSerializer
            retrieve: CinemaDetailSerializer
        """
        if self.action == "list":
            return cinema_serializers.CinemaSerializer

        return cinema_serializers.CinemaDetailSerializer

    def get_queryset(self):
        """
        Dynamically builds the queryset based on the action and query parameters.

        Returns:
            QuerySet: Optimized Cinema queryset with prefetched relations.

        Raises:
            ValidationError: If the 'date' parameter is in an invalid format.
        """
        if self.action == "retrieve":
            raw_date = self.request.query_params.get("date")

            try:
                parsed_date = (
                    date_class.fromisoformat(raw_date) if raw_date else timezone.now().date()
                )
            except ValueError:
                raise rest_exceptions.ValidationError(
                    {"date": cinema_constants.ErrorMessages.INVALID_DATE_FORMAT}
                )

            slots_qs = (
                slot_models.Slot.objects.filter(
                    start_time__gt=timezone.now(), start_time__date=parsed_date
                )
                .select_related("movie", "language")
                .prefetch_related("movie__genres")
                .order_by("start_time")
            )

            return cinema_models.Cinema.objects.select_related("city").prefetch_related(
                Prefetch("slots", queryset=slots_qs)
            )

        return cinema_models.Cinema.objects.select_related("city")
