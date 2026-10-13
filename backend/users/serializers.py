from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile, Address

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone", "avatar_url"]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "full_name", "phone", "street_address", "city_or_zone", "country", "is_default", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "profile"]
        read_only_fields = ["id", "is_staff"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "phone"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email address already exists.")
        return value

    def create(self, validated_data):
        phone = validated_data.pop("phone", "")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, phone=phone)
        return user
