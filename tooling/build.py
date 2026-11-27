#!/usr/bin/env python3
"""Render docs/topics/ into .build/docs/html/ (the build output — never hand-edit).

    python .docs-kit/docsite.py build --project . [--check] [--page <slug>]
    python .docs-kit/docsite.py build --project . --check-reader

Sources: docs/topics/*/index.md, or one level deeper in a `topic_group_folders`
folder (TOML frontmatter between +++ fences, markdown
body with raw-HTML passthrough and <!-- include: … --> directives), shared
components in docs/site/components/, vendored assets in docs/site/assets/.
Site config: docs/site/site.toml.

Exit codes: 0 built / clean · 1 content error, or a configuration error found
while rendering · 2 a configuration error from the checks of site.toml at
start, printed as `build.py: error: …`, or --check found the generated site
stale against a fresh render.

--check-reader renders every topic page with and without the chapter reader,
reports any content the reader changes and writes nothing (reader_content.py).

Runs on Python 3.12 with the pinned .docs-kit/requirements.txt dependencies.
No application runtime is needed.
"""

from __future__ import annotations

import datetime
import argparse
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import os
import html
import posixpath
import re
import sys
import subprocess
import tomllib
from urllib.parse import urlsplit
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
import page_source
import theme_colors  # `[theme_colors]` becomes theme_colors.ASSET, linked right after base.css
from page_source import INCLUDE_DEPTH, INCLUDE_RE, PAGE_END  # noqa: F401  (names this module has always had)
from worklog_entries import fenced_spans, links_checked_from

COMPONENTS = KIT_SITE / "components"
KATEX_SRC = KIT_SITE / "assets" / "vendor" / "katex"

# `brand` is accepted and not read: the sidebar header names the site (site_name).
FRONTMATTER_KEYS = {"title", "slug", "brand", "brand_sub", "body_class", "math", "components", "page_css", "toc", "raw", "ongoing", "reader",
                    "description", "thumbnail", "page_only", "opening"}
# A [[nav]] table accepts only these keys. TOML assigns every key written after a table header to that
# table, so a top-level setting placed below the first [[nav]] silently becomes part of a nav entry.
NAV_KEYS = {"label", "file", "group", "short", "hidden"}
# Project adapters removed in 5.0.0. A site.toml that still names one fails, so a
# project never builds without the mapping or evidence gate it relied on. The
# evidence adapter's optional `document_origin` went with `evidence_validator`.
REMOVED_HOOKS = ("path_resolver", "evidence_validator")
# Kept-copy settings removed in 5.0.0, for the same reason: exact-byte copies of
# old documents (`evidence_manifests`) and single old paths mapped to current
# files (`legacy_files`). A finished working document is cited from Git instead.
REMOVED_COPY_SETTINGS = ("evidence_manifests", "legacy_files")
KNOWN_COMPONENTS = ("toc", "nav", "tabs", "diagram", "code", "filelinks",
                    "lightbox", "plot-toggles", "carousel", "panel-switcher",
                    "fold-controls", "chapter-reader", "slide-face", "page-redirect")  # emission order
# Vendored font folders under assets/vendor/, published to assets/fonts/<family>/.
FONT_FAMILIES = ("atkinson-hyperlegible", "saira-condensed", "ibm-plex-sans", "ibm-plex-mono")
# `[group_colors]` in site.toml becomes this stylesheet; each value is written into a style rule.
GROUP_COLORS_ASSET = "assets/group-colors.css"
GROUP_COLOR = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})")
# NOTE: "plot-toggles" must precede "carousel" — it wraps each inline SVG in
# a .fig-unit that the carousel then treats as one slide.

_SVG_IMG_RE = re.compile(r'<img([^>]*?)\ssrc="\.\./figures/([^"]+\.svg)"([^>]*?)/?>')

# Typed collapsible folds (the spine+fold layout prototype):
#   <!-- fold: math The route-level problem -->
#   ...markdown (blank-line separated from the markers)...
#   <!-- /fold -->
# `<!-- fold: math (open) The route-level problem -->` makes the fold start open.
# Types drive the color + the reader's "Also show" options (fold-controls.js).
FOLD_TYPES = ("math", "experiment", "code", "dead-end")
# The markers match to the end of their own line only. Matching further would
# swallow the blank line after a closing marker, and Markdown would then read
# the next paragraph as part of the HTML block and show it as raw text.
_FOLD_OPEN_RE = re.compile(
    r"^<!--\s*fold:\s*(" + "|".join(FOLD_TYPES) + r")\s+(\(open\)\s+)?(.+?)\s*-->[ \t]*$", re.M)
_FOLD_CLOSE_RE = re.compile(r"^<!--\s*/fold\s*-->[ \t]*$", re.M)


def folds_to_html(chunk: str, name: str) -> str:
    n_open = len(_FOLD_OPEN_RE.findall(chunk))
    n_close = len(_FOLD_CLOSE_RE.findall(chunk))
    if n_open != n_close:
        err(f"{name}: unbalanced fold markers ({n_open} open, {n_close} close)")

    def open_sub(m: re.Match) -> str:
        kind, opened, title = m.group(1), m.group(2), m.group(3)
        return (f'<details class="fold fold-{kind}" data-fold="{kind}"{" open" if opened else ""}>\n'
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
    taken: set[str] = set()  # ids of the figures inlined so far on this page

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
        # Inlined figures share one DOM: Matplotlib's generic ids must not bind clip paths or glyph
        # references to a different figure. A page with the chapter reader names every id after its
        # figure. Any other page renames only an id that an earlier figure of the page already has,
        # so the first figure keeps its ids and a link that reached one before still reaches it.
        # Both keep the tg-<group>-- convention consumed by plot-toggles.js.
        prefix = f"figure-{Path(fname).stem}-{occurrence}"
        identifiers = re.findall(r'\bid="([^"]+)"', svg)

        def renamed(key: str) -> str:
            if key.startswith("tg-") and "--" in key:
                return key.split("--", 1)[0] + "--" + prefix + "-" + key.split("--", 1)[1]
            return prefix + "-" + key

        if namespace_ids:
            remap = {key: renamed(key) for key in identifiers
                     if (key.startswith("tg-") and "--" in key) or not key.startswith(Path(fname).stem + "-")}
        else:
            # A toggle group written without "--" keeps its "tg-<group>" start, and a new name that is
            # itself taken gets a counter.
            remap = {}
            for key in dict.fromkeys(identifiers):
                if key not in taken:
                    continue
                fresh = key + "--" + prefix if key.startswith("tg-") and "--" not in key else renamed(key)
                base, number = fresh, 1
                while fresh in taken or fresh in identifiers or fresh in remap.values():
                    number += 1
                    fresh = f"{base}-{number}"
                remap[key] = fresh
            if remap:
                # A style rule inside the figure that selects a renamed id follows it. Only a "#name" in a
                # selector is rewritten, that is one followed by "{" before any ";" or "}"; a colour is not.
                svg = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda block: block[1] + re.sub(
                    r'#([A-Za-z_][\w-]*)(?=[^{};]*\{)', lambda match: '#' + remap.get(match[1], match[1]), block[2]) + block[3],
                    svg, flags=re.S)
        if remap:
            svg = re.sub(r'\bid="([^"]+)"', lambda match: 'id="' + remap.get(match[1], match[1]) + '"', svg)
            svg = re.sub(r'url\(#([^)]*)\)', lambda match: 'url(#' + remap.get(match[1], match[1]) + ')', svg)
            svg = re.sub(r'((?:xlink:)?href=")#([^"]+)"', lambda match: match[1] + '#' + remap.get(match[2], match[2]) + '"', svg)
        taken.update(remap.get(key, key) for key in identifiers)
        if namespace_ids:
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

# Page tabs: top-level <!-- tab: Label --> markers split the page part into
# panels (content before the first marker stays above the bar as the shared
# header). Distinct hook classes from the mode-views tabs on purpose.
TAB_RE = re.compile(r"^<!--\s*tab:\s*(.+?)\s*-->\s*$", re.M)

# Registry markers render as human-readable callout cards (the label chip
# comes from CSS ::before); the raw **INVARIANT:**/**DON'T-REDO:** tags stay
# in the md source for `lint --registry`. A marker paragraph = the token at
# line start through the next blank line or fenced code block.
_CALLOUT_RES = (
    (re.compile(r"(?m)^\*\*INVARIANT:\*\*\s*((?:[^\n]+\n?)+?)(?=\n\s*\n|\Z)"), "inv"),
    (re.compile(r"(?m)^\*\*DON'T-REDO:\*\*\s*((?:[^\n]+\n?)+?)(?=\n\s*\n|\Z)"), "redo"),
)


def _marker_cards(text: str) -> str:
    for rx, kind in _CALLOUT_RES:
        text = rx.sub(
            lambda m, k=kind: f'<div class="callout {k}">\n\n{m.group(1).rstrip()}\n\n</div>\n',
            text,
        )
    return text


def markers_to_callouts(body: str) -> str:
    """Marker paragraphs as cards, outside fenced code blocks.

    A marker inside a fenced block, with backticks or tildes and also one left
    open to the end, stays text, so a page can show the source form. Only the
    text between fenced blocks is converted, so a marker paragraph that runs
    into a fence ends where the fence starts; a blank line then separates the
    card's closing tag from the fence, which would otherwise stay inside the
    HTML block.
    """
    parts, position = [], 0
    for start, end in fenced_spans(body):
        text = body[position:start]
        converted = _marker_cards(text)
        if converted != text and not converted.endswith("\n\n"):
            converted += "\n"
        parts += [converted, body[start:end]]
        position = end
    parts.append(_marker_cards(body[position:]))
    return "".join(parts)
HEADING_ID_RE = re.compile(r"\s*\{#([A-Za-z0-9][A-Za-z0-9_-]*)\}\s*$")

_errors: list[str] = []


KIT_SITE_URL = "https://davszi.github.io/documentation-kit/"
# When the site was last built, for the sidebar's last line. The time is the one
# thing a build does not derive from the sources, so it lives in this file
# alone: no page links it with a version, the asset digest leaves it out, and
# `--check` does not compare it. The navigation script loads it.
BUILD_INFO = "html/build-info.js"
# The repository address `docsite.py init` writes until the project sets its own.
STARTER_REPOSITORY = "https://github.com/example/project"


def kit_line_shown(site: dict) -> bool:
    """Whether the sidebar's last line is shown: `kit_link`, true unless site.toml says false."""
    shown = site.get("kit_link", True)
    if not isinstance(shown, bool):
        err("site.toml: kit_link must be true or false")
        return True
    return shown


def kit_line(site: dict) -> str:
    """The sidebar's foot: a link to the project's repository when `gh_repo` names one, then the kit
    with its pinned version and the place for the build time unless `kit_link` is false."""
    parts = []
    repo = site.get("gh_repo", "")
    address = urlsplit(repo)
    # A real address only: the starter's placeholder would send readers to a repository that is not the project's.
    if address.scheme in ("https", "http") and address.hostname and repo.rstrip("/").removesuffix(".git") != STARTER_REPOSITORY:
        host = "GitHub" if address.hostname in ("github.com", "www.github.com") else address.hostname
        parts.append(f'<a class="kit-source" href="{html.escape(repo, quote=True)}">Source on {html.escape(host)}<span aria-hidden="true"> ↗</span></a>')
    if site.get("_kit_line", True):
        version = (KIT_SITE.parent / "VERSION").read_text().strip()
        parts.append(f'<a href="{KIT_SITE_URL}">Built with the documentation kit {html.escape(version)}<span aria-hidden="true"> ↗</span></a>'
                     '<span class="kit-built" data-kit-built hidden></span>')
    return '<p class="kit-line">' + "".join(parts) + "</p>\n" if parts else ""


def write_build_info() -> None:
    """Record the time of this build, in UTC to the minute."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    (OUTPUT_ROOT / BUILD_INFO).write_text(f'window.docsSiteBuilt = "{stamp}";\n')


def err(msg: str) -> None:
    _errors.append(msg)


_notes: list[str] = []


def note(msg: str) -> None:
    """Something an automatically listed reference page tolerated; it never fails the build."""
    _notes.append(msg)


class DocsRenderer(mistune.HTMLRenderer):
    """HTML renderer with explicit-{#id} headings, source-anchored code
    fences and explicit display/inline math delimiters."""

    def __init__(self, math_enabled: bool = False) -> None:
        super().__init__(escape=False)
        self.heading_ids: list[str] = []
        # The ids of the page so far. A page rendered in several parts, one per tab, hands every part the same dict.
        self.seen_ids: dict[str, int] = page_source.taken_ids()  # a heading never takes an id of the shell
        self.math_enabled = math_enabled

    def heading(self, text: str, level: int, **attrs) -> str:
        m = HEADING_ID_RE.search(text)
        if m:
            hid, text = m.group(1), text[: m.start()]
        else:
            hid = page_source.slugify(html.unescape(text))  # the rendered text, its character references decoded
        hid = page_source.unique_heading_id(hid, self.seen_ids)  # a repeated heading: result, result-1, …
        self.heading_ids.append(hid)
        return f'<h{level}{self.id_attribute(hid)}>{text}</h{level}>\n'

    def id_attribute(self, hid: str) -> str:
        return f' id="{hid}"'

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


class ListedFileRenderer(DocsRenderer):
    """The renderer for an automatically listed file: every HTML fragment of the
    file passes `ListedHtml`, and a heading id that the kit's page uses is left out."""

    def __init__(self, raw_html) -> None:
        super().__init__(math_enabled=False)
        self.raw_html = raw_html

    def block_html(self, html: str) -> str:
        return self.raw_html.fragment(html, block=True) + "\n"

    def inline_html(self, html: str) -> str:
        return self.raw_html.fragment(html)

    def id_attribute(self, hid: str) -> str:
        return super().id_attribute(hid) if self.raw_html.admits_identifier(hid) else ""


def render_listed_file(text: str, source: str, *, reader: bool = False, tree: bool = False) -> tuple[str, list[str]]:
    """An automatically listed file as HTML that keeps only admitted raw HTML,
    and notes on what was not admitted. `reader` and `tree` say that the page gets the
    reader's bar and the Reference tree, whose ids a heading then leaves alone."""
    from source_pages import ListedHtml
    raw_html = ListedHtml(source)
    text = text.replace("\x00", "\ufffd")  # ListedHtml marks tags with U+0000
    renderer = ListedFileRenderer(raw_html)
    renderer.seen_ids = page_source.taken_ids(reader=reader, tree=tree)
    rendered = mistune.create_markdown(renderer=renderer, plugins=["table", "math"])(text)
    return raw_html.finish(rendered)


def validate_frontmatter(meta: dict, name: str) -> None:
    unknown = set(meta) - FRONTMATTER_KEYS
    if unknown:
        err(f"{name}: unknown frontmatter keys: {sorted(unknown)}")
    if "title" not in meta:
        err(f"{name}: frontmatter needs title")
    if "toc" not in meta:
        err(f"{name}: frontmatter needs toc (the sidebar is generated)")
    if "opening" in meta and meta["opening"] != "keep":
        err(f'{name}: frontmatter opening accepts only "keep": the text before the first chapter is kept on purpose')
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
    """Frontmatter and body; a problem is recorded as a build error. Projects use `page_source.page_source`."""
    meta, body = page_source.split_frontmatter(raw, name, err)
    if meta is None:
        return {}, body
    validate_frontmatter(meta, name)
    return meta, body


SITE_MAP_MARKER = "<!-- site-map -->"
_IMAGE_RE = re.compile(r'<img[^>]+src="([^"]+\.(?:svg|png|jpe?g|webp|gif))"|!\[[^\]]*\]\(([^)\s]+\.(?:svg|png|jpe?g|webp|gif))\)', re.I)


def site_name(site: dict) -> str:
    """The site's name in the sidebar header: `home_label`, else `title`.

    Every page shows the same name, because the header links to the home page.
    A blank `home_label` counts as unset.
    """
    label = site.get("home_label")
    if isinstance(label, str) and label.strip():
        return label.strip()
    return site.get("title") or "Documentation"


def tab_title(site: dict, fname: str, title: str) -> str:
    """A page's browser-tab title: the site's `title`, then the page's short name.

    The short name is the page's `[[nav]]` label when an entry lists the page,
    else its title. The home page shows the site's title alone. A site without
    a `title` keeps the page's title alone.
    """
    name = site.get("title")
    if not isinstance(name, str) or not name.strip():
        return title
    name = name.strip()
    if fname == "index.html":
        return name
    entry = next((n for n in site.get("nav", []) if n.get("file") == fname), None)
    short = entry["label"] if entry else title
    return f"{name} · {short}" if short and short != name else name


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
    # One character has room for a larger size than two or three.
    glyph = " brand-mark-glyph" if len(mark) == 1 else ""
    return f'<span class="brand-mark{glyph}" aria-hidden="true">{html.escape(mark)}</span>'


def site_map_html(site: dict) -> str:
    """Home-page cards for every visible page, grouped as in the navigation.

    Each card takes its title and subtitle from the page frontmatter and its
    thumbnail from the first figure on the page, so the map stays current.
    """
    sources = {}
    for path in topic_pages():
        meta, body = parse_frontmatter(path.read_text(), path.relative_to(PAGES).as_posix())
        sources[meta.get("slug", path.parent.name) + ".html"] = (meta, page_source.rendered_part(body))
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
    """Replace include markers; a problem is recorded as a build error. Projects use `page_source.page_source`."""
    return page_source.expand_includes(body, name, site=SRC, local=local_resource, problem=err,
                                       kit_site=KIT_SITE, _stack=_stack)


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


READER_BAR_ID_RE = re.compile(r"""\bid\s*=\s*["']chapter-reader["']""")


def places_reader_bar(body: str) -> bool:
    """Whether a page's own source places the reader's bar: the include of the component, or its id written out.

    Listing the `chapter-reader` component loads its script and styles; the bar is in the page only when
    the source puts it there. A bar that arrives through a project's own fragment is not seen here, and a
    heading "Chapter reader" then shares the bar's id, as it did before headings were numbered past the shell.
    """
    return (any(match.group(1) == "components/chapter-reader.html" for match in page_source.INCLUDE_RE.finditer(body))
            or bool(READER_BAR_ID_RE.search(body)))


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
    body = page_source.rendered_part(body)
    comps = list(meta.get("components", ["toc", "nav"]))
    automatic_reader = (bool(site.get("chapter_reader")) and meta.get("reader", True)
                        and "chapter-reader" not in comps and "page-redirect" not in comps and "location.replace(" not in body)
    if SITE_MAP_MARKER in body:
        body = body.replace(SITE_MAP_MARKER, site_map_html(site))

    # Heading ids are unique across the tabs of the page, and none is an id of the shell around them.
    seen_ids = page_source.taken_ids(reader=automatic_reader or places_reader_bar(body),
                                     tree=bool(site.get("_repository_tree")),
                                     plot_labels="plot-toggles" in comps and bool(site.get("plot_toggle_labels")))

    def render_chunk(chunk: str) -> str:
        chunk = expand_includes(chunk, name)
        if meta.get("raw"):
            # Whole-body HTML passthrough (the escape hatch as a mode):
            # converted pages whose content is still hand-built HTML skip
            # markdown entirely, so blank lines / indentation inside big
            # markup can't re-enter the markdown parser.
            return slides_to_html(chunk, name)
        renderer = DocsRenderer(math_enabled=bool(meta.get("math")))
        renderer.seen_ids = seen_ids
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
                (COMPONENTS / "chapter-reader.html").read_text(),
                opening="keep" if meta.get("opening") == "keep" else "warn")
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
    """Records for the sidebar's repository section: registered ones in declared
    order, then automatically listed ones; an automatic page carries its title."""
    from source_pages import first_heading
    from source_tree import TreeFile

    return [TreeFile(page.source, page.route,
                     page.title or first_heading(local_resource(REPO / page.source).read_text()) or page.source,
                     page.description, page.pinned)
            for page in source_pages]


def automatic_link_checks(site: dict, declared_local: set[str]):
    """`exists` and `media_ok` for automatically listed pages.

    Only tracked files and folders, files of a checked-out submodule and
    declared local evidence count, so the page does not depend on untracked
    files of one checkout. Media must also be packageable: a raster image
    (`raster_image`; declared local evidence by its suffix, as it may be
    absent), tracked, no symlink, nothing under `[publication]` private
    prefixes or suffixes.
    """
    from site_paths import resolve_site_path
    tracked = consumer_tracked_paths()
    folders = {parent for path in tracked for parent in path.parents if parent.is_relative_to(REPO)}
    local = {REPO / name for name in declared_local}
    publication = site.get("publication") if isinstance(site.get("publication"), dict) else {}
    private = tuple(tuple(value for value in publication.get(key, []) if isinstance(value, str) and value)
                    if isinstance(publication.get(key, []), list) else ()
                    for key in ("private_prefixes", "private_suffixes"))

    def candidates(path: Path) -> tuple[Path, ...]:
        # The kit's own mapping, as for every other page: the build output.
        return (path, resolve_site_path(path, root=REPO))

    def exists(path: Path) -> bool:
        for item in candidates(path):
            if item in tracked or item in folders or item in local:
                return True
            # A tracked parent is a submodule, such as the kit, checked out at its pinned commit.
            if any(parent in tracked for parent in item.parents) and os.path.lexists(item):
                return True
        return False

    def media_ok(path: Path) -> bool:
        from source_pages import RASTER_SUFFIXES, raster_image
        for item in candidates(path):
            if item in local:
                return item.suffix.lower() in RASTER_SUFFIXES
            if item not in tracked or not item.is_relative_to(REPO):
                continue
            relative = item.relative_to(REPO).as_posix()
            if (any(parent.is_symlink() for parent in (item, *item.parents) if parent.is_relative_to(REPO) and parent != REPO)
                    or relative.startswith(private[0]) or relative.endswith(private[1])):
                continue
            # Read only a regular file, after the symlink check: a pipe would block.
            if item.is_file() and raster_image(item):
                return True
        return False

    return exists, media_ok


def build_source_page(page, routes: dict[str, str], site: dict, shell: str,
                      unchecked: dict[str, set[str]], automatic_checks=None,
                      plain: bool = False) -> tuple[str, str] | None:
    """Render one registered Markdown file as a whole-file page.

    The source keeps its own folder as link origin; no topic-page markers
    (includes, folds, registry callouts or the notes tail) are interpreted, so
    examples of those markers inside the record stay literal. When the page is
    the project's worklog, links in entries dated before
    `worklog_links_checked_from` may point at removed targets; `unchecked`
    receives the page's links whose fragments are not verified.

    An automatically listed page (`page.automatic`) never fails: its problems
    become notes, `automatic_checks` gives its `(exists, media_ok)` tests and
    `plain` shows the source as preformatted text, the fallback when the
    rendered page cannot be packaged.
    """
    from source_pages import (exists_in, first_heading, origin_banner, quiet_text, read_source, rewrite_links,
                              table_of_contents, wrap_tables)
    from site_paths import resolve_site_path
    from worklog_entries import configured_entry

    name = page.source
    if page.automatic:
        text = read_source(REPO / page.source)[0]
    else:
        text = local_resource(REPO / page.source).read_text()
    title = page.title or first_heading(text)
    if not title:
        err(f"{name}: a source page needs a level-one heading or a registered title")
        return None
    meta = {"title": title, "slug": page.slug, "toc": [], "math": page.math, "body_class": "source-page reference-page",
            "page_css": ["build-sheet.css"]}
    report = note if page.automatic else err
    if plain:
        content = "<pre>" + html.escape(text) + "</pre>\n"
        problems = []
        unchecked[page.route] = set()
    else:
        try:
            around = {"reader": bool(page.reader and site.get("chapter_reader")), "tree": bool(site.get("_repository_tree"))}
            if page.automatic:
                content, tolerated = render_listed_file(text, name, **around)
            else:
                renderer = DocsRenderer(math_enabled=page.math)
                renderer.seen_ids = page_source.taken_ids(**around)
                content = mistune.create_markdown(renderer=renderer, plugins=["table", "math"])(text)
        except Exception as problem:  # noqa: BLE001 - only an automatic page reaches the fallback
            if not page.automatic:
                raise
            note(f"{name}: Markdown rendering failed ({type(problem).__name__}); shown as plain text")
            return build_source_page(page, routes, site, shell, unchecked, automatic_checks, plain=True)
        if page.automatic:
            for problem in tolerated:
                note(problem)
        worklog = configured_entry(site, "worklog")
        is_worklog = isinstance(worklog, str) and posixpath.normpath(worklog) == page.source and not page.automatic
        exists, media_ok = automatic_checks if page.automatic else (exists_in(REPO, resolve_site_path), None)
        content, problems, unchecked[page.route] = rewrite_links(
            wrap_tables(content), page, routes, REPO, exists,
            site.get("_links_checked_from") if is_worklog else None, media_ok=media_ok)
    if page.automatic:
        content = quiet_text(content)
    for problem in problems:
        report(problem)
    banner = origin_banner(page, site.get("gh_repo", ""), site.get("_edit_ref", site.get("gh_ref", "main")),
                           raw=(REPO / page.source).read_text() if page.copy_raw else None)
    content = banner + content
    comps = ["toc", "nav", "code", "filelinks"]
    if page.reader and site.get("chapter_reader"):
        from chapter_layout import reader_page
        from source_pages import merge_short_introduction
        content = merge_short_introduction(content)
        try:
            # A record is written for agents and may open with a line of its own: no warning for it.
            content, meta["toc"] = reader_page([(None, content)], [], title,
                                               (COMPONENTS / "chapter-reader.html").read_text(), opening="record")
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
    return finish_page(meta, page.slug, name, content, comps, site, shell, {}, listed=page.automatic)


def finish_page(meta: dict, slug: str, name: str, content: str, comps: list, site: dict,
                shell: str, id_to_panel: dict, listed: bool = False) -> tuple[str, str]:
    """Inline figures, select components and fill the shared shell.

    The content of an automatically listed file (`listed`) inlines no figure
    and turns on no component: neither may follow what the file contains.
    """
    if not listed:
        content = inline_svg_figures(content, name, namespace_ids="chapter-reader" in comps)

    if meta.get("ongoing"):
        content = (
            '<div class="ongoing-banner">ongoing — this experiment is live; '
            "numbers may still move</div>\n" + content
        )

    # Typed folds need this component for both their styling and reader bar.
    # Inspect rendered content so folds from included fragments count too.
    if not listed and '<details class="fold ' in content and "fold-controls" not in comps:
        comps.append("fold-controls")
    if not listed and "data-slide-face" in content and "slide-face" not in comps:
        comps.append("slide-face")
    # A Reference tree too large to inline is loaded by nav.js.
    if site.get("_repository_tree_script") and "nav" not in comps:
        comps.append("nav")
    for c in comps:
        if c not in KNOWN_COMPONENTS:
            err(f"{name}: unknown component {c!r} (known: {KNOWN_COMPONENTS})")

    nav_entries = site.get("nav", [])
    fname = f"{slug}.html"
    tree = site.get("_repository_tree", [])
    # Registered records are listed by the repository tree; pages need a nav entry.
    from source_tree import TREE_INDEX
    if fname not in {n["file"] for n in nav_entries} and fname not in {f.route for f in tree} and fname != TREE_INDEX:
        err(f"{name}: {fname} missing from site.toml [[nav]] registry")
    crossnav_lines, last_group, section_close = [], None, '    </div>'
    # Every group is a native disclosure, so a reader can close what they do
    # not need; it works without JavaScript and with the reader. A group starts
    # open. `folded_groups` names the groups that start closed unless they hold
    # the current page.
    folded = set(site.get("folded_groups", []))
    current_group = next((n.get("group") for n in nav_entries
                          if n["file"] == fname and not n.get("hidden", False) and fname != "index.html"), None)
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
                crossnav_lines.append(section_close)
            if group and group in folded:
                opened = " open data-nav-default" if group == current_group else ""
                crossnav_lines.append(f'    <details class="nav-section nav-section-fold" data-group="{html.escape(group)}"{opened}>')
                crossnav_lines.append(f'    <summary class="nav-group" data-group="{html.escape(group)}">{html.escape(group)}</summary>')
                section_close = '    </details>'
            elif group:
                crossnav_lines.append(f'    <details class="nav-section nav-section-fold" data-group="{html.escape(group)}" open data-nav-open>')
                crossnav_lines.append(f'    <summary class="nav-group" data-group="{html.escape(group)}">{html.escape(group)}</summary>')
                section_close = '    </details>'
            last_group = group
        attrs = ' class="xpage current" aria-current="page"' if current else ' class="xpage"'
        if group:
            attrs += f' data-group="{html.escape(group)}"'
        short = n_entry.get("short", n_entry["label"])
        if short != n_entry["label"]:
            attrs += f' title="{html.escape(n_entry["label"], quote=True)}"'
        crossnav_lines.append(f'    <a{attrs} href="{n_entry["file"]}">{html.escape(short)}</a>')
    if last_group:
        crossnav_lines.append(section_close)
    crossnav = "\n".join(crossnav_lines)
    toc = toc_html(meta.get("toc", []), name, id_to_panel)
    if site.get("nested_nav") and "chapter-reader" not in comps:
        crossnav, toc = nested_nav_html(nav_entries, fname, toc), ""
    if tree:
        from source_tree import tree_html
        listed = any(entry.get("file") == fname and not entry.get("hidden") for entry in nav_entries)
        crossnav += "\n" + tree_html(tree, fname, listed=listed, script=site.get("_repository_tree_script"))

    # Right after base.css, so its colours replace the kit's before any other stylesheet reads them.
    head_extra = f'<link rel="stylesheet" href="{theme_colors.ASSET}">\n' if site.get(theme_colors.TABLE) else ""
    # Before every other stylesheet but base.css, so a page's own CSS can still set --g.
    head_extra += f'<link rel="stylesheet" href="{GROUP_COLORS_ASSET}">\n' if site.get("group_colors") else ""
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
    if "plot-toggles" in comps and site.get("plot_toggle_labels"):
        scripts = plot_toggle_labels_script(site["plot_toggle_labels"]) + scripts
    if meta.get("math"):
        scripts += katex_scripts()

    body_class = ' class="' + html.escape(meta['body_class'], quote=True) + '"' if meta.get('body_class') else ''
    page = shell.replace("<body>", '<body' + body_class + ' data-site-home-label="' + html.escape(site_name(site), quote=True) + '">')
    values = {
        "{{TITLE}}": html.escape(meta.get("title", "")),
        "{{TAB_TITLE}}": html.escape(tab_title(site, fname, meta.get("title", ""))),
        "{{BRAND}}": brand_mark_html(site) + '<span class="brand-name">' + html.escape(site_name(site)) + "</span>",
        "{{BRAND_SUB}}": html.escape(meta.get("brand_sub", "")),
        "{{TOC}}": toc,
        "{{CROSSNAV}}": crossnav,
        "{{KIT_LINE}}": kit_line(site),
        "{{HEAD_EXTRA}}": head_extra,
        "{{CONTENT}}": content.rstrip() + "\n",
        "{{SCRIPTS}}": scripts,
    }
    # One pass over the shell: a placeholder written in a page's own text or
    # title stays text, and no script tag is written twice.
    page = re.sub("|".join(map(re.escape, values)), lambda match: values[match[0]], page)
    return fname, page


def local_resource(path: Path) -> Path:
    return page_source.local_resource(path, REPO, consumer_tracked_paths())


@lru_cache(maxsize=1)
def consumer_tracked_paths() -> frozenset[Path]:
    return page_source.tracked_paths(REPO)


def plot_toggle_labels_script(labels: dict[str, str]) -> str:
    """`[plot_toggle_labels]` as the JSON block that plot-toggles.js reads.

    `<`, `>` and `&` are escaped inside the JSON strings, so no label can end
    the script element.
    """
    data = json.dumps(labels, ensure_ascii=False, sort_keys=True)
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return f'<script type="application/json" id="plot-toggle-labels">{data}</script>\n'


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
    if site.get("group_colors"):
        assets[GROUP_COLORS_ASSET] = group_colors_css(site["group_colors"])
    if site.get(theme_colors.TABLE):
        assets[theme_colors.ASSET] = theme_colors.stylesheet(site[theme_colors.TABLE])
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


def group_colors_css(colors: dict[str, str]) -> bytes:
    """Colour each named navigation group through --g, as nav.js reads it.

    The sidebar group header and its page links, the home-page map group and
    the build-sheet chapter number of a page in the group take the colour.
    """
    lines = ["/* Generated from [group_colors] in docs/site/site.toml. */"]
    for name, color in colors.items():
        quoted = '"' + "".join(f"\\{ord(c):x} " if c in '"\\' or ord(c) < 32 or ord(c) == 127 else c
                               for c in name) + '"'
        lines.append(f".toc [data-group={quoted}],.map-group[data-group={quoted}]{{--g:{color}}}")
        # The map card's top edge, also outside `.home-map`, as the theme's hard-coded groups had it.
        lines.append(f".map-group[data-group={quoted}] .map-card{{border-top:2px solid var(--g)}}")
        lines.append(f"body:has(.xpage.current[data-group={quoted}]){{--bs-number:{color}}}")
    return ("\n".join(lines) + "\n").encode()


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
    ap.add_argument("--check-reader", action="store_true",
                    help="verify the chapter reader keeps every topic page's content; write nothing")
    args = ap.parse_args()

    site = tomllib.loads(local_resource(SRC / "site.toml").read_text())
    for key in REMOVED_HOOKS:
        if key in site:
            ap.error(f"site.toml: {key} was removed in kit 5.0.0; the kit no longer loads a project adapter. "
                     "Follow \"Remove the adapter hooks\" in the kit's docs/topics/releases/migrations/5.0.0.md, "
                     f"then delete the {key} setting")
    for key in REMOVED_COPY_SETTINGS:
        if key in site:
            ap.error(f"site.toml: {key} was removed in kit 5.0.0; the kit no longer keeps or maps copies of old documents. "
                     "Follow \"Remove the adapter hooks\" in the kit's docs/topics/releases/migrations/5.0.0.md, "
                     f"then delete the {key} setting")
    if "formula_check_required" in site and not isinstance(site["formula_check_required"], bool):
        ap.error("site.toml: formula_check_required must be true or false")
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
    if not isinstance(site.get("home_label", ""), str):
        ap.error("site.toml: home_label must be text")
    from topic_structure import GROUP_FOLDER_NAME
    group_folders = site.get("topic_group_folders", [])
    if (not isinstance(group_folders, list) or len(set(map(str, group_folders))) != len(group_folders)
            or any(not isinstance(name, str) or not GROUP_FOLDER_NAME.fullmatch(name) for name in group_folders)):
        ap.error("site.toml: topic_group_folders must list distinct folder names under docs/topics, without slashes")
    folded = site.get("folded_groups", [])
    if not isinstance(folded, list) or any(not isinstance(name, str) for name in folded) or len(set(folded)) != len(folded):
        ap.error("site.toml: folded_groups must list distinct navigation group names")
    # The sidebar lists visible entries except the home page, one section per run of a group.
    runs: list = []
    for entry in site.get("nav", []):
        if entry.get("hidden", False) or entry["file"] == "index.html":
            continue
        if not runs or runs[-1] != entry.get("group"):
            runs.append(entry.get("group"))
    for name in folded:
        if name not in runs:
            ap.error(f"site.toml: folded_groups names {name!r}, which no visible [[nav]] entry uses as its group")
        if runs.count(name) > 1:
            ap.error(f"site.toml: folded group {name!r} is split by other [[nav]] entries; keep its entries together")
    colors = site.get("group_colors", {})
    if not isinstance(colors, dict):
        ap.error('site.toml: group_colors must be a [group_colors] table mapping group names to colours, such as "guide" = "#6ee7c5"')
    visible_groups = {entry.get("group") for entry in site.get("nav", []) if not entry.get("hidden", False)}
    for name, color in colors.items():
        if name not in visible_groups:
            ap.error(f"site.toml: group_colors names {name!r}, which no visible [[nav]] entry uses as its group")
        if not isinstance(color, str) or not GROUP_COLOR.fullmatch(color):
            ap.error(f"site.toml: group_colors gives group {name!r} the colour {color!r}; "
                     "use a hex colour such as \"#6ee7c5\"")
    from figure_themes import problems as figure_problems, project_dark
    invalid = theme_colors.problems(site.get(theme_colors.TABLE, {}))
    if invalid:
        # Every bad key at once, so a project fixes the table in one pass.
        ap.error("site.toml: " + "\n  ".join(invalid))
    unreadable = [*theme_colors.contrast_problems(site.get(theme_colors.TABLE)),
                  *figure_problems(project_dark(site.get(theme_colors.TABLE, {})))]
    if unreadable:
        ap.error("site.toml: [theme_colors] fails a colour check. Text and marks must stay readable, and the figure "
                 "series, of which accent is the first, must stay apart:\n  " + "\n  ".join(unreadable))
    labels = site.get("plot_toggle_labels", {})
    if not isinstance(labels, dict):
        ap.error('site.toml: plot_toggle_labels must be a [plot_toggle_labels] table mapping plot group keys '
                 'to chip labels, such as "corridor" = "road corridor"')
    for key, label in labels.items():
        if not isinstance(label, str):
            ap.error(f"site.toml: plot_toggle_labels gives group {key!r} the label {label!r}; use a text string")
    try:
        site["_links_checked_from"] = links_checked_from(site)
    except ValueError as problem:
        ap.error(f"site.toml: {problem}")
    from source_pages import reference_settings
    try:
        reference_settings(site)
    except ValueError as problem:
        ap.error(str(problem))
    from capability_map import settings as capability_settings
    try:
        capability_settings(site)
    except ValueError as problem:
        ap.error(f"site.toml: {problem}")
    global KNOWN_COMPONENTS
    extra = site.get("extra_components", [])
    if not isinstance(extra, list) or any(not isinstance(c, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", c) or c in KNOWN_COMPONENTS for c in extra) or len(set(extra)) != len(extra):
        ap.error("extra_components must name distinct local components")
    KNOWN_COMPONENTS = (*KNOWN_COMPONENTS, *extra)
    for name in extra:
        if not component_script(name).is_file():
            ap.error(f"local component missing: {name}.js")
    site["_kit_line"] = kit_line_shown(site)
    shell = (COMPONENTS / "shell.html").read_text()
    if args.check_reader:
        if not site.get("chapter_reader"):
            print("chapter_reader is off in site.toml; there is nothing to compare")
            return 0
        from reader_content import report
        return report(topic_pages(),
                      lambda path, reader: (build_page(path, site if reader else dict(site, chapter_reader=False), shell)
                                            or (None, None))[1],
                      _errors, root=REPO)

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
    for group in site.get("topic_group_folders", []):
        folder = PAGES / group
        if not folder.is_dir():
            err(f"topic_group_folders: docs/topics/{group} is not a folder")
            continue
        # A group folder only groups: its pages and records live in the topic folders inside it.
        for flat_source in sorted(folder.glob("*.md")):
            err(f"topic group folder {group} holds {flat_source.name}: a group folder holds only topic folders; "
                f"use {group}/<topic>/{flat_source.name}")
    if not md_files:
        err(f"no pages found in {PAGES}")
    from source_pages import (automatic_pages, fragment_notes, fragment_problems, load_registry,
                              unlink_missing_fragments)
    source_pages, problems = load_registry(site, REPO, consumer_tracked_paths())
    for problem in problems:
        err(problem)
    seen_slugs: set[str] = set()
    for md_path in md_files:
        local_resource(md_path)
        meta, _ = parse_frontmatter(md_path.read_text(), md_path.name)
        pages_meta.append(meta)
        slug = meta.get("slug", md_path.parent.name)
        if slug in seen_slugs:
            err(f"duplicate slug: {slug}")
        seen_slugs.add(slug)
    # Automatic routes avoid every topic and registered route, so they never collide.
    automatic, tolerated = automatic_pages(site, REPO, consumer_tracked_paths(), source_pages,
                                           {slug + ".html" for slug in seen_slugs}
                                           | {page.route for page in source_pages}, KIT_SITE.parent)
    for problem in tolerated:
        note(problem)
    site["_repository_tree"] = repository_tree(source_pages + automatic)
    from source_tree import TREE_INDEX, TREE_SCRIPT, is_large, shared_tree_html, tree_script
    # The page lock keeps the tree out of pages a general-password reader opens,
    # so a locked publication always writes it once.
    locked = isinstance(site.get("publication"), dict) and site["publication"].get("lock") is True
    if is_large(site["_repository_tree"]) or (locked and site["_repository_tree"]):
        # Written once and loaded by nav.js instead of repeated in every page.
        outputs["html/" + TREE_SCRIPT] = tree_script(site["_repository_tree"])
        site["_repository_tree_script"] = (TREE_SCRIPT + "?v="
                                           + hashlib.sha256(outputs["html/" + TREE_SCRIPT]).hexdigest()[:10])
    automatic_checks = automatic_link_checks(site, bundle.declared_local)
    for md_path in md_files:
        built = build_page(md_path, site, shell)
        if built:
            try:
                outputs["html/" + built[0]] = bundle.rewrite_page(built[1]).encode()
            except (ValueError, OSError) as problem:
                err(str(problem))
    routes = {page.source: page.route for page in source_pages + automatic}
    unchecked_links: dict[str, set[str]] = {}
    for page in source_pages + automatic:
        if page.slug in seen_slugs:
            err(f"route collision: {page.route} is produced by more than one page ({page.source})")
            continue
        seen_slugs.add(page.slug)
        built = build_source_page(page, routes, site, shell, unchecked_links, automatic_checks)
        if built:
            pages_meta.append({"page_css": ["build-sheet.css"]})
            markup = built[1]
            if page.automatic:
                markup, tolerated = unlink_missing_fragments(markup, page.source)
                for problem in tolerated:
                    note(problem)
            try:
                outputs["html/" + built[0]] = bundle.rewrite_page(markup).encode()
            except (ValueError, OSError) as problem:
                if not page.automatic:
                    err(str(problem))
                    continue
                # The listing links every automatic page, so one that cannot be
                # packaged is still built: as its source text, without links or media.
                note(f"{page.source}: {problem}; shown as plain text")
                plain = build_source_page(page, routes, site, shell, unchecked_links, automatic_checks, plain=True)
                outputs["html/" + plain[0]] = bundle.rewrite_page(plain[1]).encode()
    if site.get("_repository_tree_script"):
        # Readers without JavaScript open the whole tree on this page.
        tree = site["_repository_tree"]
        if "html/" + TREE_INDEX in outputs:
            err(f"route collision: {TREE_INDEX} is the Reference index of a large tree")
        else:
            content = (f'<h1 id="reference">Reference</h1>\n<p>All {len(tree)} files of the sidebar\'s Reference '
                       'section, by folder.</p>\n<div class="toc reference-index"><div class="repo-tree">'
                       + shared_tree_html(tree) + '</div></div>\n')
            meta = {"title": "Reference", "slug": TREE_INDEX[:-len(".html")], "toc": [],
                    "body_class": "reference-page reference-index-page", "page_css": ["build-sheet.css"]}
            built = finish_page(meta, meta["slug"], TREE_INDEX, content, ["nav"], site, shell, {})
            pages_meta.append({"page_css": ["build-sheet.css"]})
            outputs["html/" + built[0]] = bundle.rewrite_page(built[1]).encode()
    rendered = {name[5:]: data.decode() for name, data in outputs.items()
                if name.startswith("html/") and name.endswith(".html") and "/" not in name[5:]}
    # Source pages check every fragment they link. Other pages check fragments
    # pointing into source pages, whose anchors come from Markdown headings.
    # Links from or into automatically listed pages are only noted.
    source_routes = {page.route for page in source_pages}
    automatic_routes = {page.route for page in automatic}
    for problem in [*fragment_problems(rendered, source_routes, set(rendered) - automatic_routes, unchecked_links),
                    *fragment_problems(rendered, set(rendered) - source_routes - automatic_routes, source_routes)]:
        err(problem)
    for problem in fragment_notes(rendered, automatic_routes):
        note(problem)
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
        "source_pages": {page.route: page.source for page in source_pages + automatic},
        # The Reference tree written once when it is too large to inline; it carries page titles.
        "reference_tree": ({"script": "html/" + TREE_SCRIPT, "index": "html/" + TREE_INDEX}
                           if site.get("_repository_tree_script") else None),
        "local_media": sorted(bundle.local_media), "large_captures_packaged": False,
        # Repository source of each copied resource; publication checks these.
        "resource_origins": dict(sorted(origins.items())),
        "kit": {"version": (KIT_SITE.parent / "VERSION").read_text().strip(),
                "asset_sha256": hashlib.sha256(b"".join(key.encode() + outputs[key] for key in sorted(outputs) if key.startswith("html/assets/"))).hexdigest()},
        # Every generated file, so the next build can prune what it no longer produces.
        # The build-time file belongs to the kit line: a site without the line publishes no build time.
        "files": sorted([*outputs, "site-build.json", *([BUILD_INFO] if site.get("_kit_line", True) else [])])}, indent=2) + "\n").encode()
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
            if rel in outputs or rel in unmanaged or (rel == BUILD_INFO and site.get("_kit_line", True)):
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
    # Lint reads these lines from `build --check` and shows them as its own notes.
    if args.check:
        for message in _notes:
            print(f"NOTE: reference page {message}")
    elif _notes:
        print(f"note: {len(_notes)} problem(s) in automatically listed reference pages were tolerated; "
              "`lint` lists them")

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
    # The build time moves only when the build changed the site, or the file is missing.
    if site.get("_kit_line", True) and (wrote or removed or not (OUTPUT_ROOT / BUILD_INFO).is_file()):
        write_build_info()
    for w in wrote:
        print(f"wrote .build/docs/{w}")
    for r in removed:
        print(f"removed obsolete .build/docs/{r}")
    if not wrote and not removed:
        print("generated site already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
