from django.urls import path

from apps.movie.views import MovieListAPIView

urlpatterns = [
    path("", MovieListAPIView.as_view(), name="movie-list"),
]
