"""Check that every formula on a project's built pages compiles.

`docsite.py lint` reads each built page that loads the kit's KaTeX, finds the
formulas the page's math renderer would find, and compiles them with the KaTeX
the kit ships, in `theme/assets/vendor/katex/katex.min.js`. A formula that does
not compile shows as raw text on the page, so each failure is an error that
names the page and the formula.

The formulas are found as the vendored auto-render finds them in a browser:
inside the element with the class `content`, in each run of adjacent text,
outside `pre`, `code`, `script` and `style`, between `$$` and `$$` (display)
or `\\(` and `\\)` (inline), with braces balanced. An opening delimiter whose
closing one is not in the same run of text stays raw on the page too: inside
the build's own formula wrappers (`span.math-inline`, `div.math`) that means
Markdown split the formula with markup, and anywhere else that the formula is
not closed. Both are errors.

KaTeX is JavaScript, and building a site needs no Node.js. Python finds the
formulas; one Node process, `tooling/formula_compile.cjs`, compiles them.
Node is `DOCS_NODE` when set, otherwise `node` on `PATH`. Without Node the
formulas are not compiled and lint prints a note, unless the project sets
`formula_check_required = true` in `docs/site/site.toml`; then it is an error,
so a check run without Node cannot pass silently.
"""

from __future__ import annotations

from html.parser import HTMLParser
import json
import os
from pathlib import Path
import shutil
import subprocess

KIT = Path(__file__).resolve().parents[1]
COMPILER = KIT / "tooling" / "formula_compile.cjs"
# The delimiters and ignored tags of the build's renderMathInElement call.
DELIMITERS = (("$$", "$$", True), ("\\(", "\\)", False))
# `noscript` and `template` are never shown while the renderer runs.
IGNORED_TAGS = {"pre", "code", "script", "style", "noscript", "template"}
WRAPPER_CLASSES = {"math-inline", "math"}
RENDERER = "assets/katex/contrib/auto-render.min.js"
SHOWN = 160  # characters of a formula shown in a message


def _end_of_math(right: str, text: str, start: int) -> int:
    """auto-render's findEndOfMath: the closing delimiter outside braces."""
    index, braces = start, 0
    while index < len(text):
        if braces <= 0 and text.startswith(right, index):
            return index
        if text[index] == "\\":
            index += 1
        elif text[index] == "{":
            braces += 1
        elif text[index] == "}":
            braces -= 1
        index += 1
    return -1


def split_at_delimiters(text: str) -> tuple[list[tuple[str, bool]], str | None]:
    """(formulas, unclosed) in one run of text, as auto-render splits it.

    Each formula is (TeX, display). `unclosed` is the rest of the text from an
    opening delimiter whose closing one does not follow, or None.
    """
    formulas = []
    while True:
        starts = [(text.find(left), left, right, display) for left, right, display in DELIMITERS]
        starts = [item for item in starts if item[0] >= 0]
        if not starts:
            return formulas, None
        index = min(item[0] for item in starts)
        # At one position the first listed delimiter wins, as in auto-render.
        _, left, right, display = next(item for item in starts if item[0] == index)
        text = text[index:]
        end = _end_of_math(right, text, len(left))
        if end < 0:
            return formulas, text
        formulas.append((text[len(left):end], display))
        text = text[end + len(right):]


class _Formulas(HTMLParser):
    """Collects the runs of text that the page's math renderer reads."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.content_tag: str | None = None
        self.content_depth = 0
        self.ignored = 0
        self.run: list[str] = []
        # [tag, depth, split, raw parts, unclosed runs] of an open formula wrapper
        self.wrapper: list = []
        self.formulas: list[tuple[str, bool]] = []
        self.unclosed: list[str] = []
        self.split: list[str] = []

    def _flush(self) -> None:
        text, self.run = "".join(self.run), []
        if not text:
            return
        formulas, unclosed = split_at_delimiters(text)
        self.formulas.extend(formulas)
        if unclosed is not None:
            # Inside a wrapper it is decided at the wrapper's end: split or not closed.
            (self.wrapper[4] if self.wrapper else self.unclosed).append(unclosed)

    def handle_starttag(self, tag, attrs):
        self._flush()
        classes = set((dict(attrs).get("class") or "").split())
        if self.content_tag is None:
            if "content" in classes:
                self.content_tag, self.content_depth = tag, 1
            return
        if tag == self.content_tag:
            self.content_depth += 1
        if self.wrapper:
            if tag == self.wrapper[0]:
                self.wrapper[1] += 1
            self.wrapper[2] = True
            self.wrapper[3].append(self.get_starttag_text() or "")
        elif not self.ignored and classes & WRAPPER_CLASSES:
            self.wrapper = [tag, 1, False, [], []]
        if tag in IGNORED_TAGS:
            self.ignored += 1

    def handle_startendtag(self, tag, attrs):
        self._flush()
        if self.wrapper:
            self.wrapper[2] = True
            self.wrapper[3].append(self.get_starttag_text() or "")

    def handle_endtag(self, tag):
        self._flush()
        if self.content_tag is None or self.content_depth == 0:
            return
        if tag in IGNORED_TAGS and self.ignored:
            self.ignored -= 1
        if self.wrapper:
            if tag == self.wrapper[0]:
                self.wrapper[1] -= 1
            if self.wrapper[1] == 0:
                if self.wrapper[2]:
                    self.split.append("".join(self.wrapper[3]))
                else:
                    self.unclosed.extend(self.wrapper[4])
                self.wrapper = []
            else:
                self.wrapper[3].append(f"</{tag}>")
        if tag == self.content_tag:
            self.content_depth -= 1

    def handle_data(self, data):
        if self.content_tag is None or self.content_depth == 0:
            return
        if self.wrapper:
            self.wrapper[3].append(data)
        if not self.ignored:
            self.run.append(data)

    def handle_comment(self, data):
        self._flush()

    def close(self):
        super().close()
        self._flush()


def page_formulas(markup: str) -> tuple[list[tuple[str, bool]], list[str], list[str]]:
    """(formulas, split, unclosed) of one built page.

    `formulas` holds (TeX, display) pairs; `split` the text of each formula
    wrapper that Markdown split with markup; `unclosed` the text from each
    opening delimiter outside a wrapper that does not close in its run.
    """
    parser = _Formulas()
    parser.feed(markup)
    parser.close()
    return parser.formulas, parser.split, parser.unclosed


def renders_math(markup: str) -> bool:
    """Whether the page loads the kit's math renderer."""
    return RENDERER in markup


def find_node() -> str | None:
    """The Node.js to run: `DOCS_NODE` when set, otherwise `node` on PATH.

    A `DOCS_NODE` that names no executable raises ValueError: the person asked
    for that Node, so the check does not quietly fall back or skip.
    """
    configured = os.environ.get("DOCS_NODE")
    if configured:
        found = shutil.which(configured)
        if found is None:
            raise ValueError(f"DOCS_NODE names no executable: {configured}")
        return found
    return shutil.which("node")


def required(site: dict) -> bool:
    """`formula_check_required = true`: lint fails when Node.js is missing."""
    return site.get("formula_check_required") is True


def compile_formulas(node: str, formulas: list[tuple[str, bool]]) -> tuple[str, list[str | None]]:
    """(KaTeX version, one KaTeX error message or None per formula)."""
    payload = json.dumps([{"tex": tex, "display": display} for tex, display in formulas])
    result = subprocess.run([node, str(COMPILER)], input=payload, capture_output=True,
                            text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"{COMPILER.name} exited with {result.returncode}")
    answer = json.loads(result.stdout)
    if len(answer.get("results", ())) != len(formulas):
        raise RuntimeError(f"{COMPILER.name} answered {len(answer.get('results', ()))} of {len(formulas)} formulas")
    return answer["katex"], answer["results"]


def _shown(text: str) -> str:
    text = " ".join(text.split())
    return text if len(text) <= SHOWN else text[:SHOWN - 1] + "…"


def _written(tex: str, display: bool) -> str:
    return _shown(f"$${tex}$$" if display else f"\\({tex}\\)")


def check(root: Path, site: dict, html_dir: Path, names: dict[str, str],
          find=find_node) -> tuple[list[str], list[str], str | None]:
    """(errors, notes, summary) for the built pages in `html_dir`.

    `names` maps a built page to its source, as `topic_structure.page_sources`
    gives it. `find` returns the Node.js to run, or None when there is none.
    """
    errors: list[str] = []
    notes: list[str] = []
    found: list[tuple[str, str, bool]] = []
    pages = 0
    for path in sorted(Path(html_dir).glob("*.html")):
        markup = path.read_text(errors="replace")
        if not renders_math(markup):
            continue
        source = names.get(path.name)
        label = f"{source} ({path.name})" if source else path.name
        formulas, split, unclosed = page_formulas(markup)
        pages += 1
        for text in split:
            errors.append(f"{label}: formula split by Markdown: {_shown(text)}")
        for text in unclosed:
            errors.append(f"{label}: formula not closed in the same text: {_shown(text)}")
        found.extend((label, tex, display) for tex, display in formulas)
    if not pages:
        return errors, notes, None
    try:
        node = find()
    except ValueError as problem:
        errors.append(f"formula check could not run: {problem}")
        return errors, notes, None
    if node is None:
        message = (f"formula check skipped: Node.js was not found (set DOCS_NODE or put node on PATH); "
                   f"{len(found)} formula(s) on {pages} page(s) were not compiled")
        if required(site):
            errors.append(message + "; docs/site/site.toml sets formula_check_required = true")
        else:
            notes.append(message)
        return errors, notes, None
    try:
        version, results = compile_formulas(node, [(tex, display) for _, tex, display in found])
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as problem:
        errors.append(f"formula check could not run {COMPILER.relative_to(KIT)} with {node}: {problem}")
        return errors, notes, None
    failed = 0
    for (label, tex, display), problem in zip(found, results):
        if problem is not None:
            failed += 1
            errors.append(f"{label}: formula does not compile: {_written(tex, display)} — {_shown(problem)}")
    summary = (f"formula check: {len(found) - failed} of {len(found)} formula(s) on {pages} page(s) "
               f"compile with KaTeX {version}")
    return errors, notes, summary
