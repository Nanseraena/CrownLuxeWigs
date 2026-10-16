from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.db.models import Sum, Count, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError, NotFound

from cart.services import get_existing_cart
from catalog.models import ProductVariant, Product
from promotions.models import Coupon
from .models import Order, OrderItem, DeliveryMethod
from .serializers import CheckoutSerializer, OrderSerializer, DeliveryMethodSerializer, PublicOrderTrackingSerializer

class DeliveryMethodViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = DeliveryMethod.objects.filter(is_active=True)
    serializer_class = DeliveryMethodSerializer

class CheckoutView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        cart = get_existing_cart(request)
        items = list(cart.items.select_related("variant", "variant__product").all())
        if not items:
            raise ValidationError({"cart": "Your cart is empty."})

        # Lock and revalidate each variant, calculate subtotal authoritatively
        locked = {}
        subtotal = Decimal("0.00")
        for cart_item in items:
            try:
                variant = ProductVariant.objects.select_for_update().select_related("product").get(
                    pk=cart_item.variant_id,
                    is_active=True,
                    product__is_published=True
                )
            except ProductVariant.DoesNotExist:
                raise ValidationError({"cart": f"Item '{cart_item.variant.sku}' is no longer available."})

            if variant.stock_quantity < cart_item.quantity:
                raise ValidationError({"cart": f"Insufficient stock for {variant.product.name} ({variant.sku}). Available: {variant.stock_quantity}."})

            locked[cart_item.pk] = variant
            subtotal += variant.price * cart_item.quantity

        # Delivery fee calculation
        delivery_method = None
        delivery_fee = Decimal("0.00")
        if validated.get("delivery_method_id"):
            try:
                delivery_method = DeliveryMethod.objects.get(pk=validated["delivery_method_id"], is_active=True)
                delivery_fee = delivery_method.base_fee
            except DeliveryMethod.DoesNotExist:
                pass

        # Coupon discount calculation
        discount_amount = Decimal("0.00")
        coupon_code = validated.get("coupon_code", "").strip().upper()
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                valid, _ = coupon.is_valid(subtotal)
                if valid:
                    discount_amount = coupon.calculate_discount(subtotal)
                    coupon.used_count += 1
                    coupon.save(update_fields=["used_count"])
            except Coupon.DoesNotExist:
                pass

        total = max(Decimal("0.00"), subtotal + delivery_fee - discount_amount)

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=validated["customer_name"],
            email=validated["email"],
            phone=validated["phone"],
            delivery_address=validated["delivery_address"],
            delivery_method=delivery_method,
            currency=getattr(settings, "DEFAULT_CURRENCY", "UGX"),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            discount_amount=discount_amount,
            coupon_code=coupon_code,
            total=total,
            payment_method=validated.get("payment_method", "mtn_momo"),
            payment_status="pending",
            notes=validated.get("notes", "")
        )

        for cart_item in items:
            variant = locked[cart_item.pk]
            variant.stock_quantity -= cart_item.quantity
            variant.save(update_fields=["stock_quantity", "updated_at"])

            OrderItem.objects.create(
                order=order,
                variant=variant,
                product_name=variant.product.name,
                sku=variant.sku,
                variant_description={
                    "length_inches": variant.length_inches,
                    "color": variant.color,
                    "texture": variant.texture,
                    "lace_type": variant.lace_type,
                    "density": variant.density,
                    "cap_size": variant.cap_size
                },
                unit_price=variant.price,
                quantity=cart_item.quantity,
                line_total=variant.price * cart_item.quantity
            )

        cart.items.all().delete()
        return Response({
            "message": "Order created successfully.",
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    lookup_field = "order_number"

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related("items", "delivery_method").order_by("-created_at")
        return Order.objects.filter(user=user).prefetch_related("items", "delivery_method").order_by("-created_at")

class OrderTrackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, order_number):
        try:
            order = Order.objects.prefetch_related("items", "delivery_method").get(order_number__iexact=order_number)
            # A tracking URL is intentionally public for guest checkout, but
            # it must never reveal delivery addresses, contact data, notes, or
            # payment references. Authenticated customers use /orders/ for
            # their complete order record.
            return Response(PublicOrderTrackingSerializer(order).data)
        except Order.DoesNotExist:
            raise NotFound("Order not found with that order number.")

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        paid_orders = Order.objects.filter(payment_status="paid")
        total_revenue = paid_orders.aggregate(Sum("total"))["total__sum"] or Decimal("0.00")
        pending_orders = Order.objects.filter(status__in=["pending", "processing"]).count()
        
        low_stock_variants = ProductVariant.objects.filter(stock_quantity__lte=5, is_active=True).select_related("product")[:10]
        low_stock_data = [{
            "id": v.id,
            "product_name": v.product.name,
            "sku": v.sku,
            "stock_quantity": v.stock_quantity,
            "price": v.price
        } for v in low_stock_variants]

        recent_orders = Order.objects.prefetch_related("items").order_by("-created_at")[:8]

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "pending_orders": pending_orders,
            "low_stock_count": ProductVariant.objects.filter(stock_quantity__lte=5, is_active=True).count(),
            "low_stock_items": low_stock_data,
            "recent_orders": OrderSerializer(recent_orders, many=True).data
        })
