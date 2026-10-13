from django.contrib import admin
from .models import Order, OrderItem, DeliveryMethod

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "sku", "variant_description", "unit_price", "quantity", "line_total"]

@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ["name", "zone", "base_fee", "estimated_delivery", "is_active", "sort_order"]
    list_filter = ["zone", "is_active"]
    search_fields = ["name", "zone"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "customer_name", "phone", "total", "currency", "status", "payment_status", "payment_method", "created_at"]
    list_filter = ["status", "payment_status", "payment_method", "created_at"]
    search_fields = ["order_number", "customer_name", "email", "phone"]
    inlines = [OrderItemInline]
    readonly_fields = ["order_number", "created_at", "updated_at"]
