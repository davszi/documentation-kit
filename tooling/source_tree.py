"""Sidebar folder tree of the repository Markdown that a site renders.

Every registered source page appears at its repository path, beside the topic
entry pages, so a reader can browse records by folder. Topic pages link to
their existing route and carry a `page` badge; records link to their rendered
source page. The current page is marked and its ancestor folders start open;
native `<details>` keep the tree usable without JavaScript.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import html

TREE_LABEL = "Repository files"
TREE_LABEL_ID = "repo-tree-label"


@dataclass(frozen=True)
class TreeFile:
    path: str                # repository-relative POSIX path of the Markdown source
    route: str               # public file name, such as git.html
    title: str
    description: str | None
    page: bool               # a topic page written for people, not a rendered record


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


def _file_html(item: TreeFile, current: str) -> str:
    name = item.path.rsplit("/", 1)[-1]
    classes = "repo-tree-file" + (" is-page" if item.page else "") + (" current" if item.route == current else "")
    attrs = f' class="{classes}"' + (' aria-current="page"' if item.route == current else "")
    hint = item.title + (": " + item.description if item.description else "")
    badge = '<span class="repo-tree-badge">page</span>' if item.page else ""
    return (f'<li><a{attrs} href="{html.escape(item.route, quote=True)}" title="{html.escape(hint, quote=True)}">'
            f'<span class="repo-tree-name">{html.escape(name)}{badge}</span>'
            f'<span class="repo-tree-title">{html.escape(item.title)}</span></a></li>')


def _folder_html(folder: _Folder, current: str) -> str:
    items = []
    for name in sorted(folder.folders, key=str.casefold):
        child = folder.folders[name]
        opened, count = child.holds(current), child.count()
        items.append(f'<li class="repo-tree-folder{" has-current" if opened else ""}">'
                     f'<details{" open" if opened else ""}><summary>'
                     f'<span class="repo-tree-name">{html.escape(name)}/</span>'
                     f'<span class="repo-tree-count" title="{count} file{"" if count == 1 else "s"}">{count}</span>'
                     f'</summary>{_folder_html(child, current)}</details></li>')
    for item in sorted(folder.files, key=lambda entry: entry.path.casefold()):
        items.append(_file_html(item, current))
    return '<ul class="repo-tree-list">' + "".join(items) + "</ul>"


def tree_html(files: list[TreeFile], current: str) -> str:
    """The labelled tree for the page whose public file name is `current`; empty without files."""
    if not files:
        return ""
    return (f'    <div class="repo-tree" role="group" aria-labelledby="{TREE_LABEL_ID}">\n'
            f'    <span class="repo-tree-label" id="{TREE_LABEL_ID}">{TREE_LABEL}</span>\n'
            f'    {_folder_html(_folder_tree(files), current)}\n'
            f'    </div>')
