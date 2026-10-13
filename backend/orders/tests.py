from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Category, Product, ProductVariant
from cart.models import Cart, CartItem
from .models import Order

class CheckoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        category = Category.objects.create(name="Bob Wigs")
        product = Product.objects.create(name="Classic Bob", category=category, is_published=True)
        self.variant = ProductVariant.objects.create(product=product, sku="BOB-12", length_inches=12, price="100000.00", stock_quantity=3)
        self.token = "8d4a3d0f-4b3a-4ec4-a12f-765d6b8e8a21"
        cart = Cart.objects.create(token=self.token)
        CartItem.objects.create(cart=cart, variant=self.variant, quantity=2)
        self.client.credentials(HTTP_X_CART_TOKEN=self.token)
    def test_checkout_creates_pending_order_and_decrements_stock(self):
        response = self.client.post("/api/v1/checkout/", {"customer_name":"Test Customer", "email":"test@example.com", "phone":"0700000000", "delivery_address":"Kampala"}, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        order = Order.objects.get()
        self.assertEqual(order.total, 200000)
        self.assertEqual(order.payment_status, "pending")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 1)
        self.assertEqual(CartItem.objects.count(), 0)
