from django.contrib.auth import get_user_model
from django.db import models
from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    book_id = models.ForeignKey(
        to=Book, related_name="borrowings", on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        to=get_user_model(), related_name="borrowings", on_delete=models.CASCADE
    )
