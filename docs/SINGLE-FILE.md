# The single-file storefront

`dist/mystery-flower-box.html` is the whole site in one file — 29 pages, every
link working, every image embedded. Nothing is fetched from the internet, so it
works on a plane, on a locked-down laptop, or straight out of WhatsApp.

Roughly 920 KB. Send it as a document; the recipient taps it and it opens in
their browser.

## What works in it

- **All 29 pages** — home, shop, three product pages, how it works, gallery,
  find a box, subscriptions, corporate, partnerships, investors, competitions,
  refer a friend, FAQ, contact, about, news plus five articles, four policy
  pages, basket, and a 404.
- **The box builder** — pick a plan and the price updates, tick colours and
  varieties to leave out, hit the cap and the remaining options disable
  themselves with an explanation, switch on total mystery and everything below
  locks. The summary updates as you go.
- **A real basket** — add boxes with their exclusions attached, change
  quantities, remove lines, see the total. It survives a page reload.
- **Gallery filters, the stockist search, likes, copy-to-clipboard, the
  competition countdown** and every form, which validate and show a success
  state.

Checkout is the one thing that does not complete — it shows a note instead,
because there is no payment processor in an HTML file.

## Why it survives odd viewers

Routing is CSS `:target` first: every page is a `<div class="page">` in the
document, and `#shop` shows the shop because of a stylesheet rule, not
JavaScript. If a phone's in-app browser blocks scripts, every page and link
still works — you just lose the builder and basket. JavaScript is enhancement
on top, never the thing holding the site together.

Fonts are embedded as base64 WOFF2 (Baloo 2 and Roboto Slab, Latin subsets,
67 KB) so headings are right offline. Illustrations are one inline SVG sprite
referenced with `<use>`, so each drawing is stored once no matter how often it
appears. The logo is a data URI.

## Rebuilding it

```bash
python3 tools/build_singlefile.py            # → dist/mystery-flower-box.html
```

Content lives in `tools/site_content.py` — products, prices, reviews, gallery
entries, stockists, FAQs and articles are plain Python data, so copy changes
don't mean touching markup. Styling is `sitefile/app.css` (the theme's
stylesheet plus single-file additions) and behaviour is `sitefile/app.js`.

To check it after a change:

```bash
npm i -D playwright
node tools/verify_singlefile.js
```

That opens the file in Chromium, visits all 29 pages and asserts each renders
alone, drives the box builder and basket, exercises the filters and a form,
reports console errors, and writes desktop and mobile screenshots to
`dist/shots/`.

## How it relates to the Shopify build

Same brand system, same words, same illustrations — the Shopify theme in
`theme/` is the real shop. This file is for showing people the whole thing
without asking them to log into a preview or wait for the theme to be
published. When the two diverge, the Shopify theme is the source of truth.
