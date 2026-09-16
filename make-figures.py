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



#: Post 2. (model, traded %, ci_lo, ci_hi, n) on the default prompt -- and, of the runs that
#: REFUSED, the share that went looking for a lawful branch instead. Different denominators, so
#: both are labelled with their n rather than presented as one series.
GENERATIONS = [
    ("gpt-4-0613", 69.0, 63.6, 74.0, 300, 9.1, 11),
    ("gpt-4o", 11.4, 8.1, 15.8, 263, 77.7, 233),
    ("gpt-5.5", 0.0, 0.0, 1.3, 300, 99.3, 300),
]


def saturation() -> str:
    """Two panels, because the finding is that the two series move in OPPOSITE directions: trading
    collapses while leaving the scenario becomes near-universal. One panel alone tells half of it."""
    W, panel, gap, row, top = 600, 264, 72, 54, 44
    H = top + row * len(GENERATIONS) + 16
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Across three model generations the rate of trading on the tip falls '
         f'from 69 percent to 11.4 percent to zero, while the share of refusing runs that instead go '
         f'looking for a lawful branch rises from 9 percent to 78 percent to 99 percent.">',
         '<g font-family="inherit" fill="currentColor">']
    for k, (title, sub) in enumerate([("Traded on the tip", "of all runs"),
                                      ("Went looking for a lawful branch", "of runs that refused")]):
        x0 = k * (panel + gap)
        o.append(f'<text x="{x0}" y="12" font-size="12" font-weight="600">{esc(title)}</text>')
        o.append(f'<text x="{x0}" y="27" font-size="10.5" opacity="0.55">{esc(sub)}</text>')
        o.append(f'<line x1="{x0}" y1="34" x2="{x0 + panel}" y2="34" stroke="currentColor" '
                 f'opacity="0.2"/>')
    for i, (name, rate, lo, hi, n, alt, alt_n) in enumerate(GENERATIONS):
        y = top + i * row
        o.append(f'<text x="0" y="{y + 10}" font-size="12.5" opacity="0.92">{esc(name)}</text>')
        for k, (v, vlo, vhi, vn) in enumerate([(rate, lo, hi, n), (alt, None, None, alt_n)]):
            x0 = k * (panel + gap)
            o.append(f'<rect x="{x0}" y="{y + 18}" width="{panel}" height="9" fill="currentColor" '
                     f'opacity="0.09" rx="1"/>')
            w = v / 100 * panel
            if v > 0:
                o.append(f'<rect x="{x0}" y="{y + 18}" width="{w:.1f}" height="9" '
                         f'fill="currentColor" opacity="0.9" rx="1"/>')
            else:
                o.append(f'<rect x="{x0}" y="{y + 16}" width="2.5" height="13" fill="currentColor"/>')
            if vlo is not None:
                a, b = vlo / 100 * panel, vhi / 100 * panel
                o.append(f'<line x1="{x0 + a:.1f}" y1="{y + 22.5}" x2="{x0 + b:.1f}" '
                         f'y2="{y + 22.5}" stroke="currentColor" stroke-width="1" opacity="0.55"/>')
                for e in (a, b):
                    o.append(f'<line x1="{x0 + e:.1f}" y1="{y + 19}" x2="{x0 + e:.1f}" '
                             f'y2="{y + 26}" stroke="currentColor" stroke-width="1" opacity="0.55"/>')
            anchor = "end" if v > 60 else "start"
            tx = x0 + w + (-6 if anchor == "end" else 8)
            o.append(f'<text x="{tx:.1f}" y="{y + 26}" font-size="11" text-anchor="{anchor}" '
                     f'opacity="0.6">{v:.1f}%</text>')
            o.append(f'<text x="{x0}" y="{y + 41}" font-size="10" opacity="0.4">n={vn}</text>')
    o.append("</g></svg>")
    return "\n".join(o)


def setup() -> str:
    """Post 3's environment. Replaces an ASCII diagram in a code block: the two output channels are
    the whole point, and a code block does not make them look like channels."""
    W, H = 600, 232
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Three documents feed the agent: a purchase order, an invoice, and a '
         f'vendor record holding both a restricted account number and a permitted reference label. The '
         f'agent has two ways out — the submitted answer, and an outbound validation tool call — and '
         f'the restricted value can travel by either.">',
         '<g font-family="inherit" fill="currentColor">']
    docs = ["purchase order", "invoice", "vendor record"]
    for i, d in enumerate(docs):
        y = 26 + i * 30
        o.append(f'<text x="0" y="{y}" font-size="12.5" opacity="0.9" text-anchor="end" '
                 f'transform="translate(126,0)">{esc(d)}</text>')
        o.append(f'<line x1="132" y1="{y - 4}" x2="196" y2="{y - 4}" stroke="currentColor" '
                 f'opacity="0.3"/>')
    # what the vendor record carries -- the two candidate values
    o.append(f'<text x="0" y="118" font-size="11.5" opacity="0.9">remittance_iban</text>')
    o.append(f'<text x="0" y="133" font-size="10" opacity="0.55" letter-spacing="0.08em">'
             f'RESTRICTED</text>')
    o.append(f'<text x="0" y="158" font-size="11.5" opacity="0.9">remittance_ref</text>')
    o.append(f'<text x="0" y="173" font-size="10" opacity="0.55" letter-spacing="0.08em">'
             f'PERMITTED</text>')
    o.append(f'<line x1="0" y1="100" x2="126" y2="100" stroke="currentColor" opacity="0.2"/>')
    # the agent
    o.append(f'<rect x="196" y="34" width="96" height="46" fill="none" stroke="currentColor" '
             f'stroke-width="1.5" opacity="0.75" rx="2"/>')
    o.append(f'<text x="244" y="62" font-size="13.5" font-weight="600" text-anchor="middle">'
             f'AGENT</text>')
    o.append(f'<line x1="196" y1="150" x2="196" y2="57" stroke="currentColor" opacity="0.3"/>')
    o.append(f'<line x1="0" y1="150" x2="0" y2="150" stroke="currentColor" opacity="0.3"/>')
    # two channels out
    for i, (label, note) in enumerate([("submit(… destination)", "channel 1 — the answer"),
                                       ("bank_validation(destination)",
                                        "channel 2 — leaves the trust boundary")]):
        y = 48 + i * 58
        o.append(f'<line x1="292" y1="57" x2="330" y2="{y + 4}" stroke="currentColor" '
                 f'opacity="0.45"/>')
        o.append(f'<text x="338" y="{y + 8}" font-size="12" opacity="0.92">{esc(label)}</text>')
        o.append(f'<text x="338" y="{y + 24}" font-size="10.5" opacity="0.55">{esc(note)}</text>')
    o.append(f'<text x="0" y="{H - 4}" font-size="11" opacity="0.5">'
             f'Both values are present in every condition — a policy sanctions the alternative, it '
             f'does not create it.</text>')
    o.append("</g></svg>")
    return "\n".join(o)


FIGURES = {
    "policy-ladder": (ladder, None),
    "three-claims": (claims, None),
    "saturation": (saturation, None),
    "setup": (setup, None),
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
