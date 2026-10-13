from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Exists, OuterRef, Min
from .models import Category, Product, ProductVariant, Review
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    lookup_field = "slug"

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "category__slug": ["exact"],
        "hair_type": ["exact"],
        "texture": ["icontains"],
        "default_length_inches": ["exact"],
        "default_color": ["icontains"],
        "default_lace_type": ["icontains"],
        "is_featured": ["exact"],
        "is_new_arrival": ["exact"],
        "is_best_seller": ["exact"]
    }
    search_fields = ["name", "description", "texture", "default_color", "default_lace_type", "category__name"]
    ordering_fields = ["created_at", "name", "price_order"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Product.objects.filter(is_published=True, category__is_active=True)\
            .select_related("category")\
            .prefetch_related("images", "variants", "reviews")\
            .annotate(price_order=Min("variants__price"))

        params = self.request.query_params
        variant_filters = {"product_id": OuterRef("pk"), "is_active": True}
        if params.get("min_price"):
            variant_filters["price__gte"] = params["min_price"]
        if params.get("max_price"):
            variant_filters["price__lte"] = params["max_price"]
        if params.get("length_inches"):
            variant_filters["length_inches"] = params["length_inches"]
        if params.get("in_stock", "").lower() in ("true", "1", "yes"):
            variant_filters["stock_quantity__gt"] = 0

        has_variant_filter = any(key in params for key in ("min_price", "max_price", "length_inches")) or \
                             params.get("in_stock", "").lower() in ("true", "1", "yes")
        if has_variant_filter:
            qs = qs.annotate(_matching_variant=Exists(ProductVariant.objects.filter(**variant_filters))).filter(_matching_variant=True)

        sort_param = params.get("ordering")
        if sort_param == "price_asc":
            qs = qs.order_by("price_order")
        elif sort_param == "price_desc":
            qs = qs.order_by("-price_order")

        return qs.distinct()

    def get_serializer_class(self):
        return ProductDetailSerializer if self.action == "retrieve" else ProductListSerializer

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
