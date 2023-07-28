from rest_framework import serializers

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("borrow_date", "expected_return_date", "actual_return_date", "book_id", "user_id")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("borrow_date", "expected_return_date", "actual_return_date", "book_id", "user_id")
