import uuid
from django.db import models
from orders.models import Order

class Payment(models.Model):
    PROVIDER_CHOICES = [
        ("mtn_momo", "MTN Mobile Money"),
        ("airtel_money", "Airtel Money"),
        ("card", "Credit / Debit Card"),
        ("cod", "Cash on Delivery"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    order = models.OneToOneField(Order, related_name="payment", on_delete=models.CASCADE)
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, default="UGX")
    phone_number = models.CharField(max_length=40, blank=True)
    transaction_reference = models.CharField(max_length=120, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    provider_metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.transaction_reference:
            self.transaction_reference = f"PAY-{self.provider.upper()[:3]}-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_reference} - {self.order.order_number} ({self.status})"
