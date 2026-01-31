from rest_framework import serializers as rest_serializers

from apps.base import models as base_models


class LanguageSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Language model.

    Converts Language model instances into JSON format and validates
    incoming data for language-related operations.

    Fields:
        id (int): Unique identifier of the language.
        name (str): Name of the language.
    """

    class Meta:
        model = base_models.Language
        fields = ["id", "name"]


class CitySerializer(rest_serializers.ModelSerializer):
    """
    Serializer for City model.

    Converts City model instances into JSON format and validates
    incoming data for city-related operations.

    Fields:
        id (int): Unique identifier of the city.
        name (str): Name of the city.
    """

    class Meta:
        model = base_models.City
        fields = ["id", "name"]


class GenreSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Genre model.

    Converts Genre model instances into JSON format and validates
    incoming data for genre-related operations.

    Fields:
        id (int): Unique identifier of the genre.
        name (str): Name of the genre.
    """

    class Meta:
        model = base_models.Genre
        fields = ["id", "name"]
