from django.contrib import admin
from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_filter = ("user_id", "book_id")
    search_fields = ("book_id__title",)
