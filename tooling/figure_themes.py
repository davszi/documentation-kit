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

The kit does not depend on matplotlib: `write_both` uses it only where it is
installed, and `matplotlib_rc` returns a plain dict.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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


def palette(theme: str = "dark") -> Palette:
    if theme not in THEMES:
        raise ValueError(f"figure theme {theme!r} is not one of: {', '.join(THEMES)}")
    return THEMES[theme]


def variant_path(path, theme: str = "dark") -> Path:
    """Where a figure's file for a theme lies: the dark file keeps its name, the light one gets `.light`."""
    path = Path(path)
    palette(theme)
    if theme == "dark":
        return path
    return path.with_name(f"{path.stem}.{theme}{path.suffix}")


def matplotlib_rc(theme: str = "dark") -> dict:
    """rcParams that colour a matplotlib figure for a theme; use with `matplotlib.rc_context`.

    Colours only: surfaces, text, axes, grid, legend and the series cycle. The
    SVG hash salt keeps generated ids the same from run to run.
    """
    p = palette(theme)
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
    for theme in THEMES:
        target = variant_path(path, theme)
        if matplotlib is None:
            _save(draw(palette(theme)), target, savefig)
        else:
            with matplotlib.rc_context(matplotlib_rc(theme)):
                _save(draw(palette(theme)), target, savefig)
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
