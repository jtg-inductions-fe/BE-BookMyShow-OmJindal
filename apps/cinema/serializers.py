from rest_framework import serializers

from apps.cinema.models import Cinema


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cinema information.

    This serializer is used in cinema list views and provides
    basic details about a cinema along with its city information.
    """

    city = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Cinema
        fields = [
            "id",
            "image",
            "name",
            "city",
            "address",
        ]


class CinemaDetailSerializer(CinemaSerializer):
    """
    Serializer for detailed cinema information.

    This serializer extends basic cinema details by including all
    movie slots available in the cinema.
    """

    movies = serializers.SerializerMethodField()

    class Meta(CinemaSerializer.Meta):
        fields = CinemaSerializer.Meta.fields + ["movies"]

    def get_movies(self, cinema):
        movie_map = {}

        for slot in cinema.slots_by_cinema.all():
            movie = slot.movie
            language = slot.language
            if movie.id not in movie_map:
                movie_map[movie.id] = {
                    "movie": {
                        "id": movie.id,
                        "name": movie.name,
                        "poster": movie.poster,
                        "duration": f"{movie.duration}",
                        "genres": [
                            {"id": g.id, "name": g.name} for g in movie.genres.all()
                        ],
                    },
                    "languages": {},
                }

            language_map = movie_map[movie.id]["languages"]

            if language.id not in language_map:
                language_map[language.id] = {
                    "id": language.id,
                    "name": language.name,
                    "slots": [],
                }

            language_map[language.id]["slots"].append(
                {"id": slot.id, "start_time": slot.start_time, "price": slot.price}
            )

        result = []
        for movie_data in movie_map.values():
            movie_data["languages"] = list(movie_data["languages"].values())
            result.append(movie_data)

        return list(movie_map.values())
