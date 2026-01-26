from rest_framework import generics as rest_generics

from apps.slot import models as slot_models
from apps.slot import serializers as slot_serializers


class SlotDetailView(rest_generics.RetrieveAPIView):
    """
    Detailed retrieval of a specific Slot including
    its seats occupancy.

    URL Parameters:
        - pk (int): The unique identifier (Primary Key) of the Slot.
    """

    serializer_class = slot_serializers.SlotDetailSerializer

    def get_queryset(self):
        """
        Builds a optimized queryset for fetching slot occupancy data.

        Filter Logic:
            Only includes 'tickets' from bookings where the status is 'BOOKED'.
            Cancelled bookings are excluded from the occupancy list.

        Returns:
            QuerySet: Slot instances with complete details.
        """
        return slot_models.Slot.objects.select_related(
            "cinema", "movie", "cinema__city", "language"
        ).prefetch_related("cinema__seats")
