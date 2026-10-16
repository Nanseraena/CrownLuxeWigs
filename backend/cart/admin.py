from django.contrib import admin
from .models import Cart, CartItem, WishlistItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("added_at", "updated_at")
    autocomplete_fields = ("variant",)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token", "created_at", "updated_at")
    search_fields = ("token", "user__email", "user__username")
    inlines = [CartItemInline]
    autocomplete_fields = ("user",)
    list_select_related = ("user",)

@admin.register(WishlistItem)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    search_fields = ("user__email", "product__name")
    autocomplete_fields = ("user", "product")
    list_select_related = ("user", "product")
    readonly_fields = ("created_at",)
