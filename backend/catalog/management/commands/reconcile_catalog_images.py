from django.core.management.base import BaseCommand

from catalog.management.commands.seed_catalog import APPROVED_GALLERY_BY_SLUG
from catalog.models import Product


class Command(BaseCommand):
    help = "Report or unpublish catalog entries without an approved product-specific primary image."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Unpublish records reported by this audit.")

    def handle(self, *args, **options):
        review = []
        for product in Product.objects.filter(is_published=True).prefetch_related("images"):
            approved = APPROVED_GALLERY_BY_SLUG.get(product.slug)
            primary = product.primary_image
            if not approved or not primary or primary.image_url != approved[0]:
                review.append(product)
                self.stdout.write(f"{product.id}\t{product.slug}\tneeds approved primary image")

        if options["apply"]:
            Product.objects.filter(pk__in=[product.pk for product in review]).update(is_published=False)
            action = "Unpublished"
        else:
            action = "Found"
        self.stdout.write(self.style.WARNING(f"{action} {len(review)} product(s) requiring image review."))
