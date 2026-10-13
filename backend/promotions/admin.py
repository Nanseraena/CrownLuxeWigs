from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_type", "value", "min_order_amount", "used_count", "usage_limit", "is_active", "expiry_date"]
    list_filter = ["discount_type", "is_active"]
    search_fields = ["code", "description"]
