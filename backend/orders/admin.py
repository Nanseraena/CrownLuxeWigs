from django.contrib import admin
from .models import Order, OrderItem, DeliveryMethod

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "sku", "variant_description", "unit_price", "quantity", "line_total"]
    autocomplete_fields = ("variant",)

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
    readonly_fields = ["order_number", "subtotal", "delivery_fee", "discount_amount", "total", "created_at", "updated_at"]
    list_select_related = ("user", "delivery_method")
    list_editable = ("status", "payment_status")
    date_hierarchy = "created_at"
    autocomplete_fields = ("user", "delivery_method")
    fieldsets = (
        ("Order", {"fields": ("order_number", "user", "status", "payment_status", "payment_method", "payment_reference")}),
        ("Customer & delivery", {"fields": ("customer_name", "email", "phone", "delivery_address", "delivery_method", "tracking_number", "notes")}),
        ("Totals", {"fields": ("currency", "subtotal", "delivery_fee", "discount_amount", "coupon_code", "total")}),
        ("Audit", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
