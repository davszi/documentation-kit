"""Adapt existing document sections to the shared reader without editing sources.

Only presentation wrappers and section-anchor ownership change. Original text,
tables, figures, controls and links remain in the same order within each chapter.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import html
from html.parser import HTMLParser
import re


@dataclass
class Element:
    tag: str
    attrs: dict
    start: int
    opening_end: int
    closing_start: int = 0
    end: int = 0
    children: list["Element"] = field(default_factory=list)

    def descendants(self):
        yield self
        for child in self.children:
            yield from child.descendants()


class Structure(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.roots, self.stack = text, [], []
        self.offsets = [0]
        for line in text.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.feed(text)
        self.close()
        if self.stack:
            raise ValueError("Unclosed document element: " + self.stack[-1].tag)

    def source_position(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.source_position()
        node = Element(tag, dict(attrs), start, start + len(self.get_starttag_text()))
        (self.stack[-1].children if self.stack else self.roots).append(node)
        if tag in self.VOID:
            node.closing_start = node.end = node.opening_end
        else:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            node = self.stack.pop()
            node.closing_start = node.end = node.opening_end

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1].tag != tag:
            raise ValueError("Mismatched document closing tag: " + tag)
        node = self.stack.pop()
        node.closing_start = self.source_position()
        node.end = self.text.index(">", node.closing_start) + 1


def label(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def adapt_sections(content: str, toc: list, *, group: str | None = None, reserved_ids: set | None = None):
    """Return wrapped chapters, generated TOC entries and the original page title."""
    structure = Structure(content)
    roots = structure.roots
    # Some legacy pages have a single styling host around the whole document.
    # Retain it as a display-contents host; neither its selectors nor content move.
    if len(roots) == 1 and roots[0].tag in {"div", "article"}:
        host = roots[0]
        inside, entries, title = adapt_sections(
            content[host.opening_end:host.closing_start], toc, group=group, reserved_ids=reserved_ids)
        opening = content[host.start:host.opening_end]
        opening = opening[:-1] + ' data-reader-host="">'
        return opening + inside + content[host.closing_start:host.end], entries, title

    main = {href[1:]: text for text, href in toc
            if not text.startswith("-") and href.startswith("#") and href != "#top"}
    has_flat_headings = any(node.tag == "h2" for node in roots)
    boundaries = []
    for root in roots:
        nodes = list(root.descendants())
        anchor = next((node for node in nodes if node.attrs.get("id") in main), None)
        is_card = root.tag == "section" and "card" in root.attrs.get("class", "").split()
        if root.tag == "h2" or is_card and (not has_flat_headings or anchor):
            heading = next((node for node in nodes if node.tag in {"h2", "h3"}), None)
            anchor = anchor or (root if root.attrs.get("id") else heading)
            if anchor is None or not anchor.attrs.get("id"):
                raise ValueError("A chapter needs a section or heading anchor")
            identifier = anchor.attrs["id"]
            title = main.get(identifier)
            if title is None:
                title = label(content[heading.opening_end:heading.closing_start]) if heading else identifier
            boundaries.append((root.start, anchor, title))

    title_node = next((node for node in roots if node.tag == "h1"), None)
    page_title = content[title_node.start:title_node.end] if title_node else ""
    first = boundaries[0][0] if boundaries else len(content)
    introduction = content[:first]
    if title_node:
        introduction = introduction[:title_node.start] + introduction[title_node.end:]
    existing_ids = {node.attrs["id"] for root in roots for node in root.descendants()
                    if node.attrs.get("id")}
    existing_ids.update(reserved_ids or ())
    intro_id = "reader-introduction"
    while intro_id in existing_ids:
        intro_id += "-intro"
    chapters, entries = [], []

    def wrap(identifier, title, body):
        nonlocal group
        attrs = f' id="{html.escape(identifier, quote=True)}" data-reader-chapter=""'
        if group:
            attrs += f' data-reader-group="{html.escape(group, quote=True)}"'
            group = None  # A group heading appears once in the navigation rail.
        chapters.append('<section class="card reader-adapted"' + attrs + '>\n' + body + '\n</section>\n')
        entries.append([title, "#" + identifier])

    # An introduction stays a first-class chapter, not hidden in About. Only
    # the redundant page-title heading moves into About beside the shared header.
    meaningful = re.sub(r"<!--[\s\S]*?-->", "", introduction).strip()
    if meaningful:
        intro_label = next((text for text, href in toc if href == "#top"), "Introduction")
        wrap(intro_id, intro_label,
             '<h2 data-reader-generated="">' + html.escape(intro_label) + '</h2>\n' + introduction)
    else:
        chapters.append(introduction)
    for i, (start, anchor, title) in enumerate(boundaries):
        end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(content)
        body = content[start:end]
        # Transfer the original public anchor to its containing chapter. Keep
        # the inner element, heading, all other attributes and relative paths.
        aliases = [node for root in roots for node in root.descendants()
                   if start <= node.start < end and node.attrs.get("id") == anchor.attrs["id"]]
        for node in reversed(aliases):
            a, b = node.start - start, node.opening_end - start
            opening = re.sub(r'\s+id=("[^"]*"|\x27[^\x27]*\x27)', "", body[a:b], count=1)
            body = body[:a] + opening + body[b:]
        wrap(anchor.attrs["id"], title, body)
    if not entries:
        raise ValueError("No readable chapters found")
    return "".join(chapters), entries, page_title


def reader_page(chunks: list[tuple[str | None, str]], toc: list, title: str, toolbar: str):
    sections, entries, titles = [], [], []
    reserved = {identifier for _, content in chunks for identifier in re.findall(r'\bid="([^"]+)"', content)}
    for group, content in chunks:
        if not content.strip():
            continue
        markup, links, heading = adapt_sections(content, toc, group=group, reserved_ids=reserved)
        reserved.update(href[1:] for _, href in links)
        sections.append(markup)
        entries.extend(links)
        if heading:
            titles.append(heading)
    public = {href for _, href in entries}
    # Keep subchapter navigation and any legacy aliases alongside generated
    # chapter links. The controller puts each under its containing chapter.
    entries.extend([text if text.startswith("-") else "-" + text, href]
                   for text, href in toc if href not in public and href != "#top")
    overview = ('<details class="topic-overview" open>\n'
                '<summary data-reader-generated="">' + html.escape(title) + ' · About this page</summary>\n'
                + "\n".join(titles) + '\n</details>\n')
    config = '<div hidden data-reader-adapted="" data-reader-title="' + html.escape(title, quote=True) + '"></div>\n'
    return config + overview + toolbar + "\n".join(sections), entries
