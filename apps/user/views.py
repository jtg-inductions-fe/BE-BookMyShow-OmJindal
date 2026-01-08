from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from apps.user.serializers import (
    SignUpSerializer,
    UserProfileSerializer,
    ProfileUpdateSerializer,
    BookingHistorySerializer,
    BookingCancelSerializer,
)

from apps.slot.models import Booking


class SignupView(CreateAPIView):
    """
    API view to create user's profile.
    """

    serializer_class = SignUpSerializer


class ProfileView(RetrieveUpdateAPIView):
    """
    API view to retrieve and update authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_serializer_class(self):
        """
        Return serializer based on HTTP method.
        """
        if self.request.method == "PATCH":
            return ProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        """
        Return the currently authenticated user.
        """
        return self.request.user


class PurchaseHistoryView(ListAPIView):
    """
    API view to retrieve the authenticated user's booking history.

    Returns a list of bookings made by the logged-in user along with
    nested slot, movie, and cinema details.
    """

    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects.filter(user=self.request.user)
            .prefetch_related("tickets_by_booking")
            .select_related(
                "slot",
                "slot__cinema",
                "slot__cinema__city",
                "slot__movie",
                "slot",
            )
        )


class BookingCancelView(UpdateAPIView):
    """
    API view to cancel a booking.

    Allows an authenticated user to cancel their own booking
    using a PATCH request.

    The booking status is updated to `CANCELLED`.
    """

    serializer_class = BookingCancelSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
