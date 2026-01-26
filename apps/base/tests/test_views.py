from django.urls import reverse
from rest_framework import status

from apps.base.tests.utils import BaseTestUtils


class LanguageListViewTests(BaseTestUtils):
    """
    LanguageListViewTests should return list of languages
    """

    def setUp(self):
        super().setUp()
        self.create_language({"name": "Spanish"})
        self.create_language({"name": "French"})

    def test_language_list_returns_languages(self):
        response = self.client.get(reverse("language-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "Spanish")
        self.assertEqual(results[1]["name"], "French")


class GenreListViewTests(BaseTestUtils):
    """
    LanguageListViewTests should return list of genres
    """

    def setUp(self):
        super().setUp()
        self.create_genre({"name": "Horror"})
        self.create_genre({"name": "Comedy"})

    def test_language_list_returns_languages(self):
        response = self.client.get(reverse("genre-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "Horror")
        self.assertEqual(results[1]["name"], "Comedy")


class CityListViewTests(BaseTestUtils):
    """
    LanguageListViewTests should return list of cities
    """

    def setUp(self):
        super().setUp()
        self.create_city({"name": "Lucknow"})
        self.create_city({"name": "Khizrabad"})

    def test_language_list_returns_languages(self):
        response = self.client.get(reverse("city-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "Lucknow")
        self.assertEqual(results[1]["name"], "Khizrabad")
