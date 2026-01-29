from rest_framework import filters as rest_filters
from rest_framework import generics as rest_generics

from apps.base import models as base_models
from apps.base import serializers as base_serializers


class LanguageListView(rest_generics.ListAPIView):
    """
    API view to retrieve a list of all genres.

    Method: GET
        Parameters: None
        Response:
            200 OK:
                Returns a JSON array of language objects sorted in ascending
                alphabetical order by language name.
                Example:
                [
                    {
                        "id": 1,
                        "name": "english"
                    },
                ]
    """

    queryset = base_models.Language.objects.all()
    serializer_class = base_serializers.LanguageSerializer


class GenreListView(rest_generics.ListAPIView):
    """
    API view to retrieve a list of all genres.

    Method: GET
        Parameters: None
        Response:
            200 OK:
                Returns a JSON array of genre objects sorted in ascending
                alphabetical order by genre name.
                Example:
                [
                    {
                        "id": 1,
                        "name": "action"
                    },
                ]
    """

    queryset = base_models.Genre.objects.all()
    serializer_class = base_serializers.GenreSerializer


class CityListView(rest_generics.ListAPIView):
    """
    API view to retrieve a list of all cities.

    It supports searching cities by name as a search
    query paramter.

    Method: GET
        Parameters:
            search (str, optional, query parameter):
                Filters cities by partial or full name match.
                Example: /cities/?search=Mum
        Response:
            200 OK:
                Returns a JSON array of city objects sorted in ascending
                alphabetical order by city name.
                Example:
                [
                    {
                        "id": 1,
                        "name": "mumbai",
                    }
                ]
    """

    queryset = base_models.City.objects.all()
    serializer_class = base_serializers.CitySerializer
    filter_backends = [rest_filters.SearchFilter]
    search_fields = ["name"]
