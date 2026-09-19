"""Vector primitives for Mystery Flower Box illustrations.

Everything is emitted as plain SVG strings so the artwork stays editable and
renders identically to PNG via cairosvg. Palette is the brand palette from the
Mystery Flower Box brand guidelines (section 2.4).
"""

import math
import random

# --- Brand palette -----------------------------------------------------------
FORGET_ME_NOT = "#C5B7D8"
SUNFLOWER = "#FEC985"
TURF = "#9CA379"
GENUM = "#EDAD80"
PEONY = "#FF80C3"
HYDRANGEA = "#FFBBE2"
RASPBERRY = "#AF0E63"
CHARCOAL = "#414141"
WHITE = "#FFFFFF"
CREAM = "#FFF6FB"
BLUSH = "#FFE7F4"

BLOOMS = [PEONY, HYDRANGEA, SUNFLOWER, GENUM, FORGET_ME_NOT, RASPBERRY]
PASTELS = [HYDRANGEA, SUNFLOWER, FORGET_ME_NOT, GENUM, PEONY]


def tint(hex_colour, amount):
    """Mix a hex colour towards white. amount 0 = original, 1 = white."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r = round(r + (255 - r) * amount)
    g = round(g + (255 - g) * amount)
    b = round(b + (255 - b) * amount)
    return f"#{r:02X}{g:02X}{b:02X}"


def shade(hex_colour, amount):
    """Darken a hex colour. amount 0 = original, 1 = black."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02X%02X%02X" % (
        round(r * (1 - amount)), round(g * (1 - amount)), round(b * (1 - amount)))


# --- Low level shapes --------------------------------------------------------

def blob(cx, cy, r, fill, points=7, wobble=0.22, seed=0, opacity=1.0):
    """An organic pebble shape - the 'container edge' motif from the guidelines."""
    rnd = random.Random(seed)
    pts = []
    for i in range(points):
        a = (2 * math.pi * i) / points
        rr = r * (1 + rnd.uniform(-wobble, wobble))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    for i in range(points):
        p0 = pts[i]
        p1 = pts[(i + 1) % points]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d += f"Q {p0[0]:.1f} {p0[1]:.1f} {mx:.1f} {my:.1f} "
    d += "Z"
    op = "" if opacity >= 1 else f' opacity="{opacity}"'
    return f'<path d="{d}" fill="{fill}"{op}/>'


def petal(cx, cy, length, width, angle, fill, opacity=1.0):
    """A single rounded petal pointing along `angle` (degrees)."""
    op = "" if opacity >= 1 else f' opacity="{opacity}"'
    return (
        f'<ellipse cx="{cx:.1f}" cy="{cy - length / 2:.1f}" rx="{width / 2:.1f}" '
        f'ry="{length / 2:.1f}" fill="{fill}"{op} '
        f'transform="rotate({angle:.1f} {cx:.1f} {cy:.1f})"/>'
    )


# --- Flowers -----------------------------------------------------------------

def daisy(cx, cy, r, petal_colour=HYDRANGEA, centre=WHITE, petals=6, rot=0,
          centre_ratio=0.34):
    """The Mystery Flower Box signature daisy (matches the logo motif)."""
    out = []
    for i in range(petals):
        a = rot + (360 / petals) * i
        out.append(petal(cx, cy, r * 1.25, r * 0.92, a, petal_colour))
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * centre_ratio:.1f}" fill="{centre}"/>')
    return "".join(out)


def gerbera(cx, cy, r, outer=PEONY, inner=None, centre=CHARCOAL):
    inner = inner or tint(outer, 0.35)
    out = []
    for i in range(12):
        out.append(petal(cx, cy, r * 1.3, r * 0.46, i * 30, outer))
    for i in range(10):
        out.append(petal(cx, cy, r * 0.82, r * 0.34, i * 36 + 18, inner))
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.24:.1f}" fill="{centre}"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.12:.1f}" fill="{tint(centre, 0.4)}"/>')
    return "".join(out)


def rose(cx, cy, r, colour=PEONY):
    """A stylised spiral rose built from nested arcs."""
    out = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{colour}"/>']
    steps = 5
    for i in range(steps):
        rr = r * (1 - (i + 1) / (steps + 1))
        c = tint(colour, 0.12 * (i + 1))
        sweep = 1 if i % 2 == 0 else 0
        x0 = cx - rr
        x1 = cx + rr
        out.append(
            f'<path d="M {x0:.1f} {cy:.1f} A {rr:.1f} {rr:.1f} 0 1 {sweep} {x1:.1f} {cy:.1f} '
            f'A {rr * 0.86:.1f} {rr * 0.86:.1f} 0 0 {1 - sweep} {x0:.1f} {cy:.1f} Z" fill="{c}"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.16:.1f}" fill="{tint(colour, 0.6)}"/>')
    return "".join(out)


def tulip(cx, cy, size, colour=PEONY, stem_len=0, leaf=True):
    """Tulip head; optional stem drawn downwards."""
    w = size
    h = size * 1.15
    out = []
    if stem_len:
        out.append(stem(cx, cy + h * 0.32, stem_len, leaf=leaf))
    cup = (
        f'M {cx - w / 2:.1f} {cy - h * 0.18:.1f} '
        f'C {cx - w / 2:.1f} {cy + h * 0.55:.1f} {cx + w / 2:.1f} {cy + h * 0.55:.1f} '
        f'{cx + w / 2:.1f} {cy - h * 0.18:.1f} '
        f'C {cx + w * 0.42:.1f} {cy - h * 0.62:.1f} {cx + w * 0.16:.1f} {cy - h * 0.34:.1f} '
        f'{cx:.1f} {cy - h * 0.62:.1f} '
        f'C {cx - w * 0.16:.1f} {cy - h * 0.34:.1f} {cx - w * 0.42:.1f} {cy - h * 0.62:.1f} '
        f'{cx - w / 2:.1f} {cy - h * 0.18:.1f} Z'
    )
    out.append(f'<path d="{cup}" fill="{colour}"/>')
    out.append(
        f'<path d="M {cx:.1f} {cy - h * 0.5:.1f} C {cx - w * 0.2:.1f} {cy - h * 0.1:.1f} '
        f'{cx - w * 0.2:.1f} {cy + h * 0.2:.1f} {cx:.1f} {cy + h * 0.35:.1f}" '
        f'stroke="{tint(colour, 0.35)}" stroke-width="{w * 0.1:.1f}" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def stem(x, y, length, colour=TURF, width=None, leaf=True, bend=0.18):
    width = width or max(4, length * 0.045)
    x2 = x + length * bend * 0.4
    out = [
        f'<path d="M {x:.1f} {y:.1f} C {x + length * 0.14:.1f} {y + length * 0.35:.1f} '
        f'{x2 - length * 0.12:.1f} {y + length * 0.65:.1f} {x2:.1f} {y + length:.1f}" '
        f'stroke="{colour}" stroke-width="{width:.1f}" fill="none" stroke-linecap="round"/>'
    ]
    if leaf:
        ly = y + length * 0.52
        out.append(
            f'<path d="M {x + length * 0.06:.1f} {ly:.1f} '
            f'C {x + length * 0.34:.1f} {ly - length * 0.2:.1f} {x + length * 0.42:.1f} {ly + length * 0.04:.1f} '
            f'{x + length * 0.1:.1f} {ly + length * 0.16:.1f} Z" fill="{colour}"/>')
        ly2 = y + length * 0.74
        out.append(
            f'<path d="M {x2 - length * 0.03:.1f} {ly2:.1f} '
            f'C {x2 - length * 0.34:.1f} {ly2 - length * 0.18:.1f} {x2 - length * 0.4:.1f} {ly2 + length * 0.06:.1f} '
            f'{x2 - length * 0.06:.1f} {ly2 + length * 0.16:.1f} Z" fill="{shade(colour, 0.12)}"/>')
    return "".join(out)


def sprig(x, y, length, colour=TURF, leaves=7, rot=0):
    """Eucalyptus-style foliage sprig."""
    out = [f'<g transform="rotate({rot} {x:.1f} {y:.1f})">']
    out.append(f'<path d="M {x:.1f} {y:.1f} L {x:.1f} {y - length:.1f}" stroke="{colour}" '
               f'stroke-width="{max(3, length * 0.025):.1f}" stroke-linecap="round"/>')
    for i in range(leaves):
        t = (i + 1) / (leaves + 1)
        ly = y - length * t
        r = length * 0.115 * (1.15 - t * 0.45)
        side = -1 if i % 2 else 1
        out.append(f'<ellipse cx="{x + side * r * 1.15:.1f}" cy="{ly:.1f}" rx="{r * 1.25:.1f}" '
                   f'ry="{r * 0.82:.1f}" fill="{colour if i % 2 else shade(colour, 0.12)}" '
                   f'transform="rotate({side * -22} {x + side * r * 1.15:.1f} {ly:.1f})"/>')
    out.append("</g>")
    return "".join(out)


def potted_plant(cx, cy, size, pot=GENUM, leaf=TURF):
    """A house plant in a pot, sitting on the baseline `cy`."""
    w = size
    h = size * 0.62
    out = []
    for i, (dx, dy, r, rot) in enumerate([
            (-0.42, -0.52, 0.30, -34), (0.40, -0.55, 0.29, 30),
            (-0.16, -0.78, 0.30, -12), (0.20, -0.80, 0.28, 14), (0.02, -0.98, 0.26, 0)]):
        out.append(f'<ellipse cx="{cx + w * dx:.1f}" cy="{cy - h + size * dy:.1f}" '
                   f'rx="{size * r * 0.72:.1f}" ry="{size * r:.1f}" '
                   f'fill="{leaf if i % 2 == 0 else shade(leaf, 0.14)}" '
                   f'transform="rotate({rot} {cx + w * dx:.1f} {cy - h + size * dy:.1f})"/>')
    out.append(f'<path d="M {cx - w * 0.42:.1f} {cy - h:.1f} L {cx + w * 0.42:.1f} {cy - h:.1f} '
               f'L {cx + w * 0.3:.1f} {cy:.1f} L {cx - w * 0.3:.1f} {cy:.1f} Z" fill="{pot}"/>')
    out.append(f'<rect x="{cx - w * 0.47:.1f}" y="{cy - h - size * 0.1:.1f}" width="{w * 0.94:.1f}" '
               f'height="{size * 0.13:.1f}" rx="{size * 0.06:.1f}" fill="{shade(pot, 0.1)}"/>')
    return "".join(out)


# --- The box -----------------------------------------------------------------

def mystery_box(cx, baseline, width, body=PEONY, lid=None, label=True, open_lid=True):
    """The Mystery Flower Box itself, drawn front-on sitting on `baseline`.

    Returns (behind, front) markup so a bouquet can be sandwiched between the
    open lid flaps and the front face of the box.
    """
    lid = lid or tint(body, 0.22)
    w = width
    h = width * 0.60
    left = cx - w / 2
    top = baseline - h
    behind, front = [], []

    if open_lid:
        # two lid flaps folded outwards, drawn behind the bouquet
        for side in (-1, 1):
            x0 = cx + side * w * 0.5
            behind.append(
                f'<path d="M {x0:.1f} {top + h * 0.06:.1f} '
                f'L {x0 + side * w * 0.42:.1f} {top - h * 0.36:.1f} '
                f'L {x0 + side * w * 0.30:.1f} {top - h * 0.58:.1f} '
                f'L {x0 - side * w * 0.10:.1f} {top - h * 0.14:.1f} Z" fill="{lid}"/>')
    # dark interior visible above the front wall
    behind.append(f'<rect x="{left:.1f}" y="{top - h * 0.14:.1f}" width="{w:.1f}" '
                  f'height="{h * 0.3:.1f}" rx="{w * 0.03:.1f}" fill="{shade(body, 0.34)}"/>')

    front.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'rx="{w * 0.05:.1f}" fill="{body}"/>')
    # front rim highlight
    front.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h * 0.13:.1f}" '
                 f'rx="{w * 0.03:.1f}" fill="{tint(body, 0.22)}"/>')
    # soft shadow on the ground
    front.append(f'<ellipse cx="{cx:.1f}" cy="{baseline + h * 0.03:.1f}" rx="{w * 0.56:.1f}" '
                 f'ry="{h * 0.07:.1f}" fill="{shade(body, 0.3)}" opacity="0.18"/>')
    if label:
        ly = top + h * 0.60
        front.append(f'<circle cx="{cx:.1f}" cy="{ly:.1f}" r="{w * 0.155:.1f}" fill="{WHITE}" opacity="0.95"/>')
        front.append(daisy(cx, ly, w * 0.085, HYDRANGEA, WHITE, 6, 12))
    return "".join(behind), "".join(front)


def confetti(seed, count, x0, y0, x1, y1, colours=None, size=14):
    colours = colours or PASTELS
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        x = rnd.uniform(x0, x1)
        y = rnd.uniform(y0, y1)
        c = rnd.choice(colours)
        s = size * rnd.uniform(0.55, 1.35)
        kind = rnd.random()
        if kind < 0.45:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.4:.1f}" fill="{c}" opacity="0.85"/>')
        elif kind < 0.78:
            out.append(daisy(x, y, s * 0.55, c, WHITE, 5, rnd.uniform(0, 72)))
        else:
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s * 0.5:.1f}" height="{s * 0.9:.1f}" '
                       f'rx="{s * 0.24:.1f}" fill="{c}" opacity="0.8" '
                       f'transform="rotate({rnd.uniform(0, 180):.0f} {x:.1f} {y:.1f})"/>')
    return "".join(out)


def bouquet(cx, baseline, spread, seed=1, palette=None, include_foliage=True,
            heads=16, head_scale=1.0, width_ratio=1.25, height_ratio=1.0):
    """A burst of mixed blooms rising from a point - the money shot.

    `spread` is the radius of the dome of flowers above `baseline`.
    """
    palette = palette or BLOOMS
    rnd = random.Random(seed)
    out = []
    if include_foliage:
        for i in range(9):
            a = -78 + i * 19.5 + rnd.uniform(-7, 7)
            out.append(sprig(cx + rnd.uniform(-spread * 0.28, spread * 0.28), baseline,
                             spread * rnd.uniform(0.95, 1.3), TURF, 8, a))
    placed = []
    for i in range(heads):
        a = math.radians(-176 + (i + 0.5) * (172.0 / heads) + rnd.uniform(-6, 6))
        rad = spread * rnd.uniform(0.44, 1.0)
        hx = cx + math.cos(a) * rad * width_ratio
        hy = baseline + math.sin(a) * rad * height_ratio
        placed.append((hx, hy, rnd.uniform(0.78, 1.25) * head_scale,
                       rnd.choice(palette), rnd.random()))
    placed.sort(key=lambda h: h[1])
    for hx, hy, sc, col, kind in placed:
        out.append(f'<path d="M {hx:.1f} {hy:.1f} Q {(hx + cx) / 2:.1f} {(hy + baseline) / 2:.1f} '
                   f'{cx:.1f} {baseline:.1f}" stroke="{TURF}" fill="none" '
                   f'stroke-width="{spread * 0.026:.1f}" stroke-linecap="round"/>')
    for hx, hy, sc, col, kind in placed:
        r = spread * 0.19 * sc
        if kind < 0.30:
            out.append(daisy(hx, hy, r, col, WHITE if col != WHITE else SUNFLOWER, 6,
                             rnd.uniform(0, 60)))
        elif kind < 0.58:
            out.append(gerbera(hx, hy, r * 0.95, col))
        elif kind < 0.82:
            out.append(rose(hx, hy, r * 0.9, col))
        else:
            out.append(tulip(hx, hy - r * 0.2, r * 1.45, col))
    return "".join(out)


def vase(cx, baseline, width, colour=FORGET_ME_NOT):
    """A simple ceramic vase sitting on `baseline`."""
    w = width
    h = width * 1.35
    top = baseline - h
    neck = w * 0.34
    d = (f'M {cx - neck:.1f} {top:.1f} '
         f'C {cx - neck:.1f} {top + h * 0.22:.1f} {cx - w / 2:.1f} {top + h * 0.3:.1f} '
         f'{cx - w / 2:.1f} {top + h * 0.62:.1f} '
         f'C {cx - w / 2:.1f} {baseline:.1f} {cx + w / 2:.1f} {baseline:.1f} '
         f'{cx + w / 2:.1f} {top + h * 0.62:.1f} '
         f'C {cx + w / 2:.1f} {top + h * 0.3:.1f} {cx + neck:.1f} {top + h * 0.22:.1f} '
         f'{cx + neck:.1f} {top:.1f} Z')
    out = [f'<path d="{d}" fill="{colour}"/>']
    out.append(f'<path d="{d}" fill="{tint(colour, 0.35)}" opacity="0.5" '
               f'transform="translate({-w * 0.08:.1f},0) scale(0.55,1) '
               f'translate({cx * 0.818:.1f},0)"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{top:.1f}" rx="{neck:.1f}" ry="{neck * 0.3:.1f}" '
               f'fill="{shade(colour, 0.18)}"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{baseline:.1f}" rx="{w * 0.52:.1f}" ry="{h * 0.045:.1f}" '
               f'fill="{shade(colour, 0.3)}" opacity="0.16"/>')
    return "".join(out)


def svg(width, height, body, bg=None, extra_defs=""):
    b = f'<rect width="{width}" height="{height}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">{extra_defs}{b}{body}</svg>')
