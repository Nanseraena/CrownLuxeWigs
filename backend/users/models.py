from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    phone = models.CharField(max_length=40, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=180)
    phone = models.CharField(max_length=40)
    street_address = models.CharField(max_length=255)
    city_or_zone = models.CharField(max_length=120, default="Kampala")
    country = models.CharField(max_length=80, default="Uganda")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]
        verbose_name_plural = "addresses"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.street_address}, {self.city_or_zone}"
