from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import override_settings
from unittest.mock import patch
from .models import GoogleIdentity

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

    def test_password_login_creates_persistent_server_session_and_logout_invalidates_it(self):
        User.objects.create_user(username="sessionuser", email="session@example.com", password="StrongPassword123!")
        response = self.client.post("/api/v1/auth/login/", {"identifier": "session@example.com", "password": "StrongPassword123!"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("crownluxe_sessionid", response.cookies)
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 200)
        self.assertEqual(self.client.post("/api/v1/auth/logout/", {}, format="json").status_code, 204)
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 403)

    @override_settings(GOOGLE_OAUTH_CLIENT_ID="test-google-client")
    @patch("users.views.id_token.verify_oauth2_token")
    def test_google_login_creates_and_reuses_identity_by_subject(self, verify):
        verify.return_value = {
            "sub": "google-unique-subject", "email": "google@example.com", "email_verified": True,
            "iss": "https://accounts.google.com", "given_name": "Google", "family_name": "Customer",
        }
        first = self.client.post("/api/v1/auth/google/", {"credential": "signed-token"}, format="json")
        self.assertEqual(first.status_code, 200, first.data)
        self.assertEqual(GoogleIdentity.objects.count(), 1)
        second = self.client.post("/api/v1/auth/google/", {"credential": "signed-token"}, format="json")
        self.assertEqual(second.status_code, 200)
        self.assertEqual(User.objects.filter(email="google@example.com").count(), 1)

    @override_settings(GOOGLE_OAUTH_CLIENT_ID="test-google-client")
    @patch("users.views.id_token.verify_oauth2_token")
    def test_google_login_does_not_link_an_existing_password_account_by_email(self, verify):
        User.objects.create_user(username="local", email="existing@example.com", password="StrongPassword123!")
        verify.return_value = {"sub": "different-subject", "email": "existing@example.com", "email_verified": True, "iss": "accounts.google.com"}
        response = self.client.post("/api/v1/auth/google/", {"credential": "signed-token"}, format="json")
        self.assertEqual(response.status_code, 409, response.data)
        self.assertEqual(GoogleIdentity.objects.count(), 0)
