"""Views for theater app"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Movie, Show, ScreenShowMapper, Seat
from .serializers import (
    MoviesSerializer,
    ShowScreenSerializer,
    AvailabeSeatsSerializer,
)
from django.db.models import Q
from rest_framework.permissions import AllowAny


class MoviesByCityView(APIView):
    """Display list of movies based on city."""

    permission_classes = (AllowAny,)

    def get(self, request, city=None):
        queryset = Show.objects.filter(
            screen_show__screen__theater__city__slug=city
        )
        movies = Movie.objects.filter(show__in=queryset)
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowsByMovieView(APIView):
    """List of shows and screens based on movie , city or both."""

    permission_classes = (AllowAny,)

    def get(self, request):
        movie = request.GET.get("movie")
        city = request.GET.get("city")
        queryset = ScreenShowMapper.objects.all()
        if city and movie:
            queryset = queryset.filter(
                Q(screen__theater__city__slug=city)
                & Q(show__movie__slug=movie)
            )
        elif city:
            queryset = queryset.filter(screen__theater__city__slug=city)
        elif movie:
            queryset = queryset.filter(show__movie__slug=movie)
        serializer = ShowScreenSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SeatingsByShowView(APIView):
    """Listing all the seats available for perticular show."""

    permission_classes = (AllowAny,)

    def get(self, request, show=None):
        screen_show = ScreenShowMapper.objects.get(slug=show)
        if not screen_show:
            return Response(
                {"detail": "Screen or show not found."}, status=404
            )
        screen_show_serialized = ShowScreenSerializer(screen_show)
        seats = Seat.objects.filter(fare__screen_show__slug=show)
        seat_groups = {}
        for seat in seats:
            if seat.fare.seating_class.name not in seat_groups:
                seat_groups[seat.fare.seating_class.name] = []
            seat_groups[seat.fare.seating_class.name].append(seat)
        seat_data = []
        for seating_class, seat_list in seat_groups.items():
            seat_data.append(
                {
                    "seating_class": seating_class,
                    "price": seat_list[0].fare.price,
                    "seats": AvailabeSeatsSerializer(
                        seat_list, many=True
                    ).data,
                }
            )
        response_data = {
            **screen_show_serialized.data,
            "seating_arrangement": seat_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
