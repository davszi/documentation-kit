#!/usr/bin/env python3
"""The capability map: what the project's tooling does, where it lives and who imports it.

    python .docs-kit/docsite.py capability-map --project .

rewrites the generated "Imported by" column of the map. `docsite.py lint` checks
the map when `docs/site/site.toml` names `tooling_roots`; a project that sets
none of the settings below is not checked.

Settings, top-level in site.toml, above the first [[nav]] table:
  tooling_roots     folders whose direct entries every row of the map must cover
  capability_map    the map's path (default docs/CAPABILITY_MAP.md)
  experiment_roots  folders whose subfolders are experiments; a tool that
                    imports from one gets a warning

The map holds one table with the columns Need | Code | State | Imported by. "Used
by" is generated from Python imports only; rules/engineering/code.md, section
"The capability map", owns the format and what the check does not cover.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path, PurePosixPath

DEFAULT_MAP = "docs/CAPABILITY_MAP.md"
HEADER = ("need", "code", "state", "imported by")
STATES = ("exists", "partly", "missing")
NO_CODE = "—"
NO_IMPORTS = "no Python imports"
NOT_PYTHON = "not scanned: no Python code"
COMMAND = "docsite.py capability-map --project ."
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")


# ---------------------------------------------------------------- settings
def _folders(value, key: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{key} must list project-relative folders, such as [\"tools/\"]")
    folders = []
    for item in value:
        path = PurePosixPath(item) if isinstance(item, str) else None
        if (path is None or not item.strip() or "\\" in item or path.is_absolute()
                or ".." in path.parts or str(path) == "."):
            raise ValueError(f"{key} must list project-relative folders inside the project, such as [\"tools/\"]; "
                             f"{item!r} is not one")
        folders.append(str(path))
    if len(set(folders)) != len(folders):
        raise ValueError(f"{key} lists a folder twice")
    return tuple(folders)


def settings(site: dict) -> dict | None:
    """The validated settings, or None when the project has not opted in.

    Raises ValueError for a wrong value or for `capability_map` or
    `experiment_roots` without `tooling_roots`, which would check nothing.
    """
    if "tooling_roots" not in site:
        for key in ("capability_map", "experiment_roots"):
            if key in site:
                raise ValueError(f"{key} needs tooling_roots; without it the capability map is not checked")
        return None
    tooling = _folders(site["tooling_roots"], "tooling_roots")
    if not tooling:
        raise ValueError("tooling_roots must name at least one folder; remove the setting to turn the check off")
    experiments = _folders(site.get("experiment_roots", []), "experiment_roots")
    for a in tooling + experiments:
        for b in tooling + experiments:
            if a != b and PurePosixPath(a).is_relative_to(b):
                raise ValueError(f"tooling_roots and experiment_roots must not overlap: {a} lies inside {b}")
    path = site.get("capability_map", DEFAULT_MAP)
    pure = PurePosixPath(path) if isinstance(path, str) else None
    if pure is None or pure.is_absolute() or ".." in pure.parts or pure.suffix != ".md" or "\\" in path:
        raise ValueError("capability_map must name a project-relative Markdown file, such as \"docs/CAPABILITY_MAP.md\"")
    return {"tooling_roots": tooling, "experiment_roots": experiments, "map": str(pure)}


def site_settings(root: Path) -> dict | None:
    config = Path(root) / "docs/site/site.toml"
    site = tomllib.loads(config.read_text()) if config.is_file() else {}
    return settings(site)


# ---------------------------------------------------------------- repository
def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True)
    if result.returncode != 0:
        raise ValueError("the capability map check needs a Git checkout; git ls-files failed")
    return sorted(set(filter(None, result.stdout.decode().split("\0"))))


def _inside(path: str, folder: str) -> bool:
    return path == folder or path.startswith(folder + "/")


def root_entries(tracked: list[str], root: str) -> list[str]:
    """Every tracked file or folder directly under a tooling root.

    Names that start with a dot and `__init__.py` are not entries.
    """
    entries = set()
    for path in tracked:
        if not path.startswith(root + "/"):
            continue
        rest = path[len(root) + 1:].split("/")
        if rest[0].startswith(".") or (len(rest) == 1 and rest[0] == "__init__.py"):
            continue
        entries.add(f"{root}/{rest[0]}")
    return sorted(entries)


class ImportIndex:
    """Python imports of the tracked files, resolved to tracked paths.

    A name resolves against the importing file's folder, the project root and
    each tooling root, in that order; relative imports resolve against their
    package. Imports inside functions count. Dynamic imports (importlib,
    __import__), subprocess calls and sys.path changes are not followed.
    """

    def __init__(self, root: Path, tracked: list[str], tooling_roots: tuple[str, ...]):
        self.root, self.tooling_roots = Path(root), tooling_roots
        self.files = set(tracked)
        self.dirs = {str(parent) for path in tracked for parent in PurePosixPath(path).parents if str(parent) != "."}
        self.unreadable: list[str] = []
        self.imports: dict[str, list[tuple[int, str]]] = {}
        for path in tracked:
            if path.endswith(".py") and (self.root / path).is_file():
                self.imports[path] = self._scan(path)

    def _module(self, base: str, parts: list[str]) -> str | None:
        stem = "/".join(p for p in (base, *parts) if p)
        if parts and stem + ".py" in self.files:
            return stem + ".py"
        if (stem + "/__init__.py" if stem else "__init__.py") in self.files:
            return stem + "/__init__.py" if stem else "__init__.py"
        if parts and stem in self.dirs:
            return stem
        return None

    def _deepest(self, base: str, parts: list[str]) -> str | None:
        for end in range(len(parts), 0, -1):
            found = self._module(base, parts[:end])
            if found:
                return found
        return None

    def _scan(self, path: str) -> list[tuple[int, str]]:
        try:
            tree = ast.parse((self.root / path).read_bytes(), filename=path)
        except (SyntaxError, ValueError) as problem:
            self.unreadable.append(f"{path}: {problem.__class__.__name__}")
            return []
        folder = str(PurePosixPath(path).parent)
        folder = "" if folder == "." else folder
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for base in (folder, "", *self.tooling_roots):
                        target = self._deepest(base, alias.name.split("."))
                        if target:
                            found.append((node.lineno, target))
                            break
            elif isinstance(node, ast.ImportFrom):
                parts = node.module.split(".") if node.module else []
                if node.level:
                    package = PurePosixPath(path).parent
                    for _ in range(node.level - 1):
                        package = package.parent
                    bases = ["" if str(package) == "." else str(package)]
                else:
                    bases = [folder, "", *self.tooling_roots]
                for base in bases:
                    targets = [self._module(base, parts + [alias.name]) for alias in node.names if alias.name != "*"]
                    targets = [t for t in targets if t]
                    if not targets:
                        whole = self._deepest(base, parts) if parts else self._module(base, [])
                        targets = [whole] if whole else []
                    if targets:
                        found.extend((node.lineno, t) for t in targets)
                        break
        return [(line, target) for line, target in found if target != path]


# ---------------------------------------------------------------- the map's table
def split_row(line: str) -> list[str]:
    """Cells of a Markdown table row; a pipe inside backticks or escaped stays in its cell."""
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    cells, cell, code, i = [], "", False, 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body) and body[i + 1] == "|":
            cell += "\\|"
            i += 2
            continue
        if ch == "`":
            code = not code
        if ch == "|" and not code:
            cells.append(cell.strip())
            cell = ""
        else:
            cell += ch
        i += 1
    if cell.strip():
        cells.append(cell.strip())
    return cells


def table_rows(text: str) -> tuple[int, list[tuple[int, list[str]]]] | None:
    """The line index of the capability table's header and its rows as (line index, cells)."""
    lines = text.splitlines()
    fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence or not line.lstrip().startswith("|"):
            continue
        if tuple(c.lower() for c in split_row(line)) != HEADER:
            continue
        rows = []
        for j in range(i + 2, len(lines)):
            if not lines[j].lstrip().startswith("|"):
                break
            rows.append((j, split_row(lines[j])))
        return i, rows
    return None


def code_links(cell: str, map_path: str, root: Path) -> tuple[list[str], list[str]]:
    """Project-relative paths the Code cell links, and links that leave the project."""
    paths, outside = [], []
    folder = PurePosixPath(map_path).parent
    for target in LINK_RE.findall(re.sub(r"`[^`]*`", "", cell)):
        if re.match(r"[a-z][a-z0-9+.-]*:", target):
            continue
        part = target.partition("#")[0].partition("?")[0]
        if not part:
            continue
        joined = os.path.normpath(str(folder / part))
        if joined.startswith("..") or os.path.isabs(joined):
            outside.append(target)
            continue
        paths.append("" if joined == "." else joined.replace(os.sep, "/"))
    return paths, outside


def _unit(path: str, s: dict) -> str:
    """How a user is named: its tooling entry, its experiment folder, or its own path."""
    for root in s["tooling_roots"]:
        if path.startswith(root + "/"):
            first = path[len(root) + 1:].split("/")
            return f"{root}/{first[0]}" + ("/" if len(first) > 1 else "")
    for root in s["experiment_roots"]:
        if path.startswith(root + "/"):
            first = path[len(root) + 1:].split("/")
            return f"{root}/{first[0]}/" if len(first) > 1 else path
    return path


def users_cell(paths: list[str], index: ImportIndex, s: dict) -> str:
    """The generated "Imported by" text for a row that links `paths`."""
    if not paths:
        return NO_CODE
    if not any(p.endswith(".py") or any(f.endswith(".py") and _inside(f, p) for f in index.imports)
               for p in paths):
        return NOT_PYTHON
    users = set()
    for path, imports in index.imports.items():
        if any(_inside(path, p) for p in paths):
            continue
        if any(any(_inside(target, p) for p in paths) for _, target in imports):
            unit = _unit(path, s)
            if not any(_inside(p, unit.rstrip("/")) for p in paths):
                users.add(unit)
    return ", ".join(f"`{u}`" for u in sorted(users)) if users else NO_IMPORTS


# ---------------------------------------------------------------- check and write
def check(root: Path, site: dict | None = None) -> tuple[list[str], list[str]]:
    """Errors and warnings for the project's capability map; none when it has not opted in."""
    root = Path(root)
    try:
        s = settings(site) if site is not None else site_settings(root)
    except ValueError as problem:
        return [f"site.toml: {problem}"], []
    if s is None:
        return [], []
    try:
        tracked = tracked_files(root)
    except ValueError as problem:
        return [str(problem)], []
    errors: list[str] = []
    warnings: list[str] = []
    map_path = s["map"]
    for folder in s["tooling_roots"] + s["experiment_roots"]:
        if not any(_inside(path, folder) for path in tracked):
            key = "tooling_roots" if folder in s["tooling_roots"] else "experiment_roots"
            errors.append(f"site.toml: {key} names {folder}/, which holds no tracked file")
    index = ImportIndex(root, tracked, s["tooling_roots"])
    for problem in index.unreadable:
        warnings.append(f"capability map: cannot read the imports of {problem}")
    for path, imports in sorted(index.imports.items()):
        if not any(_inside(path, r) for r in s["tooling_roots"]):
            continue
        for line, target in imports:
            for exp_root in s["experiment_roots"]:
                if target.startswith(exp_root + "/"):
                    folder = _unit(target, s)
                    warnings.append(f"{path}:{line} imports {target} from the experiment folder {folder}; "
                                    "move reused code into the tooling tree (rules/engineering/code.md#where-code-lives)")
    if not (root / map_path).is_file():
        errors.append(f"capability map {map_path} is missing; tooling_roots in site.toml turns its check on")
        return errors, warnings
    if map_path not in tracked:
        errors.append(f"capability map {map_path} is not tracked by Git")
    table = table_rows((root / map_path).read_text())
    if table is None:
        errors.append(f"{map_path}: no table with the columns Need | Code | State | Imported by")
        return errors, warnings
    linked: set[str] = set()
    for line, cells in table[1]:
        where = f"{map_path}:{line + 1}"
        if len(cells) != 4:
            errors.append(f"{where}: a row needs four cells, Need | Code | State | Imported by")
            continue
        need, code, state, used = cells
        paths, outside = code_links(code, map_path, root)
        for target in outside:
            errors.append(f"{where}: code link {target} leaves the project")
        linked.update(paths)
        if state.lower() not in STATES:
            errors.append(f"{where}: state {state!r} is not exists, partly or missing")
        elif state.lower() == "missing" and paths:
            errors.append(f"{where}: a missing need links no code; use partly when some code exists")
        elif state.lower() != "missing" and not paths:
            errors.append(f"{where}: state {state} needs a link to the code in the Code column")
        expected = users_cell(paths, index, s)
        if used != expected:
            errors.append(f"{where}: Imported by is out of date for {need!r}; run `{COMMAND}` "
                          f"(expected: {expected})")
    for folder in s["tooling_roots"]:
        for entry in root_entries(tracked, folder):
            if not any(p == entry or (p.startswith(entry + "/")) for p in linked):
                errors.append(f"{map_path}: {entry} is under the tooling root {folder}/ but no row links it")
    return errors, warnings


def write(root: Path) -> int:
    """Rewrite the "Imported by" cells of the project's map; return how many changed."""
    root = Path(root)
    s = site_settings(root)
    if s is None:
        raise LookupError("site.toml names no tooling_roots; the capability map is not used")
    path = root / s["map"]
    if not path.is_file():
        raise ValueError(f"capability map {s['map']} is missing")
    text = path.read_text()
    table = table_rows(text)
    if table is None:
        raise ValueError(f"{s['map']}: no table with the columns Need | Code | State | Imported by")
    index = ImportIndex(root, tracked_files(root), s["tooling_roots"])
    lines = text.splitlines(keepends=True)
    changed = 0
    for line, cells in table[1]:
        if len(cells) != 4:
            raise ValueError(f"{s['map']}:{line + 1}: a row needs four cells, Need | Code | State | Imported by")
        expected = users_cell(code_links(cells[1], s["map"], root)[0], index, s)
        if cells[3] != expected:
            ending = "\n" if lines[line].endswith("\n") else ""
            lines[line] = "| " + " | ".join(cells[:3] + [expected]) + " |" + ending
            changed += 1
    if changed:
        path.write_text("".join(lines))
    return changed


def main() -> int:
    root = Path(os.environ.get("DOCSITE_PROJECT_ROOT", Path.cwd())).resolve()
    try:
        changed = write(root)
    except LookupError as problem:
        print(problem)
        return 0
    except ValueError as problem:
        print(f"capability-map: error: {problem}", file=sys.stderr)
        return 1
    print(f"capability map: {changed} row(s) of Imported by rewritten" if changed else "capability map: Imported by is up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
