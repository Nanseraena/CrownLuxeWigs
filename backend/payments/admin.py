from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["transaction_reference", "order", "provider", "amount", "currency", "status", "created_at"]
    list_filter = ["provider", "status", "currency"]
    search_fields = ["transaction_reference", "order__order_number", "phone_number"]
    readonly_fields = ["transaction_reference", "created_at", "updated_at"]
    autocomplete_fields = ("order",)
    list_select_related = ("order",)
