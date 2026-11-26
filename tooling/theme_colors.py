"""A project's own site colours: the `[theme_colors]` table in docs/site/site.toml.

The reader's colours are CSS custom properties on `:root` in
`theme/components/base.css`. Fifteen of them are base colours a project may
set; the others are derived colours, each a mix of two base colours, that the
theme uses for its sidebar, slide faces, diagrams and figures:

    [theme_colors]
    bg = "#2b211b"
    panel = "#3a2c23"
    text = "#e6dccd"

The build writes the set colours, and every derived colour that mixes one of
them, to `assets/theme-colors.css`, which each page links after `base.css`.
Without the table nothing is written and the pages keep the kit's colours.

A derived colour keeps its exact kit value until a project sets one of the two
base colours it mixes; then it is mixed again from the project's colours, so
the reader keeps the kit's light and dark steps in the project's hues. Each
mix is a plain sRGB mix, as CSS `color-mix(in srgb, ...)` computes it.

`problems` checks the table's keys and values; `contrast_problems` checks that
text stays readable on the surfaces it sits on, with the WCAG ratios that the
figure palettes use. `figure_themes` reads the same table to draw figures on
the project's surfaces.
"""
from __future__ import annotations

from pathlib import Path
import os
import re
import tomllib

ASSET = "assets/theme-colors.css"
TABLE = "theme_colors"
HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})")

# The base colours a project may set, with the kit's values (base.css :root).
BASE = {
    "bg": "#0d1117", "bg2": "#0f141b", "panel": "#161b22", "panel2": "#1c2432",
    "border": "#2d333c", "text": "#c9d1d9", "bright": "#e6edf3", "muted": "#8b949e",
    "accent": "#39d2c0", "secondary": "#bc8cff", "blue": "#79c0ff", "link": "#58a6ff",
    "orange": "#ffa657", "red": "#f47067", "green": "#57ab5a",
}
_FIXED = {"black": "#000000", "white": "#ffffff"}

# Derived colours: name -> (kit value, first colour, its share in percent, second colour).
# The shares were fitted to the kit's values; tests/test_theme_colors.py keeps each
# mix of the kit's base colours close to the kit value it replaces.
DERIVED = {
    # Surfaces darker than the page
    "deck-bg": ("#05080c", "bg", 50, "black"),           # behind the slides of a deck
    "on-fill": ("#05080d", "bg", 50, "black"),           # text on a filled chapter pill
    "present-bg": ("#070a0f", "bg", 60, "black"),        # behind a presented slide
    "sidebar-bg": ("#080c13", "bg", 72, "black"),        # the sidebar
    "slide-figure-bg": ("#0b1016", "bg", 95, "black"),   # a figure on a slide face
    "slide-top": ("#0f1620", "panel2", 28, "bg"),        # the top of a slide face's gradient
    # Slide faces, diagrams and generated figures (figure_themes.DARK). The copies of base
    # colours keep their dark values where the reader's print style turns the page light.
    "figure-ink": ("#e6edf3", "bright", 100, "bright"),
    "figure-bg": ("#0d1117", "bg", 100, "bg"),
    "figure-panel": ("#121a24", "panel2", 50, "bg"),
    "figure-panel2": ("#162130", "panel2", 81, "bg"),
    "deck-line": ("#1e2a36", "panel2", 68, "border"),
    "figure-line": ("#2f3b4a", "panel2", 80, "muted"),
    "figure-held": ("#5b6b80", "panel2", 38, "muted"),   # the is-held tone of a slide face
    "figure-dim": ("#7d8896", "text", 58, "panel2"),
    "figure-sub": ("#a9b4c2", "text", 52, "muted"),
    # Diagrams and code
    "diagram-box": ("#161b22", "panel", 100, "panel"),
    "diagram-raised": ("#1c2432", "panel2", 100, "panel2"),
    "diagram-muted": ("#8b949e", "muted", 100, "muted"),
    "diagram-link": ("#58a6ff", "link", 100, "link"),
    "diagram-fill": ("#20262e", "border", 45, "panel"),
    "code-edge": ("#232a33", "border", 70, "bg2"),
    "code-edge-hi": ("#343c46", "border", 91, "muted"),
    "code-gutter": ("#4d5866", "panel2", 54, "muted"),
    "faint": ("#768390", "muted", 84, "panel2"),          # diagram lines and code comments
    "diagram-label": ("#9da7b3", "text", 76, "panel2"),
    # Sidebar text, from quiet to strong
    "nav-number": ("#6f7f92", "text", 55, "panel2"),
    "nav-group": ("#8394a7", "muted", 100, "muted"),
    "nav-chapter": ("#93a2b3", "muted", 77, "text"),
    "reader-chapter": ("#b0bfce", "text", 69, "muted"),
    "nav-text-soft": ("#d5dde6", "bright", 42, "text"),
    "nav-text": ("#dbe2ea", "bright", 61, "text"),
    "nav-text-strong": ("#e3e9f0", "bright", 87, "text"),
    "nav-hover": ("#e9eff6", "bright", 87, "white"),
    # Reading text
    "reader-text": ("#dde4ec", "bright", 68, "text"),
    "reader-strong": ("#f2f6fa", "bright", 50, "white"),
    "sheet-text": ("#e5ebf0", "bright", 100, "bright"),
    # The tint of hover washes and thin lines; the theme uses it only see-through, as --rule-rgb
    "rule": ("#94b2d6", "text", 45, "muted"),
    # Controls that scripts draw over pages and figures: lightbox, carousel, plot chips, lock notice
    "overlay": ("#080a0e", "bg", 60, "black"),          # the lightbox backdrop, see-through
    "lightbox-bg": ("#101319", "bg", 78, "panel"),      # behind an enlarged picture
    "caption": ("#9aa4b2", "muted", 73, "text"),        # lightbox hint, carousel label, a chip's default dot
    "control": ("#141820", "bg2", 86, "border"),        # a carousel arrow, see-through
    "control-hover": ("#3c465a", "panel2", 83, "bright"),
    "control-text": ("#dfe6ef", "bright", 76, "text"),
    "control-dot": ("#8c96a5", "muted", 96, "text"),    # a carousel dot, see-through
    "chip": ("#1e2430", "panel2", 98, "bg"),            # a plot-toggle chip, see-through
    "chip-hover": ("#374155", "panel2", 74, "muted"),
    "chip-text": ("#cdd6e0", "text", 82, "bright"),
    "warn-line": ("#f0883e", "orange", 90, "black"),    # the edge of the lock page's notice
    # Group tones: navigation groups without a [group_colors] colour take them in order
    # (nav.js), and so do the reader's chapter parts. Each is a lighter step of a hue.
    "group-tone-1": ("#6ee7c5", "accent", 70, "white"),
    "group-tone-2": ("#b69cff", "secondary", 81, "text"),
    "group-tone-3": ("#ffb35c", "orange", 89, "white"),
    "group-tone-4": ("#5cc8ff", "blue", 100, "blue"),
    "group-tone-5": ("#ff8597", "red", 81, "white"),
    "group-tone-6": ("#9ad46b", "green", 66, "white"),
}
# Derived from a hue, not a neutral: their mixes only follow the hue, so they stay further
# from the kit's value (tests/test_theme_colors.py allows more for them).
HUE_DERIVED = ("warn-line", *(f"group-tone-{n}" for n in range(1, 7)))

# Colours the theme also uses see-through. Each has a second property, `--<name>-rgb`,
# with its channels, used as `rgba(var(--accent-rgb),.35)`: that is the legacy syntax
# the theme had, so the kit's pages render exactly as before (a color-mix() tint would
# move gradients to Oklab and round differently).
CHANNELS = ("bg", "accent", "secondary", "blue", "orange", "red", "green", "sidebar-bg", "deck-bg", "rule",
            "overlay", "control", "control-hover", "control-dot", "chip", "chip-hover", "group-tone-1", "group-tone-2")

TEXT_CONTRAST, MARK_CONTRAST = 4.5, 3.0  # WCAG ratios: text, and graphical marks
_TEXT_ON = {"bg": "the page", "bg2": "code and panels", "panel": "cards", "panel2": "raised cards"}
# (text colour, surface) pairs the theme shows; each must reach TEXT_CONTRAST.
TEXT_PAIRS = (
    *[(text, surface) for text in ("text", "bright", "muted") for surface in ("bg", "bg2", "panel", "panel2")],
    *[(hue, surface) for hue in ("accent", "secondary", "blue", "link", "orange", "red", "green")
      for surface in ("bg", "panel")],
    *[(text, "sidebar-bg") for text in ("nav-group", "nav-chapter", "reader-chapter", "nav-text-soft",
                                        "nav-text", "nav-text-strong", "nav-hover")],
    ("nav-number", "bg2"),
    ("faint", "bg2"),                     # code comments in a code block
    ("diagram-label", "panel"),
    ("reader-text", "bg"), ("reader-strong", "bg"), ("sheet-text", "panel"),
    *[(f"group-tone-{n}", "sidebar-bg") for n in range(1, 7)],   # group labels in the sidebar
    ("caption", "overlay"), ("control-text", "control"), ("chip-text", "chip"),
    ("bg", "accent"),                     # the lock page's button text
    ("red", "figure-panel"),              # the is-alert tone's text on a slide tile
)
# (mark colour, surface) pairs: lines and outlines that must reach MARK_CONTRAST.
MARK_PAIRS = (("figure-held", "bg"), ("figure-held", "figure-panel"),   # the is-held tone's dashed outline
              ("red", "figure-panel"))                                   # the is-alert tone's outline


def problems(table) -> list[str]:
    """What is wrong with a `[theme_colors]` value: keys and hex colours only."""
    if not isinstance(table, dict):
        return [f'{TABLE} must be a [{TABLE}] table mapping colour names to hex colours, such as bg = "#2b211b"']
    found = []
    for key, value in table.items():
        if key not in BASE:
            found.append(f"{TABLE} sets {key!r}, which is not a theme colour; "
                         f"the colours a project can set are: {', '.join(BASE)}")
        elif not isinstance(value, str) or not HEX.fullmatch(value):
            found.append(f"{TABLE} gives {key!r} the value {value!r}; use a 3 or 6 digit hex colour such as \"#2b211b\"")
    return found


def _six(color: str) -> str:
    color = color.lower()
    return "#" + "".join(c * 2 for c in color[1:]) if len(color) == 4 else color


def _rgb(color: str) -> tuple[int, int, int]:
    color = _six(color)
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


def mix(first: str, share: int, second: str) -> str:
    """`color-mix(in srgb, first share%, second)` for opaque colours, as a hex colour."""
    t = share / 100
    return "#" + "".join(f"{round(a * t + b * (1 - t)):02x}" for a, b in zip(_rgb(first), _rgb(second)))


def resolve(table: dict | None = None) -> dict[str, str]:
    """Every theme colour, base and derived, for a valid table (None: the kit's colours)."""
    table = {key: _six(value) for key, value in (table or {}).items()}
    colors = {**BASE, **table}
    for name, (kit, first, share, second) in DERIVED.items():
        if first in table or second in table:
            anchors = {**colors, **_FIXED}
            colors[name] = mix(anchors[first], share, anchors[second])
        else:
            colors[name] = kit
    return colors


def overrides(table: dict) -> dict[str, str]:
    """The colours the stylesheet sets: the table's own and the derived ones that mix them."""
    colors = resolve(table)
    names = [*BASE, *DERIVED]
    changed = {name for name in table} | {name for name, (_, first, _, second) in DERIVED.items()
                                          if first in table or second in table}
    return {name: colors[name] for name in names if name in changed}


def stylesheet(table: dict) -> bytes:
    """The generated stylesheet; it redefines the custom properties on :root only."""
    lines = [f"/* Generated from [{TABLE}] in docs/site/site.toml. */", ":root{"]
    for name, value in overrides(table).items():
        lines.append(f"  --{name}:{value};")
        if name in CHANNELS:
            lines.append(f"  --{name}-rgb:{','.join(map(str, _rgb(value)))};")
    return ("\n".join(lines) + "\n}\n").encode()


def _linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def contrast(first: str, second: str) -> float:
    """The WCAG contrast ratio of two opaque colours."""
    lum = sorted((0.2126 * r + 0.7152 * g + 0.0722 * b
                  for r, g, b in (map(_linear, _rgb(color)) for color in (first, second))), reverse=True)
    return (lum[0] + 0.05) / (lum[1] + 0.05)


def shown_ratio(ratio: float) -> str:
    """A ratio cut, not rounded, to two decimals: 4.497 shows as 4.49, never as a passing 4.50."""
    return f"{int(ratio * 100) / 100:.2f}"


def contrast_problems(table: dict | None = None) -> list[str]:
    """Each text or mark colour that would be hard to read on its surface with these colours."""
    colors = resolve(table)
    found = []
    for pairs, floor, kind in ((TEXT_PAIRS, TEXT_CONTRAST, "text"), (MARK_PAIRS, MARK_CONTRAST, "mark")):
        for fg, surface in pairs:
            ratio = contrast(colors[fg], colors[surface])
            if ratio < floor:
                found.append(f"{TABLE}: {kind} colour {fg} {colors[fg]} on {surface} {colors[surface]} "
                             f"has contrast {shown_ratio(ratio)}:1; {kind} needs at least {floor}:1")
    return found


def project_table(root=None) -> dict:
    """The `[theme_colors]` table of a project, or {} when it sets none.

    ``root`` defaults to DOCSITE_PROJECT_ROOT or the working directory, as for
    the build. A table that fails ``problems`` raises ValueError.
    """
    root = Path(root if root is not None else os.environ.get("DOCSITE_PROJECT_ROOT", Path.cwd()))
    config = root / "docs" / "site" / "site.toml"
    if not config.is_file():
        return {}
    table = tomllib.loads(config.read_text()).get(TABLE, {})
    found = problems(table)
    if found:
        raise ValueError(f"{config}: " + "; ".join(found))
    return table
