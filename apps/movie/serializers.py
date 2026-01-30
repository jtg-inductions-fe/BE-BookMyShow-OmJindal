from rest_framework import serializers as rest_serializers

from apps.movie import models as movie_models


class MovieSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Movie model listing.

    Fields:
        id (int): Unique identifier of the movie.
        poster (str): URL of the movie poster image.
        name (str): The title of the movie.
        genres ([str]): List of genre names associated with the movie.
        duration (str): Duration of the movie.
        languages ([str]): List of language names associated with the movie.
        description (str): Detailed movie description.
    """

    genres = rest_serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    languages = rest_serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = movie_models.Movie
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
    Detailed serializer for a single Movie instance.

    Extends MovieSerializer to include nested cinema and slot data.

    Fields:
        id (int): Unique identifier of the movie.
        poster (str): URL of the movie poster image.
        name (str): The title of the movie.
        genres ([str]): List of genre names associated with the movie.
        duration (int): Duration of the movie.
        languages ([str]): List of language names associated with the movie.
        description (str): Detailed movie description.

        cinemas (list): Contains basic cinema information.
            id (int): Unique identifier of the cinema.
            image (str): URL of the cinema image.
            name (str): Name of the cinema.
            city (str): Name of the city where the cinema is located.
            address (str): Full address of the cinema.

        languages (list): List of languages available.
            id (int): Unique identifier of the language.
            name (str): Name of the language.

            slots (list): List of showtime slots available in this language.
                id (int): Unique identifier of the slot.
                start_time (datetime): Start time of the show.
                price (int): Ticket price for the slot.
    """

    cinemas = rest_serializers.SerializerMethodField()

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ["cinemas"]

    def get_cinemas(self, movie):
        """
        The method provides a hierarchical grouping of available
        showtimes categorized by Cinema and then by Language.
        """
        cinema_map = {}

        for slot in movie.slots.all():
            cinema = slot.cinema
            city = cinema.city
            language = slot.language

            # Initialize cinema entry if not exists
            if cinema.id not in cinema_map:
                request = self.context.get("request")
                image_url = cinema.image.url
                image_url = request.build_absolute_uri(image_url)

                cinema_map[cinema.id] = {
                    "cinema": {
                        "id": cinema.id,
                        "image": image_url,
                        "name": cinema.name,
                        "city": city.name,
                        "address": cinema.address,
                    },
                    "languages": {},
                }

            language_map = cinema_map[cinema.id]["languages"]

            # Initialize language entry within the cinema if not exists
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
        for cinema_data in cinema_map.values():
            cinema_data["languages"] = list(cinema_data["languages"].values())

        return list(cinema_map.values())
