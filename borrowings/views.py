from datetime import datetime

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
            queryset = queryset.filter(owner=user_id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.id)
        return queryset.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Filter by not returned books",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="user_id",
                description="Filter by user id (only for admins)",
                required=False,
                type=str,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)


class ReturnBookView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, pk, *args, **kwargs):
        try:
            borrowing = Borrowing.objects.get(pk=pk)
        except Borrowing.DoesNotExist:
            return Response({"error": "Borrowing not found"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff and borrowing.owner != request.user:
            return Response(
                {"error": "You don't have permission to return this book"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if borrowing.actual_return_date is not None:
            return Response(
                {"error": "This book has already been returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = datetime.now()
        borrowing.save()

        return Response(
            {"message": "Book returned successfully"}, status=status.HTTP_200_OK
        )
