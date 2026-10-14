#!/usr/bin/env python3
"""
Convert, process, and map the photorealistic AI mannequin salon images
across all categories, collections, and products for CrownLuxe Wigs.
Replaces any programmatic line drawings with 100% photorealistic salon photography
featuring realistic mannequin heads on stands with HD lace frontals.
"""

import os
import json
from PIL import Image, ImageEnhance, ImageOps

BASE_DIR = "/home/ena/Desktop/Wig_Ecommerce"
OUTPUT_DIR = os.path.join(BASE_DIR, "frontend/public/images/wigs")
BRAIN_DIR = "/home/ena/.gemini/antigravity/brain/e8dcac74-8780-4485-9de0-70294ca19e8d"
USER_UPLOAD_DIR = os.path.join(BRAIN_DIR, ".user_uploaded")

# Base source images
IMG_HONEY_BOB = os.path.join(BRAIN_DIR, "luxury_honey_blonde_bob_wig_1791973304330.jpg")
IMG_DUMMY_OMBRE_BOB = os.path.join(USER_UPLOAD_DIR, "media_1791972949754_fc7c5ee5.png")
IMG_BURGUNDY_STRAIGHT = os.path.join(BRAIN_DIR, "wig_99j_burgundy_bone_straight_1791973605579.jpg")
IMG_613_BLONDE = os.path.join(BRAIN_DIR, "luxury_613_platinum_blonde_wig_1791973491858.jpg")
IMG_SPICED_GINGER = os.path.join(BRAIN_DIR, "spiced_ginger_loose_wave_wig_1791973485189.jpg")
IMG_WATER_WAVE = os.path.join(BRAIN_DIR, "water_wave_wig_product_1791973490684.jpg")
IMG_BUNDLES_CLOSURE = os.path.join(BRAIN_DIR, "luxury_hair_bundles_closure_1791973491168.jpg")
IMG_BONE_STRAIGHT = os.path.join(BRAIN_DIR, "bone_straight_wig_1791889362305.jpg")
IMG_DEEP_WAVE = os.path.join(BRAIN_DIR, "deep_wave_wig_1791889384619.jpg")
IMG_BLUNT_BOB = os.path.join(BRAIN_DIR, "blunt_bob_wig_1791889415025.jpg")
IMG_GLUELESS_WAVE = os.path.join(BRAIN_DIR, "glueless_wear_wig_1791889451080.jpg")
IMG_HD_LACE_WAVE = os.path.join(BRAIN_DIR, "hd_lace_wig_1791889489508.jpg")
IMG_RAW_HUMAN = os.path.join(BRAIN_DIR, "human_hair_wig_1791889191615.jpg")

def crop_and_resize(src_path, target_size=(900, 1100), crop_box=None):
    im = Image.open(src_path).convert("RGB")
    if crop_box:
        im = im.crop(crop_box)
    
    # Fit or resize while keeping aspect ratio
    src_w, src_h = im.size
    target_w, target_h = target_size
    
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Center crop to exact target dimensions
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    im = im.crop((left, top, left + target_w, top + target_h))
    return im

def adjust_color(im, hue_shift=0, sat_factor=1.0, contrast_factor=1.0, brightness_factor=1.0):
    """Subtly adjust color to produce realistic variations (e.g. chocolate brown, jet black)."""
    if sat_factor != 1.0:
        im = ImageEnhance.Color(im).enhance(sat_factor)
    if contrast_factor != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast_factor)
    if brightness_factor != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness_factor)
    return im

def save_webp(im, rel_path, quality=94):
    full_path = os.path.join(OUTPUT_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    im.save(full_path, "WEBP", quality=quality)
    print(f"  ✓ Saved realistic photo: {rel_path} ({im.size[0]}x{im.size[1]})")
    return full_path

# ─────────────────────────────────────────────────────────────
# 1. Product & Category Mappings to High-Res Salon Photos
# ─────────────────────────────────────────────────────────────

def process_all():
    print("Converting and saving realistic mannequin salon photography across catalog...\n")

    # ── CATEGORIES ──
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (900, 1100)), "categories/lace-front-wigs.webp")
    save_webp(crop_and_resize(IMG_WATER_WAVE, (900, 1100)), "categories/closure-wigs.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (900, 1100)), "categories/glueless-wigs.webp")
    save_webp(crop_and_resize(IMG_HONEY_BOB, (900, 1100)), "categories/bob-wigs.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "categories/curly-wavy-wigs.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "categories/straight-wigs.webp")
    save_webp(crop_and_resize(IMG_BURGUNDY_STRAIGHT, (900, 1100)), "categories/colored-wigs.webp")
    save_webp(crop_and_resize(IMG_SPICED_GINGER, (900, 1100)), "categories/specialty-wigs.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "categories/hair-extensions.webp")

    # ── COLLECTIONS ──
    save_webp(crop_and_resize(IMG_DUMMY_OMBRE_BOB, (1400, 800)), "collections/new-arrivals.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (1400, 800)), "collections/best-sellers.webp")
    save_webp(crop_and_resize(IMG_HONEY_BOB, (1400, 800)), "collections/trending-now.webp")
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (1400, 800)), "collections/premium-collection.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (1400, 800)), "collections/everyday-wigs.webp")
    save_webp(crop_and_resize(IMG_BLUNT_BOB, (1400, 800)), "collections/work-office-looks.webp")
    save_webp(crop_and_resize(IMG_613_BLONDE, (1400, 800)), "collections/wedding-occasion.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (1400, 800)), "collections/beginner-friendly.webp")
    save_webp(crop_and_resize(IMG_BLUNT_BOB, (1400, 800)), "collections/affordable-finds.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (1400, 800)), "collections/long-hair.webp")
    save_webp(crop_and_resize(IMG_HONEY_BOB, (1400, 800)), "collections/short-hair.webp")

    # ── HD LACE EXPERIENCE SHOWCASE ──
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (1600, 900)), "lace-experience/hd-lace-hero.webp")
    save_webp(crop_and_resize(IMG_DUMMY_OMBRE_BOB, (900, 1200)), "lace-experience/hd-lace-melt-portrait.webp")
    
    # Close-up macro crops of the melted lace hairline from high-res source
    src_hd = Image.open(IMG_HD_LACE_WAVE)
    w, h = src_hd.size
    lace_crop_1 = src_hd.crop((int(w * 0.25), int(h * 0.15), int(w * 0.75), int(h * 0.55)))
    save_webp(lace_crop_1.resize((1200, 800), Image.Resampling.LANCZOS), "lace-experience/lace-mesh-macro.webp")

    src_ginger = Image.open(IMG_SPICED_GINGER)
    w, h = src_ginger.size
    lace_crop_2 = src_ginger.crop((int(w * 0.25), int(h * 0.10), int(w * 0.75), int(h * 0.50)))
    save_webp(lace_crop_2.resize((1000, 800), Image.Resampling.LANCZOS), "lace-experience/lace-texture-closeup.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (1400, 900)), "lace-experience/pre-plucked-comparison.webp")

    # ── DETAILS ──
    save_webp(lace_crop_1.resize((1000, 800), Image.Resampling.LANCZOS), "details/hd-lace-hairline-detail.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (1000, 800)), "details/cap-construction.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (1000, 800)), "details/glueless-elastic-band-detail.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (1000, 800)), "details/hair-texture-bone-straight.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (1000, 800)), "details/hair-texture-deep-wave.webp")
    save_webp(crop_and_resize(IMG_WATER_WAVE, (1000, 800)), "details/hair-texture-kinky-curly.webp")

    # ── LACE FRONT WIGS ──
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "lace-front/13x4-bone-straight-black.webp")
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (900, 1100)), "lace-front/13x6-body-wave-black.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "lace-front/deep-wave-13x6-black.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (900, 1100)), "lace-front/pre-plucked-body-wave.webp")
    save_webp(crop_and_resize(IMG_RAW_HUMAN, (900, 1100)), "lace-front/kinky-straight-transparent.webp")
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (900, 1100)), "lace-front/loose-wave-lace-front.webp")

    # ── CLOSURE WIGS ──
    save_webp(crop_and_resize(IMG_WATER_WAVE, (900, 1100)), "closure/5x5-water-wave-black.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "closure/4x4-silky-straight-black.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "closure/2x6-bone-straight-black.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "closure/deep-wave-closure.webp")

    # ── GLUELESS WIGS ──
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (900, 1100)), "glueless/wear-and-go-body-wave.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "glueless/bye-bye-knots-straight.webp")
    save_webp(crop_and_resize(IMG_BLUNT_BOB, (900, 1100)), "glueless/30-second-throw-on-bob.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "glueless/glueless-curly-wear-go.webp")

    # ── BOB WIGS ──
    save_webp(crop_and_resize(IMG_BLUNT_BOB, (900, 1100)), "bob/blunt-cut-sleek-bob-black.webp")
    save_webp(crop_and_resize(IMG_HONEY_BOB, (900, 1100)), "bob/asymmetrical-bob-black.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "bob/deep-wave-curly-bob-bangs.webp")
    # Chocolate bob variation
    im_choc = adjust_color(crop_and_resize(IMG_BLUNT_BOB, (900, 1100)), sat_factor=1.2, brightness_factor=1.05)
    save_webp(im_choc, "bob/layered-chocolate-bob.webp")
    save_webp(crop_and_resize(IMG_DUMMY_OMBRE_BOB, (900, 1100)), "bob/wavy-bob-black.webp")
    save_webp(crop_and_resize(IMG_BURGUNDY_STRAIGHT, (900, 1100)), "bob/burgundy-bob-bangs.webp")

    # ── CURLY & WAVY WIGS ──
    save_webp(crop_and_resize(IMG_WATER_WAVE, (900, 1100)), "curly-wavy/water-wave-long.webp")
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (900, 1100)), "curly-wavy/loose-wave-mermaid.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "curly-wavy/kinky-curly-natural.webp")
    save_webp(crop_and_resize(IMG_WATER_WAVE, (900, 1100)), "curly-wavy/raw-cambodian-deep-curly.webp")
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (900, 1100)), "curly-wavy/body-wave-long.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "curly-wavy/deep-wave-natural-black.webp")

    # ── STRAIGHT WIGS ──
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "straight/bone-straight-glass-finish.webp")
    save_webp(crop_and_resize(IMG_RAW_HUMAN, (900, 1100)), "straight/yaki-straight-blowout.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "straight/silky-straight-burmese.webp")
    save_webp(crop_and_resize(IMG_RAW_HUMAN, (900, 1100)), "straight/kinky-straight-black.webp")

    # ── COLORED WIGS ──
    save_webp(crop_and_resize(IMG_HONEY_BOB, (900, 1100)), "colored/piano-honey-blonde-balayage.webp")
    save_webp(crop_and_resize(IMG_SPICED_GINGER, (900, 1100)), "colored/ginger-copper-loose-wave.webp")
    save_webp(crop_and_resize(IMG_BURGUNDY_STRAIGHT, (900, 1100)), "colored/burgundy-99j-bone-straight.webp")
    save_webp(crop_and_resize(IMG_613_BLONDE, (900, 1100)), "colored/613-platinum-blonde.webp")
    save_webp(crop_and_resize(IMG_DUMMY_OMBRE_BOB, (900, 1100)), "colored/ombre-caramel-honey.webp")
    save_webp(im_choc, "colored/chocolate-brown-silky.webp")
    save_webp(crop_and_resize(IMG_HONEY_BOB, (900, 1100)), "colored/honey-blonde-wave.webp")
    save_webp(crop_and_resize(IMG_SPICED_GINGER, (900, 1100)), "colored/copper-red-wave.webp")

    # ── SPECIALTY WIGS ──
    save_webp(crop_and_resize(IMG_GLUELESS_WAVE, (900, 1100)), "specialty/360-full-lace-body-wave.webp")
    save_webp(crop_and_resize(IMG_DEEP_WAVE, (900, 1100)), "specialty/headband-deep-wave.webp")
    save_webp(crop_and_resize(IMG_BLUNT_BOB, (900, 1100)), "specialty/pixie-cut-jet-black.webp")
    save_webp(crop_and_resize(IMG_BONE_STRAIGHT, (900, 1100)), "specialty/french-bangs-bone-straight.webp")
    save_webp(crop_and_resize(IMG_HD_LACE_WAVE, (900, 1100)), "specialty/full-lace-wig-faceless-mannequin.webp")

    # ── HAIR EXTENSIONS ──
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/bundles-body-wave-closure.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/bundles-bone-straight.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/clip-in-straight.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/tape-in-extensions.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/curly-extensions.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/closure-piece-hd.webp")
    save_webp(crop_and_resize(IMG_BUNDLES_CLOSURE, (900, 1100)), "extensions/frontal-piece-hd-lace.webp")

    print("\nAll photorealistic dummy mannequin images successfully generated and deployed!")

if __name__ == "__main__":
    process_all()
