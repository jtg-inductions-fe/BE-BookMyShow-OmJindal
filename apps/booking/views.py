from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

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
    API endpoints for managing user bookings including
    booking creation, booking history retrieval, and booking cancellation.

    Permissions:
        - IsAuthenticated: Only authenticated users can access booking endpoints.
        - IsOwnerOrReadOnly: Users can only modify their own bookings.

    Allowed HTTP Methods:
        GET, POST, PATCH

    Actions:
    1. LIST (GET) (/bookings/)
        Description:
            Returns booking history of the authenticated user including
            movie, cinema, showtime, seat details and booking status.
        Response:
            200 OK
            [
                {
                    "id": int,
                    "movie": str,
                    "language": str,
                    "cinema_name": str,
                    "cinema_address": str,
                    "cinema_city": str,
                    "start_time": datetime,
                    "status": B,
                    "seats": [
                        {
                            "row_number": int,
                            "seat_number": int
                        }
                    ]
                }
            ]
        Errors:
            401 Unauthorized:
                - Authentication credentials were not provided.
                - Token is expired

    2. CREATE (POST) (/bookings/)
        Description:
            Creates a new booking for a specific slot with selected seats.
        Request Body:
            {
                "slot": int,
                "seats": [int]
            }
        Response:
            201 Created
            {
                "id": int,
                "status": str
            }
        Errors:
            400 Bad Request:
                - Booking is closed for this showtime as it has already started or ended.
                - Please select at least one seat to proceed with the booking.
                - Duplicate seats are not allowed for booking
                - Seats do not belong to the cinema.
                - Seats are already booked.
            401 Unauthorized:
                - Authentication credentials were not provided.
                - Token is expired

    3. PARTIAL UPDATE (PATCH) (/bookings/{id}/)
        Description:
            Cancels an existing booking by updating its status to CANCELLED.
        Response:
            200 OK
            {
                "id": int,
                "status": C
            }
        Errors:
            400 Bad Request:
                - This booking has already been cancelled.
                - Cannot cancel a booking for a show that has already started or finished.
            403 Forbidden:
                - You do not have permission to perform this action.
            404 Not Found:
                - No Booking matches the given query.
            401 Unauthorized:
                - Authentication credentials were not provided.
                - Token is expired
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
        Builds a optimized queryset for fetching booking information.
        """
        if self.action == "partial_update":
            return Booking.objects.select_related("slot", "user")
        return (
            Booking.objects.filter(user=self.request.user)
            .select_related("slot__movie", "slot__cinema", "slot__cinema__city")
            .prefetch_related("seats")
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        """
        Ensures the slot object is available in the context
        during creation.
        """
        context = super().get_serializer_context()
        if self.action == "create":
            slot_id = self.request.data.get("slot")
            context["slot"] = get_object_or_404(
                Slot.objects.select_related("cinema").prefetch_related(
                    "cinema__seats", "cinema__seats__bookings"
                ),
                id=slot_id,
            )
        return context
