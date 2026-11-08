+++
title = "Build a site"
brand = "Documentation kit"
brand_sub = "how it works · pages · reader · commands"
description = "How the kit turns tracked Markdown into a checked website: the two kinds of pages, publishing existing records, what readers get, figures and slides, and every command from build to upgrade."
components = ["toc", "nav", "code", "filelinks", "lightbox", "carousel", "panel-switcher"]
page_css = ["build-sheet.css"]
math = true
toc = [["How it works", "#how-a-build-works"], ["Two kinds of pages", "#two-kinds-of-pages"], ["Existing Markdown", "#existing-markdown"], ["The reader", "#the-reader"], ["Figures and slides", "#figures-and-slides"], ["Build", "#build"], ["Lint", "#lint"], ["Preview", "#preview"], ["Upgrade", "#upgrade"], ["Reference guides", "#reference-guides"]]
+++

# Build a site

<section class="card" id="how-a-build-works">

<!-- slide -->
<p class="slide-eyebrow">Build a site</p>
<p class="slide-title">Your Markdown goes in; a checked, self-contained website comes out</p>
<p class="slide-lead">One command reads your tracked sources through the pinned kit. Nothing extra is installed, and nothing outside the project is published.</p>
<div class="slide-main"><div class="slide-row"><div class="slide-tile is-term"><h4>You write</h4><p>topic pages and records under docs/ · site.toml</p></div><div class="slide-tile"><h4>The kit renders</h4><p>reader, theme, fonts, math · link and anchor checks</p></div><div class="slide-tile is-held"><span class="slide-tag">generated</span><h4>.build/docs/</h4><p>plain HTML · rebuilt, never edited</p></div></div></div>
<p class="slide-scope">This card is a slide face: the summary that opens a chapter; docsite.py slides collects faces into a deck</p>
<!-- /slide -->

## One command turns your tracked Markdown into a checked, self-contained site

<p class="bs-lead"><code>docsite.py build</code> reads the project's tracked sources through the pinned kit and writes plain HTML into <code>.build/docs/</code>; that output is never edited.</p>

<figure id="fig-build">
<div class="bs-flow" role="img" aria-label="Tracked project sources and the pinned kit enter docsite.py build. The build writes generated HTML, assets and a build manifest into .build/docs. Lint and the freshness check read that output. Generated output never flows back into source.">
<div class="bs-node bs-teal"><span class="bs-label">Project sources · tracked</span><b>What you write</b><ul><li><code>docs/topics/*/index.md</code> pages</li><li>registered Markdown records</li><li><code>docs/site/site.toml</code></li><li>figures and media</li></ul></div>
<div class="bs-arrow"><span>build</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Pinned kit · <code>.docs-kit/</code></span><b>What renders it</b><ul><li>Markdown, includes, slide faces</li><li>reader, theme, fonts, math</li><li>link rewriting and checks</li></ul></div>
<div class="bs-arrow"><span>writes</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Generated · ignored by Git</span><b><code>.build/docs/</code></b><ul><li><code>html/*.html</code>, <code>assets/</code></li><li>media under <code>_media/</code></li><li><code>site-build.json</code></li></ul></div>
<div class="bs-back"><span>×</span> Output never flows back. Change a source, the configuration or a generator, then rebuild.</div>
</div>
<figcaption><b>Figure 1.</b> Follow the arrows from what you write to what readers get. This diagram contains no measured results.</figcaption>
</figure>

[Figure 1](#fig-build) is the whole pipeline. Because the output is generated, it can always be deleted and rebuilt, and a reviewer only has to look at sources. Because only tracked files are read, what you publish is exactly what is in Git: a stray local file cannot leak onto the site, and a file you forgot to add fails the build instead of producing a page with a broken image. The site needs no web framework and no JavaScript install; the reader, theme, fonts and math come from the pinned kit.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Fix the typo in the output</h3><p>Someone edits <code>.build/docs/html/guide.html</code>. The next build overwrites the fix, and the source still has the typo.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Fix the source, rebuild</h3><p>The typo is fixed in <code>docs/topics/guide/index.md</code>; <code>build</code> regenerates the page and <code>build --check</code> confirms nothing else is stale.</p></div>
</div>

<!-- fold: code How links are rewritten -->

Inside a page, link to other pages by their generated name, such as `evidence.html#numbers-and-staleness`. Links to any other repository file become source links: GitHub on a served site, the local checkout when the pages are opened as files. Every path stays inside the project; a link, include or image that escapes it fails the build. [Authoring paths](authoring.html#authoring-paths) has the exact rules.

<!-- /fold -->

</section>

<section class="card" id="two-kinds-of-pages">

## A site has two kinds of pages: ones you write for people, and records published as they are

<p class="bs-lead">Write a topic page when you want to explain something; register a record when it already exists and must stay the only copy.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Written for people</span><h3>Topic page</h3><ul>
<li>lives at <code>docs/topics/&lt;name&gt;/index.md</code></li>
<li>frontmatter gives its title and chapter labels</li>
<li>chapters from <code>##</code> headings or <code>&lt;section class="card"&gt;</code></li>
<li>build-sheet blocks, figures, folds and slide faces</li>
<li>appears in the menu through a <code>[[nav]]</code> entry</li>
</ul><p>This page is one. So are Get started and the three practice pages.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Already exists</span><h3>Registered record</h3><ul>
<li>any tracked Markdown file, wherever it lives</li>
<li>one <code>[[source_pages]]</code> entry in <code>site.toml</code></li>
<li>rendered whole, with a source line and edit link</li>
<li>links resolved from the file's own folder</li>
<li>stays plain Markdown that agents keep reading</li>
</ul><p>Every rule guide on this site is one, as are the README and release notes.</p></div>
</div>

The split follows what each reader needs. An agent needs the exact contract in plain Markdown, at a stable path its router names. A person needs the conclusion, a figure and the reason, in order. A topic page explains a subject and links into its records; a registered record publishes the contract itself without changing a character. Neither replaces the other, so neither is ever a second copy.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Rewrite the record as a page</h3><p>A rule guide is copied into a topic page with cards and figures, and the Markdown is kept for agents. The next rule change lands in one of them.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Register it, explain it once</h3><p>The guide is registered as it is; one topic page explains it with examples and links to its sections.</p></div>
</div>

[Authoring paths](authoring.html#authoring-paths) covers frontmatter, link origins and includes; [records and pages](writing-practices.html#records-and-pages) explains the split as a documentation rule.

</section>

<section class="card" id="existing-markdown">

## Existing Markdown becomes a page without being moved or copied

<p class="bs-lead">One <code>[[source_pages]]</code> entry publishes a tracked Markdown file at a route you choose; the file stays where it is and stays the only copy.</p>

<figure id="fig-source-page">
<div class="bs-flow" role="img" aria-label="A tracked Markdown file, for example docs/notes/decision.md, stays unchanged. A source_pages entry in site.toml names the file and its route. The build renders decision.html with a source line and edit link, resolving links from the file's own folder and checking anchors between registered pages.">
<div class="bs-node bs-teal"><span class="bs-label">Stays where it is</span><b>Your Markdown file</b><ul><li><code>docs/notes/decision.md</code></li><li>agents keep reading it as Markdown</li></ul></div>
<div class="bs-arrow"><span>register</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>docs/site/site.toml</code></span><b>One entry</b><ul><li><code>[[source_pages]]</code></li><li><code>source = "docs/notes/decision.md"</code></li><li><code>slug = "decision"</code></li></ul></div>
<div class="bs-arrow"><span>build</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Generated</span><b><code>decision.html</code></b><ul><li>whole file, rendered</li><li>source line and edit link</li><li>links and anchors checked</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> Publishing a record is a pointer, not a copy. This diagram contains no measured results.</figcaption>
</figure>

**The problem it solves.** Projects already have Markdown worth reading on a site: rules, decision notes, a README, release notes. Copying a file into a page creates a second copy that drifts. Moving it breaks every link and every agent route that points at its path. Registering it changes nothing about the file; the site simply learns where it is.

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">top of page</span><h3>Source line</h3><p>Shows the file's path and an "Edit source" link to the original, so readers fix the file, not the page.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">links</span><h3>Resolved from its folder</h3><p><code>../other.md</code> and images work exactly as they do on GitHub, because they resolve from the file's own folder.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">between records</span><h3>Page links, checked</h3><p>A link to another registered file becomes <code>other.html#section</code>; the build fails if that section does not exist.</p></div>
</div>

The same lines, both ways. Switch between them:

<div class="panel-switcher" data-panel-switcher data-panel-default="markdown">
<div class="panel-switcher-controls" role="group" aria-label="View of a registered record">
<button type="button" data-panel-choice="markdown" aria-pressed="false" aria-controls="view-markdown">As agents read it</button>
<button type="button" data-panel-choice="page" aria-pressed="false" aria-controls="view-page">As this site renders it</button>
</div>
<div id="view-markdown" data-panel="markdown">

```markdown source=rules/experiments/workflow.md#L36-L38
- A **qualification** gives a pass, fail or inconclusive verdict on a named
  system, build or model: platform qualification, a benchmark contract, a
  parity check, model release evaluation.
```

</div>
<div id="view-page" data-panel="page">
<div class="bs-part bs-orange"><span class="bs-label">Rendered from the same lines · <code>rules/experiments/workflow.md</code></span><h3>Qualification</h3><p>A <b>qualification</b> gives a pass, fail or inconclusive verdict on a named system, build or model: platform qualification, a benchmark contract, a parity check, model release evaluation.</p><p><a href="experiment-workflow.html#choose-the-purpose">Open it on its page</a></p></div>
</div>
</div>

<!-- fold: code The full registry entry -->

```toml
[[source_pages]]
source = "docs/notes/decision.md"   # required: a tracked file inside the project
slug = "decision"                   # required: the page is decision.html
title = "Decision record"           # optional: defaults to the file's first # heading
description = "Why we chose …"      # optional: card text on the home page
reader = true                       # optional: chapter cards instead of one scroll
math = true                         # optional: render formulas
```

Each route also needs a `[[nav]]` entry: with a `group` it appears in the menu; with `hidden = true` it is reachable by link only. One slug belongs to one page; a collision fails the build. [Registered source pages](authoring.html#registered-source-pages) owns the contract.

<!-- /fold -->

</section>

<section class="card" id="the-reader">

## Readers move chapter by chapter, keep the menu docked and pin a reference

<p class="bs-lead">Every topic page becomes a row of chapter cards; readers choose one, two or all chapters and open optional depth only when they want it.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">try</span><h3>Move</h3><p>Press <kbd>→</kbd> and <kbd>←</kbd>, or the arrows in the top bar. Each chapter remembers where you stopped.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">try</span><h3>Choose the layout</h3><p><b>One chapter</b>, <b>Two chapters</b> side by side, or <b>All chapters</b> as one long scroll.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">try</span><h3>Dock the menu</h3><p>On screens wider than 900 px the menu starts docked. <code>«</code> hides it; <code>☰</code> brings it back docked. Each page remembers your choice.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">try now</span><h3>Pin a reference</h3><p>Choose <b>Two chapters</b>, press <code>⌖</code> on this chapter's header, then press <kbd>→</kbd>: this chapter stays, the other column moves.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">try now</span><h3>Open a layer</h3><p>The buttons under this heading open every fold of one kind: Math, Experiments, Code or Alternatives. Each column keeps its own choice.</p></div>
</div>

Long technical pages fail readers in two ways: the point scrolls away under detail, or a definition disappears while you read the part that uses it. Chapters keep one claim per screen. Pinning holds the definition beside its use. Layers keep the visible story short without deleting the detail; it stays one click away, and printing a page opens all of it.

<!-- fold: code How to write chapters and layers -->

A chapter is a `##` heading, or an explicit `<section class="card" id="…">` when you want control over its contents. The frontmatter `toc` gives each chapter its short label in the toolbar. A layer is a typed fold: `<!-- fold: math Title -->` … `<!-- /fold -->`, with `experiment`, `code` or `dead-end` (shown as Alternatives) in place of `math`. These lines in this site's configuration turn the reader on for every page that does not opt out:

```toml source=docs/site/site.toml#L4-L8
title = "Documentation kit"
home_label = "Kit"
gh_repo = "https://github.com/davszi/documentation-kit"
gh_ref = "main"
chapter_reader = true
```

<!-- /fold -->

<!-- fold: math How the progress bar counts -->

The bar under the site name shows the active chapter $k$ of the page's $n$ chapters:

$$
\text{progress} = \frac{k}{n}, \qquad 1 \le k \le n
$$

This page has $n = 10$ chapters, so this fourth chapter fills $4/10$ of the bar.

<!-- /fold -->

<!-- fold: dead-end Why not one long scroll -->

A single scroll is still available as **All chapters**, and it is what print and no-JavaScript readers get. As the default it loses the two things above: one claim per screen, and a reference held beside its use. The reader adds both without changing the source; it is the same Markdown either way.

<!-- /fold -->

</section>

<section class="card" id="figures-and-slides">

## Figures come from the page source; slide faces turn chapters into a deck

<p class="bs-lead">Diagrams are HTML written in the page, images are tracked files, and the summary card that opens a chapter doubles as a presentation slide.</p>

<div class="bs-grid g2">
<figure id="fig-captures">
<div class="fig-carousel">
<img src="../topics/build-a-site/media/reader.png" alt="This site's Experiments page in the reader at 1600 by 1000 pixels: menu docked on the left, the keep-experiments-small chapter in the active card, the next chapter at the right edge.">
<img src="../topics/build-a-site/media/home.png" alt="This site's home page at 1600 by 1000 pixels with its hero, the three paths and the adoption steps.">
</div>
<figcaption><b>Figure 3.</b> Two captures of this site (2026-11-08) in a carousel. It advances by itself and pauses on hover; click a capture to open it full screen, scroll to zoom, drag to pan, <kbd>Esc</kbd> to close.</figcaption>
</figure>
<div class="bs-grid g1">
<div class="bs-part bs-teal"><span class="bs-label">Figures</span><h3>Built from the page, checked by the build</h3><ul>
<li>flows and diagrams are HTML blocks with a text alternative, like Figures 1 and 2</li>
<li>images are tracked files; the build packages them and fails on a missing one</li>
<li>images and SVG figures open full screen</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">Slides</span><h3>A chapter's summary is its slide</h3><ul>
<li>write a face between <code>&lt;!-- slide --&gt;</code> and <code>&lt;!-- /slide --&gt;</code> at the start of a chapter</li>
<li>the first chapter of this page opens with one</li>
<li>every fact on a slide is also in its chapter</li>
</ul></div>
</div>
</div>

```bash
.build/docs-env/bin/python .docs-kit/docsite.py slides --project . --select build-a-site --out overview
.build/docs-env/bin/python .docs-kit/docsite.py slides --project . --select guide --select other#intro,result --out review --title "Review"
```

`slides` builds the site, then collects the faces of the selected chapters into `.build/slides/<name>.html`. A bare slug takes every face in reading order; `slug#a,b` takes those chapters in the order given; repeat `--select` to combine pages. See [generated figures](authoring.html#generated-figures), [slide faces and decks](authoring.html#slide-faces-and-decks) and [figures and access](figures.html).

</section>

<section class="card" id="build">

## Build writes the site; --check proves it is current without writing

<p class="bs-lead">Run <code>build</code> after changing a source; run <code>build --check</code> to confirm nothing is stale.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">writes</span><h3><code>build</code></h3><p>Renders every page into <code>.build/docs/</code> from tracked sources and the pinned kit, and removes obsolete output.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">writes</span><h3><code>build --page &lt;slug&gt;</code></h3><p>Renders only that page while you work on it; shared assets still sync.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">reads</span><h3><code>build --check</code></h3><p>Renders in memory and fails if the generated site no longer matches its sources. Writes nothing.</p></div>
</div>

```bash
.build/docs-env/bin/python .docs-kit/docsite.py build --project .
.build/docs-env/bin/python .docs-kit/docsite.py build --project . --page guide
.build/docs-env/bin/python .docs-kit/docsite.py build --project . --check
```

The build fails instead of publishing a broken page: untracked or missing media, paths that leave the project, route collisions and wrong anchors into registered pages all stop it. Generated output is never edited; change the source, configuration or generator and rebuild. [How a build works](#how-a-build-works) explains why.

</section>

<section class="card" id="lint">

## Lint checks the records behind the site; --strict makes warnings fail

<p class="bs-lead">Run <code>lint --strict</code> before you commit documentation; it covers what the build cannot see.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">links</span><h3>Links and anchors</h3><p>Markdown links and anchors in <code>docs/</code>, <code>AGENTS.md</code>, <code>CLAUDE.md</code> and <code>README.md</code> resolve, and so do links in the built HTML.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">excerpts</span><h3>Code excerpts</h3><p>A fenced block tagged <code>source=path#La-Lb</code> must still appear in its file, at the stated lines.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">figures</span><h3>Figure manifest</h3><p>Figure files and manifest entries match both ways, and their generators exist.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">records</span><h3>Worklog and open work</h3><p>Worklog dates run newest first; every open-work bullet links its owner, with no struck or ticked lines.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">site</span><h3>Fresh, self-contained output</h3><p>The built site is fresh and loads no external resources.</p></div>
</div>

```bash
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --registry
```

Without `--strict`, warnings print but the run passes; with it, any warning fails. `--registry` lists every `INVARIANT` and `DON'T-REDO` marker in the project and exits. A project with established file names sets `worklog` or `open_work` in `site.toml`; see [resources](resources.html).

</section>

<section class="card" id="preview">

## Review the built site on loopback before anyone else sees it

<p class="bs-lead">Serve <code>.build/docs/</code> on 127.0.0.1 and read the changed pages at wide and narrow widths.</p>

```bash
python3.12 -m http.server 8321 --bind 127.0.0.1 --directory .build/docs
```

Open `http://127.0.0.1:8321/html/index.html`. The server exposes only the generated output, not the repository. A successful build and lint still need a look at the rendered page: check the changed layout at wide and narrow widths before committing or publishing. [Validation](validation.html#validation-and-review) lists what a complete review covers, including the reusable browser checks.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>"Lint passed, so it looks fine"</h3><p>The new table is never opened on a phone; it pushes the page sideways for every narrow reader.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Open the changed page at both widths</h3><p>The table is checked at desktop and phone width before the commit, and the review is mentioned in the handoff.</p></div>
</div>

</section>

<section class="card" id="upgrade">

## An upgrade moves the pin only after you read what changed

<p class="bs-lead">The submodule commit is your version. Nothing changes until you move it, rebuild, review and commit the new pin.</p>

<figure id="fig-upgrade">
<div class="bs-flow" role="img" aria-label="Read the release notes between your pinned version and the target. Move the .docs-kit submodule to the reviewed commit or tag. Rebuild and lint, review the pages, then commit the pin together with any consumer changes.">
<div class="bs-node bs-teal"><span class="bs-label">Read</span><b>Release notes</b><ul><li>changes since your pin</li><li>migration guide if any</li></ul></div>
<div class="bs-arrow"><span>move</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>.docs-kit</code></span><b>Check out the target</b><ul><li>a reviewed commit or tag</li></ul></div>
<div class="bs-arrow"><span>verify</span></div>
<div class="bs-node bs-orange"><span class="bs-label">One commit</span><b>Rebuild, review, commit</b><ul><li>build and lint</li><li>pin plus consumer changes</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> The upgrade sequence. This diagram contains no measured results.</figcaption>
</figure>

```bash
git -C .docs-kit fetch --tags
git -C .docs-kit checkout <reviewed-kit-commit-or-tag>
.build/docs-env/bin/python .docs-kit/docsite.py build --project .
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
git add .docs-kit
```

Others clone with `git clone --recurse-submodules <project-url>` and get exactly your pinned kit. Share fixes upstream in the kit, not by editing a consumer's submodule checkout. [Release notes](releases.html) list what each version changes for consumers; [README · Pin and upgrade](readme.html#pin-and-upgrade) has the details.

</section>

<section class="card" id="reference-guides">

## Each toolkit task has one reference guide

<p class="bs-lead">This page explains how the toolkit fits together; each reference guide holds the exact contract for one task.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Toolkit reference guides by task">

| To… | Read… | It covers |
|---|---|---|
| Configure the site | [Tooling and ownership](authoring.html#tooling-and-ownership) | `site.toml` keys, navigation, adapters and project components |
| Write pages | [Authoring paths](authoring.html#authoring-paths), [registered source pages](authoring.html#registered-source-pages) | Entry pages and frontmatter, link origins, includes, registered records |
| Shape the reader | [Reader](reader.html), [panel switcher](panel-switcher.html) | Chapter views, reading layers, the home site map, the panel switcher contract |
| Draw, derive and present | [Generated figures](authoring.html#generated-figures), [slide faces and decks](authoring.html#slide-faces-and-decks) | Generated figures and number ledgers, math, slide faces and decks |
| Package images, media and evidence | [Resources and evidence](resources.html) | Resource closure, local-only captures, inventories, path adapters |
| Check and publish | [Validation](validation.html), [publication export](publication.html) | Complete validation, browser checks, export into an existing publication |

</div>

The writing side of a page (section design, figures, mathematics, code excerpts) is explained on [Documentation and writing](writing-practices.html).

</section>
