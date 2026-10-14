#!/usr/bin/env python3
"""
Update seed_catalog.py with the full 34 unique primary + gallery images mapping.
"""
import re

SEED_FILE = "/home/ena/Desktop/Wig_Ecommerce/backend/catalog/management/commands/seed_catalog.py"

PRODUCT_GALLERY_MAP = {
    "crownluxe-13x4-hd-bone-straight-frontal-wig": [
        "/images/wigs/lace-front/13x4-bone-straight-black.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "luxe-deep-wave-13x6-melted-frontal-wig": [
        "/images/wigs/lace-front/deep-wave-13x6-black.webp",
        "/images/wigs/details/hair-texture-deep-wave.webp"
    ],
    "crownluxe-pre-plucked-body-wave-invisible-swiss-lace-frontal": [
        "/images/wigs/lace-front/pre-plucked-body-wave.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-transparent-13x4-kinky-straight-frontal-wig": [
        "/images/wigs/lace-front/kinky-straight-transparent.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-5x5-hd-closure-water-wave-wig": [
        "/images/wigs/closure/5x5-water-wave-black.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-4x4-pre-cut-glueless-silky-straight-closure-wig": [
        "/images/wigs/closure/4x4-silky-straight-black.webp",
        "/images/wigs/details/cap-construction.webp"
    ],
    "crownluxe-2x6-deep-middle-part-closure-wig": [
        "/images/wigs/closure/2x6-bone-straight-black.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-3d-dome-cap-wear-go-body-wave-wig": [
        "/images/wigs/glueless/wear-and-go-body-wave.webp",
        "/images/wigs/details/cap-construction.webp"
    ],
    "crownluxe-bye-bye-knots-glueless-straight-wig": [
        "/images/wigs/glueless/bye-bye-knots-straight.webp",
        "/images/wigs/details/glueless-elastic-band-detail.webp"
    ],
    "crownluxe-beginner-friendly-30-second-throw-on-bob": [
        "/images/wigs/glueless/30-second-throw-on-bob.webp",
        "/images/wigs/details/cap-construction.webp"
    ],
    "crownluxe-10-precision-blunt-cut-sleek-bob": [
        "/images/wigs/bob/blunt-cut-sleek-bob-black.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-12-asymmetrical-chic-bone-straight-bob": [
        "/images/wigs/bob/asymmetrical-bob-black.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-14-deep-wave-curly-bob-with-fringe-bangs": [
        "/images/wigs/bob/deep-wave-curly-bob-bangs.webp",
        "/images/wigs/details/hair-texture-deep-wave.webp"
    ],
    "crownluxe-10-layered-side-part-bob-in-chocolate-brown": [
        "/images/wigs/bob/layered-chocolate-bob.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-28-water-wave-high-definition-curls": [
        "/images/wigs/curly-wavy/water-wave-long.webp",
        "/images/wigs/details/hair-texture-deep-wave.webp"
    ],
    "crownluxe-24-loose-wave-mermaid-luster-wig": [
        "/images/wigs/curly-wavy/loose-wave-mermaid.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-22-kinky-curly-4c-scalp-blended-natural-wig": [
        "/images/wigs/curly-wavy/kinky-curly-natural.webp",
        "/images/wigs/details/hair-texture-kinky-curly.webp"
    ],
    "crownluxe-26-raw-cambodian-deep-curly-wig": [
        "/images/wigs/curly-wavy/raw-cambodian-deep-curly.webp",
        "/images/wigs/details/hair-texture-deep-wave.webp"
    ],
    "crownluxe-30-glass-finish-bone-straight-virgin-wig": [
        "/images/wigs/straight/bone-straight-glass-finish.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-28-yaki-straight-textured-blowout-wig": [
        "/images/wigs/straight/yaki-straight-blowout.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-24-silky-straight-raw-burmese-donor-wig": [
        "/images/wigs/straight/silky-straight-burmese.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-p4-27-piano-honey-blonde-balayage-wig": [
        "/images/wigs/colored/piano-honey-blonde-balayage.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-350-spiced-ginger-copper-loose-wave-wig": [
        "/images/wigs/colored/ginger-copper-loose-wave.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-99j-deep-wine-burgundy-bone-straight-wig": [
        "/images/wigs/colored/burgundy-99j-bone-straight.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-613-russian-virgin-platinum-ice-blonde-wig": [
        "/images/wigs/colored/613-platinum-blonde.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-ombre-warm-caramel-to-honey-blonde-wave-wig": [
        "/images/wigs/colored/ombre-caramel-honey.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
    "crownluxe-rich-chocolate-brown-4-silky-straight-wig": [
        "/images/wigs/colored/chocolate-brown-silky.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-360-full-lace-high-ponytail-body-wave-wig": [
        "/images/wigs/specialty/360-full-lace-body-wave.webp",
        "/images/wigs/details/cap-construction.webp"
    ],
    "crownluxe-headband-slip-on-deep-wave-travel-wig": [
        "/images/wigs/specialty/headband-deep-wave.webp",
        "/images/wigs/details/hair-texture-deep-wave.webp"
    ],
    "crownluxe-pixie-cut-short-tapered-textured-wig": [
        "/images/wigs/specialty/pixie-cut-jet-black.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-french-bangs-silky-bone-straight-wig": [
        "/images/wigs/specialty/french-bangs-bone-straight.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-raw-virgin-hair-bundles-3pack-5x5-hd-closure": [
        "/images/wigs/extensions/bundles-body-wave-closure.webp",
        "/images/wigs/extensions/closure-piece-hd.webp"
    ],
    "crownluxe-raw-cuticle-aligned-bone-straight-bundles-3pack": [
        "/images/wigs/extensions/bundles-bone-straight.webp",
        "/images/wigs/details/hair-texture-bone-straight.webp"
    ],
    "crownluxe-13x4-ear-to-ear-hd-frontal-piece-solo": [
        "/images/wigs/extensions/frontal-piece-hd-lace.webp",
        "/images/wigs/details/hd-lace-hairline-detail.webp"
    ],
}

with open(SEED_FILE, "r") as f:
    content = f.read()

count = 0
for slug, images_list in PRODUCT_GALLERY_MAP.items():
    formatted_images = '[\n                    ' + ',\n                    '.join(f'"{img}"' for img in images_list) + '\n                ]'
    slug_pat = rf'("slug": "{re.escape(slug)}")'
    m = re.search(slug_pat, content)
    if not m:
        print(f"Warning: slug {slug} not found")
        continue

    start_pos = m.end()
    # Find the images array after this slug
    img_match = re.search(r'"images":\s*\[[^\]]*\]', content[start_pos:start_pos + 1200])
    if not img_match:
        print(f"Warning: images not found for {slug}")
        continue

    old_span = img_match.span()
    abs_start = start_pos + old_span[0]
    abs_end = start_pos + old_span[1]

    content = content[:abs_start] + f'"images": {formatted_images}' + content[abs_end:]
    count += 1
    print(f"  ✓ {slug}")

with open(SEED_FILE, "w") as f:
    f.write(content)

print(f"\nSuccessfully updated {count} products in {SEED_FILE}")
