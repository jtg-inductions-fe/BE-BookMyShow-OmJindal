from django.urls import path

from apps.movie.views import MovieListAPIView, MovieDetailAPIView, MovieCinemasAPIView

urlpatterns = [
    path("", MovieListAPIView.as_view(), name="movie-list"),
    path("<int:pk>/", MovieDetailAPIView.as_view(), name="movie-detail"),
    path("<int:pk>/cinemas/", MovieCinemasAPIView.as_view(), name="movie-cinemas"),
]
