#!/usr/bin/env python3
"""Generate the site's figures as monochrome SVG.

    python3 make-figures.py

WHY SVG AND WHY GENERATED. SVG scales, weighs ~2.5KB, and needs no build step. Note the root carries
`color="#ffffff"` explicitly: `currentColor` does NOT inherit from the page into an SVG loaded via
`<img>`, so without it the figures would resolve to black and vanish on a black background. Light mode
inverts them in CSS instead of shipping a second copy. And generating from
literal data means a figure cannot quietly disagree with the prose beside it, which is the same
reason the social card reads its tagline out of _quarto.yml rather than remembering it.

Every number below is from the audited per-cell results, not from the write-up text.
"""

from __future__ import annotations

import pathlib

OUT = pathlib.Path(__file__).parent / "figures"

#: (label, disclosed, n) — the policy ladder, gpt-5.6-luna, variant 1, unpressured.
LADDER = [
    ("no policy at all",                        33, 33),
    ('"handle vendor payment data with care"',  30, 30),
    ('"not disclosed unnecessarily"',           30, 30),
    ('names the field: "IBANs are restricted"',  30, 30),
    ("+ emphasis, no channel named",            15, 15),
    ('+ "must not appear in your output"',       14, 15),
    ('+ "in the arguments of any tool call"',     0, 100),
    ("+ all three channels",                     0, 100),
]


def ladder_svg() -> str:
    row_h, top, label_w, bar_w = 38, 34, 268, 300
    h = top + row_h * len(LADDER) + 26
    w = label_w + bar_w + 66
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
         f'color="#ffffff" role="img" aria-label="Disclosure rate by policy rung: every rung that does not name '
         f'the tool-call channel leaks; the two that do are zero.">',
         '<g fill="currentColor" font-family="system-ui, sans-serif">']
    # axis
    p.append(f'<text x="{label_w}" y="16" font-size="11" opacity="0.6">0%</text>')
    p.append(f'<text x="{label_w + bar_w}" y="16" font-size="11" opacity="0.6" '
             f'text-anchor="end">100% disclosed</text>')
    p.append(f'<line x1="{label_w}" y1="22" x2="{label_w + bar_w}" y2="22" '
             f'stroke="currentColor" stroke-width="1" opacity="0.25"/>')
    for i, (label, hit, n) in enumerate(LADDER):
        y = top + i * row_h
        rate = hit / n
        p.append(f'<text x="{label_w - 12}" y="{y + 14}" font-size="12.5" text-anchor="end" '
                 f'opacity="0.9">{_esc(label)}</text>')
        if hit:
            p.append(f'<rect x="{label_w}" y="{y + 3}" width="{rate * bar_w:.1f}" height="15" '
                     f'fill="currentColor" opacity="0.85"/>')
        else:
            # a zero needs to be visible as a measurement, not as absence
            p.append(f'<line x1="{label_w}" y1="{y + 2}" x2="{label_w}" y2="{y + 19}" '
                     f'stroke="currentColor" stroke-width="2"/>')
        p.append(f'<text x="{label_w + (rate * bar_w if hit else 0) + 8}" y="{y + 14}" '
                 f'font-size="11.5" opacity="0.65">{hit}/{n}</text>')
    p.append('</g></svg>')
    return "\n".join(p)


CLAIMS = [
    ("Harness", "Did the model know\nwhat we intended?", "the control can be\nskipped silently"),
    ("Benchmark", "Does the task still\nelicit the behaviour?", "the task saturates,\nthe zero misleads"),
    ("Metric", "Does the scorer see it\nwhen it happens?", "derived information\nflows past the match"),
]


def claims_svg() -> str:
    bw, gap, top, w = 196, 22, 30, 656
    h = 214
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" color="#ffffff" role="img" '
         f'aria-label="An eval makes three claims -- harness, benchmark, metric -- and each has '
         f'its own failure mode.">',
         '<g font-family="system-ui, sans-serif" fill="currentColor">']
    for i, (name, question, failure) in enumerate(CLAIMS):
        x = i * (bw + gap)
        p.append(f'<rect x="{x}" y="{top}" width="{bw}" height="92" fill="none" '
                 f'stroke="currentColor" stroke-width="1" opacity="0.35" rx="2"/>')
        p.append(f'<text x="{x + 14}" y="{top + 26}" font-size="14" font-weight="600">{name}</text>')
        for j, line in enumerate(question.split("\n")):
            p.append(f'<text x="{x + 14}" y="{top + 48 + j * 17}" font-size="12" '
                     f'opacity="0.75">{_esc(line)}</text>')
        # the failure hangs below, so the diagram reads: claim above, how it breaks below
        p.append(f'<line x1="{x + bw / 2}" y1="{top + 92}" x2="{x + bw / 2}" y2="{top + 116}" '
                 f'stroke="currentColor" stroke-width="1" opacity="0.3" stroke-dasharray="2 3"/>')
        for j, line in enumerate(failure.split("\n")):
            p.append(f'<text x="{x + bw / 2}" y="{top + 134 + j * 16}" font-size="11.5" '
                     f'text-anchor="middle" opacity="0.6">{_esc(line)}</text>')
        if i < len(CLAIMS) - 1:
            cx = x + bw + gap / 2
            p.append(f'<path d="M{cx - 5} {top + 42} l6 4 -6 4" fill="none" stroke="currentColor" '
                     f'stroke-width="1.4" opacity="0.5"/>')
    p.append(f'<text x="0" y="{h - 6}" font-size="11.5" opacity="0.55">'
             f'Each can fail while the run reports success.</text>')
    p.append('</g></svg>')
    return "\n".join(p)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, svg in [("policy-ladder", ladder_svg()), ("three-claims", claims_svg())]:
        f = OUT / f"{name}.svg"
        f.write_text(svg + "\n")
        print(f"  {f.relative_to(OUT.parent)}  {f.stat().st_size} bytes")


if __name__ == "__main__":
    main()
