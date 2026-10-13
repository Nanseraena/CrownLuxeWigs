from decimal import Decimal
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    parent = models.ForeignKey("self", related_name="subcategories", on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "category"
            slug, i = base, 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1; slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self): return self.name


class Collection(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "collection"
            slug, i = base, 1
            while Collection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1; slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self): return self.name


class Product(models.Model):
    HAIR_TYPES = [("human", "Human hair"), ("synthetic", "Synthetic"), ("blend", "Blend")]
    HAIR_ORIGIN_CHOICES = [
        ("brazilian", "Brazilian"),
        ("peruvian", "Peruvian"),
        ("malaysian", "Malaysian"),
        ("indian", "Indian"),
        ("vietnamese", "Vietnamese"),
        ("cambodian", "Cambodian"),
        ("other", "Other"),
        ("unspecified", "Unspecified"),
    ]

    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    sku = models.CharField(max_length=80, blank=True, db_index=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Category, related_name="subcategory_products", on_delete=models.SET_NULL, null=True, blank=True)
    collections = models.ManyToManyField(Collection, related_name="products", blank=True)
    description = models.TextField(blank=True)
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPES, default="human")
    hair_origin = models.CharField(max_length=40, choices=HAIR_ORIGIN_CHOICES, default="unspecified", db_index=True)
    texture = models.CharField(max_length=80, blank=True, db_index=True)
    default_length_inches = models.PositiveSmallIntegerField(null=True, blank=True)
    default_color = models.CharField(max_length=60, blank=True)
    default_lace_type = models.CharField(max_length=80, blank=True)
    is_published = models.BooleanField(default=False, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_new_arrival = models.BooleanField(default=False, db_index=True)
    is_best_seller = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_published", "category"]),
            models.Index(fields=["is_published", "hair_type"]),
            models.Index(fields=["is_published", "hair_origin"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "product"
            slug, i = base, 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1; slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def min_price(self):
        v = self.variants.filter(is_active=True).order_by("price").first()
        return v.price if v else None

    @property
    def compare_at_price(self):
        v = self.variants.filter(is_active=True).order_by("price").first()
        return v.compare_at_price if v and v.compare_at_price else None

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def average_rating(self):
        approved = self.reviews.filter(is_approved=True)
        if not approved.exists():
            return 5.0
        avg = approved.aggregate(models.Avg("rating"))["rating__avg"]
        return round(float(avg), 1) if avg else 5.0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    @property
    def available_colors(self):
        colors = []
        for c in self.variants.filter(is_active=True).values_list("color", flat=True):
            if c and c not in colors:
                colors.append(c)
        return colors

    @property
    def available_lengths(self):
        lengths = set()
        for l in self.variants.filter(is_active=True, length_inches__isnull=False).values_list("length_inches", flat=True):
            if l is not None:
                lengths.add(l)
        return sorted(list(lengths))

    @property
    def available_densities(self):
        densities = []
        for d in self.variants.filter(is_active=True).values_list("density", flat=True):
            if d and d not in densities:
                densities.append(d)
        return densities

    @property
    def available_lace_types(self):
        laces = []
        for l in self.variants.filter(is_active=True).values_list("lace_type", flat=True):
            if l and l not in laces:
                laces.append(l)
        return laces

    def __str__(self): return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    sku = models.CharField(max_length=80, unique=True)
    length_inches = models.PositiveSmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=60, blank=True)
    texture = models.CharField(max_length=80, blank=True)
    lace_type = models.CharField(max_length=80, blank=True)
    density = models.CharField(max_length=40, blank=True)
    cap_size = models.CharField(max_length=40, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[])
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product__name", "length_inches", "color"]
        indexes = [
            models.Index(fields=["product", "is_active"]),
            models.Index(fields=["stock_quantity"]),
            models.Index(fields=["product", "is_active", "color"]),
            models.Index(fields=["product", "is_active", "length_inches"]),
        ]

    @property
    def in_stock(self): return self.is_active and self.stock_quantity > 0
    def __str__(self): return f"{self.product.name} / {self.sku}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000)
    alt_text = models.CharField(max_length=240, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["sort_order", "id"]
    def __str__(self): return f"Image for {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", related_name="product_reviews", on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer_name} ({self.rating}*) on {self.product.name}"

