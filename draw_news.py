#!/usr/bin/env python3
"""Draw a one-day world news infographic for Saturday 21 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1000
BG = "#0D1526"
CARD = "#17233A"
EDGE = "#2C3C5A"
WHITE = "#F5F7FB"
GREY = "#AEBBD0"
AMBER = "#FFC46B"
CORAL = "#FF7A6B"

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

STORIES = [
    ("MARKETS", "AI STOCKS PLUNGE",
     "Wall St -3.7%; S&P 500 and Dow in correction as AI spending doubts grow.",
     AMBER, "chart"),
    ("UKRAINE", "DRONES OVER UKRAINE",
     "400+ drones, 110 missiles; debris in Poland puts NATO on alert.",
     CORAL, "drone"),
    ("ENERGY", "STRAIT OF HORMUZ",
     "Six vessel attacks, a US drone downed; shipping still 65% below pre-war.",
     CORAL, "ship"),
    ("CLIMATE", "CLIMATE TALKS STALL",
     "COP31 in Antalya overruns as fossil fuels split the draft deal.",
     AMBER, "globe"),
    ("DIPLOMACY", "UK-EU RESET DEAL",
     "Biggest post-Brexit pacts signed in Brussels, easing trade and travel.",
     AMBER, "arrows"),
    ("SPACE", "MERCURY ORBIT",
     "BepiColombo reaches the planet after an eight-year ESA/JAXA voyage.",
     AMBER, "orbit"),
    ("DISASTER", "PERU EARTHQUAKE",
     "M6.7 quake in the central Andes sends people into Lima's streets.",
     CORAL, "quake"),
    ("HEALTH", "MEASLES STATUS LOST",
     "US loses elimination status; 7,700 cases and 13 deaths since 2025.",
     AMBER, "health"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, max_w, size, path=BOLD, floor=15):
    """Shrink a single line until it fits max_w."""
    while size > floor:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, floor)


def wrap(text, f, max_w, limit=2):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == limit:
                break
    if cur and len(lines) < limit:
        lines.append(cur)
    return lines


def glyph(kind, cx, cy, color):
    r = 18
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#1E2C46", outline=color, width=2)
    if kind == "chart":
        for i, h in enumerate((7, 11, 14, 17)):
            x = cx - 10 + i * 6
            draw.rectangle([x, cy + h - 11, x + 3, cy + h - 4], fill=color)
        draw.line([cx - 12, cy + 8, cx + 12, cy + 8], fill=color, width=2)
    elif kind == "drone":
        draw.rounded_rectangle([cx-6, cy-4, cx+6, cy+4], radius=2, fill=color)
        for sx in (-1, 1):
            for sy in (-1, 1):
                x, y = cx + sx * 12, cy + sy * 9
                draw.line([cx + sx * 5, cy + sy * 3, x, y], fill=color, width=2)
                draw.ellipse([x-3, y-3, x+3, y+3], outline=color, width=2)
    elif kind == "ship":
        draw.polygon([(cx-13, cy+2), (cx+13, cy+2), (cx+9, cy+9), (cx-9, cy+9)], fill=color)
        draw.rectangle([cx-2, cy-8, cx+2, cy+2], fill=color)
        for off in (-4, 4):
            draw.arc([cx-14, cy+5+off, cx+14, cy+11+off], 0, 180, fill=color, width=2)
    elif kind == "globe":
        draw.ellipse([cx-11, cy-11, cx+11, cy+11], outline=color, width=2)
        draw.line([cx-11, cy, cx+11, cy], fill=color, width=1)
        draw.arc([cx-6, cy-11, cx+6, cy+11], 90, 270, fill=color, width=1)
        draw.line([cx, cy-11, cx, cy+11], fill=color, width=1)
    elif kind == "arrows":
        draw.line([cx-13, cy-5, cx+5, cy-5], fill=color, width=3)
        draw.polygon([(cx+10, cy-5), (cx+3, cy-9), (cx+3, cy-1)], fill=color)
        draw.line([cx+13, cy+5, cx-5, cy+5], fill=color, width=3)
        draw.polygon([(cx-10, cy+5), (cx-3, cy+1), (cx-3, cy+9)], fill=color)
    elif kind == "orbit":
        draw.ellipse([cx-9, cy-9, cx+9, cy+9], fill=color)
        draw.ellipse([cx-16, cy-5, cx+16, cy+5], outline=color, width=2)
    elif kind == "quake":
        pts = [(cx-14, cy+2), (cx-8, cy+2), (cx-4, cy-9), (cx, cy+10),
               (cx+4, cy-6), (cx+8, cy+2), (cx+14, cy+2)]
        draw.line(pts, fill=color, width=3, joint="curve")
    elif kind == "health":
        draw.rectangle([cx-3, cy-11, cx+3, cy+11], fill=color)
        draw.rectangle([cx-11, cy-3, cx+11, cy+3], fill=color)
        for a in (0, 90, 180, 270):
            import math
            rad = math.radians(a)
            x, y = cx + int(15*math.cos(rad)), cy + int(15*math.sin(rad))
            draw.ellipse([x-2, y-2, x+2, y+2], fill=color)


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Header
draw.rectangle([0, 0, W, 7], fill=AMBER)
draw.text((46, 30), "WORLD NEWS  /  ONE DAY", font=font(BOLD, 23), fill=AMBER)
draw.text((46, 66), "SATURDAY 21 NOVEMBER 2026", font=font(BOLD, 43), fill=WHITE)
draw.text((46, 121), "Eight stories that shaped the day", font=font(REG, 21), fill=GREY)
draw.line([46, 150, W-46, 150], fill=EDGE, width=2)

# Cards
MARGIN, GAP, CARD_W, CARD_H, ROW_GAP, TOP = 46, 16, 446, 184, 16, 162
for i, (tag, headline, sub, accent, kind) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x = MARGIN + col * (CARD_W + GAP)
    y = TOP + row * (CARD_H + ROW_GAP)
    draw.rounded_rectangle([x, y, x+CARD_W, y+CARD_H], radius=14,
                           fill=CARD, outline=EDGE, width=2)
    draw.rounded_rectangle([x+1, y+16, x+6, y+CARD_H-16], radius=2, fill=accent)
    glyph(kind, x+42, y+38, accent)
    draw.text((x+70, y+29), tag, font=font(BOLD, 17), fill=accent)
    hf = fit(headline, CARD_W-42, 33)
    draw.text((x+22, y+62), headline, font=hf, fill=WHITE)
    sf = font(REG, 21)
    lines = wrap(sub, sf, CARD_W-42, limit=2)
    if len(" ".join(sub.split())) > len(" ".join(lines)):
        sf = font(REG, 19)
        lines = wrap(sub, sf, CARD_W-42, limit=2)
    for j, line in enumerate(lines):
        draw.text((x+22, y+106 + j*27), line, font=sf, fill=GREY)

footer = "21 NOVEMBER 2026  /  EIGHT STORIES  /  ONE WORLD"
ff = fit(footer, W-92, 18, path=BOLD, floor=13)
draw.text(((W - draw.textlength(footer, font=ff)) / 2, 962), footer, font=ff, fill=GREY)

img.save("/home/ejoy/makefun/newswork21/entry.png", optimize=True)
print("saved entry.png", img.size)
