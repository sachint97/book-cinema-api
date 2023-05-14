"""Test for booking API's"""


from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import (City, Movie, Theater, Screen, Show, ScreenShowMapper,
                         SeatingClass, Fare, Seat, BookingSeat, Booking)
from django.contrib.auth import get_user_model

BOOKING_URL = reverse("booking:ticket-booking")
PAYMENT_URL = reverse("booking:payment")


class TestingBookingView(TestCase):
    """Create and test for booking and payments."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_book_seats_view(self):
        """Test booking seats of a particular show."""

        self.assertTrue(self.client.credentials)
        city = {"name": "testing city 3", "slug": "testing-slug-3"}
        movie = {
            "title": "testing3",
            "description": "testing description3",
            "duration": "2:00",
            "release_date": "2020-04-20",
            "language": "english",
            "certificate": "UA",
            "slug": "testing-slug-3",
        }
        theater = {
            "name": "theater3",
            "slug": "theater-slug-3",
            "address": "theater-address",
        }
        show = {
            "slug": "testing-show-3",
            "start_date": "2023-05-01",
            "end_date": "2023-05-01",
            "start_time": "08:30",
            "end_time": "11:00",
        }
        screen = {"name": "testing screen 3", "slug": "testing-screen-slug-3"}

        city_obj = City.objects.create(**city)
        self.assertIsNotNone(city_obj)
        theater_obj = Theater.objects.create(**theater, city=city_obj)
        self.assertIsNotNone(theater_obj)
        movie_obj = Movie.objects.create(**movie)
        self.assertIsNotNone(movie_obj)
        show_obj = Show.objects.create(**show, movie=movie_obj)
        self.assertIsNotNone(show_obj)
        screen_obj = Screen.objects.create(**screen, theater=theater_obj)
        self.assertIsNotNone(screen_obj)
        screen_show_obj = ScreenShowMapper.objects.create(
            show=show_obj, screen=screen_obj, slug="testing-screen-show-mapper"
        )
        self.assertIsNotNone(screen_show_obj)
        seating_class_obj = SeatingClass.objects.create(
            name="Silver", slug="silver"
        )
        self.assertIsNotNone(seating_class_obj)
        fare_obj = Fare.objects.create(
            screen_show=screen_show_obj,
            seating_class=seating_class_obj,
            price=400,
            slug="testing-screen-show-400",
        )
        self.assertIsNotNone(fare_obj)
        seat_obj = Seat.objects.create(
            row=1,
            column=1,
            is_available=True,
            slug="seat-1-1",
            screen=screen_obj,
            fare=fare_obj,
        )
        self.assertIsNotNone(seat_obj)
        data = {
            "booking_date": "2023-06-06",
            "screen_show": str(screen_show_obj.slug),
            "seats": [
                {
                    "seating_class": seating_class_obj.slug,
                    "row": seat_obj.row,
                    "column": seat_obj.column,
                }
            ],
        }
        res = self.client.post(BOOKING_URL, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_payment_view(self):
        """Test for Payment success."""

        city = {"name": "testing city 4", "slug": "testing-slug-4"}
        movie = {
            "title": "testing4",
            "description": "testing description4",
            "duration": "2:00",
            "release_date": "2020-04-20",
            "language": "english",
            "certificate": "UA",
            "slug": "testing-slug-4",
        }
        theater = {
            "name": "theater4",
            "slug": "theater-slug-4",
            "address": "theater-address",
        }
        show = {
            "slug": "testing-show-4",
            "start_date": "2023-05-01",
            "end_date": "2023-05-01",
            "start_time": "08:30",
            "end_time": "11:00",
        }
        screen = {"name": "testing screen 4", "slug": "testing-screen-slug-4"}

        city_obj = City.objects.create(**city)
        self.assertIsNotNone(city_obj)
        theater_obj = Theater.objects.create(**theater, city=city_obj)
        self.assertIsNotNone(theater_obj)
        movie_obj = Movie.objects.create(**movie)
        self.assertIsNotNone(movie_obj)
        show_obj = Show.objects.create(**show, movie=movie_obj)
        self.assertIsNotNone(show_obj)
        screen_obj = Screen.objects.create(**screen, theater=theater_obj)
        self.assertIsNotNone(screen_obj)
        screen_show_obj = ScreenShowMapper.objects.create(
            show=show_obj,
            screen=screen_obj,
            slug="testing-screen-show-mapper-1",
        )
        self.assertIsNotNone(screen_show_obj)
        seating_class_obj = SeatingClass.objects.create(
            name="Gold", slug="gold"
        )
        self.assertIsNotNone(seating_class_obj)
        fare_obj = Fare.objects.create(
            screen_show=screen_show_obj,
            seating_class=seating_class_obj,
            price=600,
            slug="testing-screen-show-600",
        )
        self.assertIsNotNone(fare_obj)
        seat_obj = Seat.objects.create(
            row=1,
            column=1,
            is_available=True,
            slug="gold-seat-1-1",
            screen=screen_obj,
            fare=fare_obj,
        )
        self.assertIsNotNone(seat_obj)
        booking_obj = Booking.objects.create(
            user=self.user,
            screen_show=screen_show_obj,
            booking_date="2023-06-06",
            slug="booking-slug-1",
        )
        self.assertIsNotNone(booking_obj)
        booking_seat_obj = BookingSeat.objects.create(
            seat=seat_obj,
            booking=booking_obj,
            booking_status=True,
            slug="booking-seat-slug-1",
        )
        self.assertIsNotNone(booking_seat_obj)
        data = {
            "booking": str(booking_obj.slug),
            "amount": 600,
            "payment_method": "UPI",
        }
        res = self.client.post(PAYMENT_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
