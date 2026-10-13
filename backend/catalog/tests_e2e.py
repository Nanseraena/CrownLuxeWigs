import uuid
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Category, Product, ProductVariant
from cart.models import Cart, CartItem
from orders.models import Order, DeliveryMethod
from payments.models import Payment
from promotions.models import Coupon

class FullCustomerJourneyE2ETest(TestCase):
    """
    Complete end-to-end customer journey testing every requirement:
    1. Browse catalog
    2. Search for curly human hair
    3. Open product details
    4. Select 20-inch variant in available color
    5. Add variant to cart (guest X-Cart-Token)
    6. Verify correct item and options appear in cart
    7. Update quantity to 2 and verify subtotal
    8. Check cart persistence across request
    9. Apply discount coupon
    10. Complete checkout with Ugandan delivery zone
    11. Initiate and verify mobile money payment in sandbox
    12. Verify order transitions to paid and processing
    13. Verify stock quantity decremented atomically
    14. Verify admin dashboard reflects revenue and recent order
    """

    def setUp(self):
        self.client = APIClient()
        self.guest_token = str(uuid.uuid4())
        self.client.credentials(HTTP_X_CART_TOKEN=self.guest_token)

        # 1. Setup Category
        self.category = Category.objects.create(name="Deep Wave & Curly Wigs", slug="deep-wave-curly-wigs", is_active=True)

        # 2. Setup Product
        self.product = Product.objects.create(
            name="Luxe Deep Wave 13x6 Melted Frontal Wig",
            slug="luxe-deep-wave-13x6-frontal-wig",
            category=self.category,
            hair_type="human",
            texture="Deep Wave",
            default_length_inches=20,
            default_color="1B Natural Black",
            default_lace_type="13x6 HD Ear-to-Ear Lace",
            is_published=True,
            is_featured=True,
            is_best_seller=True
        )

        # 3. Setup Variants
        self.variant_20 = ProductVariant.objects.create(
            product=self.product,
            sku="CL-DW-20",
            length_inches=20,
            color="1B Natural Black",
            texture="Deep Wave",
            lace_type="13x6 HD Lace",
            density="180%",
            cap_size="Medium (22.5\")",
            price=Decimal("540000.00"),
            compare_at_price=Decimal("650000.00"),
            stock_quantity=10,
            is_active=True
        )

        self.variant_24 = ProductVariant.objects.create(
            product=self.product,
            sku="CL-DW-24",
            length_inches=24,
            color="1B Natural Black",
            texture="Deep Wave",
            lace_type="13x6 HD Lace",
            density="180%",
            cap_size="Medium (22.5\")",
            price=Decimal("680000.00"),
            compare_at_price=Decimal("800000.00"),
            stock_quantity=5,
            is_active=True
        )

        # 4. Delivery Method
        self.delivery = DeliveryMethod.objects.create(
            name="Standard Delivery (Kampala Central)",
            zone="Kampala Central",
            base_fee=Decimal("10000.00"),
            estimated_delivery="1 day",
            is_active=True
        )

        # 5. Coupon
        self.coupon = Coupon.objects.create(
            code="WELCOME10",
            discount_type="percentage",
            value=Decimal("10.00"),
            min_order_amount=Decimal("100000.00"),
            is_active=True
        )

    def test_complete_e2e_journey(self):
        # Step 1: Browse catalog
        resp_catalog = self.client.get("/api/v1/products/")
        self.assertEqual(resp_catalog.status_code, 200)
        self.assertGreaterEqual(resp_catalog.data["count"], 1)

        # Step 2: Search for curly human-hair wig
        resp_search = self.client.get("/api/v1/products/?search=curly&hair_type=human")
        self.assertEqual(resp_search.status_code, 200)
        self.assertTrue(any(p["slug"] == self.product.slug for p in resp_search.data["results"]))

        # Step 3: Open product details
        resp_detail = self.client.get(f"/api/v1/products/{self.product.slug}/")
        self.assertEqual(resp_detail.status_code, 200)
        self.assertEqual(resp_detail.data["name"], self.product.name)
        self.assertEqual(len(resp_detail.data["variants"]), 2)

        # Step 4 & 5: Add 20-inch variant to cart
        resp_add = self.client.post("/api/v1/cart/items/", {
            "variant_id": self.variant_20.id,
            "quantity": 1
        }, format="json")
        self.assertEqual(resp_add.status_code, 201)
        self.assertEqual(resp_add.data["cart"]["item_count"], 1)
        cart_item_id = resp_add.data["item_id"]

        # Step 6: Verify cart contents
        resp_cart = self.client.get("/api/v1/cart/")
        self.assertEqual(resp_cart.status_code, 200)
        self.assertEqual(resp_cart.data["items"][0]["sku"], "CL-DW-20")
        self.assertEqual(Decimal(str(resp_cart.data["subtotal"])), Decimal("540000.00"))

        # Step 7 & 8: Update quantity to 2 and verify subtotal (540,000 * 2 = 1,080,000)
        resp_update = self.client.patch(f"/api/v1/cart/items/{cart_item_id}/", {
            "quantity": 2
        }, format="json")
        self.assertEqual(resp_update.status_code, 200)
        self.assertEqual(resp_update.data["item_count"], 2)
        self.assertEqual(Decimal(str(resp_update.data["subtotal"])), Decimal("1080000.00"))

        # Verify persistence across fresh client instance using same X-Cart-Token
        fresh_client = APIClient()
        fresh_client.credentials(HTTP_X_CART_TOKEN=self.guest_token)
        resp_persisted = fresh_client.get("/api/v1/cart/")
        self.assertEqual(resp_persisted.status_code, 200)
        self.assertEqual(resp_persisted.data["item_count"], 2)

        # Step 9: Validate coupon application
        resp_coupon = self.client.post("/api/v1/promotions/apply/", {
            "code": "WELCOME10",
            "subtotal": "1080000.00"
        }, format="json")
        self.assertEqual(resp_coupon.status_code, 200)
        self.assertTrue(resp_coupon.data["valid"])
        expected_discount = Decimal("108000.00")  # 10% of 1,080,000
        self.assertEqual(Decimal(str(resp_coupon.data["discount_amount"])), expected_discount)

        # Step 10: Complete Checkout
        # Subtotal: 1,080,000; Delivery: 10,000; Discount: 108,000 => Total: 982,000
        resp_checkout = self.client.post("/api/v1/checkout/", {
            "customer_name": "Diana Aine",
            "email": "diana@example.com",
            "phone": "+256782112233",
            "delivery_address": "Plot 28 Lumumba Avenue, Nakasero, Kampala",
            "delivery_method_id": self.delivery.id,
            "coupon_code": "WELCOME10",
            "payment_method": "mtn_momo",
            "notes": "Deliver by 3 PM"
        }, format="json")
        self.assertEqual(resp_checkout.status_code, 201)
        order_data = resp_checkout.data["order"]
        order_number = order_data["order_number"]
        self.assertEqual(Decimal(str(order_data["subtotal"])), Decimal("1080000.00"))
        self.assertEqual(Decimal(str(order_data["delivery_fee"])), Decimal("10000.00"))
        self.assertEqual(Decimal(str(order_data["discount_amount"])), expected_discount)
        self.assertEqual(Decimal(str(order_data["total"])), Decimal("982000.00"))
        self.assertEqual(order_data["status"], "pending")
        self.assertEqual(order_data["payment_status"], "pending")

        # Step 11: Inventory check - stock was originally 10, should now be 8
        self.variant_20.refresh_from_db()
        self.assertEqual(self.variant_20.stock_quantity, 8)

        # Cart should now be empty after checkout
        resp_empty_cart = self.client.get("/api/v1/cart/")
        self.assertEqual(resp_empty_cart.data["item_count"], 0)

        # Step 12: Initiate Payment
        resp_init_pay = self.client.post("/api/v1/payments/initiate/", {
            "order_number": order_number,
            "provider": "mtn_momo",
            "phone_number": "+256782112233"
        }, format="json")
        self.assertEqual(resp_init_pay.status_code, 200)
        pay_ref = resp_init_pay.data["transaction_reference"]

        # Step 13: Verify/Simulate MoMo Payment Confirmation
        resp_verify_pay = self.client.post("/api/v1/payments/verify/", {
            "transaction_reference": pay_ref,
            "simulated_pin": "1234"
        }, format="json")
        self.assertEqual(resp_verify_pay.status_code, 200)
        self.assertEqual(resp_verify_pay.data["payment_status"], "paid")

        # Step 14: Track Order
        resp_track = self.client.get(f"/api/v1/orders/track/{order_number}/")
        self.assertEqual(resp_track.status_code, 200)
        self.assertEqual(resp_track.data["payment_status"], "paid")
        self.assertEqual(resp_track.data["status"], "processing")
        self.assertEqual(resp_track.data["payment_reference"], pay_ref)

        # Step 15: Admin Dashboard Stats check
        resp_admin = self.client.get("/api/v1/admin/dashboard-stats/")
        self.assertEqual(resp_admin.status_code, 200)
        self.assertEqual(resp_admin.data["total_orders"], 1)
        self.assertEqual(Decimal(str(resp_admin.data["total_revenue"])), Decimal("982000.00"))
        self.assertTrue(any(o["order_number"] == order_number for o in resp_admin.data["recent_orders"]))
