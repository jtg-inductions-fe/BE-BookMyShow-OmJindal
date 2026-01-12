from django.urls import path

from apps.slot.views import SlotTicketRetrieveView, BookingCreationView

urlpatterns = [
    path("<int:id>/", SlotTicketRetrieveView.as_view(), name="slot-ticket-detail"),
    path("<int:id>/book/", BookingCreationView.as_view(), name="slot-booking"),
]
