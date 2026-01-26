from rest_framework import serializers as rest_serializers

from apps.movie import models as movie_models


class MovieSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for Movie model listing.

    This serializer provides basic movie details and uses slug fields
    to represent Many-to-Many relationships for genres and languages.

    Attributes:
        genres (SlugRelatedField): A list of genre names.
        languages (SlugRelatedField): A list of language names.
    """

    genres = rest_serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    languages = rest_serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

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
    """

    cinemas = rest_serializers.SerializerMethodField()

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ["cinemas"]

    def get_cinemas(self, movie):
        """
        The method provides a hierarchical grouping of available
        showtimes categorized by Cinema and then by Language.

        Args:
            movie (Movie): The Movie instance being serialized.

        Returns:
            list: A list of cinema dictionaries, each containing nested
                  languages and their respective showtime slots.
        """
        cinema_map = {}

        for slot in movie.slots.all():
            cinema = slot.cinema
            city = cinema.city
            language = slot.language

            # Initialize cinema entry if not exists
            if cinema.id not in cinema_map:
                request = self.context.get("request")
                image_url = None
                if cinema.image:
                    image_url = (
                        request.build_absolute_uri(cinema.image.url)
                        if request
                        else cinema.image.url
                    )

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

        # Convert dictionary maps back into lists for JSON response
        for cinema_data in cinema_map.values():
            cinema_data["languages"] = list(cinema_data["languages"].values())

        return list(cinema_map.values())
