from django.urls import path

from apps.user.views import (
    SignupView,
    LoginView,
    ProfileView,
    LogoutView,
    ProfileUpdateView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view, name="profile"),
    path("profile/update/", ProfileUpdateView.as_view, name="profile_update"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
