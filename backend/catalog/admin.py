from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage, Review

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "hair_type", "is_published", "is_featured", "is_new_arrival", "is_best_seller", "created_at")
    list_filter = ("category", "hair_type", "is_published", "is_featured", "is_new_arrival", "is_best_seller")
    search_fields = ("name", "description", "sku")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline, ProductImageInline]
    list_select_related = ("category",)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "length_inches", "color", "price", "stock_quantity", "is_active")
    list_filter = ("is_active", "product__category", "length_inches")
    search_fields = ("sku", "product__name")

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_primary", "sort_order", "alt_text")
    list_filter = ("is_primary",)
    search_fields = ("product__name", "alt_text")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "product", "rating", "is_verified_purchase", "is_approved", "created_at")
    list_filter = ("rating", "is_approved", "is_verified_purchase")
    search_fields = ("reviewer_name", "product__name", "comment")
