from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Category, Product, ProductVariant
from .models import Cart, CartItem

class CartApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Lace Front")
        self.product = Product.objects.create(name="Silky Straight Wig", category=self.category, is_published=True)
        self.variant = ProductVariant.objects.create(product=self.product, sku="SILK-18-NB", length_inches=18, color="Natural Black", price="180000.00", stock_quantity=4)
        self.token = "7d1f6fd8-76b8-4e42-99b8-2bd490bc61a1"
        self.client.credentials(HTTP_X_CART_TOKEN=self.token)
    def test_add_selected_variant_to_guest_cart(self):
        response = self.client.post("/api/v1/cart/items/", {"variant_id": self.variant.id, "quantity": 1}, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["cart"]["item_count"], 1)
        self.assertEqual(response.data["cart"]["items"][0]["variant_id"], self.variant.id)
        self.assertEqual(response.data["cart"]["items"][0]["unit_price"], "180000.00")
    def test_repeated_add_merges_variant_quantity(self):
        for _ in range(2):
            response = self.client.post("/api/v1/cart/items/", {"variant_id": self.variant.id, "quantity": 1}, format="json")
            self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)
    def test_cannot_add_more_than_stock(self):
        response = self.client.post("/api/v1/cart/items/", {"variant_id": self.variant.id, "quantity": 5}, format="json")
        self.assertEqual(response.status_code, 400)
    def test_cart_requires_token_for_guest_retrieval(self):
        client = APIClient()
        response = client.get("/api/v1/cart/")
        self.assertEqual(response.status_code, 400)

    def test_guest_cart_merges_on_login(self):
        # 1. Add item to guest cart
        self.client.post("/api/v1/cart/items/", {"variant_id": self.variant.id, "quantity": 1}, format="json")

        # 2. Authenticate customer
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username="mergeuser", password="password123")
        self.client.force_authenticate(user=user)

        # 3. Call merge endpoint
        response = self.client.post("/api/v1/cart/merge/", {"guest_token": self.token}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cart"]["item_count"], 1)

        # 4. Verify guest cart was cleared and user cart has the item
        user_cart = Cart.objects.get(user=user)
        self.assertEqual(user_cart.items.count(), 1)
        self.assertEqual(user_cart.items.first().variant, self.variant)
