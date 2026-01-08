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


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie detail.

    This serializer is used to represent of a particular movie.
    """

    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    languages = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

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
