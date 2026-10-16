from django.core.management.base import BaseCommand

from catalog.models import Product
from catalog.taxonomy import CANONICAL_COLORS, CANONICAL_TEXTURES


class Command(BaseCommand):
    help = "Report catalog records with missing/conflicting controlled attributes or image mappings."

    def handle(self, *args, **options):
        issues = []
        # Storefront checks concern visible products. Unpublished records are
        # retained for editorial review and must not contaminate this report.
        for product in Product.objects.filter(is_published=True).select_related("category", "subcategory").prefetch_related("images", "variants"):
            product_issues = []
            if product.texture not in CANONICAL_TEXTURES:
                product_issues.append("missing or non-canonical texture")
            if not product.default_color:
                product_issues.append("missing default color")
            elif product.default_color not in CANONICAL_COLORS:
                product_issues.append("non-canonical default color")
            if not product.default_length_inches:
                product_issues.append("missing default length")
            if not product.images.exists():
                product_issues.append("missing product image")
            elif not product.images.filter(is_primary=True).exists():
                product_issues.append("no primary image")
            variants = product.variants.filter(is_active=True)
            if not variants.exists():
                product_issues.append("no active variants")
            elif product.texture and variants.exclude(texture__in=("", product.texture)).exists():
                product_issues.append("variant texture conflicts with product texture")
            if product_issues:
                issues.append((product, product_issues))

        if not issues:
            self.stdout.write(self.style.SUCCESS("Catalog audit passed: no metadata or image mapping issues found."))
            return
        for product, product_issues in issues:
            self.stdout.write(f"{product.id}\t{product.slug}\t{'; '.join(product_issues)}")
        self.stdout.write(self.style.WARNING(f"Catalog audit found {len(issues)} product(s) requiring review."))
