from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing

BORROWING_LIST_URL = reverse("borrowings:borrowing-list")
BORROWING_DETAIL_URL = reverse("borrowings:borrowing-detail", args=[1])


def create_simple_borrowing(user, actual_return_date) -> Borrowing:
    return Borrowing.objects.create(
        expected_return_date=datetime.now(),
        actual_return_date=actual_return_date,
        book=Book.objects.create(
            title="test",
            author="test",
            cover="SOFT",
            inventory=1,
            daily_fee=2.99,
        ),
        user=user
    )


class UnauthenticatedBorrowingTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="123456"
        )

    def test_can_not_enter_list_borrowings(self) -> None:
        response = self.client.get(BORROWING_LIST_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_enter_detail_borrowing(self) -> None:
        create_simple_borrowing(self.user, None)
        response = self.client.get(BORROWING_DETAIL_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

    def test_see_only_their_borrowings(self) -> None:
        another_user = get_user_model().objects.create_user(
            email="test@user.com",
            password="123456"
        )
        create_simple_borrowing(another_user, None)
        create_simple_borrowing(self.user, None)

        response = self.client.get(BORROWING_LIST_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_can_enter_detail_borrowing(self) -> None:
        create_simple_borrowing(self.user, None)
        response = self.client.get(BORROWING_DETAIL_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_filter_by_is_active(self) -> None:
        create_simple_borrowing(self.user, None)
        create_simple_borrowing(self.user, datetime.now())

        response = self.client.get(BORROWING_LIST_URL + "?is_active=1")

        self.assertEquals(len(response.data), 1)

    def test_can_not_filter_by_user_id(self) -> None:
        create_simple_borrowing(self.user, None)
        create_simple_borrowing(self.user, None)

        response = self.client.get(BORROWING_LIST_URL + "?user_id=10")

        self.assertEquals(len(response.data), 2)

    def test_can_not_borrow_a_book(self) -> None:
        Book.objects.create(
            title="test",
            author="test",
            cover="SOFT",
            inventory=0,
            daily_fee=2.99,
        )
        borrowing = {
            "expected_return_date": datetime.now(),
            "book": 1
        }
        response = self.client.post(BORROWING_LIST_URL, borrowing)

        self.assertEquals(list(response.data.keys()), ["non_field_errors"])


class AdminBorrowingTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_see_only_their_borrowings(self) -> None:
        another_user = get_user_model().objects.create_user(
            email="test@user.com",
            password="123456"
        )
        create_simple_borrowing(another_user, None)
        create_simple_borrowing(self.user, None)

        response = self.client.get(BORROWING_LIST_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_can_filter_by_user_id(self) -> None:
        create_simple_borrowing(self.user, None)
        create_simple_borrowing(self.user, None)
        another_user = get_user_model().objects.create_user(
            email="test@user.com",
            password="123456"
        )
        create_simple_borrowing(another_user, None)

        response = self.client.get(BORROWING_LIST_URL + "?user_id=2")

        self.assertEquals(len(response.data), 1)
