from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.slot.serializers import SlotTicketSerializer, BookingCreateSerializer
from apps.slot.models import Slot, Booking


class SlotTicketRetrieveSerializer(RetrieveAPIView):
    """
    API view to retrieve a slot along with its confirmed bookings and tickets.
    """

    serializer_class = SlotTicketSerializer
    lookup_field = "id"

    def get_queryset(self):

        return Slot.objects.select_related(
            "cinema", "movie", "cinema__city"
        ).prefetch_related(
            Prefetch(
                "bookings_by_slot",
                queryset=Booking.objects.filter(
                    status=Booking.BookingStatus.CONFIRMED
                ).prefetch_related("tickets_by_booking"),
            )
        )


class BookingCreationSerializer(CreateAPIView):
    """
    API view to create a booking for a specific slot.
    """

    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["slot"] = get_object_or_404(Slot, id=self.kwargs["id"])
        return context
