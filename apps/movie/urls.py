from django.urls import path

from apps.movie.views import MovieListAPIView, MovieDetailAPIView

urlpatterns = [
    path("", MovieListAPIView.as_view(), name="movie-list"),
    path("<int:pk>/", MovieDetailAPIView.as_view(), name="movie-detail"),
]
