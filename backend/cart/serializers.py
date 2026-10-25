from rest_framework import serializers
from catalog.models import ProductVariant
from catalog.serializers import ProductImageSerializer, ProductListSerializer
from .models import Cart, CartItem, WishlistItem

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="variant.product_id", read_only=True)
    product_name = serializers.CharField(source="variant.product.name", read_only=True)
    product_slug = serializers.CharField(source="variant.product.slug", read_only=True)
    sku = serializers.CharField(source="variant.sku", read_only=True)
    variant_id = serializers.IntegerField(source="variant.id", read_only=True)
    variant_options = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(source="variant.price", max_digits=12, decimal_places=2, read_only=True)
    line_total = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product_name", "product_slug", "variant_id", "sku", "variant_options", "unit_price", "quantity", "line_total", "image", "added_at"]
    def get_variant_options(self, obj):
        v = obj.variant
        return {"length_inches": v.length_inches, "color": v.color, "texture": v.texture, "lace_type": v.lace_type, "density": v.density, "cap_size": v.cap_size}
    def get_image(self, obj):
        image = obj.variant.product.primary_image
        return ProductImageSerializer(image).data if image else None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ["token", "items", "item_count", "subtotal", "created_at", "updated_at"]

class AddCartItemSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, max_value=50, default=1)
    def validate_variant_id(self, value):
        try:
            variant = ProductVariant.objects.select_related("product").get(pk=value, is_active=True, product__is_published=True, product__category__is_active=True)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("This wig variant is unavailable.")
        self.context["variant"] = variant
        return value
    def validate(self, attrs):
        variant = self.context["variant"]
        if attrs["quantity"] > variant.stock_quantity:
            raise serializers.ValidationError({"quantity": f"Only {variant.stock_quantity} unit(s) are currently available."})
        return attrs

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=50)

class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    product_details = ProductListSerializer(source="product", read_only=True)
    class Meta:
        model = WishlistItem
        fields = ["id", "product", "product_name", "product_slug", "product_details", "created_at"]
        read_only_fields = ["id", "product_name", "product_slug", "created_at"]
