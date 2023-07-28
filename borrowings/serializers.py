from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("borrow_date", "expected_return_date", "actual_return_date", "book_id", "user_id")
        read_only_fields = ("user_id", "borrow_date")

    def validate(self, data):
        book = data.get("book_id")
        if book and book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock.")

        return data

    def create(self, validated_data) -> Borrowing:
        validated_data["user_id"] = self.context.get("request").user

        book = Book.objects.get(id=validated_data["book_id"].id)
        book.inventory -= 1
        book.save()

        return Borrowing.objects.create(**validated_data)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("borrow_date", "expected_return_date", "actual_return_date", "book_id", "user_id")
