from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import override_settings
from unittest.mock import patch
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Address, GoogleIdentity

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

    @override_settings(GOOGLE_OAUTH_CLIENT_ID="test-google-client")
    @patch("users.views.id_token.verify_oauth2_token")
    def test_google_login_rejects_a_token_from_an_untrusted_issuer(self, verify):
        verify.return_value = {
            "sub": "untrusted-subject", "email": "attacker@example.com", "email_verified": True,
            "iss": "https://malicious.example",
        }
        response = self.client.post("/api/v1/auth/google/", {"credential": "invalid-token"}, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(GoogleIdentity.objects.count(), 0)

    def test_session_authenticated_write_requires_a_csrf_token(self):
        user = User.objects.create_user(username="csrfuser", email="csrf@example.com", password="StrongPassword123!")
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.force_login(user)

        blocked = csrf_client.patch("/api/v1/auth/me/", {"first_name": "Changed"}, format="json")
        self.assertEqual(blocked.status_code, 403)

        csrf_client.get("/api/v1/auth/csrf/")
        csrf_client.credentials(HTTP_X_CSRFTOKEN=csrf_client.cookies["csrftoken"].value)
        allowed = csrf_client.patch("/api/v1/auth/me/", {"first_name": "Changed"}, format="json")
        self.assertEqual(allowed.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Changed")

    @patch("users.views.send_password_reset_email")
    def test_password_reset_does_not_disclose_whether_an_email_exists(self, send_reset):
        User.objects.create_user(username="resetuser", email="reset@example.com", password="StrongPassword123!")
        known = self.client.post("/api/v1/auth/password-reset/", {"email": "reset@example.com"}, format="json")
        unknown = self.client.post("/api/v1/auth/password-reset/", {"email": "unknown@example.com"}, format="json")

        self.assertEqual(known.status_code, 200)
        self.assertEqual(unknown.status_code, 200)
        self.assertEqual(known.data, unknown.data)
        self.assertEqual(send_reset.call_count, 1)

    def test_password_reset_token_is_single_use(self):
        user = User.objects.create_user(username="singleuse", email="singleuse@example.com", password="StrongPassword123!")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        payload = {"uid": uid, "token": token, "password": "AnotherStrongPassword123!"}

        first = self.client.post("/api/v1/auth/password-reset/confirm/", payload, format="json")
        second = self.client.post("/api/v1/auth/password-reset/confirm/", payload, format="json")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 400)

    def test_user_cannot_read_or_modify_another_users_address(self):
        owner = User.objects.create_user(username="owner", email="owner@example.com", password="StrongPassword123!")
        other = User.objects.create_user(username="other", email="other@example.com", password="StrongPassword123!")
        address = Address.objects.create(
            user=owner, full_name="Owner", phone="0700000000",
            street_address="Private Road", city_or_zone="Kampala",
        )
        self.client.force_authenticate(other)

        self.assertEqual(self.client.get(f"/api/v1/addresses/{address.pk}/").status_code, 404)
        self.assertEqual(
            self.client.patch(f"/api/v1/addresses/{address.pk}/", {"city_or_zone": "Changed"}, format="json").status_code,
            404,
        )
        address.refresh_from_db()
        self.assertEqual(address.city_or_zone, "Kampala")
