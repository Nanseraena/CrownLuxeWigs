from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.order_number", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "order_number", "provider", "amount", "currency",
            "phone_number", "transaction_reference", "status",
            "provider_metadata", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "transaction_reference", "created_at", "updated_at"]

class InitiatePaymentSerializer(serializers.Serializer):
    order_number = serializers.CharField(max_length=40)
    provider = serializers.ChoiceField(choices=Payment.PROVIDER_CHOICES)
    phone_number = serializers.CharField(max_length=40, required=False, allow_blank=True)

class VerifyPaymentSerializer(serializers.Serializer):
    transaction_reference = serializers.CharField(max_length=120)
    simulated_pin = serializers.CharField(max_length=10, required=False, allow_blank=True)
