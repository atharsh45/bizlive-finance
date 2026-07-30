from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "transaction_type", "payment_status", "payment_method", "created_at")
    list_filter = ("transaction_type", "payment_status", "payment_method")
    search_fields = ("title", "client_or_vendor", "reference_no")
