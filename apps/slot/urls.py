from django.urls import path

from apps.slot.views import SlotTicketRetrieveSerializer, BookingCreationSerializer

urlpatterns = [
    path(
        "<int:id>/", SlotTicketRetrieveSerializer.as_view(), name="slot-ticket-detail"
    ),
    path("<int:id>/book/", BookingCreationSerializer.as_view(), name="slot-booking"),
]
