"""URL's related to theater"""

from rest_framework.urls import path
from .views import MoviesByCityView,ShowsByMovieView,SeatingsByShowView

app_name = "theater"

urlpatterns = [
    path("movies/<str:city>/",MoviesByCityView.as_view(),name="movies-by-city"),
    path("shows/",ShowsByMovieView.as_view(),name="shows-movie"),
    path("seats-available/<str:show>/",SeatingsByShowView.as_view(),name="seats-by-show")
]