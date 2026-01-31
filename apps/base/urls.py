from django.urls import path

from apps.base import views as base_views

urlpatterns = [
    path("languages/", base_views.LanguageListView.as_view(), name="language-list"),
    path("genres/", base_views.GenreListView.as_view(), name="genre-list"),
    path("cities/", base_views.CityListView.as_view(), name="city-list"),
]
