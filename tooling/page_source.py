"""A topic page's source as the build reads it: frontmatter apart, includes expanded.

For a project's own checks that look at what a page says without building it:

    import sys; sys.path.insert(0, ".docs-kit/tooling")
    from page_source import page_source

    meta, body = page_source("docs/topics/guide/guide.md", project=".")

`meta` is the `+++` frontmatter as a dict. `body` is the text after it, up to
a `<!-- page-end -->` marker, with every `<!-- include: path -->` marker
replaced by the fragment it names, fragments in fragments included. The build
cuts at the marker and expands includes with these same functions.

Nothing else of the build is applied: a project's `content_transform` does
not run, slide markers, fold markers, tabs and the site-map marker stay as
written, and no Markdown is rendered. Frontmatter keys are not validated;
`build` and `lint` do that.

Every problem of a page is collected and raised once as `PageSourceError`, a
`ValueError` whose `problems` lists them: a missing or unterminated
frontmatter fence, TOML that does not parse, an include that is missing,
untracked, empty, unreadable, outside the theme and the project, part of a
cycle, or nested deeper than `INCLUDE_DEPTH`. Importing this module reads no
environment variable and no project.

The kit's tools read the headings of Markdown source through
`markdown_headings`. It and the build make a heading's id with the same
`slugify` and `unique_heading_id`; the build slugifies the rendered heading,
so its id can still differ, as `markdown_headings` says.

`page_source`, `PageSourceError` and its `problems` are the stable interface.
The other names serve the build and may change.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
import tomllib

INCLUDE_DEPTH = 8
INCLUDE_RE = re.compile(r"<!--\s*include:\s*(\S+)\s*-->")
PAGE_END = "<!-- page-end -->"  # working-notes tail below this never renders
KIT_SITE = Path(__file__).resolve().parents[1] / "theme"


class PageSourceError(ValueError):
    """A page whose source cannot be read as the build reads it; `problems` has every reason."""

    def __init__(self, problems: list[str]):
        super().__init__("; ".join(problems))
        self.problems = tuple(problems)


def split_frontmatter(raw: str, name: str, problem: Callable[[str], None]) -> tuple[dict | None, str]:
    """The `+++` frontmatter and the text after it; `(None, text)` after reporting why it cannot be read."""
    if not raw.startswith("+++\n"):
        problem(f"{name}: missing +++ frontmatter fence at top")
        return None, raw
    end = raw.find("\n+++\n", 4)
    if end < 0:
        problem(f"{name}: unterminated +++ frontmatter")
        return None, raw
    try:
        return tomllib.loads(raw[4:end]), raw[end + 5:]
    except tomllib.TOMLDecodeError as e:
        problem(f"{name}: frontmatter TOML error: {e}")
        return None, raw[end + 5:]


def rendered_part(body: str) -> str:
    """The body up to its `<!-- page-end -->` marker; the build renders nothing below it."""
    return body.split(PAGE_END, 1)[0]


# Ids of the elements that the build writes around a page's content: the shell (theme/components/shell.html)
# on every page, the label of the Reference tree on a site that has one, the reader's bar on a page that uses
# the reader, and the labels of plot toggles on a page that shows them.
SHELL_IDS = ("backdrop", "sidebar", "toc", "top", "menu")
TREE_IDS = ("repo-tree-label",)
READER_IDS = ("chapter-reader",)
PLOT_LABEL_IDS = ("plot-toggle-labels",)


def taken_ids(*, reader: bool = False, tree: bool = False, plot_labels: bool = False) -> dict[str, int]:
    """The ids a built page holds before its first heading, for `unique_heading_id`.

    The build starts every page with them, so a heading "Menu" gets `menu-1`
    and can be reached; with the id `menu` a link found the shell's button
    first. An id is taken only on a page that holds its element, which the
    three flags say: where the page has no Reference tree, a heading keeps
    `repo-tree-label` and the links to it keep working. Lint's anchor list
    and the record notes read a Markdown file as GitHub shows it, where no
    shell exists, and start empty. Ids that scripts create while the page
    runs and the ids of the lock page are not reserved: no built page holds
    them.
    """
    ids = SHELL_IDS + (TREE_IDS if tree else ()) + (READER_IDS if reader else ()) + (PLOT_LABEL_IDS if plot_labels else ())
    return dict.fromkeys(ids, 0)


def unique_heading_id(hid: str, seen: dict[str, int]) -> str:
    """`hid`, or `hid-1`, `hid-2`… when an earlier heading of the page took it; `seen` carries the page's ids.

    GitHub numbers repeated headings the same way, so a link to the second
    "Result" heading is `#result-1` on GitHub and in the built page. The build,
    lint and the record notes all number through this function.
    """
    if not hid:
        return hid
    result = hid
    while result in seen:
        seen[hid] += 1
        result = f"{hid}-{seen[hid]}"
    seen[result] = 0
    return result


def slugify(text: str) -> str:
    """The id of a heading without an explicit `{#id}`, GitHub style.

    Tags are dropped, then punctuation, and every white-space character becomes
    a hyphen, so the spaces left around stripped punctuation stay as `--`. The
    build passes the rendered heading with its character references decoded;
    lint and the record notes pass the Markdown source text.
    """
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s", "-", text.strip())


# The ATX headings of Markdown source as the kit's readers have always read them. Group 1 is the run of `#`
# that gives the level, group 2 the heading text. Lint's anchors and the changed record sections read every
# level; the record notes' chapter index needs text on the line and separates with a space or tab only; a
# source page's title is a level-one heading written `# `; a worklog entry is a level-two heading written `## `.
ATX_HEADING = re.compile(r"(#{1,6})\s+(.*)")
ATX_HEADING_WITH_TEXT = re.compile(r"(#{1,6})[ \t]+(.+?)[ \t]*$")
TITLE_HEADING = re.compile(r"(#) (.*)")
ENTRY_HEADING = re.compile(r"(##) (.*)")
# A heading's explicit id, and the end of its text that is cut off before the text is used: from the first
# `{#` to the last `}` for lint and the record notes, only the last `{#…}` for a source page's title.
EXPLICIT_ID = re.compile(r"\{#([A-Za-z0-9][\w-]*)\}\s*$")
ID_SUFFIX = re.compile(r"\{#.*\}\s*$")
LAST_ID_SUFFIX = re.compile(r"\s*\{#[^}]*\}\s*$")
_FENCE_MARKS = ("```", "~~~")


@dataclass(frozen=True)
class Heading:
    line: int  # 1-based, counted at the line breaks the reader was given
    offset: int  # where the heading's line starts in the text
    level: int
    text: str  # without the cut-off end, stripped
    anchor: str  # the explicit `{#id}`, or `slugify` of the text; numbered through `seen`


def markdown_headings(text: str, *, syntax: re.Pattern = ATX_HEADING, fences: str | None = "indented",
                      skip: Sequence[tuple[int, int]] = (), line_breaks: str = "all", frontmatter: bool = False,
                      id_suffix: re.Pattern | None = ID_SUFFIX, seen: dict[str, int] | None = None) -> list[Heading]:
    """The headings of Markdown source, with the ids lint and the record notes give them, in file order.

    The defaults read the file as lint's anchor list does. The readers differ,
    and each keyword keeps one reader's rule:

    - `syntax`: which lines are headings, one of the patterns above.
    - `fences`: `"indented"` skips the lines from a line that starts with
      three backticks or tildes after any indentation to the next such line,
      either character closing; `"column0"` does the same for fence lines
      that start in the first column; None skips no lines.
    - `skip`: (start, end) offsets, such as fenced code that
      `worklog_entries.fenced_spans` finds; a heading whose line starts
      inside one is skipped.
    - `line_breaks`: `"all"` splits lines as `str.splitlines` does, at every
      Unicode line break; `"newline"` splits at `\\n` only.
    - `frontmatter`: skip a `+++` TOML frontmatter block at the top that is
      closed by a second `+++` line.
    - `id_suffix`: the end of the heading text cut off before the text is
      used and slugified; None keeps the whole text. An explicit id is always
      the one `EXPLICIT_ID` finds.
    - `seen`: the ids the page holds already, for `unique_heading_id`;
      it is updated.

    The build reads headings with mistune instead and slugifies their rendered
    text, so its ids can differ from these, for example for a heading that
    holds a link.
    """
    seen = {} if seen is None else seen
    if line_breaks == "all":
        lines = text.splitlines()
        lengths = [len(line) for line in text.splitlines(keepends=True)]
    elif line_breaks == "newline":
        lines = text.split("\n")
        lengths = [len(line) + 1 for line in lines]
    else:
        raise ValueError(f"line_breaks must be 'all' or 'newline', not {line_breaks!r}")
    if fences not in ("indented", "column0", None):
        raise ValueError(f"fences must be 'indented', 'column0' or None, not {fences!r}")
    start = 0
    if frontmatter and lines and lines[0] == "+++":
        closing = next((i for i in range(1, len(lines)) if lines[i] == "+++"), None)
        if closing is not None:
            start = closing + 1
    found, in_fence, offset = [], False, sum(lengths[:start])
    for index in range(start, len(lines)):
        line, line_start = lines[index], offset
        offset += lengths[index]
        mark = line.lstrip() if fences == "indented" else line
        if fences is not None and mark.startswith(_FENCE_MARKS):
            in_fence = not in_fence
            continue
        if in_fence or any(begin <= line_start < end for begin, end in skip):
            continue
        match = syntax.match(line)
        if not match:
            continue
        body = match.group(2)
        kept = id_suffix.sub("", body) if id_suffix is not None else body
        explicit = EXPLICIT_ID.search(body)
        anchor = unique_heading_id(explicit.group(1) if explicit else slugify(kept), seen)
        found.append(Heading(index + 1, line_start, len(match.group(1)), kept.strip(), anchor))
    return found


def tracked_paths(repo: Path) -> frozenset[Path]:
    """Every file the project's Git repository tracks; a name that is not UTF-8 is kept as the system reads it."""
    result = subprocess.run(["git", "ls-files", "-z"], cwd=repo, capture_output=True, check=True)
    return frozenset(repo / os.fsdecode(path) for path in result.stdout.split(b"\0") if path)


def local_resource(path: Path, repo: Path, tracked: frozenset[Path]) -> Path:
    """`path` resolved, when it is a tracked file inside the project and no symlink; ValueError otherwise."""
    resolved = path.resolve()
    if path.is_symlink() or not resolved.is_relative_to(repo):
        raise ValueError(f"Project resource escapes its root: {path}")
    if resolved not in tracked:
        raise ValueError(f"Local site input must be tracked by the consumer Git repository: {path}")
    return resolved


def expand_includes(body: str, name: str, *, site: Path, local: Callable[[Path], Path],
                    problem: Callable[[str], None], kit_site: Path = KIT_SITE,
                    _stack: tuple[Path, ...] = ()) -> str:
    """Replace include markers; included fragments may include others (depth-limited, no cycles).

    A path is looked up in the kit's theme first, then under `site`, where
    `local` resolves it or raises ValueError. A problem is reported through
    `problem` and its marker becomes empty text, so one run names them all.
    """
    def rep(m: re.Match) -> str:
        relative = Path(m.group(1))
        chain = " -> ".join([*(item.name for item in _stack), m.group(1)])
        if relative.is_absolute() or ".." in relative.parts:
            problem(f"{name}: include paths must stay inside the theme or project: {chain}")
            return ""
        shared = kit_site / relative
        if shared.is_file() and not shared.is_symlink() and shared.resolve().is_relative_to(kit_site):
            p = shared
        else:
            try:
                p = local(site / relative)
            except (ValueError, OSError, RuntimeError) as error:
                # Missing or untracked fragment, or a link loop: name the include chain, not a traceback.
                problem(f"{name}: include not found or not tracked: {chain} ({error})")
                return ""
        if not p.is_file():
            problem(f"{name}: include not found: {chain}")
            return ""
        try:
            text = p.read_text()
        except (OSError, UnicodeDecodeError) as error:
            problem(f"{name}: include cannot be read as text: {chain} ({type(error).__name__})")
            return ""
        if not text.strip():
            problem(f"{name}: include is empty: {m.group(1)}")
        resolved = p.resolve()
        if resolved in _stack:
            problem(f"{name}: include cycle: {chain}")
            return ""
        if len(_stack) >= INCLUDE_DEPTH:
            problem(f"{name}: includes nest deeper than {INCLUDE_DEPTH} levels: {chain}")
            return ""
        return expand_includes(text, name, site=site, local=local, problem=problem, kit_site=kit_site,
                               _stack=(*_stack, resolved))

    return INCLUDE_RE.sub(rep, body)


def page_source(path, project) -> tuple[dict, str]:
    """Frontmatter and include-expanded body of the page at `path` in the project at `project`.

    `path` is absolute or relative to `project`. Raises `PageSourceError` with
    every problem of the page.
    """
    repo = Path(project).resolve()
    page = Path(path)
    page = page if page.is_absolute() else repo / page
    name = page.relative_to(repo).as_posix() if page.is_relative_to(repo) else str(page)
    try:
        tracked = tracked_paths(repo)
    except (OSError, subprocess.CalledProcessError):
        raise PageSourceError([f"{repo}: not a Git repository; includes must be tracked files"]) from None
    try:
        raw = page.read_text()
    except (OSError, UnicodeDecodeError) as error:
        raise PageSourceError([f"{name}: cannot read the page: {error}"]) from None
    problems: list[str] = []
    meta, body = split_frontmatter(raw, name, problems.append)
    try:
        body = expand_includes(rendered_part(body), name, site=repo / "docs/site", problem=problems.append,
                               local=lambda item: local_resource(item, repo, tracked))
    except (ValueError, OSError, RuntimeError) as error:  # nothing leaves as another type
        problems.append(f"{name}: {error}")
    if problems:
        raise PageSourceError(problems)
    return meta, body


# The per-version migration guides the kit had until 5.9.0. 5.10.0 keeps one guide at a fixed
# address, so a project's link to one of these finds nothing through no fault of the project.
REMOVED_GUIDES = frozenset(name + ".md" for name in (
    "1.1.0", "2.0.0", "3.0.0", "3.1.0", "3.2.0", "4.0.0", "5.0.0", "5.1.0", "5.2.0", "5.5.0", "5.8.0", "5.9.0"))
REMOVED_GUIDE_PROBLEM = "link to a migration guide the kit removed"
REMOVED_GUIDE_NOTE = ("the kit keeps one migration guide since 5.10.0, docs/topics/releases/migration.md; "
                      "the guides of earlier versions are at its tag v5.9.0")


def removed_kit_guide(dest: Path) -> bool:
    """Whether `dest` is one of the kit's removed per-version migration guides.

    A project that linked one passed its checks before the upgrade. The build and lint report such
    a link as a note, so the project still passes; any other missing file stays an error.
    """
    folder = Path(__file__).resolve().parents[1] / "docs/topics/releases/migrations"
    return Path(dest).resolve().parent == folder and Path(dest).name in REMOVED_GUIDES
