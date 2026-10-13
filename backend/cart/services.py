from django.db import transaction
import uuid
from rest_framework.exceptions import ValidationError, NotFound
from catalog.models import ProductVariant
from .models import Cart, CartItem

def get_or_create_cart(request):
    """Account carts are user-owned; guests pass a UUID in X-Cart-Token."""
    if request.user and request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    token = request.headers.get("X-Cart-Token") or request.data.get("cart_token") or request.query_params.get("cart_token")
    if token:
        try:
            parsed_token = uuid.UUID(str(token))
            cart = Cart.objects.filter(token=parsed_token, user__isnull=True).first()
            if cart is None:
                cart = Cart.objects.create(token=parsed_token)
            return cart
        except (ValueError, TypeError):
            pass
    cart = Cart.objects.create()
    return cart

def get_existing_cart(request):
    if request.user and request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart: return Cart.objects.create(user=request.user)
        return cart
    token = request.headers.get("X-Cart-Token") or request.query_params.get("cart_token") or request.data.get("cart_token")
    if not token: raise ValidationError({"cart_token": "Send X-Cart-Token for guest cart requests."})
    try: return Cart.objects.get(token=token, user__isnull=True)
    except (Cart.DoesNotExist, ValueError): raise NotFound("Cart not found. Create a cart by adding an item first.")

@transaction.atomic
def add_variant(cart, variant_id, quantity):
    try:
        variant = ProductVariant.objects.select_for_update().select_related("product", "product__category").get(
            pk=variant_id, is_active=True, product__is_published=True, product__category__is_active=True
        )
    except ProductVariant.DoesNotExist:
        raise ValidationError({"variant_id": "This wig variant is unavailable."})

    item = CartItem.objects.select_for_update().filter(cart=cart, variant=variant).first()
    new_quantity = quantity + (item.quantity if item else 0)
    if variant.stock_quantity < new_quantity:
        raise ValidationError({"quantity": f"Only {variant.stock_quantity} unit(s) are available; your cart would contain {new_quantity}."})

    if item:
        item.quantity = new_quantity
        item.save(update_fields=["quantity", "updated_at"])
    else:
        item = CartItem.objects.create(cart=cart, variant=variant, quantity=quantity)
    return item

@transaction.atomic
def update_item_quantity(cart, item_id, quantity):
    try:
        item = CartItem.objects.select_for_update().select_related("variant").get(pk=item_id, cart=cart)
    except CartItem.DoesNotExist: raise NotFound("Cart item not found.")
    if not item.variant.is_active or not item.variant.product.is_published:
        raise ValidationError({"item": "This product is no longer available."})
    if quantity > item.variant.stock_quantity:
        raise ValidationError({"quantity": f"Only {item.variant.stock_quantity} unit(s) are currently available."})
    item.quantity = quantity
    item.save(update_fields=["quantity", "updated_at"])
    return item

@transaction.atomic
def merge_guest_cart(user_cart, guest_token):
    """Safely merges guest cart items into authenticated user cart."""
    try:
        parsed_token = uuid.UUID(str(guest_token))
        guest_cart = Cart.objects.filter(token=parsed_token, user__isnull=True).prefetch_related("items__variant").first()
    except (ValueError, TypeError):
        return user_cart

    if not guest_cart or not guest_cart.items.exists():
        return user_cart

    for g_item in guest_cart.items.all():
        variant = g_item.variant
        if not variant.is_active or not variant.product.is_published or variant.stock_quantity <= 0:
            continue

        existing_item = CartItem.objects.filter(cart=user_cart, variant=variant).first()
        desired_quantity = g_item.quantity + (existing_item.quantity if existing_item else 0)
        final_quantity = min(desired_quantity, variant.stock_quantity)

        if existing_item:
            existing_item.quantity = final_quantity
            existing_item.save(update_fields=["quantity", "updated_at"])
        else:
            CartItem.objects.create(cart=user_cart, variant=variant, quantity=final_quantity)

    guest_cart.items.all().delete()
    guest_cart.delete()
    user_cart.refresh_from_db()
    return user_cart
