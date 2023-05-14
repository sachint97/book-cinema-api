"""Serializer for booking API's"""

from rest_framework import serializers
from core.models import Booking, BookingSeat, Payment
from theater.serializers import SeatingClassSerializer, SeatSerializer


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for booking show."""

    screen_show = SeatingClassSerializer(read_only=True)
    booking_date = serializers.DateField(required=True)

    class Meta:
        model = Booking
        fields = ["screen_show", "booking_date"]


class BookingSeatSerializer(serializers.ModelSerializer):
    """Serializer for booking seats."""

    booking = BookingSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = BookingSeat
        fields = [
            "seat",
            "booking",
            "booking_status",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment."""

    booking = BookingSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ["payment_method", "amount", "booking", "coupon"]
