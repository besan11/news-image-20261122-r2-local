# Front page renderer — news-image-20261122 round 2.
# Draws one 1024x1024 cream broadsheet summing up Sunday 22 November 2026.
# Everything here is drawn in code with PIL: no photos, no downloaded art.
# Run: python3 render.py  (writes entry.png next to this file)

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

CREAM = (246, 239, 220)
PAPER = (250, 244, 228)
INK = (26, 26, 26)
RED = (166, 30, 34)
DARKRED = (122, 20, 24)
NAVY = (31, 58, 95)
DARKNAVY = (18, 38, 68)
TEAL = (18, 110, 105)
GOLD = (176, 124, 18)
GREEN = (46, 110, 58)
PURPLE = (96, 62, 128)
GREY = (110, 104, 90)
LIGHTBLUE = (178, 208, 224)
SKY = (135, 185, 214)
SAND = (214, 196, 150)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)

W, H = 1024, 1024


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_SERIF = "DejaVuSerif-Bold.ttf"
F_SERIF_R = "DejaVuSerif.ttf"
F_SANS = "DejaVuSans.ttf"
F_SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines starting at (x, y); returns y after the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if clipped."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def pill(draw, x, y, text, fnt, fg, bg):
    """White fact pill inside lead art; returns width used."""
    pad_x, pad_y = 7, 4
    tw = draw.textlength(text, font=fnt)
    draw.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + fnt.size + 2 * pad_y],
                           radius=4, fill=bg, outline=INK, width=1)
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=fg)
    return tw + 2 * pad_x


def kicker(draw, x, y, w, text, fnt):
    """Red kicker bar with white text across the top of a card."""
    h = 16
    draw.rectangle([x, y, x + w, y + h], fill=RED)
    draw.text((x + 5, y + 2), text, font=fnt, fill=WHITE)
    return y + h


def num_badge(draw, cx, cy, n, r=9):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=WHITE, width=1)
    f = font(F_SANS_B, 11)
    tw = draw.textlength(str(n), font=f)
    draw.text((cx - tw / 2, cy - 8), str(n), font=f, fill=WHITE)


# ---------------------------------------------------------------- scenes
# Each painter fills the box (x, y, w, h) with one big simple scene.

def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARKNAVY)
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(28, 78, 110))
    for i in range(5):
        wx = x + 12 + i * 52
        d.arc([wx, y + h - 26, wx + 44, y + h - 6], 180, 360, fill=SKY, width=3)
    # tanker 1 (left, stern hit)
    d.rectangle([x + 18, y + 62, x + 128, y + 92], fill=(150, 40, 36))
    d.rectangle([x + 30, y + 44, x + 62, y + 62], fill=(210, 205, 190))
    d.rectangle([x + 96, y + 50, x + 108, y + 62], fill=(210, 205, 190))
    d.rectangle([x + 128, y + 70, x + 150, y + 92], fill=(90, 24, 22))
    # tanker 2 (right, engine-room hit)
    d.rectangle([x + 178, y + 70, x + 288, y + 96], fill=(36, 90, 70))
    d.rectangle([x + 196, y + 52, x + 226, y + 70], fill=(210, 205, 190))
    d.rectangle([x + 252, y + 56, x + 264, y + 70], fill=(210, 205, 190))
    # projectile arcs + bursts
    d.arc([x + 60, y - 6, x + 200, y + 78], 200, 340, fill=(255, 170, 60), width=4)
    d.arc([x + 190, y - 2, x + 300, y + 84], 200, 340, fill=(255, 170, 60), width=4)
    for cx, cy in ((x + 132, y + 58), (x + 262, y + 66)):
        for r, col in ((16, (255, 200, 90)), (10, (255, 120, 40)), (5, WHITE)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.text((x + 8, y + 6), "STRAIT OF HORMUZ", font=font(F_SANS_B, 12), fill=(200, 220, 240))


def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 96, 88))
    d.rectangle([x, y + int(h * 0.66), x + w, y + h], fill=(120, 74, 32))
    # globe
    gx, gy, gr = x + 62, y + 58, 42
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=SKY, outline=WHITE, width=2)
    d.ellipse([gx - 26, gy - 30, gx - 2, gy - 6], fill=GREEN)
    d.ellipse([gx + 4, gy + 6, gx + 28, gy + 30], fill=GREEN)
    d.ellipse([gx - 8, gy - 12, gx + 14, gy + 4], fill=GREEN)
    # thermometer
    d.rectangle([x + 138, y + 18, x + 152, y + 82], fill=WHITE, outline=INK, width=1)
    d.ellipse([x + 130, y + 78, x + 160, y + 108], fill=RED, outline=INK, width=1)
    d.rectangle([x + 142, y + 34, x + 148, y + 82], fill=RED)
    # clock
    cx, cy, cr = x + 258, y + 48, 30
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=WHITE, outline=INK, width=2)
    d.line([cx, cy, cx, cy - 20], fill=INK, width=3)
    d.line([cx, cy, cx + 14, cy + 6], fill=INK, width=3)
    # delegates row (table + heads)
    d.rectangle([x + 12, y + 104, x + w - 12, y + 116], fill=(90, 52, 22))
    for i, col in enumerate(((166, 30, 34), (31, 58, 95), (46, 110, 58),
                             (176, 124, 18), (96, 62, 128), (18, 110, 105))):
        hx = x + 30 + i * 48
        d.ellipse([hx, y + 84, hx + 18, y + 102], fill=(232, 190, 150))
        d.rectangle([hx - 4, y + 102, hx + 22, y + 106], fill=col)


def scene_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 74))
    d.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(24, 60, 92))
    for i in range(4):
        wx = x + 20 + i * 70
        d.arc([wx, y + h - 24, wx + 52, y + h - 6], 180, 360, fill=SKY, width=3)
    # freighter hull + containers
    d.polygon([(x + 30, y + 88), (x + 288, y + 88), (x + 272, y + 118),
               (x + 48, y + 118)], fill=(120, 28, 26))
    for i, col in enumerate(((200, 60, 40), (60, 120, 90), (200, 160, 60))):
        d.rectangle([x + 60 + i * 62, y + 62, x + 116 + i * 62, y + 88], fill=col)
    # flames
    for fx, fh in ((x + 78, 44), (x + 138, 58), (x + 198, 46), (x + 248, 36)):
        d.polygon([(fx - 14, y + 66), (fx, y + 66 - fh), (fx + 14, y + 66),
                   (fx + 6, y + 66 - fh // 2), (fx - 6, y + 66 - fh // 2)],
                  fill=(255, 140, 30))
        d.polygon([(fx - 7, y + 66), (fx, y + 66 - fh // 2), (fx + 7, y + 66)],
                  fill=(255, 210, 80))
    # smoke
    for sx, sy, sr in ((x + 90, y + 22, 12), (x + 150, y + 12, 15), (x + 220, y + 20, 11)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 95))
    # lifeboat
    d.polygon([(x + 236, y + 122), (x + 276, y + 122), (x + 268, y + 134),
               (x + 244, y + 134)], fill=(230, 180, 60))
    d.text((x + 8, y + 6), "GULF OF FINLAND", font=font(F_SANS_B, 12), fill=(200, 220, 240))


def scene_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    d.rectangle([x + 14, y + 30, x + w - 14, y + h - 8], fill=(120, 120, 116))
    d.rectangle([x + 14, y + 30, x + w - 14, y + 40], fill=(70, 70, 68))
    for wx in (x + 34, x + 84, x + 134):
        d.rectangle([wx, y + 44, wx + 22, y + 66], fill=(255, 220, 120))
    for fx in (x + 44, x + 94, x + 144):
        d.polygon([(fx - 10, y + 32), (fx, y + 6), (fx + 10, y + 32)], fill=(255, 120, 30))
        d.polygon([(fx - 5, y + 32), (fx, y + 16), (fx + 5, y + 32)], fill=(255, 210, 80))
    d.ellipse([x + w - 34, y + 4, x + w - 14, y + 24], fill=(120, 120, 125))


def scene_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARKNAVY)
    d.line([x + w // 2, y + 8, x + w // 2 - 16, y + h - 6], fill=WHITE, width=4)
    d.line([x + w // 2, y + 8, x + w // 2 + 16, y + h - 6], fill=WHITE, width=4)
    d.line([x + 30, y + 26, x + w - 30, y + 26], fill=WHITE, width=3)
    d.line([x + 30, y + 44, x + w - 30, y + 44], fill=WHITE, width=3)
    f = font(F_SANS_B, 26)
    d.text((x + w - 62, y + h - 34), "2h", font=f, fill=(255, 200, 90))
    d.polygon([(x + 14, y + 12), (x + 26, y + 30), (x + 18, y + 30),
               (x + 30, y + 52), (x + 16, y + 30), (x + 24, y + 30)],
              fill=(255, 210, 80))


def scene_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    d.rectangle([x, y, x + w, y + h // 2], fill=WHITE)
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(220, 40, 50))
    d.ellipse([x + w // 2 - 22, y + h // 2 - 22, x + w // 2 + 22, y + h // 2 + 22],
              fill=NAVY, outline=WHITE, width=3)
    f = font(F_SANS_B, 13)
    d.text((x + w // 2 - 8, y + h // 2 - 9), "N", font=f, fill=WHITE)
    d.rectangle([x, y + h - 8, x + w, y + h], fill=NAVY)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 200, 150))
    d.rectangle([x + 18, y + 26, x + 128, y + 52], fill=WHITE, outline=INK, width=2)
    d.rectangle([x + 128, y + 32, x + 152, y + 52], fill=WHITE, outline=INK, width=2)
    d.ellipse([x + 40, y + 52, x + 56, y + 68], fill=INK)
    d.ellipse([x + 116, y + 52, x + 132, y + 68], fill=INK)
    for bx in (x + 30, x + 62, x + 94):
        d.rectangle([bx, y + 8, bx + 24, y + 24], fill=(190, 140, 60), outline=INK, width=1)
    d.ellipse([x + w - 34, y + 6, x + w - 14, y + 26], fill=(255, 200, 90))


def scene_chapo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 190))
    d.rectangle([x + 18, y + 6, x + w - 18, y + h - 6], fill=(250, 244, 224),
                outline=INK, width=2)
    f = font(F_SANS_B, 15)
    d.text((x + 52, y + 10), "WANTED", font=f, fill=RED)
    d.ellipse([x + 62, y + 28, x + 122, y + 62], fill=(200, 170, 130))
    d.rectangle([x + 52, y + 56, x + 132, y + 74], fill=(70, 70, 78))
    f2 = font(F_SANS_B, 11)
    d.text((x + 58, y + 78), "TOP 10", font=f2, fill=RED)


def scene_fbi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 40))
    for i in range(4):
        d.rectangle([x + 14 + i * 40, y + 12, x + 42 + i * 40, y + 22], fill=(60, 90, 130))
        d.rectangle([x + 14 + i * 40, y + 28, x + 42 + i * 40, y + 34], fill=(40, 60, 90))
    d.rectangle([x + 66, y + 42, x + 118, y + 78], fill=(255, 200, 60), outline=INK, width=2)
    d.arc([x + 78, y + 30, x + 106, y + 54], 180, 360, fill=(255, 200, 60), width=5)
    d.ellipse([x + 88, y + 56, x + 96, y + 64], fill=INK)
    f = font(F_SANS_B, 12)
    d.text((x + 124, y + 58), "NCIC", font=f, fill=WHITE)


def scene_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 88, 84))
    for bx, bh in ((x + 12, 46), (x + 58, 58), (x + 104, 40), (x + 142, 52)):
        d.rectangle([bx, y + h - 8 - bh, bx + 38, y + h - 8], fill=(52, 52, 56))
        for wy in range(3):
            d.rectangle([bx + 6, y + h - 8 - bh + 6 + wy * 12, bx + 16,
                         y + h - 8 - bh + 14 + wy * 12], fill=(255, 210, 90))
    d.polygon([(x + 30, y + 6), (x + 44, y + 30), (x + 18, y + 30)], fill=(255, 120, 30))
    d.ellipse([x + w - 30, y + 4, x + w - 12, y + 22], fill=(200, 200, 205))
    d.rectangle([x + w - 52, y + h - 26, x + w - 8, y + h - 8], fill=WHITE, outline=RED, width=2)
    f = font(F_SANS_B, 12)
    d.text((x + w - 44, y + h - 25), "+", font=f, fill=RED)


def scene_bayelsa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 90, 120))
    for i in range(3):
        wx = x + 10 + i * 58
        d.arc([wx, y + h - 22, wx + 46, y + h - 4], 180, 360, fill=SKY, width=3)
    d.polygon([(x + 40, y + 34), (x + 150, y + 34), (x + 138, y + 52),
               (x + 52, y + 52)], fill=(150, 80, 40))
    d.polygon([(x + 40, y + 34), (x + 150, y + 34), (x + 146, y + 26),
               (x + 48, y + 26)], fill=(90, 50, 30))
    d.ellipse([x + 132, y + 56, x + 162, y + 86], outline=(255, 120, 60), width=5)
    d.ellipse([x + 142, y + 66, x + 152, y + 76], outline=(255, 120, 60), width=3)


def scene_belgium(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.polygon([(x + 20, y + 40), (x + 90, y + 40), (x + 100, y + 52),
               (x + 20, y + 52)], fill=WHITE, outline=INK, width=1)
    d.polygon([(x + 100, y + 40), (x + 150, y + 46), (x + 100, y + 52)], fill=WHITE,
              outline=INK, width=1)
    d.rectangle([x + 120, y + 20, x + 132, y + 40], fill=WHITE, outline=INK, width=1)
    d.rectangle([x + 10, y + 58, x + w - 10, y + 80], fill=RED)
    f = font(F_SANS_B, 14)
    d.text((x + 52, y + 62), "STRIKE", font=f, fill=WHITE)
    d.ellipse([x + w - 36, y + 8, x + w - 12, y + 32], fill=(255, 220, 120))


def scene_vegas(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 22))
    for r in range(3):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + 10 + c * 16, y + 8 + r * 14,
                             x + 26 + c * 16, y + 22 + r * 14], fill=WHITE)
    d.polygon([(x + 20, y + 56), (x + 150, y + 56), (x + 164, y + 72),
               (x + 34, y + 72)], fill=(200, 30, 40))
    d.ellipse([x + 52, y + 68, x + 68, y + 84], fill=INK)
    d.ellipse([x + 128, y + 68, x + 144, y + 84], fill=INK)
    f = font(F_SANS_B, 22)
    d.text((x + w - 48, y + 50), "P1", font=f, fill=(255, 210, 80))


PANEL_SCENES = {
    4: scene_bahrain, 5: scene_power, 6: scene_poland, 7: scene_gaza,
    8: scene_chapo, 9: scene_fbi, 10: scene_kryvyi, 11: scene_bayelsa,
    12: scene_belgium, 13: scene_vegas,
}
LEAD_SCENES = {1: scene_hormuz, 2: scene_cop31, 3: scene_sparta}


# ---------------------------------------------------------------- content
# All wording written fresh from the builder's own news verification
# (see NOTES.md). Nothing copied from other entries' pages.

LEADS = [
    dict(num=1, place="STRAIT OF HORMUZ · WAR", pill="2 STRUCK · NO CASUALTIES",
         head="Two tankers hit leaving Hormuz as Iran tightens its grip on shipping",
         body="One hit in the stern, one in the engine room off Khasab. Tehran says "
              "a third tanker struck a mine and burned. (UKMTO, Reuters)",
         scene=scene_hormuz),
    dict(num=2, place="ANTALYA, TÜRKIYE · CLIMATE", pill="VOTE 06:00 GMT SUN",
         head="COP31 nears a deal as a new text is tabled after overtime talks",
         body="Hosts say fossil-fuel and adaptation-finance concerns are now "
              "addressed; objections were due by 03:00 GMT. Adoption not yet "
              "confirmed. (Reuters)",
         scene=scene_cop31),
    dict(num=3, place="GULF OF FINLAND · WAR AT SEA", pill="16 CREW SAFE",
         head="Russian military cargo ship ablaze in the Baltic after drone strike",
         body="Sparta II, owned by a Russian defence logistics firm and bound for "
              "Kaliningrad, burned west of Gogland; it drifted into Finnish "
              "waters. (Reuters)",
         scene=scene_sparta),
]

PANELS = [
    dict(num=4, place="MANAMA, BAHRAIN · IRAN WAR",
         head="Bahrain says Iranian strike set a site ablaze",
         body="No injuries; the IRGC says it hit US bases. (Reuters)",
         scene=scene_bahrain),
    dict(num=5, place="TEHRAN · ENERGY",
         head="Iran begins rationing electricity from Sunday",
         body="Cuts of up to two hours a day as gas output lags. (RFE/RL)",
         scene=scene_power),
    dict(num=6, place="WARSAW · NATO",
         head="Rutte in Warsaw: all of NATO stands with Poland",
         body="Visit follows Friday's Russian missile incursion. (AFP)",
         scene=scene_poland),
    dict(num=7, place="GAZA CITY · CEASEFIRE",
         head="Drone strike hits a Gaza food-aid van, kills three",
         body="IDF says it targeted Islamic Jihad members. (Reuters)",
         scene=scene_gaza),
    dict(num=8, place="SINALOA, MEXICO · CRIME",
         head="Mexico captures cartel boss 'El Chapo Isidro'",
         body="Taken with two other leaders of his gang. (Reuters)",
         scene=scene_chapo),
    dict(num=9, place="WASHINGTON · CYBER",
         head="Trump plays down hack of FBI crime database",
         body="The FBI has not confirmed the NCIC breach. (Reuters)",
         scene=scene_fbi),
    dict(num=10, place="KRYVYI RIH · WAR",
         head="Strike hits Zelenskyy's home city; 2 dead, 60 hurt",
         body="Double-tap attack as rescuers arrived. (AP)",
         scene=scene_kryvyi),
    dict(num=11, place="BAYELSA, NIGERIA · DISASTER",
         head="Boat carrying mourners capsizes; 24 dead",
         body="Hundreds feared missing on the Nun River. (AP)",
         scene=scene_bayelsa),
    dict(num=12, place="BRUSSELS · LABOUR",
         head="Belgian national strike to ground flights Monday",
         body="No regular air traffic 07:00–21:00, Skeyes says. (AFP)",
         scene=scene_belgium),
    dict(num=13, place="LAS VEGAS · FORMULA 1",
         head="Verstappen on pole as Vegas races under lights",
         body="Antonelli dropped 5 places; race 04:00 UTC. (F1)",
         scene=scene_vegas),
]

BRIEFS = [
    "14 Tallinn: Estonia to shut its Russia border (Reuters)",
    "15 Doha: Qatari mediators hold talks in Tehran (Xinhua)",
    "16 Washington: Trump seeks a 'permanent' Iran deal (Fox)",
    "17 Jerusalem: Eisenkot invites Likud to talks (S. Times)",
    "18 Gaza: Araghchi seeks emergency OIC meeting (AJ)",
    "19 Turin: Zverev v Alcaraz for the title, 18:00 CET (ATP)",
    "20 Tehran: Uranium stockpile 'will not leave' Iran (AJ)",
    "21 Myanmar: 4.1 quake in early hours, 95 km deep (EMSC)",
    "22 Lviv: Russia fired 3 missiles, 148 drones (ISW)",
    "23 Washington: SEC eyes Nvidia; shares fell 14% (Reuters)",
    "24 Missouri: Judge approves $7.25bn Roundup deal (AFP)",
    "25 Wellington: Pant's 128 puts India 629/6 (Reuters)",
    "26 Mogadishu: UAE envoy's 72 hours run out (Reuters)",
    "27 Canberra: Bystanders pull driver from burning car (ABC)",
    "28 Copenhagen: Denmark expels Russian attaché (AFP)",
    "29 Seoul: $75,000 bounty for exam-cheating tips (K. Times)",
    "30 New Delhi: Japan to train live-fire in India (JKN)",
    "31 Ranchi: Akvan cancels 14 flights (ANI)",
    "32 Melbourne: Cummins keeps Test captaincy (ABC)",
    "33 Washington: Trump warns of AI tax abroad (Reuters)",
    "34 Kinshasa: Ebola deaths pass 5,300 in DR Congo (Reuters)",
    "35 Caracas: US details $12bn Venezuela haul (State Dept)",
]

TICKER = [
    ("2", "tankers hit leaving Hormuz", "UKMTO"),
    ("16", "crew off burning Russian ship", "Finland"),
    ("~200", "nations at the COP31 talks", ""),
    ("03:00", "GMT deadline for objections", "COP31"),
    ("11", "killed in Chapo gunfight", "Mexico"),
    ("24", "dead in Bayelsa boat", "Nigeria"),
]

CHIPS = [
    ("EUROPE 9", NAVY), ("MIDDLE EAST 8", DARKRED), ("AMERICAS 8", GREEN),
    ("ASIA-PACIFIC 4", GOLD), ("AFRICA 3", TEAL), ("OCEANIA 3", PURPLE),
]

DATE_CHECK = ("Left out as earlier news: Peru 6.9 quake — 20 Nov · US midterm "
              "results — 3 Nov · Eisenkot tasking — 8 Nov · ATP semi-finals — "
              "21 Nov · Shenzhen summit — 19 Nov · Kerch Bridge strikes — "
              "earlier this week · Wall Street's fall into correction — 20 Nov · "
              "Voyager 1's light-day — 18 Nov.")

CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-65, 60), (-55, 52), (-60, 46),
                 (-75, 35), (-80, 25), (-90, 21), (-97, 16), (-105, 20),
                 (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    "samerica": [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10),
                 (-35, -20), (-45, -30), (-55, -35), (-65, -45), (-70, -55),
                 (-75, -40), (-75, -20), (-80, -5)],
    "europe": [(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (18, 56),
               (25, 60), (30, 62), (35, 60), (40, 55), (35, 50), (30, 45),
               (25, 40), (20, 38), (10, 38), (0, 36)],
    "africa": [(-10, 35), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
               (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -25), (12, -15), (10, -5),
               (5, 5), (-5, 5), (-15, 10)],
    "asia": [(40, 55), (50, 60), (60, 65), (70, 70), (90, 72), (110, 75),
             (130, 72), (150, 70), (170, 66), (180, 65), (170, 60),
             (160, 55), (150, 45), (140, 40), (130, 35), (120, 30),
             (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
             (80, 10), (75, 8), (70, 20), (60, 25), (55, 26), (50, 30),
             (45, 30), (40, 35)],
    "oceania": [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22),
                (153, -28), (150, -37), (140, -38), (130, -32), (120, -34),
                (113, -26)],
}

# lon, lat, nudge dx, dy (px) — nudges keep clustered pins readable
PINS = [
    (56, 26, 1, 0, -12), (30, 37, 2, -14, 4), (24, 60, 3, 6, -8),
    (50, 26, 4, 10, 8), (51, 35, 5, 14, -6), (21, 52, 6, -12, -4),
    (34, 31, 7, -4, 12), (-107, 25, 8, 0, 0), (-77, 39, 9, 0, 0),
    (33, 48, 10, 12, 6), (6, 5, 11, 0, 0), (4, 51, 12, -14, 8),
    (-115, 36, 13, 0, 0),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 232), outline=INK, width=1)

    def proj(lon, lat):
        return (x + (lon + 170) / 360 * w, y + (75 - lat) / 130 * h)

    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=SAND,
                  outline=(150, 130, 95))
    for lon, lat, n, dx, dy in PINS:
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=WHITE, width=1)
        f = font(F_SANS_B, 8)
        tw = d.textlength(str(n), font=f)
        d.text((px - tw / 2, py - 5), str(n), font=f, fill=WHITE)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)
    mx, cw = 22, 980

    # top strip
    f_top = font(F_SANS_B, 13)
    d.text((mx, 10), "THE WORLD IN ONE DAY", font=f_top, fill=RED)
    right = "SUNDAY'S NEWS · ONE PAGE · 35 STORIES"
    d.text((mx + cw - d.textlength(right, font=f_top), 10), right,
           font=f_top, fill=INK)
    d.line([mx, 30, mx + cw, 30], fill=INK, width=1)

    # masthead + sub-deck
    f_mast = font(F_SERIF, 60)
    mast = "Sunday 22 November 2026"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 34), mast,
           font=f_mast, fill=INK)
    f_dek = font(F_SERIF_R, 17)
    dek = ("Tankers hit in the Strait of Hormuz · COP31 nears a deal in "
           "Antalya · Russian ship ablaze in the Baltic")
    d.text(((W - d.textlength(dek, font=f_dek)) / 2, 100), dek,
           font=f_dek, fill=RED)
    d.line([mx, 124, mx + cw, 124], fill=INK, width=2)

    # ticker: six big numbers
    cell = cw / 6
    f_num = font(F_SERIF, 30)
    f_cap = font(F_SANS, 10)
    for i, (num, cap, src) in enumerate(TICKER):
        cx = mx + i * cell
        if i:
            d.line([cx, 132, cx, 178], fill=GREY, width=1)
        d.text((cx + 8, 130), num, font=f_num, fill=RED)
        cap_lines = fit_lines(d, cap, f_cap, cell - 16, 2)
        text_block(d, cx + 8, 162, cap_lines, f_cap, INK, 12)
    d.line([mx, 188, mx + cw, 188], fill=INK, width=1)

    # region chips
    f_chip = font(F_SANS_B, 12)
    xx = mx
    for label, col in CHIPS:
        tw = d.textlength(label, font=f_chip) + 16
        d.rectangle([xx, 192, xx + tw, 214], fill=col)
        d.text((xx + 8, 196), label, font=f_chip, fill=WHITE)
        xx += tw + 6
    f_tot = font(F_SANS_B, 13)
    tot = "35 STORIES"
    d.text((mx + cw - d.textlength(tot, font=f_tot), 196), tot,
           font=f_tot, fill=INK)

    # leads
    lw, gap = 318, 13
    ly = 220
    for i, lead in enumerate(LEADS):
        x = mx + i * (lw + gap)
        lead["scene"](d, x, ly, lw, 120)
        d.rectangle([x, ly, x + lw, ly + 120], outline=INK, width=1)
        pill(d, x + 8, ly + 120 - 26, lead["pill"], font(F_SANS_B, 11),
             INK, WHITE)
        yy = ly + 128
        f_pl = font(F_SANS_B, 12)
        d.text((x, yy), f"{lead['num']} · {lead['place']}", font=f_pl, fill=RED)
        yy += 17
        f_h = font(F_SERIF, 19)
        hl = fit_lines(d, lead["head"], f_h, lw, 3)
        yy = text_block(d, x, yy, hl, f_h, INK, 22)
        f_b = font(F_SANS, 12)
        bl = fit_lines(d, lead["body"], f_b, lw, 3)
        text_block(d, x, yy + 3, bl, f_b, INK, 15)
    d.line([mx, 494, mx + cw, 494], fill=INK, width=1)

    # panels: two rows of five
    pw, pgap = 188, 10
    for row in range(2):
        py = 500 + row * 150
        for col in range(5):
            p = PANELS[row * 5 + col]
            x = mx + col * (pw + pgap)
            p["scene"](d, x, py, pw, 52)
            d.rectangle([x, py, x + pw, py + 52], outline=INK, width=1)
            num_badge(d, x + pw - 12, py + 12, p["num"])
            yy = kicker(d, x, py + 54, pw, p["place"], font(F_SANS_B, 9))
            f_ph = font(F_SANS_B, 13)
            hl = fit_lines(d, p["head"], f_ph, pw, 3)
            yy = text_block(d, x, yy + 3, hl, f_ph, INK, 15)
            f_pb = font(F_SANS, 11)
            bl = fit_lines(d, p["body"], f_pb, pw, 2)
            text_block(d, x, yy + 2, bl, f_pb, INK, 13)
    d.line([mx, 812, mx + cw, 812], fill=INK, width=1)

    # map + briefs headers
    f_sec = font(F_SANS_B, 12)
    d.text((mx, 818), "WHERE IT HAPPENED", font=f_sec, fill=RED)
    d.text((mx + 330, 818), "ALSO ON SUNDAY 22 NOVEMBER — 22 MORE STORIES",
           font=f_sec, fill=RED)

    # map
    draw_map(d, mx, 834, 300, 110)
    f_cap2 = font(F_SANS, 9)
    d.text((mx, 946), "Red numbers mark stories 1–13. Positions are approximate.",
           font=f_cap2, fill=GREY)

    # briefs: two columns of eleven
    f_br = font(F_SANS, 10)
    for i, item in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        bx = mx + 330 + col * 336
        by = 834 + row * 11
        lines = fit_lines(d, item, f_br, 326, 1)
        d.text((bx, by), lines[0], font=f_br, fill=INK)

    # date check
    d.rectangle([mx, 958, mx + cw, 994], outline=RED, width=2)
    f_dc = font(F_SANS_B, 11)
    d.text((mx + 8, 962), "DATE CHECK", font=f_dc, fill=RED)
    f_dct = font(F_SANS, 10)
    dc_lines = fit_lines(d, DATE_CHECK, f_dct, cw - 110, 2)
    text_block(d, mx + 100, 963, dc_lines, f_dct, INK, 12)

    # footer
    f_ft = font(F_SANS, 10)
    d.text((mx, 1000),
           "Every story here happened, or was first reported, on Sunday "
           "22 November 2026 in at least one time zone.",
           font=f_ft, fill=INK)
    foot_r = "Sources named beside each story · Original drawings"
    d.text((mx + cw - d.textlength(foot_r, font=f_ft), 1000), foot_r,
           font=f_ft, fill=INK)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png",
          os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")


if __name__ == "__main__":
    build()
