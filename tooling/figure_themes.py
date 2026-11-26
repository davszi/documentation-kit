"""Dark and light colours for generated figures, and the settings matplotlib needs for either.

A page shows the dark figure, because the reader is dark. The light figure is
for slides and print. A generator draws once per theme and writes both files:

    <name>.svg          dark, the file pages show
    <name>.light.svg    light, beside it

The same naming holds for any suffix (`.png`, `.pdf`). `write_both` does this
for a matplotlib figure or for SVG text:

    import sys; sys.path.insert(0, ".docs-kit/tooling")
    from figure_themes import write_both

    def draw(colors):
        fig, ax = plt.subplots()
        ax.plot(x, y, color=colors.accent)
        return fig

    write_both("docs/figures/speed.svg", draw)

Series take `colors.series` in its order and never cycle past it; `alert` marks
a problem, is not a series colour and carries a label. `tests/test_figure_themes.py`
checks both palettes: text against its surfaces, marks against the surface, and
series colours against each other, also as seen with a red or green colour
deficiency. One pair stays close in the dark palette, whose colours are the
reader's: violet and blue, the second and fourth series. Label the lines of a
dark chart that shows both.

A project that sets its own site colours in `[theme_colors]` (`theme_colors.py`)
gets dark figures in them: `palette("dark")` takes the surfaces and text colours
of the project's site, and the hues the table sets (`accent`, `secondary` for
violet, `orange` for warm, `blue`, `red` for alert), read from
`docs/site/site.toml` under DOCSITE_PROJECT_ROOT or the working directory, so
run generators from the project root. The series order stays. `problems` runs
the contrast and series checks on such a palette, and `palette` refuses one
that fails them.
`DARK` and `LIGHT` stay the kit's palettes; the light one does not change.

The kit does not depend on matplotlib: `write_both` uses it only where it is
installed, and `matplotlib_rc` returns a plain dict.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

import theme_colors


@dataclass(frozen=True)
class Palette:
    name: str
    ink: str      # primary text
    sub: str      # secondary text
    dim: str      # axis labels and other muted text
    line: str     # grid lines, axes and panel borders
    panel: str    # a filled panel on the surface
    bg: str       # the surface
    accent: str
    warm: str
    violet: str
    blue: str
    alert: str    # a problem; not a series colour

    @property
    def series(self) -> tuple[str, ...]:
        """The series colours in their fixed order; neighbours in it stay apart."""
        return (self.accent, self.violet, self.warm, self.blue)


DARK = Palette("dark", ink="#e6edf3", sub="#a9b4c2", dim="#7d8896", line="#2f3b4a", panel="#121a24", bg="#0d1117",
               accent="#39d2c0", warm="#ffa657", violet="#bc8cff", blue="#79c0ff", alert="#ff7b72")
LIGHT = Palette("light", ink="#1f2328", sub="#59636e", dim="#656d76", line="#d0d7de", panel="#f6f8fa", bg="#ffffff",
                accent="#0f9a8c", warm="#bc5c00", violet="#8a55fb", blue="#0a5fbb", alert="#cf222e")
THEMES = {"dark": DARK, "light": LIGHT}


# The site colour each dark figure role takes; the kit's values are DARK's.
SITE_ROLES = {"ink": "figure-ink", "sub": "figure-sub", "dim": "figure-dim", "line": "figure-line",
              "panel": "figure-panel", "bg": "figure-bg"}
# The [theme_colors] key each dark figure hue takes, only when the table sets that key. Figures
# share the interface's hues: the first series is the site's accent.
HUE_KEYS = {"accent": "accent", "violet": "secondary", "warm": "orange", "blue": "blue", "alert": "red"}
TEXT_CONTRAST, MARK_CONTRAST = theme_colors.TEXT_CONTRAST, theme_colors.MARK_CONTRAST

# Series checks, after the categorical colour method of the dataviz guide. Distances are
# Euclidean in OKLab x100; colour deficiencies are simulated with Machado, Oliveira and
# Fernandes (2009) at severity 1.0, to which the thresholds are calibrated.
BAND = {"dark": (0.48, 0.80), "light": (0.43, 0.78)}  # OKLCH lightness of a series colour
# The guide's dark band ends at 0.70 for a #191919 surface; the kit's dark figures sit on the
# darker #0d1117 and reach 0.80 (warm), so the dark band here ends there.
CHROMA_FLOOR = 0.10            # OKLCH chroma; below it a hue reads as grey
APART = 15.0                   # neighbours in the series order, full colour vision
APART_DEFICIENT = 8.0          # the same neighbours as seen with each colour deficiency
PAIR_APART = 10.0              # any two series colours that are not neighbours, full colour vision
ALERT_APART = 10.0             # alert against every series colour, full colour vision
# Alert carries a label, so it is not held to the deficiency floor: the kit's own light
# palette has alert and warm 3.4 apart for deuteranopia, and its dark one 7.8.
MACHADO = {
    "protanopia": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216),
                   (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413),
                     (-0.011820, 0.042940, 0.968881)),
    "tritanopia": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602),
                   (0.004733, 0.691367, 0.303900)),
}


def _linear(color: str) -> tuple[float, float, float]:
    channels = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)


def oklab(color: str, vision: str | None = None) -> tuple[float, float, float]:
    """A colour in OKLab, as seen with full colour vision or with a deficiency from MACHADO."""
    rgb = _linear(color)
    if vision:
        rgb = tuple(min(max(sum(k * c for k, c in zip(row, rgb)), 0.0), 1.0) for row in MACHADO[vision])
    l, m, s = (v ** (1 / 3) for v in (0.4122214708 * rgb[0] + 0.5363325363 * rgb[1] + 0.0514459929 * rgb[2],
                                      0.2119034982 * rgb[0] + 0.6806995451 * rgb[1] + 0.1073969566 * rgb[2],
                                      0.0883024619 * rgb[0] + 0.2817188376 * rgb[1] + 0.6299787005 * rgb[2]))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklch(color: str) -> tuple[float, float]:
    """OKLCH lightness and chroma."""
    lightness, a, b = oklab(color)
    return lightness, (a * a + b * b) ** 0.5


def distance(first: str, second: str, vision: str | None = None) -> float:
    """OKLab distance x100, with full colour vision or a deficiency from MACHADO."""
    return 100 * sum((x - y) ** 2 for x, y in zip(oklab(first, vision), oklab(second, vision))) ** 0.5


def project_dark(table: dict) -> Palette:
    """DARK on a project's site colours: a `[theme_colors]` table, already checked."""
    if not table:
        return DARK
    colors = theme_colors.resolve(table)
    return replace(DARK, **{role: colors[name] for role, name in SITE_ROLES.items()},
                   **{role: colors[key] for role, key in HUE_KEYS.items() if key in table})


def series_problems(p: Palette) -> list[str]:
    """Series colours that sit outside the lightness band, read as grey or come too close."""
    found = []
    low, high = BAND[p.name] if p.name in BAND else BAND["dark"]
    # Named by place, not by colour: two series may share one colour, and the message must name both.
    roles = ("accent", "violet", "warm", "blue")
    series = list(zip(roles, p.series))
    for role in ("accent", "violet", "warm", "blue", "alert"):
        lightness, chroma = oklch(getattr(p, role))
        if not low <= lightness <= high:
            found.append(f"{p.name} figures: {role} {getattr(p, role)} has OKLCH lightness {lightness:.3f}, "
                         f"outside {low}-{high}")
        if chroma < CHROMA_FLOOR:
            found.append(f"{p.name} figures: {role} {getattr(p, role)} has OKLCH chroma {chroma:.3f}, "
                         f"below {CHROMA_FLOOR}; it reads as grey")
    for (one, first), (two, second) in zip(series, series[1:]):
        pair = f"{one} {first} and {two} {second}"
        apart = distance(first, second)
        if apart < APART:
            found.append(f"{p.name} figures: neighbouring series {pair} are {apart:.1f} apart; need {APART}")
        for vision in MACHADO:
            apart = distance(first, second, vision)
            if apart < APART_DEFICIENT:
                found.append(f"{p.name} figures: neighbouring series {pair} are {apart:.1f} apart with "
                             f"{vision}; need {APART_DEFICIENT}")
    # Series that are not neighbours in the order still share a chart: no two may read as one colour.
    for index, (one, first) in enumerate(series):
        for two, second in series[index + 2:]:
            apart = distance(first, second)
            if apart < PAIR_APART:
                found.append(f"{p.name} figures: series {one} {first} and {two} {second} are {apart:.1f} apart; "
                             f"need {PAIR_APART}")
    for role, color in series:
        apart = distance(p.alert, color)
        if apart < ALERT_APART:
            found.append(f"{p.name} figures: alert {p.alert} and {role} {color} are {apart:.1f} apart; "
                         f"need {ALERT_APART}")
    return found


def problems(p: Palette) -> list[str]:
    """Text hard to read, marks hard to see on the palette's two surfaces, and series too close."""
    found = series_problems(p)
    for surface in ("bg", "panel"):
        back = getattr(p, surface)
        for role in ("ink", "sub", "dim"):
            ratio = theme_colors.contrast(getattr(p, role), back)
            if ratio < TEXT_CONTRAST:
                found.append(f"{p.name} figures: text {role} {getattr(p, role)} on {surface} {back} "
                             f"has contrast {theme_colors.shown_ratio(ratio)}:1; text needs at least {TEXT_CONTRAST}:1")
        for role in ("accent", "violet", "warm", "blue", "alert"):
            ratio = theme_colors.contrast(getattr(p, role), back)
            if ratio < MARK_CONTRAST:
                found.append(f"{p.name} figures: mark {role} {getattr(p, role)} on {surface} {back} "
                             f"has contrast {theme_colors.shown_ratio(ratio)}:1; marks need at least {MARK_CONTRAST}:1")
    return found


def palette(theme: str = "dark", root=None) -> Palette:
    """The palette a generator draws a theme with; the dark one on the project's site colours.

    ``root`` is the project root; it defaults to DOCSITE_PROJECT_ROOT or the
    working directory. A project palette that fails ``problems`` raises ValueError.
    """
    if theme not in THEMES:
        raise ValueError(f"figure theme {theme!r} is not one of: {', '.join(THEMES)}")
    if theme != "dark":
        return THEMES[theme]
    chosen = project_dark(theme_colors.project_table(root))
    found = problems(chosen)
    if found:
        raise ValueError("[theme_colors] makes the dark figure palette hard to read: " + "; ".join(found))
    return chosen


def variant_path(path, theme: str = "dark") -> Path:
    """Where a figure's file for a theme lies: the dark file keeps its name, the light one gets `.light`."""
    path = Path(path)
    if theme not in THEMES:
        palette(theme)  # names the themes there are
    if theme == "dark":
        return path
    return path.with_name(f"{path.stem}.{theme}{path.suffix}")


def matplotlib_rc(theme: str = "dark") -> dict:
    """rcParams that colour a matplotlib figure for a theme; use with `matplotlib.rc_context`.

    Colours only: surfaces, text, axes, grid, legend and the series cycle. The
    SVG hash salt keeps generated ids the same from run to run.
    """
    return _rc(palette(theme))


def _rc(p: Palette) -> dict:
    cycle = ", ".join(repr(color) for color in p.series)
    return {
        "figure.facecolor": p.bg, "figure.edgecolor": p.bg,
        "savefig.facecolor": p.bg, "savefig.edgecolor": p.bg,
        "axes.facecolor": p.bg, "axes.edgecolor": p.line,
        "axes.labelcolor": p.sub, "axes.titlecolor": p.ink,
        "axes.prop_cycle": f"cycler('color', [{cycle}])",
        "text.color": p.ink,
        "xtick.color": p.line, "ytick.color": p.line,
        "xtick.labelcolor": p.dim, "ytick.labelcolor": p.dim,
        "grid.color": p.line,
        "legend.facecolor": p.panel, "legend.edgecolor": p.line, "legend.labelcolor": p.sub,
        "patch.edgecolor": p.bg,
        "svg.hashsalt": "docs-kit-figure",
    }


def write_both(path, draw, **savefig) -> list[Path]:
    """Draw a figure once per theme and write `<name>.<ext>` and `<name>.light.<ext>`.

    `draw(colors)` gets the theme's `Palette` and returns SVG text or a
    matplotlib figure. Where matplotlib is installed, `draw` runs inside that
    theme's `matplotlib_rc` context; a figure is saved with `savefig` passed
    on, and closed. Returns the written paths, dark first.
    """
    try:
        import matplotlib
    except ImportError:
        matplotlib = None
    written = []
    # Both palettes first, so a project palette that fails its checks writes no file.
    palettes = {theme: palette(theme) for theme in THEMES}
    for theme, colors in palettes.items():
        target = variant_path(path, theme)
        if matplotlib is None:
            _save(draw(colors), target, savefig)
        else:
            with matplotlib.rc_context(_rc(colors)):
                _save(draw(colors), target, savefig)
        written.append(target)
    return written


def _save(result, target: Path, savefig: dict) -> None:
    if isinstance(result, str):
        target.write_text(result if result.endswith("\n") else result + "\n")
        return
    if not hasattr(result, "savefig"):
        raise TypeError(f"draw must return SVG text or a matplotlib figure, not {type(result).__name__}")
    import matplotlib.pyplot as plt
    options = dict(savefig)
    # No creation date in the file, so an unchanged figure is the same bytes.
    dated = {".svg": "Date", ".pdf": "CreationDate"}.get(target.suffix)
    if dated:
        options["metadata"] = {dated: None, **options.get("metadata", {})}
    result.savefig(target, **options)
    plt.close(result)
