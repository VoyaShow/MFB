# Where the content lives

Everything on this site is editable without touching code. This is the map.

## Theme editor (Online Store → Themes → Customize)

Each page is built from sections, and each section's content is in its own
settings. Nothing is hard-coded into a template.

| Page | Sections you can edit |
| --- | --- |
| Home | Hero, marquee, three products, why MFB, how it works, your box your rules, customer reactions, gallery, review wall, what's blooming, Golden Ticket tracker, subscription plans, refer a friend, competition, partner offers, Instagram, latest news, investor stats, newsletter |
| Product | Price note, displayed rating and review count, and the box builder options — colours, varieties, household needs, clue options, and the maximum number of exclusions |
| Find a box | The stockist list (name, address, hours, stock level, map position) and the QR registration form |
| Corporate / Partnerships | The enquiry form fields themselves — add, remove or reorder questions as blocks |
| Customer gallery | Photos, names, locations, captions, categories, like and comment counts, and which box each links to |

## The box builder

On the product section you control exactly what customers may exclude:

- **Colours** — `Label:hex` pairs, comma separated. The hex drives the swatch.
- **Varieties** — a comma-separated list.
- **Household needs** — pet-friendly, low pollen, no strong scent, low light.
- **Clue options** — what a customer can ask to be told before delivery.
- **Maximum exclusions** — a cap on colours and on varieties, so a box can still
  be filled generously. When a customer hits the cap the remaining options
  disable themselves and a note explains why.

Everything a customer chooses is written into Shopify **line item properties**,
so it appears on the order in admin, in the packing slip and in the customer's
confirmation email:

- Flower colours to leave out
- Flower varieties to leave out
- Household needs
- Clue before delivery
- Mystery level (when "total mystery" is ticked)
- Preferred delivery date
- Gift message

Empty properties are removed before submit, so orders stay clean.

## Shopify admin

| Content | Where |
| --- | --- |
| Product titles, descriptions, prices, photos | Products |
| Card badge and short description | Product → Metafields (`mfb.flag`, `mfb.short_description`) |
| Purchase option small print | Variant → Metafields (`mfb.plan_note`, `mfb.boxes`) |
| Page copy that isn't in a section | Online Store → Pages |
| News articles | Online Store → Blog posts |
| Navigation | Online Store → Navigation (`mfb-main`, `mfb-footer`, `mfb-footer-commercial`) |

## Forms and where they go

| Form | Type | Lands in |
| --- | --- | --- |
| Newsletter (footer, homepage) | `customer` | Customers, tagged `newsletter` |
| Competition entry | `customer` | Customers, tagged `competition` |
| Corporate gifting enquiry | `contact` | Store contact email |
| Brand partnership enquiry | `contact` | Store contact email |
| Retail stockist enquiry | `contact` | Store contact email |
| QR box registration | `contact` | Store contact email |
| Gallery upload | `contact` | Store contact email |
| Contact | `contact` | Store contact email |

Contact forms go to the store's sender email (Settings → Notifications). Once
Klaviyo is connected, the customer forms feed straight into its flows via tags.
