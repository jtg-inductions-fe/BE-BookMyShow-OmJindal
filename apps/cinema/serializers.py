from rest_framework import serializers

from apps.cinema import models as cinema_models


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cinema information.

    Attributes:
        city (SlugRelatedField): Displays the city name instead of the ID.
    """

    city = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = cinema_models.Cinema
        fields = [
            "id",
            "image",
            "name",
            "city",
            "address",
        ]


class CinemaDetailSerializer(CinemaSerializer):
    """
    Detailed serializer for a single Cinema instance.

    Extends CinemaSerializer to include nested movie and slot data.
    """

    movies = serializers.SerializerMethodField()

    class Meta(CinemaSerializer.Meta):
        fields = CinemaSerializer.Meta.fields + ["movies"]

    def get_movies(self, cinema):
        """
        The method provides a hierarchical grouping of available
        showtimes categorized by movies and then by Language.

        Args:
            cinema (Cinema): The cinema instance being serialized.

        Returns:
            list: A structured list of movies and slots.
        """
        movie_map = {}
        request = self.context.get("request")

        for slot in cinema.slots.all():
            movie = slot.movie
            language = slot.language

            # Initialize movie entry if not exists
            if movie.id not in movie_map:
                poster_url = movie.poster.url if movie.poster else None
                if poster_url and request:
                    poster_url = request.build_absolute_uri(poster_url)

                movie_map[movie.id] = {
                    "movie": {
                        "id": movie.id,
                        "name": movie.name,
                        "poster": poster_url,
                        "duration": str(movie.duration),
                        "genres": [{"id": g.id, "name": g.name} for g in movie.genres.all()],
                    },
                    "languages": {},
                }

            language_map = movie_map[movie.id]["languages"]

            # Initialize language entry within the movie if not exists
            if language.id not in language_map:
                language_map[language.id] = {
                    "id": language.id,
                    "name": language.name,
                    "slots": [],
                }

            # Append showtime details to the language group
            language_map[language.id]["slots"].append(
                {"id": slot.id, "start_time": slot.start_time, "price": slot.price}
            )

        # Convert dictionary maps back into lists for JSON response
        for movie_data in movie_map.values():
            movie_data["languages"] = list(movie_data["languages"].values())

        return list(movie_map.values())
