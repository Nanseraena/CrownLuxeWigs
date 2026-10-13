from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "id", "code", "description", "discount_type", "value",
            "min_order_amount", "max_discount", "expiry_date", "is_active"
        ]

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=40)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2, required=False)
