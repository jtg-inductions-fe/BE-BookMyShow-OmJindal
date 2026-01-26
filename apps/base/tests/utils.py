from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.base.models import City, Genre, Language
from apps.booking.models import Booking, Ticket
from apps.cinema.models import Cinema
from apps.movie.models import Movie
from apps.slot.models import Slot

User = get_user_model()


class BaseTestUtils(APITestCase):
    """
    BaseTestUtils class to provide utility functions for testcases
    """

    def setUp(self):
        self.user_object = None
        self.superuser_object = None
        self.city_object = None
        self.language_object = None
        self.genre_object = None
        self.cinema_object = None
        self.movie_object = None
        self.slot_object = None
        self.booking_object = None
        self.ticket_object = None
        self.user = {
            "email": "test@test.com",
            "password": "StrongPass@123",
            "confirm_password": "StrongPass@123",
            "name": "Test User",
            "phone_number": "9999999999",
        }
        self.city = {"name": "Jaipur"}
        self.language = {"name": "Mandarin Chinese"}
        self.genre = {"name": "Historic"}
        self.cinema = {
            "name": "PVR",
            "address": "Connaught Place",
            "rows": 50,
            "seats_per_row": 50,
            "image": "/cinema/pvr.jpeg",
        }
        self.movie = {
            "name": "Interstellar",
            "duration": timedelta(minutes=169),
            "description": "Space",
            "release_date": date(2014, 11, 7),
            "poster": "interstellar.jpg",
        }
        self.slot = {
            "price": 250,
            "start_time": timezone.now(),
            "end_time": timezone.now() + timedelta(hours=3),
        }
        self.ticket = {
            "seat_row": 1,
            "seat_column": 1,
        }
        return super().setUp()

    def create_user(self, data={}):
        """
        Function to create a user
        """
        user_data = self.user
        if "confirm_password" in user_data:
            user_data.pop("confirm_password")
        self.user_object = User.objects.create_user(
            **{
                **user_data,
                **data,
            }
        )
        return self.user_object

    def create_superuser(self, data={}):
        """
        Function to create a superuser
        """
        user_data = self.user
        if "confirm_password" in user_data:
            user_data.pop("confirm_password")
        self.superuser_object = User.objects.create_superuser(
            **{
                **self.user,
                **data,
            }
        )
        return self.superuser_object

    def authenticate(self):
        """
        Function to authenticate the user
        """
        response = self.client.post(
            reverse("login"),
            {
                "email": self.user_object.email,
                "password": self.user.get("password"),
            },
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def create_city(self, data={}):
        """
        Function to create a city instance
        """
        self.city_object = City.objects.create(
            **{
                **self.city,
                **data,
            }
        )
        return self.city_object

    def create_language(self, data={}):
        """
        Function to create a language instance
        """
        self.language_object = Language.objects.create(
            **{
                **self.language,
                **data,
            }
        )
        return self.language_object

    def create_genre(self, data={}):
        """
        Function to create a genre instance
        """
        self.genre_object = Genre.objects.create(
            **{
                **self.genre,
                **data,
            }
        )
        return self.genre_object

    def create_cinema(self, city=None, data={}):
        """
        Function to create a cinema instance
        """
        if not (self.city_object or city):
            self.create_city()
        self.cinema_object = Cinema.objects.create(
            city=city or self.city_object,
            **{
                **self.cinema,
                **data,
            },
        )
        return self.cinema_object

    def create_movie(self, data={}):
        """
        Function to create a movie instance
        """
        self.movie_object = Movie.objects.create(
            **{
                **self.movie,
                **data,
            }
        )
        return self.movie_object

    def create_slot(self, movie=None, cinema=None, data={}):
        """
        Function to create a slot instance
        """
        if not (self.movie_object or movie):
            self.create_movie()
        if not (self.cinema_object or cinema):
            self.create_cinema()
        self.slot_object = Slot.objects.create(
            movie=movie or self.movie_object,
            cinema=cinema or self.cinema_object,
            **{
                **self.slot,
                **data,
            },
        )
        return self.slot_object

    def create_booking(self):
        """
        Function to create a booking instance
        """
        if not self.user_object:
            self.create_user()
        if not self.slot_object:
            self.create_slot()
        self.booking_object = Booking.objects.create(
            user=self.user_object,
            slot=self.slot_object,
            status=Booking.BookingStatus.CONFIRMED,
        )
        return self.booking_object

    def create_ticket(self, data={}):
        """
        Function to create a ticket instance
        """
        if not self.booking_object:
            self.create_booking()
        self.ticket_object = Ticket.objects.create(
            booking=self.booking_object,
            **{
                **self.ticket,
                **data,
            },
        )
        return self.ticket_object
