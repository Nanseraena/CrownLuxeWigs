import re
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.db import transaction
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address, Profile, GoogleIdentity
from .serializers import RegisterSerializer, UserSerializer, AddressSerializer
from .emails import send_password_reset_email, send_welcome_email

User = get_user_model()


def _google_username(email, subject):
    base = re.sub(r"[^a-zA-Z0-9_.-]", "", email.split("@", 1)[0])[:120] or "google_user"
    candidate = base
    suffix = 1
    while User.objects.filter(username__iexact=candidate).exists():
        candidate = f"{base[:110]}_{suffix}"
        suffix += 1
    return candidate


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


@method_decorator(csrf_protect, name="dispatch")
class GoogleLoginView(APIView):
    """Exchange a GIS ID token for a rotated, persistent Django session."""
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        credential = str(request.data.get("credential", ""))
        if not credential or not settings.GOOGLE_OAUTH_CLIENT_ID:
            return Response({"detail": "Google sign-in is not configured."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            claims = id_token.verify_oauth2_token(credential, google_requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID)
            if claims.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
                raise ValueError("Invalid issuer")
            if not claims.get("sub") or not claims.get("email") or not claims.get("email_verified"):
                raise ValueError("Google account email is not verified")
        except Exception:
            return Response({"detail": "Google credential is invalid or expired."}, status=status.HTTP_401_UNAUTHORIZED)

        with transaction.atomic():
            identity = GoogleIdentity.objects.select_for_update().select_related("user").filter(subject=claims["sub"]).first()
            if identity:
                user = identity.user
            else:
                # Matching email alone is never proof that an existing local account owns this Google identity.
                if User.objects.filter(email__iexact=claims["email"]).exists():
                    return Response({"detail": "An account with this email already exists. Sign in with its password to link it through account settings."}, status=status.HTTP_409_CONFLICT)
                user = User.objects.create_user(
                    username=_google_username(claims["email"], claims["sub"]), email=claims["email"],
                    first_name=claims.get("given_name", ""), last_name=claims.get("family_name", ""),
                )
                user.set_unusable_password()
                user.save(update_fields=["password"])
                Profile.objects.create(user=user, avatar_url=claims.get("picture", ""))
                GoogleIdentity.objects.create(user=user, subject=claims["sub"], email_at_link_time=claims["email"])
        if not user.is_active:
            return Response({"detail": "This account is inactive."}, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        return Response({"user": UserSerializer(user).data})


@method_decorator(csrf_protect, name="dispatch")
class PasswordLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        identifier = str(request.data.get("identifier", request.data.get("username", ""))).strip()
        password = request.data.get("password", "")
        username = identifier
        if "@" in identifier:
            user = User.objects.filter(email__iexact=identifier).only("username").first()
            username = user.username if user else identifier
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response({"user": UserSerializer(user).data})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_welcome_email(user)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Account created successfully.",
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        # Always return the same response: never reveal which emails have accounts.
        user = User.objects.filter(email__iexact=email, is_active=True).first() if email else None
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/account/reset-password?uid={uid}&token={token}"
            send_password_reset_email(user, reset_url)
        return Response({"detail": "If an account exists for this email, a reset link has been sent."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        uid = request.data.get("uid", "")
        token = request.data.get("token", "")
        password = request.data.get("password", "")
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id, is_active=True)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "This password reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "This password reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(password, user)
        except Exception as error:
            return Response({"password": list(getattr(error, "messages", ["Choose a stronger password."]))}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save(update_fields=["password"])
        return Response({"detail": "Your password has been reset. You can now sign in."})

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        user = request.user
        data = request.data
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "email" in data and data["email"] != user.email:
            if User.objects.filter(email__iexact=data["email"]).exclude(pk=user.pk).exists():
                return Response({"email": "Email is already taken."}, status=status.HTTP_400_BAD_REQUEST)
            user.email = data["email"]
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        if "phone" in data:
            profile.phone = data["phone"]
        if "avatar_url" in data:
            profile.avatar_url = data["avatar_url"]
        profile.save()

        return Response(UserSerializer(user).data)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
