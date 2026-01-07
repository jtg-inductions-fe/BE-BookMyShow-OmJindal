from rest_framework import serializers

from apps.cinema.models import Cinema
from apps.movie.models import Movie
from apps.slot.models import Slot


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cinema information.

    This serializer is used in cinema list views and provides
    basic details about a cinema along with its city information.
    """

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "address",
            "city",
            "image",
        ]


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["id", "start_time"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "duration",
            "poster",
        ]


class CinemaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed cinema information.

    This serializer extends basic cinema details by including all
    movie slots available in the cinema.
    """

    city = serializers.SlugRelatedField(read_only=True, slug_field="name")
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "address",
            "city",
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
