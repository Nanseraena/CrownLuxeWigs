from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "image_url", "sort_order"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image_url", "alt_text", "is_primary", "sort_order"]

class ProductVariantSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)
    class Meta:
        model = ProductVariant
        fields = ["id", "sku", "length_inches", "color", "texture", "lace_type", "density", "cap_size", "price", "compare_at_price", "stock_quantity", "in_stock"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "product", "reviewer_name", "rating", "title", "comment", "is_verified_purchase", "created_at"]
        read_only_fields = ["id", "is_verified_purchase", "created_at"]

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    min_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    compare_at_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category", "hair_type", "texture",
            "default_length_inches", "default_color", "default_lace_type", "min_price",
            "compare_at_price", "primary_image", "average_rating", "review_count",
            "is_featured", "is_new_arrival", "is_best_seller", "created_at"
        ]

    def get_primary_image(self, obj):
        image = obj.primary_image
        return ProductImageSerializer(image).data if image else None

class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ["images", "variants", "reviews", "updated_at"]

    def get_variants(self, obj):
        variants = obj.variants.filter(is_active=True).order_by("price")
        return ProductVariantSerializer(variants, many=True).data

    def get_reviews(self, obj):
        approved = obj.reviews.filter(is_approved=True)[:10]
        return ReviewSerializer(approved, many=True).data
