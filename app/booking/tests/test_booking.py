from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import *
from django.contrib.auth import get_user_model

LOGIN_USER_URL = reverse("user:login")


def create_user(**kwargs):
    """Create and return new user"""
    kwargs.pop("confirm_password")
    return get_user_model().objects.create_user(**kwargs)

class TestingBookingView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.city = {"name":"testing city 3","slug":"testing-slug-3"}
        self.movie = {"title":"testing3","description":"testing description3",
                      "duration":"2:00","release_date":"2020-04-20",
                      "language":"english","certificate":"UA",
                      "slug":"testing-slug-3"}
        self.theater = {"name":"theater3","slug":"theater-slug-3",
                        "address":"theater-address"}
        self.show = {"slug":"testing-show-3","start_date":"2023-05-01",
                     "end_date":"2023-05-01","start_time":"08:30",
                     "end_time":"11:00"}
        self.screen = {"name":"testing screen 3",
                       "slug":"testing-screen-slug-3"}

    def test_book_seats_view(self):

        city_obj = City.objects.create(**self.city)
        self.assertIsNotNone(city_obj)
        theater_obj = Theater.objects.create(**self.theater,city=city_obj)
        self.assertIsNotNone(theater_obj)
        movie_obj = Movie.objects.create(**self.movie)
        self.assertIsNotNone(movie_obj)
        show_obj = Show.objects.create(**self.show,movie=movie_obj)
        self.assertIsNotNone(show_obj)
        screen_obj = Screen.objects.create(**self.screen,theater=theater_obj)
        self.assertIsNotNone(screen_obj)
        screen_show_obj = ScreenShowMapper.objects.create(
            show=show_obj,screen=screen_obj,slug="testing-screen-show-mapper"
        )
        self.assertIsNotNone(screen_show_obj)
        seating_class_obj=SeatingClass.objects.create(name="Silver",
                                                      slug="silver")
        self.assertIsNotNone(seating_class_obj)
        fare_obj = Fare.objects.create(screen_show=screen_show_obj,
                                       seating_class=seating_class_obj,
                                       price=400,slug="testing-screen-show-400"
                                       )
        self.assertIsNotNone(fare_obj)
        seat_obj = Seat.objects.create(row=1,column=1,is_available=True,
                                       slug="seat-1-1",screen=screen_obj,
                                       fare=fare_obj)
        self.assertIsNotNone(seat_obj)
        data={
            "booking_date":"2023-06-06",
            "screen_show" : str(screen_show_obj.slug),
            "seats":[{
                "seating_class":seating_class_obj.slug,
                "row":seat_obj.row,
                "column":seat_obj.column
            }]
        }
        user_details = {
            "name": "Test name",
            "email": "test@example.com",
            "password": "testingpassword",
            "confirm_password": "testingpassword",
        }
        user = create_user(**user_details)
        payload = {"email": user_details["email"],
                   "password": user_details["password"]}
        res_login = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(res_login.status_code,status.HTTP_200_OK)
        headers = {
        'HTTP_AUTHORIZATION': 'Bearer {}'.format(
            res_login.data['access_token'])
        }
        res = self.client.post(f"api/booking/seat-booking/",
                               data=data,headers=headers)
        self.assertEqual(res.status_code,status.HTTP_200_OK)


    def test_payment_view(self):
        pass