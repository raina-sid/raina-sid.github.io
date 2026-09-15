#!/usr/bin/env python3
"""Regenerate og-card.png, the image shown when the site is shared.

    python3 make-og-card.py

Kept in the repo because the previous card was an undocumented binary: when the site's tagline
changed, the card silently kept advertising the old one, and nothing flagged it. A generator means
the card is derived from the same string as the site rather than remembered separately.

Design: monochrome, matching the site. Black ground, white type, no accent. 1200x630 is the OG
standard; LinkedIn and Slack both crop toward the centre, so nothing important goes near an edge.
"""

from __future__ import annotations

import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
MARGIN = 92
BG, FG, MUTED, RULE = "#000000", "#ffffff", "#9a9a9a", "#2a2a2a"

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

ROOT = pathlib.Path(__file__).parent


def site_description() -> str:
    """Read the tagline from _quarto.yml, so the card cannot drift from the site again."""
    text = (ROOT / "_quarto.yml").read_text()
    m = re.search(r'^\s*description:\s*"(.+?)"\s*$', text, re.M)
    if not m:
        raise SystemExit("no description found in _quarto.yml")
    return m.group(1)


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    domain = ImageFont.truetype(SERIF, 21)
    name = ImageFont.truetype(SERIF_BOLD, 82)
    tag = ImageFont.truetype(SERIF, 35)

    # letterspaced domain, drawn per-character since PIL has no tracking
    y = 132
    x = MARGIN
    for ch in "RAINA-SID.GITHUB.IO":
        d.text((x, y), ch, font=domain, fill=MUTED)
        x += d.textlength(ch, font=domain) + 6

    d.text((MARGIN, 196), "Siddharth Raina", font=name, fill=FG)

    rule_y = 352
    d.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=RULE, width=1)

    lines = wrap(d, site_description(), tag, W - 2 * MARGIN)
    y = 402
    for ln in lines[:3]:
        d.text((MARGIN, y), ln, font=tag, fill=FG)
        y += 52

    out = ROOT / "og-card.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.name}  {img.size[0]}x{img.size[1]}  {out.stat().st_size} bytes")
    print(f"tagline used: {site_description()!r}")


if __name__ == "__main__":
    main()
