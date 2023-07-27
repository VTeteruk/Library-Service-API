from rest_framework.viewsets import ModelViewSet

from books.serializers import BookSerializer
from books.models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
