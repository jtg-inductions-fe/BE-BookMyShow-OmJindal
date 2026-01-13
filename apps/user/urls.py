from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.views import (
    SignupView,
    ProfileView,
    PurchaseHistoryView,
    BookingCancelView
)

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("bookings/", PurchaseHistoryView.as_view(), name="user-purchase-history"),
    path("bookings/<int:pk>/", BookingCancelView.as_view(), name="booking-cancel"),
]
