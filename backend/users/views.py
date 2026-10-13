from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address, Profile
from .serializers import RegisterSerializer, UserSerializer, AddressSerializer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Account created successfully.",
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

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
