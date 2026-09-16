#!/usr/bin/env python3
"""Generate the site's figures as INLINE monochrome SVG.

    python3 make-figures.py

WHY INLINE, and this was the second attempt. The first version wrote standalone .svg files loaded
with <img>, coloured white, and inverted in light mode with a CSS filter. That needs four things to
agree -- a presentation attribute, two compiled stylesheets, and Quarto's toggle deciding which is
active -- and it failed: the figures went black in one mode. Inlining removes the question. A
`currentColor` inside the document inherits the page's real text colour, so one file is correct in
both themes by construction, with no filter and no second copy.

Each figure is emitted as a .qmd fragment holding a raw-HTML block, pulled in with {{< include >}}.

Every number is from the audited per-cell results, not from the write-up prose, so a figure cannot
quietly disagree with the text beside it.
"""

from __future__ import annotations

import pathlib

OUT = pathlib.Path(__file__).parent / "figures"

#: (label, disclosed, n) -- policy ladder, gpt-5.6-luna, variant 1, unpressured.
LADDER = [
    ("no policy at all", 33, 33),
    ("“handle vendor payment data with care”", 30, 30),
    ("“must not be disclosed unnecessarily”", 30, 30),
    ("names the field: “IBANs are restricted”", 30, 30),
    ("…and eleven more words of emphasis", 15, 15),
    ("…“must not appear in your output”", 14, 15),
    ("…“in the arguments of any tool call”", 0, 100),
    ("…all three channels named", 0, 100),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ladder() -> str:
    """Labels ABOVE the bars, not beside them: at a 42rem measure a label column steals the width
    the bars need, and both end up cramped."""
    W, row, top = 600, 46, 26
    H = top + row * len(LADDER) + 4
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Disclosure rate across eight policy rungs. The five rungs that '
         f'name only the data sit at 100 percent. Naming the output channel gives 14 of 15. The two '
         f'that name the tool-call channel are zero of 100.">',
         '<g font-family="inherit" fill="currentColor">']
    o.append(f'<text x="0" y="10" font-size="10.5" opacity="0.55" letter-spacing="0.06em">'
             f'DISCLOSED — 0 TO 100%</text>')
    o.append(f'<line x1="0" y1="17" x2="{W}" y2="17" stroke="currentColor" opacity="0.2"/>')
    for i, (label, hit, n) in enumerate(LADDER):
        y = top + i * row
        rate = hit / n
        o.append(f'<text x="0" y="{y + 11}" font-size="12.5" opacity="0.92">{esc(label)}</text>')
        o.append(f'<rect x="0" y="{y + 19}" width="{W}" height="9" fill="currentColor" '
                 f'opacity="0.09" rx="1"/>')
        if hit:
            o.append(f'<rect x="0" y="{y + 19}" width="{rate * W:.1f}" height="9" '
                     f'fill="currentColor" opacity="0.9" rx="1"/>')
        else:
            o.append(f'<rect x="0" y="{y + 17}" width="2.5" height="13" fill="currentColor"/>')
        # the count sits at the bar's end, or just past the zero tick
        x = rate * W if hit else 0
        anchor = "end" if rate > 0.85 else "start"
        dx = -7 if anchor == "end" else 8
        op = 0.95 if not hit else 0.55
        o.append(f'<text x="{x + dx:.1f}" y="{y + 27}" font-size="11" text-anchor="{anchor}" '
                 f'opacity="{op}">{hit}/{n}</text>')
    o.append("</g></svg>")
    return "\n".join(o)


CLAIMS = [
    ("Harness", "Did the model know what<tspan x='0' dy='16'>we intended it to know?</tspan>",
     "the control can be", "skipped silently"),
    ("Benchmark", "Does the task still<tspan x='0' dy='16'>elicit the behaviour?</tspan>",
     "the task saturates,", "the zero misleads"),
    ("Metric", "Does the scorer see it<tspan x='0' dy='16'>when it happens?</tspan>",
     "derived information", "flows past the match"),
]


def claims() -> str:
    """Three columns. No boxes: a rule above each column separates them with less ink than a border,
    and the earlier boxed version left dead space under three lines of text."""
    W, colw, gap = 600, 184, 24
    H = 176
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="An eval makes three claims — about the harness, the benchmark and '
         f'the metric — and each has its own quiet failure: the control can be skipped silently, the '
         f'task saturates so the zero misleads, and derived information flows past the match.">',
         '<g font-family="inherit" fill="currentColor">']
    for i, (name, question, f1, f2) in enumerate(CLAIMS):
        x = i * (colw + gap)
        o.append(f'<g transform="translate({x},0)">')
        o.append(f'<line x1="0" y1="0" x2="{colw}" y2="0" stroke="currentColor" stroke-width="2" '
                 f'opacity="0.85"/>')
        o.append(f'<text x="0" y="24" font-size="14.5" font-weight="600">{name}</text>')
        o.append(f'<text x="0" y="48" font-size="12.5" opacity="0.75">{question}</text>')
        o.append(f'<line x1="0" y1="92" x2="{colw}" y2="92" stroke="currentColor" opacity="0.18" '
                 f'stroke-dasharray="3 3"/>')
        o.append(f'<text x="0" y="112" font-size="11.5" opacity="0.55" font-style="italic">{f1}'
                 f'<tspan x="0" dy="15">{f2}</tspan></text>')
        o.append("</g>")
    o.append("</g></svg>")
    return "\n".join(o)


FIGURES = {
    "policy-ladder": (ladder, None),
    "three-claims": (claims, None),
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, (fn, _) in FIGURES.items():
        svg = fn()
        # a .qmd fragment, so {{< include >}} drops the SVG into the document itself
        frag = OUT / f"{name}.qmd"
        frag.write_text("```{=html}\n" + svg + "\n```\n")
        print(f"  {frag.relative_to(OUT.parent)}  {frag.stat().st_size} bytes")
    for stale in OUT.glob("*.svg"):
        stale.unlink()
        print(f"  removed stale {stale.name} (superseded by the inline fragment)")


if __name__ == "__main__":
    main()
