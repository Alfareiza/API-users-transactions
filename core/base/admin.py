from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "date", "amount", "type", "category", "user_email")
    list_filter = ("date", "category", "user_email")
    search_fields = ("user_email", )
    ordering = ("date", )
