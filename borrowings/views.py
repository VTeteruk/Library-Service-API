from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import generics
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = Borrowing.objects.filter(user_id=self.request.user.id)
        return queryset


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
