from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = Borrowing.objects.filter(user_id=self.request.user.id)
        return queryset


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
