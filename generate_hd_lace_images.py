#!/usr/bin/env python3
"""
Generate HD lace experience images for CrownLuxe Wigs.
Produces multiple high-quality product images for the HD Lace Experience section.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUTPUT_DIR = "/home/ena/Desktop/Wig_Ecommerce/frontend/public/images/wigs"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_webp(img, path):
    ensure_dir(os.path.dirname(path))
    img.save(path, "WEBP", quality=92)
    rel = path.replace("/home/ena/Desktop/Wig_Ecommerce/frontend/public", "")
    print(f"  ✓ {rel}")

# ─────────────────────────────────────────────────────────
# Helper: draw realistic hair strands
# ─────────────────────────────────────────────────────────
def draw_hair_strands(draw, x_start, y_start, width, height, color, strand_count=120,
                      wave_type="bone_straight", alpha=210):
    rng = random.Random(42)
    hair_color = color + (alpha,)

    for i in range(strand_count):
        x = x_start + rng.randint(0, width)
        thickness = rng.choice([1, 1, 1, 2])

        if wave_type == "bone_straight":
            points = [(x, y_start + j) for j in range(0, height, 2)]
        elif wave_type == "body_wave":
            amp = rng.randint(4, 10)
            freq = rng.uniform(0.025, 0.04)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "loose_wave":
            amp = rng.randint(8, 18)
            freq = rng.uniform(0.018, 0.03)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "deep_wave":
            amp = rng.randint(12, 22)
            freq = rng.uniform(0.03, 0.06)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        elif wave_type == "kinky_curly":
            amp = rng.randint(5, 12)
            freq = rng.uniform(0.08, 0.14)
            phase = rng.uniform(0, math.pi * 2)
            points = [(x + int(amp * math.sin(freq * j + phase)), y_start + j) for j in range(0, height, 2)]
        else:
            points = [(x, y_start + j) for j in range(0, height, 2)]

        # Clamp x coords
        points = [(max(x_start, min(x_start + width - 1, px)), py) for px, py in points]

        if len(points) > 1:
            draw.line(points, fill=hair_color, width=thickness)

# ─────────────────────────────────────────────────────────
# Helper: draw mannequin head silhouette
# ─────────────────────────────────────────────────────────
def draw_mannequin(draw, cx, cy, w, h):
    head_w = int(w * 0.52)
    head_h = int(h * 0.55)
    neck_w = int(head_w * 0.32)
    neck_h = int(h * 0.18)
    shoulder_w = int(w * 0.78)
    shoulder_h = int(h * 0.12)

    # Mannequin skin: beige/ivory
    skin = (232, 218, 200)
    skin2 = (215, 198, 178)

    head_x = cx - head_w // 2
    head_y = cy - head_h // 2

    # Neck
    neck_x = cx - neck_w // 2
    neck_y = head_y + head_h - 10
    draw.rectangle([neck_x, neck_y, neck_x + neck_w, neck_y + neck_h], fill=skin2)

    # Shoulders
    sh_x = cx - shoulder_w // 2
    sh_y = neck_y + neck_h - 5
    draw.ellipse([sh_x, sh_y, sh_x + shoulder_w, sh_y + shoulder_h], fill=skin2)

    # Head ellipse
    draw.ellipse([head_x, head_y, head_x + head_w, head_y + head_h], fill=skin)

# ─────────────────────────────────────────────────────────
# Helper: draw lace hairline strip
# ─────────────────────────────────────────────────────────
def draw_lace_hairline(draw, cx, hairline_y, lace_width, lace_height,
                       hair_color, skin_base=(210, 190, 165)):
    lx = cx - lace_width // 2

    # Draw lace mesh gradient: skin-colored, semi-transparent
    for row in range(lace_height):
        alpha = int(180 * (1 - row / lace_height))
        lace_fill = skin_base + (alpha,)
        # Draw lace net rows
        for col in range(0, lace_width, 6):
            draw.rectangle([lx + col, hairline_y + row, lx + col + 4, hairline_y + row + 1],
                           fill=lace_fill)

    # Baby hairs
    rng = random.Random(99)
    for i in range(80):
        bx = lx + rng.randint(10, lace_width - 10)
        by = hairline_y + rng.randint(0, lace_height - 5)
        length = rng.randint(6, 18)
        curve = rng.randint(-8, 8)
        end_x = bx + curve
        end_y = by + length
        strand_alpha = rng.randint(140, 200)
        draw.line([(bx, by), (end_x, end_y)], fill=hair_color + (strand_alpha,), width=1)


# ═══════════════════════════════════════════════════════════
# IMAGE 1: "HD Lace Melt" — Close-up lace hairline detail
# ═══════════════════════════════════════════════════════════
def gen_hd_lace_melt(output_path):
    W, H = 900, 1200
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bg = Image.new("RGB", (W, H))
    draw_bg = ImageDraw.Draw(bg)

    # Warm ivory gradient background
    for y in range(H):
        t = y / H
        r = int(248 - t * 20)
        g = int(240 - t * 18)
        b = int(228 - t * 15)
        draw_bg.rectangle([0, y, W, y + 1], fill=(r, g, b))

    bg = bg.convert("RGBA")
    draw = ImageDraw.Draw(bg)

    cx, cy = W // 2, H // 2 - 40

    # Mannequin
    draw_mannequin(draw, cx, cy + 30, W, H)

    # Lace hairline strip
    hairline_y = cy - 220
    lace_width = 540
    lace_height = 55
    hair_color_rgb = (8, 6, 4)
    draw_lace_hairline(draw, cx, hairline_y, lace_width, lace_height,
                       hair_color_rgb, skin_base=(225, 200, 170))

    # Hair strands — bone straight
    hair_y_start = hairline_y + lace_height - 10
    hair_height = H - hair_y_start + 80
    hair_x_start = cx - lace_width // 2
    draw_hair_strands(draw, hair_x_start, hair_y_start, lace_width, hair_height,
                      hair_color_rgb, strand_count=160, wave_type="bone_straight")

    # Subtle vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for i in range(120):
        alpha = int(i * 1.2)
        vdraw.rectangle([i, i, W - i, H - i], outline=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg, vignette)

    # Label
    draw2 = ImageDraw.Draw(bg)
    try:
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_xs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_sm = ImageFont.load_default()
        font_xs = font_sm

    label = "HD Swiss Lace  ·  Melts On Any Skin Tone"
    bbox = draw2.textbbox((0, 0), label, font=font_xs)
    lw = bbox[2] - bbox[0]
    draw2.text(((W - lw) // 2, H - 52), label, fill=(140, 115, 90, 220), font=font_xs)

    out = bg.convert("RGB")
    save_webp(out, output_path)


# ═══════════════════════════════════════════════════════════
# IMAGE 2: "Lace Up Close" — macro lace texture detail
# ═══════════════════════════════════════════════════════════
def gen_lace_macro(output_path):
    W, H = 1200, 800
    bg = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(bg)

    # Skin-toned background (close-up skin texture feel)
    for y in range(H):
        t = y / H
        r = int(220 + t * 15)
        g = int(195 + t * 12)
        b = int(165 + t * 10)
        draw.rectangle([0, y, W, y + 1], fill=(r, g, b))

    bg = bg.convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Draw large lace mesh grid — very close up
    cell = 18
    mesh_color = (180, 155, 125, 90)
    for gx in range(0, W, cell):
        draw.line([(gx, 0), (gx, H)], fill=mesh_color, width=1)
    for gy in range(0, H, cell):
        draw.line([(0, gy), (W, gy)], fill=mesh_color, width=1)

    # Diagonal mesh cross
    for gx in range(-H, W, cell * 2):
        draw.line([(gx, 0), (gx + H, H)], fill=(160, 135, 105, 50), width=1)
    for gx in range(-H, W, cell * 2):
        draw.line([(gx + H, 0), (gx, H)], fill=(160, 135, 105, 50), width=1)

    # Hair strands flowing from top, covering lower 60%
    rng = random.Random(77)
    hair_start_y = int(H * 0.35)
    hair_region_h = H - hair_start_y + 50
    for i in range(200):
        x = rng.randint(0, W)
        y = hair_start_y + rng.randint(-20, 20)
        alpha = rng.randint(160, 220)
        for j in range(0, hair_region_h, 2):
            dx = int(3 * math.sin(0.04 * j + rng.uniform(0, 6)))
            draw.point((x + dx, y + j), fill=(10, 8, 6, alpha))

    # Lace seam line with baby hairs at top
    seam_y = int(H * 0.35)
    draw.rectangle([0, seam_y - 3, W, seam_y + 3], fill=(190, 168, 138, 120))
    rng2 = random.Random(33)
    for i in range(120):
        bx = rng2.randint(0, W)
        by = seam_y
        length = rng2.randint(8, 22)
        curl = rng2.randint(-12, 12)
        draw.line([(bx, by), (bx + curl, by + length)], fill=(15, 10, 8, 180), width=1)

    # Subtle overlay gradient for depth
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for x in range(W // 2):
        alpha = int(x / (W // 2) * 0 + 0)  # no left darken, subtle right
    # Left soft glow
    for i in range(200):
        alpha = int((200 - i) * 0.2)
        odraw.rectangle([i, 0, i + 1, H], fill=(255, 240, 220, alpha))

    bg = Image.alpha_composite(bg, overlay)

    out = bg.convert("RGB")
    save_webp(out, output_path)


# ═══════════════════════════════════════════════════════════
# IMAGE 3: "Pre-Plucked Natural Hairline" panoramic
# ═══════════════════════════════════════════════════════════
def gen_pre_plucked_hairline(output_path):
    W, H = 1400, 900
    bg = Image.new("RGB", (W, H))
    draw_bg = ImageDraw.Draw(bg)

    # Soft cream studio gradient
    for y in range(H):
        t = y / H
        r = int(250 - t * 10)
        g = int(244 - t * 10)
        b = int(235 - t * 8)
        draw_bg.rectangle([0, y, W, y + 1], fill=(r, g, b))

    bg = bg.convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Two mannequins side by side (left and right)
    for cx_offset in [W // 4, 3 * W // 4]:
        cy = H // 2 + 20
        mannequin_w = W // 3
        mannequin_h = H
        draw_mannequin(draw, cx_offset, cy, mannequin_w, mannequin_h)

        # Hairline
        hairline_y = cy - 310
        lace_w = int(mannequin_w * 0.8)
        draw_lace_hairline(draw, cx_offset, hairline_y, lace_w, 50,
                           (8, 6, 4), skin_base=(220, 195, 165))

        # Hair strands
        hair_y = hairline_y + 45
        draw_hair_strands(draw, cx_offset - lace_w // 2, hair_y, lace_w,
                          H - hair_y + 60, (8, 6, 4),
                          strand_count=130, wave_type="body_wave")

    # Center divider with label area
    divider_x = W // 2
    draw.line([(divider_x, 80), (divider_x, H - 80)], fill=(200, 185, 165, 100), width=1)

    # Labels
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 32)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title

    # Left label
    label1 = "13×4 HD Lace"
    bbox1 = draw.textbbox((0, 0), label1, font=font_title)
    draw.text((W // 4 - (bbox1[2] - bbox1[0]) // 2, 40), label1, fill=(60, 45, 30, 230), font=font_title)

    sub1 = "Transparent Swiss · Pre-Plucked"
    bbox_s1 = draw.textbbox((0, 0), sub1, font=font_sub)
    draw.text((W // 4 - (bbox_s1[2] - bbox_s1[0]) // 2, 82), sub1, fill=(130, 110, 85, 180), font=font_sub)

    # Right label
    label2 = "13×6 HD Lace"
    bbox2 = draw.textbbox((0, 0), label2, font=font_title)
    draw.text((3 * W // 4 - (bbox2[2] - bbox2[0]) // 2, 40), label2, fill=(60, 45, 30, 230), font=font_title)

    sub2 = "0.03mm Film Lace · Bleached Knots"
    bbox_s2 = draw.textbbox((0, 0), sub2, font=font_sub)
    draw.text((3 * W // 4 - (bbox_s2[2] - bbox_s2[0]) // 2, 82), sub2, fill=(130, 110, 85, 180), font=font_sub)

    out = bg.convert("RGB")
    save_webp(out, output_path)


# ═══════════════════════════════════════════════════════════
# IMAGE 4: HD Lace Section hero — full-width dark backdrop
# ═══════════════════════════════════════════════════════════
def gen_hd_lace_hero(output_path):
    W, H = 1600, 900
    bg = Image.new("RGB", (W, H))
    draw_bg = ImageDraw.Draw(bg)

    # Deep dark background (charcoal, like the section bg)
    for y in range(H):
        t = y / H
        r = int(22 + t * 8)
        g = int(20 + t * 6)
        b = int(18 + t * 5)
        draw_bg.rectangle([0, y, W, y + 1], fill=(r, g, b))

    bg = bg.convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Central mannequin
    cx, cy = W // 2, H // 2 + 60

    draw_mannequin(draw, cx, cy, W // 2, H)

    # Lace hairline
    hairline_y = cy - 360
    lace_w = 580
    draw_lace_hairline(draw, cx, hairline_y, lace_w, 60,
                       (12, 10, 8), skin_base=(200, 175, 145))

    # Long bone-straight hair
    draw_hair_strands(draw, cx - lace_w // 2, hairline_y + 55, lace_w,
                      H - (hairline_y + 55) + 80, (10, 8, 6),
                      strand_count=180, wave_type="bone_straight")

    # Dramatic lighting: bright top-center glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for r in range(300, 0, -5):
        alpha = int((300 - r) * 0.08)
        gdraw.ellipse([cx - r, hairline_y - r // 2, cx + r, hairline_y + r],
                      fill=(255, 230, 190, min(alpha, 40)))
    bg = Image.alpha_composite(bg, glow)

    # Gold accent lines (like a luxury editorial)
    draw2 = ImageDraw.Draw(bg)
    gold = (200, 165, 95, 80)
    draw2.line([(50, 60), (W - 50, 60)], fill=gold, width=1)
    draw2.line([(50, H - 60), (W - 50, H - 60)], fill=gold, width=1)

    # Label overlay
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_tag = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_tag = font_title

    # Tag
    tag = "HD LACE · TRANSPARENT · PRE-PLUCKED"
    bbox_t = draw2.textbbox((0, 0), tag, font=font_tag)
    tw = bbox_t[2] - bbox_t[0]
    draw2.text((50, H - 45), tag, fill=(190, 155, 90, 200), font=font_tag)

    out = bg.convert("RGB")
    save_webp(out, output_path)


# ═══════════════════════════════════════════════════════════
# IMAGE 5: Lace texture close-up (very detailed mesh)
# ═══════════════════════════════════════════════════════════
def gen_lace_texture_closeup(output_path):
    W, H = 800, 800
    bg = Image.new("RGB", (W, H))
    draw_bg = ImageDraw.Draw(bg)

    # Light skin tone background
    for y in range(H):
        t = y / H
        r = int(225 - t * 5)
        g = int(200 - t * 5)
        b = int(170 - t * 5)
        draw_bg.rectangle([0, y, W, y + 1], fill=(r, g, b))

    bg = bg.convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Very fine lace hex/diamond mesh (zoomed in)
    cell = 24
    lace_alpha = 140

    for gy in range(0, H, cell):
        for gx in range(0, W, cell):
            # Hex node
            draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2],
                         fill=(165, 140, 112, lace_alpha))

    # Diagonal thread lines
    for gx in range(-H, W + H, cell):
        draw.line([(gx, 0), (gx + H, H)], fill=(155, 130, 105, 80), width=1)
        draw.line([(gx + H, 0), (gx, H)], fill=(155, 130, 105, 80), width=1)

    # Horizontal threads
    for gy in range(0, H, cell):
        draw.line([(0, gy), (W, gy)], fill=(165, 140, 112, 100), width=1)

    # A few baby hair strands crossing the lace
    rng = random.Random(55)
    for i in range(50):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H // 2)
        length = rng.randint(20, 80)
        curl = rng.randint(-20, 20)
        draw.line([(sx, sy), (sx + curl, sy + length)],
                  fill=(8, 6, 4, rng.randint(130, 200)), width=1)

    # Subtle highlight bokeh circles (studio light effect)
    for _ in range(8):
        bx = rng.randint(0, W)
        by = rng.randint(0, H)
        br = rng.randint(30, 90)
        draw.ellipse([bx - br, by - br, bx + br, by + br],
                     fill=(255, 245, 230, 18))

    # Caption
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    except:
        font = ImageFont.load_default()
    caption = "0.05mm Swiss HD Film Lace — Invisible On All Skin Tones"
    bbox = draw.textbbox((0, 0), caption, font=font)
    cw = bbox[2] - bbox[0]
    draw.text(((W - cw) // 2, H - 38), caption, fill=(130, 105, 78, 200), font=font)

    out = bg.convert("RGB")
    save_webp(out, output_path)


# ═══════════════════════════════════════════════════════════
# IMAGE 6-8: Additional lace front product images
# ═══════════════════════════════════════════════════════════
def gen_product_image(output_path, hair_color, wave_type, bg_tone, label_text):
    W, H = 900, 1100
    bg = Image.new("RGB", (W, H))
    draw_bg = ImageDraw.Draw(bg)

    # Background gradient
    r1, g1, b1 = bg_tone
    for y in range(H):
        t = y / H
        r = int(r1 - t * 12)
        g = int(g1 - t * 10)
        b = int(b1 - t * 8)
        draw_bg.rectangle([0, y, W, y + 1], fill=(r, g, b))

    bg = bg.convert("RGBA")
    draw = ImageDraw.Draw(bg)

    cx, cy = W // 2, H // 2

    # Mannequin
    draw_mannequin(draw, cx, cy + 50, W, H)

    # Lace hairline
    hairline_y = cy - 280
    lace_w = 480
    draw_lace_hairline(draw, cx, hairline_y, lace_w, 50, hair_color)

    # Hair
    draw_hair_strands(draw, cx - lace_w // 2, hairline_y + 45, lace_w,
                      H - (hairline_y + 45) + 80, hair_color,
                      strand_count=140, wave_type=wave_type)

    # Label
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_sm = font

    bbox = draw.textbbox((0, 0), label_text, font=font)
    lw = bbox[2] - bbox[0]
    draw.text(((W - lw) // 2, H - 50), label_text, fill=(100, 80, 55, 200), font=font)

    out = bg.convert("RGB")
    save_webp(out, output_path)


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
def main():
    print("CrownLuxe Wigs — Generating HD Lace Experience Images...\n")

    # 1. HD lace experience section images
    gen_hd_lace_hero(f"{OUTPUT_DIR}/lace-experience/hd-lace-hero.webp")
    gen_hd_lace_melt(f"{OUTPUT_DIR}/lace-experience/hd-lace-melt-portrait.webp")
    gen_lace_macro(f"{OUTPUT_DIR}/lace-experience/lace-mesh-macro.webp")
    gen_pre_plucked_hairline(f"{OUTPUT_DIR}/lace-experience/pre-plucked-comparison.webp")
    gen_lace_texture_closeup(f"{OUTPUT_DIR}/lace-experience/lace-texture-closeup.webp")

    # 2. Additional product images for lace-front products
    gen_product_image(
        f"{OUTPUT_DIR}/lace-front/13x4-bone-straight-black.webp",
        hair_color=(8, 6, 4),
        wave_type="bone_straight",
        bg_tone=(248, 242, 234),
        label_text="13×4 Bone Straight  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/lace-front/13x6-body-wave-black.webp",
        hair_color=(10, 8, 6),
        wave_type="body_wave",
        bg_tone=(246, 240, 232),
        label_text="13×6 Body Wave  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/lace-front/deep-wave-13x6-black.webp",
        hair_color=(8, 6, 4),
        wave_type="deep_wave",
        bg_tone=(245, 238, 228),
        label_text="13×6 Deep Wave  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/lace-front/pre-plucked-body-wave.webp",
        hair_color=(10, 8, 6),
        wave_type="body_wave",
        bg_tone=(247, 241, 233),
        label_text="Pre-Plucked Body Wave  ·  HD Lace"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/lace-front/kinky-straight-transparent.webp",
        hair_color=(6, 5, 3),
        wave_type="bone_straight",
        bg_tone=(246, 240, 231),
        label_text="Kinky Straight  ·  Transparent Lace"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/lace-front/loose-wave-lace-front.webp",
        hair_color=(9, 7, 5),
        wave_type="loose_wave",
        bg_tone=(248, 243, 235),
        label_text="Loose Wave  ·  13×4 Lace Front"
    )

    # 3. Closure wigs
    gen_product_image(
        f"{OUTPUT_DIR}/closure/4x4-silky-straight-black.webp",
        hair_color=(8, 6, 4),
        wave_type="bone_straight",
        bg_tone=(247, 241, 233),
        label_text="4×4 Closure  ·  Silky Straight"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/closure/5x5-water-wave-black.webp",
        hair_color=(10, 8, 6),
        wave_type="loose_wave",
        bg_tone=(245, 239, 230),
        label_text="5×5 Closure  ·  Water Wave"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/closure/2x6-bone-straight-black.webp",
        hair_color=(7, 5, 3),
        wave_type="bone_straight",
        bg_tone=(248, 242, 234),
        label_text="2×6 Closure  ·  Bone Straight"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/closure/deep-wave-closure.webp",
        hair_color=(9, 7, 5),
        wave_type="deep_wave",
        bg_tone=(245, 238, 229),
        label_text="Deep Wave Closure  ·  Natural Black"
    )

    # 4. Glueless
    gen_product_image(
        f"{OUTPUT_DIR}/glueless/wear-and-go-body-wave.webp",
        hair_color=(8, 6, 4),
        wave_type="body_wave",
        bg_tone=(248, 243, 236),
        label_text="Wear & Go  ·  Body Wave  ·  Glueless"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/glueless/bye-bye-knots-straight.webp",
        hair_color=(7, 5, 3),
        wave_type="bone_straight",
        bg_tone=(247, 241, 233),
        label_text="Bye Bye Knots  ·  Bone Straight"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/glueless/glueless-curly-wear-go.webp",
        hair_color=(9, 7, 5),
        wave_type="kinky_curly",
        bg_tone=(246, 240, 232),
        label_text="Glueless Curly  ·  Wear & Go"
    )

    # 5. Bob wigs
    gen_product_image(
        f"{OUTPUT_DIR}/bob/blunt-cut-sleek-bob-black.webp",
        hair_color=(6, 4, 2),
        wave_type="bone_straight",
        bg_tone=(248, 243, 236),
        label_text="Blunt Cut Sleek Bob  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/bob/asymmetrical-bob-black.webp",
        hair_color=(8, 6, 4),
        wave_type="bone_straight",
        bg_tone=(246, 240, 232),
        label_text="Asymmetrical Bob  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/bob/deep-wave-curly-bob-bangs.webp",
        hair_color=(10, 8, 6),
        wave_type="deep_wave",
        bg_tone=(245, 239, 230),
        label_text="Curly Bob  ·  Deep Wave  ·  With Bangs"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/bob/burgundy-bob-bangs.webp",
        hair_color=(80, 15, 30),
        wave_type="body_wave",
        bg_tone=(248, 240, 235),
        label_text="Burgundy Bob  ·  With Bangs"
    )

    # 6. Curly/wavy
    gen_product_image(
        f"{OUTPUT_DIR}/curly-wavy/deep-wave-natural-black.webp",
        hair_color=(8, 6, 4),
        wave_type="deep_wave",
        bg_tone=(246, 240, 232),
        label_text="Deep Wave  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/curly-wavy/water-wave-long.webp",
        hair_color=(10, 8, 6),
        wave_type="loose_wave",
        bg_tone=(247, 241, 233),
        label_text="Water Wave  ·  Long  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/curly-wavy/body-wave-long.webp",
        hair_color=(9, 7, 5),
        wave_type="body_wave",
        bg_tone=(248, 242, 234),
        label_text="Body Wave  ·  Long  ·  Natural Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/curly-wavy/kinky-curly-natural.webp",
        hair_color=(6, 4, 2),
        wave_type="kinky_curly",
        bg_tone=(246, 239, 230),
        label_text="Kinky Curly  ·  Natural Black"
    )

    # 7. Straight
    gen_product_image(
        f"{OUTPUT_DIR}/straight/bone-straight-glass-finish.webp",
        hair_color=(6, 4, 2),
        wave_type="bone_straight",
        bg_tone=(248, 244, 237),
        label_text="Bone Straight  ·  Glass Finish"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/straight/silky-straight-burmese.webp",
        hair_color=(8, 6, 4),
        wave_type="bone_straight",
        bg_tone=(247, 242, 234),
        label_text="Silky Straight  ·  Burmese Virgin Hair"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/straight/kinky-straight-black.webp",
        hair_color=(7, 5, 3),
        wave_type="bone_straight",
        bg_tone=(246, 240, 232),
        label_text="Kinky Straight  ·  Natural Black"
    )

    # 8. Colored wigs
    gen_product_image(
        f"{OUTPUT_DIR}/colored/613-platinum-blonde.webp",
        hair_color=(215, 195, 130),
        wave_type="body_wave",
        bg_tone=(248, 245, 238),
        label_text="613 Platinum Blonde  ·  Body Wave"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/colored/burgundy-99j-bone-straight.webp",
        hair_color=(85, 12, 28),
        wave_type="bone_straight",
        bg_tone=(248, 240, 235),
        label_text="99J Burgundy  ·  Bone Straight"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/colored/ginger-copper-loose-wave.webp",
        hair_color=(168, 78, 28),
        wave_type="loose_wave",
        bg_tone=(248, 242, 233),
        label_text="Ginger Copper  ·  Loose Wave"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/colored/honey-blonde-wave.webp",
        hair_color=(190, 145, 60),
        wave_type="body_wave",
        bg_tone=(248, 244, 234),
        label_text="Honey Blonde  ·  Body Wave"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/colored/chocolate-brown-silky.webp",
        hair_color=(90, 50, 20),
        wave_type="bone_straight",
        bg_tone=(246, 240, 231),
        label_text="Chocolate Brown  ·  Silky Straight"
    )

    # 9. Specialty
    gen_product_image(
        f"{OUTPUT_DIR}/specialty/360-full-lace-body-wave.webp",
        hair_color=(8, 6, 4),
        wave_type="body_wave",
        bg_tone=(247, 241, 233),
        label_text="360 Full Lace  ·  Body Wave"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/specialty/pixie-cut-jet-black.webp",
        hair_color=(4, 3, 2),
        wave_type="bone_straight",
        bg_tone=(248, 243, 236),
        label_text="Pixie Cut  ·  Jet Black"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/specialty/french-bangs-bone-straight.webp",
        hair_color=(7, 5, 3),
        wave_type="bone_straight",
        bg_tone=(247, 242, 234),
        label_text="French Bangs  ·  Bone Straight"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/specialty/headband-deep-wave.webp",
        hair_color=(9, 7, 5),
        wave_type="deep_wave",
        bg_tone=(246, 240, 232),
        label_text="Headband Wig  ·  Deep Wave"
    )

    # 10. Extensions
    gen_product_image(
        f"{OUTPUT_DIR}/extensions/bundles-body-wave-closure.webp",
        hair_color=(8, 6, 4),
        wave_type="body_wave",
        bg_tone=(247, 241, 233),
        label_text="Bundles + Closure  ·  Body Wave"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/extensions/bundles-bone-straight.webp",
        hair_color=(6, 4, 2),
        wave_type="bone_straight",
        bg_tone=(248, 243, 236),
        label_text="Bundles  ·  Bone Straight"
    )

    # 11. Category tiles
    gen_product_image(
        f"{OUTPUT_DIR}/categories/lace-front-wigs.webp",
        hair_color=(8, 6, 4),
        wave_type="body_wave",
        bg_tone=(247, 242, 234),
        label_text="Lace Front Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/closure-wigs.webp",
        hair_color=(9, 7, 5),
        wave_type="bone_straight",
        bg_tone=(248, 243, 235),
        label_text="Closure Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/glueless-wigs.webp",
        hair_color=(8, 6, 4),
        wave_type="body_wave",
        bg_tone=(247, 241, 233),
        label_text="Glueless Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/bob-wigs.webp",
        hair_color=(7, 5, 3),
        wave_type="bone_straight",
        bg_tone=(248, 242, 234),
        label_text="Bob Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/curly-wavy-wigs.webp",
        hair_color=(9, 7, 5),
        wave_type="deep_wave",
        bg_tone=(246, 240, 231),
        label_text="Curly & Wavy Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/straight-wigs.webp",
        hair_color=(6, 4, 2),
        wave_type="bone_straight",
        bg_tone=(248, 243, 236),
        label_text="Straight Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/colored-wigs.webp",
        hair_color=(185, 140, 55),
        wave_type="body_wave",
        bg_tone=(248, 244, 235),
        label_text="Colored Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/specialty-wigs.webp",
        hair_color=(8, 6, 4),
        wave_type="body_wave",
        bg_tone=(247, 241, 233),
        label_text="Specialty Wigs  ·  CrownLuxe"
    )
    gen_product_image(
        f"{OUTPUT_DIR}/categories/hair-extensions.webp",
        hair_color=(7, 5, 3),
        wave_type="loose_wave",
        bg_tone=(248, 242, 234),
        label_text="Hair Extensions  ·  CrownLuxe"
    )

    # 12. Collection banners
    for slug, label, hc, wt, bg_t in [
        ("new-arrivals", "New Arrivals  ·  CrownLuxe", (8, 6, 4), "body_wave", (247, 242, 234)),
        ("best-sellers", "Best Sellers  ·  CrownLuxe", (9, 7, 5), "loose_wave", (246, 241, 233)),
        ("trending-now", "Trending Now  ·  CrownLuxe", (185, 140, 55), "body_wave", (248, 244, 235)),
        ("premium-collection", "Premium Collection  ·  CrownLuxe", (6, 4, 2), "bone_straight", (248, 243, 236)),
        ("everyday-wigs", "Everyday Wigs  ·  CrownLuxe", (8, 6, 4), "body_wave", (247, 241, 233)),
        ("work-office-looks", "Work & Office  ·  CrownLuxe", (7, 5, 3), "bone_straight", (248, 242, 234)),
        ("wedding-occasion", "Wedding & Occasion  ·  CrownLuxe", (9, 7, 5), "loose_wave", (248, 243, 235)),
        ("beginner-friendly", "Beginner Friendly  ·  CrownLuxe", (8, 6, 4), "body_wave", (247, 242, 234)),
        ("affordable-finds", "Affordable Finds  ·  CrownLuxe", (7, 5, 3), "bone_straight", (246, 240, 232)),
        ("long-hair", "Long Hair  ·  CrownLuxe", (9, 7, 5), "body_wave", (248, 243, 235)),
        ("short-hair", "Short Hair  ·  CrownLuxe", (6, 4, 2), "bone_straight", (247, 241, 233)),
    ]:
        gen_product_image(
            f"{OUTPUT_DIR}/collections/{slug}.webp",
            hair_color=hc, wave_type=wt, bg_tone=bg_t, label_text=label
        )

    print("\n" + "─" * 60)
    count = len([f for r, d, files in os.walk(OUTPUT_DIR) for f in files if f.endswith(".webp")])
    print(f"Generated : {count} images total")
    print(f"Output    : {OUTPUT_DIR}")
    print("\nDone! The HD Lace Experience section images are ready.")


if __name__ == "__main__":
    main()
