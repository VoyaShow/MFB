# Mystery Flower Box — Shopify storefront

A bespoke Shopify theme and store build for **Mystery Flower Box**, built to the
*Shopify Ecommerce Platform Technical Specification* and the *Mystery Flower Box
Brand Guidelines*.

> Customers don't pick flowers. They buy the surprise.

## What's in here

| Path | What it is |
| --- | --- |
| `theme/` | The complete Shopify theme (Liquid, CSS, JS, JSON templates, illustrated assets) |
| `tools/flora.py` | Vector primitives used to draw the brand illustrations |
| `tools/make_assets.py` | Regenerates every illustrated asset in `theme/assets/` |
| `docs/` | Brand reference, deployment notes and the content that was loaded into the store |

## The theme

A hand-built theme — no Dawn, no page builder — so every pixel follows the brand
guidelines. Highlights:

- **The box builder** (`sections/main-product.liquid`) — the heart of the site.
  Customers can't choose what goes in, but they can tell us what to leave out:
  colours, varieties, allergy and pet needs, how much of a clue they want before
  delivery, and a delivery date. Selections are written into Shopify line item
  properties so the packhouse sees them on the order.
- **Customer reactions & review wall** — unboxing reactions with video support,
  plus a verified review wall.
- **Customer gallery** — filterable masonry wall with likes, "Shop this box"
  links and an upload form.
- **Retail locator** — searchable stockist list with live stock levels, an
  interactive map and QR box registration.
- **Commercial funnels** — corporate gifting and brand partnership enquiry forms
  that capture volume, audience, timing, sample dimensions and budget.
- Subscriptions, loyalty, referrals, competitions, Golden Ticket tracker,
  What's Blooming Today, grower stories and an investor section.

Every section is editable in the Shopify theme editor — the MFB team can change
copy, imagery, stockists, gallery photos and reviews without touching code.

## Regenerating the artwork

```bash
pip install cairosvg pillow
python3 tools/make_assets.py
```

The illustrations are placeholders drawn in the brand palette. Swap them for real
photography through the theme editor — every image in every section has an
image picker.

## Deploying

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).
