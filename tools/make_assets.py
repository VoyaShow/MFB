#!/usr/bin/env python3
"""Generate every illustrated asset used by the Mystery Flower Box theme.

Usage:  python3 tools/make_assets.py [output_dir]

Outputs SVG sources (for crisp inline/decorative use) and PNG renders (for
Shopify product media, which does not accept SVG) into theme/assets/.
"""

import math
import os
import random
import sys

import cairosvg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flora import (  # noqa: E402
    BLOOMS, BLUSH, CHARCOAL, CREAM, FORGET_ME_NOT, GENUM, HYDRANGEA, PASTELS,
    PEONY, RASPBERRY, SUNFLOWER, TURF, WHITE, blob, bouquet, confetti, daisy,
    gerbera, mystery_box, potted_plant, rose, shade, sprig, stem, svg, tint,
    tulip, vase,
)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "theme", "assets")
os.makedirs(OUT, exist_ok=True)

WRITTEN = []


def write(name, markup, png_size=None):
    path = os.path.join(OUT, name + ".svg")
    with open(path, "w") as fh:
        fh.write(markup)
    WRITTEN.append(name + ".svg")
    if png_size:
        w, h = png_size
        cairosvg.svg2png(bytestring=markup.encode(), write_to=os.path.join(OUT, name + ".png"),
                         output_width=w, output_height=h)
        WRITTEN.append(name + ".png")


def soft_bg(w, h, seed, base=CREAM, colours=None):
    """Pastel blobs behind a scene."""
    colours = colours or [BLUSH, tint(SUNFLOWER, 0.5), tint(FORGET_ME_NOT, 0.5)]
    rnd = random.Random(seed)
    out = [f'<rect width="{w}" height="{h}" fill="{base}"/>']
    for i in range(3):
        out.append(blob(rnd.uniform(0, w), rnd.uniform(0, h), max(w, h) * rnd.uniform(0.28, 0.46),
                        colours[i % len(colours)], 8, 0.26, seed + i, 0.85))
    return "".join(out)


# ---------------------------------------------------------------------------
# 1. Product hero images
# ---------------------------------------------------------------------------

def product_flower_box(seed=7):
    w = h = 1400
    behind, front = mystery_box(w / 2, h * 0.94, 660, PEONY)
    out = [soft_bg(w, h, seed, CREAM, [BLUSH, tint(PEONY, 0.72), tint(SUNFLOWER, 0.6)])]
    out.append(confetti(seed + 1, 26, 60, 60, w - 60, h * 0.5, PASTELS, 34))
    out.append(behind)
    out.append(bouquet(w / 2, h * 0.72, 470, seed, BLOOMS, heads=20))
    out.append(front)
    return svg(w, h, "".join(out))


def product_flower_plant_box(seed=12):
    w = h = 1400
    behind, front = mystery_box(w / 2, h * 0.94, 660, FORGET_ME_NOT)
    out = [soft_bg(w, h, seed, CREAM, [tint(FORGET_ME_NOT, 0.55), BLUSH, tint(TURF, 0.66)])]
    out.append(confetti(seed + 1, 22, 60, 60, w - 60, h * 0.5, PASTELS, 32))
    out.append(behind)
    out.append(bouquet(w * 0.40, h * 0.72, 390, seed, [PEONY, HYDRANGEA, SUNFLOWER, RASPBERRY],
                       heads=13))
    out.append(potted_plant(w * 0.70, h * 0.72, 250, GENUM, TURF))
    out.append(front)
    return svg(w, h, "".join(out))


def product_plant_box(seed=21):
    w = h = 1400
    behind, front = mystery_box(w / 2, h * 0.94, 660, TURF)
    out = [soft_bg(w, h, seed, CREAM, [tint(TURF, 0.62), BLUSH, tint(SUNFLOWER, 0.6)])]
    out.append(confetti(seed + 1, 18, 60, 60, w - 60, h * 0.5,
                        [TURF, tint(TURF, 0.4), SUNFLOWER, HYDRANGEA], 30))
    out.append(behind)
    for i in range(7):
        out.append(sprig(w * 0.26 + i * w * 0.08, h * 0.72, 330, TURF, 8, -34 + i * 11))
    for x, y, s_, pot in [(w * 0.34, h * 0.70, 250, HYDRANGEA), (w * 0.66, h * 0.70, 240, SUNFLOWER),
                          (w * 0.50, h * 0.63, 290, GENUM)]:
        out.append(potted_plant(x, y, s_, pot, TURF))
    out.append(front)
    return svg(w, h, "".join(out))


def product_alt(seed, palette, box_colour):
    """A second angle: the box closed with a ribbon, a bunch resting beside it."""
    w = h = 1400
    rnd = random.Random(seed)
    behind, front = mystery_box(w * 0.60, h * 0.90, 620, box_colour, open_lid=False)
    out = [soft_bg(w, h, seed, CREAM, [BLUSH, tint(palette[0], 0.68), tint(SUNFLOWER, 0.55)])]
    out.append(confetti(seed + 3, 18, 60, 60, w - 60, h * 0.5, PASTELS, 30))
    out.append(bouquet(w * 0.30, h * 0.78, 300, seed + 1, palette, heads=13))
    out.append(front)
    out.append(f'<rect x="{w * 0.60 - 26:.0f}" y="{h * 0.90 - 620 * 0.60:.0f}" width="52" '
               f'height="{620 * 0.60:.0f}" fill="{tint(box_colour, 0.6)}" opacity="0.95"/>')
    out.append(daisy(w * 0.60, h * 0.90 - 620 * 0.60, 54, HYDRANGEA, WHITE, 6, 14))
    return svg(w, h, "".join(out))


# ---------------------------------------------------------------------------
# 2. Homepage hero collage
# ---------------------------------------------------------------------------

def hero_collage(seed=3):
    w, h = 1600, 1280
    rnd = random.Random(seed)
    behind, front = mystery_box(w / 2, h * 0.97, 700, PEONY)
    out = [f'<rect width="{w}" height="{h}" fill="{CREAM}"/>']
    out.append(blob(w * 0.5, h * 0.54, 570, tint(PEONY, 0.76), 9, 0.14, seed, 1))
    out.append(blob(w * 0.5, h * 0.54, 468, tint(HYDRANGEA, 0.4), 9, 0.11, seed + 4, 1))
    out.append(confetti(seed + 2, 30, 40, 40, w - 40, h * 0.7, PASTELS, 36))
    out.append(behind)
    out.append(bouquet(w / 2, h * 0.72, 440, seed + 9, BLOOMS, heads=19))
    out.append(front)
    for i in range(5):
        a = math.radians(200 + i * 34)
        out.append(daisy(w / 2 + math.cos(a) * 660, h * 0.52 + math.sin(a) * 480,
                         rnd.uniform(28, 46), rnd.choice(PASTELS), WHITE, 6, rnd.uniform(0, 60)))
    return svg(w, h, "".join(out))


# ---------------------------------------------------------------------------
# 3. Customer gallery tiles
# ---------------------------------------------------------------------------

SCENES = [
    ("vase", "Flowers on the kitchen table"),
    ("window", "Blooms on a windowsill"),
    ("held", "Unboxing on the doorstep"),
    ("desk", "Brightening up the desk"),
    ("party", "A birthday surprise"),
    ("plantshelf", "The plant shelf"),
]


def scene_vase(w, h, seed, palette):
    out = [soft_bg(w, h, seed, CREAM, [tint(palette[0], 0.7), BLUSH, tint(SUNFLOWER, 0.62)])]
    base = h * 0.82
    out.append(f'<rect x="0" y="{base:.0f}" width="{w}" height="{h - base:.0f}" fill="{tint(GENUM, 0.45)}"/>')
    out.append(bouquet(w / 2, base - h * 0.30, w * 0.27, seed + 3, palette, heads=15))
    out.append(vase(w / 2, base, w * 0.20, tint(FORGET_ME_NOT, 0.18)))
    return svg(w, h, "".join(out))


def scene_window(w, h, seed, palette):
    out = [f'<rect width="{w}" height="{h}" fill="{tint(FORGET_ME_NOT, 0.62)}"/>']
    out.append(f'<rect x="{w * 0.08:.0f}" y="{h * 0.06:.0f}" width="{w * 0.84:.0f}" '
               f'height="{h * 0.66:.0f}" rx="{w * 0.06:.0f}" fill="{tint(SUNFLOWER, 0.6)}"/>')
    out.append(f'<rect x="{w * 0.49:.0f}" y="{h * 0.06:.0f}" width="{w * 0.02:.0f}" '
               f'height="{h * 0.66:.0f}" fill="{WHITE}"/>')
    out.append(f'<rect x="{w * 0.08:.0f}" y="{h * 0.37:.0f}" width="{w * 0.84:.0f}" '
               f'height="{h * 0.02:.0f}" fill="{WHITE}"/>')
    out.append(f'<rect x="0" y="{h * 0.72:.0f}" width="{w}" height="{h * 0.1:.0f}" fill="{WHITE}"/>')
    out.append(bouquet(w * 0.34, h * 0.60, w * 0.19, seed, palette, heads=12))
    out.append(vase(w * 0.34, h * 0.72, w * 0.13, tint(PEONY, 0.42)))
    out.append(potted_plant(w * 0.72, h * 0.72, w * 0.2, GENUM, TURF))
    return svg(w, h, "".join(out))


def scene_held(w, h, seed, palette):
    behind, front = mystery_box(w / 2, h * 0.92, w * 0.52, PEONY)
    out = [soft_bg(w, h, seed, tint(PEONY, 0.8), [BLUSH, WHITE, tint(SUNFLOWER, 0.66)])]
    out.append(confetti(seed + 5, 20, 0, 0, w, h * 0.5, PASTELS, 32))
    out.append(behind)
    out.append(bouquet(w / 2, h * 0.68, w * 0.25, seed + 1, palette, heads=14))
    out.append(front)
    for side in (-1, 1):
        cx = w / 2 + side * w * 0.31
        out.append(f'<rect x="{cx - w * 0.065:.1f}" y="{h * 0.70:.1f}" width="{w * 0.13:.1f}" '
                   f'height="{h * 0.22:.1f}" rx="{w * 0.065:.1f}" fill="{tint(GENUM, 0.24)}"/>')
    return svg(w, h, "".join(out))


def scene_desk(w, h, seed, palette):
    out = [soft_bg(w, h, seed, CREAM, [tint(TURF, 0.66), BLUSH, tint(FORGET_ME_NOT, 0.6)])]
    base = h * 0.74
    out.append(f'<rect x="0" y="{base:.0f}" width="{w}" height="{h - base:.0f}" fill="{tint(GENUM, 0.38)}"/>')
    out.append(f'<rect x="{w * 0.08:.0f}" y="{base - h * 0.2:.0f}" width="{w * 0.34:.0f}" '
               f'height="{h * 0.2:.0f}" rx="{w * 0.02:.0f}" fill="{tint(CHARCOAL, 0.66)}"/>')
    out.append(f'<rect x="{w * 0.11:.0f}" y="{base - h * 0.17:.0f}" width="{w * 0.28:.0f}" '
               f'height="{h * 0.13:.0f}" rx="{w * 0.012:.0f}" fill="{tint(FORGET_ME_NOT, 0.5)}"/>')
    out.append(bouquet(w * 0.70, base - h * 0.22, w * 0.18, seed + 2, palette, heads=12))
    out.append(vase(w * 0.70, base, w * 0.13, tint(PEONY, 0.3)))
    return svg(w, h, "".join(out))


def scene_party(w, h, seed, palette):
    rnd = random.Random(seed)
    out = [f'<rect width="{w}" height="{h}" fill="{tint(SUNFLOWER, 0.52)}"/>']
    for i in range(9):
        x = w * (i + 0.5) / 9
        out.append(f'<path d="M {x:.0f} 0 L {x + w * 0.055:.0f} 0 L {x + w * 0.0275:.0f} {h * 0.1:.0f} Z" '
                   f'fill="{PASTELS[i % len(PASTELS)]}"/>')
    out.append(confetti(seed, 30, 0, h * 0.08, w, h * 0.6, PASTELS, 30))
    base = h * 0.8
    out.append(f'<rect x="0" y="{base:.0f}" width="{w}" height="{h - base:.0f}" fill="{WHITE}"/>')
    out.append(bouquet(w * 0.32, base - h * 0.28, w * 0.20, seed + 1, palette, heads=13))
    out.append(vase(w * 0.30, base, w * 0.13, tint(FORGET_ME_NOT, 0.2)))
    _b, _f = mystery_box(w * 0.72, base, w * 0.36, PEONY, open_lid=False)
    out.append(_f)
    return svg(w, h, "".join(out))


def scene_plantshelf(w, h, seed, palette):
    out = [soft_bg(w, h, seed, CREAM, [tint(TURF, 0.6), BLUSH, tint(SUNFLOWER, 0.6)])]
    for row, y in enumerate((h * 0.46, h * 0.82)):
        out.append(f'<rect x="{w * 0.06:.0f}" y="{y:.0f}" width="{w * 0.88:.0f}" '
                   f'height="{h * 0.035:.0f}" rx="{h * 0.017:.0f}" fill="{tint(GENUM, 0.3)}"/>')
        for i in range(3):
            out.append(potted_plant(w * (0.22 + i * 0.28), y, w * 0.14,
                                    [HYDRANGEA, SUNFLOWER, FORGET_ME_NOT][(i + row) % 3], TURF))
    return svg(w, h, "".join(out))


SCENE_FN = {
    "vase": scene_vase, "window": scene_window, "held": scene_held,
    "desk": scene_desk, "party": scene_party, "plantshelf": scene_plantshelf,
}


# ---------------------------------------------------------------------------
# 4. Small utility art
# ---------------------------------------------------------------------------

def stem_swatch(colour, seed):
    w = h = 600
    out = [f'<rect width="{w}" height="{h}" rx="48" fill="{tint(colour, 0.78)}"/>']
    out.append(stem(w / 2, h * 0.42, h * 0.5, TURF, 14, True))
    out.append(daisy(w / 2, h * 0.4, 118, colour, WHITE, 6, seed * 11))
    return svg(w, h, "".join(out))


def grower_portrait(seed, skin, shirt):
    w = h = 700
    rnd = random.Random(seed)
    out = [f'<rect width="{w}" height="{h}" fill="{tint(TURF, 0.72)}"/>']
    out.append(blob(w * 0.5, h * 0.55, 300, tint(SUNFLOWER, 0.5), 8, 0.2, seed, 1))
    for i in range(5):
        out.append(sprig(w * 0.12 + i * w * 0.2, h, h * 0.42, TURF, 7, rnd.uniform(-12, 12)))
    out.append(f'<path d="M {w * 0.22:.0f} {h:.0f} C {w * 0.22:.0f} {h * 0.66:.0f} '
               f'{w * 0.78:.0f} {h * 0.66:.0f} {w * 0.78:.0f} {h:.0f} Z" fill="{shirt}"/>')
    out.append(f'<circle cx="{w / 2:.0f}" cy="{h * 0.45:.0f}" r="{w * 0.16:.0f}" fill="{skin}"/>')
    out.append(f'<path d="M {w * 0.33:.0f} {h * 0.42:.0f} C {w * 0.36:.0f} {h * 0.24:.0f} '
               f'{w * 0.64:.0f} {h * 0.24:.0f} {w * 0.67:.0f} {h * 0.42:.0f} '
               f'C {w * 0.6:.0f} {h * 0.34:.0f} {w * 0.4:.0f} {h * 0.34:.0f} {w * 0.33:.0f} {h * 0.42:.0f} Z" '
               f'fill="{shade(skin, 0.55)}"/>')
    out.append(daisy(w * 0.68, h * 0.36, 34, PEONY, WHITE, 6, 10))
    return svg(w, h, "".join(out))


def favicon():
    return svg(64, 64, daisy(32, 32, 24, PEONY, WHITE, 6, 10) , bg=None)


def og_image():
    w, h = 1200, 630
    out = [f'<rect width="{w}" height="{h}" fill="{PEONY}"/>']
    out.append(blob(w * 0.18, h * 0.2, 300, tint(PEONY, 0.22), 8, 0.2, 5, 1))
    out.append(blob(w * 0.9, h * 0.85, 330, tint(PEONY, 0.18), 8, 0.2, 9, 1))
    out.append(confetti(4, 20, 0, 0, w, h, [WHITE, HYDRANGEA, SUNFLOWER], 34))
    out.append(bouquet(w * 0.78, h * 0.92, 250, 6, [WHITE, HYDRANGEA, SUNFLOWER, FORGET_ME_NOT]))
    out.append(f'<text x="80" y="300" font-family="Baloo 2, Fredoka, sans-serif" font-size="96" '
               f'font-weight="800" fill="{WHITE}">Mystery Flower Box</text>')
    out.append(f'<text x="84" y="376" font-family="Roboto Slab, serif" font-size="38" '
               f'fill="{WHITE}" opacity="0.92">Customers don’t pick flowers.</text>')
    out.append(f'<text x="84" y="428" font-family="Roboto Slab, serif" font-size="38" '
               f'fill="{WHITE}" opacity="0.92">They buy the surprise.</text>')
    return svg(w, h, "".join(out))


def pattern_tile():
    w = h = 400
    out = [f'<rect width="{w}" height="{h}" fill="none"/>']
    spots = [(100, 100, HYDRANGEA), (300, 180, SUNFLOWER), (180, 300, FORGET_ME_NOT),
             (340, 360, GENUM), (40, 250, PEONY)]
    for x, y, c in spots:
        out.append(daisy(x, y, 26, c, WHITE, 6, (x + y) % 60))
    return svg(w, h, "".join(out))


def blob_divider(colour):
    return svg(1440, 90, f'<path d="M0,60 C240,0 480,90 720,55 C960,20 1200,85 1440,35 L1440,90 L0,90 Z" '
                         f'fill="{colour}"/>')


# ---------------------------------------------------------------------------

def main():
    write("mfb-product-flower-box", product_flower_box(), (1400, 1400))
    write("mfb-product-flower-plant-box", product_flower_plant_box(), (1400, 1400))
    write("mfb-product-plant-box", product_plant_box(), (1400, 1400))
    write("mfb-product-flower-box-alt", product_alt(31, [PEONY, HYDRANGEA, SUNFLOWER, RASPBERRY], PEONY), (1400, 1400))
    write("mfb-product-flower-plant-box-alt", product_alt(33, [FORGET_ME_NOT, PEONY, SUNFLOWER, TURF], FORGET_ME_NOT), (1400, 1400))
    write("mfb-product-plant-box-alt", product_alt(35, [TURF, SUNFLOWER, GENUM, HYDRANGEA], TURF), (1400, 1400))

    write("mfb-hero", hero_collage(), (1600, 1280))
    write("mfb-og-image", og_image(), (1200, 630))
    write("mfb-favicon", favicon(), (64, 64))
    write("mfb-pattern", pattern_tile())
    write("mfb-divider-cream", blob_divider(CREAM))
    write("mfb-divider-white", blob_divider(WHITE))
    write("mfb-divider-blush", blob_divider(BLUSH))

    palettes = [
        [PEONY, HYDRANGEA, SUNFLOWER], [SUNFLOWER, GENUM, PEONY],
        [FORGET_ME_NOT, HYDRANGEA, PEONY], [RASPBERRY, PEONY, HYDRANGEA],
        [SUNFLOWER, TURF, HYDRANGEA], [GENUM, PEONY, FORGET_ME_NOT],
    ]
    idx = 0
    for round_no in range(2):
        for name, _label in SCENES:
            idx += 1
            fn = SCENE_FN[name]
            markup = fn(900, 900, 40 + idx * 7, palettes[idx % len(palettes)])
            write(f"mfb-gallery-{idx:02d}", markup, (900, 900))

    for i, (colour, label) in enumerate([
            (PEONY, "peony"), (SUNFLOWER, "sunflower"), (FORGET_ME_NOT, "forget-me-not"),
            (GENUM, "genum"), (HYDRANGEA, "hydrangea"), (TURF, "turf")]):
        write(f"mfb-blooming-{label}", stem_swatch(colour, i + 1), (600, 600))

    for i, (skin, shirt) in enumerate([
            ("#E8B48C", TURF), ("#8D5A3B", GENUM), ("#F2CBA6", FORGET_ME_NOT)]):
        write(f"mfb-grower-{i + 1}", grower_portrait(i * 13 + 2, skin, shirt), (700, 700))

    print(f"Wrote {len(WRITTEN)} files to {OUT}")


if __name__ == "__main__":
    main()
