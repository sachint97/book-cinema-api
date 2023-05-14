from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import *


class TheaterViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_movie_by_city(self):
        city = {"name":"testing city","slug":"testing-slug"}
        movie = {"title":"testing","description":"testing description",
                      "duration":"2:00","release_date":"2020-04-20",
                      "language":"english","certificate":"UA",
                      "slug":"testing-slug"}
        theater = {"name":"theater","slug":"theater-slug",
                        "address":"theater-address"}
        city_obj = City.objects.create(**city)
        theater_obj = Theater.objects.create(**theater,city=city_obj)
        movie_obj = Movie.objects.create(**movie)
        res = self.client.get(f"/api/theater/movies/{city['slug']}/")
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_shows_by_movies(self):
        city = {"name":"testing city 1","slug":"testing-slug-1"}
        movie = {"title":"testing1","description":"testing description 1",
                      "duration":"2:00","release_date":"2020-04-20",
                      "language":"english","certificate":"UA",
                      "slug":"testing-slug-1"}
        show = {"slug":"testing-show","start_date":"2023-05-01",
                     "end_date":"2023-05-01","start_time":"08:30",
                     "end_time":"11:00"}
        city_obj = City.objects.create(**city)
        movie_obj = Movie.objects.create(**movie)
        show_obj = Show.objects.create(**show,movie=movie_obj)
        res = self.client.get(
            f"/api/theater/shows/?city={city['slug']}&movie={movie['slug']}")
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        res1 = self.client.get(
            f"/api/theater/shows/?city={city['slug']}")
        self.assertEqual(res1.status_code,status.HTTP_200_OK)

        res2 = self.client.get(
            f"/api/theater/shows/?&movie={movie['slug']}")
        self.assertEqual(res2.status_code,status.HTTP_200_OK)

    def test_seating_by_show_view(self):
        city = {"name":"testing city","slug":"testing-slug"}
        movie = {"title":"testing","description":"testing description",
                      "duration":"2:00","release_date":"2020-04-20",
                      "language":"english","certificate":"UA",
                      "slug":"testing-slug"}
        theater = {"name":"theater","slug":"theater-slug",
                        "address":"theater-address"}
        show = {"slug":"testing-show","start_date":"2023-05-01",
                     "end_date":"2023-05-01","start_time":"08:30",
                     "end_time":"11:00"}
        screen = {"name":"testing screen","slug":"testing-screen-slug"}
        city_obj = City.objects.create(**city)
        theater_obj = Theater.objects.create(**theater,city=city_obj)
        movie_obj = Movie.objects.create(**movie)
        show_obj = Show.objects.create(**show,movie=movie_obj)
        screen_obj = Screen.objects.create(**screen,theater=theater_obj)
        screen_show_obj = ScreenShowMapper.objects.create(
            show=show_obj,screen=screen_obj,slug="testing-screen-show-mapper"
        )
        seating_class_obj=SeatingClass.objects.create(name="Gold",slug="gold")
        fare_obj = Fare.objects.create(screen_show=screen_show_obj,
                                       seating_class=seating_class_obj,
                                       price=400,slug="testing-screen-show-400"
                                       )
        seat_obj = Seat.objects.create(row=1,column=1,is_available=True,
                                       slug="seat-1-1",screen=screen_obj,
                                       fare=fare_obj)
        res = self.client.get(
            f"/api/theater/seats-available/{str(screen_show_obj.slug)}/")

        self.assertEqual(res.status_code,status.HTTP_200_OK)


