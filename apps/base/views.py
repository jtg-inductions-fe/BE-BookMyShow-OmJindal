from rest_framework import filters as rest_filters
from rest_framework import generics as rest_generics

from apps.base import models as base_models
from apps.base import serializers as base_serializers


class LanguageListView(rest_generics.ListAPIView):
    """
    API view to retrieve a list of all languages.

    Returns:
        HTTP 200: A list of language objects.
    """

    queryset = base_models.Language.objects.all()
    serializer_class = base_serializers.LanguageSerializer


class GenreListView(rest_generics.ListAPIView):
    """
    API view to retrieve a list of all genres.

    Returns:
        HTTP 200: A list of genre objects.
    """

    queryset = base_models.Genre.objects.all()
    serializer_class = base_serializers.GenreSerializer


class CityListView(rest_generics.ListAPIView):
    """
    API view to retrieve a list of all cities.

    Query Parameters:
        search (str): Optional. Filter cities by name (e.g., /cities/?search=Mum).

    Returns:
        HTTP 200: A list of city objects matching the search criteria.
    """

    queryset = base_models.City.objects.all()
    serializer_class = base_serializers.CitySerializer
    filter_backends = [rest_filters.SearchFilter]
    search_fields = ["name"]
