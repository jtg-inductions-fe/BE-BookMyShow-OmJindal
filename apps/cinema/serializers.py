from rest_framework import serializers

from apps.cinema.models import Cinema


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cinema information.

    This serializer is used in cinema list views and provides
    basic details about a cinema along with its city information.
    """

    city = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "address",
            "city",
            "image",
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
                    "movie": {
                        "name": movie.name,
                        "poster": movie.poster,
                        "duration": f"{movie.duration}",
                    },
                    "slots": [],
                }

            movie_map[movie.id]["slots"].append(
                {"id": slot.id, "start_time": slot.start_time}
            )

        return list(movie_map.values())
