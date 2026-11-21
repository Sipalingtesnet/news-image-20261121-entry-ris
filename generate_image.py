#!/usr/bin/env python3
"""THE WORLD TODAY -- newspaper front page for Saturday 21 November 2026.

Renders entry.png (1024x1024) using Pillow only.
Fully deterministic: no randomness, no timestamps, no network.
All paragraphs are wrapped to their boxes; fonts auto-shrink if needed
so no text is ever clipped.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 12  # minimum margin on every side

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 242, 231)
INK = (26, 26, 30)
NAVY = (19, 31, 58)
RED = (188, 32, 32)
GRAY = (105, 105, 110)
RULE = (70, 70, 76)
MAP_FILL = (228, 222, 205)
PANEL_BG = (250, 247, 239)
GOLD = (232, 196, 106)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def wrap(text, f, maxw):
    """Word-wrap text so every line fits maxw pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_paragraph(text, path, size, maxw, maxh, min_size=10):
    """Return (lines, font, line_height) guaranteed to fit maxw x maxh."""
    while size >= min_size:
        f = font(path, size)
        lh = int(size * 1.28)
        lines = wrap(text, f, maxw)
        if len(lines) * lh <= maxh and all(
            d.textlength(ln, font=f) <= maxw for ln in lines
        ):
            return lines, f, lh
        size -= 1
    raise RuntimeError("text does not fit even at minimum size: " + text[:40])


def draw_paragraph(text, x, y, maxw, maxh, path=SANS, size=17, fill=INK):
    lines, f, lh = fit_paragraph(text, path, size, maxw, maxh)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def center_text(text, cx, y, f, fill):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- masthead
MAST_TOP, MAST_BOT = M, 118
d.rectangle([M, MAST_TOP, W - M, MAST_BOT], fill=NAVY)
center_text("THE WORLD TODAY", W / 2, 22, font(SERIF_B, 64), (255, 255, 255))
d.line([M + 24, 96, W - M - 24, 96], fill=GOLD, width=2)
center_text("SATURDAY 21 NOVEMBER 2026", W / 2, 99, font(SANS_B, 17), GOLD)

# ---------------------------------------------------------------- lead story
LEAD_TOP = 126
d.text((M, LEAD_TOP), "Missiles Land in Poland", font=font(SERIF_B, 34), fill=INK)
d.line([M, 172, W - M, 172], fill=RULE, width=2)

BODY_TOP, BODY_BOT = 182, 434
TEXT_W = 560
lead_body = (
    "Two Russian missiles and a suspected drone came down in Poland. "
    "Poland called it a deliberate provocation; NATO called it a grave "
    "violation of its airspace."
)
draw_paragraph(lead_body, M, BODY_TOP, TEXT_W, BODY_BOT - BODY_TOP,
               path=SANS, size=17)

# --- drawn scene: schematic map of Poland with two red impact markers
MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 592, BODY_TOP - 4, W - M, BODY_BOT
d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], outline=RULE, width=1, fill=MAP_FILL)

# rough Poland outline in unit coordinates (x right, y down)
POLAND = [
    (0.10, 0.16), (0.28, 0.07), (0.52, 0.04), (0.72, 0.09), (0.90, 0.12),
    (0.94, 0.32), (0.89, 0.52), (0.94, 0.72), (0.82, 0.90), (0.58, 0.95),
    (0.32, 0.90), (0.14, 0.80), (0.06, 0.56), (0.09, 0.32),
]
pad = 26
mw = MAP_X1 - MAP_X0 - 2 * pad
mh = MAP_Y1 - MAP_Y0 - 2 * pad - 18  # leave room for caption
poly = [(MAP_X0 + pad + ux * mw, MAP_Y0 + pad + uy * mh) for ux, uy in POLAND]
d.polygon(poly, fill=(238, 233, 218), outline=INK)
d.line(poly + [poly[0]], fill=INK, width=3, joint="curve")

center_text("POLAND", (MAP_X0 + MAP_X1) / 2, MAP_Y0 + 6, font(SANS_B, 15), GRAY)

# two impact markers (red rings with a cross), plus faint approach lines
for ux, uy in [(0.66, 0.34), (0.52, 0.58)]:
    px = MAP_X0 + pad + ux * mw
    py = MAP_Y0 + pad + uy * mh
    d.line([MAP_X1 - 8, py - 30, px, py], fill=(210, 120, 110), width=2)
    r = 11
    d.ellipse([px - r, py - r, px + r, py + r], outline=RED, width=3)
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.line([px - r - 5, py, px + r + 5, py], fill=RED, width=2)
    d.line([px, py - r - 5, px, py + r + 5], fill=RED, width=2)

center_text("Impact sites (schematic)", (MAP_X0 + MAP_X1) / 2,
            MAP_Y1 - 22, font(SANS, 13), GRAY)

# ---------------------------------------------------------------- 2x2 grid
GRID_TOP = 446
PANEL_W = (W - 2 * M - 12) // 2  # 494
PANEL_H = 180
ROW_GAP = 12
PX = [M, M + PANEL_W + 12]
PY = [GRID_TOP, GRID_TOP + PANEL_H + ROW_GAP]


def panel_frame(x, y, title):
    d.rectangle([x, y, x + PANEL_W, y + PANEL_H], fill=PANEL_BG, outline=RULE, width=2)
    d.text((x + 10, y + 7), title, font=font(SERIF_B, 22), fill=INK)
    d.line([x + 10, y + 38, x + PANEL_W - 10, y + 38], fill=RULE, width=1)


def panel_text(x, y, text):
    tx = x + 152
    tw = PANEL_W - 162
    draw_paragraph(text, tx, y + 48, tw, PANEL_H - 58, path=SANS, size=16)


ILLO_X = 18  # illustration offset inside panel
ILLO_Y = 50
ILLO_W, ILLO_H = 122, 118

# --- panel 1: Markets (falling chart)
x, y = PX[0], PY[0]
panel_frame(x, y, "Markets Slump")
ax, ay = x + ILLO_X, y + ILLO_Y
d.line([ax, ay, ax, ay + ILLO_H], fill=INK, width=2)
d.line([ax, ay + ILLO_H, ax + ILLO_W, ay + ILLO_H], fill=INK, width=2)
pts = [(ax + 6, ay + 14), (ax + 34, ay + 34), (ax + 56, ay + 26),
       (ax + 82, ay + 66), (ax + 112, ay + 100)]
d.line(pts, fill=RED, width=4, joint="curve")
ex, ey = pts[-1]
d.polygon([(ex + 6, ey + 8), (ex - 8, ey + 2), (ex + 2, ey - 8)], fill=RED)
panel_text(x, y, "US stocks fell about 3.7% as AI shares sold off, pushing the "
                 "S&P 500 into correction. The Nasdaq lost more than 5%.")

# --- panel 2: Cyclone (spiral)
x, y = PX[1], PY[0]
panel_frame(x, y, "Cyclone Akvan Hits India")
cx, cy = x + ILLO_X + ILLO_W / 2, y + ILLO_Y + ILLO_H / 2
spiral = []
steps = 160
for i in range(steps + 1):
    t = i / steps
    ang = t * 4.6 * 3.141592653589793
    r = 4 + t * 50
    spiral.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.88))
d.line(spiral, fill=NAVY, width=4, joint="curve")
d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=PAPER, outline=NAVY, width=3)
panel_text(x, y, "Cyclone Akvan crossed the Odisha coast near Gopalpur, "
                 "bringing strong winds and heavy rain.")

# --- panel 3: Berlin summit (table with flags)
x, y = PX[0], PY[1]
panel_frame(x, y, "Berlin Summit on Ukraine")
tx0, ty0 = x + ILLO_X, y + ILLO_Y
# table
d.ellipse([tx0 + 8, ty0 + 62, tx0 + ILLO_W - 8, ty0 + 106],
          fill=(150, 110, 70), outline=INK, width=2)
# chairs (small circles around table)
for fx, fy in [(0.18, 0.52), (0.5, 0.46), (0.82, 0.52), (0.3, 0.95), (0.7, 0.95)]:
    sx, sy = tx0 + fx * ILLO_W, ty0 + fy * ILLO_H
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=NAVY)
# three flags on poles above the table
flags = [
    ("UA", [(0, 0, 200), (255, 215, 0)]),
    ("DE", [(20, 20, 20), (200, 30, 30), (255, 205, 0)]),
    ("US", None),
]
for i, (tag, bands) in enumerate(flags):
    fx = tx0 + 16 + i * 38
    fy = ty0 + 4
    d.line([fx, fy, fx, fy + 52], fill=INK, width=2)
    fw, fh = 26, 18
    if bands:
        bh = fh / len(bands)
        for j, c in enumerate(bands):
            d.rectangle([fx, fy + j * bh, fx + fw, fy + (j + 1) * bh], fill=c)
    else:  # simplified US flag: stripes + canton
        for j in range(6):
            c = (190, 40, 40) if j % 2 == 0 else (250, 250, 250)
            d.rectangle([fx, fy + j * 3, fx + fw, fy + (j + 1) * 3], fill=c)
        d.rectangle([fx, fy, fx + 11, fy + 9], fill=(30, 50, 120))
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
panel_text(x, y, "Leaders of the coalition of the willing meet in Berlin on "
                 "Ukraine, with President Zelenskyy and US negotiators taking part.")

# --- panel 4: GTA 6 (controller)
x, y = PX[1], PY[1]
panel_frame(x, y, "GTA 6 Passes $2.36 Billion")
gx, gy = x + ILLO_X, y + ILLO_Y
body = [gx + 10, gy + 30, gx + ILLO_W - 10, gy + 86]
d.rounded_rectangle(body, radius=24, fill=NAVY, outline=INK, width=2)
d.ellipse([gx + 2, gy + 48, gx + 42, gy + 108], fill=NAVY, outline=INK, width=2)
d.ellipse([gx + ILLO_W - 42, gy + 48, gx + ILLO_W - 2, gy + 108],
          fill=NAVY, outline=INK, width=2)
# d-pad
d.rectangle([gx + 26, gy + 52, gx + 38, gy + 76], fill=PAPER)
d.rectangle([gx + 20, gy + 58, gx + 44, gy + 70], fill=PAPER)
# buttons
for bx, by, c in [(86, 52, RED), (98, 62, GOLD), (74, 62, (90, 160, 90)),
                  (86, 72, (90, 120, 200))]:
    d.ellipse([gx + bx - 5, gy + by - 5, gx + bx + 5, gy + by + 5], fill=c)
panel_text(x, y, "Grand Theft Auto 6 has taken about $2.36 billion in launch "
                 "revenue, with more than 24.5 million copies sold.")

# ---------------------------------------------------------------- bottom strip
STRIP_TOP, STRIP_BOT = 826, 950
d.rectangle([M, STRIP_TOP, W - M, STRIP_BOT], fill=PANEL_BG, outline=RULE, width=2)
d.text((M + 10, STRIP_TOP + 7), "Cancer Pill Breakthrough", font=font(SERIF_B, 22), fill=INK)
d.line([M + 10, STRIP_TOP + 38, W - M - 10, STRIP_TOP + 38], fill=RULE, width=1)
# capsule icon
cx0, cy0 = M + 22, STRIP_TOP + 62
d.rounded_rectangle([cx0, cy0, cx0 + 74, cy0 + 30], radius=15,
                    fill=(250, 250, 250), outline=INK, width=2)
d.rounded_rectangle([cx0, cy0, cx0 + 37, cy0 + 30], radius=15, fill=RED, outline=INK, width=2)
d.rectangle([cx0 + 22, cy0 + 1, cx0 + 37, cy0 + 29], fill=RED)
d.line([cx0 + 37, cy0, cx0 + 37, cy0 + 30], fill=INK, width=2)
draw_paragraph(
    "A trial of the pill daraxonrasib found tumours stopped growing in nearly "
    "all patients; cancer became undetectable in one in 12.",
    M + 116, STRIP_TOP + 52, (W - M - 10) - (M + 116), STRIP_BOT - (STRIP_TOP + 52) - 10,
    path=SANS, size=17,
)

# ---------------------------------------------------------------- ticker
TICK_TOP, TICK_BOT = 958, H - M
d.rectangle([M, TICK_TOP, W - M, TICK_BOT], fill=NAVY)
ticker = (
    "UK and EU sign food, carbon and youth-mobility deals  \u2014  "
    "Trump-Xi-Putin summit ends with few results  \u2014  "
    "World Court: Myanmar committed genocide against Rohingya  \u2014  "
    "India 159 for 1 at stumps in Wellington Test."
)
lines, f, lh = fit_paragraph(ticker, SANS, 14, W - 2 * M - 24, TICK_BOT - TICK_TOP - 10)
ty = TICK_TOP + (TICK_BOT - TICK_TOP - len(lines) * lh) // 2
for i, ln in enumerate(lines):
    d.text((M + 12, ty + i * lh), ln, font=f, fill=(240, 238, 228))

# ---------------------------------------------------------------- save
img.save("entry.png", "PNG", optimize=True)
print("saved entry.png")
