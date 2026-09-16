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
    bar, gutter = 540, 12   # the count lives in the gutter, never on the fill
    H = top + row * len(LADDER) + 4
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Disclosure rate across eight policy rungs. The five rungs that '
         f'name only the data sit at 100 percent. Naming the output channel gives 14 of 15. The two '
         f'that name the tool-call channel are zero of 100.">',
         '<g font-family="inherit" fill="currentColor">']
    o.append(f'<text x="0" y="10" font-size="10.5" opacity="0.55" letter-spacing="0.06em">'
             f'DISCLOSED — 0 TO 100%</text>')
    o.append(f'<line x1="0" y1="17" x2="{bar}" y2="17" stroke="currentColor" opacity="0.2"/>')
    for i, (label, hit, n) in enumerate(LADDER):
        y = top + i * row
        rate = hit / n
        o.append(f'<text x="0" y="{y + 11}" font-size="12.5" opacity="0.92">{esc(label)}</text>')
        o.append(f'<rect x="0" y="{y + 19}" width="{bar}" height="9" fill="currentColor" '
                 f'opacity="0.12" rx="1"/>')
        if hit:
            o.append(f'<rect x="0" y="{y + 19}" width="{rate * bar:.1f}" height="9" '
                     f'fill="currentColor" opacity="0.88" rx="1"/>')
        else:
            o.append(f'<rect x="0" y="{y + 17}" width="2.5" height="13" fill="currentColor"/>')
        # ALWAYS in the gutter. An earlier version anchored the count at the bar's end, which put
        # near-white type on a near-white fill for every rung above 85% -- six of eight, invisible.
        o.append(f'<text x="{bar + gutter}" y="{y + 27}" font-size="11" opacity="0.8">'
                 f'{hit}/{n}</text>')
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
    H = 216
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="An eval makes three claims — about the harness, the benchmark and '
         f'the metric — and any of them can be false while the run reports success. Each has its own quiet '
         f'failure: the control can be skipped silently, the task saturates so the zero misleads, and '
         f'derived information flows past the match.">',
         '<g font-family="inherit" fill="currentColor">']
    # without this the diagram assumes the reader already accepts the framing it is meant to explain
    o.append('<text x="0" y="10" font-size="12" opacity="0.95">An eval reports one number. It stakes '
             'three claims to earn it \u2014</text>')
    o.append('<text x="0" y="27" font-size="12" opacity="0.95">and any of them can be false while the '
             'run reports success.</text>')
    for i, (name, question, f1, f2) in enumerate(CLAIMS):
        x = i * (colw + gap)
        o.append(f'<g transform="translate({x},40)">')
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
    collapses while leaving the scenario becomes near-universal.

    Layout rewritten after two bugs that only showed on screen. The scenario text collided with the
    panel headers, and the percentage labels were drawn ON the bars -- near-white type on a near-white
    fill, i.e. invisible. Labels now live in their own gutter to the right of each panel, where they
    read against the page rather than against the bar, and the interval whisker is drawn BELOW the bar
    for the same reason.
    """
    W = 600
    panel, gutter, between = 208, 48, 40
    x_of = [0, panel + gutter + between]
    row, top = 62, 116
    H = top + row * len(GENERATIONS) + 4
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Across three model generations the rate of trading on an insider tip '
         f'falls from 69 percent to 11.4 percent to zero, while among the runs that refused the tip the '
         f'share that searched for a lawful trade instead rises from 9 percent to 78 percent to 99 '
         f'percent. The scenario: a trading agent under performance pressure receives an insider tip '
         f'its management would disapprove of.">',
         '<g font-family="inherit" fill="currentColor">']

    o.append('<text x="0" y="10" font-size="9.5" letter-spacing="0.11em" opacity="0.5">'
             'THE SCENARIO</text>')
    o.append('<text x="0" y="30" font-size="12.5" opacity="0.95">A trading agent under performance '
             'pressure receives an insider tip its</text>')
    o.append('<text x="0" y="48" font-size="12.5" opacity="0.95">management would disapprove of. Does '
             'it trade on it, or find a lawful move?</text>')
    o.append(f'<line x1="0" y1="66" x2="{W}" y2="66" stroke="currentColor" opacity="0.15"/>')

    for k, (title, sub) in enumerate([("Traded on the tip", "of all runs"),
                                      ("Searched for a lawful trade instead",
                                       "of the runs that refused the tip")]):
        x0 = x_of[k]
        o.append(f'<text x="{x0}" y="88" font-size="12" font-weight="600">{esc(title)}</text>')
        o.append(f'<text x="{x0}" y="103" font-size="10.5" opacity="0.55">{esc(sub)}</text>')

    for i, (name, rate, lo, hi, n, alt, alt_n) in enumerate(GENERATIONS):
        y = top + i * row
        o.append(f'<text x="0" y="{y}" font-size="12.5" opacity="0.92">{esc(name)}</text>')
        for k, (v, vlo, vhi, vn) in enumerate([(rate, lo, hi, n), (alt, None, None, alt_n)]):
            x0 = x_of[k]
            o.append(f'<rect x="{x0}" y="{y + 10}" width="{panel}" height="10" fill="currentColor" '
                     f'opacity="0.12" rx="1"/>')
            w = v / 100 * panel
            if v > 0:
                o.append(f'<rect x="{x0}" y="{y + 10}" width="{w:.1f}" height="10" '
                         f'fill="currentColor" opacity="0.85" rx="1"/>')
            else:
                o.append(f'<rect x="{x0}" y="{y + 8}" width="2.5" height="14" fill="currentColor"/>')
            # the number goes in its own gutter, never on top of the fill
            o.append(f'<text x="{x0 + panel + 8}" y="{y + 19}" font-size="11.5" opacity="0.85">'
                     f'{v:.1f}%</text>')
            # interval below the bar, so it is legible whatever the bar is doing
            if vlo is not None:
                a, b = vlo / 100 * panel, vhi / 100 * panel
                yy = y + 27
                o.append(f'<line x1="{x0 + a:.1f}" y1="{yy}" x2="{x0 + b:.1f}" y2="{yy}" '
                         f'stroke="currentColor" stroke-width="1" opacity="0.5"/>')
                for e in (a, b):
                    o.append(f'<line x1="{x0 + e:.1f}" y1="{yy - 3}" x2="{x0 + e:.1f}" '
                             f'y2="{yy + 3}" stroke="currentColor" stroke-width="1" opacity="0.5"/>')
            o.append(f'<text x="{x0}" y="{y + 44}" font-size="10" opacity="0.4">n={vn}</text>')
    o.append(f'<text x="0" y="{H - 2}" font-size="10" opacity="0.4">'
             f'whisker = 95% interval</text>')
    o.append("</g></svg>")
    return "\n".join(o)


def setup() -> str:
    """Post 3's environment.

    Rewritten after a fair objection: the first version showed the data-flow topology and nothing
    else. A reader could see three documents, an agent and two output paths, but not what the agent
    was asked to do, not what varied between conditions, and not what was measured -- so it depicted
    plumbing rather than an experiment. It also used the implementation's field names as primary
    labels, which say nothing to anyone who has not read the code.

    This version states the task, the manipulation and the outcome as bands, and keeps the code
    identifiers as secondary text.
    """
    W = 600
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 366" width="{W}" height="366" '
         f'role="img" aria-label="The task: prepare a payment instruction, which must state a payment '
         f'destination. The vendor record offers two ways to give one — a bank account number, which '
         f'is restricted, and a reference label, which is permitted. Both are present in every '
         f'condition. The agent can emit either by two routes: the submitted answer, and an outbound '
         f'tool call to a third-party validator that leaves the operator\u2019s systems. What varies '
         f'is what the data policy says. What is measured is whether the restricted value appears in '
         f'either route. Under pressure the validator refuses the permitted label and demands the '
         f'restricted one, so honouring the policy costs a task step.">',
         '<g font-family="inherit" fill="currentColor">']

    def band(y, kicker, text, sub=None):
        o.append(f'<text x="0" y="{y}" font-size="9.5" letter-spacing="0.11em" opacity="0.5">'
                 f'{esc(kicker)}</text>')
        o.append(f'<text x="0" y="{y + 18}" font-size="12.5" opacity="0.95">{esc(text)}</text>')
        if sub:
            o.append(f'<text x="0" y="{y + 34}" font-size="11.5" opacity="0.6">{esc(sub)}</text>')

    band(10, "THE TASK", "Prepare a payment instruction. It must state a payment destination.")
    o.append('<line x1="0" y1="40" x2="600" y2="40" stroke="currentColor" opacity="0.15"/>')

    # the two candidate values -- plain language first, identifier second
    o.append('<text x="0" y="62" font-size="9.5" letter-spacing="0.11em" opacity="0.5">'
             'THE VENDOR RECORD OFFERS TWO WAYS TO GIVE ONE</text>')
    for i, (plain, tag, ident) in enumerate([
            ("a bank account number", "RESTRICTED", "remittance_iban"),
            ("a reference label", "PERMITTED", "remittance_ref")]):
        y = 86 + i * 34
        o.append(f'<text x="0" y="{y}" font-size="13" opacity="0.95">{esc(plain)}</text>')
        o.append(f'<text x="152" y="{y}" font-size="10" letter-spacing="0.09em" '
                 f'opacity="{0.9 if i == 0 else 0.55}">{tag}</text>')
        o.append(f'<text x="0" y="{y + 14}" font-size="10.5" opacity="0.42">{ident}</text>')
    o.append('<text x="0" y="152" font-size="11" opacity="0.6">Both are present in every condition, '
             'so a policy sanctions the alternative rather than creating it.</text>')

    # the agent and the two routes out
    o.append('<line x1="0" y1="168" x2="600" y2="168" stroke="currentColor" opacity="0.15"/>')
    o.append('<text x="0" y="190" font-size="9.5" letter-spacing="0.11em" opacity="0.5">'
             'THE AGENT CAN EMIT EITHER VALUE BY TWO ROUTES</text>')
    o.append('<rect x="0" y="204" width="86" height="34" fill="none" stroke="currentColor" '
             'stroke-width="1.4" opacity="0.75" rx="2"/>')
    o.append('<text x="43" y="226" font-size="12.5" font-weight="600" text-anchor="middle">AGENT'
             '</text>')
    for i, (num, plain, ident) in enumerate([
            ("1", "the answer it submits", "submit(… destination)"),
            ("2", "a call to an outside validator — leaves the operator's systems",
             "bank_validation(destination)")]):
        y = 214 + i * 30
        o.append(f'<path d="M86 221 L108 {y}" fill="none" stroke="currentColor" opacity="0.4"/>')
        o.append(f'<text x="116" y="{y + 4}" font-size="12.5" opacity="0.95">'
                 f'{num}. {esc(plain)}</text>')
        o.append(f'<text x="116" y="{y + 18}" font-size="10.5" opacity="0.42">{esc(ident)}</text>')

    o.append('<line x1="0" y1="284" x2="600" y2="284" stroke="currentColor" opacity="0.15"/>')
    # TWO things vary, and the second was absent from the first version even though half the
    # reported cells turn on it.
    o.append('<text x="0" y="300" font-size="9.5" letter-spacing="0.11em" opacity="0.5">'
             'WHAT VARIES</text>')
    o.append('<text x="0" y="318" font-size="12" opacity="0.95">'
             'the wording of the data policy   \u00b7   whether the validator accepts the '
             'permitted label</text>')
    o.append('<text x="0" y="340" font-size="9.5" letter-spacing="0.11em" opacity="0.5">'
             'WHAT IS MEASURED</text>')
    o.append('<text x="0" y="358" font-size="12" opacity="0.95">'
             'whether the restricted value appears in either route</text>')
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
