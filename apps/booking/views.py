from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.booking import constants as booking_constants
from apps.booking import serializers as booking_serializers
from apps.booking.models import Booking
from apps.booking.permission import IsOwnerOrReadOnly
from apps.slot.models import Slot


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Unified ViewSet managing the complete Booking lifecycle.

    Endpoints:
        - GET /bookings/: Retrieve history of the authenticated user.
        - POST /bookings/: Create a new booking (requires slot_id in body).
        - PATCH /bookings/{id}/: Soft-cancel a specific booking.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "patch"]

    def get_serializer_class(self):
        """
        Determines the serializer based on the HTTP action.
        """
        if self.action == "create":
            return booking_serializers.BookingCreateSerializer
        if self.action == "partial_update":
            return booking_serializers.BookingCancelSerializer
        return booking_serializers.BookingHistorySerializer

    def get_queryset(self):
        """
        Provides optimized querysets.
        """
        if self.action == "partial_update":
            return Booking.objects.all()
        return (
            Booking.objects.filter(user=self.request.user)
            .select_related("slot__movie", "slot__language", "slot__cinema", "slot__cinema__city")
            .prefetch_related("tickets__cinema_seat")
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        """
        Ensures the 'slot' object is available in the context during creation.
        """
        context = super().get_serializer_context()
        if self.action == "create":
            slot_id = self.request.data.get("slot")
            context["slot"] = get_object_or_404(Slot.objects.select_related("cinema"), id=slot_id)
        return context

    def perform_update(self, serializer):
        """
        Applies the cancellation status during a PATCH request.
        """
        serializer.save(status=booking_constants.BookingStatus.CANCELLED)
