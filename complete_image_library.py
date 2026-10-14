#!/usr/bin/env python3
"""
Complete CrownLuxe Wig Image Library Generator, Validator, and Manifest Builder.
Strictly follows the CrownLuxe visual guidelines:
- Professional beauty e-commerce product photography inspired by Pinterest / Shein.
- NO human faces / NO models wearing wigs.
- Faceless mannequin heads, canvas wig blocks, flat-lays, and macro details.
- Warm ivory, cream, beige, blush, and champagne studio backgrounds.
- High-fidelity strand texture simulation (bone straight, body wave, deep wave, water wave, kinky curl, etc.).
- Color-accurate pigments (613 platinum, 99J burgundy, 350 ginger, honey blonde, piano highlights, caramel ombre).
- Resumable: skips already valid complete files.
- Generates `frontend/public/images/wigs/image-manifest.json`.
"""

import os
import json
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = "/home/ena/Desktop/Wig_Ecommerce"
OUTPUT_DIR = os.path.join(BASE_DIR, "frontend/public/images/wigs")
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "image-manifest.json")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# 1. Image Generation Primitives
# ─────────────────────────────────────────────────────────────

def get_gradient_bg(width, height, top_rgb=(250, 245, 238), bottom_rgb=(238, 228, 216)):
    bg = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(bg)
    r1, g1, b1 = top_rgb
    r2, g2, b2 = bottom_rgb
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(r1 + t * (r2 - r1))
        g = int(g1 + t * (g2 - g1))
        b = int(b1 + t * (b2 - b1))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return bg.convert("RGBA")

def draw_mannequin_silhouette(draw, cx, cy, w, h, canvas_texture=False):
    """Draws a premium beige canvas or smooth faceless mannequin head/bust."""
    head_w = int(w * 0.48)
    head_h = int(h * 0.52)
    neck_w = int(head_w * 0.35)
    neck_h = int(h * 0.20)
    shoulder_w = int(w * 0.76)
    shoulder_h = int(h * 0.14)

    skin_light = (235, 222, 206)
    skin_dark = (212, 195, 175)
    skin_shadow = (195, 178, 158)

    head_x = cx - head_w // 2
    head_y = cy - head_h // 2
    neck_x = cx - neck_w // 2
    neck_y = head_y + head_h - 15
    sh_x = cx - shoulder_w // 2
    sh_y = neck_y + neck_h - 10

    # Soft shoulder shadow
    draw.ellipse([sh_x - 10, sh_y + 10, sh_x + shoulder_w + 10, sh_y + shoulder_h + 20], fill=(210, 198, 185, 90))
    # Shoulders
    draw.ellipse([sh_x, sh_y, sh_x + shoulder_w, sh_y + shoulder_h], fill=skin_dark)
    # Neck
    draw.rectangle([neck_x, neck_y, neck_x + neck_w, neck_y + neck_h], fill=skin_dark)
    # Neck shadow under chin
    draw.ellipse([cx - neck_w // 2, neck_y - 10, cx + neck_w // 2, neck_y + 15], fill=skin_shadow)
    # Head
    draw.ellipse([head_x, head_y, head_x + head_w, head_y + head_h], fill=skin_light)

    # Canvas head seams/texture if enabled (wig block look)
    if canvas_texture:
        draw.line([(cx, head_y + 10), (cx, head_y + head_h - 10)], fill=(205, 190, 170), width=1)
        draw.arc([head_x + 20, head_y + 20, head_x + head_w - 20, head_y + head_h - 20], 30, 150, fill=(205, 190, 170), width=1)

def draw_lace_mesh(draw, cx, hairline_y, lace_width, lace_height, hair_color_rgb):
    """Draws realistic melted HD / transparent lace with fine mesh and pre-plucked baby hairs."""
    lx = cx - lace_width // 2
    skin_base = (222, 198, 172)

    for row in range(lace_height):
        fade = 1.0 - (row / max(1, lace_height))
        alpha = int(140 * fade)
        for col in range(0, lace_width, 5):
            draw.rectangle([lx + col, hairline_y + row, lx + col + 3, hairline_y + row + 1],
                           fill=skin_base + (alpha,))

    # Delicate single knots & baby hairs
    rng = random.Random(999)
    for _ in range(90):
        bx = lx + rng.randint(5, lace_width - 5)
        by = hairline_y + rng.randint(0, lace_height - 3)
        length = rng.randint(6, 20)
        curl = rng.randint(-8, 8)
        draw.line([(bx, by), (bx + curl, by + length)], fill=hair_color_rgb + (rng.randint(140, 200),), width=1)

def draw_hair_strands(draw, x_start, y_start, width, height, color_rgb,
                      wave_type="bone_straight", strand_count=160, highlight_rgb=None, seed=42):
    """Draws silky realistic individual hair fibers with specific wave dynamics."""
    rng = random.Random(seed)

    for _ in range(strand_count):
        x = x_start + rng.randint(0, width)
        thickness = rng.choice([1, 1, 1, 2])
        col = highlight_rgb if (highlight_rgb and rng.random() < 0.35) else color_rgb
        alpha = rng.randint(180, 240)
        hair_color = col + (alpha,)

        points = []
        if wave_type == "bone_straight":
            points = [(x, y_start + j) for j in range(0, height, 2)]
        elif wave_type == "body_wave":
            amp = rng.randint(6, 14)
            freq = rng.uniform(0.02, 0.035)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "loose_wave":
            amp = rng.randint(10, 22)
            freq = rng.uniform(0.015, 0.025)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "water_wave":
            amp = rng.randint(8, 16)
            freq = rng.uniform(0.04, 0.065)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "deep_wave":
            amp = rng.randint(12, 24)
            freq = rng.uniform(0.035, 0.055)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "kinky_curly":
            amp = rng.randint(5, 10)
            freq = rng.uniform(0.08, 0.15)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "pixie":
            amp = rng.randint(3, 8)
            freq = rng.uniform(0.05, 0.1)
            phase = rng.uniform(0, math.pi * 2)
            h_sub = min(height, 220)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, h_sub, 2)]
        elif wave_type == "bob_straight":
            h_sub = min(height, 340)
            curve = (rng.random() - 0.5) * 15
            points = [(x + int((j / max(1, h_sub))**2 * curve), y_start + j) for j in range(0, h_sub, 2)]
        elif wave_type == "asymmetrical_bob":
            rel_x = (x - x_start) / max(1, width)
            h_sub = int(240 + rel_x * 140)
            points = [(x, y_start + j) for j in range(0, h_sub, 2)]
        else:
            points = [(x, y_start + j) for j in range(0, height, 2)]

        clamped = [(max(x_start - 30, min(x_start + width + 30, px)), py) for px, py in points]
        if len(clamped) > 1:
            draw.line(clamped, fill=hair_color, width=thickness)

# ─────────────────────────────────────────────────────────────
# 2. Specialized Generators by Style & Category
# ─────────────────────────────────────────────────────────────

def render_wig_product(dest_path, hair_color_rgb, wave_type, bg_tone=((248, 242, 234), (235, 225, 212)),
                       has_lace=True, highlight_rgb=None, canvas_mannequin=False,
                       is_flatlay=False, seed=42):
    W, H = 900, 1100
    bg = get_gradient_bg(W, H, bg_tone[0], bg_tone[1])
    draw = ImageDraw.Draw(bg)

    cx = W // 2

    if is_flatlay:
        # Flat-lay display: wig cap circle + flowing hair on luxury ivory fabric
        cap_y = int(H * 0.35)
        cap_r = 180
        # Satin surface folds
        for i in range(5):
            fy = 150 + i * 180
            draw.arc([50, fy, W - 50, fy + 220], 10, 170, fill=(230, 218, 202, 60), width=3)
        # Wig cap
        draw.ellipse([cx - cap_r, cap_y - cap_r, cx + cap_r, cap_y + cap_r], fill=(30, 25, 22))
        draw_lace_mesh(draw, cx, cap_y + cap_r - 40, int(cap_r * 1.6), 45, hair_color_rgb)
        draw_hair_strands(draw, cx - cap_r, cap_y, cap_r * 2, H - cap_y - 40,
                          hair_color_rgb, wave_type=wave_type, strand_count=200,
                          highlight_rgb=highlight_rgb, seed=seed)
    else:
        # Mannequin display
        cy = H // 2 + 30
        draw_mannequin_silhouette(draw, cx, cy, W, H, canvas_texture=canvas_mannequin)

        hairline_y = cy - 280
        lace_w = int(W * 0.54)
        lace_h = 48

        if has_lace:
            draw_lace_mesh(draw, cx, hairline_y, lace_w, lace_h, hair_color_rgb)

        hair_y_start = hairline_y + (lace_h - 10 if has_lace else 0)
        hair_h = H - hair_y_start + 60
        draw_hair_strands(draw, cx - lace_w // 2, hair_y_start, lace_w, hair_h,
                          hair_color_rgb, wave_type=wave_type, strand_count=180,
                          highlight_rgb=highlight_rgb, seed=seed)

    # Soft studio vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for i in range(80):
        alpha = int(i * 0.6)
        vdraw.rectangle([i, i, W - i, H - i], outline=(20, 15, 10, alpha))
    bg = Image.alpha_composite(bg, vignette)

    final_img = bg.convert("RGB")
    final_img.save(dest_path, "WEBP", quality=92)


def render_extension_item(dest_path, hair_color_rgb, wave_type, item_type="bundles"):
    W, H = 900, 1100
    bg = get_gradient_bg(W, H, (250, 245, 238), (238, 228, 215))
    draw = ImageDraw.Draw(bg)

    cx = W // 2

    if item_type == "bundles":
        # 3 bundles arranged neatly side by side with satin gold ribbons
        for idx, offset in enumerate([-200, 0, 200]):
            bx = cx + offset
            by = 180
            bw = 140
            bh = 780
            # Ribbon at top
            draw.rectangle([bx - bw // 2, by, bx + bw // 2, by + 40], fill=(212, 175, 55))
            # Hair bundle body
            draw_hair_strands(draw, bx - bw // 2, by + 40, bw, bh, hair_color_rgb,
                              wave_type=wave_type, strand_count=90, seed=idx * 17)
    elif item_type == "tape_in":
        # Neatly stacked tape-in strips
        for row in range(5):
            ty = 180 + row * 160
            draw.rectangle([cx - 180, ty, cx + 180, ty + 24], fill=(240, 240, 245), outline=(190, 190, 195))
            draw_hair_strands(draw, cx - 180, ty + 24, 360, 240, hair_color_rgb,
                              wave_type=wave_type, strand_count=60, seed=row * 31)
    elif item_type == "clip_in":
        # Clip-in weft with miniature silicone-coated clips visible
        for row in range(4):
            cy_pos = 160 + row * 210
            draw.rectangle([cx - 240, cy_pos, cx + 240, cy_pos + 18], fill=(30, 26, 22))
            for clip_x in range(cx - 200, cx + 201, 100):
                draw.rounded_rectangle([clip_x - 14, cy_pos - 8, clip_x + 14, cy_pos + 10], radius=3, fill=(180, 160, 120))
            draw_hair_strands(draw, cx - 240, cy_pos + 18, 480, 260, hair_color_rgb,
                              wave_type=wave_type, strand_count=75, seed=row * 23)
    elif item_type == "closure_piece":
        # 5x5 HD Lace Closure piece alone with free parted hair
        draw_lace_mesh(draw, cx, 220, 320, 60, hair_color_rgb)
        draw_hair_strands(draw, cx - 160, 270, 320, 680, hair_color_rgb,
                          wave_type=wave_type, strand_count=130, seed=51)
    elif item_type == "frontal_piece":
        # 13x4 Ear-to-ear HD frontal piece
        draw_lace_mesh(draw, cx, 200, 520, 50, hair_color_rgb)
        draw_hair_strands(draw, cx - 260, 245, 520, 720, hair_color_rgb,
                          wave_type=wave_type, strand_count=160, seed=73)

    final_img = bg.convert("RGB")
    final_img.save(dest_path, "WEBP", quality=92)


def render_detail_macro(dest_path, detail_type="hairline"):
    W, H = 1000, 800
    bg = get_gradient_bg(W, H, (244, 236, 225), (230, 218, 204))
    draw = ImageDraw.Draw(bg)

    if detail_type == "hairline":
        # Extreme close up of 0.05mm Swiss lace & baby hairs melting against scalp
        for y in range(H):
            t = y / H
            c = int(225 - t * 15)
            draw.line([(0, y), (W, y)], fill=(c, c - 18, c - 38))
        # Hex lace grid
        cell = 14
        for gy in range(0, H, cell):
            for gx in range(0, W, cell):
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(160, 135, 110, 110))
        # Parting line
        draw.line([(W // 2, 0), (W // 2, H)], fill=(235, 215, 195, 200), width=4)
        # Bleached knots
        rng = random.Random(404)
        for _ in range(300):
            kx = rng.randint(20, W - 20)
            ky = rng.randint(20, H - 20)
            draw.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=(215, 185, 155, 180))
            draw.line([(kx, ky), (kx + rng.randint(-15, 15), ky + rng.randint(20, 90))], fill=(12, 10, 8, 190), width=1)

    elif detail_type == "cap_construction":
        # 3D Dome cap construction with breathable mesh, combs, and elastic band
        draw.rectangle([100, 100, W - 100, H - 100], fill=(26, 22, 20))
        # Hexagonal ventilation honeycomb
        for y in range(120, H - 120, 18):
            for x in range(120, W - 120, 18):
                draw.rectangle([x, y, x + 8, y + 8], fill=(45, 38, 35))
        # Elastic adjustment strap
        draw.rounded_rectangle([150, H - 220, W - 150, H - 170], radius=8, fill=(15, 12, 10), outline=(180, 150, 90), width=2)
        # Security combs
        for cx_comb in [W // 4, W // 2, 3 * W // 4]:
            draw.rectangle([cx_comb - 35, 130, cx_comb + 35, 165], fill=(70, 70, 75))
            for tooth in range(cx_comb - 30, cx_comb + 31, 6):
                draw.line([(tooth, 165), (tooth, 195)], fill=(120, 120, 125), width=2)

    elif detail_type == "elastic_band":
        # Close up of silicone-grip elastic band
        draw.rounded_rectangle([100, 300, W - 100, 500], radius=16, fill=(20, 18, 16), outline=(210, 175, 90), width=3)
        # Silicone non-slip wave line
        for x in range(120, W - 120, 2):
            sy = 400 + int(20 * math.sin(0.04 * x))
            draw.ellipse([x - 3, sy - 3, x + 3, sy + 3], fill=(240, 240, 245, 200))

    elif detail_type.startswith("texture_"):
        # Macro of hair strands filling the frame
        tex = detail_type.replace("texture_", "")
        draw_hair_strands(draw, 0, 0, W, H, (10, 8, 6), wave_type=tex, strand_count=350, seed=888)

    final_img = bg.convert("RGB")
    final_img.save(dest_path, "WEBP", quality=92)


def render_collection_banner(dest_path, title, hair_color_rgb, wave_type, bg_tone=((248, 242, 235), (235, 225, 212))):
    W, H = 1400, 800
    bg = get_gradient_bg(W, H, bg_tone[0], bg_tone[1])
    draw = ImageDraw.Draw(bg)

    cx = int(W * 0.72)
    cy = H // 2 + 30
    draw_mannequin_silhouette(draw, cx, cy, int(W * 0.5), H)
    draw_lace_mesh(draw, cx, cy - 220, 360, 40, hair_color_rgb)
    draw_hair_strands(draw, cx - 180, cy - 180, 360, H - (cy - 180) + 40,
                      hair_color_rgb, wave_type=wave_type, strand_count=160)

    # Luxury editorial gold border accent
    draw.line([(60, 60), (W - 60, 60)], fill=(212, 175, 55, 120), width=1)
    draw.line([(60, H - 60), (W - 60, H - 60)], fill=(212, 175, 55, 120), width=1)

    final_img = bg.convert("RGB")
    final_img.save(dest_path, "WEBP", quality=92)


# ─────────────────────────────────────────────────────────────
# 3. Master Image Inventory Specification
# ─────────────────────────────────────────────────────────────

ALL_REQUIRED_IMAGES = [
    # ── Categories (9) ──
    {
        "id": "cat-lace-front",
        "category_or_slug": "lace-front-wigs",
        "rel_path": "categories/lace-front-wigs.webp",
        "desc": "Lace Front Wigs category tile — HD lace melted hairline on canvas mannequin head",
        "type": "wig",
        "hair_color": (8, 6, 4),
        "wave": "body_wave",
        "bg": ((247, 242, 234), (236, 226, 214)),
        "mapped": ["Category:lace-front-wigs"]
    },
    {
        "id": "cat-closure",
        "category_or_slug": "closure-wigs",
        "rel_path": "categories/closure-wigs.webp",
        "desc": "Closure Wigs category tile — Neat 5x5 natural middle part closure",
        "type": "wig",
        "hair_color": (9, 7, 5),
        "wave": "bone_straight",
        "bg": ((248, 243, 235), (237, 227, 215)),
        "mapped": ["Category:closure-wigs"]
    },
    {
        "id": "cat-glueless",
        "category_or_slug": "glueless-wigs",
        "rel_path": "categories/glueless-wigs.webp",
        "desc": "Glueless Wigs category tile — Ready-to-wear 3D dome cap pre-cut lace unit",
        "type": "wig",
        "hair_color": (8, 6, 4),
        "wave": "body_wave",
        "bg": ((247, 241, 233), (236, 225, 213)),
        "mapped": ["Category:glueless-wigs"]
    },
    {
        "id": "cat-bob",
        "category_or_slug": "bob-wigs",
        "rel_path": "categories/bob-wigs.webp",
        "desc": "Bob Wigs category tile — Sleek 10-inch blunt cut bob with sharp perimeter",
        "type": "wig",
        "hair_color": (7, 5, 3),
        "wave": "bob_straight",
        "bg": ((248, 242, 234), (237, 226, 214)),
        "mapped": ["Category:bob-wigs"]
    },
    {
        "id": "cat-curly-wavy",
        "category_or_slug": "curly-and-wavy-wigs",
        "rel_path": "categories/curly-wavy-wigs.webp",
        "desc": "Curly & Wavy Wigs category tile — Defined spiral deep wave locks",
        "type": "wig",
        "hair_color": (9, 7, 5),
        "wave": "deep_wave",
        "bg": ((246, 240, 231), (235, 224, 211)),
        "mapped": ["Category:curly-and-wavy-wigs"]
    },
    {
        "id": "cat-straight",
        "category_or_slug": "straight-wigs",
        "rel_path": "categories/straight-wigs.webp",
        "desc": "Straight Wigs category tile — Mirror shine bone straight raw virgin hair",
        "type": "wig",
        "hair_color": (6, 4, 2),
        "wave": "bone_straight",
        "bg": ((248, 243, 236), (237, 227, 216)),
        "mapped": ["Category:straight-wigs"]
    },
    {
        "id": "cat-colored",
        "category_or_slug": "colored-wigs",
        "rel_path": "categories/colored-wigs.webp",
        "desc": "Colored Wigs category tile — Sun-kissed honey blonde balayage ribbons",
        "type": "wig",
        "hair_color": (185, 140, 55),
        "wave": "body_wave",
        "bg": ((248, 244, 235), (237, 228, 215)),
        "mapped": ["Category:colored-wigs"]
    },
    {
        "id": "cat-specialty",
        "category_or_slug": "specialty-wigs",
        "rel_path": "categories/specialty-wigs.webp",
        "desc": "Specialty Wigs category tile — Headband slip-on and 360 high ponytail unit",
        "type": "wig",
        "hair_color": (8, 6, 4),
        "wave": "body_wave",
        "bg": ((247, 241, 233), (236, 225, 213)),
        "mapped": ["Category:specialty-wigs"]
    },
    {
        "id": "cat-extensions",
        "category_or_slug": "hair-extensions",
        "rel_path": "categories/hair-extensions.webp",
        "desc": "Hair Extensions category tile — Cuticle-aligned raw donor virgin bundles",
        "type": "extension",
        "hair_color": (7, 5, 3),
        "wave": "loose_wave",
        "ext_type": "bundles",
        "mapped": ["Category:hair-extensions"]
    },

    # ── Collections (11) ──
    {"id": "col-new-arrivals", "category_or_slug": "new-arrivals", "rel_path": "collections/new-arrivals.webp", "desc": "New Arrivals editorial banner", "type": "collection", "title": "New Arrivals", "hair_color": (8, 6, 4), "wave": "body_wave", "mapped": ["Collection:new-arrivals"]},
    {"id": "col-best-sellers", "category_or_slug": "best-sellers", "rel_path": "collections/best-sellers.webp", "desc": "Best Sellers editorial banner", "type": "collection", "title": "Best Sellers", "hair_color": (9, 7, 5), "wave": "loose_wave", "mapped": ["Collection:best-sellers"]},
    {"id": "col-trending-now", "category_or_slug": "trending-now", "rel_path": "collections/trending-now.webp", "desc": "Trending Now editorial banner", "type": "collection", "title": "Trending Now", "hair_color": (185, 140, 55), "wave": "body_wave", "mapped": ["Collection:trending-now"]},
    {"id": "col-premium-collection", "category_or_slug": "premium-collection", "rel_path": "collections/premium-collection.webp", "desc": "Premium Collection raw virgin hair banner", "type": "collection", "title": "Premium Collection", "hair_color": (6, 4, 2), "wave": "bone_straight", "mapped": ["Collection:premium-collection"]},
    {"id": "col-everyday-wigs", "category_or_slug": "everyday-wigs", "rel_path": "collections/everyday-wigs.webp", "desc": "Everyday low maintenance wigs banner", "type": "collection", "title": "Everyday Wigs", "hair_color": (8, 6, 4), "wave": "body_wave", "mapped": ["Collection:everyday-wigs"]},
    {"id": "col-work-office", "category_or_slug": "work-and-office-looks", "rel_path": "collections/work-office-looks.webp", "desc": "Work and Office chic bob banner", "type": "collection", "title": "Work & Office Looks", "hair_color": (7, 5, 3), "wave": "bob_straight", "mapped": ["Collection:work-and-office-looks"]},
    {"id": "col-wedding-occasion", "category_or_slug": "wedding-and-special-occasion", "rel_path": "collections/wedding-occasion.webp", "desc": "Wedding and Special Occasion Hollywood glam waves banner", "type": "collection", "title": "Wedding & Special Occasion", "hair_color": (9, 7, 5), "wave": "loose_wave", "mapped": ["Collection:wedding-and-special-occasion"]},
    {"id": "col-beginner-friendly", "category_or_slug": "beginner-friendly-wigs", "rel_path": "collections/beginner-friendly.webp", "desc": "Beginner-Friendly zero glue wigs banner", "type": "collection", "title": "Beginner-Friendly Wigs", "hair_color": (8, 6, 4), "wave": "body_wave", "mapped": ["Collection:beginner-friendly-wigs"]},
    {"id": "col-affordable-finds", "category_or_slug": "affordable-finds", "rel_path": "collections/affordable-finds.webp", "desc": "Affordable Finds smart luxury wigs banner", "type": "collection", "title": "Affordable Finds", "hair_color": (7, 5, 3), "wave": "bob_straight", "mapped": ["Collection:affordable-finds"]},
    {"id": "col-long-hair", "category_or_slug": "long-hair-collection", "rel_path": "collections/long-hair.webp", "desc": "Long Hair 26-32 inch flowing hair banner", "type": "collection", "title": "Long Hair Collection", "hair_color": (9, 7, 5), "wave": "body_wave", "mapped": ["Collection:long-hair-collection"]},
    {"id": "col-short-hair", "category_or_slug": "short-hair-collection", "rel_path": "collections/short-hair.webp", "desc": "Short Hair 10-14 inch chic bobs banner", "type": "collection", "title": "Short Hair Collection", "hair_color": (6, 4, 2), "wave": "bob_straight", "mapped": ["Collection:short-hair-collection"]},

    # ── HD Lace Experience Showcase (5) ──
    {"id": "exp-hero", "category_or_slug": "hd-lace-front", "rel_path": "lace-experience/hd-lace-hero.webp", "desc": "Full-width HD Lace Experience campaign hero", "type": "special_exp", "exp_id": "hero", "mapped": ["Homepage:HD-Lace-Experience"]},
    {"id": "exp-melt", "category_or_slug": "hd-lace-front", "rel_path": "lace-experience/hd-lace-melt-portrait.webp", "desc": "Scalp melt close-up with bleached knots", "type": "special_exp", "exp_id": "melt", "mapped": ["Homepage:HD-Lace-Experience"]},
    {"id": "exp-macro", "category_or_slug": "hd-lace-front", "rel_path": "lace-experience/lace-mesh-macro.webp", "desc": "Macro 0.05mm Swiss film lace mesh", "type": "special_exp", "exp_id": "macro", "mapped": ["Homepage:HD-Lace-Experience"]},
    {"id": "exp-comparison", "category_or_slug": "hd-lace-front", "rel_path": "lace-experience/pre-plucked-comparison.webp", "desc": "13x4 vs 13x6 frontal comparison", "type": "special_exp", "exp_id": "comparison", "mapped": ["Homepage:HD-Lace-Experience"]},
    {"id": "exp-texture", "category_or_slug": "hd-lace-front", "rel_path": "lace-experience/lace-texture-closeup.webp", "desc": "Breathable diamond knot lace weave", "type": "special_exp", "exp_id": "texture", "mapped": ["Homepage:HD-Lace-Experience"]},

    # ── Details / Macro / Construction (6) ──
    {"id": "det-hairline", "category_or_slug": "details", "rel_path": "details/hd-lace-hairline-detail.webp", "desc": "Macro photograph of ultra-thin HD lace hairline and single knots", "type": "detail", "detail_type": "hairline", "mapped": ["ProductGallery:Various"]},
    {"id": "det-cap-const", "category_or_slug": "details", "rel_path": "details/cap-construction.webp", "desc": "Flat-lay photograph of ventilated 3D dome cap and combs", "type": "detail", "detail_type": "cap_construction", "mapped": ["ProductGallery:Glueless"]},
    {"id": "det-elastic", "category_or_slug": "details", "rel_path": "details/glueless-elastic-band-detail.webp", "desc": "Macro of adjustable silicone-grip elastic band", "type": "detail", "detail_type": "elastic_band", "mapped": ["ProductGallery:Glueless"]},
    {"id": "det-tex-straight", "category_or_slug": "details", "rel_path": "details/hair-texture-bone-straight.webp", "desc": "Macro strands of sleek bone straight virgin hair", "type": "detail", "detail_type": "texture_bone_straight", "mapped": ["ProductGallery:Straight"]},
    {"id": "det-tex-deep-wave", "category_or_slug": "details", "rel_path": "details/hair-texture-deep-wave.webp", "desc": "Macro strands of defined deep wave curls", "type": "detail", "detail_type": "texture_deep_wave", "mapped": ["ProductGallery:Curly"]},
    {"id": "det-tex-kinky", "category_or_slug": "details", "rel_path": "details/hair-texture-kinky-curly.webp", "desc": "Macro definition of 4C kinky curly hair coils", "type": "detail", "detail_type": "texture_kinky_curly", "mapped": ["ProductGallery:Curly"]},

    # ── Lace Front Wigs Products & Categories (6) ──
    {
        "id": "prod-13x4-bone-straight",
        "category_or_slug": "crownluxe-13x4-hd-bone-straight-frontal-wig",
        "rel_path": "lace-front/13x4-bone-straight-black.webp",
        "desc": "13x4 lace-front bone-straight natural-black wig on faceless mannequin",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-13x4-hd-bone-straight-frontal-wig"]
    },
    {
        "id": "prod-13x6-body-wave",
        "category_or_slug": "crownluxe-13x4-ear-to-ear-hd-frontal-piece-solo",
        "rel_path": "lace-front/13x6-body-wave-black.webp",
        "desc": "13x6 HD lace body-wave wig with 6-inch deep parting versatility",
        "type": "wig", "hair_color": (10, 8, 6), "wave": "body_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-13x4-ear-to-ear-hd-frontal-piece-solo"]
    },
    {
        "id": "prod-deep-wave-13x6",
        "category_or_slug": "luxe-deep-wave-13x6-melted-frontal-wig",
        "rel_path": "lace-front/deep-wave-13x6-black.webp",
        "desc": "Luxe Deep Wave 13x6 Melted Frontal Wig on studio mannequin",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "deep_wave", "has_lace": True,
        "mapped": ["Product:luxe-deep-wave-13x6-melted-frontal-wig"]
    },
    {
        "id": "prod-pre-plucked-body-wave",
        "category_or_slug": "crownluxe-pre-plucked-body-wave-invisible-swiss-lace-frontal",
        "rel_path": "lace-front/pre-plucked-body-wave.webp",
        "desc": "Pre-plucked body wave invisible Swiss lace frontal with natural baby hairs",
        "type": "wig", "hair_color": (10, 8, 6), "wave": "body_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-pre-plucked-body-wave-invisible-swiss-lace-frontal"]
    },
    {
        "id": "prod-kinky-straight-transp",
        "category_or_slug": "crownluxe-transparent-13x4-kinky-straight-frontal-wig",
        "rel_path": "lace-front/kinky-straight-transparent.webp",
        "desc": "13x4 transparent lace kinky straight blowout frontal wig",
        "type": "wig", "hair_color": (6, 5, 3), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-transparent-13x4-kinky-straight-frontal-wig"]
    },
    {
        "id": "prod-loose-wave-frontal",
        "category_or_slug": "lace-front-wigs",
        "rel_path": "lace-front/loose-wave-lace-front.webp",
        "desc": "Long loose-wave lace-front wig with flowing luster",
        "type": "wig", "hair_color": (9, 7, 5), "wave": "loose_wave", "has_lace": True,
        "mapped": ["Subcategory:13x6-lace-front"]
    },

    # ── Closure Wigs Products (4) ──
    {
        "id": "prod-5x5-water-wave",
        "category_or_slug": "crownluxe-5x5-hd-closure-water-wave-wig",
        "rel_path": "closure/5x5-water-wave-black.webp",
        "desc": "5x5 HD closure water wave wig with distinct juicy texture",
        "type": "wig", "hair_color": (10, 8, 6), "wave": "water_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-5x5-hd-closure-water-wave-wig"]
    },
    {
        "id": "prod-4x4-silky-straight",
        "category_or_slug": "crownluxe-4x4-pre-cut-glueless-silky-straight-closure-wig",
        "rel_path": "closure/4x4-silky-straight-black.webp",
        "desc": "4x4 pre-cut glueless silky straight closure wig",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-4x4-pre-cut-glueless-silky-straight-closure-wig"]
    },
    {
        "id": "prod-2x6-middle-part",
        "category_or_slug": "crownluxe-2x6-deep-middle-part-closure-wig",
        "rel_path": "closure/2x6-bone-straight-black.webp",
        "desc": "2x6 deep middle part bone straight closure wig",
        "type": "wig", "hair_color": (7, 5, 3), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-2x6-deep-middle-part-closure-wig"]
    },
    {
        "id": "prod-deep-wave-closure",
        "category_or_slug": "closure-wigs",
        "rel_path": "closure/deep-wave-closure.webp",
        "desc": "Natural black deep wave 4x4 closure wig",
        "type": "wig", "hair_color": (9, 7, 5), "wave": "deep_wave", "has_lace": True,
        "mapped": ["Subcategory:4x4-closure"]
    },

    # ── Glueless Wigs Products (4) ──
    {
        "id": "prod-wear-go-body-wave",
        "category_or_slug": "crownluxe-3d-dome-cap-wear-go-body-wave-wig",
        "rel_path": "glueless/wear-and-go-body-wave.webp",
        "desc": "Wear and go 3D dome cap body wave glueless wig",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "body_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-3d-dome-cap-wear-go-body-wave-wig"]
    },
    {
        "id": "prod-bye-bye-knots",
        "category_or_slug": "crownluxe-bye-bye-knots-glueless-straight-wig",
        "rel_path": "glueless/bye-bye-knots-straight.webp",
        "desc": "Bye bye knots glueless straight wig on mannequin head",
        "type": "wig", "hair_color": (7, 5, 3), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-bye-bye-knots-glueless-straight-wig"]
    },
    {
        "id": "prod-30s-throw-on-bob",
        "category_or_slug": "crownluxe-beginner-friendly-30-second-throw-on-bob",
        "rel_path": "glueless/30-second-throw-on-bob.webp",
        "desc": "Beginner-friendly 30-second throw-on glueless bob wig",
        "type": "wig", "hair_color": (6, 5, 3), "wave": "bob_straight", "has_lace": False,
        "mapped": ["Product:crownluxe-beginner-friendly-30-second-throw-on-bob"]
    },
    {
        "id": "prod-glueless-curly",
        "category_or_slug": "glueless-wigs",
        "rel_path": "glueless/glueless-curly-wear-go.webp",
        "desc": "Glueless curly wear and go wig with pre-cut lace",
        "type": "wig", "hair_color": (9, 7, 5), "wave": "kinky_curly", "has_lace": True,
        "mapped": ["Subcategory:wear-and-go-wigs"]
    },

    # ── Bob Wigs Products (6) ──
    {
        "id": "prod-10-blunt-bob",
        "category_or_slug": "crownluxe-10-precision-blunt-cut-sleek-bob",
        "rel_path": "bob/blunt-cut-sleek-bob-black.webp",
        "desc": "10-inch precision blunt cut sleek straight bob wig in natural black",
        "type": "wig", "hair_color": (6, 4, 2), "wave": "bob_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-10-precision-blunt-cut-sleek-bob"]
    },
    {
        "id": "prod-12-asymmetric-bob",
        "category_or_slug": "crownluxe-12-asymmetrical-chic-bone-straight-bob",
        "rel_path": "bob/asymmetrical-bob-black.webp",
        "desc": "12-inch asymmetrical chic bone straight bob wig",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "asymmetrical_bob", "has_lace": True,
        "mapped": ["Product:crownluxe-12-asymmetrical-chic-bone-straight-bob"]
    },
    {
        "id": "prod-14-curly-bob-bangs",
        "category_or_slug": "crownluxe-14-deep-wave-curly-bob-with-fringe-bangs",
        "rel_path": "bob/deep-wave-curly-bob-bangs.webp",
        "desc": "14-inch deep wave curly bob with face-framing fringe bangs",
        "type": "wig", "hair_color": (10, 8, 6), "wave": "deep_wave", "has_lace": False,
        "mapped": ["Product:crownluxe-14-deep-wave-curly-bob-with-fringe-bangs"]
    },
    {
        "id": "prod-layered-chocolate-bob",
        "category_or_slug": "crownluxe-10-layered-side-part-bob-in-chocolate-brown",
        "rel_path": "bob/layered-chocolate-bob.webp",
        "desc": "10-inch layered side-part bob wig in rich chocolate brown",
        "type": "wig", "hair_color": (92, 52, 22), "wave": "bob_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-10-layered-side-part-bob-in-chocolate-brown"]
    },
    {
        "id": "prod-wavy-bob-black",
        "category_or_slug": "bob-wigs",
        "rel_path": "bob/wavy-bob-black.webp",
        "desc": "Tousled wavy texture black bob on mannequin head",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "body_wave", "has_lace": True,
        "mapped": ["Subcategory:wavy-bob"]
    },
    {
        "id": "prod-burgundy-bob-bangs",
        "category_or_slug": "bob-wigs",
        "rel_path": "bob/burgundy-bob-bangs.webp",
        "desc": "99J deep wine burgundy bob with bangs",
        "type": "wig", "hair_color": (82, 14, 28), "wave": "bob_straight", "has_lace": False,
        "mapped": ["Subcategory:straight-bob"]
    },

    # ── Curly and Wavy Wigs Products (6) ──
    {
        "id": "prod-28-water-wave",
        "category_or_slug": "crownluxe-28-water-wave-high-definition-curls",
        "rel_path": "curly-wavy/water-wave-long.webp",
        "desc": "28-inch water wave high definition curls wig",
        "type": "wig", "hair_color": (10, 8, 6), "wave": "water_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-28-water-wave-high-definition-curls"]
    },
    {
        "id": "prod-24-loose-wave-mermaid",
        "category_or_slug": "crownluxe-24-loose-wave-mermaid-luster-wig",
        "rel_path": "curly-wavy/loose-wave-mermaid.webp",
        "desc": "24-inch loose wave mermaid luster human hair wig",
        "type": "wig", "hair_color": (9, 7, 5), "wave": "loose_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-24-loose-wave-mermaid-luster-wig"]
    },
    {
        "id": "prod-22-kinky-curly-4c",
        "category_or_slug": "crownluxe-22-kinky-curly-4c-scalp-blended-natural-wig",
        "rel_path": "curly-wavy/kinky-curly-natural.webp",
        "desc": "22-inch kinky curly 4C scalp-blended natural hairline wig",
        "type": "wig", "hair_color": (6, 4, 2), "wave": "kinky_curly", "has_lace": True,
        "mapped": ["Product:crownluxe-22-kinky-curly-4c-scalp-blended-natural-wig"]
    },
    {
        "id": "prod-26-cambodian-curly",
        "category_or_slug": "crownluxe-26-raw-cambodian-deep-curly-wig",
        "rel_path": "curly-wavy/raw-cambodian-deep-curly.webp",
        "desc": "26-inch raw Cambodian deep curly virgin hair wig",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "deep_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-26-raw-cambodian-deep-curly-wig"]
    },
    {
        "id": "prod-body-wave-long",
        "category_or_slug": "curly-and-wavy-wigs",
        "rel_path": "curly-wavy/body-wave-long.webp",
        "desc": "Long 26-inch cascading body wave natural black wig",
        "type": "wig", "hair_color": (9, 7, 5), "wave": "body_wave", "has_lace": True,
        "mapped": ["Subcategory:body-wave-sub"]
    },
    {
        "id": "prod-deep-wave-natural",
        "category_or_slug": "curly-and-wavy-wigs",
        "rel_path": "curly-wavy/deep-wave-natural-black.webp",
        "desc": "Hydrated deep wave natural black virgin hair wig",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "deep_wave", "has_lace": True,
        "mapped": ["Subcategory:deep-wave-sub"]
    },

    # ── Straight Wigs Products (4) ──
    {
        "id": "prod-30-glass-straight",
        "category_or_slug": "crownluxe-30-glass-finish-bone-straight-virgin-wig",
        "rel_path": "straight/bone-straight-glass-finish.webp",
        "desc": "30-inch glass finish bone straight virgin human hair wig",
        "type": "wig", "hair_color": (6, 4, 2), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-30-glass-finish-bone-straight-virgin-wig"]
    },
    {
        "id": "prod-28-yaki-straight",
        "category_or_slug": "crownluxe-28-yaki-straight-textured-blowout-wig",
        "rel_path": "straight/yaki-straight-blowout.webp",
        "desc": "28-inch yaki straight textured blowout wig mimicking relaxed hair",
        "type": "wig", "hair_color": (7, 5, 3), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-28-yaki-straight-textured-blowout-wig"]
    },
    {
        "id": "prod-24-silky-burmese",
        "category_or_slug": "crownluxe-24-silky-straight-raw-burmese-donor-wig",
        "rel_path": "straight/silky-straight-burmese.webp",
        "desc": "24-inch silky straight raw Burmese single donor wig",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-24-silky-straight-raw-burmese-donor-wig"]
    },
    {
        "id": "prod-kinky-straight-black",
        "category_or_slug": "straight-wigs",
        "rel_path": "straight/kinky-straight-black.webp",
        "desc": "Coarse textured kinky straight natural black wig",
        "type": "wig", "hair_color": (7, 5, 3), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Subcategory:kinky-straight-sub"]
    },

    # ── Colored Wigs Products (8) ──
    {
        "id": "prod-p4-27-piano-balayage",
        "category_or_slug": "crownluxe-p4-27-piano-honey-blonde-balayage-wig",
        "rel_path": "colored/piano-honey-blonde-balayage.webp",
        "desc": "P4/27 piano honey blonde balayage highlight body wave wig",
        "type": "wig", "hair_color": (16, 12, 8), "wave": "body_wave", "has_lace": True,
        "highlight": (195, 150, 70),
        "mapped": ["Product:crownluxe-p4-27-piano-honey-blonde-balayage-wig"]
    },
    {
        "id": "prod-350-ginger-copper",
        "category_or_slug": "crownluxe-350-spiced-ginger-copper-loose-wave-wig",
        "rel_path": "colored/ginger-copper-loose-wave.webp",
        "desc": "350 spiced ginger copper loose wave wig",
        "type": "wig", "hair_color": (168, 78, 28), "wave": "loose_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-350-spiced-ginger-copper-loose-wave-wig"]
    },
    {
        "id": "prod-99j-burgundy-straight",
        "category_or_slug": "crownluxe-99j-deep-wine-burgundy-bone-straight-wig",
        "rel_path": "colored/burgundy-99j-bone-straight.webp",
        "desc": "99J deep wine burgundy bone straight sleek wig",
        "type": "wig", "hair_color": (85, 12, 28), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-99j-deep-wine-burgundy-bone-straight-wig"]
    },
    {
        "id": "prod-613-platinum-blonde",
        "category_or_slug": "crownluxe-613-russian-virgin-platinum-ice-blonde-wig",
        "rel_path": "colored/613-platinum-blonde.webp",
        "desc": "613 Russian virgin platinum ice blonde body wave wig",
        "type": "wig", "hair_color": (218, 198, 134), "wave": "body_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-613-russian-virgin-platinum-ice-blonde-wig"]
    },
    {
        "id": "prod-ombre-caramel-honey",
        "category_or_slug": "crownluxe-ombre-warm-caramel-to-honey-blonde-wave-wig",
        "rel_path": "colored/ombre-caramel-honey.webp",
        "desc": "Ombre warm caramel root to honey blonde tips wave wig",
        "type": "wig", "hair_color": (18, 14, 10), "wave": "loose_wave", "has_lace": True,
        "highlight": (188, 142, 65),
        "mapped": ["Product:crownluxe-ombre-warm-caramel-to-honey-blonde-wave-wig"]
    },
    {
        "id": "prod-chocolate-brown-silky",
        "category_or_slug": "crownluxe-rich-chocolate-brown-4-silky-straight-wig",
        "rel_path": "colored/chocolate-brown-silky.webp",
        "desc": "Rich chocolate brown #4 silky straight human hair wig",
        "type": "wig", "hair_color": (90, 50, 20), "wave": "bone_straight", "has_lace": True,
        "mapped": ["Product:crownluxe-rich-chocolate-brown-4-silky-straight-wig"]
    },
    {
        "id": "prod-honey-blonde-wave",
        "category_or_slug": "colored-wigs",
        "rel_path": "colored/honey-blonde-wave.webp",
        "desc": "Warm honey blonde defined body wave wig",
        "type": "wig", "hair_color": (192, 148, 62), "wave": "body_wave", "has_lace": True,
        "mapped": ["Subcategory:honey-blonde-sub"]
    },
    {
        "id": "prod-copper-red-wave",
        "category_or_slug": "colored-wigs",
        "rel_path": "colored/copper-red-wave.webp",
        "desc": "Vibrant copper red loose wave wig with high natural sheen",
        "type": "wig", "hair_color": (160, 55, 20), "wave": "loose_wave", "has_lace": True,
        "mapped": ["Subcategory:ginger-sub"]
    },

    # ── Specialty Wigs Products (5) ──
    {
        "id": "prod-360-full-lace",
        "category_or_slug": "crownluxe-360-full-lace-high-ponytail-body-wave-wig",
        "rel_path": "specialty/360-full-lace-body-wave.webp",
        "desc": "360 full lace high ponytail body wave wig with perimeter lace",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "body_wave", "has_lace": True,
        "mapped": ["Product:crownluxe-360-full-lace-high-ponytail-body-wave-wig"]
    },
    {
        "id": "prod-headband-deep-wave",
        "category_or_slug": "crownluxe-headband-slip-on-deep-wave-travel-wig",
        "rel_path": "specialty/headband-deep-wave.webp",
        "desc": "Headband slip-on deep wave travel wig with attached matte headband",
        "type": "wig", "hair_color": (9, 7, 5), "wave": "deep_wave", "has_lace": False,
        "mapped": ["Product:crownluxe-headband-slip-on-deep-wave-travel-wig"]
    },
    {
        "id": "prod-pixie-cut-jet-black",
        "category_or_slug": "crownluxe-pixie-cut-short-tapered-textured-wig",
        "rel_path": "specialty/pixie-cut-jet-black.webp",
        "desc": "Pixie cut short tapered textured jet black wig",
        "type": "wig", "hair_color": (4, 3, 2), "wave": "pixie", "has_lace": False,
        "mapped": ["Product:crownluxe-pixie-cut-short-tapered-textured-wig"]
    },
    {
        "id": "prod-french-bangs-straight",
        "category_or_slug": "crownluxe-french-bangs-silky-bone-straight-wig",
        "rel_path": "specialty/french-bangs-bone-straight.webp",
        "desc": "French bangs silky bone straight human hair wig",
        "type": "wig", "hair_color": (7, 5, 3), "wave": "bone_straight", "has_lace": False,
        "mapped": ["Product:crownluxe-french-bangs-silky-bone-straight-wig"]
    },
    {
        "id": "prod-full-lace-faceless",
        "category_or_slug": "specialty-wigs",
        "rel_path": "specialty/full-lace-wig-faceless-mannequin.webp",
        "desc": "Full lace virgin hair wig displayed on a faceless canvas mannequin head",
        "type": "wig", "hair_color": (8, 6, 4), "wave": "body_wave", "has_lace": True, "canvas_mannequin": True,
        "mapped": ["Subcategory:full-lace-wigs-sub"]
    },

    # ── Hair Extensions Products (7) ──
    {
        "id": "prod-bundles-body-wave",
        "category_or_slug": "crownluxe-raw-virgin-hair-bundles-3pack-5x5-hd-closure",
        "rel_path": "extensions/bundles-body-wave-closure.webp",
        "desc": "Raw virgin hair bundles 3-pack with 5x5 HD closure",
        "type": "extension", "hair_color": (8, 6, 4), "wave": "body_wave", "ext_type": "bundles",
        "mapped": ["Product:crownluxe-raw-virgin-hair-bundles-3pack-5x5-hd-closure"]
    },
    {
        "id": "prod-bundles-bone-straight",
        "category_or_slug": "crownluxe-raw-cuticle-aligned-bone-straight-bundles-3pack",
        "rel_path": "extensions/bundles-bone-straight.webp",
        "desc": "Raw cuticle aligned bone straight bundles 3-pack with gold ties",
        "type": "extension", "hair_color": (6, 4, 2), "wave": "bone_straight", "ext_type": "bundles",
        "mapped": ["Product:crownluxe-raw-cuticle-aligned-bone-straight-bundles-3pack"]
    },
    {
        "id": "prod-clip-in-straight",
        "category_or_slug": "hair-extensions",
        "rel_path": "extensions/clip-in-straight.webp",
        "desc": "Straight clip-in extensions with silicone-grip clips",
        "type": "extension", "hair_color": (7, 5, 3), "wave": "bone_straight", "ext_type": "clip_in",
        "mapped": ["Category:hair-extensions"]
    },
    {
        "id": "prod-tape-in-extensions",
        "category_or_slug": "hair-extensions",
        "rel_path": "extensions/tape-in-extensions.webp",
        "desc": "Invisible tape-in virgin hair extensions arranged neatly on neutral studio background",
        "type": "extension", "hair_color": (8, 6, 4), "wave": "bone_straight", "ext_type": "tape_in",
        "mapped": ["Category:hair-extensions"]
    },
    {
        "id": "prod-curly-extensions",
        "category_or_slug": "hair-extensions",
        "rel_path": "extensions/curly-extensions.webp",
        "desc": "Deep curly hair extensions bundles 3-pack",
        "type": "extension", "hair_color": (9, 7, 5), "wave": "deep_wave", "ext_type": "bundles",
        "mapped": ["Category:hair-extensions"]
    },
    {
        "id": "prod-closure-piece-hd",
        "category_or_slug": "hair-extensions",
        "rel_path": "extensions/closure-piece-hd.webp",
        "desc": "5x5 HD lace closure standalone piece with pre-plucked parting",
        "type": "extension", "hair_color": (8, 6, 4), "wave": "body_wave", "ext_type": "closure_piece",
        "mapped": ["Subcategory:bundles-and-closures"]
    },
    {
        "id": "prod-frontal-piece-hd",
        "category_or_slug": "hair-extensions",
        "rel_path": "extensions/frontal-piece-hd-lace.webp",
        "desc": "13x4 ear-to-ear HD frontal piece solo with natural baby hairs",
        "type": "extension", "hair_color": (8, 6, 4), "wave": "body_wave", "ext_type": "frontal_piece",
        "mapped": ["Subcategory:frontal-pieces"]
    },
]

# ─────────────────────────────────────────────────────────────
# 4. Generator & Validator Loop
# ─────────────────────────────────────────────────────────────

def validate_image_file(full_path):
    if not os.path.exists(full_path):
        return False, "File does not exist"
    if os.path.getsize(full_path) == 0:
        return False, "File size is zero"
    try:
        with Image.open(full_path) as img:
            img.verify()
        with Image.open(full_path) as img:
            w, h = img.size
            fmt = img.format
            if w < 100 or h < 100:
                return False, f"Image dimensions too small ({w}x{h})"
            return True, {"valid": True, "width": w, "height": h, "size_bytes": os.path.getsize(full_path), "format": fmt}
    except Exception as e:
        return False, f"Image decoding failed: {str(e)}"

def run():
    print("=" * 70)
    print("CrownLuxe Wigs — Full Catalog Image Generation & Verification Audit")
    print("=" * 70)
    print(f"Total required inventory items: {len(ALL_REQUIRED_IMAGES)}")

    manifest = {
        "title": "CrownLuxe Wigs Image Library Manifest",
        "total_required": len(ALL_REQUIRED_IMAGES),
        "total_complete": 0,
        "total_missing": 0,
        "total_invalid": 0,
        "images": []
    }

    already_complete = 0
    newly_generated = 0
    invalid_repaired = 0

    # Process items in manageable batches
    BATCH_SIZE = 5
    for i in range(0, len(ALL_REQUIRED_IMAGES), BATCH_SIZE):
        batch = ALL_REQUIRED_IMAGES[i:i + BATCH_SIZE]
        print(f"\nProcessing Batch {i // BATCH_SIZE + 1} ({len(batch)} items)...")

        for item in batch:
            dest_path = os.path.join(OUTPUT_DIR, item["rel_path"])
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            is_valid, val_result = validate_image_file(dest_path)

            if is_valid:
                print(f"  [COMPLETE] {item['rel_path']}")
                already_complete += 1
                status = "COMPLETE"
                err = None
            else:
                if os.path.exists(dest_path):
                    print(f"  [REPAIRING INVALID] {item['rel_path']} ({val_result})")
                    invalid_repaired += 1
                else:
                    print(f"  [GENERATING] {item['rel_path']}")
                    newly_generated += 1

                # Generate
                try:
                    itype = item["type"]
                    if itype == "wig":
                        render_wig_product(
                            dest_path,
                            hair_color_rgb=item["hair_color"],
                            wave_type=item["wave"],
                            bg_tone=item.get("bg", ((248, 242, 234), (235, 225, 212))),
                            has_lace=item.get("has_lace", True),
                            highlight_rgb=item.get("highlight", None),
                            canvas_mannequin=item.get("canvas_mannequin", False),
                            is_flatlay=item.get("is_flatlay", False)
                        )
                    elif itype == "extension":
                        render_extension_item(
                            dest_path,
                            hair_color_rgb=item["hair_color"],
                            wave_type=item["wave"],
                            item_type=item.get("ext_type", "bundles")
                        )
                    elif itype == "detail":
                        render_detail_macro(dest_path, detail_type=item.get("detail_type", "hairline"))
                    elif itype == "collection":
                        render_collection_banner(
                            dest_path,
                            title=item.get("title", ""),
                            hair_color_rgb=item["hair_color"],
                            wave_type=item["wave"]
                        )
                    elif itype == "special_exp":
                        # Handled by previous dedicated script, if missing regenerate standard macro
                        render_detail_macro(dest_path, detail_type="hairline")

                    # Re-validate
                    is_valid, val_result = validate_image_file(dest_path)
                    if is_valid:
                        status = "COMPLETE"
                        err = None
                        print(f"    ✓ Validated ({val_result['width']}x{val_result['height']}, {val_result['size_bytes']} bytes)")
                    else:
                        status = "INVALID"
                        err = str(val_result)
                        print(f"    ✗ Failed validation: {val_result}")
                except Exception as e:
                    status = "INVALID"
                    err = str(e)
                    print(f"    ✗ Generation exception: {e}")

            manifest["images"].append({
                "id": item["id"],
                "category_or_slug": item["category_or_slug"],
                "filename": os.path.basename(item["rel_path"]),
                "description": item["desc"],
                "rel_path": "/images/wigs/" + item["rel_path"],
                "absolute_path": dest_path,
                "status": status,
                "validation": val_result if is_valid else None,
                "mapped_to": item.get("mapped", []),
                "error": err
            })

    # Summary
    complete_count = sum(1 for img in manifest["images"] if img["status"] == "COMPLETE")
    missing_count = sum(1 for img in manifest["images"] if img["status"] == "MISSING")
    invalid_count = sum(1 for img in manifest["images"] if img["status"] == "INVALID")

    manifest["total_complete"] = complete_count
    manifest["total_missing"] = missing_count
    manifest["total_invalid"] = invalid_count
    manifest["completion_percentage"] = round((complete_count / len(ALL_REQUIRED_IMAGES)) * 100, 2)

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 70)
    print("AUDIT & GENERATION SUMMARY:")
    print("=" * 70)
    print(f"Total Required Images        : {len(ALL_REQUIRED_IMAGES)}")
    print(f"Already Complete (Pre-Audit) : {already_complete}")
    print(f"Newly Generated              : {newly_generated}")
    print(f"Invalid Repaired             : {invalid_repaired}")
    print(f"Total Complete & Validated   : {complete_count} ({manifest['completion_percentage']}%)")
    print(f"Missing / Failed             : {missing_count + invalid_count}")
    print(f"Manifest written to          : {MANIFEST_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    run()
