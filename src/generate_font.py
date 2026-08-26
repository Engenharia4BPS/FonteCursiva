#!/usr/bin/env python3
"""Build experimental FonteCursiva Model/Trace TrueType fonts.

Current prototype glyphs: C, c, a, t, r, i, n.
The remaining glyphs come from a supplied base TrueType font so that the
resulting TTF keeps a complete structure compatible with Microsoft Word.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

UPM = 2048
SCALE = UPM / 1000.0
VERSION = "0.2.3"


def bezier(p0, p1, p2, p3, n=90):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((
            u**3 * p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3 * p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1],
        ))
    return pts


def line(p0, p1, n=30):
    return [
        (p0[0] + (p1[0]-p0[0])*i/n, p0[1] + (p1[1]-p0[1])*i/n)
        for i in range(n + 1)
    ]


def resample(poly, spacing):
    if not poly:
        return []
    out = [poly[0]]
    remaining = spacing
    prev = poly[0]
    for cur in poly[1:]:
        while True:
            dx, dy = cur[0]-prev[0], cur[1]-prev[1]
            seg = math.hypot(dx, dy)
            if seg < 1e-9:
                break
            if seg < remaining:
                remaining -= seg
                prev = cur
                break
            r = remaining / seg
            prev = (prev[0] + dx*r, prev[1] + dy*r)
            out.append(prev)
            remaining = spacing
    return out


def add_circle(pen, cx, cy, radius, steps=20):
    pts = [
        (
            cx + math.cos(2*math.pi*i/steps)*radius,
            cy + math.sin(2*math.pi*i/steps)*radius,
        )
        for i in range(steps)
    ]
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()


def sc(pt):
    return (pt[0] * SCALE, pt[1] * SCALE)


def B(a, b, c, d, n=90):
    return [sc(p) for p in bezier(a, b, c, d, n)]


def L(a, b, n=30):
    return [sc(p) for p in line(a, b, n)]


PATHS = {
    "C": [
        B((25,0),(70,15),(100,100),(110,230)),
        B((110,230),(125,500),(270,700),(445,690)),
        B((445,690),(520,685),(555,635),(530,590)),
        B((530,590),(500,545),(455,550),(430,575)),
        B((110,230),(95,100),(155,10),(280,-5)),
        B((280,-5),(390,-8),(480,35),(550,90)),
    ],
    "c": [
        B((-25,55),(15,70),(55,105),(95,155)),
        B((95,155),(125,220),(180,255),(245,255)),
        B((245,255),(175,265),(105,235),(70,170)),
        B((70,170),(35,105),(60,35),(135,22)),
        B((135,22),(215,8),(285,45),(345,105)),
    ],
    "a": [
        B((-25,55),(20,75),(65,115),(100,165)),
        B((100,165),(135,240),(205,270),(270,250)),
        B((270,250),(335,225),(345,145),(315,85)),
        B((315,85),(280,20),(195,5),(135,45)),
        B((135,45),(75,85),(82,195),(155,225)),
        B((155,225),(230,255),(300,205),(305,105)),
        B((305,105),(315,65),(355,70),(420,115)),
    ],
    "t": [
        B((-25,55),(20,75),(65,115),(100,165)),
        B((100,165),(125,285),(145,470),(160,635)),
        B((160,635),(165,675),(185,680),(185,625)),
        B((185,625),(170,430),(160,230),(165,95)),
        B((165,95),(175,50),(220,60),(285,110)),
        L((95,385),(255,405)),
    ],
    "r": [
        B((-25,55),(20,75),(65,115),(100,165)),
        B((100,165),(115,225),(130,280),(140,320)),
        B((140,320),(150,260),(185,220),(225,220)),
        B((225,220),(270,220),(300,250),(305,290)),
        B((305,290),(295,205),(255,130),(220,85)),
        B((220,85),(250,50),(300,65),(365,115)),
    ],
    "i": [
        B((-25,55),(20,75),(65,115),(100,165)),
        B((100,165),(112,130),(115,90),(110,55)),
        B((110,55),(125,35),(165,60),(220,110)),
    ],
    "n": [
        B((-25,55),(20,75),(65,115),(100,165)),
        B((100,165),(112,225),(125,280),(135,315)),
        B((135,315),(140,235),(145,145),(145,65)),
        B((145,65),(155,195),(215,285),(280,285)),
        B((280,285),(345,285),(360,210),(350,125)),
        B((350,125),(345,80),(380,70),(430,115)),
    ],
}

ADVANCE_1000 = {
    "C": 545,
    "c": 345,
    "a": 405,
    "t": 285,
    "r": 355,
    "i": 220,
    "n": 420,
}


def make_glyph(ch: str, dotted: bool):
    pen = TTGlyphPen(None)
    spacing = (82 if dotted else 11) * SCALE
    radius = (11 if dotted else 24) * SCALE
    for path in PATHS[ch]:
        for x, y in resample(path, spacing):
            add_circle(pen, x, y, radius)
    if ch == "i":
        add_circle(pen, 112*SCALE, 400*SCALE, radius)
    return pen.glyph()


def rename_font(font: TTFont, family: str):
    values = {
        1: family,
        2: "Regular",
        3: f"{family};{VERSION}",
        4: family,
        5: f"Version {VERSION}",
        6: family.replace(" ", ""),
        16: family,
        17: "Regular",
    }
    table = font["name"]
    for rec in table.names:
        if rec.nameID in values:
            try:
                rec.string = values[rec.nameID].encode(rec.getEncoding())
            except Exception:
                rec.string = values[rec.nameID].encode("utf-16-be")
    for nid, text in values.items():
        table.setName(text, nid, 3, 1, 0x409)
        table.setName(text, nid, 1, 0, 0)


def build_font(base_font: Path, output: Path, family: str, dotted: bool):
    font = TTFont(str(base_font))
    glyph_table = font["glyf"]
    metrics = font["hmtx"].metrics

    cmap = {}
    for table in font["cmap"].tables:
        if table.isUnicode():
            cmap.update(table.cmap)

    for ch in "Ccatrin":
        glyph_name = cmap[ord(ch)]
        glyph_table[glyph_name] = make_glyph(ch, dotted)
        metrics[glyph_name] = (int(ADVANCE_1000[ch]*SCALE), 0)

    font["hhea"].ascent = int(800*SCALE)
    font["hhea"].descent = int(-220*SCALE)
    font["OS/2"].sTypoAscender = int(800*SCALE)
    font["OS/2"].sTypoDescender = int(-220*SCALE)
    font["OS/2"].usWinAscent = int(820*SCALE)
    font["OS/2"].usWinDescent = int(240*SCALE)

    rename_font(font, family)
    font.save(str(output))


def make_preview(base_font: Path, model: Path, trace: Path, output: Path):
    image = Image.new("RGB", (1800, 1000), "white")
    draw = ImageDraw.Draw(image)
    title = ImageFont.truetype(str(base_font), 42)
    solid = ImageFont.truetype(str(model), 190)
    dotted = ImageFont.truetype(str(trace), 190)
    small = ImageFont.truetype(str(trace), 90)

    draw.text((70,30), f"FonteCursiva v{VERSION} — protótipo", font=title, fill="black")
    draw.text((70,120), "Catarina", font=solid, fill="black")
    draw.text((70,390), "Catarina", font=dotted, fill="gray")
    draw.text((70,680), "Catarina   catarina   ca   Cat", font=small, fill="gray")
    image.save(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-font", required=True, type=Path,
                        help="Path to a complete TrueType base font (for example DejaVuSans.ttf)")
    parser.add_argument("--output-dir", default=Path("dist"), type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    model = args.output_dir / "FonteCursivaModel-v0.2.3.ttf"
    trace = args.output_dir / "FonteCursivaTrace-v0.2.3.ttf"
    preview = args.output_dir / "preview-v0.2.3.png"

    build_font(args.base_font, model, "FonteCursiva Model 023", dotted=False)
    build_font(args.base_font, trace, "FonteCursiva Trace 023", dotted=True)
    make_preview(args.base_font, model, trace, preview)

    print(model)
    print(trace)
    print(preview)


if __name__ == "__main__":
    main()
