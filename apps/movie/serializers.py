from rest_framework import serializers

from apps.movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    languages = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "poster",
            "name",
            "genres",
            "duration",
            "languages",
            "description",
        ]


class MovieDetailSerializer(MovieSerializer):
    """
    Serializer to represent a movie along with the cinemas
    and slots where it is currently playing.
    """

    cinemas = serializers.SerializerMethodField()

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ["cinemas"]

    def get_cinemas(self, movie):
        cinema_map = {}

        for slot in movie.slots_by_movie.all():
            cinema = slot.cinema
            city = cinema.city
            language = slot.language
            if cinema.id not in cinema_map:
                cinema_map[cinema.id] = {
                    "cinema": {
                        "id": cinema.id,
                        "image": cinema.image,
                        "name": cinema.name,
                        "city": city.name,
                        "address": cinema.address,
                    },
                    "languages": {},
                }

            language_map = cinema_map[cinema.id]["languages"]

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
        for cinema_data in cinema_map.values():
            cinema_data["languages"] = list(cinema_data["languages"].values())
            result.append(cinema_data)

        return list(cinema_map.values())
