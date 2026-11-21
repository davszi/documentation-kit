#!/usr/bin/python3 -I
"""Draw the figures of the approval-failed-open record and its page.

Usage (from the repository root):
    python3 -I docs/topics/approval-failed-open/draw_figures.py [--check]

Reads measurement/timeline.csv and measurement/summary.txt beside this script
(ADP `main` at b8b80e0b, measured read-only on 2026-11-15) and numbers.md.
Every number a figure prints is read from numbers.md, and the script asserts
it against the measured series it draws, so a figure cannot show a number the
record does not hold. numbers.md itself must be current: `numbers.py --check`
runs first.

Writes, for the page, one HTML fragment per figure under
docs/site/fragments/approval-failed-open/ (each holds a wide and an upright
SVG; the page stylesheet shows one by the figure's width), and, for the
record, standalone SVG files with their manifest under figures/: each in the
dark theme the page shows (`pileup-wide.svg`) and in the light theme for
slides and print beside it (`pileup-wide.light.svg`, tooling/figure_themes.py).
The page fragments are dark only. With --check it writes nothing and exits 1
when a file differs.

The colours are literal (tooling/svg_figures.py explains why). Each SVG draws
its own surface, so it reads the same on the kit's dark pages and in any
viewer with a light background. Stdlib only.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
import datetime as dt
import html
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tooling"))
from figure_themes import LIGHT, variant_path  # noqa: E402
from svg_figures import SANS, generated_header, standalone  # noqa: E402

TOPIC = os.path.relpath(HERE, REPO)
SCRIPT = f"{TOPIC}/draw_figures.py"
FRAGMENTS = os.path.join(REPO, "docs", "site", "fragments", "approval-failed-open")
FIGDIR = os.path.join(HERE, "figures")
INPUTS = [f"{TOPIC}/measurement/timeline.csv", f"{TOPIC}/measurement/summary.txt", f"{TOPIC}/numbers.md"]

# Surface, ink and tones. Series colours: the reference categorical palette's
# dark steps (dataviz skill), validated on SURFACE: adjacent CVD dE >= 8.4,
# normal-vision dE >= 19.3, all >= 3:1.
SURFACE, INK, SUB, DIM, GRID, RULE = "#121a24", "#e6edf3", "#a9b4c2", "#7d8896", "#243041", "#3a4757"
HARNESS, PQ, ATTENDED, POOL, DOCTOOLS = "#3987e5", "#d95926", "#199e70", "#c98500", "#d55181"
WORDS, DOCS, ALERT, ACCENT = "#9085e9", "#8b97a6", "#ff7b72", "#39d2c0"
GROUPS = [  # stack order, bottom to top
    ("Per-question run harnesses", "code_harness", HARNESS),
    ("Other qualification code", "code_pq_other", PQ),
    ("Attended evidence", "code_attended", ATTENDED),
    ("Resource slot and pool", "code_pool", POOL),
    ("Documentation and evidence tooling", ("code_doctools", "code_evidencetools"), DOCTOOLS),
]


@dataclass(frozen=True)
class PileupColors:
    """The colours of the pile-up figure, the one figure drawn in both themes."""
    surface: str
    ink: str
    sub: str
    dim: str
    grid: str
    groups: tuple  # one per GROUPS entry, in its order
    words: str
    on_band: str        # labels inside the harness and qualification bands
    shade: str          # the cleanup band, at shade_opacity
    shade_opacity: str
    hairline_opacity: str  # the turning-point lines, in ink


PILEUP_DARK = PileupColors(SURFACE, INK, SUB, DIM, GRID, tuple(c for _n, _col, c in GROUPS), WORDS, "#ffffff", "#ffffff", "0.05",
                           "0.35")
# Light: neutrals from figure_themes.LIGHT. Groups keep the hue of the reference
# palette's light steps, darkened only as far as needed: the two labelled bands
# carry white text (4.50:1), the rest are marks that clear 3:1 on the cleanup
# shade too (3.30:1 on white). Adjacent in the stack: normal-vision dE >= 16.4,
# protan/deutan dE >= 10.0 (OKLab x100). Ink hairlines need more opacity on white.
PILEUP_LIGHT = PileupColors(LIGHT.bg, LIGHT.ink, LIGHT.sub, LIGHT.dim, LIGHT.line,
                            ("#3077cf", "#cd4d10", "#4e9c79", "#bf8102", "#d56b94"), "#6250d6", "#ffffff", LIGHT.ink, "0.05",
                            "0.5")
PILEUP_THEMES = {"dark": PILEUP_DARK, "light": PILEUP_LIGHT}


# --- inputs -------------------------------------------------------------------
def load_numbers():
    """Id -> value of the first table of numbers.md, plus the unit text."""
    values, units = {}, {}
    for line in open(os.path.join(HERE, "numbers.md")):
        m = re.match(r"\| `([a-z0-9_]+)` \| (-?[\d,.]+) \| ([^|]*) \|", line)
        if m:
            raw = m.group(2).replace(",", "")
            values[m.group(1)] = float(raw) if "." in raw else int(raw)
            units[m.group(1)] = m.group(3).strip()
    return values, units


with open(os.path.join(HERE, "measurement", "timeline.csv"), newline="") as fh:
    ROWS = list(csv.DictReader(fh))
BY = {r["date"]: r for r in ROWS}
N, UNIT = load_numbers()


def series(col, start="2026-09-15"):
    cols = col if isinstance(col, tuple) else (col,)
    return [sum(int(r[c]) for c in cols) for r in ROWS if r["date"] >= start]


def at(col, day):
    cols = col if isinstance(col, tuple) else (col,)
    return sum(int(BY[day][c]) for c in cols)


def n(key, measured=None):
    """A number the figures print: from numbers.md, checked against the series."""
    value = N[key]
    if measured is not None:
        assert value == measured, f"{key}: numbers.md has {value}, the measurement gives {measured}"
    return value


def fmt(value):
    return f"{value:,}"


def words(r):
    return int(r["added_words_open"]) + int(r["added_words_worklog"]) + int(r["added_words_sessions"])


def first_days():
    """Subsystem -> first day, as summarize.py printed them in summary.txt."""
    found = {}
    for line in open(os.path.join(HERE, "measurement", "summary.txt")):
        m = re.match(r"- (.+?) \((\d{4}-\d{2}-\d{2})\): (\d+) doc lines", line)
        if m:
            found[m.group(1)] = m.group(2)
    return found


# --- drawing helpers ------------------------------------------------------------
def t(x, y, s, size=16, fill=INK, anchor="start", weight=400, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{SANS}"{extra}>{html.escape(s)}</text>')


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}" fill="{fill}"{extra}/>'


def line(x1, y1, x2, y2, stroke, width=1, extra=""):
    return f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{stroke}" stroke-width="{width}" fill="none"{extra}/>'


def svg(fid, variant, width, height, title, desc, body, surface=SURFACE):
    """An SVG with its own surface; ids are unique per figure and variant."""
    sid = f"{fid}-{variant}"
    return (f'<svg class="inline-fig afo-{variant}" viewBox="0 0 {width} {height}" role="img" '
            f'aria-labelledby="{sid}-title {sid}-desc">\n'
            f'<title id="{sid}-title">{html.escape(title)}</title>\n<desc id="{sid}-desc">{html.escape(desc)}</desc>\n'
            f'<rect x="0" y="0" width="{width}" height="{height}" rx="14" fill="{surface}"/>\n'
            + "\n".join(body) + "\n</svg>")


def figure(fid, number, title, wide, tall, caption):
    return (f'<figure class="afo-fig" id="{fid}">\n'
            f'<div class="afo-scroll" role="region" aria-label="{html.escape(title, quote=True)}" tabindex="0" data-reader-horizontal>\n'
            f'{wide}\n{tall}\n</div>\n<figcaption><b>Figure {number}.</b> {caption}</figcaption>\n</figure>\n')


def badge(x, y, kind, size=14):
    """The statement kind a figure shows: Measured or Interpretation."""
    color = ACCENT if kind == "Measured" else "#bc8cff"
    w = len(kind) * size * 0.62 + 18
    dash = '' if kind == "Measured" else ' stroke-dasharray="5 4"'
    return (f'<rect x="{x:.1f}" y="{y - size - 4:.1f}" width="{w:.1f}" height="{size + 12:.1f}" rx="{(size + 12) / 2:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="1.5"{dash}/>' + t(x + w / 2, y + 2, kind.upper(), size - 2, color, "middle", 600,
                                                                            ' letter-spacing="1.2"'))


def day_x(day, x0, x1, start, end):
    d = dt.date.fromisoformat(day) if isinstance(day, str) else day
    return x0 + (d - start).days / ((end - start).days) * (x1 - x0)


# --- sizes ------------------------------------------------------------------------------
# The wide drawing is shown from 700 px of figure width up, so a 16 px label never
# renders below 11.2 px; the upright one is 300 units wide with labels of 13 units
# or more, 12.3 px in the 284 px column of a 390 px phone.
WIDE_W, TALL_W = 1000, 300


def sizes(wide):
    return (WIDE_W, 17, 16) if wide else (TALL_W, 15, 13)


def levels(xs, r):
    """Stack discs that would touch: the level of each x, lowest free first."""
    last, out = {}, []
    for x in xs:
        lv = 0
        while lv in last and x - last[lv] < 2 * r + 3:
            lv += 1
        last[lv] = x
        out.append(lv)
    return out


# --- Figure 2: the pile-up ---------------------------------------------------------
START, END = dt.date(2026, 9, 15), dt.date(2026, 11, 16)
DAYS = [dt.date.fromisoformat(r["date"]) for r in ROWS if r["date"] >= START.isoformat()]
EVENTS = [  # number, day, wide label, upright label
    (1, "2026-09-27", "first qualification code", "first qualification code"),
    (2, "2026-10-05", f"one commit adds {N['add_b_15d3e02a'] / 1e9:.2f} GB of run output",
     f"{N['add_b_15d3e02a'] / 1e9:.2f} GB run output, one commit"),
    (3, "2026-10-08", f"harness pattern; {fmt(N['w_max_day'])} words in a day", f"harness pattern; {fmt(N['w_max_day'])} words"),
    (4, "2026-10-17", "plans move into frozen copies", "plans into frozen copies"),
    (5, "2026-10-28", "the attended-session recorder", "attended-session recorder"),
    (6, "2026-11-04", "attended parts, slot and pool land", "attended parts, slot, pool"),
    (7, "2026-11-10", f"peak {fmt(N['sup_peak'])} lines; cleanup starts", f"peak {fmt(N['sup_peak'])}; cleanup"),
    (8, "2026-11-15", "attended evidence retired", "attended evidence retired"),
]


def pileup(variant, c=PILEUP_DARK):
    wide = variant == "wide"
    W, fs, small = sizes(wide)
    x0, x1 = (78, 980) if wide else (42, 290)
    body = []
    # Legend: every series named, identity never by colour alone.
    groups = [(name, col, color) for (name, col, _dark), color in zip(GROUPS, c.groups)]
    entries = [(name, color, "box") for name, _col, color in groups] + [("Product code (contrast)", c.ink, "line"),
                                                                        ("Words written per day", c.words, "box")]
    y = 30 if wide else 26
    if wide:
        for i, (name, color, kind) in enumerate(entries):
            cx, cy = 20 + (i % 3) * 330, y + (i // 3) * 26
            body.append(rect(cx, cy - 12, 16, 14, color, ' rx="3"') if kind == "box" else line(cx, cy - 5, cx + 18, cy - 5, color, 3))
            body.append(t(cx + 26, cy, name, small, c.sub))
        y += 3 * 26 + 18
    else:
        for i, (name, color, kind) in enumerate(entries):
            cy = y + i * 19
            body.append(rect(12, cy - 11, 13, 12, color, ' rx="3"') if kind == "box" else line(12, cy - 5, 26, cy - 5, color, 3))
            body.append(t(33, cy, name.replace("Documentation and evidence", "Docs and evidence"), small, c.sub))
        y += len(entries) * 19 + 14
    r = 12 if wide else 9
    xe_all = [min(day_x(day, x0, x1, START, END), x1 - 1) for _k, day, _w, _u in EVENTS]
    lv = levels(xe_all, r) if not wide else [0] * len(EVENTS)
    top = y + 34 + (2 * r + 3) * max(lv)
    h = 300 if wide else 220
    bottom = top + h
    ymax = 300000

    def sy(v):
        return bottom - v / ymax * h

    body.append(t(x0 if wide else 12, top - (22 if wide else 28) - (2 * r + 3) * max(lv), "Lines of Python", fs, c.ink, weight=600))
    for v in range(0, ymax + 1, 50000 if wide else 100000):
        body.append(line(x0, sy(v), x1, sy(v), c.grid, 1))
        body.append(t(x0 - 6, sy(v) + 5, f"{v // 1000}k" if v else "0", small, c.dim, "end"))
    xs = [day_x(d, x0, x1, START, END) for d in DAYS] + [x1]
    cx0, cx1 = day_x("2026-11-10", x0, x1, START, END), x1
    body.append(rect(cx0, top - 6, cx1 - cx0, bottom - top + 6, c.shade, f' fill-opacity="{c.shade_opacity}"'))
    # Stacked bands as post steps; a surface-coloured edge keeps a gap between fills.
    base = [0] * len(DAYS)
    for name, col, color in groups:
        upper = [b + v for b, v in zip(base, series(col))]
        pts = []
        for i, u in enumerate(upper):
            pts += [(xs[i], sy(u)), (xs[i + 1], sy(u))]
        low = []
        for i in range(len(base) - 1, -1, -1):
            low += [(xs[i + 1], sy(base[i])), (xs[i], sy(base[i]))]
        d = "M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts + low) + "Z"
        body.append(f'<path d="{d}" fill="{color}" stroke="{c.surface}" stroke-width="1.2"><title>{html.escape(name)}</title></path>')
        base = upper
    assert max(base) == n("sup_peak"), "stack top differs from sup_peak"
    prod = series("code_product")
    pts = []
    for i, v in enumerate(prod):
        pts += [(xs[i], sy(v)), (xs[i + 1], sy(v))]
    body.append('<path d="M' + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + f'" fill="none" stroke="{c.ink}" stroke-width="2.6">'
                '<title>Product code</title></path>')
    assert prod[-1] == n("prod_now", at("code_product", "2026-11-15"))
    body.append(t(xs[1] + 4, sy(prod[0]) - 10, "product code", small, c.ink, weight=600))
    cross = UNIT["cross_day"].split(" on ")[1].split(",")[0]
    assert at(("code_attended", "code_doctools", "code_evidencetools", "code_pool", "code_harness", "code_pq_other"), cross) == n("cross_day")
    xc = day_x(cross, x0, x1, START, END)
    body.append(f'<circle cx="{xc:.1f}" cy="{sy(n("cross_day")):.1f}" r="{6 if wide else 5}" fill="{c.surface}" stroke="{c.ink}" stroke-width="2"/>')
    body.append(t(xc - 10, sy(n("cross_day")) - 13, f"passes the product on {cross[5:]}" if wide else f"passes it {cross[5:]}",
                  small, c.ink, "end"))
    xp = day_x("2026-11-10", x0, x1, START, END)
    if wide:
        body.append(t(xp - 14, sy(n("sup_peak")) - 12, f"{fmt(n('sup_peak'))} lines, three times the product", fs, c.ink, "end", 600))
        li = len(DAYS) - 3
        hb, pq = series("code_harness")[li], series("code_pq_other")[li]
        body.append(t(xs[li] - 10, sy(hb * 0.45), "per-question run harnesses", small, c.on_band, "end", 600))
        body.append(t(xs[li] - 10, sy(hb + pq * 0.5) + 5, "other qualification code", small, c.on_band, "end", 600))
        body.append(t(cx0 + (cx1 - cx0) / 2, top + 16, "cleanup", small, c.sub, "middle"))
    else:
        body.append(t(xp - 6, sy(n("sup_peak")) - 9, f"peak {fmt(n('sup_peak'))}", small, c.ink, "end", 600))
    # Words panel.
    wtop = bottom + (44 if wide else 42)
    wh = 110 if wide else 80
    wbottom = wtop + wh
    wmax = 56000

    def wy(v):
        return wbottom - v / wmax * wh

    body.append(t(x0 if wide else 12, wtop - 12, "Words written per day for the developer" if wide else "Words per day", fs, c.ink, weight=600))
    for v in (0, 25000, 50000):
        body.append(line(x0, wy(v), x1, wy(v), c.grid, 1))
        body.append(t(x0 - 6, wy(v) + 5, f"{v // 1000}k" if v else "0", small, c.dim, "end"))
    body.append(rect(cx0, wtop - 2, cx1 - cx0, wbottom - wtop + 2, c.shade, f' fill-opacity="{c.shade_opacity}"'))
    wseries = [words(r_) for r_ in ROWS if r_["date"] >= START.isoformat()]
    bw = (x1 - x0) / ((END - START).days)
    for i, v in enumerate(wseries):
        if v:
            body.append(rect(xs[i] + bw * 0.12, wy(v), bw * 0.76, wbottom - wy(v), c.words, ' rx="1"'))
    imax = max(range(len(wseries)), key=lambda i: wseries[i])
    assert wseries[imax] == n("w_max_day") and DAYS[imax].isoformat() == UNIT["w_max_day"].split(" on ")[1]
    body.append(t(xs[imax] + bw + 5, wy(wseries[imax]) + 13, f"{fmt(n('w_max_day'))} on {DAYS[imax].isoformat()[5:]}", small, c.ink))
    for m in (dt.date(2026, 10, 1), dt.date(2026, 11, 1)):
        xm = day_x(m, x0, x1, START, END)
        body.append(line(xm, wbottom, xm, wbottom + 6, c.dim, 1))
        body.append(t(xm, wbottom + 22, m.strftime("1 %b"), small, c.dim, "middle"))
    body.append(t(x0, wbottom + 22, "15 Sep", small, c.dim, "middle" if not wide else "start"))
    # Turning points: a hairline through both panels and a numbered disc above.
    for (k, _day, _w, _u), xe, level in zip(EVENTS, xe_all, lv):
        cy = top - 6 - r - level * (2 * r + 3)
        body.append(line(xe, cy + r, xe, wbottom, c.ink, 1, f' stroke-opacity="{c.hairline_opacity}"'))
        body.append(f'<circle cx="{xe:.1f}" cy="{cy:.1f}" r="{r}" fill="{c.ink}"/>')
        body.append(t(xe, cy + (5.5 if wide else 4.5), str(k), 16 if wide else 13, c.surface, "middle", 700))
    ky = wbottom + (58 if wide else 54)
    if wide:
        body.append(t(20, ky, "Turning points", fs, c.ink, weight=600))
        for i, (k, day, label, _u) in enumerate(EVENTS):
            kx, kyy = 20 + (i // 4) * 490, ky + 28 + (i % 4) * 26
            body.append(t(kx, kyy, f"{k}", small, c.ink, weight=700))
            body.append(t(kx + 22, kyy, day[5:], small, c.dim))
            body.append(t(kx + 80, kyy, label, small, c.sub))
        H = ky + 28 + 4 * 26
    else:
        body.append(t(12, ky, "Turning points (shaded: cleanup)", fs, c.ink, weight=600))
        for i, (k, day, _w, label) in enumerate(EVENTS):
            kyy = ky + 24 + i * 20
            body.append(t(12, kyy, f"{k}", small, c.ink, weight=700))
            body.append(t(28, kyy, day[5:], small, c.dim))
            body.append(t(70, kyy, label, small, c.sub))
        H = ky + 24 + 8 * 20
    title = "Supporting code piled up past the product, after weeks of plans"
    desc = (f"Stacked lines of supporting Python by group from 15 September to 15 November 2026, with product code as a line. "
            f"Supporting code passes the product on {cross}, peaks at {fmt(n('sup_peak'))} lines on 2026-11-10, three times the "
            f"product, and is {fmt(n('sup_now'))} lines on 2026-11-15. Below, words written per day; the largest day is "
            f"{fmt(n('w_max_day'))} words on 2026-10-08. Eight numbered turning points are listed under the chart.")
    return svg("fig-pileup", variant, W, int(H + 16), title, desc, body, c.surface), title


# --- Figure 1: the size against the product -------------------------------------------
def scale(variant):
    wide = variant == "wide"
    W, fs, small = sizes(wide)
    rows = [("2026-10-01", "1 Oct", "sup_1001", "prod_1001", None),
            ("2026-11-10", "10 Nov, peak", "sup_peak", "prod_1110", "three times the product"),
            ("2026-11-15", "15 Nov, today", "sup_now", "prod_now", None)]
    body = []
    xmax = 300000
    bx0, bx1, y = (190, 900, 30) if wide else (12, 236, 26)

    def sx(v):
        return bx0 + v / xmax * (bx1 - bx0)

    legend = [(GROUPS[0][2], "Per-question run harnesses", "Run harnesses"),
              (GROUPS[1][2], "Other qualification code", "Other qualification code"),
              (ATTENDED, "Attended evidence, slot and pool, tooling", "Attended, slot, pool, tooling")]
    for i, (c, wl, tl) in enumerate(legend):
        lx = (20 + i * 300) if wide else 12
        body.append(rect(lx, y - 12, 14, 14, c, ' rx="3"'))
        body.append(t(lx + 22, y, wl if wide else tl, small, SUB))
        if not wide:
            y += 19
    if not wide:
        body.append(line(12, y - 5, 26, y - 5, INK, 3))
        body.append(t(34, y, "Product code", small, SUB))
    y += 34 if wide else 30
    for day, label, skey, pkey, note in rows:
        sup = n(skey, sum(at(col, day) for _n, col, _c in GROUPS))
        prod = n(pkey, at("code_product", day))
        if wide:
            body.append(t(bx0 - 14, y + 20, label, fs, INK, "end", 600))
        else:
            body.append(t(12, y, label, fs, INK, weight=600))
            y += 9
        bar_h = 24 if wide else 18
        x = bx0
        for name, col, c in GROUPS:
            v = at(col, day)
            if v:
                body.append(rect(x, y, sx(v) - bx0 - 1, bar_h, c))
                x += sx(v) - bx0
        body.append(t(sx(sup) + 8, y + bar_h - 5, fmt(sup), small, INK, weight=600))
        py = y + bar_h + 7
        body.append(rect(bx0, py, sx(prod) - bx0, 6, INK, ' rx="2"'))
        body.append(t(sx(prod) + 8, py + 8, f"product {fmt(prod)}" + (f"; supporting code is {note}" if note and wide else ""),
                      small, SUB))
        y = py + (44 if wide else 36)
    if not wide:
        body.append(t(12, y - 6, "At the peak: three times the product", small, INK, weight=600))
        y += 18
    for v in range(0, xmax + 1, 100000):
        body.append(t(sx(v), y + 4, f"{v // 1000}k" if v else "0", small, DIM, "middle" if v else "start"))
    body.append(t(bx1 if wide else W - 12, y + 26, "lines of Python", small, DIM, "end"))
    H = y + 40
    title = "Supporting code against the product at three dates"
    desc = (f"Horizontal bars. On 1 October 2026 supporting code was {fmt(n('sup_1001'))} lines against {fmt(n('prod_1001'))} "
            f"lines of product code; at the peak on 10 November {fmt(n('sup_peak'))} against {fmt(n('prod_1110'))}, three times "
            f"the product; on 15 November {fmt(n('sup_now'))} against {fmt(n('prod_now'))}. The per-question run harnesses and "
            "the other qualification code make up most of the bars.")
    return svg("fig-scale", variant, W, int(H), title, desc, body), title


# --- Figure 3: each pile's peak against today ---------------------------------------
def piles(variant):
    wide = variant == "wide"
    W, fs, small = sizes(wide)
    rows = [  # wide name, upright name, peak id, now id, colour, verdict
        ("Per-question run harnesses", "Run harnesses", "harn_peak", "harn_now", HARNESS, "still there"),
        ("Other qualification code", "Other qualification code", "pq_now", "pq_now", PQ, "still there"),
        ("Attended evidence", "Attended evidence", "att_peak", "att_now", ATTENDED, "retired"),
        ("Plans in docs/open", "Plans in docs/open", "open_peak", "open_now", DOCS, "smaller"),
        ("Resource slot and pool", "Resource slot and pool", "pool_peak", "pool_now", POOL, "still there"),
        ("Frozen document copies", "Frozen document copies", "frozen_peak_lines", "frozen_now_lines", DOCS, "deleted"),
    ]
    assert n("harn_now") == at("code_harness", "2026-11-15") and n("pq_now") == max(series("code_pq_other"))
    assert n("frozen_now_lines") == at("frozen_doc_copy_lines", "2026-11-15") == 0
    body = []
    xmax = 140000
    nx, bx0, bx1, y = (20, 300, 700, 34) if wide else (12, 12, 288, 26)

    def sx(v, top=xmax):
        return bx0 + v / top * (bx1 - bx0)

    def verdict_text(x, y_, verdict):
        keep = verdict == "still there"
        return t(x, y_, verdict, small, INK if keep else SUB, "end", 700 if keep else 400)

    body.append(rect(nx, y - 13, 26, 15, "#ffffff", ' fill-opacity="0.12" stroke="#ffffff" stroke-opacity="0.6" stroke-width="1.5" rx="3"'))
    body.append(t(nx + 34, y, "peak", small, SUB))
    kx = nx + (100 if wide else 86)
    body.append(rect(kx, y - 13, 26, 15, "#ffffff", ' rx="3"'))
    body.append(t(kx + 34, y, "15 Nov 2026", small, SUB))
    if wide:
        body.append(t(W - 20, y, "lines of Python or text", small, DIM, "end"))
    y += 30 if wide else 30
    for wname, tname, pk, nk, color, verdict in rows:
        peak, now = n(pk), n(nk)
        bar_h = 22 if wide else 16
        if wide:
            body.append(t(nx, y + 17, wname, fs, INK, weight=600))
        else:
            body.append(t(nx, y, tname, fs, INK, weight=600))
            body.append(verdict_text(W - 12, y, verdict))
            y += 8
        body.append(rect(bx0, y, sx(peak) - bx0, bar_h, color, f' fill-opacity="0.18" stroke="{color}" stroke-width="1.5" rx="3"'))
        if now:
            body.append(rect(bx0, y, sx(now) - bx0, bar_h, color, ' rx="3"'))
        label = f"{fmt(peak)} → {fmt(now)}"
        if wide:
            body.append(t(bx1 + 20, y + 17, label, small, INK))
            body.append(verdict_text(W - 20, y + 17, verdict))
            y += 42
        else:
            body.append(t(nx, y + bar_h + 17, label, small, SUB))
            y += bar_h + 44
    for v in range(0, xmax + 1, 50000 if wide else 70000):
        body.append(line(sx(v), y - 8, sx(v), y - 2, DIM, 1))
        body.append(t(sx(v), y + 14, f"{v // 1000}k" if v else "0", small, DIM,
                      "start" if not v else "end" if v == xmax and not wide else "middle"))
    y += 34
    body.append(line(nx, y, W - (20 if wide else 12), y, RULE, 1))
    y += 30
    peak_gb, now_gb = n("exp_b_peak") / 1e9, n("exp_b_now") / 1e9
    gmax = 7.0
    bar_h = 22 if wide else 16
    if wide:
        body.append(t(nx, y + 17, "Run output in Git", fs, INK, weight=600))
    else:
        body.append(t(nx, y, "Run output in Git", fs, INK, weight=600))
        body.append(verdict_text(W - 12, y, "still there"))
        y += 8
    body.append(rect(bx0, y, sx(peak_gb, gmax) - bx0, bar_h, DOCS, f' fill-opacity="0.18" stroke="{DOCS}" stroke-width="1.5" rx="3"'))
    body.append(rect(bx0, y, sx(now_gb, gmax) - bx0, bar_h, DOCS, ' rx="3"'))
    label = f"{peak_gb:.2f} GB → {now_gb:.2f} GB"
    if wide:
        body.append(t(bx1 + 20, y + 17, label, small, INK))
        body.append(verdict_text(W - 20, y + 17, "still there"))
        y += 34
    else:
        body.append(t(nx, y + bar_h + 17, label, small, SUB))
        y += bar_h + 30
    for v in range(0, 8, 2 if wide else 3):
        body.append(t(sx(v, gmax), y + 10, f"{v} GB", small, DIM, "middle" if v else "start"))
    H = y + 26
    title = "What the cleanup removed from each pile, and what is still there"
    desc = ("Each pile's peak as an outlined bar and its size on 15 November 2026 as a filled bar. "
            f"Per-question run harnesses {fmt(n('harn_peak'))} lines at the peak, {fmt(n('harn_now'))} now; other qualification "
            f"code {fmt(n('pq_now'))}, at its peak now; attended evidence {fmt(n('att_peak'))} to {fmt(n('att_now'))}; plans in "
            f"docs/open {fmt(n('open_peak'))} to {fmt(n('open_now'))}; resource slot and pool {fmt(n('pool_peak'))} to "
            f"{fmt(n('pool_now'))}; frozen document copies {fmt(n('frozen_peak_lines'))} to 0. Run output in Git "
            f"{peak_gb:.2f} GB at the peak, {now_gb:.2f} GB now.")
    return svg("fig-piles", variant, W, int(H), title, desc, body), title


# --- Figure 4: the approval step that failed open (interpretation) -------------------
def arrow(x1, y1, x2, y2, color, width=3):
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 12 * math.cos(a), y2 - 12 * math.sin(a)
    return (line(x1, y1, hx, hy, color, width)
            + f'<path d="M{x2:.1f} {y2:.1f}L{hx + 6 * math.sin(a):.1f} {hy - 6 * math.cos(a):.1f}'
              f'L{hx - 6 * math.sin(a):.1f} {hy + 6 * math.cos(a):.1f}Z" fill="{color}"/>')


def gate(variant):
    wide = variant == "wide"
    W, fs, small = sizes(wide)
    body = []

    def box(x, y, w, h, head, lines_, color, dashed=False, fill_opacity="0.10"):
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" fill-opacity="{fill_opacity}" '
               f'stroke="{color}" stroke-width="2"{dash}/>', t(x + 14, y + (30 if wide else 24), head, fs, INK, weight=600)]
        for i, s in enumerate(lines_):
            out.append(t(x + 14, y + (56 if wide else 45) + i * (22 if wide else 18), s, small, SUB))
        return out

    def barrier(x, y, h):
        """Two posts with an opening between them: the gate stands open."""
        return [line(x, y, x, y + h * 0.3, ALERT, 5), line(x, y + h * 0.7, x, y + h, ALERT, 5)]

    words_day = fmt(n("w_per_day_build"))
    if wide:
        body.append(badge(20, 36, "Interpretation", 18))
        # Each step brings more plans: the loop over the top.
        body.append(f'<path d="M845 92V64H155V84" stroke="{DIM}" stroke-width="2" fill="none" stroke-dasharray="6 5"/>')
        body.append(f'<path d="M155 92l-6-11h12z" fill="{DIM}"/>')
        body.append(t(500, 56, "each step brings more plans", small, DIM, "middle"))
        body += box(20, 92, 270, 128, "Agents write plans", [f"{words_day} words per", "calendar day for 47 days"], WORDS)
        body.append(arrow(290, 156, 372, 156, SUB))
        body += box(380, 92, 250, 128, "Approval", ["the developer reads,", "then answers"], SUB, fill_opacity="0.04")
        body += barrier(600, 102, 108)
        body.append(t(588, 162, "open", small, ALERT, "end", 600))
        body.append(arrow(602, 156, 702, 156, ALERT))
        body.append(t(652, 144, "yes", small, ALERT, "middle", 600))
        body += box(710, 92, 270, 128, "Work goes ahead", ["code and documents added,", "none removed, no total"], PQ)
        body.append(arrow(845, 220, 845, 262, PQ))
        body.append(t(832, 250, f"{fmt(n('sup_peak'))} lines at the peak", small, INK, "end", 600))
        body += box(20, 268, 470, 112, "Fails closed: what the step assumed", ["work waits until the text is read;", "more text means slower work"],
                    ACCENT, True)
        body += box(510, 268, 470, 112, "Fails open: what happened", ["more text than one person reads;", "yes without reading, work goes on"],
                    ALERT)
        H = 396
    else:
        body.append(badge(12, 28, "Interpretation", 14))
        y = 48
        body += box(12, y, 276, 84, "Agents write plans", [f"{words_day} words per calendar", "day for 47 days"], WORDS)
        body.append(arrow(150, y + 84, 150, y + 116, SUB))
        y += 120
        body += box(12, y, 276, 84, "Approval", ["the developer reads,", "then answers"], SUB, fill_opacity="0.04")
        # The same open gate, turned: two posts across the box's lower edge.
        body.append(line(110, y + 84, 138, y + 84, ALERT, 5))
        body.append(line(162, y + 84, 190, y + 84, ALERT, 5))
        body.append(arrow(150, y + 84, 150, y + 120, ALERT))
        body.append(t(198, y + 106, "open: yes", small, ALERT, "start", 600))
        y += 124
        body += box(12, y, 276, 84, "Work goes ahead", ["code and documents added,", "none removed, no total"], PQ)
        body.append(t(12, y + 106, f"{fmt(n('sup_peak'))} lines at the peak", small, INK, weight=600))
        y += 124
        body += box(12, y, 276, 84, "Fails closed: assumed", ["work waits until the text", "is read"], ACCENT, True)
        y += 96
        body += box(12, y, 276, 84, "Fails open: happened", ["more text than one person reads;", "yes without reading"], ALERT)
        H = y + 98
    title = "The approval step failed open"
    desc = (f"Diagram, an interpretation. Agents write plans, {words_day} words per calendar day for 47 days; the approval step "
            "expects the developer to read them before answering. A step that fails closed would hold work until the text is read. "
            f"This one failed open: with more text than one person reads, the answer was yes without reading, and work went ahead "
            f"to {fmt(n('sup_peak'))} lines of supporting code. Each step brought more plans.")
    return svg("fig-gate", variant, W, int(H), title, desc, body), title


# --- Figure 5: the two halves of the approval finding ----------------------------------
BUILDS = [  # summary.txt subsystem, label, approved
    ("per-experiment harnesses (sdk_reuse)", "Per-question harness pattern", False),
    ("run output in Git", "Run output in Git", False),
    ("frozen document copies", "Frozen document copies", False),
    ("attended (Plan 11, recorder)", "Attended-session recorder", False),
    ("attended_parts (Plan 11 implementation)", "Attended parts", True),
    ("native pool / slot", "Resource slot and pool", False),
    ("central evidence store", "Central evidence store", False),
]


def approvals(variant):
    wide = variant == "wide"
    W, fs, small = sizes(wide)
    body = []
    x0 = 20 if wide else 12
    y = 34 if wide else 28
    body.append(badge(x0, y, "Measured", 18 if wide else 14))
    y += 36 if wide else 32
    body.append(t(x0, y, "First half: approvals in agents' records, rarely in commits" if wide
                  else "First half: records, not commits", fs, INK, weight=600))
    y += 26 if wide else 22
    bx0, bx1 = (x0, 700) if wide else (x0, 212)

    def frac_bar(label, part, whole, color, note):
        nonlocal y
        h = 20 if wide else 16
        body.append(t(x0, y + 4, label, small, SUB))
        y += 12
        body.append(rect(bx0, y, bx1 - bx0, h, "#ffffff", ' fill-opacity="0.07" rx="3"'))
        body.append(rect(bx0, y, max((bx1 - bx0) * part / whole, 3), h, color, ' rx="3"'))
        body.append(t(bx1 + 10, y + h - 4, note, small, INK, weight=600))
        y += h + (26 if wide else 24)

    generic, named = n("appr_build_generic"), n("appr_build_named")
    assert generic + named == n("appr_build")
    frac_bar("Approval statements in the build-up's records that say “the user”, “owner” or “human”" if wide
             else "Records: “the user”, “owner”, “human”", generic, n("appr_build"), DOCS, f"{generic} of {n('appr_build')}")
    frac_bar("Commit messages that cite a decision, build-up" if wide else "Commits citing a decision, build-up",
             n("appr_cm_build"), n("commits_build"), ALERT, f"{n('appr_cm_build')} of {n('commits_build')}")
    frac_bar("Commit messages that cite a decision, cleanup" if wide else "Commits citing a decision, cleanup",
             n("appr_cm_clean"), n("commits_clean"), ACCENT, f"{n('appr_cm_clean')} of {n('commits_clean')}")
    y += 4
    body.append(line(x0, y, W - x0, y, RULE, 1))
    y += 34 if wide else 30
    body.append(t(x0, y, "Second half: no approval found in the 7 days before a build" if wide
                  else "Second half: no approval found", fs, INK, weight=600))
    if not wide:
        y += 19
        body.append(t(x0, y, "in the 7 days before each build", small, SUB))
    y += 14 if wide else 12
    start, end = dt.date(2026, 9, 24), dt.date(2026, 11, 12)
    tx0, tx1 = (330, 980) if wide else (12, 288)
    days = first_days()
    for name, label, approved in BUILDS:
        first = dt.date.fromisoformat(days[name])
        if wide:
            body.append(t(x0, y + 21, label, small, SUB))
            ry = y + 6
        else:
            body.append(t(x0, y + 14, label, small, SUB))
            ry = y + 22
        wx0 = day_x(first - dt.timedelta(days=7), tx0, tx1, start, end)
        xf = day_x(first, tx0, tx1, start, end) + (tx1 - tx0) / (end - start).days / 2
        body.append(line(tx0, ry + 9, tx1, ry + 9, GRID, 1))
        body.append(rect(wx0, ry, xf - wx0, 18, "#ffffff", ' fill-opacity="0.16" rx="3"'))
        if approved:
            xa = day_x("2026-11-02", tx0, tx1, start, end) + (tx1 - tx0) / (end - start).days / 2
            body.append(f'<circle cx="{xa:.1f}" cy="{ry + 9}" r="7" fill="{ACCENT}"/>')
            body.append(f'<circle cx="{xf:.1f}" cy="{ry + 9}" r="7" fill="{ACCENT}"/>')
            body.append(t(wx0 - 10, ry + 15, "“lets build it now fully”, 11-02" if wide else "approved 11-02", small, ACCENT, "end", 600))
        else:
            body.append(f'<circle cx="{xf:.1f}" cy="{ry + 9}" r="8" fill="{SURFACE}" stroke="{ALERT}" stroke-width="2"/>')
            body.append(line(xf - 4, ry + 5, xf + 4, ry + 13, ALERT, 2) + line(xf + 4, ry + 5, xf - 4, ry + 13, ALERT, 2))
        y += 32 if wide else 46
    for m, lab in ((dt.date(2026, 10, 1), "1 Oct"), (dt.date(2026, 11, 1), "1 Nov")):
        xm = day_x(m, tx0, tx1, start, end)
        body.append(t(xm, y + 12, lab, small, DIM, "middle"))
    y += 40
    key = [("no", "first file, no approval found"), ("win", "the 7 days searched"), ("yes", "approval found")]
    for i, (kind, text) in enumerate(key):
        kx = (x0 + i * 300) if wide else x0
        if kind == "no":
            body.append(f'<circle cx="{kx + 8}" cy="{y - 5}" r="8" fill="{SURFACE}" stroke="{ALERT}" stroke-width="2"/>')
            body.append(line(kx + 4, y - 9, kx + 12, y - 1, ALERT, 2) + line(kx + 12, y - 9, kx + 4, y - 1, ALERT, 2))
        elif kind == "win":
            body.append(rect(kx, y - 14, 26, 18, "#ffffff", ' fill-opacity="0.16" rx="3"'))
        else:
            body.append(f'<circle cx="{kx + 8}" cy="{y - 5}" r="7" fill="{ACCENT}"/>')
        body.append(t(kx + 34, y, text, small, SUB))
        if not wide:
            y += 22
    H = y + (20 if wide else 0)
    title = "Approvals were written into records, but six builds had none before them"
    desc = (f"Two measured halves. First: in the build-up the records carry {n('appr_build')} approval statements, {generic} of "
            f"them about the user, owner or human, but only {n('appr_cm_build')} of {n('commits_build')} commit messages cite a "
            f"decision, against {n('appr_cm_clean')} of {n('commits_clean')} in the cleanup. Second: for six builds, the harness "
            "pattern, run output in Git, the frozen copies, the recorder, the slot and pool, and the evidence store, the search "
            "found no approval in the seven days before their first file; the attended parts were approved on 2 November with "
            "the developer's words “lets build it now fully”.")
    return svg("fig-approvals", variant, W, int(H), title, desc, body), title


# --- Figure 6: what the cleanup deleted -----------------------------------------------
def cleanup(variant):
    wide = variant == "wide"
    W, fs, small = sizes(wide)
    body = []
    x0 = 20 if wide else 12
    bx0, bx1 = (x0, 980) if wide else (x0, 288)
    xmax = 280000

    def sx(v):
        return bx0 + v / xmax * (bx1 - bx0)

    parts = [("Evidence store", "del_a18d94e5", DOCS),
             ("Frozen copies", "del_1a541cf2", DOCS),
             ("Attended evidence", "del_3197ab3e", ATTENDED),
             ("Attended recorder", "del_1797bc4b", ATTENDED),
             (f"{n('nr_other_commits')} other commits", "nr_other_lines", DIM)]
    assert sum(n(k) for _l, k, _c in parts) == n("nr_lines_del")
    y = 34 if wide else 28
    body.append(t(x0, y, f"Lines deleted by the {n('nr_commits')} net-removal commits, 10–15 Nov" if wide
                  else f"Deleted by {n('nr_commits')} net-removal commits", fs, INK, weight=600))
    y += 16
    h = 34 if wide else 24
    x = bx0
    centres = []
    for label, key, color in parts:
        w = sx(n(key)) - bx0
        body.append(rect(x, y, w - 2, h, color, ' rx="3"'))
        centres.append(x + w / 2)
        x += w
    body.append(t(sx(n("nr_lines_del")) + 10, y + h - (10 if wide else 7), fmt(n("nr_lines_del")), fs, INK, weight=700))
    ly = y + h + (24 if wide else 20)
    if wide:
        # The first label sits under its own segment; the others climb a stair from the right,
        # so no leader crosses a label.
        body.append(t(bx0 + 2, ly, f"{parts[0][0]} {fmt(n(parts[0][1]))}", small, SUB))
        rest = list(zip(parts[1:], centres[1:]))
        for row, ((label, key, color), cx) in enumerate(reversed(rest)):
            yy = ly + row * 24
            body.append(line(cx, y + h + 2, cx, yy - 5, color, 1.5))
            body.append(t(cx + 8, yy, f"{label} {fmt(n(key))}", small, SUB))
        y = ly + (len(rest) - 1) * 24 + 46
    else:
        for i, (label, key, color) in enumerate(parts):
            yy = ly + i * 19
            body.append(rect(x0, yy - 11, 12, 12, color, ' rx="2"'))
            body.append(t(x0 + 20, yy, f"{label} {fmt(n(key))}", small, SUB))
        y = ly + len(parts) * 19 + 22
    body.append(t(x0, y, "Supporting code on the same scale: peak, then 15 Nov" if wide else "Supporting code, same scale", fs, INK, weight=600))
    y += 16
    drop = n("sup_drop_lines", n("sup_peak") - n("sup_now"))
    body.append(rect(bx0, y, sx(n("sup_peak")) - bx0, h, "#ffffff",
                     f' fill-opacity="0.06" stroke="{SUB}" stroke-width="1.5" stroke-dasharray="5 4" rx="3"'))
    x = bx0
    for _name, col, color in GROUPS:
        v = at(col, "2026-11-15")
        if v:
            body.append(rect(x, y, sx(v) - bx0 - (1 if v > 1000 else 0), h, color))
            x += sx(v) - bx0
    assert round(x, 3) == round(sx(n("sup_now")), 3)
    body.append(t(bx0, y + h + 20, f"{fmt(n('sup_now'))} of {fmt(n('sup_peak'))}", small, SUB))
    body.append(t(sx(n("sup_peak")) if wide else bx1, y + h + (20 if wide else 40), f"−{fmt(drop)} lines, {n('sup_drop_pct')} %",
                  small, INK, "end", 700))
    y += h + (52 if wide else 70)
    for v in range(0, xmax + 1, 100000):
        body.append(t(sx(v), y, f"{v // 1000}k" if v else "0", small, DIM, "middle" if v else "start"))
    H = y + 18
    title = "The cleanup deleted 145,353 lines, mostly documents; supporting code fell 8.2 %"
    desc = (f"Two bars on one scale. The {n('nr_commits')} net-removal commits from 10 to 15 November deleted "
            f"{fmt(n('nr_lines_del'))} lines: the evidence store {fmt(n('del_a18d94e5'))}, the frozen copies "
            f"{fmt(n('del_1a541cf2'))}, attended evidence {fmt(n('del_3197ab3e'))}, the attended recorder "
            f"{fmt(n('del_1797bc4b'))} and {n('nr_other_commits')} other commits {fmt(n('nr_other_lines'))}. Supporting code "
            f"fell from {fmt(n('sup_peak'))} to {fmt(n('sup_now'))} lines, by {fmt(drop)} or {n('sup_drop_pct')} %.")
    return svg("fig-cleanup", variant, W, int(H), title, desc, body), title


# --- output ---------------------------------------------------------------------------
CAPTIONS = {
    "fig-scale": (1, "Supporting code, stacked by group in the colours of Figure 2, against product code (white) on three days. "
                     "Measured from <code>timeline.csv</code>; every number is a row of the record's "
                     "<a href=\"../topics/approval-failed-open/numbers.md\">numbers</a>."),
    "fig-pileup": (2, "The pile-up. Top: lines of supporting Python by group, stacked, against product code (white line). "
                      "Bottom: words written per day into plans, the worklog and session notes. The numbered lines are the "
                      "turning points; the shaded band is the cleanup. Measured from <code>timeline.csv</code>."),
    "fig-piles": (3, "Each pile at its peak (outline) and on 15 November 2026 (filled). Code piles keep their colours from "
                     "Figure 2; document piles and run output are grey. Plans fell on 10-17 because they moved into the "
                     "frozen copies, not because they ended. Measured."),
    "fig-gate": (4, "How the approval step failed open. This is an interpretation; its two numbers are measured. A step that "
                    "fails closed would have slowed work as the text grew; this one let work through."),
    "fig-approvals": (5, "The two halves of the approval finding. Top: where approvals were written. Bottom: for each large "
                         "build, the seven days before its first file, searched for an approval. Measured, from "
                         "<code>approvals.csv</code>, <code>approvals_commit_messages.csv</code> and <code>summary.txt</code>; "
                         "a keyword search, so a lower bound on what Git shows."),
    "fig-cleanup": (6, "What the cleanup deleted, and how much the supporting code fell, on one scale. Deleted lines count "
                       "every text line a commit removed, documents and generated lists included. Measured from "
                       "<code>cleanups.csv</code> and <code>timeline.csv</code>."),
}
DRAW = {"fig-scale": scale, "fig-pileup": pileup, "fig-piles": piles, "fig-gate": gate,
        "fig-approvals": approvals, "fig-cleanup": cleanup}
FIG_INPUTS = {
    "fig-scale": ["timeline.csv", "numbers.md"], "fig-pileup": ["timeline.csv", "numbers.md"],
    "fig-piles": ["timeline.csv", "numbers.md"], "fig-gate": ["numbers.md"],
    "fig-approvals": ["summary.txt", "numbers.md"], "fig-cleanup": ["timeline.csv", "numbers.md"],
}


def outputs():
    files = {}
    for fid, draw in DRAW.items():
        (w, title), (tl, _t) = draw("wide"), draw("tall")
        number, caption = CAPTIONS[fid]
        header = generated_header(SCRIPT, [i if i == "numbers.md" else f"measurement/{i}" for i in FIG_INPUTS[fid]])
        files[os.path.join(FRAGMENTS, f"{fid}.html")] = header + figure(fid, number, title, w, tl, caption)
    # The record's figure, as files an image link can show: dark, and light beside it.
    manifest = {}
    for name, variant in (("pileup-wide.svg", "wide"), ("pileup-upright.svg", "tall")):
        for theme, colors in PILEUP_THEMES.items():
            drawn, _title = pileup(variant, colors)
            target = variant_path(os.path.join(FIGDIR, name), theme)
            files[str(target)] = standalone(re.sub(r' class="[^"]*"', "", drawn, count=1))
            manifest[target.name] = {"script": SCRIPT, "inputs": [f"{TOPIC}/measurement/timeline.csv", f"{TOPIC}/numbers.md"],
                                     "shows": "Figure 1 of the record; Figure 2 of the page" if theme == "dark"
                                     else f"{name} in the light theme, for slides and print"}
    files[os.path.join(FIGDIR, "manifest.json")] = json.dumps(manifest, indent=2) + "\n"
    return files


def main():
    check = "--check" in sys.argv[1:]
    run = subprocess.run([sys.executable, "-I", os.path.join(HERE, "numbers.py"), "--check"], capture_output=True, text=True)
    if run.returncode:
        sys.exit(f"numbers.md is not current: {run.stdout.strip()} {run.stderr.strip()}")
    stale = []
    for path, text in outputs().items():
        current = open(path).read() if os.path.exists(path) else None
        if current != text:
            stale.append(os.path.relpath(path, REPO))
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as fh:
                    fh.write(text)
    if check and stale:
        sys.exit("stale figures, rerun draw_figures.py: " + ", ".join(stale))
    print(("figures are current" if check else f"wrote {len(stale)} of {len(outputs())} files") + ".")


if __name__ == "__main__":
    main()
