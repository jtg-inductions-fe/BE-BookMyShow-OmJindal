from rest_framework import serializers

from apps.movie.models import Movie
from apps.base.serializers import GenreSerializer, LanguageSerializer


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model.

    This serializer is used to represent movie data in list APIs.
    It includes nested, read-only representations of related
    genres and languages to provide complete contextual
    information for each movie.
    """

    genres = GenreSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "description",
            "duration",
            "release_date",
            "poster",
            "languages",
            "genres",
        ]
