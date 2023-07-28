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
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if is_active:
            queryset = queryset.filter(actual_return_date=None)
        if user_id and self.request.user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset.all()


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
