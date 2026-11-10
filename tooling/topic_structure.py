"""Topic folders pair a page with the record it explains.

Every `docs/topics/<topic>/` folder with an `index.md` page also holds at
least one record: another Markdown file in the folder or its subfolders,
outside `evidence/`. A page without a record declares why in its frontmatter
as `page_only = "<reason>"`. The site home page (`slug = "index"`) is exempt.

A project may keep topic folders one level deeper, inside a group folder named
in `topic_group_folders` in `docs/site/site.toml`:
`docs/topics/<group>/<topic>/index.md`. A nested topic counts like any other.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

GROUP_FOLDER_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def topic_group_folders(root: Path) -> tuple[str, ...]:
    """Folders under `docs/topics` that hold topic folders instead of being one.

    Read from `topic_group_folders` in `docs/site/site.toml`. Invalid values are
    skipped here; the build reports them.
    """
    try:
        site = tomllib.loads((Path(root) / "docs/site/site.toml").read_text())
    except (OSError, tomllib.TOMLDecodeError):
        return ()
    names = site.get("topic_group_folders", [])
    if not isinstance(names, list):
        return ()
    return tuple(name for name in names if isinstance(name, str) and GROUP_FOLDER_NAME.fullmatch(name))


def topic_pages(root: Path, groups: tuple[str, ...] | None = None) -> list[Path]:
    """Every topic page: `docs/topics/<topic>/index.md`, and one level deeper in a group folder."""
    topics = Path(root) / "docs/topics"
    groups = topic_group_folders(root) if groups is None else groups
    pages = [page for page in topics.glob("*/index.md") if page.parent.name not in groups]
    for group in groups:
        pages.extend((topics / group).glob("*/index.md"))
    return sorted(pages)


def is_topic_page(path: Path, root: Path, groups: tuple[str, ...] | None = None) -> bool:
    try:
        parts = Path(path).relative_to(Path(root) / "docs/topics").parts
    except ValueError:
        return False
    if not parts or parts[-1] != "index.md":
        return False
    groups = topic_group_folders(root) if groups is None else groups
    return (len(parts) == 2 and parts[0] not in groups) or (len(parts) == 3 and parts[0] in groups)


def undeclared_nested_pages(root: Path) -> list[str]:
    """Notes for pages two levels down whose parent folder is not a declared group folder.

    Such a page is not built. A folder that is itself a topic may hold any
    files, so only folders without their own page are reported.
    """
    root = Path(root)
    topics = root / "docs/topics"
    groups = topic_group_folders(root)
    notes = []
    for page in sorted(topics.glob("*/*/index.md")):
        group = page.parent.parent
        if group.name in groups or (group / "index.md").exists() or frontmatter(page) is None:
            continue
        notes.append(f'{page.relative_to(root).as_posix()}: page is not built; add "{group.name}" to '
                     f'topic_group_folders in docs/site/site.toml to build nested topics')
    return notes


def frontmatter(page: Path) -> dict | None:
    """The page's TOML frontmatter, or None when absent or invalid (the build reports it)."""
    text = page.read_text(errors="replace")
    if not text.startswith("+++\n"):
        return None
    end = text.find("\n+++\n", 4)
    if end < 0:
        return None
    try:
        return tomllib.loads(text[4:end])
    except tomllib.TOMLDecodeError:
        return None


def topic_records(folder: Path) -> list[Path]:
    page = folder / "index.md"
    return sorted(path for path in folder.rglob("*.md")
                  if path != page and path.is_file()
                  and "evidence" not in path.relative_to(folder).parts[:-1])


def topic_structure_problems(root: Path) -> tuple[list[str], list[str]]:
    """(errors, warnings) for topic folders without a record or with a misused page_only."""
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    for page in topic_pages(root):
        meta = frontmatter(page)
        if meta is None:
            continue
        folder = page.parent
        name = folder.relative_to(root).as_posix()
        declared = "page_only" in meta
        reason = meta.get("page_only")
        if declared and (not isinstance(reason, str) or not reason.strip()):
            errors.append(f"{page.relative_to(root).as_posix()}: page_only must be a non-empty reason string")
            continue
        if meta.get("slug") == "index":
            continue  # the site home page explains the site, not one record
        records = topic_records(folder)
        if records and declared:
            warnings.append(f"{name}: page_only is unnecessary; the folder holds the record "
                            f"{records[0].relative_to(root).as_posix()}")
        elif not records and not declared:
            warnings.append(f'{name}: page without a record; add {name}/{folder.name}.md '
                            f'or declare page_only = "<reason>" in its frontmatter')
    return errors, warnings
