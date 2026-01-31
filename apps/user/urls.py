from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user import views as user_views

urlpatterns = [
    path("", user_views.ProfileView.as_view(), name="profile"),
    path("signup/", user_views.SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]
