# Brand reference

Taken from *Mystery Flower Box — Brand Guidelines* (created 07/26).

## Positioning

**We are:** fun, bold, colourful, viral, modern, sustainable, high value, social-first.
**We are not:** luxury, minimal, elegant florist, wedding-focused, corporate.

> We must stand apart from traditional flower brands.

**Mission:** Customers don't pick flowers. They buy the surprise.

## Core palette (2.4)

| Name | Hex | Used for |
| --- | --- | --- |
| Forget-Me-Not | `#C5B7D8` | Mist surfaces, the Flower & Plant Box |
| Sunflower | `#FEC985` | Sand surfaces, highlight pills |
| Turf | `#9CA379` | Meadow surfaces, the Plant Box, stems and foliage |
| Genum | `#EDAD80` | Warm accents, pots and tabletops |
| Peony | `#FF80C3` | Primary brand colour, buttons, the Flower Box |
| Hydrangea | `#FFBBE2` | Blush surfaces, soft accents |

## Extended palette

| Name | Hex | Used for |
| --- | --- | --- |
| Raspberry | `#AF0E63` | Headings, hover states, accent bands |
| Charcoal | `#414141` | Body text, footer |
| White | `#FFFFFF` | Cards and surfaces |

Tints may be used but never below 50% of a colour — this guarantees legibility
and keeps the brand cohesive. The theme's derived surfaces (`--cream`,
`--blush`, `--mist`, `--meadow`, `--sand`) all sit at or above that threshold.

## Typography (2.5)

| Role | Guideline font | Theme implementation |
| --- | --- | --- |
| H1 / headline | Round Bound | **Baloo 2 800** (Google Fonts) |
| H2 / sub-titles | Roboto Slab Bold | Roboto Slab 700 |
| Body copy | Roboto Slab Regular | Roboto Slab 400 |

Round Bound is a licensed font and is not available on Google Fonts, so the
theme ships with Baloo 2 — the closest freely-servable match for the bubbly,
handmade headline feel. To use the real thing, upload the Round Bound web font
files to the theme assets and swap `--font-display` in `assets/mfb.css`.

Sizing rules from the guidelines are respected: the call to action is never
smaller than 17pt with 20/10px padding.

## Graphics (2.6)

Organic "container edges" — soft blob shapes bleeding off the edge of a panel —
are the signature graphic device, alongside the six-petal daisy from the logo.
Both are used throughout `tools/flora.py` and the section styling.

## Logo

- `theme/assets/mfb-logo.png` — full colour, for white and light backgrounds
- `theme/assets/mfb-logo-white.png` — all white, for dark and Peony backgrounds

Minimum digital size is 300px wide; the header renders it at 175px by default,
so supply a dedicated small-format lockup if the logo needs to sit smaller.
Never recolour, skew, re-layout or add effects to the logo.
