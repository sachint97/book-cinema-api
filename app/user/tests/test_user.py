"""Tests for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
LOGIN_USER_URL = reverse("user:login")
LOGOUT_USER_URL = reverse("user:logout")


def create_user(**kwargs):
    """Create and return new user"""
    kwargs.pop("confirm_password")
    return get_user_model().objects.create_user(**kwargs)


class PublicaUserApiTest(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "confirm_password": "test123",
            "name": "Test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exist_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "confirm_password": "test123",
            "name": "Test name",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 char."""
        payload = {
            "email": "test@example.com",
            "password": "test",
            "confirm_password": "test",
            "name": "Test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_password_confirm_password_missmatch(self):
        """
        Test an error is returned if password and confirm_password missmatch
        """
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "confirm_password": "test12",
            "name": "Test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """
        Test to login user successfully
        and generate access_token and refresh_token
        """
        user_details = {
            "name": "Test name",
            "email": "test@example.com",
            "password": "testingpassword",
            "confirm_password": "testingpassword",
        }
        create_user(**user_details)
        payload = {"email": user_details["email"],
                   "password": user_details["password"]}
        res = self.client.post(LOGIN_USER_URL, payload)

        self.assertIn("access_token", res.data)
        self.assertIn("refresh_token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_user_bad_credentials(self):
        """Test to return error for bad credentials"""
        user_details = {
            "name": "Test name",
            "email": "test@example.com",
            "password": "testingpassword",
            "confirm_password": "testingpassword",
        }
        create_user(**user_details)
        payload = {"email": "test@example.com", "password": "badcredentials"}
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertNotIn("access_token", res.data)
        self.assertNotIn("refresh_token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_blank_password(self):
        """Test blank password for login"""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logut_success(self):
        """Test for logout success"""
        user_details = {
            "name": "Test name",
            "email": "test@example.com",
            "password": "testingpassword",
            "confirm_password": "testingpassword",
        }
        create_user(**user_details)
        payload = {"email": user_details["email"],
                   "password": user_details["password"]}
        res = self.client.post(LOGIN_USER_URL, payload)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(res.data['access_token'])
        }
        data = {'refresh_token': res.data['refresh_token']}
        response = self.client.post(LOGOUT_USER_URL, data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_success(self):
        """Test for user profile success"""
        user_details = {
            "name": "Testname",
            "email": "test@example.com",
            "password": "testingpassword",
            "confirm_password": "testingpassword",
        }
        user = create_user(**user_details)
        self.client.force_authenticate(user=user)
        res = self.client.get(reverse(("user:profile"),
                                      kwargs={"query": "testname"}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("name", res.data)
        self.assertIn("email", res.data)
        self.assertIn("phone", res.data)


