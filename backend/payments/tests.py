from decimal import Decimal
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from orders.models import Order
from payments.models import Payment

class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order = Order.objects.create(
            customer_name="Amina Grace",
            email="amina@example.com",
            phone="+256701234567",
            delivery_address="Bukoto, Kampala",
            subtotal=Decimal("450000.00"),
            delivery_fee=Decimal("10000.00"),
            total=Decimal("460000.00"),
            payment_status="pending"
        )

    def test_initiate_mtn_momo_payment(self):
        response = self.client.post("/api/v1/payments/initiate/", {
            "order_number": self.order.order_number,
            "provider": "mtn_momo",
            "phone_number": "+256782334455",
            "payment_access_token": str(self.order.payment_access_token),
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("transaction_reference", response.data)
        self.assertEqual(response.data["provider"], "mtn_momo")
        self.assertIn("PIN", response.data["instruction"])

        payment = Payment.objects.get(order=self.order)
        self.assertEqual(payment.status, "pending")
        self.assertEqual(payment.amount, Decimal("460000.00"))

    @override_settings(PAYMENT_SIMULATION_ENABLED=True)
    def test_verify_payment_transitions_order_to_paid(self):
        payment = Payment.objects.create(
            order=self.order,
            provider="airtel_money",
            amount=self.order.total,
            phone_number=self.order.phone,
            status="pending"
        )

        response = self.client.post("/api/v1/payments/verify/", {
            "transaction_reference": payment.transaction_reference,
            "simulated_pin": "1234",
            "payment_access_token": str(self.order.payment_access_token),
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["payment_status"], "paid")

        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, "paid")
        self.assertEqual(self.order.status, "processing")
        self.assertEqual(self.order.payment_reference, payment.transaction_reference)

    def test_payment_access_and_unsigned_webhook_are_rejected(self):
        response = self.client.post("/api/v1/payments/initiate/", {"order_number": self.order.order_number, "provider": "mtn_momo"}, format="json")
        self.assertEqual(response.status_code, 403)
        payment = Payment.objects.create(order=self.order, provider="mtn_momo", amount=self.order.total)
        response = self.client.post("/api/v1/payments/verify/", {"transaction_reference": payment.transaction_reference}, format="json")
        self.assertEqual(response.status_code, 403)
        response = self.client.post("/api/v1/payments/webhook/", {"transaction_reference": payment.transaction_reference, "status": "paid"}, format="json")
        self.assertIn(response.status_code, [403, 503])
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, "pending")
