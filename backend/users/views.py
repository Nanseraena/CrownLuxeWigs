from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address, Profile
from .serializers import RegisterSerializer, UserSerializer, AddressSerializer
from .emails import send_password_reset_email, send_welcome_email

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_welcome_email(user)
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
