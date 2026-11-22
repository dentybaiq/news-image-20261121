# draw.py — renders entry.png for news-image-20261121.
# A 1024x1024 editorial infographic summing up Saturday 21 November 2026.
# Drawn with Pillow + Noto Sans (real rendered text, never an AI picture),
# so every letter stays crisp and legible even at 300 pixels wide.
# Run: python3 draw.py  (writes entry.png next to this file)

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # warm off-white paper
INK = (26, 26, 26)        # near-black
RED = (200, 16, 46)       # masthead red
GOLD = (245, 197, 66)     # hero kicker gold
HERO_TOP = (18, 38, 74)   # dark navy
HERO_BOT = (30, 58, 120)
CARD = (255, 255, 255)
CARD_EDGE = (214, 205, 190)
FOOT = (140, 132, 118)

FDIR = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

F_BLACK = lambda s: font("NotoSans-Black.ttf", s)
F_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
F_REG = lambda s: font("NotoSans-Regular.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def rounded_grad(x0, y0, x1, y1, r, top, bot):
    """Rounded rectangle filled with a vertical gradient."""
    w, h = x1 - x0, y1 - y0
    grad = Image.new("RGB", (w, h))
    gp = grad.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        col = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            gp[x, y] = col
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w, h], radius=r, fill=255)
    img.paste(grad, (x0, y0), mask)

# ---------- masthead ----------
d.line([(36, 30), (988, 30)], fill=RED, width=4)
d.text((36, 44), "THE WORLD IN ONE DAY", font=F_BOLD(30), fill=RED)
d.text((36, 82), "SATURDAY 21 NOVEMBER 2026", font=F_BLACK(62), fill=INK)
d.line([(36, 156), (988, 156)], fill=INK, width=3)

# ---------- hero: ICJ Myanmar genocide ruling ----------
hx0, hy0, hx1, hy1 = 36, 172, 988, 492
rounded_grad(hx0, hy0, hx1, hy1, 18, HERO_TOP, HERO_BOT)
d = ImageDraw.Draw(img)
d.text((62, 188), "THE HAGUE  \u2022  WORLD COURT", font=F_BOLD(24), fill=GOLD)
d.text((62, 218), "MYANMAR COMMITTED", font=F_BLACK(72), fill=(255, 255, 255))
d.text((62, 292), "GENOCIDE, COURT RULES", font=F_BLACK(72), fill=(255, 255, 255))
sub = ("The International Court of Justice rules Myanmar committed "
       "genocide against its Rohingya Muslim minority.")
lines = wrap(sub, F_REG(26), 900)
y = 372
for ln in lines:
    d.text((62, y), ln, font=F_REG(26), fill=(225, 230, 240))
    y += 32
# stat chips
chips = ["ICJ ruling", "Rohingya minority",
         "Genocide prevention", "Historic verdict"]
cx, cy = 62, 444
for c in chips:
    wch = int(d.textlength(c, font=F_BOLD(21))) + 34
    d.rounded_rectangle([cx, cy, cx + wch, cy + 36], radius=18, fill=(255, 255, 255))
    d.text((cx + 17, cy + 7), c, font=F_BOLD(21), fill=(20, 40, 80))
    cx += wch + 14

# ---------- 2x2 grid ----------
def card(x0, y0, w, h, accent, kicker, headline, body):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12,
                        fill=CARD, outline=CARD_EDGE, width=2)
    d.rectangle([x0 + 14, y0 + 16, x0 + 20, y0 + h - 16], fill=accent)
    d.text((x0 + 34, y0 + 14), kicker, font=F_BOLD(20), fill=accent)
    hl = wrap(headline, F_BOLD(26), w - 52)
    yy = y0 + 42
    for ln in hl[:2]:
        d.text((x0 + 34, yy), ln, font=F_BOLD(26), fill=INK)
        yy += 32
    bl = wrap(body, F_REG(20), w - 52)
    for ln in bl[:2]:
        d.text((x0 + 34, yy), ln, font=F_REG(20), fill=(70, 66, 60))
        yy += 25

GY, GH, GW, GAP = 506, 170, 466, 20
card(36, GY, GW, GH, (110, 24, 24), "MEXICO",
     "Mexico captures \u2018El Chapo Isidro\u2019",
     "FBI most-wanted drug lord arrested in a shoot-out; 11 dead in "
     "the firefight.")
card(36 + GW + GAP, GY, GW, GH, (200, 16, 46), "POLAND",
     "Russian missiles land in Poland",
     "Missiles and drones fall in Poland during an attack on Ukraine; "
     "NATO alert.")
card(36, GY + GH + GAP, GW, GH, (29, 78, 216), "WASHINGTON",
     "FBI probes hack of its crime database",
     "FBI investigating a suspected breach of the crime database used "
     "by police.")
card(36 + GW + GAP, GY + GH + GAP, GW, GH, (15, 118, 110), "UKRAINE",
     "Zelensky: Putin is a \u2018killer\u2019",
     "Zelensky hits back after Trump calls the Russian leader a friend.")

# ---------- bottom strip: Peru ----------
bx0, by0, bx1, by1 = 36, 882, 988, 974
d.rounded_rectangle([bx0, by0, bx1, by1], radius=12,
                    fill=CARD, outline=CARD_EDGE, width=2)
d.rectangle([bx0 + 14, by0 + 16, bx0 + 20, by1 - 16], fill=(180, 120, 20))
d.text((bx0 + 34, by0 + 10), "PERU", font=F_BOLD(20), fill=(180, 120, 20))
d.text((bx0 + 34, by0 + 34), "Magnitude 6.9 earthquake strikes Peru",
       font=F_BOLD(27), fill=INK)
d.text((bx0 + 34, by0 + 64),
       "A strong 6.9-magnitude quake hits Peru; no immediate reports of major damage.",
       font=F_REG(21), fill=(70, 66, 60))

# ---------- footer ----------
d.text((512, 988), "Compiled from news reports of Saturday 21 November 2026",
       font=F_REG(20), fill=FOOT, anchor="ma")

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
