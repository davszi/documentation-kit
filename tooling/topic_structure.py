"""Topic folders pair a page with the record it explains.

Every `docs/topics/<topic>/` folder with an `index.md` page also holds at
least one record: another Markdown file in the folder or its subfolders,
outside `evidence/`. A page without a record declares why in its frontmatter
as `page_only = "<reason>"`. The site home page (`slug = "index"`) is exempt.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


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
    for page in sorted((root / "docs/topics").glob("*/index.md")):
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
