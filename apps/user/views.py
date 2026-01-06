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
    BookingCancelSerializer
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
    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects.filter(user=self.request.user)
            .prefetch_related("tickets_by_booking")
            .select_related("slot", "slot__cinema", "slot__movie")
        )


class BookingCancelView(UpdateAPIView):
    serializer_class = BookingCancelSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
