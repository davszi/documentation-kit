"""A topic page's source as the build reads it: frontmatter apart, includes expanded.

For a project's own checks that look at what a page says without building it:

    import sys; sys.path.insert(0, ".docs-kit/tooling")
    from page_source import page_source

    meta, body = page_source("docs/topics/guide/guide.md", project=".")

`meta` is the `+++` frontmatter as a dict. `body` is the text after it, with
every `<!-- include: path -->` marker replaced by the fragment it names,
fragments in fragments included. The build expands includes with these same
functions, so the text is what the build inlines.

Nothing later in the build is applied: slide markers, fold markers, tabs and
the site-map marker stay as written, and no Markdown is rendered. Frontmatter
keys are not validated; `build` and `lint` do that.

Every problem of a page is collected and raised once as `PageSourceError`,
whose `problems` lists them: a missing or unterminated frontmatter fence, TOML
that does not parse, an include that is missing, untracked, empty, outside
the theme and the project, part of a cycle, or nested deeper than
`INCLUDE_DEPTH`. Importing this module reads no environment variable and no
project.
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import re
import subprocess
import tomllib

INCLUDE_DEPTH = 8
INCLUDE_RE = re.compile(r"<!--\s*include:\s*(\S+)\s*-->")
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


def tracked_paths(repo: Path) -> frozenset[Path]:
    """Every file the project's Git repository tracks."""
    result = subprocess.run(["git", "ls-files", "-z"], cwd=repo, capture_output=True, check=True)
    return frozenset(repo / path for path in result.stdout.decode().split("\0") if path)


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
    A path that is absolute or holds `..` raises ValueError.
    """
    def rep(m: re.Match) -> str:
        relative = Path(m.group(1))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Include paths must stay inside the theme or project")
        chain = " -> ".join([*(item.name for item in _stack), m.group(1)])
        shared = kit_site / relative
        if shared.is_file() and not shared.is_symlink() and shared.resolve().is_relative_to(kit_site):
            p = shared
        else:
            try:
                p = local(site / relative)
            except ValueError as error:  # missing or untracked fragment: name the include chain, not a traceback
                problem(f"{name}: include not found or not tracked: {chain} ({error})")
                return ""
        if not p.is_file():
            problem(f"{name}: include not found: {chain}")
            return ""
        text = p.read_text()
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
        body = expand_includes(body, name, site=repo / "docs/site", problem=problems.append,
                               local=lambda item: local_resource(item, repo, tracked))
    except ValueError as error:
        problems.append(f"{name}: {error}")
    if problems:
        raise PageSourceError(problems)
    return meta, body
