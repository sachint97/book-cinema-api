"""Serializers for the user API view"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

# from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib import auth


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    name = serializers.CharField(min_length=3, max_length=80)
    phone = serializers.CharField(min_length=3, max_length=20, required=False)
    password = serializers.CharField(
        min_length=5, max_length=64, required=True, write_only=True
    )
    confirm_password = serializers.CharField(
        min_length=5, max_length=64, required=True, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password", "confirm_password", "phone"]

    def validate_confirm_password(self, value):
        """custom validation for confirm password"""
        if value != self.initial_data["password"]:
            raise serializers.ValidationError(
                "Incorrect password", code="invalid"
            )
        return value

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        validated_data.pop("confirm_password")
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for Login View"""

    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]

    def login(self, **kwargs):
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        user = get_user_model().objects.get(email=email)
        if not user:
            raise serializers.ValidationError(
                {
                    "detail": "No account found with the given credentials."
                }
            )
        user = auth.authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."}
            )
        else:
            return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to view user profile"""

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "phone"]
