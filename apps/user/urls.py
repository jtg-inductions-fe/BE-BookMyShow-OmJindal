from django.urls import path

from apps.user.views import (
    SignupView,
    LoginView,
    ProfileView,
    LogoutView,
    CookieTokenRefreshView,
)

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="logout"),
]
