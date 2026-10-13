import uuid
from django.conf import settings
from django.db import models
from catalog.models import ProductVariant, Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wig_carts", on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["-updated_at"]
    def __str__(self): return f"Cart {self.token}"
    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.select_related("variant").all()), start=0)
    @property
    def item_count(self): return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name="cart_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["cart", "variant"], name="unique_variant_per_cart")]
    @property
    def line_total(self): return self.variant.price * self.quantity
    def __str__(self): return f"{self.variant.sku} x {self.quantity}"

class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wig_wishlist_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="wishlisted_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="unique_wishlist_product_per_user")]
        ordering = ["-created_at"]
