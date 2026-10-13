import uuid
from django.conf import settings
from django.db import models
from catalog.models import ProductVariant

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=120)
    zone = models.CharField(max_length=100)
    base_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estimated_delivery = models.CharField(max_length=120, default="1-2 business days")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "base_fee"]

    def __str__(self):
        return f"{self.name} ({self.base_fee:,.0f} UGX)"

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("dispatched", "Dispatched"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("mtn_momo", "MTN Mobile Money"),
        ("airtel_money", "Airtel Money"),
        ("card", "Credit / Debit Card"),
        ("cod", "Cash on Delivery"),
    ]

    order_number = models.CharField(max_length=24, unique=True, editable=False, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wig_orders", on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    delivery_address = models.TextField()
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    currency = models.CharField(max_length=3, default="UGX")
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=40, blank=True)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default="mtn_momo")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="pending")
    payment_reference = models.CharField(max_length=180, blank=True)
    tracking_number = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = "CLM-" + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} ({self.customer_name})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name="order_items", on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=220)
    sku = models.CharField(max_length=80)
    variant_description = models.JSONField(default=dict, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
