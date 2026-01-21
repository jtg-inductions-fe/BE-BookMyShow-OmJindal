from django.urls import path

from apps.base.views import LanguageListView, GenreListView

urlpatterns = [
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
]
