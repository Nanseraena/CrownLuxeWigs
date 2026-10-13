from rest_framework import serializers
from .models import Order, OrderItem, DeliveryMethod

class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ["id", "name", "zone", "base_fee", "estimated_delivery", "is_active", "sort_order"]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "sku", "variant_description", "unit_price", "quantity", "line_total"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_method = DeliveryMethodSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "customer_name", "email", "phone", "delivery_address",
            "delivery_method", "currency", "subtotal", "delivery_fee", "discount_amount",
            "coupon_code", "total", "status", "payment_method", "payment_status",
            "payment_reference", "tracking_number", "notes", "created_at", "updated_at", "items"
        ]

class CheckoutSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=180)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=40)
    delivery_address = serializers.CharField()
    delivery_method_id = serializers.IntegerField(required=False, allow_null=True)
    coupon_code = serializers.CharField(max_length=40, required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES, default="mtn_momo")
    notes = serializers.CharField(required=False, allow_blank=True)
