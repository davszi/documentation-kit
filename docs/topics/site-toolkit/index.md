+++
title = "Site toolkit"
brand = "Documentation kit"
brand_sub = "sources · build · checks"
description = "How a build turns tracked sources into a checked site, and which guide covers each task."
reader = false
body_class = "reference-page"
components = ["toc", "nav", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["How a build works", "#how-a-build-works"], ["Find the guide for a task", "#find-the-guide-for-a-task"], ["Render existing Markdown in place", "#render-existing-markdown-in-place"]]
+++

# The site toolkit turns tracked sources into a checked static site

<p class="bs-lead">One command reads the project's tracked sources through the pinned kit and writes a self-contained site under <code>.build/docs/</code>; lint and the freshness check then verify it.</p>

## How a build works

<figure id="fig-build">
<div class="bs-flow" role="img" aria-label="Tracked project sources and the pinned kit enter docsite.py build. The build writes generated HTML, assets and a build manifest. Lint and the freshness check read that output. Generated output never flows back into source.">
<div class="bs-node bs-teal"><span class="bs-label">Project sources · tracked</span><b>Content and configuration</b><ul><li><code>docs/topics/*/index.md</code> pages</li><li>registered Markdown records</li><li><code>docs/site/site.toml</code>, fragments, local CSS</li><li><code>docs/figures/</code> and media</li></ul></div>
<div class="bs-arrow"><span>build</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Pinned kit</span><b>Renderer and theme</b><ul><li>Markdown, includes and slide faces</li><li>shell, reader and components</li><li>link rewriting and resource closure</li></ul></div>
<div class="bs-arrow"><span>writes</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Generated · ignored by Git</span><b><code>.build/docs/</code></b><ul><li><code>html/*.html</code> and <code>assets/</code></li><li>packaged media under <code>_media/</code></li><li><code>site-build.json</code> manifest</li></ul><small>Checked by <code>build --check</code> and <code>lint --strict</code>.</small></div>
<div class="bs-back"><span>×</span> Output is never edited. Change a source, configuration or generator, then rebuild.</div>
</div>
<figcaption><b>Figure 1.</b> Follow the arrows from tracked inputs to generated output. Untracked files, symlink escapes and missing media fail the build instead of being published.</figcaption>
</figure>

Pages link to each other by their generated names, such as `evidence.html#numbers-and-staleness`.
Links to other repository files become source links: GitHub on a served site,
and the local checkout when the generated pages are opened directly as files.
[Authoring paths](authoring.html#authoring-paths)
gives the exact rules.

## Find the guide for a task

| To… | Read… | It covers |
|---|---|---|
| Run commands and configure the site | [README commands](readme.html#commands), [tooling and ownership](authoring.html#tooling-and-ownership) | `init`, `build`, `lint` and `slides`; `site.toml` keys, navigation and adapters |
| Write pages | [Authoring paths](authoring.html#authoring-paths) | Entry pages and frontmatter, link origins, includes, local components, registered source pages |
| Use the reader and components | [Reader](reader.html), [panel switcher](panel-switcher.html) | Chapter views, reading layers, the home site map and the shared panel switcher |
| Draw, derive and present | [Generated figures](authoring.html#generated-figures), [slide faces](authoring.html#slide-faces-and-decks) | Generated figures and number ledgers, KaTeX math, slide faces and decks |
| Package images, media and evidence | [Resources and evidence](resources.html) | Resource closure, local-only captures, inventories, path and evidence adapters |
| Check and publish | [Validation](validation.html), [publication export](publication.html) | Complete validation, browser checks, export into an existing publication |

Related writing rules: [slide faces](page-design.html#slide-faces),
[mathematical explanation](math.html) and [figures and access](figures.html).
The [panel switcher contract](panel-switcher.html) documents its markup.

## Render existing Markdown in place

<p class="bs-lead">A project can publish an existing Markdown record as a page without moving or copying it.</p>

A `[[source_pages]]` entry in `site.toml` names the file and its public route.
The page renders the whole file, resolves its links and media from the file's
own folder, and shows a link to the canonical source and its edit page. Links
between registered files become page links, and their anchors are checked.
[Registered source pages](authoring.html#registered-source-pages) owns the
contract. Every detailed guide on this site is rendered this way.
