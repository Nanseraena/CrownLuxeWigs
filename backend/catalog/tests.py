from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIClient
from .models import Category, Collection, Product, ProductVariant

class CatalogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Lace Front Wigs", slug="lace-front-wigs")
        self.subcat = Category.objects.create(name="13x4 Lace Front", slug="13x4-lace-front", parent=self.category)
        self.collection = Collection.objects.create(name="Best Sellers", slug="best-sellers")

        # Product 1: Brazilian Bone Straight, Natural Black, 26" & 30", In Stock
        self.product1 = Product.objects.create(
            name="CrownLuxe Bone Straight Wig",
            slug="crownluxe-bone-straight-wig",
            category=self.category,
            subcategory=self.subcat,
            hair_origin="brazilian",
            hair_type="human",
            texture="Bone Straight",
            default_color="Natural Black",
            default_length_inches=26,
            is_published=True,
            is_best_seller=True
        )
        self.product1.collections.add(self.collection)
        self.v1_1 = ProductVariant.objects.create(
            product=self.product1, sku="P1-26-BK",
            length_inches=26, color="Natural Black",
            price=Decimal("800000.00"), stock_quantity=5, is_active=True
        )
        self.v1_2 = ProductVariant.objects.create(
            product=self.product1, sku="P1-30-BK",
            length_inches=30, color="Natural Black",
            price=Decimal("950000.00"), stock_quantity=2, is_active=True
        )

        # Product 2: Peruvian Water Wave, Burgundy, 22", In Stock
        self.product2 = Product.objects.create(
            name="CrownLuxe Burgundy Water Wave Wig",
            slug="crownluxe-burgundy-water-wave-wig",
            category=self.category,
            hair_origin="peruvian",
            hair_type="human",
            texture="Water Wave",
            default_color="Burgundy",
            default_length_inches=22,
            is_published=True
        )
        self.v2_1 = ProductVariant.objects.create(
            product=self.product2, sku="P2-22-BUR",
            length_inches=22, color="Burgundy",
            price=Decimal("650000.00"), stock_quantity=4, is_active=True
        )

        # Product 3: Indian Silky Straight, Jet Black, 18", Out of stock
        self.product3 = Product.objects.create(
            name="CrownLuxe Indian Straight Out of Stock",
            slug="crownluxe-indian-straight-out-of-stock",
            category=self.category,
            hair_origin="indian",
            hair_type="human",
            texture="Silky Straight",
            default_color="Jet Black",
            default_length_inches=18,
            is_published=True
        )
        self.v3_1 = ProductVariant.objects.create(
            product=self.product3, sku="P3-18-JB",
            length_inches=18, color="Jet Black",
            price=Decimal("400000.00"), stock_quantity=0, is_active=True
        )

    def test_published_products_are_public(self):
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_unpublished_products_are_hidden(self):
        self.product1.is_published = False
        self.product1.save()
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_filter_by_color(self):
        # Filter for Burgundy
        response = self.client.get("/api/v1/products/?color=Burgundy")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], self.product2.slug)

    def test_filter_by_length(self):
        # Filter for 26 inches
        response = self.client.get("/api/v1/products/?length_inches=26")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], self.product1.slug)

    def test_filter_by_hair_origin(self):
        # Brazilian origin
        response = self.client.get("/api/v1/products/?hair_origin=brazilian")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], self.product1.slug)

        # Peruvian origin
        response_peru = self.client.get("/api/v1/products/?hair_origin=peruvian")
        self.assertEqual(response_peru.data["count"], 1)
        self.assertEqual(response_peru.data["results"][0]["slug"], self.product2.slug)

    def test_filter_combining_color_length_and_origin(self):
        # Exact intersection: Brazilian, Natural Black, 26"
        url = "/api/v1/products/?hair_origin=brazilian&color=Natural+Black&length_inches=26"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], self.product1.slug)

        # Mismatched combination returns 0
        url_empty = "/api/v1/products/?hair_origin=peruvian&color=Natural+Black"
        response_empty = self.client.get(url_empty)
        self.assertEqual(response_empty.data["count"], 0)

    def test_filter_in_stock_only(self):
        response = self.client.get("/api/v1/products/?in_stock=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        slugs = [p["slug"] for p in response.data["results"]]
        self.assertNotIn(self.product3.slug, slugs)

    def test_filter_options_facet_endpoint(self):
        response = self.client.get("/api/v1/products/filter-options/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("colors", response.data)
        self.assertIn("lengths", response.data)
        self.assertIn("hair_origins", response.data)
        self.assertIn("brazilian", response.data["hair_origins"])
        self.assertIn("Natural Black", response.data["colors"])
        self.assertIn(26, response.data["lengths"])

    def test_collections_endpoint(self):
        response = self.client.get("/api/v1/collections/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(c["slug"] == "best-sellers" for c in response.data["results"]))

    def test_filter_by_collection(self):
        response = self.client.get("/api/v1/products/?collection=best-sellers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], self.product1.slug)

    def test_category_subcategories_retrieval(self):
        response = self.client.get(f"/api/v1/categories/{self.category.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["subcategories"]) >= 1)
        self.assertEqual(response.data["subcategories"][0]["slug"], self.subcat.slug)

