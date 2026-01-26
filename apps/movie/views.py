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
    ViewSet for movie listings and detailed movie showtimes.

    This ViewSet provides endpoints to browse the movies and check
    specific showtime availability across different cinemas.

    Actions:
        list:
            Returns a paginated list of movies. Supports filtering by
            genre, language, cinemas, and release date.

        retrieve:
            Returns full data for a single movie along with
            nested 'cinemas' containing showtime slots, filtered
            by the 'city' and 'date' query parameters.
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
        Dynamically builds the queryset based on the action and query parameters.

        Raises:
            ValidationError: If the 'date' parameter is in an invalid format.
        """
        raw_date = self.request.query_params.get("date")

        # Date Parsing Logic
        try:
            parsed_date = date_class.fromisoformat(raw_date) if raw_date else timezone.now().date()
        except ValueError:
            raise rest_exceptions.ValidationError(
                {"date": movie_constants.ErrorMessages.INVALID_DATE_FORMAT}
            )

        # Detail View Query (Retrieve)
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

        # List View Query (List)
        qs = movie_models.Movie.objects.all()
        if raw_date:
            qs = qs.filter(slots__start_time__date=raw_date)

        return qs.prefetch_related("genres", "languages").distinct()
