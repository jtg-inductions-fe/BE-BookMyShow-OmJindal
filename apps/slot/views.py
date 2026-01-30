from rest_framework import generics as rest_generics

from apps.slot import models as slot_models
from apps.slot import serializers as slot_serializers


class SlotDetailView(rest_generics.RetrieveAPIView):
    """
    Retrieve API endpoint to fetch detailed slot information along with
    movie details, cinema layout, and seat availability.

    HTTP Method: (GET)
        URL Parameters:
            pk (int): Unique identifier (Primary Key) of the slot.
        Response:
            200 OK:
                Returns a JSON object with basic slot details along with movie,
                language, cinema layout information and an array of seats containing
                seat and its availability information.
                Example:
                {
                    "price": int,
                    "start_time": datetime,
                    "language": str,
                    "movie": str,
                    "cinema": {
                        "name": str,
                        "city": str,
                        "rows": int,
                        "seats_per_row": int
                    },
                    "seats": [
                        {
                            "id": int,
                            "row_number": int,
                            "seat_number": int,
                            "is_available": bool
                        }
                }
        Errors:
            404 Not Found:
                - No Slot matches the given query.
    """

    serializer_class = slot_serializers.SlotDetailSerializer

    def get_queryset(self):
        """
        Builds a optimized queryset for fetching slot information.
        """
        return slot_models.Slot.objects.select_related(
            "cinema", "movie", "cinema__city", "language"
        ).prefetch_related("cinema__seats", "cinema__seats__bookings")
