from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from apps.user.views import SignupView, ProfileView, BookingViewSet

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("", include(router.urls)),
]
