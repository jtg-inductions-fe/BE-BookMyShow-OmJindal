from django.urls import path

from apps.movie.views import MovieListAPIView, MovieDetailAPIView, MovieCinemasAPIView

urlpatterns = [
    path("movies/", MovieListAPIView.as_view(), name="movie-list"),
    path("movies/<int:id>/", MovieDetailAPIView.as_view(), name="movie-detail"),
]
