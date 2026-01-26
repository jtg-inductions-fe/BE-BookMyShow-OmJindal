from datetime import date, timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.base.tests.utils import BaseTestUtils


class MovieListViewTests(BaseTestUtils):
    """
    MovieListViewTests to test movie list retrieval
    """

    def test_movie_list_returns_movies(self):
        self.movie1 = self.create_movie(data={"name": "Movie A", "release_date": date(2010, 1, 1)})
        self.movie2 = self.create_movie(data={"name": "Movie B", "release_date": date(2020, 1, 1)})
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "Movie B")
        self.assertEqual(results[1]["name"], "Movie A")


class MovieListViewFilterTests(BaseTestUtils):
    """
    MovieListViewFilterTests to test list of movie retrieval
    based on filter of langauge, genre, latest_days
    """

    def test_movie_list_returns_filtered_movies(self):
        self.genre1 = self.create_genre(data={"name": "Actionable"})
        self.genre2 = self.create_genre(data={"name": "Scientific"})
        self.language1 = self.create_language(data={"name": "Spanish"})
        self.language2 = self.create_language(data={"name": "French"})

        self.movie1 = self.create_movie(data={"name": "Movie A", "release_date": date(2026, 1, 10)})
        self.movie2 = self.create_movie(data={"name": "Movie B", "release_date": date(2026, 1, 5)})
        self.movie3 = self.create_movie(data={"name": "Movie C", "release_date": date(2026, 1, 1)})

        self.movie1.genres.add(self.genre1, self.genre2)
        self.movie1.languages.add(self.language1, self.language2)
        self.movie2.genres.add(self.genre1)
        self.movie2.languages.add(self.language1)
        self.movie3.genres.add(self.genre2)
        self.movie3.languages.add(self.language2)

        response1 = self.client.get(
            reverse("movie-list"),
            {"language": f"{self.language1.id}", "genres": f"{self.genre1.id}"},
        )
        response2 = self.client.get(
            reverse("movie-list"),
            {"language": f"{self.language2.id}", "genres": f"{self.genre2.id}"},
        )
        response3 = self.client.get(
            reverse("movie-list"),
            {"language": f"{self.language2.id},{self.language1.id}"},
        )
        response4 = self.client.get(
            reverse("movie-list"),
            {"latest_days": 7},
        )

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        results1 = response1.data["results"]
        self.assertEqual(len(results1), 2)
        self.assertEqual(results1[0]["name"], "Movie A")
        self.assertEqual(results1[1]["name"], "Movie B")

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        results2 = response2.data["results"]
        self.assertEqual(len(results2), 2)

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        results3 = response3.data["results"]
        self.assertEqual(len(results3), 3)

        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        results4 = response4.data["results"]
        self.assertEqual(len(results4), 2)


class MovieDetailViewTests(BaseTestUtils):
    """
    MovieDetailViewTests to test particular movie retrieval
    """

    def test_movie_detail_returns_cinemas_and_slots(self):
        self.create_movie()

        self.city1 = self.create_city(data={"name": "Radaur"})
        self.city2 = self.create_city(data={"name": "KUK"})

        self.cinema1 = self.create_cinema(city=self.city1, data={"name": "PVR"})
        self.cinema2 = self.create_cinema(city=self.city2, data={"name": "INOX"})

        self.slot1 = self.create_slot(
            cinema=self.cinema1,
            data={"start_time": timezone.now()},
        )
        self.slot2 = self.create_slot(
            cinema=self.cinema1,
            data={"start_time": timezone.now() + timedelta(hours=2)},
        )
        self.slot3 = self.create_slot(
            cinema=self.cinema2,
            data={"start_time": timezone.now()},
        )

        response = self.client.get(reverse("movie-detail", args=[self.movie_object.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.movie_object.id)
        self.assertEqual(data["name"], self.movie_object.name)

        cinemas = data["cinemas"]
        self.assertEqual(len(cinemas), 2)

        cinema_map = {c["cinema"]["name"]: len(c["slots"]) for c in cinemas}

        self.assertEqual(cinema_map["PVR"], 2)
        self.assertEqual(cinema_map["INOX"], 1)


class MovieDetailCityFilterTests(BaseTestUtils):
    """
    MovieDetailViewTests to test particular movie retrieval
    and filter cinema based on city
    """

    def test_movie_detail_city_filter(self):
        self.create_movie()

        city_delhi = self.create_city(data={"name": "Vrindavan"})
        city_mumbai = self.create_city(data={"name": "Chennai"})

        cinema_delhi = self.create_cinema(city=city_mumbai)
        cinema_mumbai = self.create_cinema(city=city_delhi)

        self.create_slot(cinema=cinema_delhi)
        self.create_slot(cinema=cinema_mumbai)

        response = self.client.get(
            reverse("movie-detail", args=[self.movie_object.id]),
            {"city": city_delhi.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cinemas = response.data["cinemas"]

        self.assertEqual(len(cinemas), 1)
        self.assertEqual(
            cinemas[0]["cinema"]["city"],
            city_delhi.id,
        )
