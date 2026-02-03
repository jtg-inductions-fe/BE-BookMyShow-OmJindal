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
    Read-only API endpoints for browsing cinemas and
    viewing cinema showtime details.

    Actions:

    1. LIST (GET) (/cinemas/)
        Returns a paginated list of cinemas and supports filtering through
        cities.
    Query Parameters:
        - cities (str)
            Comma-separated list of city IDs.
            Example: ?cities=1,2,3
        - search (str):
                Filters cinemas by partial or full name/ city name match.
                Example: /cinemas/?search=PVR Guru
    Response:
        200 OK
        {
            "next": str | null,
            "previous": str | null,
            "results": [
                {
                    "id": int,
                    "image": str,
                    "name": str,
                    "city": str,
                    "address": str,
                }
            ]
        }


    2. RETRIEVE (GET) (/cinemas/{pk}/)
    Description:
        Returns detailed information for a specific cinema including
        nested showtime data grouped by movies and then by languages.
        Only future slots are returned for the selected date.
    Query Parameters:
        - date (str):
            Filter slots by date.
            Format: YYYY-MM-DD
            Default: Current date.
    Response:
        200 OK
        {
            "id": int,
            "image": str,
            "name": str,
            "city": str,
            "address": str,
            "movies": [
                {
                    "movie": {
                        "id": int,
                        "poster": str,
                        "name": str,
                        "duration": str,
                        "genres": [str],
                    },
                    "languages": [
                        {
                            "id": int,
                            "name": str,
                            "slots": [
                                {
                                    "id": int,
                                    "start_time": datetime,
                                    "price": int
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    Errors:
        400 Bad Request:
            - Invalid date format. Please use YYYY-MM-DD

        404 Not Found:
            - No Cinema matches the given query
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
        Dynamically builds the queryset based on the action and
        query parameters.
        """

        # Retrieve
        if self.action == "retrieve":
            raw_date = self.request.query_params.get("date")

            # Date Parsing Logic
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

        # List
        return cinema_models.Cinema.objects.select_related("city")
