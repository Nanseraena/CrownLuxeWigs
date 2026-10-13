from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product, ProductVariant

class CatalogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Curly Wigs")
        self.product = Product.objects.create(name="Curly Human Hair Wig", category=self.category, is_published=True)
        self.variant = ProductVariant.objects.create(product=self.product, sku="CUR-20-BLK", length_inches=20, color="Natural Black", price="250000.00", stock_quantity=3)
    def test_published_products_are_public(self):
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(x["slug"] == self.product.slug for x in response.data["results"]))
    def test_unpublished_products_are_hidden(self):
        self.product.is_published = False; self.product.save()
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
