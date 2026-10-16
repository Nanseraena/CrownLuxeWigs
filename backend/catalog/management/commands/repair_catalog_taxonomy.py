from django.core.management.base import BaseCommand

from catalog.models import Product


def controlled_values(product):
    """Classify only facts declared by the product's category hierarchy."""
    category = product.category.slug
    subcategory = product.subcategory.slug if product.subcategory else ""
    name = product.name.lower()
    values = {"product_type": "wig", "style": "standard", "construction": "lace_front"}
    if category == "hair-extensions":
        values.update(product_type="frontal_piece" if subcategory == "frontal-pieces" else "bundles")
        values["construction"] = "lace_front" if subcategory == "frontal-pieces" else "weft"
    elif category == "closure-wigs":
        values["construction"] = "closure"
    elif category == "glueless-wigs":
        values["construction"] = "glueless"
    elif category == "specialty-wigs":
        values["construction"] = "full_lace" if ("360" in name or "full lace" in name) else "headband" if "headband" in name else "glueless"

    if category == "bob-wigs" or " bob" in name:
        values["style"] = "bob"
    elif "pixie" in name:
        values["style"] = "pixie"
    elif "bang" in name or "fringe" in name:
        values["style"] = "bangs"
    elif "asymmetrical" in name:
        values["style"] = "asymmetrical"
    elif "layered" in name:
        values["style"] = "layered"
    elif product.default_length_inches and product.default_length_inches >= 20 and values["product_type"] == "wig":
        values["style"] = "long"
    return values


class Command(BaseCommand):
    help = "Report or repair controlled catalog taxonomy fields; use --apply to save changes."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Persist the reported corrections.")

    def handle(self, *args, **options):
        candidates = []
        for product in Product.objects.select_related("category", "subcategory"):
            values = controlled_values(product)
            changes = {field: value for field, value in values.items() if getattr(product, field) != value}
            if changes:
                candidates.append((product, changes))
        for product, changes in candidates:
            self.stdout.write(f"{product.id}\t{product.slug}\t{changes}")
            if options["apply"]:
                for field, value in changes.items():
                    setattr(product, field, value)
                product.save(update_fields=[*changes, "updated_at"])
        action = "updated" if options["apply"] else "found"
        self.stdout.write(self.style.SUCCESS(f"{action.capitalize()} {len(candidates)} catalog taxonomy record(s)."))
