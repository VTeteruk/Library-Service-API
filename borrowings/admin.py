from django.contrib import admin
from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_filter = ("owner", "book")
    search_fields = ("book__title",)
