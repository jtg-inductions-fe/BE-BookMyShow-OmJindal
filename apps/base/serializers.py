from rest_framework import serializers as rest_serializers

from apps.base import models as base_models


class LanguageSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Language model.
    """

    class Meta:
        model = base_models.Language
        fields = ["id", "name"]


class CitySerializer(rest_serializers.ModelSerializer):
    """
    Serializer for City model.
    """

    class Meta:
        model = base_models.City
        fields = ["id", "name"]


class GenreSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Genre model.
    """

    class Meta:
        model = base_models.Genre
        fields = ["id", "name"]
