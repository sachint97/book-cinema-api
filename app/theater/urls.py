"""URL's related to theater"""

from rest_framework.urls import path
from .views import MoviesByCityView,GetMedia,ShowsByMovieView,SeatingsByShowView

urlpatterns = [
    path("movies/<str:city>/",MoviesByCityView.as_view(),name="movies-by-city"),
    path("media/<str:movie>/",GetMedia.as_view(),name="media"),
    path("shows/",ShowsByMovieView.as_view(),name="shows-movie"),
    path("seats-available/<str:show>/",SeatingsByShowView.as_view(),name="seats-by-show")
]