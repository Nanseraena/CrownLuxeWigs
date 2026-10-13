from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from catalog.views import CategoryViewSet, ProductViewSet
from cart.views import (
    CartView, CartItemView, CartItemDetailView, CartClearView,
    MergeCartView, WishlistView, WishlistItemView
)
from orders.views import (
    CheckoutView, OrderViewSet, DeliveryMethodViewSet,
    OrderTrackView, AdminDashboardStatsView
)
from promotions.views import ApplyCouponView, ActiveCouponsView
from payments.views import (
    InitiatePaymentView, VerifyPaymentView,
    PaymentStatusView, PaymentWebhookView
)
from users.views import RegisterView, MeView, AddressViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet, basename="order")
router.register("delivery-methods", DeliveryMethodViewSet, basename="delivery-method")
router.register("addresses", AddressViewSet, basename="address")

@api_view(["GET"])
@permission_classes([AllowAny])
def health(_request):
    return Response({"status": "ok", "service": "crownluxe-wig-store-api", "version": "1.0.0"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", health),
    
    # Auth endpoints
    path("api/v1/auth/register/", RegisterView.as_view(), name="register"),
    path("api/v1/auth/me/", MeView.as_view(), name="me"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Router endpoints (catalog, orders, addresses, delivery-methods)
    path("api/v1/", include(router.urls)),

    # Cart & Wishlist endpoints
    path("api/v1/cart/", CartView.as_view(), name="cart"),
    path("api/v1/cart/items/", CartItemView.as_view(), name="cart-items"),
    path("api/v1/cart/items/<int:item_id>/", CartItemDetailView.as_view(), name="cart-item-detail"),
    path("api/v1/cart/clear/", CartClearView.as_view(), name="cart-clear"),
    path("api/v1/cart/merge/", MergeCartView.as_view(), name="cart-merge"),
    path("api/v1/wishlist/", WishlistView.as_view(), name="wishlist"),
    path("api/v1/wishlist/items/", WishlistItemView.as_view(), name="wishlist-items"),
    path("api/v1/wishlist/items/<int:product_id>/", WishlistItemView.as_view(), name="wishlist-item-detail"),

    # Checkout & Orders
    path("api/v1/checkout/", CheckoutView.as_view(), name="checkout"),
    path("api/v1/orders/track/<str:order_number>/", OrderTrackView.as_view(), name="order-track"),

    # Promotions & Coupons
    path("api/v1/promotions/apply/", ApplyCouponView.as_view(), name="apply-coupon"),
    path("api/v1/promotions/active/", ActiveCouponsView.as_view(), name="active-coupons"),

    # Payments
    path("api/v1/payments/initiate/", InitiatePaymentView.as_view(), name="payment-initiate"),
    path("api/v1/payments/verify/", VerifyPaymentView.as_view(), name="payment-verify"),
    path("api/v1/payments/status/<str:reference>/", PaymentStatusView.as_view(), name="payment-status"),
    path("api/v1/payments/webhook/", PaymentWebhookView.as_view(), name="payment-webhook"),

    # Admin Dashboard Stats
    path("api/v1/admin/dashboard-stats/", AdminDashboardStatsView.as_view(), name="admin-dashboard-stats"),

    # OpenAPI Schema & Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
