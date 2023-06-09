"""Theater serializer."""

from rest_framework import serializers
from core.models import (Media, Movie, Theater, Show, Screen, ScreenShowMapper,
                         City, SeatingClass, Seat, Fare)


class MediaSerializer(serializers.ModelSerializer):
    """Serializer to store images."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["image", "alt_text", "is_feature"]

    def get_image(self, obj):
        print(obj)
        return obj.image.url


class MoviesSerializer(serializers.ModelSerializer):
    """Serilaizer for list of movies by city."""

    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ["title", "slug", "description", "duration", "release_date",
                  "language", "certificate", "images"]
        read_only = True

    def get_images(self, obj):
        queryset = Media.objects.filter(movie=obj)
        serializers = MediaSerializer(queryset, many=True)
        return serializers.data


class CitySerializer(serializers.ModelSerializer):
    """Serializer for city model."""

    class Meta:
        model = City
        fields = ["slug", "name"]


class TheaterSerializer(serializers.ModelSerializer):
    """Serializer for Theater model."""

    city = CitySerializer(read_only=True, many=False)

    class Meta:
        model = Theater
        fields = ["name", "slug", "address", "city"]


class ShowSerializer(serializers.ModelSerializer):
    """Serializer for Show model."""

    movie = MoviesSerializer(read_only=True)

    class Meta:
        model = Show
        fields = ["movie", "start_date", "end_date", "start_time", "end_time",
                  "slug"]


class ScreenSerializer(serializers.ModelSerializer):
    """Serializer for screen model."""

    theater = TheaterSerializer(read_only=True)

    class Meta:
        model = Screen
        fields = ["name", "slug", "theater"]


class ShowScreenSerializer(serializers.ModelSerializer):
    """Serializer for ScreenShowMapper model."""

    screen = ScreenSerializer(read_only=True)
    show = ShowSerializer(read_only=True)

    class Meta:
        model = ScreenShowMapper
        fields = ["show", "screen"]


class SeatingClassSerializer(serializers.ModelSerializer):
    """Serializer for SeatingClass model."""

    class Meta:
        model = SeatingClass
        fields = ["name", "slug"]


class FareSerializer(serializers.ModelSerializer):
    """Serializer for fare model."""

    screen_show = ShowScreenSerializer(read_only=True)
    seating_class = SeatingClassSerializer(read_only=True)

    class Meta:
        model = Fare
        fields = ["screen_show", "seating_class", "price"]


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seating model."""

    screen = ScreenSerializer(read_only=True)
    fare = FareSerializer(read_only=True)

    class Meta:
        model = Seat
        fields = ["screen", "fare", "row", "column", "is_available"]


class AvailabeSeatsSerializer(serializers.ModelSerializer):
    """Serializer to check available seats."""

    class Meta:
        model = Seat
        fields = ["row", "column", "is_available"]
