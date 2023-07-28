from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

TOKEN_URL = reverse("token_obtain_pair")
DETAILS_USER_URL = reverse("users:me")


class UnauthenticatedUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="123456",
        )

    def test_user_can_access_token(self) -> None:
        user = {
            "email": "user@user.com",
            "password": "123456",
        }
        response = self.client.post(TOKEN_URL, user)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_not_enter_me_endpoint(self) -> None:
        response = self.client.get(DETAILS_USER_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="123456",
        )
        self.client.force_authenticate(self.user)

    def test_can_enter_me_endpoint(self) -> None:
        get_user_model().objects.create_user(
            email="test1@user.com",
            password="123456",
        )
        get_user_model().objects.create_user(
            email="test2@user.com",
            password="123456",
        )

        response = self.client.get(DETAILS_USER_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get("email"), self.user.email)
