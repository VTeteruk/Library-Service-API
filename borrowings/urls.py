from django.urls import path

from borrowings.views import BorrowingListView, BorrowingDetailView, ReturnBookView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowing-list"),
    path(
        "borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"
    ),
    path("borrowings/return/<int:pk>/", ReturnBookView.as_view(), name="borrowing-return")
]

app_name = "borrowings"
