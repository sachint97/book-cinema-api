"""Views for booking and paying movie tickets."""

from core.models import Booking, BookingSeat, ScreenShowMapper, Seat
from rest_framework.views import APIView
from .serializers import BookingSerializer, PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class BookSeatsView(APIView):
    """View to book show."""

    def post(self, request):
        user = request.user
        try:
            screen_show = ScreenShowMapper.objects.get(
                slug=request.data["screen_show"]
            )
        except ScreenShowMapper.DoesNotExist:
            return Response(
                {"message": "Screen show does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(screen_show=screen_show, user=user)
        seats = request.data["seats"]
        seats_queryset = Seat.objects.filter(screen=screen_show.screen)
        seats_list = []
        for seat in seats:
            queryset = seats_queryset.filter(
                screen=screen_show.screen,
                fare__seating_class__slug=seat["seating_class"],
                row=seat["row"],
                column=seat["column"],
                is_available=True,
            )
            if not queryset.exists():
                return Response(
                    {"message": f"Seat {seat} is not available"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            seats_list.append(queryset.first())
        with transaction.atomic():
            booking_seats = []
            for seat in seats_list:
                booking_seats.append(
                    BookingSeat(
                        seat=seat, booking=booking, booking_status=True
                    )
                )
            BookingSeat.objects.bulk_create(booking_seats)
            for index, booking_seat in enumerate(booking_seats):
                booking_seat.slug = f"{booking.slug}-{index+1}"
                BookingSeat.objects.bulk_update(booking_seats, ["slug"])
            for seat in seats_list:
                seat.is_available = False
                seat.save()
        return Response(
            {"message": "Booking confirmed"}, status=status.HTTP_200_OK
        )


class PaymentView(APIView):
    """Payment for booked show."""

    def post(self, request):
        try:
            booking = Booking.objects.get(slug=request.data["booking"])
        except Exception as e:
            return Response(
                {"message": "Could not find booking details",
                 "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(booking=booking, payment_status=True)
        return Response(
            {"message": "Payment successfull"}, status=status.HTTP_200_OK
        )
