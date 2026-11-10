#!/usr/bin/env python3
"""Render docs/topics/ into .build/docs/html/ (the build output — never hand-edit).

    python .docs-kit/docsite.py build --project . [--check] [--page <slug>]

Sources: docs/topics/*/index.md (TOML frontmatter between +++ fences, markdown
body with raw-HTML passthrough and <!-- include: … --> directives), shared
components in docs/site/components/, vendored assets in docs/site/assets/.
Site config: docs/site/site.toml.

Exit codes: 0 built / clean · 1 config or content error · 2 --check found
generated site stale against a fresh render.

Runs on Python 3.12 with the pinned .docs-kit/requirements.txt dependencies.
No application runtime is needed.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import os
import html
import re
import sys
import subprocess
import tomllib
from pathlib import Path

try:
    import mistune
except ImportError:  # pragma: no cover
    sys.exit("build.py needs Mistune: python -m pip install -r .docs-kit/requirements.txt")

try:
    from pygments import highlight as _pyg_highlight
    from pygments.formatters import HtmlFormatter as _PygFormatter
    from pygments.lexers import get_lexer_by_name as _pyg_lexer
except ImportError:  # pragma: no cover
    _pyg_highlight = None

from site_paths import DOCS, REPO, SITE as SRC, TOPICS as PAGES, HTML as OUT, OUTPUT_ROOT, KIT_SITE, topic_pages
from site_bundle import SiteBundle, validate_resources

COMPONENTS = KIT_SITE / "components"
KATEX_SRC = KIT_SITE / "assets" / "vendor" / "katex"

FRONTMATTER_KEYS = {"title", "slug", "brand", "brand_sub", "body_class", "math", "components", "page_css", "toc", "raw", "ongoing", "reader",
                    "description", "thumbnail", "page_only"}
# A [[nav]] table accepts only these keys. TOML assigns every key written after a table header to that
# table, so a top-level setting placed below the first [[nav]] silently becomes part of a nav entry.
NAV_KEYS = {"label", "file", "group", "short", "hidden"}
INCLUDE_DEPTH = 8
KNOWN_COMPONENTS = ("toc", "nav", "tabs", "diagram", "code", "filelinks",
                    "lightbox", "plot-toggles", "carousel", "panel-switcher",
                    "fold-controls", "chapter-reader", "slide-face", "page-redirect")  # emission order
# Vendored font folders under assets/vendor/, published to assets/fonts/<family>/.
FONT_FAMILIES = ("atkinson-hyperlegible", "saira-condensed", "ibm-plex-sans", "ibm-plex-mono")
# NOTE: "plot-toggles" must precede "carousel" — it wraps each inline SVG in
# a .fig-unit that the carousel then treats as one slide.

_SVG_IMG_RE = re.compile(r'<img([^>]*?)\ssrc="\.\./figures/([^"]+\.svg)"([^>]*?)/?>')

# Typed collapsible folds (the spine+fold layout prototype):
#   <!-- fold: math The route-level problem -->
#   ...markdown (blank-line separated from the markers)...
#   <!-- /fold -->
# Types drive the color + the reader-mode bar (fold-controls.js).
FOLD_TYPES = ("math", "experiment", "code", "dead-end")
# The markers match to the end of their own line only. Matching further would
# swallow the blank line after a closing marker, and Markdown would then read
# the next paragraph as part of the HTML block and show it as raw text.
_FOLD_OPEN_RE = re.compile(
    r"^<!--\s*fold:\s*(" + "|".join(FOLD_TYPES) + r")\s+(.+?)\s*-->[ \t]*$", re.M)
_FOLD_CLOSE_RE = re.compile(r"^<!--\s*/fold\s*-->[ \t]*$", re.M)


def folds_to_html(chunk: str, name: str) -> str:
    n_open = len(_FOLD_OPEN_RE.findall(chunk))
    n_close = len(_FOLD_CLOSE_RE.findall(chunk))
    if n_open != n_close:
        err(f"{name}: unbalanced fold markers ({n_open} open, {n_close} close)")

    def open_sub(m: re.Match) -> str:
        kind, title = m.group(1), m.group(2)
        return (f'<details class="fold fold-{kind}" data-fold="{kind}">\n'
                f'<summary><span class="fold-tag">{kind}</span> '
                f"{html.escape(title)}</summary>\n")

    chunk = _FOLD_OPEN_RE.sub(open_sub, chunk)
    # The newline after the closing tag ends the HTML block, so the next line is
    # read as Markdown even when the author left no blank line after the marker.
    return _FOLD_CLOSE_RE.sub("</details>\n", chunk)


# Slide faces: one 16:9 summary slide at the top of a chapter.
#   <!-- slide -->
#   <p class="slide-eyebrow">…</p><p class="slide-title">…</p> … <p class="slide-scope">…</p>
#   <!-- /slide -->
# The title is deliberately not an h2/h3: the reader names chapters by their
# first heading, and that heading opens the full chapter below the slide.
_SLIDE_OPEN_RE = re.compile(r"^[ \t]*<!--\s*slide\s*-->[ \t]*$", re.M)
_SLIDE_CLOSE_RE = re.compile(r"^[ \t]*<!--\s*/slide\s*-->[ \t]*$", re.M)


def slides_to_html(chunk: str, name: str) -> str:
    opens = [m.start() for m in _SLIDE_OPEN_RE.finditer(chunk)]
    closes = [m.start() for m in _SLIDE_CLOSE_RE.finditer(chunk)]
    if len(opens) != len(closes) or any(c < o for o, c in zip(opens, closes)) or any(
            n < c for c, n in zip(closes, opens[1:])):
        err(f"{name}: unbalanced or nested slide markers ({len(opens)} open, {len(closes)} close)")
        return chunk
    # The outer element is the size container; the canvas inside carries the 16:9 layout.
    chunk = _SLIDE_OPEN_RE.sub('<div class="slide-face" data-slide-face><div class="slide-canvas">\n', chunk)
    return _SLIDE_CLOSE_RE.sub("</div></div>\n", chunk)


def inline_svg_figures(content: str, name: str, *, namespace_ids: bool = False) -> str:
    """Replace <img src="../figures/*.svg"> with the SVG inlined, so page
    scripts (plot-toggles, lightbox) can reach the artist groups inside.
    The root tag loses its fixed width/height (responsive via base.css)
    and carries the img alt as aria-label."""

    occurrence = 0

    def sub(m: re.Match) -> str:
        nonlocal occurrence
        occurrence += 1
        fname = m.group(2)
        path = local_resource(DOCS / "figures" / fname)
        if not path.is_file():
            err(f"{name}: inlined SVG figure missing: {fname}")
            return m.group(0)
        svg = path.read_text()
        svg = svg[svg.find("<svg"):]
        if namespace_ids:
            # Inline galleries share one DOM: Matplotlib's generic IDs must not
            # bind clip paths or glyph references to a different figure. Keep
            # the tg-<group>-- convention consumed by plot-toggles.js.
            prefix = f"figure-{Path(fname).stem}-{occurrence}"
            identifiers = re.findall(r'\bid="([^"]+)"', svg)
            remap = {
                key: (key.split("--", 1)[0] + "--" + prefix + "-" + key.split("--", 1)[1]
                      if key.startswith("tg-") and "--" in key
                      else key if key.startswith(Path(fname).stem + "-")
                      else prefix + "-" + key)
                for key in identifiers
            }
            svg = re.sub(r'\bid="([^"]+)"', lambda match: 'id="' + remap[match[1]] + '"', svg)
            svg = re.sub(r'url\(#([^)]*)\)', lambda match: 'url(#' + remap.get(match[1], match[1]) + ')', svg)
            svg = re.sub(r'((?:xlink:)?href=")#([^"]+)"', lambda match: match[1] + '#' + remap.get(match[2], match[2]) + '"', svg)
            # Existing Matplotlib SVGs may contain spaces after path commands.
            # Keep the imported reader markup clean without changing source figures.
            svg = re.sub(r'[ \t]+$', '', svg, flags=re.MULTILINE)
        alt_m = re.search(r'alt="([^"]*)"', m.group(1) + " " + m.group(3))
        alt = alt_m.group(1) if alt_m else fname
        root_end = svg.find(">")
        root = svg[:root_end]
        root = re.sub(r'\s(?:width|height)="[^"]*"', "", root)
        if "data-decorative" in m.group(1) + " " + m.group(3):
            root += ' class="inline-fig" aria-hidden="true" focusable="false"'  # e.g. a site-map card thumbnail
        else:
            root += f' class="inline-fig" role="img" aria-label="{alt}"'
        return root + svg[root_end:]

    return _SVG_IMG_RE.sub(sub, content)
# NOTE: "code" must precede "filelinks" — the source chips code.js injects
# are rewritten to VS Code / GitHub URLs by the filelinks pass.

INCLUDE_RE = re.compile(r"<!--\s*include:\s*(\S+)\s*-->")
PAGE_END = "<!-- page-end -->"  # working-notes tail below this never renders
# Page tabs: top-level <!-- tab: Label --> markers split the page part into
# panels (content before the first marker stays above the bar as the shared
# header). Distinct hook classes from the mode-views tabs on purpose.
TAB_RE = re.compile(r"^<!--\s*tab:\s*(.+?)\s*-->\s*$", re.M)

# Registry markers render as human-readable callout cards (the label chip
# comes from CSS ::before); the raw **INVARIANT:**/**DON'T-REDO:** tags stay
# in the md source for `lint --registry`. A marker paragraph = the token at
# line start through the next blank line.
_CALLOUT_RES = (
    (re.compile(r"(?m)^\*\*INVARIANT:\*\*\s*((?:[^\n]+\n?)+?)(?=\n\s*\n|\Z)"), "inv"),
    (re.compile(r"(?m)^\*\*DON'T-REDO:\*\*\s*((?:[^\n]+\n?)+?)(?=\n\s*\n|\Z)"), "redo"),
)


def markers_to_callouts(body: str) -> str:
    for rx, kind in _CALLOUT_RES:
        body = rx.sub(
            lambda m, k=kind: f'<div class="callout {k}">\n\n{m.group(1).rstrip()}\n\n</div>\n',
            body,
        )
    return body
HEADING_ID_RE = re.compile(r"\s*\{#([A-Za-z0-9][A-Za-z0-9_-]*)\}\s*$")

_errors: list[str] = []


def err(msg: str) -> None:
    _errors.append(msg)


def slugify(text: str) -> str:
    """GitHub-style (kept in sync with docs/lint.py): strip punctuation, then
    every space becomes a hyphen — consecutive spaces stay as -- runs."""
    text = re.sub(r"<[^>]+>", "", html.unescape(text).lower())
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text.strip())


class DocsRenderer(mistune.HTMLRenderer):
    """HTML renderer with explicit-{#id} headings, source-anchored code
    fences and explicit display/inline math delimiters."""

    def __init__(self, math_enabled: bool = False) -> None:
        super().__init__(escape=False)
        self.heading_ids: list[str] = []
        self.math_enabled = math_enabled

    def heading(self, text: str, level: int, **attrs) -> str:
        m = HEADING_ID_RE.search(text)
        if m:
            hid, text = m.group(1), text[: m.start()]
        else:
            hid = slugify(text)
        self.heading_ids.append(hid)
        return f'<h{level} id="{hid}">{text}</h{level}>\n'

    def block_code(self, code: str, info: str | None = None) -> str:
        lang, source = "", ""
        if info:
            parts = info.strip().split()
            if parts and "=" not in parts[0]:
                lang = parts[0]
            for p in parts:
                if p.startswith("source="):
                    source = p[len("source="):]

        body, highlighted = html.escape(code), False
        if lang and _pyg_highlight is not None:
            try:
                lexer = _pyg_lexer(lang)
            except Exception:
                lexer = None
            if lexer is not None:
                body = _pyg_highlight(code, lexer, _PygFormatter(nowrap=True)).rstrip("\n")
                # per-line spans: the CSS counter gutter hangs off .cl::before,
                # which textContent (and so the copy button) never sees
                body = "".join(f'<span class="cl">{ln}\n</span>' for ln in body.split("\n"))
                highlighted = True

        code_attrs = f' class="language-{html.escape(lang)}"' if lang else ""
        if highlighted:
            start = 1
            m = re.search(r"#L(\d+)-L\d+$", source) if source else None
            if m:
                start = int(m.group(1))  # gutter shows REAL source line numbers
            code_attrs += f' style="counter-reset: ln {start - 1}"'

        wrap_attrs = ""
        if lang:
            wrap_attrs += f' data-lang="{html.escape(lang)}"'
        if source:
            wrap_attrs += f' data-source="{html.escape(source)}"'
        if wrap_attrs:
            return f'<div class="codeblock"{wrap_attrs}><pre><code{code_attrs}>{body}</code></pre></div>\n'
        return f"<pre><code>{body}</code></pre>\n"

    def block_math(self, text: str) -> str:
        # Keep the $$ fences: KaTeX auto-render finds them in the text node.
        return f'<div class="math">$${html.escape(text)}$$</div>\n'

    def inline_math(self, text: str) -> str:
        if not self.math_enabled:
            return f"${html.escape(text)}$"
        # Markdown has already identified this as math. Explicit delimiters
        # avoid interpreting arbitrary dollar signs in raw HTML as formulas.
        return f'<span class="math-inline">\\({html.escape(text)}\\)</span>'


def validate_frontmatter(meta: dict, name: str) -> None:
    unknown = set(meta) - FRONTMATTER_KEYS
    if unknown:
        err(f"{name}: unknown frontmatter keys: {sorted(unknown)}")
    if "title" not in meta:
        err(f"{name}: frontmatter needs title")
    if "toc" not in meta:
        err(f"{name}: frontmatter needs toc (the sidebar is generated)")
    for key in ("description", "thumbnail"):
        if key in meta and (not isinstance(meta[key], str) or not meta[key].strip()):
            err(f"{name}: {key} must be a non-empty string")
    if isinstance(meta.get("thumbnail"), str) and re.match(r"[a-z][a-z0-9+.-]*:|//", meta["thumbnail"], re.I):
        err(f"{name}: thumbnail must be a local, tracked image (no remote media)")
    if "slug" in meta and (not isinstance(meta["slug"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", meta["slug"])):
        err(f"{name}: slug must be a lowercase filename stem without directories")
    if "body_class" in meta and (not isinstance(meta["body_class"], str)
            or not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_-]*(?: [a-zA-Z_][a-zA-Z0-9_-]*)*", meta["body_class"])):
        err(f"{name}: body_class must contain plain space-separated CSS class names")


def parse_frontmatter(raw: str, name: str) -> tuple[dict, str]:
    if not raw.startswith("+++\n"):
        err(f"{name}: missing +++ frontmatter fence at top")
        return {}, raw
    end = raw.find("\n+++\n", 4)
    if end < 0:
        err(f"{name}: unterminated +++ frontmatter")
        return {}, raw
    try:
        meta = tomllib.loads(raw[4:end])
    except tomllib.TOMLDecodeError as e:
        err(f"{name}: frontmatter TOML error: {e}")
        return {}, raw[end + 5:]
    validate_frontmatter(meta, name)
    return meta, raw[end + 5:]


SITE_MAP_MARKER = "<!-- site-map -->"
_IMAGE_RE = re.compile(r'<img[^>]+src="([^"]+\.(?:svg|png|jpe?g|webp|gif))"|!\[[^\]]*\]\(([^)\s]+\.(?:svg|png|jpe?g|webp|gif))\)', re.I)


_BRAND_MARKS: dict[str, str] = {}


def brand_mark_html(site: dict) -> str:
    """The project's mark beside its name in the sidebar.

    `brand_mark` in site.toml is up to three characters or a tracked `.svg`
    file; without it the mark is the initials of the site title. Each setting
    is resolved once per build, so a bad value is reported once.
    """
    key = repr((site.get("brand_mark"), site.get("title")))
    if key not in _BRAND_MARKS:
        _BRAND_MARKS[key] = _resolve_brand_mark(site)
    return _BRAND_MARKS[key]


def _resolve_brand_mark(site: dict) -> str:
    mark = site.get("brand_mark")
    if mark is None:
        words = site.get("title", "Documentation").split()
        mark = "".join(word[0] for word in words[:2]).upper()
    elif not isinstance(mark, str) or not mark.strip():
        err("brand_mark must be up to three characters or a tracked .svg path")
        return ""
    elif mark.endswith(".svg"):
        try:
            svg = local_resource(REPO / mark).read_text()
            # Editors export an XML prolog, a doctype or a comment before the root element.
            svg = re.sub(r"^(?:\s*(?:<\?xml.*?\?>|<!DOCTYPE[^>]*>|<!--.*?-->))*\s*", "", svg, flags=re.S).strip()
        except (ValueError, OSError) as problem:
            err(f"brand_mark: {problem}")
            return ""
        if not svg.startswith("<svg"):
            err(f"brand_mark: {mark} is not an SVG file")
            return ""
        return f'<span class="brand-mark brand-mark-svg" aria-hidden="true">{svg}</span>'
    elif len(mark) > 3:
        err("brand_mark must be up to three characters or a tracked .svg path")
        return ""
    return f'<span class="brand-mark" aria-hidden="true">{html.escape(mark)}</span>'


def site_map_html(site: dict) -> str:
    """Home-page cards for every visible page, grouped as in the navigation.

    Each card takes its title and subtitle from the page frontmatter and its
    thumbnail from the first figure on the page, so the map stays current.
    """
    sources = {}
    for path in topic_pages():
        meta, body = parse_frontmatter(path.read_text(), path.relative_to(PAGES).as_posix())
        sources[meta.get("slug", path.parent.name) + ".html"] = (meta, body.split(PAGE_END, 1)[0])
    from source_pages import load_registry
    for page in load_registry(site, REPO, consumer_tracked_paths())[0]:  # problems are reported by main
        sources.setdefault(page.route, ({"description": page.description} if page.description else {}, ""))
    groups: list[tuple[str, list[str]]] = []
    for entry in site.get("nav", []):
        if entry.get("hidden") or not entry.get("group") or entry["file"] not in sources:
            continue
        meta, body = sources[entry["file"]]
        found = _IMAGE_RE.search(body)
        image = meta.get("thumbnail") or ((found.group(1) or found.group(2)) if found else None)
        thumb = (f'<span class="map-thumb"><img src="{html.escape(image)}" alt="" data-decorative loading="lazy"></span>'
                 if image else f'<span class="map-thumb map-thumb-empty" aria-hidden="true">{brand_mark_html(site)}</span>')
        card = (f'<a class="map-card" href="{entry["file"]}">{thumb}<span class="map-text">'
                f'<strong>{html.escape(entry["label"])}</strong>'
                f'<span>{html.escape(meta.get("description") or meta.get("brand_sub", ""))}</span></span></a>')
        if not groups or groups[-1][0] != entry["group"]:
            groups.append((entry["group"], []))
        groups[-1][1].append(card)
    return "\n".join(f'<section class="map-group" data-group="{html.escape(g)}"><h2>{html.escape(g.title())}</h2>'
                     f'<div class="map-grid">{"".join(cards)}</div></section>' for g, cards in groups)


def expand_includes(body: str, name: str, _stack: tuple[Path, ...] = ()) -> str:
    """Replace include markers; included fragments may include others (depth-limited, no cycles)."""
    def rep(m: re.Match) -> str:
        relative = Path(m.group(1))
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Include paths must stay inside the theme or project')
        chain = " -> ".join([*(item.name for item in _stack), m.group(1)])
        shared = KIT_SITE / relative
        if shared.is_file() and not shared.is_symlink() and shared.resolve().is_relative_to(KIT_SITE):
            p = shared
        else:
            try:
                p = local_resource(SRC / relative)
            except ValueError as error:  # missing or untracked fragment: name the include chain, not a traceback
                err(f"{name}: include not found or not tracked: {chain} ({error})")
                return ""
        if not p.is_file():
            err(f"{name}: include not found: {chain}")
            return ""
        text = p.read_text()
        if not text.strip():
            err(f"{name}: include is empty: {m.group(1)}")
        resolved = p.resolve()
        if resolved in _stack:
            err(f"{name}: include cycle: {chain}")
            return ""
        if len(_stack) >= INCLUDE_DEPTH:
            err(f"{name}: includes nest deeper than {INCLUDE_DEPTH} levels: {chain}")
            return ""
        return expand_includes(text, name, (*_stack, resolved))

    return INCLUDE_RE.sub(rep, body)


def toc_html(toc: list, name: str, id_to_panel: dict | None = None) -> str:
    lines = []
    for entry in toc:
        if not (isinstance(entry, list) and len(entry) == 2):
            err(f"{name}: toc entries are [label, href] pairs, got {entry!r}")
            continue
        label, href = entry
        sub = label.startswith("-")
        cls = "sub-link" if sub else "top"
        ptab = ""
        if id_to_panel and href.startswith("#") and href[1:] in id_to_panel:
            ptab = f' data-ptab="{id_to_panel[href[1:]]}"'
        lines.append(
            f'    <a class="{cls}" href="{href}"{ptab}>{html.escape(label[1:] if sub else label)}</a>'
        )
    return "\n".join(lines)


def katex_head() -> str:
    return '<link rel="stylesheet" href="assets/katex/katex.min.css">\n'


def katex_scripts() -> str:
    return (
        '<script defer src="assets/katex/katex.min.js"></script>\n'
        '<script defer src="assets/katex/contrib/auto-render.min.js"></script>\n'
        "<script>\n"
        'document.addEventListener("DOMContentLoaded", function(){\n'
        '  renderMathInElement(document.querySelector(".content"), {\n'
        '    delimiters: [{left: "$$", right: "$$", display: true},\n'
        '                 {left: "\\\\(", right: "\\\\)", display: false}],\n'
        '    ignoredTags: ["pre", "code", "script", "style"]\n'
        "  });\n"
        "});\n"
        "</script>\n"
    )


@lru_cache(maxsize=1)
def content_transform():
    from project_extensions import load_extension
    module = load_extension(REPO, 'content_transform')
    if module is not None and not callable(getattr(module, 'transform', None)):
        raise ValueError('content_transform must export transform')
    return module


def build_page(md_path: Path, site: dict, shell: str) -> tuple[str, str] | None:
    name = md_path.relative_to(PAGES).as_posix()
    meta, body = parse_frontmatter(md_path.read_text(), name)
    if _errors:
        return None
    module = content_transform()
    if module is not None:
        structural = {key: deepcopy(meta.get(key)) for key in ('slug', 'page_css')}
        body = module.transform(body, metadata=meta, source=md_path, root=REPO)
        if not isinstance(body, str):
            err(f'{name}: content_transform must return HTML/Markdown text')
            return None
        if any(meta.get(key) != value for key, value in structural.items()):
            err(f'{name}: content_transform must keep slug and page_css in source frontmatter')
            return None
        validate_frontmatter(meta, name)
        if _errors:
            return None
    slug = meta.get("slug", md_path.parent.name)
    body = body.split(PAGE_END, 1)[0]
    comps = list(meta.get("components", ["toc", "nav"]))
    automatic_reader = (bool(site.get("chapter_reader")) and meta.get("reader", True)
                        and "chapter-reader" not in comps and "page-redirect" not in comps and "location.replace(" not in body)
    if SITE_MAP_MARKER in body:
        body = body.replace(SITE_MAP_MARKER, site_map_html(site))

    def render_chunk(chunk: str) -> str:
        chunk = expand_includes(chunk, name)
        if meta.get("raw"):
            # Whole-body HTML passthrough (the escape hatch as a mode):
            # converted pages whose content is still hand-built HTML skip
            # markdown entirely, so blank lines / indentation inside big
            # markup can't re-enter the markdown parser.
            return slides_to_html(chunk, name)
        renderer = DocsRenderer(math_enabled=bool(meta.get("math")))
        md = mistune.create_markdown(renderer=renderer, plugins=["table", "math"])
        # Slide markers are matched after rendering: Markdown passes standalone
        # comments through unchanged, while code blocks escape example markers.
        rendered = slides_to_html(md(folds_to_html(markers_to_callouts(chunk), name)), name)
        if "reference-page" in str(meta.get("body_class", "")).split():
            # Reference pages share the source pages' narrow-screen table regions.
            from source_pages import wrap_tables
            rendered = wrap_tables(rendered)
        return rendered

    id_to_panel: dict[str, int] = {}
    parts = TAB_RE.split(body)
    if automatic_reader:
        from chapter_layout import reader_page

        chunks = [(None, render_chunk(parts[0]))]
        if len(parts) > 1:
            chunks += [(label, render_chunk(chunk))
                       for label, chunk in zip(parts[1::2], parts[2::2])]
        try:
            content, meta["toc"] = reader_page(
                chunks, meta.get("toc", []), meta["title"],
                (COMPONENTS / "chapter-reader.html").read_text())
        except ValueError as error:
            err(f"{name}: chapter layout: {error}")
            return None
        # Old page-wide tabs become chapter groups. Local figure tabs keep
        # their original markup, handlers and keyboard ownership.
        comps = [c for c in comps if c not in {"toc", "tabs"}]
        comps.append("chapter-reader")
    elif len(parts) == 1:
        content = render_chunk(body)
    else:
        pre = render_chunk(parts[0])
        labels = parts[1::2]
        panels_html = []
        for i, chunk in enumerate(parts[2::2]):
            rendered = render_chunk(chunk)
            for pid in re.findall(r'id="([^"]+)"', rendered):
                id_to_panel[pid] = i
            hidden = "" if i == 0 else " hidden"
            panels_html.append(
                f'<div class="ptab-panel" data-ptab="{i}"{hidden}>\n{rendered}\n</div>'
            )
        bar = "\n".join(
            f'  <button class="mode-tab ptab{" on" if i == 0 else ""}" data-ptab="{i}">'
            f"{html.escape(lbl)}</button>"
            for i, lbl in enumerate(labels)
        )
        content = (
            pre
            + f'\n<div class="mode-tabs ptabs">\n{bar}\n</div>\n\n'
            + "\n\n".join(panels_html)
        )

    return finish_page(meta, slug, name, content, comps, site, shell, id_to_panel)


def nested_nav_html(nav_entries: list, fname: str, toc: str) -> str:
    """Site tree for `nested_nav = true`: groups fold, the current page's group
    is open and the current page's own sections sit directly under its entry.
    Native <details> keep it usable without JavaScript."""
    groups: list[tuple[str | None, list[dict]]] = []
    for entry in nav_entries:
        if entry.get("hidden", False) or entry["file"] == "index.html":
            continue
        group = entry.get("group")
        if not groups or groups[-1][0] != group:
            groups.append((group, []))
        groups[-1][1].append(entry)
    lines = []
    # Open the current page's group; where no group holds it (the home page), open the first.
    open_group = next((group for group, entries in groups if any(e["file"] == fname for e in entries)),
                      next((group for group, _ in groups if group is not None), None))
    for group, entries in groups:
        links = []
        for entry in entries:
            current = entry["file"] == fname
            attrs = ' class="xpage current" aria-current="page"' if current else ' class="xpage"'
            if group:
                attrs += f' data-group="{html.escape(group)}"'
            short = entry.get("short", entry["label"])
            if short != entry["label"]:
                attrs += f' title="{html.escape(entry["label"], quote=True)}"'
            links.append(f'    <a{attrs} href="{entry["file"]}">{html.escape(short)}</a>')
            if current and toc.strip():
                links.append(f'    <div class="nav-sections" aria-label="On this page">\n{toc}\n    </div>')
        if group is None:
            lines.extend(links)
            continue
        is_open = group == open_group
        lines.append(f'    <details class="nav-fold" data-group="{html.escape(group)}"{" open data-nav-default" if is_open else ""}>'
                     f'<summary class="nav-group" data-group="{html.escape(group)}">'
                     f'<span class="nav-group-label">{html.escape(group)}</span></summary>')
        lines.extend(links)
        lines.append('    </details>')
    return "\n".join(lines)


def repository_tree(source_pages: list) -> list:
    """Registered records for the sidebar's repository section, in declared order."""
    from source_pages import first_heading
    from source_tree import TreeFile

    return [TreeFile(page.source, page.route,
                     page.title or first_heading(local_resource(REPO / page.source).read_text()) or page.source,
                     page.description, page.pinned)
            for page in source_pages]


def build_source_page(page, routes: dict[str, str], site: dict, shell: str) -> tuple[str, str] | None:
    """Render one registered Markdown file as a whole-file page.

    The source keeps its own folder as link origin; no topic-page markers
    (includes, folds, registry callouts or the notes tail) are interpreted, so
    examples of those markers inside the record stay literal.
    """
    from source_pages import exists_in, first_heading, origin_banner, rewrite_links, table_of_contents, wrap_tables
    from site_paths import resolve_legacy_path

    name = page.source
    text = local_resource(REPO / page.source).read_text()
    title = page.title or first_heading(text)
    if not title:
        err(f"{name}: a source page needs a level-one heading or a registered title")
        return None
    meta = {"title": title, "slug": page.slug, "toc": [], "math": page.math, "body_class": "source-page reference-page",
            "brand": site.get("title", "Documentation"), "page_css": ["build-sheet.css"]}
    renderer = DocsRenderer(math_enabled=page.math)
    content = mistune.create_markdown(renderer=renderer, plugins=["table", "math"])(text)
    content, problems = rewrite_links(wrap_tables(content), page, routes, REPO, exists_in(REPO, resolve_legacy_path))
    for problem in problems:
        err(problem)
    banner = origin_banner(page, site.get("gh_repo", ""), site.get("_edit_ref", site.get("gh_ref", "main")))
    content = banner + content
    comps = ["toc", "nav", "code", "filelinks"]
    if page.reader and site.get("chapter_reader"):
        from chapter_layout import reader_page
        from source_pages import merge_short_introduction
        content = merge_short_introduction(content)
        try:
            content, meta["toc"] = reader_page([(None, content)], [], title,
                                               (COMPONENTS / "chapter-reader.html").read_text())
        except ValueError as error:
            err(f"{name}: chapter layout: {error}")
            return None
        comps = ["nav", "code", "filelinks", "chapter-reader"]
    else:
        # The repository tree marks this page as current, so its sidebar keeps the
        # same site tree as every other page. Only nested navigation lists the
        # page's sections, under its own visible entry.
        listed = any(n.get("file") == page.route and not n.get("hidden", False) for n in site.get("nav", []))
        meta["toc"] = table_of_contents(content) if site.get("nested_nav") and listed else []
    return finish_page(meta, page.slug, name, content, comps, site, shell, {})


def finish_page(meta: dict, slug: str, name: str, content: str, comps: list, site: dict,
                shell: str, id_to_panel: dict) -> tuple[str, str]:
    """Inline figures, select components and fill the shared shell."""
    content = inline_svg_figures(content, name, namespace_ids="chapter-reader" in comps)

    if meta.get("ongoing"):
        content = (
            '<div class="ongoing-banner">ongoing — this experiment is live; '
            "numbers may still move</div>\n" + content
        )

    # Typed folds need this component for both their styling and reader bar.
    # Inspect rendered content so folds from included fragments count too.
    if '<details class="fold ' in content and "fold-controls" not in comps:
        comps.append("fold-controls")
    if "data-slide-face" in content and "slide-face" not in comps:
        comps.append("slide-face")
    for c in comps:
        if c not in KNOWN_COMPONENTS:
            err(f"{name}: unknown component {c!r} (known: {KNOWN_COMPONENTS})")

    nav_entries = site.get("nav", [])
    fname = f"{slug}.html"
    tree = site.get("_repository_tree", [])
    # Registered records are listed by the repository tree; pages need a nav entry.
    if fname not in {n["file"] for n in nav_entries} and fname not in {f.route for f in tree}:
        err(f"{name}: {fname} missing from site.toml [[nav]] registry")
    crossnav_lines, last_group = [], None
    # One site tree on every page; the current page stays in place so the
    # chapter reader can nest its chapters under it.
    for n_entry in nav_entries:
        current = n_entry["file"] == fname
        if n_entry.get("hidden", False) or n_entry["file"] == "index.html":
            continue  # the sidebar brand already links the home page
        group = n_entry.get("group")
        if group != last_group:
            # Each group is one section: its label, then its pages.
            if last_group:
                crossnav_lines.append('    </div>')
            if group:
                crossnav_lines.append(f'    <div class="nav-section" data-group="{html.escape(group)}">')
                crossnav_lines.append(f'    <span class="nav-group" data-group="{html.escape(group)}">{html.escape(group)}</span>')
            last_group = group
        attrs = ' class="xpage current" aria-current="page"' if current else ' class="xpage"'
        if group:
            attrs += f' data-group="{html.escape(group)}"'
        short = n_entry.get("short", n_entry["label"])
        if short != n_entry["label"]:
            attrs += f' title="{html.escape(n_entry["label"], quote=True)}"'
        crossnav_lines.append(f'    <a{attrs} href="{n_entry["file"]}">{html.escape(short)}</a>')
    if last_group:
        crossnav_lines.append('    </div>')
    crossnav = "\n".join(crossnav_lines)
    toc = toc_html(meta.get("toc", []), name, id_to_panel)
    if site.get("nested_nav") and "chapter-reader" not in comps:
        crossnav, toc = nested_nav_html(nav_entries, fname, toc), ""
    if tree:
        from source_tree import tree_html
        listed = any(entry.get("file") == fname and not entry.get("hidden") for entry in nav_entries)
        crossnav += "\n" + tree_html(tree, fname, listed=listed)

    head_extra = ""
    if meta.get("math"):
        if not (KATEX_SRC / "katex.min.js").is_file():
            err(f"{name}: math=true but vendored KaTeX missing at {KATEX_SRC}")
        head_extra += katex_head()
    if "chapter-reader" in comps:
        head_extra += '<link rel="stylesheet" href="assets/chapter-reader.css">\n'
    if "width-lessons" in comps:
        head_extra += '<link rel="stylesheet" href="assets/width-lessons.css">\n'
    if "panel-switcher" in comps:
        head_extra += '<link rel="stylesheet" href="assets/panel-switcher.css">\n'
    if "slide-face" in comps:
        head_extra += '<link rel="stylesheet" href="assets/slide-face.css">\n'
    for css in meta.get("page_css", []):
        if not page_stylesheet(css).is_file():
            err(f"{name}: page_css not found: {css}")
        head_extra += f'<link rel="stylesheet" href="assets/{Path(css).name}">\n'

    scripts = "".join(
        f'<script defer src="assets/{c}.js"></script>\n' for c in KNOWN_COMPONENTS if c in comps
    )
    if meta.get("math"):
        scripts += katex_scripts()

    body_class = ' class="' + html.escape(meta['body_class'], quote=True) + '"' if meta.get('body_class') else ''
    page = shell.replace("<body>", '<body' + body_class + ' data-site-home-label="' + html.escape(site.get("home_label", site.get("title", "Documentation")), quote=True) + '">')
    for k, v in {
        "{{TITLE}}": html.escape(meta.get("title", "")),
        "{{BRAND}}": brand_mark_html(site) + '<span class="brand-name">' + html.escape(meta.get("brand", slug)) + "</span>",
        "{{BRAND_SUB}}": html.escape(meta.get("brand_sub", "")),
        "{{TOC}}": toc,
        "{{CROSSNAV}}": crossnav,
        "{{HEAD_EXTRA}}": head_extra,
        "{{CONTENT}}": content.rstrip() + "\n",
        "{{SCRIPTS}}": scripts,
    }.items():
        page = page.replace(k, v)
    return fname, page


def local_resource(path: Path) -> Path:
    resolved = path.resolve()
    if path.is_symlink() or not resolved.is_relative_to(REPO):
        raise ValueError(f"Project resource escapes its root: {path}")
    if resolved not in consumer_tracked_paths():
        raise ValueError(f"Local site input must be tracked by the consumer Git repository: {path}")
    return resolved


@lru_cache(maxsize=1)
def consumer_tracked_paths() -> frozenset[Path]:
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=REPO, capture_output=True, check=True)
    return frozenset(REPO / path for path in result.stdout.decode().split('\0') if path)


def page_stylesheet(css: str) -> Path:
    if css in {"build-sheet.css", "home.css"}:
        return KIT_SITE / "assets" / css
    return local_resource(PAGES / css)


def component_script(name: str) -> Path:
    shared = COMPONENTS / f"{name}.js"
    return shared if shared.is_file() else local_resource(SRC / "components" / f"{name}.js")


def gather_assets(site: dict, *, origins: dict[str, str] | None = None) -> dict[str, bytes]:
    """Everything that lands under .build/docs/html/assets/, path → content.

    ``origins`` receives the repository path of each asset read from the project.
    """
    assets: dict[str, bytes] = {}
    assets["assets/base.css"] = (COMPONENTS / "base.css").read_bytes()
    assets["assets/chapter-reader.css"] = (COMPONENTS / "chapter-reader.css").read_bytes()
    assets["assets/panel-switcher.css"] = (COMPONENTS / "panel-switcher.css").read_bytes()
    assets["assets/slide-face.css"] = (COMPONENTS / "slide-face.css").read_bytes()
    for c in KNOWN_COMPONENTS:
        script = component_script(c)
        text = script.read_text()
        if origins is not None and script.is_relative_to(REPO):
            origins[f"html/assets/{c}.js"] = script.relative_to(REPO).as_posix()
        if c == "filelinks":
            text = text.replace("{{GH_REPO}}", site.get("gh_repo", "")).replace("{{GH_REF}}", site.get("gh_ref", "main"))
        assets[f"assets/{c}.js"] = text.encode()
    for family in FONT_FAMILIES:
        for p in sorted((KIT_SITE / "assets" / "vendor" / family).glob("*")):
            if p.is_file():
                assets[f"assets/fonts/{family}/{p.name}"] = p.read_bytes()
    if KATEX_SRC.is_dir():
        for p in sorted(KATEX_SRC.rglob("*")):
            if p.is_file():
                assets[f"assets/katex/{p.relative_to(KATEX_SRC).as_posix()}"] = p.read_bytes()
    # A built site contains the kit's styles and scripts, so its license notice goes with them.
    assets["assets/documentation-kit/LICENSE"] = (KIT_SITE.parent / "LICENSE").read_bytes()
    extra = site.get('extra_assets', {})
    if not isinstance(extra, dict):
        raise ValueError('extra_assets must map asset names to project files')
    for name, source in extra.items():
        if (not isinstance(name, str) or not name or Path(name).is_absolute()
                or '\\' in name or Path(name).as_posix() != name
                or '..' in Path(name).parts or not isinstance(source, str)
                or Path(source).is_absolute() or '..' in Path(source).parts):
            raise ValueError('extra_assets must use contained relative paths')
        destination = 'assets/' + name
        if destination in assets:
            raise ValueError('Project asset would overwrite a shared asset: ' + name)
        assets[destination] = local_resource(REPO / source).read_bytes()
        if origins is not None:
            origins["html/" + destination] = source
    return assets


def gather_page_css(pages_meta: list[dict], *, origins: dict[str, str] | None = None) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for meta in pages_meta:
        for css in meta.get("page_css", []):
            p = page_stylesheet(css)
            if p.is_file():
                name, data = f"assets/{p.name}", p.read_bytes()
                if name in out and out[name] != data:
                    raise ValueError(f"Stylesheet output collision: {name}")
                out[name] = data
                if origins is not None and p.is_relative_to(REPO):
                    origins["html/" + name] = p.relative_to(REPO).as_posix()
    return out


ASSET_LINK = re.compile(r'\b(href|src)="(assets/[^"?#]+)"')


def version_asset_links(outputs: dict[str, bytes]) -> None:
    """Add a content hash to each page's shared asset URLs.

    A browser that cached an older stylesheet or script would otherwise pair
    it with newer markup after a rebuild. The query changes only when the
    asset's bytes change, so unchanged assets stay cached.
    """
    for name in [n for n in outputs if n.startswith("html/") and n.endswith(".html")]:
        def stamp(match):
            data = outputs.get("html/" + match[2])
            if data is None:
                return match[0]
            return f'{match[1]}="{match[2]}?v={hashlib.sha256(data).hexdigest()[:10]}"'
        outputs[name] = ASSET_LINK.sub(stamp, outputs[name].decode()).encode()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify the generated site is fresh; write nothing")
    ap.add_argument("--page", help="only build this page slug (assets still sync)")
    args = ap.parse_args()

    site = tomllib.loads(local_resource(SRC / "site.toml").read_text())
    if not isinstance(site.get("nav", []), list):
        ap.error("site.toml: nav must be a list of [[nav]] tables")
    for entry in site.get("nav", []):
        if not isinstance(entry, dict):
            ap.error("site.toml: every nav entry must be a [[nav]] table")
        unknown = sorted(set(entry) - NAV_KEYS)
        if unknown or not {"label", "file"} <= set(entry):
            ap.error(f"site.toml [[nav]] entry {entry.get('file', '?')}: unknown keys {unknown} or missing label/file. "
                     "Top-level settings must appear above the first [[nav]] table.")
        types = {"label": str, "file": str, "group": str, "short": str, "hidden": bool}
        wrong = sorted(key for key, value in entry.items() if not isinstance(value, types[key]))
        if wrong:
            ap.error(f"site.toml [[nav]] entry {entry['file']}: wrong value types for {wrong} "
                     "(text for label, file, group and short; true or false for hidden)")
    if not isinstance(site.get("nested_nav", False), bool):
        ap.error("site.toml: nested_nav must be true or false")
    if not isinstance(site.get("page_number_notes", False), bool):
        ap.error("site.toml: page_number_notes must be true or false")
    global KNOWN_COMPONENTS
    extra = site.get("extra_components", [])
    if not isinstance(extra, list) or any(not isinstance(c, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", c) or c in KNOWN_COMPONENTS for c in extra) or len(set(extra)) != len(extra):
        ap.error("extra_components must name distinct local components")
    KNOWN_COMPONENTS = (*KNOWN_COMPONENTS, *extra)
    for name in extra:
        if not component_script(name).is_file():
            ap.error(f"local component missing: {name}.js")
    shell = (COMPONENTS / "shell.html").read_text()

    # Edit links need a branch; source links may pin the exact built commit.
    site["_edit_ref"] = site.get("gh_ref", "main")
    if os.environ.get("GITHUB_SHA"):
        site["gh_ref"] = os.environ["GITHUB_SHA"]
    bundle = SiteBundle(site)
    origins: dict[str, str] = {}
    outputs: dict[str, bytes] = {"html/" + name: data for name, data in gather_assets(site, origins=origins).items()}
    pages_meta = []
    md_files = topic_pages()
    for flat_source in sorted(PAGES.glob("*.md")):
        err(f"flat topic source {flat_source.name}: use <topic>/index.md")
    if not md_files:
        err(f"no pages found in {PAGES}")
    from source_pages import fragment_problems, load_registry
    source_pages, problems = load_registry(site, REPO, consumer_tracked_paths())
    for problem in problems:
        err(problem)
    site["_repository_tree"] = repository_tree(source_pages)
    seen_slugs: set[str] = set()
    for md_path in md_files:
        local_resource(md_path)
        meta, _ = parse_frontmatter(md_path.read_text(), md_path.name)
        pages_meta.append(meta)
        slug = meta.get("slug", md_path.parent.name)
        if slug in seen_slugs:
            err(f"duplicate slug: {slug}")
        seen_slugs.add(slug)
        built = build_page(md_path, site, shell)
        if built:
            try:
                outputs["html/" + built[0]] = bundle.rewrite_page(built[1]).encode()
            except (ValueError, OSError) as problem:
                err(str(problem))
    routes = {page.source: page.route for page in source_pages}
    for page in source_pages:
        if page.slug in seen_slugs:
            err(f"route collision: {page.route} is produced by more than one page ({page.source})")
            continue
        seen_slugs.add(page.slug)
        built = build_source_page(page, routes, site, shell)
        if built:
            pages_meta.append({"page_css": ["build-sheet.css"]})
            try:
                outputs["html/" + built[0]] = bundle.rewrite_page(built[1]).encode()
            except (ValueError, OSError) as problem:
                err(str(problem))
    rendered = {name[5:]: data.decode() for name, data in outputs.items()
                if name.startswith("html/") and name.endswith(".html") and "/" not in name[5:]}
    # Source pages check every fragment they link. Other pages check fragments
    # pointing into source pages, whose anchors come from Markdown headings.
    source_routes = {page.route for page in source_pages}
    for problem in [*fragment_problems(rendered, source_routes, set(rendered)),
                    *fragment_problems(rendered, set(rendered) - source_routes, source_routes)]:
        err(problem)
    if args.page and args.page not in seen_slugs:
        err("unknown page slug: " + args.page)
    for name, data in gather_page_css(pages_meta, origins=origins).items():
        destination = "html/" + name
        if destination in outputs and outputs[destination] != data:
            err(f"Local stylesheet would overwrite a shared asset: {name}")
        else:
            outputs[destination] = data
    try:
        outputs.update(bundle.gather())
        origins.update(bundle.resource_origins)
    except (ValueError, OSError) as problem:
        err(str(problem))
    version_asset_links(outputs)
    outputs[".nojekyll"] = b""
    outputs["index.html"] = ("<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
                             f"<title>{html.escape(site.get('title', 'Documentation'))}</title>"
                             "<meta http-equiv=\"refresh\" content=\"0; url=html/index.html\">"
                             "<a href=\"html/index.html\">Open the documentation</a></html>\n").encode()
    outputs["site-build.json"] = (json.dumps({"schema_version": 1, "source": "docs/topics",
        "public_pages": sorted(name for name in outputs if name.startswith("html/") and name.endswith(".html")),
        "source_pages": {page.route: page.source for page in source_pages},
        "local_media": sorted(bundle.local_media), "large_captures_packaged": False,
        # Repository source of each copied resource; publication checks these.
        "resource_origins": dict(sorted(origins.items())),
        "kit": {"version": (KIT_SITE.parent / "VERSION").read_text().strip(),
                "asset_sha256": hashlib.sha256(b"".join(key.encode() + outputs[key] for key in sorted(outputs) if key.startswith("html/assets/"))).hexdigest()},
        # Every generated file, so the next build can prune what it no longer produces.
        "files": sorted([*outputs, "site-build.json"])}, indent=2) + "\n").encode()
    for problem in validate_resources(outputs):
        err(problem)

    # Hand-edit tripwire: Generated output must hold exactly outputs + unmanaged files.
    # A file the previous build listed in site-build.json but this build no longer
    # produces (a figure moved off a page, a retired page) is obsolete and pruned;
    # a file no build ever listed is still a stray.
    unmanaged = set(site.get("unmanaged", []))
    previous: set[str] = set()
    try:
        previous = set(json.loads((OUTPUT_ROOT / "site-build.json").read_text()).get("files", []))
    except (OSError, ValueError):
        pass
    obsolete = []
    if OUTPUT_ROOT.is_dir():
        for p in sorted(OUTPUT_ROOT.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(OUTPUT_ROOT).as_posix()
            if rel in outputs or rel in unmanaged:
                continue
            if args.page and rel.endswith(".html"):
                continue  # other pages not rebuilt this run
            if rel in previous and not args.page:
                obsolete.append(rel)
                continue
            err(f"stray file in generated site (not produced by build, not in site.toml unmanaged): {rel}")

    if not OUTPUT_ROOT.resolve().is_relative_to(REPO):
        err("Generated output root must remain inside the consumer project")
    for rel in [*outputs, *obsolete]:
        dest = OUTPUT_ROOT / rel
        if Path(rel).is_absolute() or not dest.resolve().is_relative_to(OUTPUT_ROOT.resolve()) or dest.is_symlink():
            err(f"Generated output escapes its root or is a symlink: {rel}")

    if _errors:
        for e in _errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    stale, wrote = [], []
    for rel, data in sorted(outputs.items()):
        if args.page and rel.startswith("html/") and rel.endswith(".html") and rel != "html/" + args.page + ".html":
            continue
        dest = OUTPUT_ROOT / rel
        if dest.is_file() and dest.read_bytes() == data:
            continue
        if args.check:
            stale.append(rel)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            wrote.append(rel)

    removed = []
    for rel in obsolete:
        if args.check:
            stale.append(rel + " (obsolete)")
        else:
            (OUTPUT_ROOT / rel).unlink()
            removed.append(rel)

    if args.check:
        if stale:
            print("STALE (run `python .docs-kit/docsite.py build --project .`):", file=sys.stderr)
            for s in stale:
                print(f"  {s}", file=sys.stderr)
            return 2
        print("generated site is fresh")
        return 0
    for w in wrote:
        print(f"wrote .build/docs/{w}")
    for r in removed:
        print(f"removed obsolete .build/docs/{r}")
    if not wrote and not removed:
        print("generated site already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
