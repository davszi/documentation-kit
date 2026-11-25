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

`page_source`, `PageSourceError` and its `problems` are the stable interface.
The other names serve the build and may change.
"""
from __future__ import annotations

from collections.abc import Callable
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


# Ids of the elements that the build writes around a page's content: the shell (theme/components/shell.html),
# the Reference tree's label in the sidebar, and the reader's bar on a page that uses the reader.
SHELL_IDS = ("backdrop", "sidebar", "toc", "repo-tree-label", "top", "menu")
READER_IDS = ("chapter-reader",)


def taken_ids(reader: bool = False) -> dict[str, int]:
    """The ids a built page holds before its first heading, for `unique_heading_id`.

    The build starts every page with them, so a heading "Menu" gets `menu-1`
    and can be reached; with the id `menu` a link found the shell's button
    first. `reader` adds the id of the reader's bar. Lint's anchor list and
    the record notes read the Markdown file as GitHub shows it, where no
    shell exists, and start empty. Ids that scripts create while the page
    runs and the ids of the lock page are not reserved: no built page holds
    them, so a link to such a heading works where the script does not run.
    """
    return dict.fromkeys(SHELL_IDS + (READER_IDS if reader else ()), 0)


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
