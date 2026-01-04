from django.urls import path

from apps.cinema.views import CinemaListAPIView, CinemaDetailAPIView

urlpatterns = [
    path("", CinemaListAPIView.as_view(), name="cinema-list"),
    path("<int:pk>/", CinemaDetailAPIView.as_view(), name="cinema-detail"),
]