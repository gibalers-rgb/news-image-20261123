#!/usr/bin/env python3
"""Compose the front page for make.fun news-image-20261123.

The page is a 1024x1024 newspaper front page for Monday 23 November
2026. A painted illustration of the day's biggest story — a tanker
burning in the Strait of Hormuz — sits under the masthead, and below
it six short cards carry the other stories that defined the day. All
the lettering is drawn with PIL, so the text stays sharp at any size.

What the page says comes from the reporting of 23 November 2026
itself: the Hormuz/Bahrain escalation and the two tankers struck
(CNBC Indonesia / jawawa, strategicenergymap, theworldopinion); the
COP31 talks in Antalya collapsing after the EU rejected a draft that
left fossil fuels out (UN News, CNN, Le Monde); a Russian drone
hitting a home in Dymer, Kyiv region, with 14 people missing
(stablenews, spyglassnews); South Korea's education minister Choi
Kyo-jin stepping down over an AI exam-cheating scandal (stablenews,
spyglassnews); cost-of-living marches in Lisbon and across Europe
(englishnewsroom); and a confectionery factory fire west of Jakarta
that left three dead and 36 missing (spyglassnews, englishnewsroom).

Where the reporting disagreed, the page only prints what was
confirmed on the day: Bahrain accused Iran of hitting a civilian
industrial site (the IRGC claim of striking US bases was not
verified), and the factory toll is the three dead and 36 missing
reported that day.

Run it with:  python3 compose.py     (writes entry.png beside it)
"""

import hashlib
import os
import sys
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(
    HERE,
    "assets",
    "media-generation-hormuz-hero-20261123-0-9a14cb43-b8e7-4190-a9a1-ff4b76e3145a.webp",
)
OUT = os.path.join(HERE, "entry.png")

PAGE = (1024, 1024)
PAPER = (250, 246, 236)          # warm newsprint cream
CARD = (255, 253, 247)           # card white
TEXT = (26, 30, 40)              # near-black ink
MUTED = (96, 102, 116)           # body grey
DARK_BLUE = (20, 33, 61)         # masthead navy
BRASS = (198, 160, 38)           # gold rule
EDGE = (214, 209, 194)           # card hairline
CAPTION_BG = (16, 20, 30)        # caption bar

TITLE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BODY_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


@dataclass
class Story:
    section: str
    colour: tuple
    headline: str
    deck: str


DAY_STORIES = [
    Story(
        "WAR · STRAIT OF HORMUZ",
        (178, 34, 34),
        "WAR WIDENS AT HORMUZ",
        "Iran strikes a site in Bahrain, Houthis target Saudi Arabia, "
        "and two tankers are hit leaving the strait.",
    ),
    Story(
        "CLIMATE · ANTALYA",
        (34, 110, 58),
        "COP31 DEAL REJECTED",
        "The EU and other nations reject a draft pact that omits fossil "
        "fuels; the summit ends with no agreement.",
    ),
    Story(
        "WAR · KYIV REGION",
        (88, 58, 118),
        "14 MISSING IN KYIV STRIKE",
        "A Russian drone hits a residential building; at least 14 people "
        "are missing, Zelenskiy says.",
    ),
    Story(
        "POLITICS · SEOUL",
        (28, 88, 138),
        "MINISTER QUITS IN AI SCANDAL",
        "South Korea's education minister resigns over an AI cheating "
        "scandal.",
    ),
    Story(
        "EUROPE · LISBON",
        (172, 82, 22),
        "LISBON MARCHES ON COSTS",
        "Thousands take to the streets as the rising cost of living fuels "
        "anger across Portugal.",
    ),
    Story(
        "DISASTER · INDONESIA",
        (14, 118, 100),
        "FACTORY FIRE: 36 MISSING",
        "Three dead and 36 missing after a fire at a factory in Indonesia.",
    ),
]

HERO_CAPTION = "STRAIT OF HORMUZ — Tankers ablaze as the Iran–US war widens"
PAGE_FOOTER = (
    "Six stories that defined the day — Monday 23 November 2026 "
    "· as reported by the world's press"
)


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(img, width, height):
    """Crop `img` to the wanted aspect ratio, then scale it to size.

    Stretching a wide painting into a short strip would squash the
    tanker and the warships, so the sides (or top and bottom) are
    trimmed first and the proportions stay true.
    """
    w, h = img.size
    ratio = width / height
    if w / h > ratio:
        keep = int(h * ratio)
        start = (w - keep) // 2
        img = img.crop((start, 0, start + keep, h))
    else:
        keep = int(w / ratio)
        start = (h - keep) // 2
        img = img.crop((0, start, w, start + keep))
    return img.resize((width, height), Image.LANCZOS)


def wrap(draw, text, fnt, width):
    """Break `text` into as few lines as fit inside `width` pixels."""
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered(draw, text, fnt, y, fill):
    """Draw `text` centred across the whole page at height `y`."""
    x = PAGE[0] // 2 - draw.textlength(text, font=fnt) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def grid_box(col, row):
    """The box of one card in the two-column, three-row grid."""
    margin, gap, top = 24, 16, 452
    w = (PAGE[0] - 2 * margin - gap) // 2
    h = 164
    x = margin + col * (w + gap)
    y = top + row * (h + 12)
    return (x, y, x + w, y + h)


def draw_story_card(draw, box, number, story):
    """One card: coloured edge, numbered disc, section, headline, deck."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=EDGE, width=1)
    draw.rectangle([x0, y0 + 10, x0 + 6, y1 - 10], fill=story.colour)

    tx = x0 + 22
    inner = x1 - tx - 18

    disc = (x1 - 46, y0 + 12, x1 - 16, y0 + 42)
    draw.ellipse(disc, fill=story.colour)
    num = font(BOLD_FONT, 17)
    label = str(number)
    draw.text(
        (disc[0] + 15 - draw.textlength(label, font=num) / 2, y0 + 15),
        label,
        font=num,
        fill=(255, 255, 255),
    )

    draw.text((tx, y0 + 13), story.section,
              font=font(BOLD_FONT, 14), fill=story.colour)

    head = font(BOLD_FONT, 24)
    y = y0 + 40
    for line in wrap(draw, story.headline, head, inner)[:2]:
        draw.text((tx, y), line, font=head, fill=TEXT)
        y += 29

    body = font(BODY_FONT, 16)
    y += 5
    for line in wrap(draw, story.deck, body, inner)[:3]:
        draw.text((tx, y), line, font=body, fill=MUTED)
        y += 22


def build_page():
    page = Image.new("RGB", PAGE, PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead: a navy band with a gold rule, paper name and date.
    draw.rectangle([0, 0, PAGE[0], 92], fill=DARK_BLUE)
    draw.rectangle([0, 92, PAGE[0], 96], fill=BRASS)
    centered(draw, "THE WORLD IN ONE DAY", font(TITLE_FONT, 44), 8, PAPER)
    centered(draw, "MONDAY · 23 NOVEMBER 2026",
             font(BOLD_FONT, 24), 58, (222, 182, 74))

    # The hero painting, cropped to its band, with a caption strip.
    hero = Image.open(HERO).convert("RGB")
    page.paste(cover_crop(hero, PAGE[0], 340), (0, 96))
    draw = ImageDraw.Draw(page)
    draw.rectangle([0, 396, PAGE[0], 436], fill=CAPTION_BG)
    draw.rectangle([0, 436, PAGE[0], 440], fill=BRASS)
    centered(draw, HERO_CAPTION, font(BOLD_FONT, 21), 406, (247, 243, 234))

    # The six stories, two across and three down.
    for i, story in enumerate(DAY_STORIES):
        draw_story_card(draw, grid_box(i % 2, i // 2), i + 1, story)

    centered(draw, PAGE_FOOTER, font(BODY_FONT, 15), 992, MUTED)
    return page


def verify_gate(path):
    """The competition gate: a complete PNG, 1024x1024, at most 1 MiB.

    The file has to open with the PNG signature, decode fully (a cut
    file fails here rather than at the judge), and match the size the
    entrypoint promises.
    """
    with open(path, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"gate failed: {path} has no PNG signature")
    with Image.open(path) as im:
        if im.format != "PNG":
            sys.exit(f"gate failed: {path} is {im.format}, not PNG")
        im.load()
        if im.size != PAGE:
            sys.exit(f"gate failed: {path} is {im.size}, not {PAGE}")
    size = os.path.getsize(path)
    if size > 1024 * 1024:
        sys.exit(f"gate failed: {path} is {size} bytes, over 1 MiB")
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"gate ok: {path} {PAGE[0]}x{PAGE[1]} {size} bytes sha256={digest}")


def main():
    build_page().save(OUT, optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
    verify_gate(OUT)


if __name__ == "__main__":
    main()
