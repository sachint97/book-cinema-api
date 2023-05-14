from rest_framework.urls import path
from .views import BookSeatsView,PaymentView

app_name = "booking"

urlpatterns = [
    path("seat-booking/",BookSeatsView.as_view(),name="ticket-booking"),
    path("payment/",PaymentView.as_view(),name="payment")
]