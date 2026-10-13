from decimal import Decimal
from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage Discount"),
        ("fixed", "Fixed Amount Discount"),
    ]

    code = models.CharField(max_length=40, unique=True, db_index=True)
    description = models.CharField(max_length=200, blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default="percentage")
    value = models.DecimalField(max_digits=12, decimal_places=2, help_text="Percentage (e.g. 15 for 15%) or Fixed amount in UGX")
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def is_valid(self, subtotal=Decimal("0.00")):
        now = timezone.now()
        if not self.is_active:
            return False, "This coupon is inactive."
        if self.start_date and now < self.start_date:
            return False, "This coupon has not started yet."
        if self.expiry_date and now > self.expiry_date:
            return False, "This coupon has expired."
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False, "This coupon has reached its maximum usage limit."
        if subtotal < self.min_order_amount:
            return False, f"Minimum order subtotal of {self.min_order_amount:,.0f} UGX is required."
        return True, "Valid coupon."

    def calculate_discount(self, subtotal):
        valid, msg = self.is_valid(subtotal)
        if not valid:
            return Decimal("0.00")
        if self.discount_type == "percentage":
            discount = (Decimal(str(self.value)) / Decimal("100")) * subtotal
            if self.max_discount and discount > self.max_discount:
                discount = self.max_discount
        else:
            discount = min(self.value, subtotal)
        return round(discount, 2)

    def __str__(self):
        return f"{self.code} ({self.discount_type}: {self.value})"
