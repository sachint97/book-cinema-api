"""Views for user api"""

from rest_framework.views import APIView
from user.serializers import UserSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from app import settings


class CreateUserView(APIView):
    """Create a new user in the system"""

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User creation successful"},
            status=status.HTTP_201_CREATED
        )


class LoginUserView(APIView):
    """View to login into system and generate tokens."""

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.login()
        token = RefreshToken.for_user(user)
        atl = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        rtl = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
        data = {
            "access_token": str(token.access_token),
            "refresh_token": str(token),
            "access_token_life_time_in_seconds": atl.total_seconds(),
            "refresh_token_life_time_in_seconds": rtl.total_seconds(),
        }
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            r_token=request.data['refresh_token']
            token = RefreshToken(r_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "Logout operation failed.","error": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    def get(self,request,query=None):
        try:
            user = get_user_model().objects.get(slug=query)
            serializer = self.serializer_class(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "User does not exist.","error": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

