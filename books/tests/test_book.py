from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book

BOOK_LIST_URL = reverse("books:book-list")


def create_simple_book() -> Book:
    return Book.objects.create(
        title="test",
        author="test",
        cover="SOFT",
        inventory=1,
        daily_fee=2.99,
    )


class NotAdminBookTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@user.com",
            password="123456"
        )

    def test_can_see_books(self) -> None:
        create_simple_book()
        create_simple_book()

        response = self.client.get(BOOK_LIST_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_can_not_create_book(self) -> None:
        self.client.force_authenticate(self.user)
        book = {
            "title": "test",
            "author": "test",
            "cover": "SOFT",
            "inventory": 1,
            "daily_fee": 2.99,
        }

        response = self.client.post(BOOK_LIST_URL, book)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@user.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_can_see_books(self) -> None:
        create_simple_book()
        create_simple_book()

        response = self.client.get(BOOK_LIST_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_can_create_book(self) -> None:
        book = {
            "title": "test",
            "author": "test",
            "cover": "Soft",
            "inventory": 1,
            "daily_fee": 2.99,
        }

        response = self.client.post(BOOK_LIST_URL, book)

        print(response.data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)