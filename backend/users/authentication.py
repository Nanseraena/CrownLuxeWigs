from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    """Accept the store's username or its unique email address at sign-in."""

    def validate(self, attrs):
        identifier = attrs.get(self.username_field, "").strip()
        user_model = get_user_model()
        if "@" in identifier:
            user = user_model.objects.filter(email__iexact=identifier).only(self.username_field).first()
            if user:
                attrs[self.username_field] = getattr(user, self.username_field)
        return super().validate(attrs)
