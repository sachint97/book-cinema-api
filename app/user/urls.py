"""URL mapping for the user API"""

from django.urls import path
from .views import CreateUserView, LoginUserView, LogoutView, UserProfile

app_name = "user"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<str:query>/", UserProfile.as_view(), name="profile"),
]
