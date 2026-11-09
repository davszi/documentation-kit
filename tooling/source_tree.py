"""Sidebar section listing the registered Markdown records of a site.

Pinned records come first as a short list of titles in their declared order.
Every record then appears at its repository path in a folder tree inside one
"Browse by folder" disclosure. The disclosure opens, unfolded to the current file,
only on a record page that is neither pinned nor listed in the navigation;
other pages keep it closed, because their entry already marks them. Native `<details>` keep the section usable without JavaScript.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import html

TREE_LABEL = "Reference"
TREE_LABEL_ID = "repo-tree-label"


@dataclass(frozen=True)
class TreeFile:
    path: str                # repository-relative POSIX path of the Markdown source
    route: str               # public file name, such as git.html
    title: str
    description: str | None
    pinned: bool


@dataclass
class _Folder:
    folders: dict[str, "_Folder"] = field(default_factory=dict)
    files: list[TreeFile] = field(default_factory=list)

    def count(self) -> int:
        return len(self.files) + sum(folder.count() for folder in self.folders.values())

    def holds(self, route: str) -> bool:
        return (any(item.route == route for item in self.files)
                or any(folder.holds(route) for folder in self.folders.values()))


def _folder_tree(files: list[TreeFile]) -> _Folder:
    root = _Folder()
    for item in files:
        folder = root
        for part in item.path.split("/")[:-1]:
            folder = folder.folders.setdefault(part, _Folder())
        folder.files.append(item)
    return root


def _hint(item: TreeFile, lead: str) -> str:
    return html.escape(lead + (": " + item.description if item.description else ""), quote=True)


def _count(count: int) -> str:
    return f'<span class="repo-tree-count" title="{count} file{"" if count == 1 else "s"}">{count}</span>'


def _file_html(item: TreeFile, current: str, listed: bool) -> str:
    """A tree leaf: file name with the title below. A current file that is
    pinned or listed in the navigation is announced there, so the leaf is
    only styled as current."""
    name = item.path.rsplit("/", 1)[-1]
    here = item.route == current
    attrs = ' class="repo-tree-file' + (' current"' if here else '"')
    if here and not item.pinned and not listed:
        attrs += ' aria-current="page"'
    return (f'<li><a{attrs} href="{html.escape(item.route, quote=True)}" title="{_hint(item, item.title)}">'
            f'<span class="repo-tree-name">{html.escape(name)}</span>'
            f'<span class="repo-tree-title">{html.escape(item.title)}</span></a></li>')


def _folder_html(folder: _Folder, current: str, listed: bool) -> str:
    items = []
    for name in sorted(folder.folders, key=str.casefold):
        child = folder.folders[name]
        opened = child.holds(current)
        items.append(f'<li class="repo-tree-folder{" has-current" if opened else ""}">'
                     f'<details{" open" if opened else ""}><summary>'
                     f'<span class="repo-tree-name">{html.escape(name)}/</span>{_count(child.count())}'
                     f'</summary>{_folder_html(child, current, listed)}</details></li>')
    for item in sorted(folder.files, key=lambda entry: entry.path.casefold()):
        items.append(_file_html(item, current, listed))
    return '<ul class="repo-tree-list">' + "".join(items) + "</ul>"


def _pinned_html(files: list[TreeFile], current: str) -> str:
    links = []
    for item in files:
        here = item.route == current
        attrs = ' class="repo-tree-pin current" aria-current="page"' if here else ' class="repo-tree-pin"'
        links.append(f'<li><a{attrs} href="{html.escape(item.route, quote=True)}" title="{_hint(item, item.path)}">'
                     f'{html.escape(item.title)}</a></li>')
    return '<ul class="repo-tree-pinned" aria-label="Pinned files">' + "".join(links) + "</ul>"


def tree_html(files: list[TreeFile], current: str, *, listed: bool = False) -> str:
    """The section for the page whose public file name is `current`; empty without files.
    `listed` says the page has a visible navigation entry."""
    if not files:
        return ""
    pinned = [item for item in files if item.pinned]
    opened = not listed and any(item.route == current and not item.pinned for item in files)
    return (f'    <div class="repo-tree" role="group" aria-labelledby="{TREE_LABEL_ID}">\n'
            f'    <span class="repo-tree-label" id="{TREE_LABEL_ID}">{TREE_LABEL}</span>\n'
            + (f'    {_pinned_html(pinned, current)}\n' if pinned else "")
            + f'    <details class="repo-tree-all"{" open" if opened else ""}><summary>'
            f'<span class="repo-tree-name">Browse by folder</span>{_count(len(files))}</summary>\n'
            f'    {_folder_html(_folder_tree(files), current, listed)}\n'
            f'    </details>\n'
            f'    </div>')
