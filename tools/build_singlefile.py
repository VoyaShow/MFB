#!/usr/bin/env python3
"""Build the Mystery Flower Box storefront as one self-contained HTML file.

Every page lives in the document and routing is CSS `:target` first, so links
keep working in viewers that block JavaScript. Illustrations are inlined as an
SVG sprite and the logo as a data URI, so the file needs no network at all.

Usage:  python3 tools/build_singlefile.py [output.html]
"""

import base64
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "theme", "assets")

sys.path.insert(0, HERE)
import site_content as C  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, "dist", "mystery-flower-box.html")

ICONS = {}
SPRITE = []


# ---------------------------------------------------------------- assets ----

def load_icons():
    """Pull the icon set out of the theme's Liquid snippet."""
    path = os.path.join(ROOT, "theme", "snippets", "mfb-icon.liquid")
    text = open(path).read()
    for match in re.finditer(
            r"\{%-\s*when\s*'([a-z-]+)'\s*-%\}\s*(<svg.*?</svg>)", text, re.S):
        ICONS[match.group(1)] = match.group(2).strip()


def icon(name, cls=""):
    svg = ICONS.get(name, "")
    if cls:
        svg = svg.replace("<svg ", '<svg class="%s" ' % cls, 1)
    return svg


def add_art(asset, art_id):
    """Turn an SVG asset into a <symbol> for the sprite."""
    markup = open(os.path.join(ASSETS, asset)).read()
    head = re.search(r"<svg[^>]*>", markup).group(0)
    width = re.search(r'width="(\d+)"', head)
    height = re.search(r'height="(\d+)"', head)
    viewbox = re.search(r'viewBox="([^"]+)"', head)
    box = viewbox.group(1) if viewbox else "0 0 %s %s" % (
        width.group(1), height.group(1))
    body = markup[markup.index(">", markup.index("<svg")) + 1:]
    body = body[:body.rindex("</svg>")]
    # Shrink the payload: coordinates do not need sub-pixel precision here.
    body = re.sub(r"(\d+)\.\d+", r"\1", body)
    body = re.sub(r"\s+", " ", body).replace("> <", "><").strip()
    SPRITE.append('<symbol id="%s" viewBox="%s">%s</symbol>' % (art_id, box, body))
    return box


ART_BOX = {}


def build_sprite():
    ART_BOX["art-hero"] = add_art("mfb-hero.svg", "art-hero")
    for name in ("flower-box", "flower-plant-box", "plant-box"):
        ART_BOX["art-product-%s" % name] = add_art(
            "mfb-product-%s.svg" % name, "art-product-%s" % name)
        ART_BOX["art-product-%s-alt" % name] = add_art(
            "mfb-product-%s-alt.svg" % name, "art-product-%s-alt" % name)
    for i in range(1, 13):
        ART_BOX["art-gallery-%02d" % i] = add_art(
            "mfb-gallery-%02d.svg" % i, "art-gallery-%02d" % i)
    for name in ("peony", "sunflower", "forget-me-not", "genum", "hydrangea", "turf"):
        ART_BOX["art-blooming-%s" % name] = add_art(
            "mfb-blooming-%s.svg" % name, "art-blooming-%s" % name)
    for i in (1, 2, 3):
        ART_BOX["art-grower-%d" % i] = add_art(
            "mfb-grower-%d.svg" % i, "art-grower-%d" % i)
    ART_BOX["art-pattern"] = add_art("mfb-pattern.svg", "art-pattern")


def art(art_id, cls="art", label="", ratio=None, extra=""):
    box = ratio or ART_BOX.get(art_id, "0 0 100 100")
    role = ' role="img" aria-label="%s"' % label if label else ' aria-hidden="true"'
    return ('<svg class="%s" viewBox="%s" preserveAspectRatio="xMidYMid slice"%s%s>'
            '<use href="#%s" xlink:href="#%s"/></svg>'
            % (cls, box, role, (" " + extra if extra else ""), art_id, art_id))


def font_face():
    """Embed the two variable fonts so the file needs no network at all."""
    faces = []
    for family, filename in (("Baloo 2", "baloo2.woff2"),
                             ("Roboto Slab", "roboto-slab.woff2")):
        path = os.path.join(ROOT, "sitefile", "fonts", filename)
        with open(path, "rb") as fh:
            blob = base64.b64encode(fh.read()).decode()
        faces.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:300 800;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}"
            % (family, blob))
    return "".join(faces)


def data_uri(filename):
    with open(os.path.join(ASSETS, filename), "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


def gallery_art(index):
    return "art-gallery-%02d" % ((index % 12) + 1)


# -------------------------------------------------------------- fragments ---

def stars(rating):
    out = ['<span class="stars" role="img" aria-label="%s out of 5 stars">' % rating]
    for i in range(1, 6):
        star = icon("star")
        out.append(star if i <= rating else '<span style="opacity:.25">%s</span>' % star)
    out.append("</span>")
    return "".join(out)


def head(eyebrow="", heading="", sub="", align="center"):
    if not (eyebrow or heading or sub):
        return ""
    cls = "section-head" + ("" if align == "center" else " section-head--left")
    out = ['<header class="%s">' % cls]
    if eyebrow:
        out.append('<span class="eyebrow">%s</span>' % eyebrow)
    if heading:
        out.append("<h2>%s</h2>" % heading)
    if sub:
        out.append('<div class="lede">%s</div>' % sub)
    out.append("</header>")
    return "".join(out)


def section(body, tone="cream", tight=False, extra=""):
    return '<section class="section section--%s%s"%s><div class="page-width">%s</div></section>' % (
        tone, " section--tight" if tight else "", (" " + extra if extra else ""), body)


def btn(label, href, kind="", size=""):
    cls = "btn"
    if kind:
        cls += " btn--" + kind
    if size:
        cls += " btn--" + size
    return '<a class="%s" href="%s">%s</a>' % (cls, href, label)


def product_card(p):
    return (
        '<article class="product-card" data-reveal>'
        '<a class="product-card__media" href="#%s" aria-label="%s">%s'
        '<span class="pill pill--white product-card__flag">%s</span></a>'
        '<div class="product-card__body">'
        '<h3 class="product-card__title"><a href="#%s">%s</a></h3>'
        '<div class="product-card__price">£35.00</div>'
        '<p class="product-card__desc">%s</p>'
        '<div class="product-card__cta">%s</div>'
        "</div></article>"
        % (p["slug"], p.get("plain_title", p["title"]),
           art(p["art"], "art art--square", p.get("plain_title", p["title"])),
           p["flag"], p["slug"], p["title"], p["short"],
           btn("Build this box", "#" + p["slug"], "", "sm"))
    )


def three_products():
    return "".join(product_card(p) for p in C.PRODUCTS)


def feature(icon_name, title, text):
    return ('<div class="feature" data-reveal><div class="feature__icon">%s</div>'
            "<h3>%s</h3><p>%s</p></div>" % (icon(icon_name), title, text))


def reactions_block(eyebrow, heading, sub, tone="mist"):
    cards = []
    for r in C.REACTIONS:
        cards.append(
            '<article class="reaction-card" data-reveal>'
            '<div class="reaction-card__media">%s'
            '<span class="reaction-card__emoji" aria-hidden="true">%s</span></div>'
            '<div class="reaction-card__quote">%s<p style="margin-top:10px">&ldquo;%s&rdquo;</p>'
            '<div class="reaction-card__who">%s<small>%s · %s</small></div></div></article>'
            % (art(r["art"], "art", r["name"]), r["emoji"], stars(r["rating"]),
               r["quote"], r["name"], r["where"], r["box"]))
    return section(
        head(eyebrow, heading, sub) +
        '<div class="grid grid--3">%s</div>' % "".join(cards) +
        '<div class="cluster cluster--center" style="margin-top:42px">%s</div>'
        % btn("See the whole gallery", "#gallery", "secondary"),
        tone)


def reviews_block(tone="cream"):
    cards = []
    for rating, title, body, name, when in C.REVIEWS:
        cards.append(
            '<article class="review-card" data-reveal>%s'
            '<div class="review-card__title">%s</div>'
            '<p class="review-card__body">%s</p>'
            '<div class="review-card__meta"><strong>%s</strong>'
            '<span class="review-card__verified">%s Verified</span><span>%s</span></div>'
            "</article>" % (stars(rating), title, body, name, icon("check"), when))
    summary = (
        '<div class="rating-summary"><span class="rating-summary__score">4.8</span>%s'
        '<span class="muted">Based on 2,324 verified reviews</span>'
        '<span class="pill pill--white">Trustpilot &amp; Judge.me</span></div>'
        % stars(5))
    return section(
        head("Reviews", "What people say once they’ve opened it") + summary +
        '<div class="grid grid--3">%s</div>' % "".join(cards), tone)


def gallery_block(tone="white", show_head=True, grid_id="gallery-grid"):
    tabs = ['<div class="tabs" data-tabs="#%s">' % grid_id,
            '<button class="tab-btn" type="button" data-tab="all" aria-selected="true">Everything</button>']
    for f in C.GALLERY_FILTERS:
        tabs.append('<button class="tab-btn" type="button" data-tab="%s" aria-selected="false">%s</button>'
                    % (slug(f), f))
    tabs.append("</div>")

    tiles = []
    for i, (name, where, caption, cat, box, likes, comments) in enumerate(C.GALLERY):
        tiles.append(
            '<figure class="gallery-tile" data-tab-panel="%s">%s'
            '<a class="gallery-tile__shop" href="#shop">Shop this box</a>'
            '<figcaption class="gallery-tile__overlay">'
            '<span class="gallery-tile__who">%s, %s</span>'
            '<p class="gallery-tile__caption">%s</p>'
            '<div class="gallery-tile__actions">'
            '<button type="button" data-like="%s-g%d" aria-pressed="false" aria-label="Like this photo">'
            '%s <span data-like-count>%s</span></button>'
            '<span>%s %s</span></div>'
            '<span class="gallery-tile__box">%s</span></figcaption></figure>'
            % (slug(cat), art(gallery_art(i), "art art--square", caption),
               name, where, caption, grid_id, i, icon("heart"), likes,
               icon("comment"), comments, box))

    body = (head("Customer gallery", "#MysteryFlowerBox",
                 "<p>Real boxes, real homes, real reactions. Tag us and you could land on "
                 "this wall — and in the Golden Ticket draw.</p>") if show_head else "")
    return section(
        body + "".join(tabs) +
        '<div class="masonry" id="%s">%s</div>' % (grid_id, "".join(tiles)), tone)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def blooming_block():
    cards = []
    for art_id, name, note in C.BLOOMING:
        cards.append('<div class="bloom-card">%s<strong>%s</strong><span>%s</span></div>'
                     % (art(art_id, "art", name), name, note))
    return section(
        head("Live from the packhouse", "What’s blooming today?",
             "<p>A peek at the varieties we’re packing this week. We’ll never tell you "
             "exactly what lands in your box.</p>") +
        '<div class="bloom-strip">%s</div>' % "".join(cards) +
        '<p class="center muted small" style="margin-top:20px">Updated every weekday '
        "morning by the packhouse team.</p>", "meadow")


def golden_block(tone="peony", show_cta=True):
    cards = "".join(
        '<div class="ticket-card"><span class="ticket-card__icon" aria-hidden="true">%s</span>'
        "<span><strong>%s</strong>%s</span></div>" % (e, prize, who)
        for e, prize, who in C.GOLDEN)
    cta = ('<div style="margin-top:24px">%s</div>'
           % btn("See the prize list", "#competitions", "light")) if show_cta else ""
    return section(
        '<div class="split"><div><span class="eyebrow">Golden Ticket tracker</span>'
        "<h2>One in every 250 boxes hides a Golden Ticket</h2>"
        '<div class="lede"><p>Free boxes for a year, weekend breaks, grower tours and '
        "limited-edition blooms. Winners announced here and in your inbox.</p></div>%s</div>"
        '<div class="stack">%s</div></div>' % (cta, cards), tone)


def plans_block(tone="blush", show_head=True):
    cards = []
    for name, price, cadence, perks, featured in C.PLAN_CARDS:
        flag = '<span class="pill plan-card__flag">Most popular</span>' if featured else ""
        cards.append(
            '<div class="plan-card%s" data-reveal>%s<h3>%s</h3>'
            '<div class="plan-card__price">%s</div><p class="muted small">%s</p>'
            "<ul>%s</ul>%s</div>"
            % (" plan-card--featured" if featured else "", flag, name, price, cadence,
               "".join("<li>%s</li>" % p for p in perks),
               '<a class="btn %sbtn--full" href="#shop">Choose this plan</a>'
               % ("" if featured else "btn--secondary ")))
    body = (head("Subscriptions", "A surprise on repeat",
                 "<p>Pause, skip, upgrade or cancel yourself from your account — no emails, "
                 "no phone calls.</p>") if show_head else "")
    return section(body + '<div class="grid grid--4">%s</div>' % "".join(cards) +
                   '<p class="center muted" style="margin-top:30px">Every plan includes free '
                   "UK delivery, double loyalty points and first refusal on limited boxes.</p>",
                   tone)


def growers_block(tone="meadow"):
    cards = []
    for art_id, name, region, text in C.GROWERS:
        cards.append(
            '<article class="shape-card" data-reveal>%s<div style="padding:24px">'
            '<span class="pill pill--turf">%s</span><h3 style="margin-top:14px">%s</h3>'
            '<p class="muted">%s</p></div></article>'
            % (art(art_id, "art art--square", name), region, name, text))
    return section(
        head("Meet the growers", "The people behind the surprise",
             "<p>Every box starts in a Dutch greenhouse with a family that has been growing "
             "for generations.</p>") +
        '<div class="grid grid--3">%s</div>' % "".join(cards), tone)


def stats_block(stats, eyebrow, heading, sub="", tone="mist", cta=None):
    cells = "".join('<div><div class="stat__value">%s</div>'
                    '<div class="stat__label">%s</div></div>' % (v, l) for v, l in stats)
    extra = ('<div class="cluster cluster--center" style="margin-top:38px">%s</div>'
             % btn(cta[0], cta[1], "secondary")) if cta else ""
    return section(head(eyebrow, heading, sub) +
                   '<div class="stat-row">%s</div>' % cells + extra, tone)


def accordion(items):
    out = ['<div class="accordion">']
    for q, a in items:
        out.append('<details class="accordion__item"><summary class="accordion__summary">%s'
                   '</summary><div class="accordion__body rte"><p>%s</p></div></details>' % (q, a))
    out.append("</div>")
    return "".join(out)


def cta_band(heading, text="", primary=("Surprise Me!", "#shop"), secondary=None, tone="peony"):
    out = ['<div class="page-width center"><h2>%s</h2>' % heading]
    if text:
        out.append('<div class="lede" style="max-width:640px;margin:0 auto">%s</div>' % text)
    out.append('<div class="cluster cluster--center" style="margin-top:28px">')
    out.append(btn(primary[0], primary[1], "light", "lg"))
    if secondary:
        out.append('<a class="btn btn--ghost btn--lg" href="%s" style="color:#fff;border-color:#fff">%s</a>'
                   % (secondary[1], secondary[0]))
    out.append("</div></div>")
    return '<section class="section section--%s">%s</section>' % (tone, "".join(out))


def newsletter_block(tone="blush"):
    return section(
        '<div class="center"><span class="eyebrow">Join 40,000 flower people</span>'
        "<h2>10% off your first surprise</h2>"
        '<div class="lede" style="max-width:600px;margin:0 auto 26px"><p>Golden Ticket news, '
        "limited boxes and flower care tips. One email a week, never more.</p></div>"
        '<form class="prose-narrow" data-demo-form style="max-width:520px;margin:0 auto">'
        '<div data-form-fields><div class="inline-form">'
        '<input type="email" placeholder="you@example.com" aria-label="Email address" required>'
        '<button class="btn" type="submit">Send my code</button></div>'
        '<p class="form-note">We look after your data. Unsubscribe in one click.</p></div>'
        '<div class="form-success" hidden data-form-success><strong>Welcome to the club.</strong> '
        "Your 10% code is on its way.</div></form></div>", tone)


# ------------------------------------------------------------------ pages ---

PAGES = []


def page(pid, title, body):
    PAGES.append('<div class="page" id="%s" data-title="%s">%s</div>' % (pid, title, body))


def build_home():
    hero = (
        '<section class="hero"><div class="page-width hero__grid"><div>'
        '<span class="eyebrow">Rescued Dutch blooms · £35 a box</span>'
        '<h1 class="hero__title">What’s in your Mystery Flower Box?</h1>'
        '<div class="lede"><p>Customers don’t pick flowers. They buy the surprise. '
        "Choose your box, tell us what to leave out, and let our growers do the rest.</p></div>"
        '<div class="hero__badges">'
        '<span class="pill">Every box £35</span>'
        '<span class="pill pill--sun">Free UK delivery</span>'
        '<span class="pill pill--violet">Tell us what to leave out</span></div>'
        '<div class="cluster" style="margin-top:28px">%s%s</div>'
        '<div class="hero__ticker"><span>%s Surplus Dutch blooms rescued</span>'
        "<span>%s Next-day delivery</span><span>%s Golden Tickets inside</span></div>"
        '</div><div class="hero__media">%s</div></div></section>'
        % (btn("Surprise Me!", "#shop", "", "lg"),
           btn("How it works", "#how-it-works", "secondary", "lg"),
           icon("recycle"), icon("truck"), icon("gift"),
           art("art-hero", "art", "A Mystery Flower Box bursting with surprise blooms"))
    )

    marquee_items = ["Surplus flowers rescued", "One clear price",
                     "Tell us what to leave out", "Golden Tickets inside",
                     "Supporting Dutch growers", "Never the same box twice"]
    run = " ".join("%s ✿" % i for i in marquee_items)
    marquee = ('<div class="marquee" aria-hidden="true"><div class="marquee__track">'
               "<span>%s</span><span>%s</span></div></div>" % (run, run))

    products = section(
        head("This week’s mystery boxes", "One price. Three boxes. Endless surprises.",
             "<p>No endless bouquets to scroll through. Pick your box, set your exclusions on "
             "the box builder, and open the lid to find out.</p>") +
        '<div class="grid grid--3">%s</div>' % three_products() +
        '<p class="center lede" style="margin-top:34px">Every box is £35. Always.</p>', "white")

    why = section(
        head("Why Mystery Flower Box", "Not a florist. A very good surprise.") +
        '<div class="grid grid--4">%s</div>'
        % "".join(feature(i, t, x) for i, t, x in C.WHY), "cream")

    steps = "".join(
        '<div class="step" data-reveal><div class="step__num">%d</div><h3>%s</h3>'
        '<p class="muted">%s</p></div>' % (i + 1, t, x)
        for i, (t, x) in enumerate(C.STEPS))
    how = section(
        head("How it works", "Four steps to a very good day") +
        '<div class="grid grid--4">%s</div>' % steps +
        '<div class="cluster cluster--center" style="margin-top:42px">%s</div>'
        % btn("Build my box", "#shop"), "white")

    chips = "".join(
        '<span class="chip"><span class="chip__label" style="cursor:default">%s%s '
        '<span aria-hidden="true">✕</span></span></span>'
        % ('<span class="chip__swatch" style="background:%s"></span>' % sw if sw else "", label)
        for label, sw in C.EXCLUSION_CHIPS)
    personalise = section(
        '<div class="split"><div class="split__media">%s</div><div>'
        '<span class="eyebrow">Your box, your rules</span>'
        "<h2>Keep the surprise. Lose the lilies.</h2>"
        '<div class="lede"><p>You don’t choose what goes in — but you can tell us what to leave '
        "out. Allergies, pets, a colour you’ve never liked: tick it on the box builder and our "
        "growers pack around it. Everything else stays a total mystery.</p></div>"
        '<div class="chips" style="margin:26px 0">%s</div>%s</div></div>'
        % (art("art-product-flower-box-alt", "art art--square",
               "Flowers beside a ribboned Mystery Flower Box"), chips,
           btn("Build my box", "#shop")), "blush")

    news_cards = "".join(article_card(a) for a in C.ARTICLES[:3])
    news = section(
        head("From the packhouse", "Latest news") +
        '<div class="grid grid--3">%s</div>' % news_cards +
        '<div class="cluster cluster--center" style="margin-top:38px">%s</div>'
        % btn("All news", "#news", "secondary"), "white")

    referral = section(
        '<div class="split split--reverse"><div class="split__media">%s</div><div>'
        '<span class="eyebrow">Refer a friend</span><h2>Give £10, get a free box</h2>'
        '<div class="lede"><p>Share your link. Your friend gets £10 off their first surprise, '
        "and after three referrals your next box is on us.</p></div>"
        '<div class="form-card" style="margin-top:26px;padding:22px">'
        '<span class="field-label">Your referral link</span><div class="cluster">'
        '<code style="flex:1;min-width:200px;word-break:break-all">mysteryflowerbox.com/r/your-name</code>'
        '<button class="btn btn--sm" type="button" data-copy="mysteryflowerbox.com/r/your-name">'
        "Copy link</button></div></div>%s</div></div>"
        % (art("art-gallery-05", "art art--square", "A Mystery Flower Box arriving at a party"),
           '<div style="margin-top:24px">%s</div>' % btn("How referrals work", "#refer-a-friend")),
        "sand")

    partners = section(
        head("Inside your box", "Partner treats and samples",
             "<p>Every box carries a surprise from a brand we actually like. No junk, no filler.</p>") +
        '<div class="grid grid--4">%s</div>'
        % "".join('<div class="feature" data-reveal><span class="pill pill--sun">%s</span>'
                  '<h3 style="margin-top:14px">%s</h3><p>%s</p></div>' % o
                  for o in C.PARTNER_OFFERS) +
        '<div class="cluster cluster--center" style="margin-top:40px">%s</div>'
        % btn("Partner with us", "#brand-partnerships", "secondary"), "white")

    insta_tiles = "".join(
        '<a href="#gallery" aria-label="View in the gallery">%s</a>'
        % art(gallery_art(i), "art art--square", "Customer photo") for i in range(6))
    instagram = section(
        head("Follow along", "@mysteryflowerbox") +
        '<div class="ig-grid">%s</div>' % insta_tiles +
        '<div class="cluster cluster--center" style="margin-top:26px">'
        '<a class="btn btn--secondary btn--sm" href="#gallery">%s @mysteryflowerbox</a></div>'
        % icon("instagram"), "cream", tight=True)

    body = "".join([
        hero, marquee, products, why, how, personalise,
        reactions_block("Real reactions", "The moment the lid comes off",
                        "<p>Thousands of unboxings, filmed on kitchen tables and doorsteps "
                        "across the country.</p>"),
        gallery_block("white", grid_id="home-gallery-grid"),
        reviews_block("cream"),
        blooming_block(),
        golden_block(),
        plans_block("blush"),
        referral,
        partners,
        instagram,
        news,
        stats_block(C.INVESTOR_STATS, "Investors &amp; partners",
                    "The numbers behind the surprise",
                    "<p>A consumer platform built on first-party data, repeat purchase and "
                    "multiple revenue streams.</p>", "mist",
                    ("Investor information", "#investors")),
        newsletter_block(),
    ])
    page("home", "Surprise flower boxes, £35", body)


def article_card(a):
    return ('<article class="article-card" data-reveal>%s<div class="article-card__body">'
            '<span class="article-card__date">%s · %s</span>'
            '<h3><a href="#%s">%s</a></h3><p class="muted">%s</p>'
            '<a class="btn btn--sm btn--secondary" href="#%s" '
            'style="align-self:flex-start;margin-top:auto">Read more</a></div></article>'
            % (art(a["art"], "art", a["title"]), a["date"], a["tag"], a["slug"],
               a["title"], a["summary"], a["slug"]))


def build_shop():
    clue_card = (
        '<div class="form-card" style="margin-bottom:38px">'
        '<h3 style="margin-bottom:6px">Prefer a clue before you buy?</h3>'
        '<p class="muted small">These are optional. Leave everything blank for the complete '
        "mystery — that is how most people do it.</p>"
        '<div class="grid grid--4" style="margin-top:18px">'
        '<label class="field"><span>Box type</span><select><option>Any box</option>'
        "<option>Flowers</option><option>Flowers &amp; plants</option><option>Plants</option></select></label>"
        '<label class="field"><span>Main colour</span><select><option>Surprise me</option>'
        "<option>Pinks</option><option>Brights</option><option>Pastels</option>"
        "<option>Whites &amp; greens</option></select></label>"
        '<label class="field"><span>Delivery</span><select><option>Next available</option>'
        "<option>Choose a date on the builder</option></select></label>"
        '<label class="field"><span>How often</span><select><option>One-off</option>'
        "<option>Subscription</option></select></label></div>"
        '<p class="form-note">Clues are set on the box builder when you pick a box — including '
        "the flowers and colours you would rather not receive.</p></div>")

    body = section(
        '<header class="section-head"><span class="eyebrow">Three clear choices · £35 each</span>'
        "<h1>Shop</h1><div class=\"lede\"><p>Three boxes. One price. Endless surprises. Choose "
        "your box, tell us what to leave out, and let our Dutch growers do the rest.</p></div></header>"
        + clue_card + '<div class="grid grid--3">%s</div>' % three_products(), "cream")

    body += section(
        head("Why it works", "Three boxes is all you need") +
        '<div class="grid grid--3">%s</div>' % "".join([
            feature("sparkle", "One clear price",
                    "Every box is £35. No upsells, no premium tiers, no decision fatigue."),
            feature("recycle", "Surplus rescued",
                    "Beautiful stems that would otherwise be wasted, bought direct from Dutch growers."),
            feature("heart", "Your rules respected",
                    "Tell us what to leave out on the box builder — allergies, pets, colours you can’t stand."),
        ]), "white")

    body += cta_band("Still can’t decide?",
                     "<p>Most people start with the Mystery Flower Box. You can always switch "
                     "next time.</p>", ("Build a Mystery Flower Box", "#mystery-flower-box"))
    page("shop", "Shop — three boxes, one price", body)


def build_product(p):
    title = p.get("plain_title", p["title"])
    plans_json = ("[" + ",".join(
        '{"id":"%s","label":"%s","price":%s,"boxes":%d}'
        % (pl["id"], pl["label"], pl["price"], pl["boxes"]) for pl in p["plans"]) + "]")

    options = []
    for i, pl in enumerate(p["plans"]):
        options.append(
            '<div class="purchase-option">'
            '<input type="radio" name="plan-%s" id="plan-%s-%s" value="%s" data-plan%s>'
            '<label class="purchase-option__label" for="plan-%s-%s">'
            '<span class="purchase-option__dot" aria-hidden="true"></span>'
            '<span class="purchase-option__text"><span class="purchase-option__name">%s</span>'
            '<span class="purchase-option__meta">%s</span></span>'
            '<span class="purchase-option__price">£%.2f</span></label></div>'
            % (p["slug"], p["slug"], pl["id"], pl["id"], " checked" if i == 0 else "",
               p["slug"], pl["id"], pl["label"], pl["note"], pl["price"]))

    colour_chips = "".join(
        '<span class="chip"><input type="checkbox" id="%s-col-%d" data-exclusion '
        'data-kind="colour" value="%s"><label class="chip__label" for="%s-col-%d">'
        '<span class="chip__swatch" style="background:%s"></span>%s'
        '<span class="chip__cross" aria-hidden="true">✕</span></label></span>'
        % (p["slug"], i, label, p["slug"], i, hexv, label)
        for i, (label, hexv) in enumerate(C.BUILDER["colours"]))

    variety_chips = "".join(
        '<span class="chip"><input type="checkbox" id="%s-var-%d" data-exclusion '
        'data-kind="variety" value="%s"><label class="chip__label" for="%s-var-%d">%s'
        '<span class="chip__cross" aria-hidden="true">✕</span></label></span>'
        % (p["slug"], i, v, p["slug"], i, v)
        for i, v in enumerate(C.BUILDER["varieties"]))

    care_chips = "".join(
        '<span class="chip"><input type="checkbox" id="%s-care-%d" data-exclusion '
        'data-kind="care" value="%s"><label class="chip__label" for="%s-care-%d">%s</label></span>'
        % (p["slug"], i, v, p["slug"], i, v)
        for i, v in enumerate(C.BUILDER["care"]))

    clue_chips = "".join(
        '<span class="chip"><input type="radio" name="clue-%s" id="%s-clue-%d" data-clue '
        'value="%s"%s><label class="chip__label" for="%s-clue-%d">%s</label></span>'
        % (p["slug"], p["slug"], i, v, ' checked data-default' if i == 0 else "",
           p["slug"], i, v)
        for i, v in enumerate(C.BUILDER["clues"]))

    builder = (
        '<form class="builder" data-box-builder data-plans=\'%s\' data-title="%s" data-art="%s">'

        '<fieldset class="builder__step" style="border:0;padding:0;margin-bottom:22px">'
        '<legend class="builder__step-title"><span class="builder__step-num">1</span> '
        "How often would you like a surprise?</legend>"
        '<p class="builder__hint">Every box is £35. Bundles are delivered on your chosen rhythm '
        "and you can pause any time.</p>"
        '<div class="purchase-options">%s</div></fieldset>'

        '<div class="builder__step" style="background:var(--blush);border-color:var(--peony)">'
        '<div class="builder__step-title"><span class="builder__step-num">2</span> '
        "How brave are you feeling?</div>"
        '<p class="builder__hint">Customers don’t pick flowers — they buy the surprise. But if '
        "there is something you would rather not receive, tell us below.</p>"
        '<div class="chips"><span class="chip chip--solo">'
        '<input type="checkbox" id="%s-surprise" data-full-surprise>'
        '<label class="chip__label" for="%s-surprise">🎁 Total mystery — surprise me completely'
        "</label></span></div></div>"

        '<fieldset class="builder__step" data-lockable data-exclusion-group data-max="%d">'
        '<legend class="builder__step-title"><span class="builder__step-num">3</span> '
        "Any colours to leave out?</legend>"
        '<p class="builder__hint">Tick anything you would rather not receive. Leave them all '
        "blank for the full surprise.</p>"
        '<div class="chips">%s</div>'
        '<p class="form-note" data-exclusion-note hidden>That is the maximum number of colours '
        "we can leave out and still fill a generous box.</p></fieldset>"

        '<fieldset class="builder__step" data-lockable data-exclusion-group data-max="%d">'
        '<legend class="builder__step-title"><span class="builder__step-num">4</span> '
        "Any flowers or plants to leave out?</legend>"
        '<p class="builder__hint">Not a fan of chrysanthemums? Allergic to lilies? Tell us and '
        "our growers will pack around it.</p>"
        '<div class="chips">%s</div>'
        '<p class="form-note" data-exclusion-note hidden>That is as many varieties as we can '
        "leave out while keeping your box full.</p></fieldset>"

        '<fieldset class="builder__step" data-lockable>'
        '<legend class="builder__step-title"><span class="builder__step-num">5</span> '
        "Anything we should know about your home?</legend>"
        '<p class="builder__hint">We will match your box to your household.</p>'
        '<div class="chips">%s</div></fieldset>'

        '<fieldset class="builder__step" data-lockable>'
        '<legend class="builder__step-title"><span class="builder__step-num">6</span> '
        "Want a clue before it lands?</legend>"
        '<p class="builder__hint">Reveal a hint the day before delivery, or keep the whole '
        "thing sealed.</p>"
        '<div class="chips">%s</div></fieldset>'

        '<fieldset class="builder__step">'
        '<legend class="builder__step-title"><span class="builder__step-num">7</span> '
        "When shall we deliver?</legend>"
        '<label class="field"><span>Preferred delivery date</span>'
        '<input type="date" data-delivery-date></label>'
        '<label class="field"><span>Gift message (optional)</span>'
        '<textarea rows="3" data-gift-message placeholder="Happy birthday! Hope this one makes '
        'you smile."></textarea></label></fieldset>'

        '<div class="summary"><h4>Your box so far</h4>'
        '<ul data-builder-summary><li>No exclusions yet — you are open to anything. 🌷</li></ul></div>'

        '<div class="cluster" style="margin-bottom:16px">'
        '<div class="quantity"><button type="button" data-qty="down" aria-label="Decrease quantity">'
        "&minus;</button>"
        '<input type="number" value="1" min="1" data-builder-qty aria-label="Quantity">'
        '<button type="button" data-qty="up" aria-label="Increase quantity">+</button></div>'
        '<button class="btn btn--lg" type="submit" data-add>Add my surprise — £35.00</button></div>'
        '<p class="form-note">%s Secure checkout. Cancel or pause a bundle any time from your '
        "account.</p></form>"
        % (plans_json, title, p["art"], "".join(options), p["slug"], p["slug"],
           C.BUILDER["max_colours"], colour_chips,
           C.BUILDER["max_varieties"], variety_chips,
           care_chips, clue_chips, icon("lock"))
    )

    gallery = (
        '<div class="product-gallery" data-gallery>'
        '<div class="product-gallery__main" data-art-main>%s</div>'
        '<div class="product-gallery__thumbs">'
        '<button class="product-gallery__thumb" type="button" data-art-thumb="%s" '
        'aria-current="true" aria-label="Show the open box">%s</button>'
        '<button class="product-gallery__thumb" type="button" data-art-thumb="%s" '
        'aria-current="false" aria-label="Show the ribboned box">%s</button></div>'
        '<div class="trust-row"><span>%s Next-day delivery available</span>'
        "<span>%s Rescued from Dutch growers</span><span>%s 7-day freshness promise</span></div></div>"
        % (art(p["art"], "art art--square", title),
           p["art"], art(p["art"], "art art--square"),
           p["art_alt"], art(p["art_alt"], "art art--square"),
           icon("truck"), icon("recycle"), icon("leaf")))

    buy = (
        '<div><span class="pill">%s</span><h1 style="margin-top:14px">%s</h1>'
        '<div class="cluster" style="margin-bottom:14px">%s'
        '<span class="small muted">%s/5 from %s reviews</span></div>'
        '<div class="product-price" data-product-price>£35.00</div>'
        '<div class="product-price__note"><span data-price-per-box>One clear price · free UK '
        "delivery</span></div>"
        '<div class="rte" style="margin-top:18px">%s<ul>%s</ul></div>%s'
        '<div class="accordion" style="margin-top:36px">%s</div></div>'
        % (p["flag"], p["title"], stars(round(p["rating"])), p["rating"], p["reviews"],
           "".join("<p>%s</p>" % b for b in p["body"]),
           "".join("<li>%s</li>" % b for b in p["bullets"]),
           builder,
           "".join('<details class="accordion__item"%s><summary class="accordion__summary">%s'
                   '</summary><div class="accordion__body rte"><p>%s</p></div></details>'
                   % (" open" if i == 0 else "", q, a)
                   for i, (q, a) in enumerate(C.PRODUCT_FAQ))))

    others = [o for o in C.PRODUCTS if o["slug"] != p["slug"]]
    body = section(
        '<nav class="breadcrumbs"><a href="#home">Home</a> / <a href="#shop">Shop</a> / '
        "<span>%s</span></nav>"
        '<div class="product-layout">%s%s</div>' % (p["title"], gallery, buy), "cream")
    body += section(
        head("Three clear choices", "The other boxes") +
        '<div class="grid grid--2">%s</div>' % "".join(product_card(o) for o in others), "white")
    page(p["slug"], title, body)


def demo_form(fields, cta="Send enquiry", success_title="Thank you — enquiry received.",
              success_text="A member of the team will be in touch within one working day.",
              note="We reply to every enquiry within one working day."):
    return (
        '<form class="form-card" data-demo-form><div data-form-fields>%s'
        '<label class="field" style="display:flex;gap:10px;align-items:flex-start">'
        '<input type="checkbox" style="width:auto;margin-top:6px" required>'
        '<span style="margin:0;font-weight:400;font-size:.92rem">I am happy for Mystery Flower '
        "Box to contact me about this enquiry. *</span></label>"
        '<button class="btn btn--lg" type="submit">%s</button>'
        '<p class="form-note">%s</p></div>'
        '<div class="form-success" hidden data-form-success><strong>%s</strong><br>%s</div></form>'
        % (fields, cta, note, success_title, success_text))


def field(label, kind="text", required=False, placeholder="", options=None, rows=None):
    req = " required" if required else ""
    star = " *" if required else ""
    ph = ' placeholder="%s"' % placeholder if placeholder else ""
    if options:
        opts = "".join("<option>%s</option>" % o for o in options)
        control = '<select%s><option value="">Please choose…</option>%s</select>' % (req, opts)
    elif rows:
        control = '<textarea rows="%d"%s%s></textarea>' % (rows, ph, req)
    else:
        control = '<input type="%s"%s%s>' % (kind, ph, req)
    return '<label class="field"><span>%s%s</span>%s</label>' % (label, star, control)


def two_col(*fields):
    return '<div class="grid grid--2">%s</div>' % "".join(fields)


BASE_FIELDS = two_col(
    field("Your name", required=True),
    field("Work email", "email", required=True),
    field("Company", required=True),
    field("Phone", "tel"),
)


def build_how_it_works():
    steps = "".join(
        '<div class="step" data-reveal><div class="step__num">%d</div><h3>%s</h3>'
        '<p class="muted">%s</p></div>' % (i + 1, t, x)
        for i, (t, x) in enumerate([
            ("Pick your box", "Flowers, plants, or both. Every box is £35, one-off or on repeat."),
            ("Set your no-list", "Up to three colours and four varieties you’d rather not receive, plus pet and allergy needs."),
            ("We pack it fresh", "Our Dutch growers fill your box the morning it leaves, working around your list."),
            ("Open the lid", "Film it, tag us, collect loyalty points — and check inside for a Golden Ticket."),
        ]))
    chips = "".join(
        '<span class="chip"><span class="chip__label" style="cursor:default">%s%s '
        '<span aria-hidden="true">✕</span></span></span>'
        % ('<span class="chip__swatch" style="background:%s"></span>' % sw if sw else "", label)
        for label, sw in C.EXCLUSION_CHIPS[:5])

    body = page_hero("How it works", "Four steps to a very good day",
                     "<p>You don’t pick the flowers. You pick the box, set your no-list, and we "
                     "do the rest.</p>", ("Surprise Me!", "#shop"))
    body += section('<div class="grid grid--4">%s</div>' % steps, "white")
    body += section(
        '<div class="split split--reverse"><div class="split__media">%s</div><div>'
        '<span class="eyebrow">The box builder</span>'
        "<h2>The only thing you choose is what you don’t want</h2>"
        '<div class="lede"><p>On every product page you’ll find the box builder. Tick the '
        "colours and varieties to leave out, flag allergies or pets, choose whether you’d like a "
        "clue before delivery, and pick your date. Everything else stays sealed until the lid "
        "comes off.</p></div><div class=\"chips\" style=\"margin:26px 0\">%s</div>%s</div></div>"
        % (art("art-product-flower-plant-box", "art art--square", "Flowers and a plant in a box"),
           chips, btn("Try the box builder", "#shop")), "blush")
    body += growers_block()
    body += section(head("Questions", "Before you order") +
                    '<div class="prose-narrow">%s</div>' % accordion(C.FAQ_GROUPS[0][1][:4]), "white")
    body += cta_band("Ready for a very good surprise?")
    page("how-it-works", "How it works", body)


def page_hero(eyebrow, heading, text="", cta=None, tone="blush"):
    out = ['<div class="page-width"><div class="center" style="max-width:760px;margin:0 auto">']
    if eyebrow:
        out.append('<span class="eyebrow">%s</span>' % eyebrow)
    out.append("<h1>%s</h1>" % heading)
    if text:
        out.append('<div class="lede">%s</div>' % text)
    if cta:
        out.append('<div class="cluster cluster--center" style="margin-top:24px">%s</div>'
                   % btn(cta[0], cta[1]))
    out.append("</div></div>")
    return ('<section class="section section--%s section--tight">%s</section>'
            % (tone, "".join(out)))


def build_gallery():
    upload_fields = (
        two_col(field("Your name", required=True), field("Email", "email", required=True)) +
        two_col(field("Town or city", required=True, placeholder="Leeds"),
                field("Which box", required=True,
                      options=["Mystery Flower Box", "Mystery Flower & Plant Box",
                               "Mystery Plant Box"])) +
        field("Instagram or TikTok handle", placeholder="@yourhandle") +
        field("Link to your photo or reel", required=True,
              placeholder="Paste a link — or reply to our email with the file") +
        field("Caption", rows=4, placeholder="Tell us about the moment"))

    body = page_hero("Customer gallery", "#MysteryFlowerBox",
                     "<p>Every box that lands somewhere lovely, shared by the people who opened "
                     "it. Tag us and you could land here — and in the Golden Ticket draw.</p>",
                     ("Upload your photo", "#upload"))
    body += gallery_block("white", show_head=False)
    body += reactions_block("Reactions", "Caught on camera", "")
    body += section(
        '<div class="page-width--narrow" style="margin:0 auto" id="upload">' +
        head("Join the wall", "Upload your unboxing",
             "<p>Send us your photo or reel and we’ll add it to the gallery. Every upload earns "
             "50 loyalty points and an entry into this month’s draw.</p>") +
        demo_form(upload_fields, "Send my photo", "Got it — thank you!",
                  "Our team reviews uploads daily. We’ll email you when yours goes live.",
                  "By uploading you give us permission to share your photo on our website and "
                  "social channels. We’ll always credit you by first name and town.") +
        "</div>", "cream")
    body += cta_band("Want to be on this wall?",
                     "<p>Order a box, open it on camera, tag #MysteryFlowerBox.</p>")
    page("gallery", "Customer gallery", body)


def build_find_a_box():
    items, pins = [], []
    for i, (name, addr, town, post, hours, stock, x, y) in enumerate(C.STOCKISTS):
        label = {"high": "Boxes in stock today", "low": "Low stock — call ahead",
                 "out": "Sold out, restocking soon"}[stock]
        items.append(
            '<button class="locator__item" type="button" data-locator-item="s%d" '
            'data-search="%s %s %s %s"><h4>%s</h4><p>%s, %s</p><p class="small">%s</p>'
            '<span class="locator__stock" data-level="%s">%s</span></button>'
            % (i, name, addr, town, post, name, addr, post, hours, stock, label))
        pins.append(
            '<button class="locator__pin" type="button" data-locator-pin="s%d" '
            'style="left:%d%%;top:%d%%" aria-label="%s">%s<span>%s</span></button>'
            % (i, x, y, name, icon("pin"), town))

    locator = (
        '<div class="locator" data-locator><div>'
        '<label class="field"><span>Search by town, postcode or retailer</span>'
        '<input type="search" data-locator-search placeholder="e.g. Leeds or LS1" '
        'aria-label="Search stockists"></label>'
        '<div class="locator__list">%s'
        '<p class="muted small" data-locator-none hidden>No stockists match that search — but we '
        "deliver everywhere.</p></div></div>"
        '<div class="locator__map">%s%s</div></div>'
        % ("".join(items),
           art("art-pattern", "art", "", extra='style="position:absolute;inset:0;width:100%;'
                                               'height:100%;opacity:.35"'),
           "".join(pins)))

    register_fields = two_col(
        field("Your name", required=True), field("Email address", "email", required=True),
        field("Box code (on the QR label)", placeholder="MFB-000000"),
        field("Where did you buy it?", placeholder="Store and town"))

    retailer_fields = BASE_FIELDS + two_col(
        field("Number of stores", required=True, placeholder="e.g. 12"),
        field("Regions covered", placeholder="e.g. North West and Yorkshire")) + field(
        "Weekly volume expected", required=True,
        options=["Under 50 boxes", "50–250 boxes", "250–1,000 boxes", "1,000+ boxes"]) + field(
        "Anything else we should know", rows=4)

    body = page_hero("Find a box", "Where to grab a box today",
                     "<p>Our boxes land in supermarkets and independents across the UK. Bought "
                     "one in store? Register it to unlock your care guide, loyalty points and a "
                     "competition entry.</p>")
    body += section(locator + (
        '<div class="form-card" style="margin-top:40px"><h3>Bought a box in store?</h3>'
        '<p class="muted">Register it here to unlock your flower care guide, enter this month’s '
        "competition and collect loyalty points.</p>%s</div>"
        % demo_form(register_fields, "Register my box", "Thanks — box registered.",
                    "Check your email for your flower care guide and your competition entry.",
                    "One registration per box code.")), "cream")
    body += section(
        head("The QR code on your box", "One scan, a lot of extras") +
        '<div class="grid grid--4">%s</div>' % "".join([
            feature("qr", "Register your box",
                    "Turn a supermarket purchase into loyalty points and a competition entry."),
            feature("leaf", "Flower care guide",
                    "A short video showing exactly how to make your stems last."),
            feature("flower", "Meet the grower",
                    "Find out which Dutch nursery grew what’s in your hands."),
            feature("gift", "Partner offers",
                    "Unlock this month’s treats from the brands inside your box."),
        ]), "white")
    body += section(
        head("For retailers", "Stock Mystery Flower Box",
             "<p>High rotation, strong margin, and a product customers photograph. Tell us about "
             "your stores and we’ll send the trade pack.</p>") +
        '<div class="page-width--narrow" style="margin:0 auto">%s</div>'
        % demo_form(retailer_fields, "Request the trade pack", "Thanks — trade pack on its way.",
                    "Our retail team will be in touch within one working day."), "mist")
    body += cta_band("Can’t get to a store?",
                     "<p>We’ll bring the surprise to your door instead.</p>",
                     ("Order online", "#shop"))
    page("find-a-box", "Find a box", body)


def build_corporate():
    fields = BASE_FIELDS + two_col(
        field("What is the occasion", required=True,
              options=["Employee gifts", "Client gifts", "Events and hospitality",
                       "Conference or exhibition", "Something else"]),
        field("How many boxes", required=True,
              options=["Under 25", "25–100", "100–500", "500–2,000", "2,000+"])) + two_col(
        field("Delivery date needed", required=True, placeholder="e.g. week of 8 December"),
        field("Budget", required=True,
              options=["Under £1,000", "£1,000–£5,000", "£5,000–£25,000", "£25,000+"])) + field(
        "Delivery to one address or many?", placeholder="e.g. 200 home addresses") + field(
        "Anything else", rows=4,
        placeholder="Personalised messages, branded inserts, allergy requirements…")

    body = page_hero("Corporate gifting", "The gift people actually talk about",
                     "<p>Employee thank-yous, client gifts, events and hospitality. One clear "
                     "price, no negotiation, and a moment worth filming.</p>",
                     ("Request a quote", "#quote"))
    body += section(
        head("Why it works at scale", "Better than a branded water bottle") +
        '<div class="grid grid--4">%s</div>' % "".join([
            feature("gift", "£35 a box",
                    "Simple budgeting. No tiers to argue about, no hidden delivery charges."),
            feature("truck", "Nationwide delivery",
                    "One list, hundreds of addresses, delivered on the date you choose."),
            feature("heart", "Personal messages",
                    "A printed card in every box, personalised per recipient if you want."),
            feature("recycle", "A story worth telling",
                    "Every box is rescued surplus — a gift with a sustainability line attached."),
        ]), "white")
    body += stats_block(
        [("50+", "boxes: bulk pricing applies"), ("14 days", "lead time for large orders"),
         ("100%", "of boxes carry your message"), ("1 invoice", "however many addresses")],
        "Corporate clients", "What companies send", "", "mist")
    body += section(
        '<div id="quote" class="anchor-offset">' +
        head("Request a quote", "Tell us what you need",
             "<p>Give us the shape of it and we’ll come back with a price and a delivery plan "
             "within one working day.</p>") +
        '<div class="page-width--narrow" style="margin:0 auto">%s</div></div>'
        % demo_form(fields, "Request a quote", "Thank you — quote request received.",
                    "Our corporate team will reply within one working day with pricing and "
                    "available dates."), "cream")
    body += section(head("Corporate FAQ", "The practical bits") +
                    '<div class="prose-narrow">%s</div>' % accordion(C.CORPORATE_FAQ), "white")
    body += cta_band("Want to try one first?",
                     "<p>Order a single box and see exactly what your team would get.</p>",
                     ("Order a sample box", "#shop"))
    page("corporate", "Corporate gifting", body)


def build_partnerships():
    fields = BASE_FIELDS + two_col(
        field("What are you interested in", required=True,
              options=["Product sampling", "Printed advertising", "Sponsored gift",
                       "Competition", "Something else"]),
        field("Expected campaign volume", required=True,
              options=["Under 10,000 boxes", "10,000–50,000 boxes", "50,000–250,000 boxes",
                       "250,000+ boxes"])) + two_col(
        field("Target audience", required=True, placeholder="e.g. women 25–45, UK, gift buyers"),
        field("Timing", required=True, placeholder="e.g. Mother’s Day 2027")) + two_col(
        field("Sample dimensions and weight", placeholder="e.g. 80 × 50 × 12mm, 30g"),
        field("Budget", required=True,
              options=["Under £5,000", "£5,000–£25,000", "£25,000–£100,000", "£100,000+"])
    ) + field("Campaign objectives", rows=4)

    cases = "".join(
        '<article class="shape-card" data-reveal>%s<div style="padding:24px">'
        '<span class="pill pill--turf">%s</span><h3 style="margin-top:14px">%s</h3>'
        '<p class="muted">%s</p></div></article>' % (art(a, "art art--square", n), r, n, t)
        for a, n, r, t in [
            ("art-grower-1", "Sampling campaign", "FMCG · 40,000 boxes",
             "A single-week sampling drop delivered a 31% QR redemption rate and 4,200 new email records."),
            ("art-grower-2", "Sponsored Golden Ticket", "Travel brand · 3 months",
             "Sponsoring the prize put the brand into every winner announcement, email and social post."),
            ("art-grower-3", "Co-branded competition", "Home &amp; lifestyle · 6 weeks",
             "Shared entry data delivered 11,000 opted-in records at a fraction of paid social cost."),
        ])

    body = page_hero("Brand partnerships", "Put your brand inside a moment people film",
                     "<p>Advertising, sampling, sponsored gifts and competitions — inside a box "
                     "that gets opened, photographed and shared.</p>",
                     ("Start an enquiry", "#enquiry"))
    body += stats_block(C.PARTNER_STATS, "The audience", "Why brands come to us",
                        "<p>A highly engaged, gift-minded audience who open our boxes on "
                        "camera.</p>", "mist")
    body += section(
        head("What you can buy", "Four ways to be in the box",
             "<p>Everything is measurable. You get scan data, redemption rates and campaign "
             "reporting.</p>") +
        '<div class="grid grid--4">%s</div>'
        % "".join('<div class="feature" data-reveal><span class="pill pill--sun">%s</span>'
                  '<h3 style="margin-top:14px">%s</h3><p>%s</p></div>' % o
                  for o in C.PARTNER_OFFERS), "white")
    body += section(
        '<div id="enquiry" class="anchor-offset">' +
        head("Partner enquiry", "Tell us about your campaign",
             "<p>The more you tell us, the faster we can come back with a rate and available "
             "slots.</p>") +
        '<div class="page-width--narrow" style="margin:0 auto">%s</div></div>'
        % demo_form(fields, "Send enquiry", "Thank you — we have your campaign brief.",
                    "Our commercial team will come back within one working day with availability "
                    "and a rate card.", "We’ll send the media kit and rate card with our reply."),
        "cream")
    body += section(head("Case studies", "Campaigns that worked") +
                    '<div class="grid grid--3">%s</div>' % cases, "meadow")
    body += cta_band("Want the media kit?",
                     "<p>Send an enquiry and we’ll attach the full rate card and audience data.</p>",
                     ("Start an enquiry", "#enquiry"), tone="raspberry")
    page("brand-partnerships", "Brand partnerships", body)


def build_investors():
    fields = two_col(field("Your name", required=True), field("Email", "email", required=True)) + \
        two_col(field("You are", required=True,
                      options=["Angel investor", "VC or institutional", "Strategic partner",
                               "Analyst or press", "Other"]),
                field("Fund or organisation", placeholder="Where you’re writing from")) + \
        field("What would you like to know", rows=4)

    body = page_hero("Investors", "A consumer platform, not a flower shop",
                     "<p>Mystery Flower Box connects supermarket retail, ecommerce, "
                     "subscriptions, loyalty and retail media into one measurable growth "
                     "engine.</p>", ("Contact the team", "#investor-contact"), tone="mist")
    body += stats_block(C.INVESTOR_STATS, "Performance", "The numbers", "", "white")
    body += section(
        '<div class="page-width--narrow" style="margin:0 auto"><h2>Company profile</h2>'
        '<div class="rte"><p>Mystery Flower Box buys surplus stock from Dutch growers and sells '
        "it as a fixed-price surprise box through supermarkets and direct ecommerce. The model "
        "removes choice paralysis, removes waste, and creates a product customers photograph and "
        "share.</p><h3>Revenue streams</h3><ul>"
        "<li>Direct ecommerce — one-off boxes and prepaid bundles</li>"
        "<li>Subscriptions — weekly, fortnightly and monthly rhythms</li>"
        "<li>Retail wholesale — supermarket and independent stockists</li>"
        "<li>Retail media — sampling, inserts, sponsorship and co-branded competitions</li>"
        "<li>Corporate gifting — employee and client programmes</li>"
        "<li>Future territory licensing</li></ul>"
        "<h3>Strategic priorities</h3><ul>"
        "<li>Convert supermarket purchasers into known digital customers via QR registration</li>"
        "<li>Build the largest first-party flower customer database in Europe</li>"
        "<li>Grow subscription share of revenue</li>"
        "<li>Monetise the box itself as a media channel</li></ul></div></div>", "cream")
    body += section(
        head("Growth plan", "Four phases") +
        '<div class="grid grid--4">%s</div>' % "".join([
            feature("sparkle", "Phase 1 · Commerce",
                    "Shop, checkout, subscriptions, CRM, analytics and retail QR registration."),
            feature("heart", "Phase 2 · Community",
                    "Gallery, reviews, referrals, rewards and automated lifecycle journeys."),
            feature("gift", "Phase 3 · Commercial",
                    "Partner marketplace, campaign reporting, corporate gifting, retail intelligence."),
            feature("pin", "Phase 4 · International",
                    "Multi-territory stores, licensing support and territory-specific integrations."),
        ]), "white")
    body += section(
        '<div id="investor-contact" class="anchor-offset">' +
        head("Investor contact", "Request the investor pack",
             "<p>Business plan, growth targets, unit economics and current fundraising "
             "position.</p>") +
        '<div class="page-width--narrow" style="margin:0 auto">%s</div></div>'
        % demo_form(fields, "Request the pack", "Thank you — request received.",
                    "We will be in touch to arrange a call and share the investor pack."), "mist")
    page("investors", "Investors", body)


def build_subscriptions():
    body = page_hero("Subscriptions", "A surprise on repeat",
                     "<p>Weekly, fortnightly or monthly. Pause, skip, upgrade or cancel "
                     "yourself — no emails, no phone calls, no awkward retention chat.</p>",
                     ("Choose a plan", "#shop"))
    body += plans_block("white", show_head=False)
    body += section(
        head("Self-service", "Everything you can do yourself") +
        '<div class="grid grid--4">%s</div>' % "".join([
            feature("truck", "Pause or skip",
                    "Going away? Skip a delivery or pause the whole plan from your account in two clicks."),
            feature("sparkle", "Change your no-list",
                    "Update the colours and varieties to leave out at any time — it applies from the next box."),
            feature("gift", "Upgrade or downgrade",
                    "Switch between weekly, fortnightly and monthly whenever you like."),
            feature("lock", "Cancel yourself",
                    "One button. No retention call, no hoops. We would rather you came back later."),
        ]), "cream")
    body += section(head("Subscription FAQ", "The details") +
                    '<div class="prose-narrow">%s</div>' % accordion(C.SUBSCRIPTION_FAQ), "white")
    body += cta_band("Start with one box",
                     "<p>Try a single surprise first. You can always switch to a plan "
                     "afterwards.</p>")
    page("subscriptions", "Subscriptions", body)


def build_competitions():
    entry_fields = two_col(field("First name", required=True),
                           field("Email address", "email", required=True)) + field(
        "Where did you hear about us?",
        options=["In a supermarket", "A QR code on a box", "Instagram or TikTok",
                 "A friend told me", "Somewhere else"])
    countdown = (
        '<div class="countdown" data-countdown="2026-12-31T23:59:59">'
        + "".join('<div class="countdown__unit"><div class="countdown__num" data-unit="%s">--</div>'
                  '<div class="countdown__label">%s</div></div>' % (k, l)
                  for k, l in [("d", "Days"), ("h", "Hours"), ("m", "Mins"), ("s", "Secs")])
        + "</div>")

    body = page_hero("Competitions &amp; Golden Tickets",
                     "There is something hiding in one box in every 250",
                     "<p>Free boxes for a year, grower tours, weekend breaks and limited-edition "
                     "blooms. Plus a monthly draw anyone can enter.</p>")
    body += golden_block("peony", show_cta=False)
    body += section(
        '<div class="center"><span class="eyebrow">This month’s draw</span>'
        "<h2>Win a year of Mystery Flower Boxes</h2>"
        '<div class="lede" style="max-width:680px;margin:0 auto 30px"><p>No purchase necessary. '
        "Enter once and you’re in every monthly draw from now on.</p></div>%s"
        '<div style="max-width:560px;margin:34px auto 0;text-align:left">%s</div></div>'
        % (countdown,
           demo_form(entry_fields, "Enter the draw", "You are in the draw. Good luck! 🎟️",
                     "We will email the winner on the closing date.",
                     "Open to UK residents 18+. No purchase necessary.")), "cream")
    body += section(
        '<div class="page-width--narrow" style="margin:0 auto"><h2>Competition terms</h2>'
        '<div class="rte">%s</div></div>' % C.COMPETITION_TERMS, "white")
    body += cta_band("Better odds if you open more boxes", tone="raspberry")
    page("competitions", "Competitions &amp; Golden Tickets", body)


def build_referral():
    rewards = "".join(
        '<div class="plan-card%s"><h3>%s</h3><div class="plan-card__price">%s</div>'
        '<p class="muted small">%s</p><ul>%s</ul>'
        '<a class="btn %sbtn--full" href="#shop">Start earning</a></div>'
        % (" plan-card--featured" if feat else "", pts, prize, note,
           "".join("<li>%s</li>" % p for p in perks), "" if feat else "btn--secondary ")
        for pts, prize, note, perks, feat in [
            ("250 points", "£5 off", "any box",
             ["Applied at checkout", "Stacks with other offers", "Never expires"], False),
            ("500 points", "Free delivery", "for three months",
             ["Automatic at checkout", "Works with subscriptions"], False),
            ("1,000 points", "A free box", "any of the three",
             ["Your exclusions still apply", "Send it to someone else if you like"], True),
            ("2,500 points", "Limited edition", "members only",
             ["Seasonal one-off boxes", "Never sold publicly"], False),
        ])

    body = page_hero("Refer a friend", "Give £10, get a free box",
                     "<p>Share your link, your friend saves £10 on their first surprise, and "
                     "after three referrals your next box is on us.</p>", tone="sand")
    body += section(
        '<div class="split split--reverse"><div class="split__media">%s</div><div>'
        "<h2>How it works</h2><div class=\"lede\"><p>Sign in to your account and we’ll generate "
        "your personal link. Share it however you like — message, email, or your stories. We "
        "track everything in your referral dashboard.</p></div>"
        '<div class="form-card" style="margin-top:26px;padding:22px">'
        '<span class="field-label">Your referral link</span><div class="cluster">'
        '<code style="flex:1;min-width:200px;word-break:break-all">mysteryflowerbox.com/r/your-name</code>'
        '<button class="btn btn--sm" type="button" data-copy="mysteryflowerbox.com/r/your-name">'
        "Copy link</button></div></div>"
        '<div class="stat-row" style="margin-top:26px">%s</div></div></div>'
        % (art("art-gallery-11", "art art--square", "Unboxing with friends"),
           "".join('<div><div class="stat__value">%s</div><div class="stat__label">%s</div></div>'
                   % s for s in [("£10", "off for your friend"), ("3", "referrals to a free box"),
                                 ("18k", "boxes given free so far"), ("∞", "referrals allowed")])),
        "white")
    body += section(
        head("Loyalty", "Points for everything you already do") +
        '<div class="grid grid--4">%s</div>' % "".join([
            feature("gift", "Buy a box", "35 points every time — one point per pound."),
            feature("star", "Leave a review", "50 points, and more if you add a photo."),
            feature("heart", "Upload to the gallery", "50 points and an entry into the monthly draw."),
            feature("sparkle", "Refer a friend", "250 points when they open their first box."),
        ]), "cream")
    body += section(head("Spend them", "What points get you") +
                    '<div class="grid grid--4">%s</div>' % rewards, "white")
    body += cta_band("Start earning today")
    page("refer-a-friend", "Refer a friend", body)


def build_faq():
    body = page_hero("Help", "Frequently asked questions",
                     "<p>Everything about boxes, exclusions, delivery, subscriptions and the "
                     "rest. Still stuck? We answer emails quickly.</p>",
                     ("Contact us", "#contact"))
    tones = ["white", "cream", "white"]
    for i, (title, items) in enumerate(C.FAQ_GROUPS):
        body += section(head(title, "") + '<div class="prose-narrow">%s</div>' % accordion(items),
                        tones[i % len(tones)])
    body += cta_band("Still have a question?",
                     "<p>We answer every email, usually the same day.</p>",
                     ("Contact us", "#contact"))
    page("faq", "FAQ", body)


def build_contact():
    fields = two_col(field("Your name", required=True),
                     field("Email address", "email", required=True)) + two_col(
        field("What is this about", required=True,
              options=["My order", "Subscriptions", "Retail or stockists",
                       "Brand partnerships", "Press", "Something else"]),
        field("Order number (if you have one)", placeholder="#1234")) + field(
        "Your message", rows=5, required=True)

    body = page_hero("Contact", "Talk to a human",
                     "<p>Order questions, partnerships, press or something that doesn’t fit a "
                     "box — send it here and we’ll reply, usually the same day.</p>")
    body += section(
        '<div class="page-width--narrow" style="margin:0 auto">' +
        head("", "Send us a message") +
        demo_form(fields, "Send message", "Message received.",
                  "We reply to every message, usually the same working day.",
                  "Prefer email? %s" % C.BRAND["email"]) + "</div>", "white")
    body += section(head("Quick answers", "The things people ask most") +
                    '<div class="prose-narrow">%s</div>' % accordion([
                        ("Where is my order?",
                         "Check your dispatch email for tracking, or sign in to your account. If "
                         "it’s more than a day late, message us and we’ll chase it."),
                        ("How do I cancel a subscription?",
                         "From your account, in two clicks — no need to contact us at all."),
                        ("My flowers didn’t last.",
                         "Send a photo within 48 hours and we’ll put it right under our 7-day "
                         "freshness promise."),
                    ]) +
                    '<div class="cluster cluster--center" style="margin-top:36px">%s</div>'
                    % btn("Full FAQ", "#faq", "secondary"), "cream")
    page("contact", "Contact", body)


def build_about():
    body = page_hero("About us", "Customers don’t pick flowers. They buy the surprise.",
                     "<p>Mystery Flower Box turns surplus flowers into fun, surprise-filled "
                     "boxes supporting Dutch flower growers. It’s not a florist — it’s a viral, "
                     "social-first consumer brand built on sustainability, value and "
                     "excitement.</p>")
    body += section(
        '<div class="page-width--narrow" style="margin:0 auto">'
        "<h2>Think blind boxes, mystery toys, lucky dips</h2>"
        '<div class="rte">%s</div></div>' % C.ABOUT_STORY, "white")
    body += section(
        head("What we are", "Fun, bold, colourful, sustainable") +
        '<div class="grid grid--4">%s</div>' % "".join([
            feature("recycle", "Sustainable by design",
                    "Our whole business exists because flowers were being wasted. Every box is a rescue."),
            feature("sparkle", "High value",
                    "£35 buys far more flower than £35 normally does. That’s the entire point."),
            feature("heart", "Social first",
                    "Our customers film the unboxing. We built the brand around that moment."),
            feature("leaf", "Grower backed",
                    "We pay Dutch growers fairly for stock that had nowhere else to go."),
        ]), "cream")
    body += growers_block()
    body += cta_band("A surprise of blooms awaits")
    page("about", "About us", body)


def build_news():
    body = page_hero("From the packhouse", "Latest news",
                     "<p>Grower stories, flower care and what happens between the auction floor "
                     "and your doormat.</p>")
    body += section('<div class="grid grid--3">%s</div>'
                    % "".join(article_card(a) for a in C.ARTICLES), "cream")
    page("news", "Latest news", body)

    for index, a in enumerate(C.ARTICLES):
        parts = []
        for kind, value in a["body"]:
            if kind == "p":
                parts.append("<p>%s</p>" % value)
            elif kind == "h2":
                parts.append("<h2>%s</h2>" % value)
            elif kind in ("ul", "ol"):
                parts.append("<%s>%s</%s>" % (kind, "".join("<li>%s</li>" % v for v in value), kind))
        nxt = C.ARTICLES[(index + 1) % len(C.ARTICLES)]
        art_body = (
            '<div class="page-width page-width--narrow">'
            '<nav class="breadcrumbs"><a href="#news">Latest news</a> / <span>%s</span></nav>'
            '<span class="eyebrow">%s · %s</span><h1>%s</h1>%s'
            '<div class="rte">%s</div>'
            '<div class="cluster" style="margin-top:36px">'
            '<a class="btn btn--sm btn--secondary" href="#%s">Next: %s</a>'
            '<a class="btn btn--sm" href="#shop">Surprise Me!</a></div></div>'
            % (a["title"], a["date"], a["tag"], a["title"],
               '<div style="border-radius:var(--radius-lg);overflow:hidden;margin:24px 0 32px">%s</div>'
               % art(a["art"], "art", a["title"]),
               "".join(parts), nxt["slug"], nxt["title"]))
        page(a["slug"], a["title"],
             '<section class="section section--cream">%s</section>' % art_body)


def build_legal():
    for p in C.LEGAL_PAGES:
        body = page_hero(p["eyebrow"], p["title"], tone="mist")
        body += section('<div class="page-width--narrow" style="margin:0 auto">'
                        '<div class="rte">%s</div></div>' % p["body"], "white")
        page(p["slug"], p["title"], body)


def build_basket():
    body = section(
        "<h1>Your basket</h1>"
        '<div data-basket-empty><div class="empty-state">%s<h3>Your basket is empty</h3>'
        '<p class="muted">Three boxes. One price. Endless surprises.</p>%s</div></div>'
        '<div data-basket-filled hidden><div data-basket-list></div>'
        '<div class="cart-footer"><div>'
        '<div class="muted small">Delivery and any discounts are calculated at checkout.</div>'
        '<div class="cart-total" data-basket-total>£0.00</div>'
        '<div class="cluster" style="justify-content:flex-end;margin-top:16px">'
        '<a class="btn btn--secondary" href="#shop">Keep shopping</a>'
        '<button class="btn btn--ghost" type="button" data-basket-clear>Empty basket</button>'
        '<button class="btn btn--lg" type="button" data-checkout>Checkout</button></div>'
        "</div></div></div>"
        % (icon("gift"), btn("Surprise Me!", "#shop", "", "lg")), "cream")
    page("basket", "Your basket", body)


def build_not_found():
    body = section(
        '<div class="center"><div style="max-width:320px;margin:0 auto 20px">%s</div>'
        "<h1>This box is empty</h1>"
        '<p class="lede" style="max-width:520px;margin:0 auto 26px">We cannot find that page — '
        "but we can find you some flowers.</p>"
        '<div class="cluster cluster--center">%s%s</div></div>'
        % (art("art-product-flower-box", "art art--square", ""),
           btn("Surprise Me!", "#shop", "", "lg"),
           btn("Back home", "#home", "secondary", "lg")), "cream")
    page("not-found", "Page not found", body)


# ------------------------------------------------------------- chrome -------

NAV = [
    ("Shop", "#shop", [
        ("Mystery Flower Box", "#mystery-flower-box"),
        ("Mystery Flower &amp; Plant Box", "#mystery-flower-and-plant-box"),
        ("Mystery Plant Box", "#mystery-plant-box"),
        ("Subscriptions", "#subscriptions"),
    ]),
    ("How it works", "#how-it-works", [
        ("How it works", "#how-it-works"),
        ("Flower care", "#flower-care"),
        ("Meet the growers", "#about"),
        ("FAQ", "#faq"),
    ]),
    ("Gallery", "#gallery", [
        ("Customer gallery", "#gallery"),
        ("Competitions &amp; Golden Tickets", "#competitions"),
        ("Refer a friend", "#refer-a-friend"),
        ("Latest news", "#news"),
    ]),
    ("Find a box", "#find-a-box", []),
    ("Business", "#corporate", [
        ("Corporate gifting", "#corporate"),
        ("Brand partnerships", "#brand-partnerships"),
        ("Investors", "#investors"),
    ]),
    ("About", "#about", []),
]

FOOTER_SHOP = [
    ("All boxes", "#shop"), ("Mystery Flower Box", "#mystery-flower-box"),
    ("Mystery Flower &amp; Plant Box", "#mystery-flower-and-plant-box"),
    ("Mystery Plant Box", "#mystery-plant-box"), ("Subscriptions", "#subscriptions"),
    ("Refer a friend", "#refer-a-friend"), ("Competitions", "#competitions"),
]

FOOTER_COMMERCIAL = [
    ("Corporate gifting", "#corporate"), ("Brand partnerships", "#brand-partnerships"),
    ("Investors", "#investors"), ("Find a box", "#find-a-box"), ("Contact", "#contact"),
    ("FAQ", "#faq"), ("Delivery &amp; returns", "#delivery-and-returns"),
    ("Flower care", "#flower-care"), ("Terms &amp; conditions", "#terms-and-conditions"),
    ("Privacy notice", "#privacy-notice"),
]


def header(logo_uri):
    nav = []
    for title, href, children in NAV:
        panel = ""
        if children:
            panel = '<div class="site-nav__panel">%s</div>' % "".join(
                '<a href="%s">%s</a>' % (h, t) for t, h in children)
        nav.append('<div class="site-nav__item"><a class="site-nav__link" href="%s">%s%s</a>%s</div>'
                   % (href, title, (" " + icon("chevron")) if children else "", panel))

    mobile = []
    for title, href, children in NAV:
        mobile.append('<a class="is-parent" href="%s">%s</a>' % (href, title))
        for t, h in children:
            mobile.append('<a class="mobile-nav__child" href="%s">%s</a>' % (h, t))
    mobile.append('<a href="#basket">Basket</a>')

    return (
        '<div class="demo-note">Interactive preview of the Mystery Flower Box storefront — '
        "<strong>every page and link works offline</strong>. Orders are not taken here.</div>"
        '<header class="site-header"><div class="page-width site-header__inner">'
        '<a class="site-header__logo" href="#home">'
        '<img class="logo-img" src="%s" alt="Mystery Flower Box" width="760" height="369" '
        'style="--logo-w:170px"></a>'
        '<nav class="site-nav" aria-label="Main">%s</nav>'
        '<div class="header-actions">%s'
        '<a class="icon-btn" href="#basket" aria-label="Basket">%s'
        '<span class="cart-count" data-basket-count hidden>0</span></a>'
        '<button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-expanded="false" '
        'aria-controls="mobile-nav" aria-label="Menu">%s</button></div></div>'
        '<div class="mobile-nav" id="mobile-nav">%s</div></header>'
        % (logo_uri, "".join(nav), btn("Surprise Me!", "#shop", "", "sm"),
           icon("cart"), icon("menu"), "".join(mobile)))


def footer(logo_white_uri):
    def column(heading, links):
        return "<div><h4>%s</h4><ul>%s</ul></div>" % (
            heading, "".join('<li><a href="%s">%s</a></li>' % (h, t) for t, h in links))

    return (
        '<footer class="site-footer"><div class="page-width"><div class="site-footer__grid">'
        '<div><div class="site-footer__logo">'
        '<img src="%s" alt="Mystery Flower Box" width="760" height="370" style="width:190px"></div>'
        "<p>Mystery Flower Box turns surplus Dutch flowers into surprise-filled boxes. Less "
        "waste, more joy, one clear price.</p>"
        '<div class="social" style="margin-top:18px">%s%s%s%s</div></div>'
        "%s%s"
        '<div><h4>Never miss a drop</h4><p class="small">Early access to limited boxes, Golden '
        "Ticket news and 10%% off your first surprise.</p>"
        '<form data-demo-form><div data-form-fields>'
        '<input type="email" placeholder="you@example.com" aria-label="Email address" required>'
        '<button class="btn btn--sm btn--full" type="submit" style="margin-top:10px">Join the '
        "club</button></div>"
        '<div class="form-success" hidden data-form-success style="color:var(--charcoal)">'
        "<strong>You are on the list.</strong> Watch your inbox 🌸</div></form></div></div>"
        '<div class="site-footer__bottom"><span>&copy; 2026 Mystery Flower Box. All rights '
        "reserved. Mystery Flower Box™</span>"
        '<span class="small">%s · %s</span></div></div></footer>'
        % (logo_white_uri,
           '<a href="#gallery" aria-label="Instagram">%s</a>' % icon("instagram"),
           '<a href="#gallery" aria-label="TikTok">%s</a>' % icon("tiktok"),
           '<a href="#gallery" aria-label="Facebook">%s</a>' % icon("facebook"),
           '<a href="#gallery" aria-label="Pinterest">%s</a>' % icon("pinterest"),
           column("Shop", FOOTER_SHOP), column("Commercial", FOOTER_COMMERCIAL),
           C.BRAND["email"], C.BRAND["instagram"]))


# ------------------------------------------------------------------ build ---

def main():
    load_icons()
    build_sprite()

    build_home()
    build_shop()
    for p in C.PRODUCTS:
        build_product(p)
    build_how_it_works()
    build_gallery()
    build_find_a_box()
    build_subscriptions()
    build_corporate()
    build_partnerships()
    build_investors()
    build_competitions()
    build_referral()
    build_faq()
    build_contact()
    build_about()
    build_news()
    build_legal()
    build_basket()
    build_not_found()

    css = open(os.path.join(ROOT, "sitefile", "app.css")).read()
    js = open(os.path.join(ROOT, "sitefile", "app.js")).read()
    logo = data_uri("mfb-logo.png")
    logo_white = data_uri("mfb-logo-white.png")
    favicon = "data:image/svg+xml;base64," + base64.b64encode(
        open(os.path.join(ASSETS, "mfb-favicon.svg"), "rb").read()).decode()

    html = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FF80C3">
<title>Mystery Flower Box — surprise flower boxes, £35</title>
<meta name="description" content="Mystery Flower Box turns surplus Dutch flowers into surprise-filled boxes. One clear price, three boxes, and you tell us what to leave out.">
<link rel="icon" href="%(favicon)s">
<style>%(fonts)s%(css)s</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>%(sprite)s</defs></svg>
%(header)s
<main id="main">%(pages)s</main>
%(footer)s
<script>%(js)s</script>
</body>
</html>
""" % {
        "favicon": favicon,
        "fonts": font_face(),
        "css": css,
        "sprite": "".join(SPRITE),
        "header": header(logo),
        "pages": "".join(PAGES),
        "footer": footer(logo_white),
        "js": js,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    ids = re.findall(r'<div class="page" id="([^"]+)"', html)
    print("pages: %d" % len(ids))
    print("artwork: %d symbols" % len(SPRITE))
    print("size: %.0f KB" % (len(html.encode("utf-8")) / 1024.0))
    print("→ %s" % OUT)
    return ids, html


if __name__ == "__main__":
    main()
