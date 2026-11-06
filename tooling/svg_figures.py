"""Shared vocabulary for project figure generators that write inline SVG fragments.

A generator reads tracked data, asserts the values its page states, and writes HTML fragments that pages
include with `<!-- include: fragments/<name>.html -->`. These helpers keep the markup consistent:
numbered figures with a labelled scroll region and caption, slide faces without ids, and standalone files
usable as `<img>` (for example a slide shown as an image). A local SVG used as a site-map thumbnail is
inlined by the build, so it may also use these literal colours.

Colours are literal hex values on purpose. Page CSS variables can be redefined by a surrounding card
(an `--accent` override recolours every figure inside it), and an SVG loaded through `<img>` cannot read
page variables at all.

    import sys; sys.path.insert(0, ".docs-kit/tooling")
    from svg_figures import figure, svg_open, text
"""
from __future__ import annotations

import html
import math
import re

INK, SUB, DIM, LINE, PANEL, BG = "#e6edf3", "#a9b4c2", "#7d8896", "#2f3b4a", "#121a24", "#0d1117"
ACCENT, WARM, VIOLET, BLUE, ALERT = "#39d2c0", "#ffa657", "#bc8cff", "#79c0ff", "#ff7b72"
SANS, MONO = "'IBM Plex Sans',system-ui,sans-serif", "'IBM Plex Mono',ui-monospace,monospace"


def num(value, digits=None):
    """A number as printed in figures, with a typographic minus."""
    out = f"{value:.{digits}f}" if digits is not None else f"{value:g}"
    return out.replace("-", "−")


def text(x, y, content, size=15, fill=INK, anchor="start", weight=400, family=SANS, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{family}"{extra}>{html.escape(content)}</text>')


def arrow(x1, y1, x2, y2, color, width=3, dash=None, head=11):
    """A straight arrow with a filled head drawn as paths (no marker ids to collide)."""
    angle = math.atan2(y2 - y1, x2 - x1)
    head = min(head, math.hypot(x2 - x1, y2 - y1) * .6)
    bx, by = x2 - head * math.cos(angle), y2 - head * math.sin(angle)
    left = (bx + head * .45 * math.sin(angle), by - head * .45 * math.cos(angle))
    right = (bx - head * .45 * math.sin(angle), by + head * .45 * math.cos(angle))
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1:.1f} {y1:.1f}L{bx:.1f} {by:.1f}" stroke="{color}" stroke-width="{width}" fill="none"{dash_attr}/>'
            f'<path d="M{x2:.1f} {y2:.1f}L{left[0]:.1f} {left[1]:.1f}L{right[0]:.1f} {right[1]:.1f}Z" fill="{color}"/>')


def panel(x, y, w, h, stroke=LINE, dashed=False, fill=PANEL, radius=14):
    dash = ' stroke-dasharray="7 6"' if dashed else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radius}" fill="{fill}" stroke="{stroke}"{dash}/>'


def svg_open(width, height, title, desc):
    """Opening tags with a title and description; `{id}` is filled in by `figure()` or `slide_svg()`."""
    return [f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="{{id}}-title {{id}}-desc" class="network-figure">',
            f'<title id="{{id}}-title">{html.escape(title)}</title>',
            f'<desc id="{{id}}-desc">{html.escape(desc)}</desc>']


def figure(fid, number, svg, caption):
    """A numbered figure: the SVG inside a labelled, keyboard-scrollable region, then its caption.

    The caption is trusted HTML (it may contain links). The title is unescaped before it is escaped again
    for the region label, so an apostrophe is announced once, not as `&#x27;`.
    """
    svg = svg.replace("{id}", fid)
    title = svg[svg.index("<title"): svg.index("</title>")].split(">", 1)[1]
    return (f'<figure class="network-plate" id="{fid}">\n'
            f'<div class="figure-scroll" role="region" aria-label="{html.escape(html.unescape(title), quote=True)}" '
            f'tabindex="0" data-reader-horizontal>\n{svg}\n</div>\n<figcaption><b>Figure {number}.</b> {caption}</figcaption>\n</figure>\n')


def slide_svg(svg):
    """Slide faces carry no ids: drop title/desc and use the description as the aria-label."""
    found = re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S) or re.search(r"<title[^>]*>(.*?)</title>", svg, re.S)
    if not found:
        raise ValueError("slide_svg needs a <desc> or <title> to label the slide")
    label = html.escape(html.unescape(found[1]), quote=True)
    svg = re.sub(r"<title[^>]*>.*?</title>\n?|<desc[^>]*>.*?</desc>\n?", "", svg, flags=re.S)
    return re.sub(r'aria-labelledby="[^"]*"', f'aria-label="{label}"', svg, count=1)


def standalone(svg):
    """A file usable as `<img>`: explicit namespace, and any `var(--x, #hex)` replaced by its fallback."""
    svg = re.sub(r"var\(--[a-z0-9-]+,\s*(#[0-9a-fA-F]{3,8})\)", r"\1", slide_svg(svg) if "{id}" in svg else svg)
    opening = re.search(r"<svg\b[^>]*>", svg)
    if opening and "xmlns=" not in opening[0]:
        svg = svg[:opening.start()] + opening[0].replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1) + svg[opening.end():]
    return svg.rstrip("\n") + "\n"


def generated_header(script, sources):
    return f"<!-- Generated by {script} from {', '.join(sources)}; do not edit. -->\n"
