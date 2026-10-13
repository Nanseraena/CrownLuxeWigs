from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Coupon

class CouponTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.coupon_pct = Coupon.objects.create(
            code="SAVE10",
            discount_type="percentage",
            value=Decimal("10.00"),
            min_order_amount=Decimal("50000.00"),
            max_discount=Decimal("20000.00"),
            is_active=True
        )
        self.coupon_fixed = Coupon.objects.create(
            code="FLAT25K",
            discount_type="fixed",
            value=Decimal("25000.00"),
            min_order_amount=Decimal("100000.00"),
            is_active=True
        )

    def test_percentage_coupon_calculation(self):
        discount = self.coupon_pct.calculate_discount(Decimal("100000.00"))
        self.assertEqual(discount, Decimal("10000.00"))

    def test_max_discount_cap(self):
        discount = self.coupon_pct.calculate_discount(Decimal("300000.00"))
        self.assertEqual(discount, Decimal("20000.00"))

    def test_min_order_requirement_fails_below_threshold(self):
        valid, msg = self.coupon_fixed.is_valid(Decimal("80000.00"))
        self.assertFalse(valid)
        self.assertIn("Minimum order subtotal", msg)

    def test_apply_coupon_api(self):
        response = self.client.post("/api/v1/promotions/apply/", {
            "code": "save10",  # Case insensitive
            "subtotal": "150000.00"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["valid"])
        self.assertEqual(Decimal(str(response.data["discount_amount"])), Decimal("15000.00"))
        self.assertEqual(Decimal(str(response.data["new_total"])), Decimal("135000.00"))
