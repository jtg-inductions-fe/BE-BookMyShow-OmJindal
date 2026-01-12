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


class MovieCinemasSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a movie along with the cinemas
    and slots where it is currently playing.
    """

    cinemas = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = ["id", "name", "cinemas", "genres"]

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
