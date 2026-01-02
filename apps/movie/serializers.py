from rest_framework import serializers

from apps.movie.models import Movie
from apps.base.serializers import GenreSerializer, LanguageSerializer


class MovieSerializer(serializers.ModelSerializer):
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
