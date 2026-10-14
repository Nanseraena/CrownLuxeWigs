# CrownLuxe image audit — 2026-10-14

Pinterest reference pages were inaccessible from this environment, so this
audit used direct visual inspection of all 81 WebP assets and the required
product-construction criteria.

## Outcome

| Measure | Count |
| --- | ---: |
| Images inspected | 81 |
| Approved active product/gallery assets | 19 across 14 products |
| Archived from public assets | 18 |
| Products withheld pending a truthful replacement | 20 |
| Human-faced display images left in active catalog | 0 |
| Incorrect active extension images | 0 |
| Incorrect active bob images | 0 |

## Archived — `REMOVE_FROM_CATALOG`

These files were visually inspected and moved to
`archive/rejected-wig-images/`. They show a human-faced display head/model or
are used as a face-based marketing visual:

```text
bob/asymmetrical-bob-black.webp
bob/burgundy-bob-bangs.webp
bob/wavy-bob-black.webp
categories/bob-wigs.webp
categories/closure-wigs.webp
categories/specialty-wigs.webp
closure/5x5-water-wave-black.webp
colored/copper-red-wave.webp
colored/ginger-copper-loose-wave.webp
colored/ombre-caramel-honey.webp
collections/new-arrivals.webp
collections/short-hair.webp
collections/trending-now.webp
curly-wavy/raw-cambodian-deep-curly.webp
curly-wavy/water-wave-long.webp
details/hair-texture-kinky-curly.webp
lace-experience/hd-lace-melt-portrait.webp
lace-experience/lace-texture-closeup.webp
```

## Product audit and mapping

`KEEP` products have a visually appropriate faceless primary image and are
published by `seed_catalog`. `REGENERATE` products are retained with their
identifier, price, variants, and stock, but are unpublished until a compliant
asset is available.

| Status | Products / findings |
| --- | --- |
| KEEP | 13x4 bone straight frontal; 13x6 deep-wave frontal; pre-plucked body-wave frontal; 4x4 straight closure; 2x6 middle-part closure; wear-and-go body-wave; 30-second blunt bob; precision blunt bob; loose-wave wig; glass bone-straight wig; 99J burgundy wig; 613 blonde wig; 360 body-wave wig; body-wave bundles + 5x5 closure. |
| REGENERATE — Bob | Asymmetrical bob (human-faced head); deep-wave curly bob with bangs (long silhouette); layered chocolate bob (straight dark blunt silhouette). Required: faceless asymmetrical, short curly-fringe, and short layered chocolate assets. |
| REGENERATE — Extensions | Bone-straight bundle pack currently includes a closure; solo 13x4 frontal is a bundle-and-closure flat lay. Required: isolated wefts and an ear-to-ear frontal. Clip-in/tape-in/curly-extension files also depict the same bundles-and-closure flat lay and are not mapped to any active product. |
| REGENERATE — construction/texture | 5x5 water-wave closure is human-faced; the straight glueless, headband, pixie, French-bang, yaki, silky-straight, water-wave, kinky-curly, deep-curly, piano-highlight, ginger, ombré, and chocolate products do not have a truthful matching image. |

## Category and collection repairs

- Bob category now uses the faceless blunt-bob asset.
- Closure category now uses the faceless 4x4 closure asset.
- Specialty category now uses the faceless 360 body-wave asset.
- New Arrivals, Short Hair, and Trending collection tiles were remapped to
  compliant faceless assets.
- The HD-lace slideshow no longer includes the two human-faced images.

## Replacement prompts

Use the shared CrownLuxe studio direction: photorealistic product photography,
warm ivory background, faceless beige canvas mannequin or flat lay, visible
hair construction, no human face/model/text/watermark.

- Extensions: `isolated 13x4 HD lace frontal hairpiece, ear-to-ear lace and
  pre-plucked hairline visible, natural-black body-wave hair, flat lay`.
- Extensions: `three natural-black bone-straight sewn weft bundles only; no
  closure, clips, mannequin or wig cap; bundle tops and lengths visible`.
- Bob: `short asymmetrical natural-black bone-straight bob on faceless beige
  canvas mannequin, shorter back and one longer front section fully visible`.
- Bob: `short rounded deep-curly bob with fringe bangs on faceless canvas
  mannequin, ends at jawline, not long hair`.
- Bob: `10-inch chocolate-brown layered side-part bob on faceless canvas
  mannequin, clear layers and short cut line`.

No replacement images were generated in this audit because a photorealistic
image-generation tool is unavailable in the current session. The catalog does
not substitute mismatched images while those assets are missing.
