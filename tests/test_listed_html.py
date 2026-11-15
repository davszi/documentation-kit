"""Raw HTML in automatically listed files: the allowlist, addresses, the kit's ids
and the payloads of the three reviews that broke the earlier filter."""
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / 'fixtures'
sys.path.insert(0, str(KIT / 'tooling'))

from build import render_listed_file  # noqa: E402
from source_pages import ADMITTED_HTML, KIT_IDS, browser_address  # noqa: E402
from source_tree import TREE_LABEL_ID  # noqa: E402

GONE = '<span class="link-gone" title="The target of this link no longer exists.">'
PNG = b'\x89PNG\r\n\x1a\nfixture'
# Elements that load, run, embed or enclose content; none may come from a listed file.
LOADING = {'applet', 'audio', 'base', 'button', 'embed', 'form', 'frame', 'frameset', 'iframe', 'image', 'input',
           'link', 'math', 'meta', 'noscript', 'object', 'picture', 'portal', 'script', 'source', 'style', 'svg',
           'template', 'textarea', 'track', 'video'}
LOADING_ATTRIBUTES = {'action', 'attributionsrc', 'background', 'data', 'dynsrc', 'formaction', 'longdesc', 'lowsrc',
                      'ping', 'poster', 'srcdoc', 'srcset', 'xlink:href'}

# The payloads of the three reviews of the earlier filter.
REVIEW_1 = """# Review 1

<p><img src="media/kept.png" alt="kept" onerror="alert(1)"></p>
<div onmouseover=alert(2)>hover</div>
<details ontoggle="alert(3)" open><summary>s</summary>x</details>
<p><a href=javascript:alert(4)>bare script link</a> <a href="java&#x09;script:alert(5)">tab</a></p>
<p><img src='https://example.com/single.png' alt='single'></p>
<p><img src=https://example.com/bare.png alt=bare></p>
<p><img srcset="https://example.com/set.png 2x" src="media/kept.png" alt="set"></p>
<svg><image href="https://example.com/svg.png"/></svg>
<p><image src="https://example.com/image.png"></p>
<video poster='https://example.com/poster.png'></video>

![protocol-relative](//example.com/relative.png)

<p><a href="https://example.com/ok" ping="https://example.com/ping">kept link</a></p>
"""
REVIEW_2 = """# Review 2

<p style="background:url('https://example.com/style.png')">styled</p>
<div style="background:u\\72l(https://example.com/escaped.png)">escaped</div>
"""
REVIEW_3 = """# Review 3

Text before.

<div class="toc"><div class="repo-tree" data-repo-tree-src="http://127.0.0.1:8999/evil.js" data-repo-tree-current="x"><details class="repo-tree-all"><summary>tree</summary></details></div></div>

Text after.

<video id="m5" poster=" //127.0.0.1:8999/m5"></video>
<img src=" //127.0.0.1:8999/b2-space" alt="space">
<img src="/\t/127.0.0.1:8999/b2-tab" alt="tab">
<img src="
//127.0.0.1:8999/b2-newline" alt="newline">
<img src="&#9;//127.0.0.1:8999/b2-entity" alt="entity">
<img src="\\\\127.0.0.1:8999/b2-backslash" alt="backslash">
<a href=" //127.0.0.1:8999/b2-link">link</a>
"""
EVIL_SVG = ('<svg xmlns="http://www.w3.org/2000/svg"><script>window.__mediaRan = "svg"</script>'
            '<rect width="9" height="9"/></svg>\n')
EVIL_HTML = '<!doctype html><title>x</title><script>window.__mediaRan = "html"</script>\n'
TYPES = """# Types

<img src="media/evil.svg" alt="svg-html"> <img src="media/evil.html" alt="html-html"> <img src="media/fake.png" alt="fake-png"> <img src="media/kept.png" alt="png-html"> <img src="media/upper.PNG" alt="upper">

![svg-md](media/evil.svg) ![html-md](media/evil.html) ![png-md](media/kept.png)

<img src="data:text/html,&lt;script&gt;alert(1)&lt;/script&gt;" alt="data-html"> <img src="data:image/svg+xml,&lt;svg/&gt;" alt="data-svg"> <img src="data:image/png;base64,iVBORw0KGgo=" alt="data-png">
"""


def invoke(*args):
    env = {name: value for name, value in os.environ.items() if name not in {'GITHUB_SHA', 'DOCSITE_PROJECT_ROOT'}}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True, env=env)


def git(root, *args):
    subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', *args],
                   cwd=root, check=True, capture_output=True)


class Elements(HTMLParser):
    """Start tags with their attributes, in order."""

    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.elements.append((tag, attrs))


def content(page):
    """A built page's content below the source line, where the file's HTML lands."""
    return page[page.index('<p class="source-origin"'):page.index('</main>')]


def unsafe(page):
    """Everything in a built page's content that could run script, load from outside
    the bundle, drive a kit component or stand in for a part of the kit."""
    found = []
    for tag, attributes in Elements(content(page)).elements:
        if tag in LOADING:
            found.append(f'<{tag}>')
        for name, value in attributes:
            value = value or ''
            if name.startswith('on') or name in LOADING_ATTRIBUTES or name.startswith('data-repo-tree'):
                found.append(f'{tag} {name}')
            elif name == 'style' and not re.fullmatch(r'counter-reset: ln \d+', value):
                found.append(f'{tag} style={value}')
            elif name == 'class' and {'toc', 'repo-tree', 'repo-tree-all', 'sidebar', 'nav-fold'} & set(value.split()):
                found.append(f'{tag} class={value}')
            elif name == 'src' and not (re.fullmatch(r'_media/[^?#]+\.(?:png|jpe?g|gif|webp|avif)', value, re.I)
                                        or re.match(r'data:image/(?:png|jpeg|gif|webp|avif)[;,]', value)):
                found.append(f'{tag} src={value}')
            elif name == 'href':
                _, scheme, other_host = browser_address(value)
                if other_host or scheme not in {None, 'http', 'https', 'mailto', 'vscode'}:
                    found.append(f'{tag} href={value}')
            elif name in {'id', 'name'} and value.lower() in KIT_IDS:
                found.append(f'{tag} {name}={value}')
    return found


def nests(page):
    """Whether every end tag of a built page closes the element opened last."""
    stack = []
    for match in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*>', page):
        name = match[2].lower()
        if name in {'br', 'hr', 'img', 'meta', 'link', 'input', 'source', 'wbr', 'col'}:
            continue
        if not match[1]:
            stack.append(name)
        elif not stack or stack.pop() != name:
            return False
    return stack == []


class Allowlist(unittest.TestCase):
    def test_the_fixture_renders_as_expected(self):
        source = (FIXTURES / 'listed-html-allowlist.md').read_text()
        rendered, notes = render_listed_file(source, 'fixture.md')
        self.assertEqual(rendered, (FIXTURES / 'listed-html-allowlist.html').read_text())
        self.assertEqual(notes, [
            'fixture.md: 42 raw HTML tag(s) outside the allowlist shown as text: audio (2), base, button (2), '
            'center (2), embed, font (2), form (2), iframe (2), image, input, link, math (2), meta, mi (2), '
            'noscript (2), object (2), picture (2), script (2), source, style (2), svg (2), template (2), '
            'textarea (2), use, video (2)',
            'fixture.md: 33 raw HTML attribute(s) outside the allowlist removed: aria-label, background, cite, '
            'class, crossorigin, data-…, dir, download, formaction, hidden, href, ismap, lang, loading, longdesc, '
            'lowsrc, on… (3), ping, poster, referrerpolicy (2), rel, role, src, srcset, style, tabindex, target, '
            'type, usemap, xlink:href',
        ])

    def test_the_fixture_shows_every_admitted_tag_and_attribute_and_nothing_else(self):
        expected = (FIXTURES / 'listed-html-allowlist.html').read_text()
        admitted = expected[expected.index('<div id="d"'):expected.index('<p>Tags outside')]
        seen = {(tag, name) for tag, attributes in Elements(admitted).elements for name, _ in attributes}
        tags = {tag for tag, _ in Elements(admitted).elements}
        self.assertEqual(tags, set(ADMITTED_HTML))
        self.assertEqual(seen, {(tag, name) for tag, names in ADMITTED_HTML.items() for name in names})
        rest = expected[expected.index('<p>Tags outside'):]
        self.assertEqual({tag for tag, _ in Elements(rest).elements}, {'p', 'img', 'a', 'blockquote', 'td', 'details'})
        self.assertEqual({name for _, attributes in Elements(rest).elements for name, _ in attributes},
                         {'src', 'href', 'open'})


class Addresses(unittest.TestCase):
    def test_an_address_is_read_as_browsers_read_it(self):
        cases = {
            ' //h/x': ('//h/x', None, True),
            '/\t/h/x': ('//h/x', None, True),
            '\n//h/x': ('//h/x', None, True),
            '\\\\h/x': ('\\\\h/x', None, True),
            '/\\h/x': ('/\\h/x', None, True),
            '\\/h/x': ('\\/h/x', None, True),
            '\x00\x1f https://h/ \x0b': ('https://h/', 'https', False),
            'JaVa\tScRi\npt:alert(1)': ('JaVaScRipt:alert(1)', 'javascript', False),
            'java script:alert(1)': ('java script:alert(1)', None, False),
            '\ufffdjavascript:x': ('\ufffdjavascript:x', None, False),
            '/x': ('/x', None, False),
            '#x': ('#x', None, False),
            '': ('', None, False),
            'a/b.md': ('a/b.md', None, False),
            'C:\\x': ('C:\\x', 'c', False),
        }
        for value, expected in cases.items():
            self.assertEqual(browser_address(value), expected, repr(value))


class KitIds(unittest.TestCase):
    def test_kit_ids_cover_the_ids_the_shell_and_components_use(self):
        used = {TREE_LABEL_ID}
        components = KIT / 'theme/components'
        for path in components.glob('*.html'):
            used |= set(re.findall(r'\bid="([A-Za-z][\w-]*)"', path.read_text()))
        # Globals the kit's scripts define or read by name, which an element's id would define first.
        globals_ = set()
        python = {path: path.read_text() for path in (KIT / 'tooling').glob('*.py')}
        constants = dict(re.findall(r'^([A-Z_]+)\s*=\s*[\'"]([^\'"]+)[\'"]', '\n'.join(python.values()), re.M))
        for text in python.values():
            globals_ |= {constants[name] for name in re.findall(r'window\.\{([A-Z_]+)\}\s*=', text)}
        for path in components.glob('*.js'):
            text = path.read_text()
            used |= set(re.findall(r'getElementById\(\s*[\'"]([^\'"]+)[\'"]', text))
            used |= set(re.findall(r'\.id\s*=\s*[\'"]([^\'"]+)[\'"]', text))
            named = dict(re.findall(r'\bvar\s+([A-Z_]+)\s*=\s*[\'"]([^\'"]+)[\'"]', text))
            globals_ |= {named.get(name, name) for name in re.findall(r'window\[\s*([A-Z_]+)\s*\]', text)}
            globals_ |= set(re.findall(r'window\.([A-Za-z_$][\w$]*)\s*=(?!=)', text))
        self.assertTrue({'docsReferenceTree', 'docsLockedReferenceTree', 'figToggles'} <= globals_, globals_)
        missing = {name for name in used | globals_ if name.lower() not in KIT_IDS}
        self.assertEqual(missing, set())

    def test_a_kit_id_or_name_is_removed_in_any_case(self):
        rendered, notes = render_listed_file(
            '# Menu\n\n## TOC\n\n## Kept {#Sidebar}\n\n<a id="SideBar" name="docsReferenceTree">a</a> '
            '<span id="module">m</span> <a id="own" name="anchor">b</a>\n', 'n.md')
        self.assertEqual(rendered, '<h1>Menu</h1>\n<h2>TOC</h2>\n<h2>Kept</h2>\n'
                                   '<p><a>a</a> <span>m</span> <a id="own" name="anchor">b</a></p>\n')
        self.assertEqual(notes, ["n.md: 6 id or name value(s) of the kit's page removed: "
                                 'SideBar, Sidebar, docsReferenceTree, menu, module, toc'])


class Structure(unittest.TestCase):
    def test_the_file_cannot_close_what_it_did_not_open(self):
        rendered, notes = render_listed_file(
            '- <div>\n  item\n\n</div></div>\n\n</div></main><div><b>out</b> </td></table>\n\n<p><b><i>left open', 'n.md')
        self.assertEqual(rendered, '<ul>\n<li><div>\nitem\n\n</div></li>\n</ul>\n\n\n'
                                   '&lt;/main&gt;<div><b>out</b> \n\n<p><b><i>left open\n\n</i></b></p></div>')
        self.assertIn('n.md: 5 raw HTML end tag(s) that close nothing the file opened removed', notes)

    def test_a_link_ends_with_the_html_block_that_opened_it(self):
        rendered, notes = render_listed_file('<div><a href="https://x">\n\nSome *Markdown*.\n\n[link](y)\n\n</div>\n',
                                             'n.md')
        self.assertEqual(rendered, '<div><a href="https://x">\n</a>\n<p>Some <em>Markdown</em>.</p>\n'
                                   '<p><a href="y">link</a></p>\n</div>\n\n')
        self.assertEqual(notes, [])

    def test_links_do_not_nest(self):
        rendered, notes = render_listed_file('[<a href="x">in</a>](y) <a href="a">a<a href="b">b</a>c</a>\n', 'n.md')
        self.assertEqual(rendered, '<p><a href="y">in</a> <a href="a">ab</a>c</p>\n')
        self.assertIn('n.md: 2 raw HTML link(s) inside another link removed', notes)

    def test_comments_and_text_never_become_markup(self):
        rendered, notes = render_listed_file(
            'a <!-- c --> b\n\n<!-- --!> <img src=x onerror=alert(1)> -->\n\n<?php ?> <!DOCTYPE html> <![CDATA[x]]>'
            '\n\ntext\x00 <\x00div>\n\n<div title="&quot;&gt;&lt;script&gt;">t</div>\n\n<!-- open', 'n.md')
        self.assertNotIn('<script', rendered)
        self.assertNotIn('<img', rendered)
        self.assertNotIn('\x00', rendered)
        self.assertIn('<div title="&quot;&gt;&lt;script&gt;">t</div>', rendered)
        self.assertIn('&lt;!-- open', rendered)
        self.assertIn('n.md: unclosed HTML comment shown as text', notes)

    def test_image_text_cannot_leave_its_alt_value(self):
        rendered, _ = render_listed_file(
            '![x <foo title=\'" onerror="alert(1)\'> <b title=\'" onerror="alert(2)\'>b</b>](p.png)\n', 'n.md')
        (tag, attributes), = Elements(rendered).elements[1:]
        self.assertEqual(tag, 'img')
        self.assertEqual([name for name, _ in attributes], ['src', 'alt'])


class Built(unittest.TestCase):
    """The three reviews' payloads and further attempts, built once in a starter project."""

    @classmethod
    def setUpClass(cls):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-listed-html-')
        cls.addClassCleanup(folder.cleanup)
        cls.root = Path(folder.name)
        git(cls.root, 'init', '-q')
        assert invoke('init', cls.root).returncode == 0
        files = {'notes/review1.md': REVIEW_1, 'notes/review2.md': REVIEW_2, 'notes/review3.md': REVIEW_3,
                 'notes/attempts.md': (FIXTURES / 'listed-html-attempts.md').read_text(),
                 'notes/end-div.md': '# End\n\ntext\n\n<div',
                 'notes/end-quote.md': '# End\n\n<img src="//h.test/end',
                 'notes/end-link.md': '# End\n\n<a href="https://example.com/">open link\n',
                 'docs/notes/figure.md': '# Figure\n\n![drawing](../figures/drawing.svg)\n',
                 'docs/figures/manifest.json': '{"drawing.svg": {}}\n',
                 'notes/upper.md': '# Upper\n\nA [link](HTTP://example.com/) with its scheme in capitals.\n',
                 'notes/types.md': TYPES,
                 'notes/placeholders.md': '# Title {{CONTENT}} {{SCRIPTS}}\n\nText {{SCRIPTS}} {{CONTENT}} {{TOC}} '
                                          '{{CROSSNAV}} {{HEAD_EXTRA}} {{TITLE}}.\n'}
        for name, text in files.items():
            path = cls.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        (cls.root / 'notes/media').mkdir()
        (cls.root / 'notes/media/kept.png').write_bytes(PNG)
        (cls.root / 'notes/media/upper.PNG').write_bytes(PNG)
        (cls.root / 'notes/media/evil.svg').write_text(EVIL_SVG)
        (cls.root / 'notes/media/evil.html').write_text(EVIL_HTML)
        (cls.root / 'notes/media/fake.png').write_text(EVIL_HTML)  # a page under an image name
        (cls.root / 'docs/figures/drawing.svg').write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><script>alert(2)</script></svg>\n')
        config = cls.root / 'docs/site/site.toml'
        config.write_text(config.read_text().replace('# reference_roots = ["docs"]', 'reference_roots = ["docs", "notes"]')
                          + '\n[[source_pages]]\nsource = "notes/upper.md"\nslug = "upper"\n'
                          '\n[publication]\npages = ["guide.html"]\n')
        git(cls.root, 'add', '-A')
        cls.build = invoke('build', '--project', cls.root)
        cls.lint = invoke('lint', '--project', cls.root, '--strict')
        cls.published = cls.root / '_site'
        cls.publish = invoke('publish', '--project', cls.root, '--out', cls.published)

    def page(self, route):
        return (self.root / '.build/docs/html' / route).read_text()

    def test_build_strict_lint_and_publish_pass(self):
        self.assertEqual(self.build.returncode, 0, self.build.stderr)
        self.assertEqual(self.lint.returncode, 0, self.lint.stdout + self.lint.stderr)
        self.assertEqual(self.publish.returncode, 0, self.publish.stdout + self.publish.stderr)

    def test_no_page_runs_script_or_loads_from_outside(self):
        routes = ['notes.review1.md.html', 'notes.review2.md.html', 'notes.review3.md.html',
                  'notes.attempts.md.html', 'notes.end-div.md.html', 'notes.end-quote.md.html',
                  'notes.end-link.md.html', 'docs.notes.figure.md.html', 'notes.types.md.html',
                  'notes.placeholders.md.html']
        for route in routes:
            page = self.page(route)
            self.assertEqual(unsafe(page), [], route)
            self.assertTrue(nests(page), route)

    def test_review_1_handlers_script_links_and_loading_attributes(self):
        body = content(self.page('notes.review1.md.html'))
        self.assertIn('<p><img src="_media/notes/media/kept.png" alt="kept"></p>', body)
        self.assertIn('<div>hover</div>', body)
        self.assertIn('<details open><summary>s</summary>x</details>', body)
        self.assertIn(GONE + 'bare script link</span>', body)
        self.assertIn(GONE + 'tab</span>', body)
        self.assertIn('<a href="https://example.com/single.png">single</a>', body)
        self.assertIn('<a href="https://example.com/bare.png">bare</a>', body)
        self.assertIn('<img src="_media/notes/media/kept.png" alt="set">', body)
        self.assertIn('&lt;svg&gt;&lt;image href=&quot;https://example.com/svg.png&quot;/&gt;&lt;/svg&gt;', body)
        self.assertIn('&lt;video poster=&#x27;https://example.com/poster.png&#x27;&gt;', body)
        self.assertIn('<a href="https://example.com/ok">kept link</a>', body)

    def test_review_2_styles(self):
        body = content(self.page('notes.review2.md.html'))
        self.assertIn('<p>styled</p>', body)
        self.assertIn('<div>escaped</div>', body)
        self.assertNotIn('style=', body)
        self.assertNotIn('escaped.png', body)

    def test_review_3_tree_gadget_and_addresses_with_spaces(self):
        page = self.page('notes.review3.md.html')
        body = content(page)
        # B1: the gadget keeps its structure but none of the attributes that drive nav.js.
        self.assertIn('<div><div><details><summary>tree</summary></details></div></div>', body)
        self.assertNotIn('repo-tree-src', body)
        self.assertEqual(page.count('data-repo-tree-src'), 0)  # the inline tree has none either
        # B2: no form loads; each image becomes a link, the video shows as text.
        self.assertIn('&lt;video id=&quot;m5&quot; poster=&quot; //127.0.0.1:8999/m5&quot;&gt;', body)
        for name, text in (('space', 'space'), ('tab', 'tab'), ('newline', 'newline'), ('entity', 'entity'),
                           ('backslash', 'backslash'), ('link', 'link')):
            self.assertIn(f'<a href="https://127.0.0.1:8999/b2-{name}">{text}</a>', body)
        self.assertEqual(re.findall(r'src="[^"]*8999', page), [])

    def test_notes_name_what_was_not_admitted(self):
        out = self.lint.stdout
        for expected in (
                'notes/review1.md: 6 raw HTML tag(s) outside the allowlist shown as text: image (2), svg (2), '
                'video (2)',
                'notes/review1.md: 5 raw HTML attribute(s) outside the allowlist removed: on… (3), ping, srcset',
                'notes/review2.md: 2 raw HTML attribute(s) outside the allowlist removed: style (2)',
                'notes/review3.md: 5 raw HTML attribute(s) outside the allowlist removed: class (3), data-… (2)',
                'notes/review3.md: external media is not loaded; shown as a link:  //127.0.0.1:8999/b2-space',
                'notes/review3.md: external media is not loaded; shown as a link: /\\x09/127.0.0.1:8999/b2-tab',
                'notes/review3.md: external media is not loaded; shown as a link: \\x0a//127.0.0.1:8999/b2-newline',
        ):
            self.assertIn('NOTE: reference page ' + expected, out)

    def test_the_end_of_a_file_closes_what_it_left_open(self):
        self.assertIn('<p>text</p>\n&lt;div', content(self.page('notes.end-div.md.html')))
        self.assertIn('<p>&lt;img src=&quot;//h.test/end</p>', content(self.page('notes.end-quote.md.html')))
        self.assertIn('<p><a href="https://example.com/">open link</a></p>', content(self.page('notes.end-link.md.html')))

    def test_lint_reads_a_scheme_in_any_case(self):
        # A registered page keeps the capitals; lint skips the link as external.
        self.assertIn('<a href="HTTP://example.com/">link</a>', self.page('upper.html'))
        self.assertNotIn('dead relative href', self.lint.stdout + self.lint.stderr)

    def test_a_listed_file_shows_no_svg_figure(self):
        body = content(self.page('docs.notes.figure.md.html'))
        self.assertIn(GONE + 'drawing</span>', body)
        self.assertNotIn('<svg', body)
        self.assertNotIn('<img', body)

    def test_only_raster_images_are_shown_and_published(self):
        body = content(self.page('notes.types.md.html'))
        for name in ('svg-html', 'html-html', 'fake-png', 'svg-md', 'html-md', 'data-html', 'data-svg'):
            self.assertIn(GONE + name + '</span>', body, name)
        self.assertIn('<img src="_media/notes/media/kept.png" alt="png-html">', body)
        self.assertIn('<img src="_media/notes/media/upper.PNG" alt="upper">', body)
        self.assertIn('<img src="_media/notes/media/kept.png" alt="png-md" />', body)
        self.assertIn('<img src="data:image/png;base64,iVBORw0KGgo=" alt="data-png">', body)
        for tree in (self.root / '.build/docs/html', self.published):
            media = sorted(path.relative_to(tree).as_posix() for path in (tree / '_media').rglob('*') if path.is_file())
            self.assertEqual(media, ['_media/notes/media/kept.png', '_media/notes/media/upper.PNG'], tree)
        self.assertIn('NOTE: reference page notes/types.md: media file media/evil.svg is not a PNG, JPEG, GIF, '
                      'WebP or AVIF image; shown as text', self.lint.stdout)
        self.assertIn('NOTE: reference page notes/types.md: media file media/fake.png is not the image its name '
                      'says; shown as text', self.lint.stdout)

    def test_placeholders_in_a_file_stay_text(self):
        page = self.page('notes.placeholders.md.html')
        for script in ('toc', 'nav', 'code', 'filelinks'):
            self.assertEqual(page.count(f'<script defer src="assets/{script}.js'), 1, script)
        self.assertEqual(page.count('<main'), 1)
        self.assertIn('<title>Title {{CONTENT}} {{SCRIPTS}}</title>', page)
        self.assertIn('Text {{SCRIPTS}} {{CONTENT}} {{TOC}} {{CROSSNAV}} {{HEAD_EXTRA}} {{TITLE}}.', page)

    def test_attempts(self):
        body = content(self.page('notes.attempts.md.html'))
        # Other loading tags show as text; an image inside them is still only a link.
        self.assertIn('&lt;iframe srcdoc=', body)
        self.assertIn('&lt;template&gt;<a href="https://h.test/tpl">https://h.test/tpl</a>&lt;/template&gt;', body)
        # Other ways to write an address.
        for name in ('i0', 'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9',
                     'x10', 'x11', 'x12', 'l4', 'l5', 'l6', 'l7'):
            self.assertIn(GONE + name + '</span>', body, name)
        for name, address in (('x1', 'http://h.test/x1'), ('x2', 'https://h.test/x2'), ('x3', 'https://h.test/x3'),
                              ('l1', 'https://h.test/l1'), ('l2', 'https://h.test/l2'), ('l3', 'http://h.test/l3')):
            self.assertIn(f'<a href="{address}">{name}</a>', body, name)
        # Nested and malformed markup: the first of a repeated attribute counts.
        self.assertIn('<img src="_media/notes/media/kept.png"> <a href="https://h.test/m6">', body)
        self.assertIn('&lt;/main&gt;<div><b>out</b>', body)
        # Inside Markdown constructs: an image in a link is text in it, a code span stays code.
        self.assertIn('<a href="https://example.com/">https://h.test/k1</a>', body)
        self.assertIn('<code>&lt;img src=//h.test/k4&gt;</code>', body)
        self.assertIn('<td><b>c</b></td>', body)
        # Markdown that writes attributes escapes their values.
        self.assertIn('<a href="https://example.com/" title="&quot; onmouseover=&quot;alert(1)">t</a>', body)
        self.assertIn('alt="&quot; onerror=&quot;alert(1)"', body)
        self.assertIn('data-source="javascript:alert(1)&quot;"', body)
        self.assertIn('data-lang="&quot;&gt;&lt;img"', body)


if __name__ == '__main__':
    unittest.main()
