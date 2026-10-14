#!/usr/bin/env python3
"""
Patch seed_catalog.py: replace "images" list per product with the correct webp image path.
"""
import re

SEED_FILE = "/home/ena/Desktop/Wig_Ecommerce/backend/catalog/management/commands/seed_catalog.py"

# Mapping: product slug -> new image path
PRODUCT_IMAGE_MAP = {
    "crownluxe-13x4-hd-bone-straight-frontal-wig":           ["/images/wigs/lace-front/13x4-bone-straight-black.webp"],
    "luxe-deep-wave-13x6-melted-frontal-wig":                ["/images/wigs/lace-front/deep-wave-13x6-black.webp"],
    "crownluxe-pre-plucked-body-wave-invisible-swiss-lace-frontal": ["/images/wigs/lace-front/pre-plucked-body-wave.webp"],
    "crownluxe-transparent-13x4-kinky-straight-frontal-wig": ["/images/wigs/lace-front/kinky-straight-transparent.webp"],
    "crownluxe-5x5-hd-closure-water-wave-wig":               ["/images/wigs/closure/5x5-water-wave-black.webp"],
    "crownluxe-4x4-pre-cut-glueless-silky-straight-closure-wig": ["/images/wigs/closure/4x4-silky-straight-black.webp"],
    "crownluxe-2x6-deep-middle-part-closure-wig":            ["/images/wigs/closure/2x6-bone-straight-black.webp"],
    "crownluxe-3d-dome-cap-wear-go-body-wave-wig":           ["/images/wigs/glueless/wear-and-go-body-wave.webp"],
    "crownluxe-bye-bye-knots-glueless-straight-wig":         ["/images/wigs/glueless/bye-bye-knots-straight.webp"],
    "crownluxe-beginner-friendly-30-second-throw-on-bob":    ["/images/wigs/bob/blunt-cut-sleek-bob-black.webp"],
    "crownluxe-10-precision-blunt-cut-sleek-bob":            ["/images/wigs/bob/blunt-cut-sleek-bob-black.webp"],
    "crownluxe-12-asymmetrical-chic-bone-straight-bob":      ["/images/wigs/bob/asymmetrical-bob-black.webp"],
    "crownluxe-14-deep-wave-curly-bob-with-fringe-bangs":    ["/images/wigs/bob/deep-wave-curly-bob-bangs.webp"],
    "crownluxe-10-layered-side-part-bob-in-chocolate-brown": ["/images/wigs/bob/layered-chocolate-bob.webp"],
    "crownluxe-28-water-wave-high-definition-curls":         ["/images/wigs/curly-wavy/water-wave-long.webp"],
    "crownluxe-24-loose-wave-mermaid-luster-wig":            ["/images/wigs/curly-wavy/deep-wave-natural-black.webp"],
    "crownluxe-22-kinky-curly-4c-scalp-blended-natural-wig": ["/images/wigs/curly-wavy/kinky-curly-natural.webp"],
    "crownluxe-26-raw-cambodian-deep-curly-wig":             ["/images/wigs/curly-wavy/body-wave-long.webp"],
    "crownluxe-30-glass-finish-bone-straight-virgin-wig":    ["/images/wigs/straight/bone-straight-glass-finish.webp"],
    "crownluxe-28-yaki-straight-textured-blowout-wig":       ["/images/wigs/straight/kinky-straight-black.webp"],
    "crownluxe-24-silky-straight-raw-burmese-donor-wig":     ["/images/wigs/straight/silky-straight-burmese.webp"],
    "crownluxe-p4-27-piano-honey-blonde-balayage-wig":       ["/images/wigs/colored/honey-blonde-wave.webp"],
    "crownluxe-350-spiced-ginger-copper-loose-wave-wig":     ["/images/wigs/colored/ginger-copper-loose-wave.webp"],
    "crownluxe-99j-deep-wine-burgundy-bone-straight-wig":    ["/images/wigs/colored/burgundy-99j-bone-straight.webp"],
    "crownluxe-613-russian-virgin-platinum-ice-blonde-wig":  ["/images/wigs/colored/613-platinum-blonde.webp"],
    "crownluxe-ombre-warm-caramel-to-honey-blonde-wave-wig": ["/images/wigs/colored/honey-blonde-wave.webp"],
    "crownluxe-rich-chocolate-brown-4-silky-straight-wig":   ["/images/wigs/colored/chocolate-brown-silky.webp"],
    "crownluxe-360-full-lace-high-ponytail-body-wave-wig":   ["/images/wigs/specialty/360-full-lace-body-wave.webp"],
    "crownluxe-headband-slip-on-deep-wave-travel-wig":       ["/images/wigs/specialty/headband-deep-wave.webp"],
    "crownluxe-pixie-cut-short-tapered-textured-wig":        ["/images/wigs/specialty/pixie-cut-jet-black.webp"],
    "crownluxe-french-bangs-silky-bone-straight-wig":        ["/images/wigs/specialty/french-bangs-bone-straight.webp"],
    "crownluxe-raw-virgin-hair-bundles-3pack-5x5-hd-closure": ["/images/wigs/extensions/bundles-body-wave-closure.webp"],
    "crownluxe-raw-cuticle-aligned-bone-straight-bundles-3pack": ["/images/wigs/extensions/bundles-bone-straight.webp"],
    "crownluxe-13x4-ear-to-ear-hd-frontal-piece-solo":      ["/images/wigs/lace-front/13x6-body-wave-black.webp"],
}

with open(SEED_FILE, "r") as f:
    content = f.read()

# Process each product slug and update its "images" list
for slug, new_images in PRODUCT_IMAGE_MAP.items():
    images_str = str(new_images).replace("'", '"')
    # Pattern: match the slug line, then find the "images": [...] nearby
    # We'll do a two-step approach: find slug, then replace the next "images": line
    slug_pattern = rf'("slug": "{re.escape(slug)}")'
    slug_match = re.search(slug_pattern, content)
    if not slug_match:
        print(f"  ⚠ Slug not found: {slug}")
        continue

    # Find "images": [...] after this slug (within next 200 chars)
    search_start = slug_match.end()
    search_end = search_start + 1200
    segment = content[search_start:search_end]
    img_match = re.search(r'"images":\s*\[[^\]]*\]', segment)
    if not img_match:
        print(f"  ⚠ No images found for: {slug}")
        continue

    old_img_str = img_match.group()
    new_img_str = f'"images": {images_str}'
    content = content[:search_start] + segment.replace(old_img_str, new_img_str, 1) + content[search_start + len(segment):]
    print(f"  ✓ {slug}")

with open(SEED_FILE, "w") as f:
    f.write(content)

print(f"\nDone! Patched {len(PRODUCT_IMAGE_MAP)} product image references in {SEED_FILE}")
