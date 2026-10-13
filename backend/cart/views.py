from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from catalog.models import Product
from .models import Cart, CartItem, WishlistItem
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, WishlistItemSerializer
from .services import get_or_create_cart, get_existing_cart, add_variant, update_item_quantity, merge_guest_cart

class CartView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        cart = get_existing_cart(request)
        cart = type(cart).objects.prefetch_related("items__variant__product__images").get(pk=cart.pk)
        return Response(CartSerializer(cart).data)

class CartItemView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_cart(request)
        item = add_variant(cart, serializer.validated_data["variant_id"], serializer.validated_data["quantity"])
        cart.refresh_from_db()
        return Response({"message": "Item added to cart.", "cart": CartSerializer(cart).data, "item_id": item.id}, status=status.HTTP_201_CREATED)

class CartItemDetailView(APIView):
    permission_classes = [AllowAny]
    def patch(self, request, item_id):
        cart = get_existing_cart(request)
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_item_quantity(cart, item_id, serializer.validated_data["quantity"])
        cart.refresh_from_db()
        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        cart = get_existing_cart(request)
        deleted, _ = CartItem.objects.filter(cart=cart, pk=item_id).delete()
        if not deleted: return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        cart.refresh_from_db()
        return Response(CartSerializer(cart).data)

class CartClearView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request):
        cart = get_existing_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)

class MergeCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        guest_token = request.data.get("guest_token") or request.headers.get("X-Cart-Token")
        if not guest_token:
            return Response({"error": "guest_token is required."}, status=status.HTTP_400_BAD_REQUEST)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        merged_cart = merge_guest_cart(user_cart, guest_token)
        return Response({
            "message": "Cart merged successfully.",
            "cart": CartSerializer(merged_cart).data
        })

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = WishlistItem.objects.filter(user=request.user, product__is_published=True).select_related("product")
        return Response(WishlistItemSerializer(qs, many=True).data)

class WishlistItemView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            product = Product.objects.get(pk=request.data.get("product_id"), is_published=True)
        except (Product.DoesNotExist, ValueError, TypeError):
            raise ValidationError({"product_id": "Published product not found."})
        item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        return Response(WishlistItemSerializer(item).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def delete(self, request, product_id):
        deleted, _ = WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
        if not deleted: return Response({"detail": "Wishlist item not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
