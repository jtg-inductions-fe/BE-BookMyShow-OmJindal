from rest_framework import serializers

from apps.movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model.

    This serializer is used to represent movie data in list APIs.
    """

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "duration",
            "release_date",
            "poster",
        ]
