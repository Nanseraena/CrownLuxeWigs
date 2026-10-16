"""
CrownLuxe Wigs Catalog Taxonomy Engine
Defines canonical taxonomies, alias normalization, and composable filter rules
for textures, colors, lengths, styles, constructions, and product types.
"""

from typing import List, Set

# 1. TEXTURE TAXONOMY
CANONICAL_TEXTURES = [
    "Bone Straight",
    "Silky Straight",
    "Yaki Straight",
    "Kinky Straight",
    "Body Wave",
    "Deep Wave",
    "Water Wave",
    "Loose Wave",
    "Curly",
    "Deep Curly",
    "Kinky Curly",
]

TEXTURE_MAP = {
    # Bone Straight (Strict)
    "bone straight": ["Bone Straight"],
    "bone-straight": ["Bone Straight"],
    "bonestraight": ["Bone Straight"],

    # Silky Straight
    "silky straight": ["Silky Straight"],
    "silky-straight": ["Silky Straight"],
    "silkystraight": ["Silky Straight"],

    # Yaki Straight
    "yaki straight": ["Yaki Straight"],
    "yaki-straight": ["Yaki Straight"],
    "yaki": ["Yaki Straight"],

    # Kinky Straight
    "kinky straight": ["Kinky Straight"],
    "kinky-straight": ["Kinky Straight"],

    # Broad Straight: Includes all straight textures, excludes wavy/curly
    "straight": ["Bone Straight", "Silky Straight", "Yaki Straight", "Kinky Straight"],

    # Body Wave
    "body wave": ["Body Wave"],
    "body-wave": ["Body Wave"],
    "bodywave": ["Body Wave"],

    # Deep Wave
    "deep wave": ["Deep Wave"],
    "deep-wave": ["Deep Wave"],
    "deepwave": ["Deep Wave"],

    # Water Wave
    "water wave": ["Water Wave"],
    "water-wave": ["Water Wave"],
    "waterwave": ["Water Wave"],

    # Loose Wave
    "loose wave": ["Loose Wave"],
    "loose-wave": ["Loose Wave"],
    "loosewave": ["Loose Wave"],

    # Broad Wavy
    "wavy": ["Body Wave", "Deep Wave", "Water Wave", "Loose Wave"],

    # Kinky Curly
    "kinky curly": ["Kinky Curly"],
    "kinky-curly": ["Kinky Curly"],

    # Deep Curly
    "deep curly": ["Deep Curly"],
    "deep-curly": ["Deep Curly"],

    # Broad Curly: Includes all curly textures, excludes straight/body wave
    "curly": ["Deep Curly", "Kinky Curly", "Curly"],
    "curls": ["Deep Curly", "Kinky Curly", "Curly"],
}

def resolve_textures(inputs: List[str]) -> List[str]:
    """
    Given a list of input texture strings (e.g. ['Bone Straight', 'curly']),
    returns the list of matching canonical textures in the database.
    """
    results: Set[str] = set()
    for raw in inputs:
        if not raw:
            continue
        cleaned = raw.strip().lower()
        if cleaned in TEXTURE_MAP:
            results.update(TEXTURE_MAP[cleaned])
        else:
            # Check for exact case-insensitive match against canonical textures
            matched = False
            for canonical in CANONICAL_TEXTURES:
                if cleaned == canonical.lower():
                    results.add(canonical)
                    matched = True
                    break
            if not matched:
                # Fallback to title-cased string if provided directly
                results.add(raw.strip())
    return sorted(list(results))


# 2. COLOR TAXONOMY
CANONICAL_COLORS = [
    "Natural Black",
    "Jet Black",
    "Natural Brown",
    "Chocolate Brown",
    "Honey Blonde",
    "Platinum Blonde",
    "Burgundy",
    "Ginger",
    "Copper",
    "Piano Highlights",
    "Ombre",
]

COLOR_MAP = {
    "black": ["Natural Black", "Jet Black"],
    "natural black": ["Natural Black"],
    "natural-black": ["Natural Black"],
    "1b": ["Natural Black"],
    "jet black": ["Jet Black"],
    "jet-black": ["Jet Black"],
    "#1": ["Jet Black"],
    "brown": ["Chocolate Brown", "Natural Brown"],
    "chocolate brown": ["Chocolate Brown"],
    "chocolate-brown": ["Chocolate Brown"],
    "#4": ["Chocolate Brown"],
    "mocha": ["Chocolate Brown"],
    "natural brown": ["Natural Brown"],
    "natural-brown": ["Natural Brown"],
    "#2": ["Natural Brown"],
    "blonde": ["Platinum Blonde", "Honey Blonde"],
    "platinum blonde": ["Platinum Blonde"],
    "platinum-blonde": ["Platinum Blonde"],
    "613": ["Platinum Blonde"],
    "#613": ["Platinum Blonde"],
    "honey blonde": ["Honey Blonde"],
    "honey-blonde": ["Honey Blonde"],
    "caramel": ["Honey Blonde"],
    "burgundy": ["Burgundy"],
    "99j": ["Burgundy"],
    "#99j": ["Burgundy"],
    "wine": ["Burgundy"],
    "ginger": ["Ginger"],
    "350": ["Ginger"],
    "#350": ["Ginger"],
    "copper": ["Copper"],
    "piano highlights": ["Piano Highlights"],
    "piano": ["Piano Highlights"],
    "p4/27": ["Piano Highlights"],
    "p4-27": ["Piano Highlights"],
    "highlights": ["Piano Highlights"],
    "balayage": ["Piano Highlights"],
    "ombre": ["Ombre"],
}

def resolve_colors(inputs: List[str]) -> List[str]:
    """
    Given a list of input color strings, resolves them to canonical variant colors.
    """
    results: Set[str] = set()
    for raw in inputs:
        if not raw:
            continue
        cleaned = raw.strip().lower().replace("_", " ")
        if cleaned in COLOR_MAP:
            results.update(COLOR_MAP[cleaned])
        else:
            for canonical in CANONICAL_COLORS:
                if cleaned == canonical.lower():
                    results.add(canonical)
                    break
            else:
                results.add(raw.strip())
    return sorted(list(results))


# 3. STYLE TAXONOMY
STYLE_MAP = {
    "bob": ["bob"],
    "bob wig": ["bob"],
    "bobs": ["bob"],
    "blunt bob": ["bob"],
    "layered bob": ["bob"],
    "asymmetrical bob": ["bob"],
    "curly bob": ["bob"],
    "pixie": ["pixie"],
    "pixie cut": ["pixie"],
    "bangs": ["bangs"],
    "fringe": ["bangs"],
    "french bangs": ["bangs"],
    "long": ["long"],
    "layered": ["layered"],
    "asymmetrical": ["asymmetrical"],
    "standard": ["standard"],
}

def resolve_styles(inputs: List[str]) -> List[str]:
    results: Set[str] = set()
    for raw in inputs:
        if not raw:
            continue
        cleaned = raw.strip().lower()
        if cleaned in STYLE_MAP:
            results.update(STYLE_MAP[cleaned])
        else:
            results.add(cleaned)
    return sorted(list(results))


# 4. PRODUCT TYPE TAXONOMY
PRODUCT_TYPE_MAP = {
    "wig": ["wig"],
    "wigs": ["wig"],
    "complete wig": ["wig"],
    "complete wigs": ["wig"],
    "bundles": ["bundles"],
    "hair bundles": ["bundles"],
    "bundle": ["bundles"],
    "weft": ["bundles"],
    "wefts": ["bundles"],
    "clip in": ["clip_in"],
    "clip-in": ["clip_in"],
    "clip-ins": ["clip_in"],
    "clip in extensions": ["clip_in"],
    "clip-in extensions": ["clip_in"],
    "tape in": ["tape_in"],
    "tape-in": ["tape_in"],
    "tape-ins": ["tape_in"],
    "tape in extensions": ["tape_in"],
    "tape-in extensions": ["tape_in"],
    "closure": ["closure_piece"],
    "closure piece": ["closure_piece"],
    "hd closure": ["closure_piece"],
    "closures": ["closure_piece"],
    "frontal": ["frontal_piece"],
    "frontal piece": ["frontal_piece"],
    "hd frontal": ["frontal_piece"],
    "frontals": ["frontal_piece"],
    "extensions": ["bundles", "clip_in", "tape_in", "closure_piece", "frontal_piece"],
    "hair extensions": ["bundles", "clip_in", "tape_in", "closure_piece", "frontal_piece"],
}

def resolve_product_types(inputs: List[str]) -> List[str]:
    results: Set[str] = set()
    for raw in inputs:
        if not raw:
            continue
        cleaned = raw.strip().lower()
        if cleaned in PRODUCT_TYPE_MAP:
            results.update(PRODUCT_TYPE_MAP[cleaned])
        else:
            results.add(cleaned)
    return sorted(list(results))


# 5. CONSTRUCTION TAXONOMY
CONSTRUCTION_MAP = {
    "lace front": ["lace_front"],
    "lace-front": ["lace_front"],
    "lace frontal": ["lace_front"],
    "frontal": ["lace_front"],
    "13x4": ["lace_front"],
    "13x6": ["lace_front"],
    "hd lace": ["lace_front"],
    "closure": ["closure"],
    "4x4": ["closure"],
    "5x5": ["closure"],
    "2x6": ["closure"],
    "glueless": ["glueless"],
    "wear and go": ["glueless"],
    "wear-and-go": ["glueless"],
    "3d dome cap": ["glueless"],
    "full lace": ["full_lace"],
    "360": ["full_lace"],
    "360 lace": ["full_lace"],
    "headband": ["headband"],
    "weft": ["weft"],
    "bundles": ["weft"],
    "clip in": ["clip_in"],
    "clip-in": ["clip_in"],
    "tape in": ["tape_in"],
    "tape-in": ["tape_in"],
}

def resolve_constructions(inputs: List[str]) -> List[str]:
    results: Set[str] = set()
    for raw in inputs:
        if not raw:
            continue
        cleaned = raw.strip().lower()
        if cleaned in CONSTRUCTION_MAP:
            results.update(CONSTRUCTION_MAP[cleaned])
        else:
            results.add(cleaned)
    return sorted(list(results))
