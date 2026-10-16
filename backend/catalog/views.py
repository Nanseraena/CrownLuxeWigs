from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Exists, OuterRef, Min, Max, Q, Count, Avg
from .models import Category, Collection, Product, ProductVariant, Review
from .taxonomy import (
    CANONICAL_TEXTURES, TEXTURE_MAP,
    resolve_colors, resolve_constructions, resolve_product_types,
    resolve_styles, resolve_textures,
)
from .serializers import (
    CategorySerializer, CollectionSerializer,
    ProductListSerializer, ProductDetailSerializer, ReviewSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related("subcategories")
    lookup_field = "slug"

    @action(detail=False, methods=["get"], url_path="all")
    def all_categories(self, request):
        qs = Category.objects.filter(is_active=True).select_related("parent")
        return Response(CategorySerializer(qs, many=True).data)

class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    queryset = Collection.objects.filter(is_active=True)
    lookup_field = "slug"

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "texture", "default_color", "default_lace_type", "category__name", "hair_origin"]
    ordering_fields = ["created_at", "name", "price_order", "is_best_seller"]
    ordering = ["-created_at"]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # Catalog data and its image paths are public storefront metadata.
        # Use short shared caching because image URLs are mutable, rather than
        # incorrectly declaring them immutable.
        if response.status_code == 200:
            response["Cache-Control"] = "public, max-age=60"
        return response

    @staticmethod
    def _values(params, *names):
        """Read repeated or comma-separated values without silently widening a filter."""
        values = []
        for name in names:
            for raw in params.getlist(name):
                values.extend(value.strip() for value in raw.split(",") if value.strip())
        return values

    def get_queryset(self):
        qs = Product.objects.filter(is_published=True, category__is_active=True)\
            .select_related("category", "subcategory")\
            .prefetch_related("images", "variants", "reviews", "collections")\
            .annotate(price_order=Min("variants__price"))

        params = self.request.query_params

        # DRF's generic SearchFilter is intentionally broad (it searches
        # descriptions too). When a search term is a supported texture, make
        # it a semantic texture constraint as well so prose mentioning
        # "bone straight" cannot surface an unrelated curl pattern.
        search_term = params.get("search", "").strip()
        normalized_search = search_term.lower()
        if normalized_search in TEXTURE_MAP or any(
            normalized_search == texture.lower() for texture in CANONICAL_TEXTURES
        ):
            qs = qs.filter(texture__in=resolve_textures([search_term]))

        # 1. Category and Subcategory
        cat_slug = params.get("category__slug") or params.get("category")
        if cat_slug:
            qs = qs.filter(
                Q(category__slug=cat_slug) |
                Q(category__parent__slug=cat_slug) |
                Q(subcategory__slug=cat_slug)
            )

        subcat_slug = params.get("subcategory__slug") or params.get("subcategory")
        if subcat_slug:
            qs = qs.filter(subcategory__slug=subcat_slug)

        # 2. Collection
        col_slug = params.get("collection")
        if col_slug:
            qs = qs.filter(collections__slug=col_slug)

        # 3. Flags (featured, new arrival, best seller)
        if params.get("is_featured", "").lower() in ("true", "1", "yes"):
            qs = qs.filter(is_featured=True)
        if params.get("is_new_arrival", "").lower() in ("true", "1", "yes"):
            qs = qs.filter(is_new_arrival=True)
        if params.get("is_best_seller", "").lower() in ("true", "1", "yes"):
            qs = qs.filter(is_best_seller=True)

        # 4. Hair Origin (multi-select supported)
        origins = [value.lower() for value in self._values(params, "hair_origin")]
        if origins:
            qs = qs.filter(hair_origin__in=origins)

        # 5. Hair Material / Type
        materials = [value.lower() for value in self._values(params, "hair_material", "hair_type")]
        if materials:
            qs = qs.filter(hair_type__in=materials)

        # 6. Texture
        textures = resolve_textures(self._values(params, "texture"))
        if textures:
            qs = qs.filter(texture__in=textures)

        # These are independent dimensions. Repeated values are ORed within a
        # dimension while each dimension narrows the queryset (AND semantics).
        product_types = resolve_product_types(self._values(params, "product_type", "type"))
        if product_types:
            qs = qs.filter(product_type__in=product_types)

        styles = resolve_styles(self._values(params, "style"))
        if styles:
            qs = qs.filter(style__in=styles)

        constructions = resolve_constructions(self._values(params, "construction"))
        if constructions:
            qs = qs.filter(construction__in=constructions)

        # 7. Color (Multi-select matched against active variants)
        colors = resolve_colors(self._values(params, "color"))
        if colors:
            qs = qs.annotate(
                _has_matching_color=Exists(
                    ProductVariant.objects.filter(
                        product_id=OuterRef("pk"), is_active=True, color__in=colors
                    )
                )
            ).filter(_has_matching_color=True)

        # 8. Length in Inches (Multi-select matched against active variants)
        lengths = self._values(params, "length_inches", "length")

        length_q = Q()
        if lengths:
            int_lengths = []
            for l in lengths:
                try:
                    int_lengths.append(int(l))
                except ValueError:
                    pass
            if int_lengths:
                length_q |= Q(length_inches__in=int_lengths)
            else:
                return qs.none()

        # Length quick groups: short (10-14), medium (16-20), long (22-26), extra_long (28-36)
        len_group = params.get("length_group")
        if len_group == "short":
            length_q |= Q(length_inches__gte=10, length_inches__lte=14)
        elif len_group == "medium":
            length_q |= Q(length_inches__gte=16, length_inches__lte=20)
        elif len_group == "long":
            length_q |= Q(length_inches__gte=22, length_inches__lte=26)
        elif len_group == "extra_long":
            length_q |= Q(length_inches__gte=28, length_inches__lte=36)
        elif len_group:
            return qs.none()

        if length_q:
            qs = qs.annotate(
                _has_matching_length=Exists(
                    ProductVariant.objects.filter(product_id=OuterRef("pk"), is_active=True).filter(length_q)
                )
            ).filter(_has_matching_length=True)

        # 9. Lace Type Filter
        lace_types = self._values(params, "lace_type")
        if lace_types:
            qs = qs.annotate(
                _has_matching_lace=Exists(
                    ProductVariant.objects.filter(
                        product_id=OuterRef("pk"), is_active=True, lace_type__in=lace_types
                    )
                )
            ).filter(_has_matching_lace=True)

        # 10. Density Filter
        densities = self._values(params, "density")
        if densities:
            qs = qs.annotate(
                _has_matching_density=Exists(
                    ProductVariant.objects.filter(
                        product_id=OuterRef("pk"), is_active=True, density__in=densities
                    )
                )
            ).filter(_has_matching_density=True)

        # 11. Price & In-Stock Variant Constraints
        variant_filter = {"product_id": OuterRef("pk"), "is_active": True}
        has_v_constraint = False
        if params.get("min_price"):
            variant_filter["price__gte"] = params["min_price"]
            has_v_constraint = True
        if params.get("max_price"):
            variant_filter["price__lte"] = params["max_price"]
            has_v_constraint = True
        if params.get("in_stock", "").lower() in ("true", "1", "yes"):
            variant_filter["stock_quantity__gt"] = 0
            has_v_constraint = True

        if has_v_constraint:
            qs = qs.annotate(
                _has_matching_stock_price=Exists(ProductVariant.objects.filter(**variant_filter))
            ).filter(_has_matching_stock_price=True)

        # 12. Ordering
        sort_param = params.get("ordering")
        if sort_param == "price_asc":
            qs = qs.order_by("price_order", "-created_at")
        elif sort_param == "price_desc":
            qs = qs.order_by("-price_order", "-created_at")
        elif sort_param in ("popularity", "-popularity"):
            qs = qs.order_by("-is_best_seller", "-created_at")
        elif sort_param in ("rating", "-rating"):
            qs = qs.annotate(avg_r=Avg("reviews__rating")).order_by("-avg_r", "-created_at")
        elif sort_param == "newest":
            qs = qs.order_by("-created_at")

        return qs.distinct()

    def get_serializer_class(self):
        return ProductDetailSerializer if self.action == "retrieve" else ProductListSerializer

    @action(detail=False, methods=["get"], url_path="filter-options")
    def filter_options(self, request):
        active_products = Product.objects.filter(is_published=True, category__is_active=True)
        active_variants = ProductVariant.objects.filter(product__in=active_products, is_active=True)

        colors = list(dict.fromkeys(
            active_variants.exclude(color="").values_list("color", flat=True).order_by("color")
        ))
        lengths = sorted(list(set(
            active_variants.filter(length_inches__isnull=False).values_list("length_inches", flat=True)
        )))
        hair_origins = list(dict.fromkeys(
            active_products.exclude(hair_origin="").values_list("hair_origin", flat=True).order_by("hair_origin")
        ))
        textures = list(dict.fromkeys(
            active_products.exclude(texture="").values_list("texture", flat=True).order_by("texture")
        ))
        densities = list(dict.fromkeys(
            active_variants.exclude(density="").values_list("density", flat=True).order_by("density")
        ))
        price_stats = active_variants.aggregate(min_p=Min("price"), max_p=Max("price"))

        return Response({
            "colors": colors,
            "lengths": lengths,
            "hair_origins": hair_origins,
            "hair_materials": ["human", "synthetic", "blend"],
            "textures": textures,
            "densities": densities,
            "price_range": {
                "min": price_stats["min_p"] or 0,
                "max": price_stats["max_p"] or 1500000
            }
        })

    @action(detail=True, methods=["post"], permission_classes=[AllowAny], url_path="reviews")
    def add_review(self, request, slug=None):
        product = self.get_object()
        data = request.data.copy()
        reviewer_name = data.get("reviewer_name")
        if not reviewer_name and request.user.is_authenticated:
            reviewer_name = request.user.get_full_name() or request.user.username
        if not reviewer_name:
            reviewer_name = "Verified Customer"

        rating = int(data.get("rating", 5))
        if rating < 1 or rating > 5:
            return Response({"rating": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            reviewer_name=reviewer_name,
            rating=rating,
            title=data.get("title", ""),
            comment=data.get("comment", ""),
            is_verified_purchase=True,
            is_approved=True
        )
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

