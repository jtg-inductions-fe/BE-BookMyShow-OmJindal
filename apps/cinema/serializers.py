from rest_framework import serializers

from apps.cinema.models import Cinema
from apps.movie.models import Movie
from apps.slot.models import Slot
from apps.base.serializers import CitySerializer


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cinema information.

    This serializer is used in cinema list views and provides
    basic details about a cinema along with its city information.
    """

    city = CitySerializer(read_only=True)

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "address",
            "city",
            "rows",
            "seats_per_row",
            "image",
        ]


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["id", "price", "start_time", "end_time"]


class MovieSerializer(serializers.ModelSerializer):
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


class CinemaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed cinema information.

    This serializer extends basic cinema details by including all
    movie slots available in the cinema.
    """

    city = CitySerializer(read_only=True)
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "address",
            "city",
            "rows",
            "seats_per_row",
            "image",
            "movies",
        ]

    def get_movies(self, cinema):
        movie_map = {}

        for slot in cinema.slots_by_cinema.all():
            movie = slot.movie

            if movie.id not in movie_map:
                movie_map[movie.id] = {
                    "movie": MovieSerializer(movie).data,
                    "slots": [],
                }

            movie_map[movie.id]["slots"].append(SlotSerializer(slot).data)

        return list(movie_map.values())
