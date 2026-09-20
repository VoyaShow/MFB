# -*- coding: utf-8 -*-
"""All copy and data for the single-file Mystery Flower Box storefront.

Kept apart from the builder so the words can be edited without touching markup.
"""

BRAND = {
    "name": "Mystery Flower Box",
    "tagline": "Customers don’t pick flowers. They buy the surprise.",
    "email": "hello@mysteryflowerbox.com",
    "instagram": "@mysteryflowerbox",
    "price": 35.00,
}

PLANS_FORTNIGHT = [
    {"id": "one-off", "label": "One-off box", "price": 35.00, "boxes": 1,
     "note": "One surprise box, delivered on your chosen date"},
    {"id": "four", "label": "4 boxes, one a fortnight", "price": 140.00, "boxes": 4,
     "note": "Two months of surprises, paid once. Skip or reschedule any box."},
    {"id": "eight", "label": "8 boxes, one a fortnight", "price": 280.00, "boxes": 8,
     "note": "Four months of surprises, paid once. Our best-value plan."},
]

PLANS_MONTH = [
    {"id": "one-off", "label": "One-off box", "price": 35.00, "boxes": 1,
     "note": "One surprise box of plants, delivered on your chosen date"},
    {"id": "four", "label": "4 boxes, one a month", "price": 140.00, "boxes": 4,
     "note": "Four months of plants, paid once. Skip or reschedule any box."},
    {"id": "eight", "label": "8 boxes, one a month", "price": 280.00, "boxes": 8,
     "note": "Eight months of plants, paid once. Our best-value plan."},
]

PRODUCTS = [
    {
        "slug": "mystery-flower-box",
        "title": "Mystery Flower Box",
        "flag": "Most popular",
        "art": "art-product-flower-box",
        "art_alt": "art-product-flower-box-alt",
        "short": "15–25 stems of rescued seasonal blooms. You set the no-list, we keep the rest a secret.",
        "rating": 4.8,
        "reviews": "1,284",
        "plans": PLANS_FORTNIGHT,
        "body": [
            "A generous box of surplus Dutch blooms, packed the morning it leaves us. "
            "You don’t choose what’s inside — that’s the surprise — but you can tell us "
            "exactly what to leave out.",
            "Expect 15–25 stems of seasonal flowers, a flower care card, and sometimes a "
            "partner treat. One in every 250 boxes hides a Golden Ticket.",
        ],
        "bullets": [
            "Rescued from Dutch growers, never wasted",
            "Free UK delivery, next-day dispatch before 2pm",
            "7-day freshness promise",
            "Set your no-list: colours, varieties, allergies, pets",
        ],
    },
    {
        "slug": "mystery-flower-and-plant-box",
        "title": "Mystery Flower &amp; Plant Box",
        "plain_title": "Mystery Flower & Plant Box",
        "flag": "Best of both",
        "art": "art-product-flower-plant-box",
        "art_alt": "art-product-flower-plant-box-alt",
        "short": "Cut stems for the table plus a living plant that stays. Same price, twice the life.",
        "rating": 4.8,
        "reviews": "612",
        "plans": PLANS_FORTNIGHT,
        "body": [
            "The best of both: a surprise mix of cut flowers for the table and a living "
            "plant that sticks around long after the blooms have gone.",
            "Expect 10–18 stems plus one or two potted plants, a care card for each, and "
            "sometimes a partner treat. One in every 250 boxes hides a Golden Ticket.",
        ],
        "bullets": [
            "Rescued from Dutch growers, never wasted",
            "Free UK delivery, next-day dispatch before 2pm",
            "7-day freshness promise on the cut stems",
            "Set your no-list: colours, varieties, allergies, pets",
        ],
    },
    {
        "slug": "mystery-plant-box",
        "title": "Mystery Plant Box",
        "flag": "Lasts for years",
        "art": "art-product-plant-box",
        "art_alt": "art-product-plant-box-alt",
        "short": "Two to four surprise house plants, peat-free and ready to live on your shelf for years.",
        "rating": 4.7,
        "reviews": "428",
        "plans": PLANS_MONTH,
        "body": [
            "A surprise selection of house plants, grown slowly under Dutch glass and "
            "rescued before they went to waste. No cut stems — just green things that keep going.",
            "Expect two to four potted plants with a care card for each, and sometimes a "
            "partner treat. One in every 250 boxes hides a Golden Ticket.",
        ],
        "bullets": [
            "Rescued from Dutch growers, never wasted",
            "Free UK delivery, next-day dispatch before 2pm",
            "Grown in peat-free compost",
            "Tick <em>pet-friendly only</em> on the box builder and we’ll pack around it",
        ],
    },
]

BUILDER = {
    "colours": [
        ("Red", "#D5344B"), ("Pink", "#FF80C3"), ("Orange", "#EDAD80"),
        ("Yellow", "#FEC985"), ("White", "#FFFFFF"), ("Purple", "#C5B7D8"),
        ("Green", "#9CA379"),
    ],
    "varieties": ["Roses", "Lilies", "Chrysanthemums", "Carnations", "Tulips",
                  "Gerberas", "Alstroemeria", "Heavy foliage", "Dried stems"],
    "care": ["Pet-friendly only", "Low pollen / allergy aware", "No strong scent", "Low light home"],
    "clues": ["No clue — total surprise", "Tell me the main colour", "Tell me one variety"],
    "max_colours": 3,
    "max_varieties": 4,
}

PRODUCT_FAQ = [
    ("What’s inside?",
     "A generous surprise mix of seasonal stems, rescued from Dutch growers the day "
     "before it reaches you. Expect 15–25 stems depending on variety, plus a flower care "
     "card and — sometimes — a partner treat or a Golden Ticket."),
    ("Delivery &amp; freshness",
     "Free UK delivery. Order before 2pm for next-day dispatch, Monday to Friday. Every "
     "box travels in water-retaining wrap and carries our 7-day freshness promise — if it "
     "isn’t perfect, we replace it."),
    ("How exclusions work",
     "You can’t choose what goes in — that’s the surprise. But you can tell us what to "
     "leave out: up to three colours and four varieties, plus household needs like "
     "pet-friendly or low pollen. Our packhouse sees your list before your box is filled."),
    ("Looking after your flowers",
     "Trim 2cm off each stem at an angle, use the flower food provided, keep out of direct "
     "sunlight and change the water every two days. The full guide is on our flower care page."),
]

WHY = [
    ("recycle", "Surplus, rescued",
     "We buy what Dutch growers can’t sell through the usual channels, so beautiful stems never go to waste."),
    ("sparkle", "Twice the flowers",
     "Because nobody is paying for a florist’s window, your £35 buys far more than £35 usually does."),
    ("heart", "Your rules respected",
     "Allergic to lilies? Cat at home? Can’t stand orange? Tick it once and our packhouse works around it."),
    ("gift", "Always a surprise",
     "Never the same box twice — and one in every 250 hides a Golden Ticket."),
]

STEPS = [
    ("Pick your box", "Flowers, plants, or both. Every box is £35."),
    ("Set your no-list", "Tell us the colours and varieties to leave out — everything else stays secret."),
    ("We pack it fresh", "Our growers fill your box the morning it leaves us, working around your list."),
    ("Open the lid", "Film the moment, tag us, and you could land in the gallery — and the Golden Ticket draw."),
]

EXCLUSION_CHIPS = [
    ("No lilies", None), ("No orange", "#EDAD80"), ("No red", "#D5344B"),
    ("No chrysanthemums", None), ("Pet-friendly only", None),
    ("Low pollen", None), ("No strong scent", None),
]

REACTIONS = [
    {"emoji": "😍", "rating": 5, "art": "art-gallery-03",
     "quote": "I actually squealed. My husband now thinks I’ve lost it — worth every penny.",
     "name": "Sophie M.", "where": "Manchester", "box": "Mystery Flower Box"},
    {"emoji": "🤯", "rating": 5, "art": "art-gallery-09",
     "quote": "I ticked ‘no lilies’ because of the cat and they got it spot on. Twenty-three stems for £35.",
     "name": "Dan &amp; Priya", "where": "Bristol", "box": "Mystery Flower &amp; Plant Box"},
    {"emoji": "🥹", "rating": 5, "art": "art-gallery-01",
     "quote": "Sent one to my mum for no reason. She rang me crying. Now it’s a monthly thing.",
     "name": "Leanne K.", "where": "Glasgow", "box": "Mystery Flower Box"},
]

REVIEWS = [
    (5, "Better than the florist down the road",
     "Twice the stems for half the money and I genuinely look forward to the delivery. The ‘leave out’ list is a brilliant touch.",
     "Rachel T.", "2 weeks ago"),
    (5, "They actually read the exclusions",
     "I’m allergic to lilies and asked for none. Six boxes in, not a single lily. That’s all I needed.",
     "Gareth P.", "1 month ago"),
    (4, "The fun is the not knowing",
     "One box was a bit green-heavy for me, but the next two were stunning. That’s the deal and I’m here for it.",
     "Meera S.", "3 weeks ago"),
    (5, "Lasted eleven days",
     "Arrived cold, wrapped properly, and still going nearly two weeks later. Cannot fault it.",
     "Jon H.", "5 days ago"),
    (5, "Best £35 in my month",
     "It’s become the thing I look forward to. Cheaper than a takeaway and it lasts a fortnight.",
     "Bex L.", "1 week ago"),
    (5, "Gifted four, kept one",
     "Sent them to my whole team. Three of them have subscribed since.",
     "Anna D.", "2 months ago"),
]

GALLERY = [
    ("Jess", "Leeds", "Third box and still smiling", "In the home", "Mystery Flower Box", "412", "23"),
    ("Marcus", "Cardiff", "Kitchen window upgrade", "In the home", "Mystery Plant Box", "298", "11"),
    ("Amira", "London", "Doorstep unboxing, 8am", "Unboxings", "Mystery Flower Box", "1,204", "88"),
    ("Tom", "Sheffield", "Desk therapy", "In the home", "Mystery Flower Box", "176", "9"),
    ("Nadia", "Belfast", "Her 40th, and she had no idea", "Occasions", "Mystery Flower &amp; Plant Box", "846", "51"),
    ("Ollie", "Brighton", "The shelf is officially full", "Plants", "Mystery Plant Box", "523", "34"),
    ("Priya", "Birmingham", "Golden Ticket! A year of boxes", "Golden Tickets", "Mystery Flower Box", "2,108", "167"),
    ("Cara", "Norwich", "Mother’s Day sorted", "Occasions", "Mystery Flower Box", "689", "40"),
    ("Ben", "Exeter", "Anniversary, 11 years", "Occasions", "Mystery Flower Box", "331", "18"),
    ("Hannah", "York", "The cat approves (pet-safe box)", "In the home", "Mystery Plant Box", "907", "62"),
    ("Ola", "Nottingham", "Unboxing with the kids", "Unboxings", "Mystery Flower &amp; Plant Box", "455", "27"),
    ("Ruth", "Aberdeen", "Second Golden Ticket in our office!", "Golden Tickets", "Mystery Flower Box", "1,533", "104"),
]

GALLERY_FILTERS = ["Unboxings", "In the home", "Occasions", "Plants", "Golden Tickets"]

BLOOMING = [
    ("art-blooming-peony", "Avalanche roses", "Aalsmeer · packed Tuesday"),
    ("art-blooming-sunflower", "Strong Gold tulips", "Westland · packed Monday"),
    ("art-blooming-forget-me-not", "Lisianthus", "Rijnsburg · packed Wednesday"),
    ("art-blooming-genum", "Germini mix", "Naaldwijk · packed today"),
    ("art-blooming-turf", "Eucalyptus cinerea", "Foliage · every box"),
    ("art-blooming-hydrangea", "Alstroemeria", "Aalsmeer · packed Thursday"),
]

GOLDEN = [
    ("🎟️", "A year of free boxes", "Priya, Birmingham — last Friday"),
    ("🚐", "Grower tour for two, Holland", "Sam, Newcastle — this month"),
    ("💐", "Limited-edition peony box", "Kelly, Southampton — last week"),
    ("🏨", "Weekend break for two", "Ruth, Aberdeen — two weeks ago"),
]

PLAN_CARDS = [
    ("Weekly", "£35", "per box, every week",
     ["Free UK delivery", "Pause or skip any time", "Double loyalty points",
      "For people who really love flowers"], False),
    ("Fortnightly", "£35", "per box, every two weeks",
     ["Free UK delivery", "Pause or skip any time", "Double loyalty points",
      "Most popular rhythm for a busy house"], True),
    ("Monthly", "£35", "per box, every month",
     ["Free UK delivery", "Pause or skip any time", "Double loyalty points",
      "A monthly treat, no commitment"], False),
    ("Gift a plan", "From £140", "4, 8 or 12 boxes, prepaid",
     ["Delivered to them, billed to you", "Personal message in the first box",
      "Nothing for them to cancel", "Perfect for birthdays and thank-yous"], False),
]

STOCKISTS = [
    ("Greenfields Supermarket", "14 Briggate", "Leeds", "LS1 6BR",
     "Mon–Sat 7am–10pm · Sun 10am–4pm", "high", 52, 38),
    ("Northside Food Hall", "3 Market Street", "Manchester", "M1 1PT",
     "Mon–Sun 8am–9pm", "low", 44, 45),
    ("Riverside Grocers", "88 Queen Street", "Cardiff", "CF10 2GB",
     "Mon–Sat 8am–8pm · Sun 11am–5pm", "high", 30, 66),
    ("The Corner Market", "201 Byres Road", "Glasgow", "G12 8UD",
     "Mon–Sun 7am–11pm", "out", 34, 22),
    ("Eastgate Fresh", "5 Gentleman’s Walk", "Norwich", "NR2 1NA",
     "Mon–Sat 8am–7pm", "high", 76, 52),
    ("Harbour Stores", "22 North Street", "Brighton", "BN1 1EB",
     "Mon–Sun 8am–9pm", "high", 63, 78),
    ("Cathedral Provisions", "9 Grainger Street", "Newcastle", "NE1 5JE",
     "Mon–Sat 7am–9pm", "low", 50, 25),
    ("Southbank Food Co.", "44 Lower Marsh", "London", "SE1 7RG",
     "Mon–Sun 7am–10pm", "high", 64, 68),
]

GROWERS = [
    ("art-grower-1", "De Vries Family", "Aalsmeer, NL",
     "Third-generation rose growers. What doesn’t meet the auction grade goes straight into your box."),
    ("art-grower-2", "Kwekerij Bloem", "Westland, NL",
     "Tulips by the million every spring. We take the surplus the day it’s cut."),
    ("art-grower-3", "Van Dijk Planten", "Rijnsburg, NL",
     "House plants grown slowly, in peat-free compost, under Dutch glass."),
]

PARTNER_OFFERS = [
    ("Sampling", "Product sampling",
     "Your sample in every box for a chosen week, with redemption tracked by QR code."),
    ("Advertising", "Printed inserts",
     "A beautifully printed card in the box, plus placement on the partner offers page."),
    ("Sponsorship", "Sponsored Golden Ticket",
     "Attach your brand to the moment someone wins something brilliant."),
    ("Competitions", "Co-branded competition",
     "We run it, you supply the prize, and we share the opted-in entries."),
]

INVESTOR_STATS = [
    ("1.2m", "stems rescued to date"),
    ("62%", "repeat purchase rate"),
    ("40k+", "first-party records"),
    ("4.8", "average review score"),
]

PARTNER_STATS = [
    ("50k+", "boxes opened each month"),
    ("40k+", "opted-in first-party records"),
    ("62%", "repeat purchase rate"),
    ("1 in 4", "share their unboxing"),
]

ARTICLES = [
    {
        "slug": "why-we-wont-let-you-pick-your-flowers",
        "title": "Why we won’t let you pick your flowers",
        "date": "1 September 2026",
        "tag": "Behind the box",
        "art": "art-product-flower-box",
        "summary": "It looks like a limitation. It’s the reason your box costs £35 and arrives twice the size you expected.",
        "body": [
            ("p", "Every week somebody emails to ask whether they can order “just the pink ones”. "
                  "The answer is no, and it isn’t stubbornness — it’s the whole business model."),
            ("h2", "Where the flowers come from"),
            ("p", "Dutch growers produce more flowers than the auction can sell. Not bad flowers: "
                  "perfect stems that arrived on a Tuesday when buyers wanted Thursday, or in a "
                  "quantity nobody had a contract for. Historically that stock was composted."),
            ("p", "We buy it. But we buy what exists that morning, not what a customer picked from a "
                  "menu three days earlier. The moment you let people choose, you need predictable "
                  "stock — and predictable stock means contracts, forecasting, and paying market rate. "
                  "That’s a florist. Florists are lovely. They’re also three times the price."),
            ("h2", "What you do get to choose"),
            ("p", "Plenty, actually. On the box builder you can tell us up to three colours and four "
                  "varieties to leave out, flag a cat in the house or an allergy in the family, and "
                  "decide whether you’d like a clue the day before delivery or complete silence until "
                  "the lid comes off."),
            ("p", "That list goes to the packhouse before your box is filled. It isn’t a suggestion — "
                  "it’s a rule we pack to."),
            ("h2", "The part we didn’t expect"),
            ("p", "When we started, we assumed the surprise was a compromise customers tolerated for "
                  "the price. It turned out to be the thing they liked most. People film the unboxing. "
                  "They text photos to their mum. They tell us the Tuesday delivery is the best part of "
                  "their week, and they’d be disappointed if they already knew what was in it."),
            ("p", "Customers don’t pick flowers. They buy the surprise."),
        ],
    },
    {
        "slug": "inside-the-packhouse",
        "title": "Inside the packhouse: how your no-list actually works",
        "date": "20 August 2026",
        "tag": "Behind the box",
        "art": "art-product-flower-plant-box",
        "summary": "Six thousand boxes a day, every one packed to a different set of rules. Here’s how we keep track.",
        "body": [
            ("p", "The most common question after “can I pick my flowers” is “do you actually read the "
                  "exclusions?” Fair question. Here’s what happens between you clicking add to basket "
                  "and a box landing on your doormat."),
            ("h2", "5am: the buy"),
            ("p", "Our buyers are at the auction before most of the country is awake, looking at what "
                  "the growers couldn’t sell. They’re buying volume and quality, not a specific list."),
            ("h2", "7am: the day’s palette"),
            ("p", "By the time the stock reaches the packhouse we know exactly what we have: how many "
                  "roses, what colours, how much foliage. That becomes the day’s palette, and it’s "
                  "published on the What’s Blooming Today feed — deliberately without telling anyone "
                  "which stems go in which box."),
            ("h2", "9am: the run sheet"),
            ("p", "Every order prints with its own rules. No lilies. No orange. Pet-friendly only. Low "
                  "pollen. The packer sees the constraints before they see the box, and the system "
                  "won’t let an order close if a flagged variety is scanned into it."),
            ("h2", "11am: the awkward ones"),
            ("p", "Occasionally a no-list collides with the day’s stock — you’ve excluded three colours "
                  "and four varieties and what’s left won’t fill a generous box. That’s why the builder "
                  "caps exclusions where it does. When it still happens, we call or email before we "
                  "pack. We’d rather have the conversation than send you a thin box."),
            ("h2", "2pm: out the door"),
            ("p", "Boxes leave in water-retaining wrap with a care card, sometimes a partner treat, and "
                  "— in one box in every 250 — a Golden Ticket."),
            ("p", "Nobody in the building knows which one."),
        ],
    },
    {
        "slug": "meet-the-de-vries-family",
        "title": "Meet the De Vries family, 40 years of roses in Aalsmeer",
        "date": "5 August 2026",
        "tag": "Grower stories",
        "art": "art-product-flower-box-alt",
        "summary": "Three generations, eleven hectares of glass, and a surplus problem that used to end in the compost heap.",
        "body": [
            ("p", "Aalsmeer is a small town with an enormous building in it. The flower auction here "
                  "moves billions of stems a year, and the De Vries family have been sending roses into "
                  "it since 1984."),
            ("h2", "The maths nobody talks about"),
            ("p", "A rose crop doesn’t stop because demand does. The glasshouse keeps producing on its "
                  "own schedule, and if a week’s harvest lands when buyers aren’t buying, the grower has "
                  "a problem measured in tens of thousands of stems."),
            ("p", "“You cannot tell a rose to wait,” Joost de Vries told us, which is the most Dutch "
                  "sentence anyone has said to us. “Either it is sold, or it is compost. For years it "
                  "was compost.”"),
            ("h2", "What changed"),
            ("p", "Surplus buying isn’t charity — the De Vries family are paid a fair price for stock "
                  "that previously returned nothing. But it does change how a week feels. A glut stops "
                  "being a crisis and becomes a phone call."),
            ("p", "For us it means the roses in your box this week may be a variety we’ve never had "
                  "before and won’t have again. For them it means forty years of growing doesn’t end in "
                  "a heap."),
            ("h2", "The bit we like best"),
            ("p", "Joost’s daughter runs the greenhouse now and sends us photos of the crop most weeks. "
                  "When you see a particularly ridiculous rose in your box — the kind with a head the "
                  "size of a fist — there’s a decent chance it came from eleven hectares of glass "
                  "outside Aalsmeer, and that ten years ago you’d never have seen it at all."),
        ],
    },
    {
        "slug": "make-your-box-last-eleven-days",
        "title": "Nine ways to make your box last eleven days",
        "date": "22 July 2026",
        "tag": "Flower care",
        "art": "art-product-plant-box",
        "summary": "Most flowers die of thirst and bacteria, not old age. Five minutes of work buys you an extra week.",
        "body": [
            ("p", "Our record, verified by a customer in York with a suspicious number of photographs, "
                  "is nineteen days. Eleven is realistic for almost everybody. Here’s how."),
            ("ol", [
                "<strong>Unpack immediately.</strong> Not after dinner. Now.",
                "<strong>Cut 2cm off every stem at an angle.</strong> Sharp knife, not blunt scissors — crushing the stem closes the very channels you’re trying to open.",
                "<strong>Strip the leaves below the waterline.</strong> Submerged leaves rot within a day and turn the water into a bacterial soup.",
                "<strong>Actually use the flower food.</strong> It’s sugar plus a biocide plus an acidifier. All three matter.",
                "<strong>Cool water, clean vase.</strong> Run the vase through the dishwasher if it’s been sitting in a cupboard.",
                "<strong>Keep them away from fruit.</strong> Ripening fruit releases ethylene, which is essentially an ageing hormone for flowers.",
                "<strong>Away from radiators and direct sun.</strong> A cool hallway beats a sunny windowsill every time.",
                "<strong>Change the water every two days</strong> and re-trim a centimetre while you’re there.",
                "<strong>Pull the stragglers.</strong> One rotting stem will take the rest with it. Remove it and the bunch carries on.",
            ]),
            ("p", "If you do the first four and nothing else, you’ll still get most of the way there. "
                  "And if a stem doesn’t last seven days, send us a photo — the freshness promise covers it."),
        ],
    },
    {
        "slug": "what-a-golden-ticket-looks-like",
        "title": "What a Golden Ticket actually looks like",
        "date": "8 July 2026",
        "tag": "Golden Tickets",
        "art": "art-product-plant-box-alt",
        "summary": "One in 250 boxes. Here’s what’s in the ticket, how to claim it, and who’s won lately.",
        "body": [
            ("p", "It’s a card, about the size of a postcard, printed on gold foil with a QR code in the "
                  "corner. It sits under the flower care card, which means a surprising number of people "
                  "find theirs two days later while tidying up."),
            ("h2", "What’s on offer"),
            ("ul", [
                "<strong>A year of free boxes</strong> — the big one, drawn a handful of times a year",
                "<strong>A grower tour for two</strong> in the Netherlands, including the 5am auction floor",
                "<strong>A weekend break</strong> for two",
                "<strong>Limited-edition boxes</strong> we never sell publicly",
                "<strong>Partner prizes</strong> from the brands whose samples travel in our boxes",
            ]),
            ("h2", "How to claim"),
            ("p", "Scan the QR code on the ticket. It takes you to a claim page that’s tied to that "
                  "specific ticket number — no forms to fill in beyond confirming where to send the "
                  "prize. We verify against the production record, which is how we know a ticket is genuine."),
            ("h2", "The odds, honestly"),
            ("p", "One in 250 boxes carries a ticket. Tickets are distributed at random across "
                  "production and nobody in the packhouse knows where they are — they go in upstream, "
                  "before boxes are assigned to orders. We can’t tell you which box has one, and we "
                  "can’t put one in on request."),
            ("h2", "Recent winners"),
            ("p", "Priya in Birmingham took the year of free boxes last month. Sam in Newcastle is going "
                  "to Aalsmeer in the spring. Ruth in Aberdeen found the second ticket in her office in a "
                  "year, which her colleagues have understandably described as suspicious."),
        ],
    },
]

FAQ_GROUPS = [
    ("The boxes", [
        ("Can I choose what’s in my box?",
         "No — that’s the surprise, and it’s how we keep the price at £35. What you can do is "
         "tell us what to leave out on the box builder."),
        ("What can I exclude?",
         "Up to three colours and four varieties, plus household needs like pet-friendly, low "
         "pollen, no strong scent or low light. Excluding everything would leave us nothing to "
         "pack, so there’s a sensible cap."),
        ("How many stems do I get?",
         "Typically 15–25 stems depending on the varieties available. Plant boxes contain two "
         "to four plants."),
        ("Can I get a clue before it arrives?",
         "Yes. Ask for the main colour or one variety to be revealed the day before delivery — "
         "or keep it completely sealed."),
        ("Why is it so much cheaper than a florist?",
         "Because we buy surplus stock direct from Dutch growers, and because you’re not paying "
         "for someone to arrange it or for a shop window."),
    ]),
    ("Delivery", [
        ("How much is delivery?",
         "Free across mainland UK. Highlands, islands and Northern Ireland may take an extra day."),
        ("Can I choose the delivery date?",
         "Yes — pick your preferred date on the box builder. Order before 2pm for next-day "
         "dispatch, Monday to Friday."),
        ("What if I’m not home?",
         "Boxes are designed to fit through a standard letterbox where possible, and left in "
         "your safe place otherwise."),
        ("My flowers arrived damaged.",
         "Send us a photo within 48 hours and we’ll replace the box or refund you. Our 7-day "
         "freshness promise covers any stem that doesn’t last the week."),
    ]),
    ("Subscriptions, points &amp; data", [
        ("How do I pause or cancel?",
         "From your account, in two clicks. No phone call, no retention chat."),
        ("How do loyalty points work?",
         "One point per pound spent, plus points for reviews, gallery uploads and referrals. "
         "250 points is £5 off; 1,000 is a free box."),
        ("I bought a box in a supermarket — can I register it?",
         "Yes. Scan the QR code on the box or use the form on the Find a Box page. You’ll get "
         "your care guide, loyalty points and a competition entry."),
        ("What do you do with my data?",
         "We use it to send your order, and — only if you’ve said yes — to email you about "
         "boxes and competitions. We never sell it. See our privacy notice for the detail."),
    ]),
]

CORPORATE_FAQ = [
    ("Can you deliver to hundreds of home addresses?",
     "Yes. Send us a spreadsheet and we handle the rest — one invoice, one delivery window, "
     "individual tracking."),
    ("Do you offer bulk pricing?",
     "Boxes remain £35 up to 50 units. Above that we’ll quote you directly — volume pricing "
     "starts at 50 boxes."),
    ("Can we brand the box?",
     "Yes — printed cards, branded sleeves and custom inserts are all possible with 14 days’ notice."),
    ("How do you handle allergies?",
     "We can apply a blanket exclusion list across an entire order, or collect preferences per recipient."),
    ("Can we pay on invoice?",
     "Yes, for orders over 50 boxes. Standard terms are 30 days from delivery."),
]

SUBSCRIPTION_FAQ = [
    ("When am I charged?",
     "On the day your box is packed, not before. You’ll get an email two days ahead so you can "
     "skip if you want to."),
    ("Can I change my exclusions later?",
     "Yes — update your no-list from your account and it applies to the next box we pack."),
    ("Can I send it to someone else?",
     "Yes. Add their address as the delivery address, or buy a prepaid gift plan so there’s "
     "nothing for them to manage."),
    ("What if I’m not in?",
     "Our boxes are designed to fit through a standard letterbox where possible, and are left "
     "in your safe place otherwise."),
    ("Is there a minimum term?", "No. Cancel after one box if you want to."),
]

LEGAL_PAGES = [
    {
        "slug": "delivery-and-returns",
        "title": "Delivery &amp; returns",
        "eyebrow": "The practical bit",
        "body": """
<h2>Delivery</h2>
<p>Delivery is free on every box across mainland UK. Order before 2pm Monday to Friday and your
box is dispatched the same day for next-day delivery. The Highlands, islands and Northern
Ireland may take one extra working day.</p>
<p>You can choose a preferred delivery date on the box builder when you order. We’ll always
email you a tracking link on the morning of dispatch.</p>
<h2>If you’re not in</h2>
<p>Our boxes are designed to fit through a standard letterbox wherever the contents allow.
Plant boxes and larger flower boxes are left in your nominated safe place, or with a neighbour
if you’ve asked us to.</p>
<h2>Our 7-day freshness promise</h2>
<p>Your flowers should still look good a week after they arrive. If a stem doesn’t last seven
days, send us a photo within 48 hours of noticing and we’ll replace the box or refund you — no
argument, no returning anything.</p>
<h2>Cancellations and changes</h2>
<p>You can change or cancel an order any time before it’s packed — usually until 2pm on the
working day before delivery. Just reply to your order confirmation or contact us.</p>
<p>Because flowers and plants are perishable, they’re exempt from the standard 14-day right to
cancel under the Consumer Contracts Regulations once they’ve been dispatched. That doesn’t
affect your rights if something arrives damaged, wrong or not as described — our freshness
promise goes further than the law requires.</p>
<h2>Subscriptions and multi-box plans</h2>
<p>Prepaid multi-box plans can be paused, rescheduled or cancelled from your account. If you
cancel part-way through a plan, we’ll refund the boxes you haven’t received.</p>
""",
    },
    {
        "slug": "terms-and-conditions",
        "title": "Terms &amp; conditions",
        "eyebrow": "The small print",
        "body": """
<h2>About these terms</h2>
<p>These terms apply when you buy a Mystery Flower Box from this website. Please read them
before you order — by placing an order you agree to them.</p>
<h2>What you’re buying</h2>
<p>A Mystery Flower Box is, by design, a surprise. We do not tell you which flowers or plants
are inside before it arrives, and the contents change with what our growers have available.
What we do guarantee is the box type you chose, a generous quantity, and that we will honour
the exclusions you set on the box builder.</p>
<p>Exclusions are limited to three colours and four varieties, plus household needs such as
pet-friendly or low pollen. This limit exists so that we can still fill your box generously.
Where a requested exclusion cannot be honoured, we will contact you before dispatch.</p>
<h2>Prices and payment</h2>
<p>Every box is £35. Multi-box plans are priced at £35 per box. Prices include VAT where
applicable and delivery within mainland UK. Payment is taken when you place your order, or on
the packing date for scheduled boxes within a plan.</p>
<h2>Availability</h2>
<p>Because our stock is rescued surplus, availability varies. If we cannot fulfil your order we
will tell you and refund you in full.</p>
<h2>Competitions and Golden Tickets</h2>
<p>Competition and Golden Ticket terms are published on our competitions page and form part of
these terms where you take part.</p>
<h2>Loyalty points and referrals</h2>
<p>Points and referral credits have no cash value, cannot be transferred or sold, and may be
withdrawn where we reasonably believe they have been obtained improperly.</p>
<h2>Your rights</h2>
<p>Nothing in these terms limits your statutory rights as a consumer. Our delivery and returns
page explains how we handle damage, delay and cancellation.</p>
""",
    },
    {
        "slug": "privacy-notice",
        "title": "Privacy notice",
        "eyebrow": "Your data",
        "body": """
<h2>Who we are</h2>
<p>Mystery Flower Box is the data controller for the personal data described here. You can
reach us at hello@mysteryflowerbox.com.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Order information</strong> — your name, delivery address, email, phone number and
the preferences you set on the box builder.</li>
<li><strong>Account information</strong> — login details, saved addresses, order history,
loyalty points and referral activity.</li>
<li><strong>Marketing preferences</strong> — whether you’ve told us we can email you.</li>
<li><strong>Gallery uploads and reviews</strong> — anything you choose to send us, including
photos, your first name and town.</li>
<li><strong>Retail registrations</strong> — if you scan the QR code on a box bought in store,
the box code and where you bought it.</li>
<li><strong>Website usage</strong> — cookies and similar technologies.</li>
</ul>
<h2>Why we use it</h2>
<p>To take and deliver your order and honour your exclusions (performance of a contract). To
run your account, loyalty points and referrals (performance of a contract). To send you
marketing, where you have consented. To comply with tax and accounting law (legal obligation).</p>
<h2>Who we share it with</h2>
<p>Our payment provider, our delivery partners, our email platform, and our packhouse — each
only with what they need. We never sell your data. Where a brand partner runs a competition
with us, we tell you at the point of entry exactly what will be shared.</p>
<h2>How long we keep it</h2>
<p>Order records for seven years, for tax purposes. Marketing data until you unsubscribe, and
for two years after your last interaction. Gallery uploads until you ask us to remove them.</p>
<h2>Your rights</h2>
<p>You can ask us for a copy of your data, to correct it, to delete it, to restrict or object
to how we use it, or to have it transferred elsewhere. You can withdraw consent to marketing at
any time. Email hello@mysteryflowerbox.com and we’ll respond within one month. If you’re not
happy with our response you can complain to the Information Commissioner’s Office at ico.org.uk.</p>
""",
    },
    {
        "slug": "flower-care",
        "title": "Flower care",
        "eyebrow": "Make it last",
        "body": """
<h2>The five minutes that buy you a week</h2>
<ol>
<li><strong>Unpack straight away.</strong> Your flowers have travelled; they want water more
than they want to sit in the hall.</li>
<li><strong>Trim 2cm off every stem</strong>, at a steep angle, with a sharp knife or scissors.</li>
<li><strong>Strip any leaves that would sit below the waterline.</strong> Leaves in water rot,
and rot is what makes a bunch go over early.</li>
<li><strong>Use the flower food we sent.</strong> It feeds the bloom and slows the bacteria.</li>
<li><strong>Fill with cool, fresh water</strong> and keep the vase out of direct sun, away from
radiators, and away from the fruit bowl.</li>
</ol>
<h2>Every couple of days</h2>
<p>Change the water completely, rinse the vase, and re-trim the stems by another centimetre. It
takes two minutes and it’s the single biggest thing you can do.</p>
<h2>By variety</h2>
<ul>
<li><strong>Tulips</strong> keep growing in the vase and will lean towards the light.</li>
<li><strong>Roses</strong> like a deep drink. If a head droops, re-cut the stem under water.</li>
<li><strong>Lilies</strong> — pinch out the orange pollen as the flowers open. If lilies aren’t
for you, tick them on the box builder and we’ll leave them out.</li>
<li><strong>Chrysanthemums and alstroemeria</strong> are the marathon runners.</li>
<li><strong>Foliage</strong> like eucalyptus can be dried afterwards.</li>
</ul>
<h2>Your plants</h2>
<p>Most of our house plants want bright, indirect light and a drink when the top two centimetres
of compost feel dry. Almost every plant that dies indoors has been overwatered, not underwatered.</p>
<h2>When it’s over</h2>
<p>Everything in your box is compostable, and the box itself is recyclable card.</p>
""",
    },
]

COMPETITION_TERMS = """
<p>Open to residents of the United Kingdom aged 18 or over. No purchase is necessary to enter
the monthly draw. One entry per person per draw. Entries close at 23:59 on the last day of each
calendar month. The winner is drawn at random within five working days of closing and notified
by email; if we cannot reach a winner within 14 days we will redraw.</p>
<p>Golden Tickets are distributed at random across production and cannot be requested, purchased
or transferred. Prizes are non-transferable and there is no cash alternative. Our decision is
final. By entering you agree that we may publish your first name and town if you win.</p>
"""

ABOUT_STORY = """
<p>Every day, Dutch growers produce more beautiful flowers than the auction system can sell.
Perfect stems, grown with care, that simply arrived on the wrong day or in the wrong quantity.
Traditionally they were composted.</p>
<p>We buy them. We pack them into a box. We don’t tell you what’s inside.</p>
<p>What you get is twice the flowers for half the money, a brand-new surprise every time, and a
small act of rescue in every delivery. What the grower gets is a reliable home for surplus
stock. What the planet gets is a lot fewer wasted flowers.</p>
<p>The only thing you choose is what you’d rather not receive — allergies, pets, a colour you’ve
never liked. Everything else stays sealed until the lid comes off.</p>
"""
