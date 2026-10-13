import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, ValidationError
from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer, InitiatePaymentSerializer, VerifyPaymentSerializer

class InitiatePaymentView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_number = serializer.validated_data["order_number"]
        provider = serializer.validated_data["provider"]
        phone_number = serializer.validated_data.get("phone_number", "")

        try:
            order = Order.objects.select_for_update().get(order_number__iexact=order_number)
        except Order.DoesNotExist:
            raise NotFound({"order_number": "Order not found."})

        if order.payment_status == "paid":
            return Response({
                "message": "Order is already paid.",
                "status": "successful",
                "order_number": order.order_number
            }, status=status.HTTP_200_OK)

        # Retrieve existing pending payment or create new one
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "provider": provider,
                "amount": order.total,
                "currency": order.currency,
                "phone_number": phone_number,
                "status": "pending",
                "provider_metadata": {
                    "mode": "sandbox",
                    "channel": provider,
                    "simulated_prompt": f"USSD push prompt sent to {phone_number or order.phone} for {order.currency} {order.total:,.0f}."
                }
            }
        )

        if not created and payment.status != "successful":
            payment.provider = provider
            payment.phone_number = phone_number or order.phone
            payment.save(update_fields=["provider", "phone_number", "updated_at"])

        instruction = ""
        if provider == "mtn_momo":
            instruction = f"A prompt has been sent to {payment.phone_number or order.phone}. Enter your MTN MoMo PIN to complete payment of UGX {order.total:,.0f}."
        elif provider == "airtel_money":
            instruction = f"An Airtel Money prompt has been sent to {payment.phone_number or order.phone}. Approve with your Airtel PIN."
        elif provider == "card":
            instruction = f"Card payment authorized for UGX {order.total:,.0f}. Confirm 3D-Secure approval."
        else:
            instruction = "Cash on Delivery confirmed. You will pay when your wig is delivered."
            payment.status = "pending"
            payment.save()
            order.status = "processing"
            order.save(update_fields=["status"])

        return Response({
            "message": "Payment initiated.",
            "payment": PaymentSerializer(payment).data,
            "instruction": instruction,
            "transaction_reference": payment.transaction_reference,
            "provider": provider,
            "amount": order.total,
            "currency": order.currency
        }, status=status.HTTP_200_OK)

class VerifyPaymentView(APIView):
    """Verifies or simulates customer confirmation of mobile money or card payment."""
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ref = serializer.validated_data["transaction_reference"]

        try:
            payment = Payment.objects.select_for_update().select_related("order").get(transaction_reference=ref)
        except Payment.DoesNotExist:
            raise NotFound({"transaction_reference": "Payment transaction not found."})

        order = payment.order
        payment.status = "successful"
        payment.provider_metadata["verification"] = "Verified in sandbox / callback received"
        payment.save(update_fields=["status", "provider_metadata", "updated_at"])

        order.payment_status = "paid"
        order.status = "processing"
        order.payment_reference = ref
        order.save(update_fields=["payment_status", "status", "payment_reference", "updated_at"])

        return Response({
            "message": "Payment verified successfully.",
            "payment_status": "paid",
            "order_status": "processing",
            "order_number": order.order_number,
            "transaction_reference": ref
        }, status=status.HTTP_200_OK)

class PaymentStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, reference):
        try:
            payment = Payment.objects.select_related("order").get(transaction_reference=reference)
            return Response(PaymentSerializer(payment).data)
        except Payment.DoesNotExist:
            raise NotFound("Payment not found.")

class PaymentWebhookView(APIView):
    """Idempotent webhook endpoint for MTN Mobile Money / Airtel Money / Card gateway."""
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        data = request.data
        ref = data.get("transaction_reference") or data.get("external_id")
        provider_status = data.get("status", "").lower()

        if not ref:
            return Response({"error": "Missing transaction_reference"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.select_for_update().select_related("order").get(transaction_reference=ref)
        except Payment.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        if provider_status in ["success", "successful", "paid"]:
            payment.status = "successful"
            payment.provider_metadata["webhook_payload"] = data
            payment.save(update_fields=["status", "provider_metadata", "updated_at"])

            order = payment.order
            order.payment_status = "paid"
            order.status = "processing"
            order.payment_reference = ref
            order.save(update_fields=["payment_status", "status", "payment_reference", "updated_at"])
        elif provider_status in ["failed", "rejected"]:
            payment.status = "failed"
            payment.save(update_fields=["status", "updated_at"])
            order = payment.order
            order.payment_status = "failed"
            order.save(update_fields=["payment_status", "updated_at"])

        return Response({"status": "acknowledged"}, status=status.HTTP_200_OK)
