from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.base.tests.utils import BaseTestUtils


class CinemaListViewTests(BaseTestUtils):
    """
    CinemaListViewTests should return list of cinemas
    """

    def test_cinema_list_returns_cinemas(self):
        self.cinema1 = self.create_cinema(data={"name": "PVR"})
        self.cinema2 = self.create_cinema(data={"name": "INOX"})
        response = self.client.get(reverse("cinemas-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "PVR")
        self.assertEqual(results[1]["name"], "INOX")


class CinemaListViewFilterTests(BaseTestUtils):
    """
    CinemaListViewFilterTests should return filtered
    list of cinemas based on city
    """

    def test_cinema_list_returns_filtered_cinemas(self):
        city1 = self.create_city(data={"name": "Jaipur"})
        city2 = self.create_city(data={"name": "Yamunanagar"})

        self.cinema1 = self.create_cinema(city=city1, data={"name": "PVR"})
        self.cinema2 = self.create_cinema(city=city2, data={"name": "PVR"})
        self.cinema3 = self.create_cinema(city=city1, data={"name": "INOX"})

        response1 = self.client.get(
            reverse("cinemas-list"),
            {"city": city1.id},
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        results1 = response1.data["results"]
        self.assertEqual(len(results1), 2)
        self.assertEqual(results1[0]["name"], "PVR")
        self.assertEqual(results1[1]["name"], "INOX")


class CinemaDetailViewFTests(BaseTestUtils):
    """
    CinemaDetailViewFCinemaDetailViewFTestsilterTests should return detail of a particular
    cinema along with movie and slot details
    """

    def test_cinema_detail_returns_movies_and_slots(self):
        movie1 = self.create_movie({"name": "Harry Potter"})
        movie2 = self.create_movie({"name": "Stranger Things"})

        self.create_cinema()

        self.slot1 = self.create_slot(
            movie=movie1,
            data={"start_time": timezone.now()},
        )
        self.slot2 = self.create_slot(
            movie=movie1,
            data={"start_time": timezone.now() + timedelta(hours=2)},
        )
        self.slot3 = self.create_slot(
            movie=movie2,
            data={"start_time": timezone.now()},
        )

        response = self.client.get(reverse("cinemas-detail", args=[self.cinema_object.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["id"], self.cinema_object.id)
        self.assertEqual(data["name"], self.cinema_object.name)

        movies = data["movies"]
        self.assertEqual(len(movies), 2)

        movie_map = {m["movie"]["name"]: len(m["slots"]) for m in movies}

        self.assertEqual(movie_map["Harry Potter"], 2)
        self.assertEqual(movie_map["Stranger Things"], 1)
