from rest_framework import serializers

from apps.movie.models import Movie
from apps.cinema.serializers import CinemaSerializer, SlotSerializer


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


class MovieCinemasSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a movie along with the cinemas
    and slots where it is currently playing.
    """

    cinemas = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "cinemas",
        ]

    def get_cinemas(self, movie):
        cinema_map = {}

        for slot in movie.slots_by_movie.all():
            cinema = slot.cinema

            if cinema.id not in cinema_map:
                cinema_map[cinema.id] = {
                    "cinema": CinemaSerializer(cinema).data,
                    "slots": [],
                }

            cinema_map[cinema.id]["slots"].append(SlotSerializer(slot).data)

        return list(cinema_map.values())
