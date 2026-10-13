from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_customer_registration(self):
        response = self.client.post("/api/v1/auth/register/", {
            "username": "florence_k",
            "email": "florence@example.com",
            "first_name": "Florence",
            "last_name": "Katusiime",
            "password": "SecurePassword123!",
            "phone": "+256755443322"
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertEqual(response.data["user"]["email"], "florence@example.com")
        self.assertTrue(User.objects.filter(username="florence_k").exists())

    def test_authenticated_profile_and_addresses(self):
        user = User.objects.create_user(username="testuser", email="user@test.com", password="password123")
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "testuser")

        # Create address
        addr_resp = self.client.post("/api/v1/addresses/", {
            "full_name": "Test User",
            "phone": "+256700000000",
            "street_address": "Plot 24 Lugogo Bypass",
            "city_or_zone": "Kampala Central",
            "is_default": True
        }, format="json")
        self.assertEqual(addr_resp.status_code, 201)
        self.assertEqual(addr_resp.data["city_or_zone"], "Kampala Central")
