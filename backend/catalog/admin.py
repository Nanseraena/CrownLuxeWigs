from django.contrib import admin
from .models import Category, Collection, Product, ProductVariant, ProductImage, Review

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ("sku", "length_inches", "color", "texture", "lace_type", "density", "price", "compare_at_price", "stock_quantity", "is_active")

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ("image_url", "alt_text", "is_primary", "sort_order")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_active", "sort_order")
    list_filter = ("is_active", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order", "name")
    autocomplete_fields = ("parent",)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order", "name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "texture", "default_color", "is_published", "is_featured", "is_best_seller", "updated_at")
    list_filter = ("category", "hair_origin", "hair_type", "is_published", "is_featured", "is_new_arrival", "is_best_seller")
    search_fields = ("name", "description", "sku")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category", "subcategory", "collections")
    inlines = [ProductVariantInline, ProductImageInline]
    list_select_related = ("category", "subcategory")
    list_editable = ("is_published", "is_featured", "is_best_seller")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    actions = ("publish_products", "unpublish_products")
    fieldsets = (
        ("Identity", {"fields": ("name", "slug", "sku", "category", "subcategory", "collections")}),
        ("Hair specification", {"fields": ("hair_type", "hair_origin", "texture", "default_length_inches", "default_color", "default_lace_type")}),
        ("Storefront", {"fields": ("description", "is_published", "is_featured", "is_new_arrival", "is_best_seller")}),
        ("Audit", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.action(description="Publish selected products")
    def publish_products(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected products")
    def unpublish_products(self, request, queryset):
        queryset.update(is_published=False)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "length_inches", "color", "price", "stock_quantity", "is_active")
    list_filter = ("is_active", "product__category", "length_inches")
    search_fields = ("sku", "product__name")
    list_select_related = ("product",)
    list_editable = ("stock_quantity", "is_active")
    autocomplete_fields = ("product",)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_primary", "sort_order", "alt_text")
    list_filter = ("is_primary",)
    search_fields = ("product__name", "alt_text")
    list_select_related = ("product",)
    list_editable = ("is_primary", "sort_order")
    autocomplete_fields = ("product",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "product", "rating", "is_verified_purchase", "is_approved", "created_at")
    list_filter = ("rating", "is_approved", "is_verified_purchase")
    search_fields = ("reviewer_name", "product__name", "comment")
    list_editable = ("is_approved",)
    list_select_related = ("product",)
    autocomplete_fields = ("product", "user")
