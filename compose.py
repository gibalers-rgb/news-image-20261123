#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261123.

A 1024x1024 newspaper front page summing up the world news of Monday
23 November 2026. The page is laid out from a painted hero illustration
of the day's lead story (a tanker ablaze in the Strait of Hormuz) plus
six short story cards, all text rendered with PIL so every word is crisp
and legible at small sizes.

Stories were checked against the 23 November 2026 reporting itself:
the Hormuz/Bahrain escalation and the two tankers hit (CNBC Indonesia /
jawawa, strategicenergymap, theworldopinion); the COP31 collapse in
Antalya with the EU rejecting a draft that omits fossil fuels (UN News,
CNN, Le Monde); the Russian drone strike on Dymer in the Kyiv region
with 14 missing (stablenews, spyglassnews); South Korea's education
minister Choi Kyo-jin resigning over the AI exam-cheating scandal
(stablenews, spyglassnews); cost-of-living marches in Lisbon and across
Europe (englishnewsroom); and the confectionery factory fire west of
Jakarta, three dead and 36 missing (spyglassnews, englishnewsroom).

Where reports conflict, the page states only what the reporting
confirms: Bahrain accused Iran of striking a civilian industrial site
(the IRGC's claim to have hit US bases is unverified), and the factory
fire toll is the three dead / 36 missing reported on the day.

Run:  python3 compose.py        (writes entry.png next to this file)
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
NEWS_CREAM = (250, 246, 236)
CARD_WHITE = (255, 253, 247)
INK = (26, 30, 40)
GREY = (96, 102, 116)
NAVY = (20, 33, 61)
GOLD = (198, 160, 38)
HAIRLINE = (214, 209, 194)
CAPTION_DARK = (16, 20, 30)

HERO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "media-generation-hormuz-hero-20261123-0-9a14cb43-b8e7-4190-a9a1-ff4b76e3145a.webp",
)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# (kicker, accent colour, headline, summary) — the six stories of the day.
STORIES = [
    (
        "WAR \u00b7 STRAIT OF HORMUZ",
        (178, 34, 34),
        "WAR WIDENS AT HORMUZ",
        "Iran strikes a site in Bahrain, Houthis target Saudi Arabia, "
        "and two tankers are hit leaving the strait.",
    ),
    (
        "CLIMATE \u00b7 ANTALYA",
        (34, 110, 58),
        "COP31 DEAL REJECTED",
        "The EU and other nations reject a draft pact that omits fossil "
        "fuels; the summit ends with no agreement.",
    ),
    (
        "WAR \u00b7 KYIV REGION",
        (88, 58, 118),
        "14 MISSING IN KYIV STRIKE",
        "A Russian drone hits a residential building; at least 14 people "
        "are missing, Zelenskiy says.",
    ),
    (
        "POLITICS \u00b7 SEOUL",
        (28, 88, 138),
        "MINISTER QUITS IN AI SCANDAL",
        "South Korea's education minister resigns over an AI cheating "
        "scandal.",
    ),
    (
        "EUROPE \u00b7 LISBON",
        (172, 82, 22),
        "LISBON MARCHES ON COSTS",
        "Thousands take to the streets as the rising cost of living fuels "
        "anger across Portugal.",
    ),
    (
        "DISASTER \u00b7 INDONESIA",
        (14, 118, 100),
        "FACTORY FIRE: 36 MISSING",
        "Three dead and 36 missing after a fire at a factory in Indonesia.",
    ),
]

CAPTION = "STRAIT OF HORMUZ \u2014 Tankers ablaze as the Iran\u2013US war widens"
FOOTER = (
    "Six stories that defined the day \u2014 Monday 23 November 2026 "
    "\u00b7 as reported by the world's press"
)


def load_font(path, size):
    return ImageFont.truetype(path, size)


def fit_cover(img, width, height):
    """Centre-crop `img` to the target aspect ratio, then scale to fit.

    A plain resize would squash a wide illustration into a short band;
    cropping first keeps the tanker and the warships at true proportions.
    """
    iw, ih = img.size
    want = width / height
    if iw / ih > want:  # too wide: trim the sides
        new_w = int(ih * want)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:  # too tall: trim top and bottom
        new_h = int(iw / want)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    return img.resize((width, height), Image.LANCZOS)


def split_lines(draw, text, fnt, max_width):
    """Greedy word wrap returning the lines of `text` that fit `max_width`."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred_text(draw, text, fnt, y, colour):
    draw.text(
        (PAGE_W // 2 - draw.textlength(text, font=fnt) / 2, y),
        text,
        font=fnt,
        fill=colour,
    )


def draw_card(draw, box, index, kicker, accent, headline, summary):
    """One story card: coloured spine, number disc, kicker, headline, text."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD_WHITE,
                           outline=HAIRLINE, width=1)
    draw.rectangle([x0, y0 + 10, x0 + 6, y1 - 10], fill=accent)

    text_x = x0 + 22
    inner_w = x1 - text_x - 18

    disc = (x1 - 46, y0 + 12, x1 - 16, y0 + 42)
    draw.ellipse(disc, fill=accent)
    num_font = load_font(SANS_BOLD, 17)
    label = str(index)
    draw.text(
        (disc[0] + 15 - draw.textlength(label, font=num_font) / 2, y0 + 15),
        label,
        font=num_font,
        fill=(255, 255, 255),
    )

    draw.text((text_x, y0 + 13), kicker,
              font=load_font(SANS_BOLD, 14), fill=accent)

    head_font = load_font(SANS_BOLD, 24)
    y = y0 + 40
    for line in split_lines(draw, headline, head_font, inner_w)[:2]:
        draw.text((text_x, y), line, font=head_font, fill=INK)
        y += 29

    body_font = load_font(SANS, 16)
    y += 5
    for line in split_lines(draw, summary, body_font, inner_w)[:3]:
        draw.text((text_x, y), line, font=body_font, fill=GREY)
        y += 22


def render():
    page = Image.new("RGB", (PAGE_W, PAGE_H), NEWS_CREAM)
    draw = ImageDraw.Draw(page)

    # Masthead: navy band, gold rule, paper name and date.
    draw.rectangle([0, 0, PAGE_W, 92], fill=NAVY)
    draw.rectangle([0, 92, PAGE_W, 96], fill=GOLD)
    centred_text(draw, "THE WORLD IN ONE DAY",
                 load_font(SERIF_BOLD, 44), 8, NEWS_CREAM)
    centred_text(draw, "MONDAY \u00b7 23 NOVEMBER 2026",
                 load_font(SANS_BOLD, 24), 58, (222, 182, 74))

    # Hero illustration, centre-cropped to the band, with a caption bar.
    hero = Image.open(HERO_PATH).convert("RGB")
    hero = fit_cover(hero, PAGE_W, 340)
    page.paste(hero, (0, 96))
    draw = ImageDraw.Draw(page)
    draw.rectangle([0, 396, PAGE_W, 436], fill=CAPTION_DARK)
    draw.rectangle([0, 436, PAGE_W, 440], fill=GOLD)
    centred_text(draw, CAPTION, load_font(SANS_BOLD, 21), 406,
                 (247, 243, 234))

    # Six story cards: two columns, three rows.
    margin, gap, top = 24, 16, 452
    card_w = (PAGE_W - 2 * margin - gap) // 2
    card_h = 164
    for i, (kicker, accent, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (card_w + gap)
        y0 = top + row * (card_h + 12)
        draw_card(draw, (x0, y0, x0 + card_w, y0 + card_h), i + 1,
                  kicker, accent, headline, summary)

    centred_text(draw, FOOTER, load_font(SANS, 15), 992, GREY)
    return page


def check_gate(path):
    """The kit gate: a whole PNG, at most 1024x1024 and at most 1 MiB.

    The file must start with the PNG signature, fully decode (a truncated
    file fails here, not at the judge), and match the declared dimensions.
    """
    with open(path, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"gate failed: {path} has no PNG signature")
    with Image.open(path) as im:
        if im.format != "PNG":
            raise SystemExit(f"gate failed: {path} is {im.format}, not PNG")
        im.load()  # decode every chunk: a truncated file raises here
        if im.size != (PAGE_W, PAGE_H):
            raise SystemExit(f"gate failed: {path} is {im.size}")
    size = os.path.getsize(path)
    if size > 1_048_576:
        raise SystemExit(f"gate failed: {path} is {size} bytes (> 1 MiB)")
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"gate ok: {path} {PAGE_W}x{PAGE_H} {size} bytes sha256={digest}")


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    render().save(out, optimize=True)
    print(f"wrote {out}")
    check_gate(out)


if __name__ == "__main__":
    main()
