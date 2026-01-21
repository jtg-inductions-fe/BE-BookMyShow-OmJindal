from rest_framework import serializers

from apps.base.models import Language, City, Genre


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for Language model.
    """

    class Meta:
        model = Language
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for City model.
    """

    class Meta:
        model = City
        fields = ["id", "name"]


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for Genre model.
    """

    class Meta:
        model = Genre
        fields = ["id", "name"]
