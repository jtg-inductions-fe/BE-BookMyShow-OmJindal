from rest_framework import serializers as rest_serializers

from apps.cinema import models as cinema_models


class CinemaSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Cinema model listing.

    Fields:
        id (int): Unique identifier of the cinema.
        image (str): URL of the cinema image.
        name (str): Name of the cinema.
        city (str): Name of the city where the cinema is located.
        address (str): Full address of the cinema.
    """

    city = rest_serializers.SlugRelatedField(read_only=True, slug_field="name")

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

    Fields:
        id (int): Unique identifier of the cinema.
        image (str): URL of the cinema image.
        name (str): Name of the cinema.
        city (str): Name of the city where the cinema is located.
        address (str): Full address of the cinema.

        movies (list): Contains basic movie information.
            id (int): Unique identifier of the movie.
            name (str): The title of the movie.
            poster (str): URL of the movie poster image.
            duration (str): Duration of the movie.
            genres ([str]): List of genre names associated with the movie.

        languages (list): List of languages available.
            id (int): Unique identifier of the language.
            name (str): Name of the language.

            slots (list): List of showtime slots available in this language.
                id (int): Unique identifier of the slot.
                start_time (datetime): Start time of the show.
                price (int): Ticket price for the slot.
    """

    movies = rest_serializers.SerializerMethodField()

    class Meta(CinemaSerializer.Meta):
        fields = CinemaSerializer.Meta.fields + ["movies"]

    def get_movies(self, cinema):
        """
        The method provides a hierarchical grouping of available
        showtimes categorized by Movie and then by Language.
        """
        movie_map = {}

        for slot in cinema.slots.all():
            movie = slot.movie
            language = slot.language

            # Initialize movie entry if not exists
            if movie.id not in movie_map:
                request = self.context.get("request")
                poster_url = movie.poster.url
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

        # Convert dictionary maps back into lists
        for movie_data in movie_map.values():
            movie_data["languages"] = list(movie_data["languages"].values())

        return list(movie_map.values())
