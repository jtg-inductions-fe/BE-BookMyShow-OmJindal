from datetime import date as date_class

from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import exceptions as rest_exceptions
from rest_framework import viewsets as rest_viewsets

from apps.movie import constants as movie_constants
from apps.movie import filter as movie_filters
from apps.movie import models as movie_models
from apps.movie import pagination as movie_paginations
from apps.movie import serializers as movie_serializers
from apps.slot import models as slot_models


class MovieViewSet(rest_viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoints for browsing movies and
    viewing movie showtime details.

    Actions:

    1. LIST (GET) (/movies/)
        Returns a paginated list of movies and supports filtering through
        languages, genres, cinemas, date and latest released.
    Query Parameters:
        - date
            Filters movies that have at least one slot on the given date.
            Format: YYYY-MM-DD
            Default: Current date
        - genres
            Comma-separated list of genre IDs.
            Example: ?genres=1,2,3
        - languages
            Comma-separated list of language IDs.
            Example: ?languages=1,2
        - cinemas
            Comma-separated list of cinema IDs. Filters movies having
            slots in the given cinemas.
            Example: ?cinemas=4,5
        - latest_days
            Filters movies released within the last N days from today.
            Example: ?latest_days=7
    Response:
        200 OK
        {
            "next": str | null,
            "previous": str | null,
            "results": [
                {
                    "id": int,
                    "poster": str,
                    "name": str,
                    "genres": [str],
                    "duration": str,
                    "languages": [str],
                    "description": str
                }
            ]
        }
    Errors:
        400 Bad Request:
            - Invalid date format. Please use YYYY-MM-DD


    2. RETRIEVE (GET) (/movies/{pk}/)
    Description:
        Returns detailed information for a specific movie including
        nested showtime data grouped by cinema and then by language.
        Only future slots are returned for the selected date.
    Query Parameters:
        - date
            Filter slots by date.
            Format: YYYY-MM-DD
            Default: Current date.
        - city
            Filter cinemas and slots for a specific city ID.
    Response:
        200 OK
        {
            "id": int,
            "poster": str,
            "name": str,
            "genres": [str],
            "duration": str,
            "languages": [str],
            "description": str,
            "cinemas": [
                {
                    "cinema": {
                        "id": int,
                        "image": str,
                        "name": str,
                        "city": str,
                        "address": str
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
            - No Movie matches the given query
    """

    pagination_class = movie_paginations.MoviePagination
    filterset_class = movie_filters.MovieFilter

    def get_serializer_class(self):
        """
        Determines which serializer to use based on the current action.

        Returns:
            list: MovieSerializer
            retrieve: MovieDetailSerializer
        """
        if self.action == "list":
            return movie_serializers.MovieSerializer
        return movie_serializers.MovieDetailSerializer

    def get_queryset(self):
        """
        Dynamically builds the queryset based on the action and
        query parameters.
        """
        raw_date = self.request.query_params.get("date")

        # Date Parsing Logic
        try:
            parsed_date = (
                date_class.fromisoformat(raw_date)
                if raw_date
                else timezone.now().date()
            )
        except ValueError:
            raise rest_exceptions.ValidationError(
                {"date": movie_constants.ErrorMessages.INVALID_DATE_FORMAT}
            )

        # Retrieve
        if self.action == "retrieve":
            city_id = self.request.query_params.get("city")

            # Filter slots for the specific date and future times
            slots_qs = (
                slot_models.Slot.objects.filter(
                    start_time__gt=timezone.now(), start_time__date=parsed_date
                )
                .select_related("cinema", "cinema__city", "language")
                .order_by("start_time")
            )

            if city_id:
                slots_qs = slots_qs.filter(cinema__city_id=city_id)

            return movie_models.Movie.objects.prefetch_related(
                Prefetch("slots", queryset=slots_qs),
                "genres",
                "languages",
            )

        # List
        qs = movie_models.Movie.objects.all()
        if raw_date:
            qs = qs.filter(slots__start_time__date=raw_date)

        return qs.prefetch_related("genres", "languages").distinct()
