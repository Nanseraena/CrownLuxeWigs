from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from cart.services import get_existing_cart
from .models import Coupon
from .serializers import CouponSerializer, ApplyCouponSerializer

class ApplyCouponView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"].strip().upper()

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response({"valid": False, "detail": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate against provided subtotal or fetch from request cart
        subtotal = serializer.validated_data.get("subtotal")
        if subtotal is None:
            try:
                cart = get_existing_cart(request)
                subtotal = cart.subtotal
            except Exception:
                subtotal = Decimal("0.00")

        valid, message = coupon.is_valid(Decimal(str(subtotal)))
        if not valid:
            return Response({"valid": False, "detail": message}, status=status.HTTP_400_BAD_REQUEST)

        discount_amount = coupon.calculate_discount(Decimal(str(subtotal)))
        new_total = max(Decimal("0.00"), Decimal(str(subtotal)) - discount_amount)

        return Response({
            "valid": True,
            "code": coupon.code,
            "description": coupon.description,
            "discount_type": coupon.discount_type,
            "value": coupon.value,
            "discount_amount": discount_amount,
            "new_total": new_total,
            "message": f"Coupon {coupon.code} applied successfully!"
        })

class ActiveCouponsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        coupons = Coupon.objects.filter(is_active=True)[:5]
        return Response(CouponSerializer(coupons, many=True).data)
