from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing
from library_service_tel_bot import send_notification


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "owner",
        )
        read_only_fields = ("owner", "borrow_date")

    def validate(self, data):
        book = data.get("book")
        if book and book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock.")

        return data

    def create(self, validated_data) -> Borrowing:
        validated_data["owner"] = self.context.get("request").user

        book = Book.objects.get(id=validated_data["book"].id)
        book.inventory -= 1
        book.save()

        send_notification(validated_data.get("expected_return_date"), book.__str__())

        return Borrowing.objects.create(**validated_data)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "owner",
        )
