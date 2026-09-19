# Deployment

## What is live now

Everything below is already on the Shopify store `e1p8ia-ak.myshopify.com`.

| Thing | Value |
| --- | --- |
| Theme | **Mystery Flower Box** — theme ID `190431527297`, currently **unpublished** |
| Preview | `https://e1p8ia-ak.myshopify.com/?preview_theme_id=190431527297` |
| Theme editor | `https://admin.shopify.com/store/e1p8ia-ak/themes/190431527297/editor` |

### The one step left for you

**Publish the theme.** The Shopify connector blocks `themePublish` and
`themeFilesDelete` as a safety measure, so the theme is deployed but not live.
Online Store → Themes → *Mystery Flower Box* → **Publish**.

Preview it first — everything renders from the preview link above without
publishing.

## How the theme was deployed

Theme files are pushed by `themeFilesUpsert`, with each file's body given as a
`URL` pointing at the raw file in this repository at a specific commit. Shopify
fetches each file itself, so binary assets never have to be re-encoded.

```graphql
mutation Up($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename checksumMd5 }
    userErrors { filename code message }
  }
}
```

```json
{
  "filename": "sections/hero.liquid",
  "body": {
    "type": "URL",
    "value": "https://raw.githubusercontent.com/VoyaShow/MFB/<commit>/theme/sections/hero.liquid"
  }
}
```

Three things to know if you push this way again:

1. **The mutation can report success and write nothing.** Always read the
   theme's files back and compare `checksumMd5` against the local files. Two
   section files silently failed on the first pass.
2. **`config/settings_data.json` only accepted a `TEXT` body**, not a URL one.
3. **Shopify validates schemas on upload.** A `link_list` setting may only use a
   reserved handle (`main-menu`, `footer`) as its `default`, `range` defaults
   must land on a step, and every block id in `settings_data.json` must be
   unique across the whole file. A violation fails the file, sometimes quietly.

Once the theme is published you can develop normally with the Shopify CLI:

```bash
shopify theme dev   --path theme --store e1p8ia-ak.myshopify.com
shopify theme check --path theme      # currently: 0 errors
shopify theme push  --path theme --theme 190431527297
```

## Catalogue

| Product | Handle | Price |
| --- | --- | --- |
| Mystery Flower Box | `mystery-flower-box` | £35 |
| Mystery Flower & Plant Box | `mystery-flower-and-plant-box` | £35 |
| Mystery Plant Box | `mystery-plant-box` | £35 |

Each has three purchase options on one "Delivery plan" option: a one-off box at
£35, a 4-box plan at £140 and an 8-box plan at £280 — £35 per box either way, so
"one clear price" holds. Inventory tracking is off, so nothing ever shows as
sold out by accident.

Collection: **Shop** (`/collections/shop`). The storefront only ever links to
this collection, never `/collections/all`.

### Metafields

| Owner | Key | Purpose |
| --- | --- | --- |
| Product | `mfb.flag` | Badge on the product card ("Most popular") |
| Product | `mfb.short_description` | Card and above-the-builder copy |
| Variant | `mfb.boxes` | How many boxes the option delivers, for the per-box price |
| Variant | `mfb.plan_note` | Small print under each purchase option |

## Pages

| Page | Handle | Template |
| --- | --- | --- |
| About Mystery Flower Box | `about-us` | `page.about` |
| How it works | `how-it-works` | `page.how-it-works` |
| Customer gallery | `customer-gallery` | `page.customer-gallery` |
| Find a box | `find-a-box` | `page.find-a-box` |
| Corporate gifting | `corporate` | `page.corporate` |
| Brand partnerships | `brand-partnerships` | `page.brand-partnerships` |
| Investors | `investors` | `page.investors` |
| Subscriptions | `subscriptions` | `page.subscriptions` |
| Competitions & Golden Tickets | `competitions` | `page.competitions` |
| Refer a friend | `refer-a-friend` | `page.refer-a-friend` |
| FAQ | `faq` | `page.faq` |
| Contact | `contact` | `page.contact` |
| Delivery & returns | `delivery-and-returns` | default |
| Terms & conditions | `terms-and-conditions` | default |
| Privacy notice | `privacy-notice` | default |
| Flower care | `flower-care` | default |

Blog: **News** (`/blogs/news`), five articles published.

Menus: `mfb-main`, `mfb-footer`, `mfb-footer-commercial`.

## Important: this store already belongs to another brand

`e1p8ia-ak.myshopify.com` is running **DutchFlowerDeals** — 28 live products, its
own pages, menus and published theme. Nothing belonging to it was changed.

That constrained a few decisions, all reversible:

- MFB uses its own menus (`mfb-*`) rather than editing `main-menu` and `footer`
- `about`, `terms`, `privacy` and `delivery` were taken, so MFB's equivalents
  are `about-us`, `terms-and-conditions`, `privacy-notice` and
  `delivery-and-returns`
- `/collections/all` would list DutchFlowerDeals stock, so every link points at
  `/collections/shop` instead
- The DutchFlowerDeals theme's leftover sections could not be deleted (the
  connector blocks it), so they were overwritten with inert stubs that declare no
  presets and therefore never appear in the theme editor

**Mystery Flower Box should have its own Shopify store.** On a clean store the
handles are free, `/collections/all` is safe, the main menu is yours, and
publishing this theme doesn't take another brand offline. Everything in
`theme/` transfers as-is; only the menu handles and page handles would change.

## Still to do before launch

1. **Publish the theme** (above).
2. **Real photography.** Every image in the build is an illustration generated
   by `tools/make_assets.py`, in the brand palette, as a stand-in. Each one sits
   behind an image picker in the theme editor — swap them without touching code.
   Product photos go on the products themselves in Shopify admin.
3. **Real recurring subscriptions.** The 4- and 8-box plans are prepaid bundles
   that check out natively today. True weekly/fortnightly recurring billing with
   customer-managed pause and skip needs a subscription app (Recharge or Shopify
   Subscriptions), which also requires Shopify Payments. Once installed, add
   selling plans to the three products and the purchase options on the box
   builder pick them up.
4. **Currency.** The specification prices boxes at €35; the store is set to GBP,
   so everything is £35. If MFB sells into the eurozone, add a market in Shopify
   and set the euro price there.
5. **Apps from the specification** that are not installed: Klaviyo, Judge.me,
   Trustpilot, LoyaltyLion, ReferralCandy, GA4 and GTM. The sections that will
   eventually be driven by them (reviews, gallery, loyalty, referrals) are built
   and editable by hand in the meantime, so the site is complete without them.
6. **Fill in the real details** the placeholders stand in for: social URLs in the
   footer, the stockist list on Find a Box, the competition closing date, and
   `hello@mysteryflowerbox.com` if that is not the address you want.
