from rest_framework import serializers

from apps.movie.models import Movie
from apps.cinema.serializers import CinemaSerializer, SlotSerializer


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    languages = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "duration",
            "release_date",
            "poster",
            "genres",
            "languages",
        ]


class MovieCinemasSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a movie along with the cinemas
    and slots where it is currently playing.
    """

    cinemas = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "cinemas",
            "genres",
            "description",
            "duration",
            "release_date",
            "poster",
        ]

    def get_cinemas(self, movie):
        cinema_map = {}

        for slot in movie.slots_by_movie.all():
            cinema = slot.cinema
            city = cinema.city
            if cinema.id not in cinema_map:
                cinema_map[cinema.id] = {
                    "cinema": {
                        "name": cinema.name,
                        "address": cinema.address,
                        "city": city.name,
                        "image": cinema.image,
                    },
                    "slots": [],
                }

            cinema_map[cinema.id]["slots"].append(
                {"id": slot.id, "start_time": slot.start_time}
            )

        return list(cinema_map.values())
