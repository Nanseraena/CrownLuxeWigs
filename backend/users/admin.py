from django.contrib import admin
from .models import Profile, Address

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "created_at"]
    search_fields = ["user__username", "user__email", "phone"]
    autocomplete_fields = ("user",)
    list_select_related = ("user",)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user", "city_or_zone", "phone", "is_default", "created_at"]
    list_filter = ["city_or_zone", "is_default"]
    search_fields = ["full_name", "user__username", "street_address", "phone"]
    autocomplete_fields = ("user",)
    list_select_related = ("user",)
