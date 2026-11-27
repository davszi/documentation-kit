+++
title = "Build a site"
brand_sub = "how it works · pages · reader · commands"
description = "How the kit turns tracked Markdown into a checked website: writing a topic page, what readers get, figures and slides, publishing Markdown you already have, and the commands from build to upgrade."
components = ["toc", "nav", "code", "filelinks", "lightbox", "carousel", "panel-switcher"]
page_css = ["build-sheet.css"]
math = true
toc = [["How it works", "#how-a-build-works"], ["Write a page", "#write-a-topic-page"], ["The reader", "#the-reader"], ["Figures and slides", "#figures-and-slides"], ["Existing Markdown", "#existing-markdown"], ["Build", "#build"], ["Lint", "#lint"], ["Preview", "#preview"], ["Upgrade", "#upgrade"], ["Reference guides", "#reference-guides"]]
page_only = "Explains building a site; its records are the site guides in rules/site/."
+++

# Build a site

<section class="card" id="how-a-build-works">

<!-- slide -->
<style>
/* Local to this face: a one-way pipeline across the canvas above the two things that never happen; a tall drawing replaces the pipeline below 720 px. */
.slide-main.fx-build {justify-content:space-between!important;gap:1.6cqi!important;}
.fx-build > figure {flex:1 1 0!important;min-height:0!important;display:flex!important;flex-direction:column!important;gap:.4cqi!important;margin:0!important;}
.fx-build svg {display:block!important;width:100%!important;}
.fx-build svg.fx-wide {flex:1 1 0!important;min-height:0!important;height:100%!important;}
.fx-build svg.fx-tall {display:none!important;}
.fx-build figcaption {font:1cqi/1.3 "IBM Plex Mono",monospace!important;color:var(--sf-dim)!important;text-align:right!important;}
.fx-never {display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:3cqi!important;margin:0!important;padding:0!important;list-style:none!important;}
.fx-never > li {display:grid!important;grid-template-columns:2.6cqi minmax(0,1fr)!important;column-gap:.8cqi!important;margin:0!important;padding:.9cqi 0 0!important;border-top:1px solid color-mix(in srgb,var(--sf-alert) 45%,var(--sf-line))!important;}
.fx-never > li::before {content:"\00d7"!important;grid-row:1 / span 2!important;font:700 2.4cqi/1 "IBM Plex Sans",sans-serif!important;color:var(--sf-alert)!important;}
.fx-never b {font:600 1.7cqi/1.2 "IBM Plex Sans",sans-serif!important;color:var(--sf-ink)!important;}
.fx-never p {grid-column:2!important;margin:.3cqi 0 0!important;font-size:1.35cqi!important;line-height:1.38!important;color:var(--sf-sub)!important;}
.fx-never code {font:1.25cqi "IBM Plex Mono",monospace!important;color:var(--sf-ink)!important;background:none!important;padding:0!important;white-space:nowrap!important;}
@container (max-width: 719.98px) {
  .fx-build > figure {flex:none!important;}
  .fx-build svg.fx-wide {display:none!important;}
  .fx-build svg.fx-tall {display:block!important;height:auto!important;}
  .fx-build figcaption {font-size:12px!important;text-align:left!important;}
  .fx-never {grid-template-columns:1fr!important;gap:14px!important;}
  .fx-never > li {grid-template-columns:24px minmax(0,1fr)!important;column-gap:8px!important;padding-top:10px!important;}
  .fx-never > li::before {font-size:22px!important;}
  .fx-never b {font-size:16px!important;}
  .fx-never p {font-size:14px!important;}
  .fx-never code {font-size:13px!important;white-space:normal!important;}
}
</style>
<p class="slide-eyebrow">Build a site</p>
<p class="slide-title">Tracked Markdown in, a checked, self-contained site out</p>
<div class="slide-main fx-build">
<figure>
<svg class="inline-fig fx-wide" viewBox="0 0 1200 436" role="img" aria-label="docsite.py build reads the project's tracked sources: the topic pages, registered Markdown records, docs/site/site.toml, figures and media. An untracked file is not read. The pinned kit renders Markdown, includes and slide faces with the reader, theme, fonts and math, rewrites and checks links, and writes the pages with their assets and media under html/, and site-build.json beside them, into .build/docs, which Git ignores. Output never flows back into source.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<path d="M1010 64V22H190V56" fill="none" stroke="#ff7b72" stroke-width="3" stroke-dasharray="10 8"/><path d="M190 70l-8-16h16z" fill="#ff7b72"/>
<rect x="436" y="6" width="330" height="32" rx="16" fill="#0d1117"/>
<circle cx="458" cy="22" r="14" fill="#0d1117" stroke="#ff7b72" stroke-width="3"/><path d="M452 16l12 12M464 16l-12 12" stroke="#ff7b72" stroke-width="3" stroke-linecap="round"/>
<text x="482" y="29" font-size="20" fill="#ff7b72" font-weight="600">output never flows back</text>
<rect x="4" y="70" width="370" height="290" rx="16" fill="#0f1d22" stroke="#39d2c0" stroke-width="3"/>
<text x="28" y="110" font-size="17" fill="#39d2c0" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">TRACKED IN GIT</text>
<g fill="#121a24" stroke="#39d2c0" stroke-width="2"><path d="M28 140h17l8 8v22H28z"/><path d="M28 196h17l8 8v22H28z"/><path d="M28 252h17l8 8v22H28z"/><path d="M28 308h17l8 8v22H28z"/></g>
<text x="68" y="164" font-size="19" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">docs/topics/*/index.md</text>
<text x="68" y="220" font-size="21" fill="#e6edf3">registered Markdown records</text>
<text x="68" y="276" font-size="19" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">docs/site/site.toml</text>
<text x="68" y="332" font-size="21" fill="#e6edf3">figures and media</text>
<path d="M98 380V366" stroke="#7d8896" stroke-width="3" stroke-dasharray="5 4"/>
<path d="M86 384h17l8 8v22H86z" fill="none" stroke="#7d8896" stroke-width="2" stroke-dasharray="4 3"/>
<text x="124" y="410" font-size="20" fill="#a9b4c2">untracked file</text>
<circle cx="282" cy="403" r="15" fill="#0d1117" stroke="#ff7b72" stroke-width="3"/><path d="M276 397l12 12M288 397l-12 12" stroke="#ff7b72" stroke-width="3" stroke-linecap="round"/>
<text x="306" y="410" font-size="20" fill="#ff7b72" font-weight="600">not read</text>
<path d="M382 215H436" stroke="#39d2c0" stroke-width="9"/><path d="M458 215l-24-15v30z" fill="#39d2c0"/>
<text x="418" y="192" font-size="19" fill="#39d2c0" font-weight="600" text-anchor="middle">reads</text>
<rect x="452" y="62" width="320" height="306" rx="20" fill="none" stroke="#bc8cff" stroke-width="12" stroke-opacity=".12"/>
<rect x="458" y="68" width="308" height="294" rx="16" fill="#17142a" stroke="#bc8cff" stroke-width="3"/>
<text x="482" y="110" font-size="17" fill="#bc8cff" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">PINNED KIT</text>
<text x="482" y="158" font-size="29" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">docsite.py build</text>
<g fill="#bc8cff"><circle cx="488" cy="205" r="4.5"/><circle cx="488" cy="246" r="4.5"/><circle cx="488" cy="287" r="4.5"/><circle cx="488" cy="328" r="4.5"/></g>
<g font-size="20" fill="#e6edf3"><text x="504" y="212">Markdown and includes</text><text x="504" y="253">slide faces</text><text x="504" y="294">reader, theme, fonts, math</text><text x="504" y="335">link rewriting and checks</text></g>
<path d="M776 215H830" stroke="#39d2c0" stroke-width="9"/><path d="M852 215l-24-15v30z" fill="#39d2c0"/>
<text x="812" y="192" font-size="19" fill="#39d2c0" font-weight="600" text-anchor="middle">writes</text>
<rect x="852" y="70" width="344" height="290" rx="16" fill="none" stroke="#ffa657" stroke-width="2.5" stroke-dasharray="10 7"/>
<text x="876" y="110" font-size="17" fill="#ffa657" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">GENERATED</text>
<text x="1176" y="110" font-size="17" fill="#7d8896" text-anchor="end">Git ignores it</text>
<text x="876" y="160" font-size="29" fill="#ffa657" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.build/docs/</text>
<path d="M884 196V322M884 204h10M884 244h10M884 284h10M884 322h10" fill="none" stroke="#7d8896" stroke-width="2"/>
<g font-size="20" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace"><text x="902" y="211">html/*.html</text><text x="902" y="251">html/assets/</text><text x="902" y="291">html/_media/</text><text x="902" y="329">site-build.json</text></g>
</g>
</svg>
<svg class="inline-fig fx-tall" viewBox="0 0 340 820" role="img" aria-label="docsite.py build reads the project's tracked sources: the topic pages, registered Markdown records, docs/site/site.toml, figures and media. An untracked file is not read. The pinned kit renders them and writes the pages with their assets and media under html/, and site-build.json beside them, into .build/docs, which Git ignores. Output never flows back into source.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<path d="M28 760H10V40H28" fill="none" stroke="#ff7b72" stroke-width="2.5" stroke-dasharray="8 6"/><path d="M40 40l-14-7v14z" fill="#ff7b72"/>
<rect x="0" y="380" width="22" height="196" fill="#0d1117"/>
<text transform="translate(17 566) rotate(-90)" font-size="15" fill="#ff7b72" font-weight="600">× output never flows back</text>
<rect x="40" y="6" width="298" height="200" rx="12" fill="#0f1d22" stroke="#39d2c0" stroke-width="2"/>
<text x="56" y="34" font-size="15" fill="#39d2c0" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">TRACKED IN GIT</text>
<text x="56" y="70" font-size="15" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">docs/topics/*/index.md</text>
<text x="56" y="106" font-size="17" fill="#e6edf3">registered Markdown records</text>
<text x="56" y="142" font-size="15" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">docs/site/site.toml</text>
<text x="56" y="178" font-size="17" fill="#e6edf3">figures and media</text>
<rect x="40" y="216" width="196" height="58" rx="10" fill="none" stroke="#7d8896" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="54" y="240" font-size="16" fill="#a9b4c2">untracked file</text>
<text x="54" y="263" font-size="16" fill="#ff7b72" font-weight="600">× not read</text>
<path d="M290 210V294" stroke="#39d2c0" stroke-width="6"/><path d="M290 312l-11-18h22z" fill="#39d2c0"/>
<text x="276" y="300" font-size="15" fill="#39d2c0" font-weight="600" text-anchor="end">reads</text>
<rect x="40" y="316" width="298" height="206" rx="12" fill="#17142a" stroke="#bc8cff" stroke-width="2"/>
<text x="56" y="344" font-size="15" fill="#bc8cff" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">PINNED KIT</text>
<text x="56" y="378" font-size="21" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">docsite.py build</text>
<g font-size="16" fill="#e6edf3"><text x="56" y="412">Markdown and includes</text><text x="56" y="440">slide faces</text><text x="56" y="468">reader, theme, fonts, math</text><text x="56" y="496">link rewriting and checks</text></g>
<path d="M290 526V560" stroke="#39d2c0" stroke-width="6"/><path d="M290 578l-11-18h22z" fill="#39d2c0"/>
<text x="276" y="560" text-anchor="end" font-size="15" fill="#39d2c0" font-weight="600">writes</text>
<rect x="40" y="580" width="298" height="214" rx="12" fill="none" stroke="#ffa657" stroke-width="2" stroke-dasharray="8 6"/>
<text x="56" y="608" font-size="15" fill="#ffa657" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">GENERATED</text>
<text x="322" y="608" font-size="15" fill="#7d8896" text-anchor="end">Git ignores it</text>
<text x="56" y="642" font-size="21" fill="#ffa657" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.build/docs/</text>
<g font-size="15" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace"><text x="72" y="676">html/*.html</text><text x="72" y="704">html/assets/</text><text x="72" y="732">html/_media/</text><text x="72" y="760">site-build.json</text></g>
</g>
</svg>
<figcaption>Figure 1 redrawn with the paths that its reading notes name</figcaption>
</figure>
<ul class="fx-never">
<li><b>An untracked file is not read</b><p>A stray local file cannot leak onto the site, and a file you forgot to add fails the build.</p></li>
<li><b>An edit to the output is lost</b><p>The next build overwrites it. Fix the source and rebuild; <code>build --check</code> confirms nothing else is stale.</p></li>
</ul>
</div>
<p class="slide-scope">Illustration of the build · no measured results</p>
<!-- /slide -->

## One command turns your tracked Markdown into a checked, self-contained site

<p class="bs-lead"><code>docsite.py build</code> reads the project's tracked sources through the pinned kit and writes plain HTML into <code>.build/docs/</code>; that output is never edited.</p>

<div class="bs-grid g2">
<figure id="fig-build">
<svg class="inline-fig" viewBox="0 0 600 400" role="img" aria-label="docsite.py build reads only the project&#x27;s tracked sources, pages, records, site.toml, figures and media, through the pinned kit, which renders them with the reader, theme, fonts and math and checks links. An untracked file is not read. The build writes plain HTML, assets and a manifest into .build/docs. Output never flows back into source.">
<rect x="8" y="8" width="330" height="140" rx="12" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="26" y="42" font-size="26" fill="#39d2c0" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">tracked in Git</text>
<text x="26" y="76" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">pages and records</text>
<text x="26" y="105" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">site.toml</text>
<text x="26" y="134" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">figures and media</text>
<rect x="370" y="8" width="222" height="104" rx="12" fill="none" stroke="#7d8896" stroke-width="2" stroke-dasharray="9 7"/>
<text x="481" y="48" font-size="25" fill="#a9b4c2" text-anchor="middle" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">untracked file</text>
<text x="481" y="84" font-size="25" fill="#ff7b72" text-anchor="middle" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">not read</text>
<path d="M481 112V136" stroke="#7d8896" stroke-width="3" stroke-dasharray="6 6"/>
<circle cx="481" cy="156" r="19" fill="#0d1117" stroke="#ff7b72" stroke-width="3"/><path d="M473 148L489 164M489 148L473 164" stroke="#ff7b72" stroke-width="3.5" stroke-linecap="round"/>
<path d="M173 148 L173 182" stroke="#a9b4c2" stroke-width="3" fill="none"/><path d="M173 196L180.0 182.0L166.0 182.0Z" fill="#a9b4c2"/>
<rect x="84" y="196" width="508" height="84" rx="12" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="102" y="230" font-size="26" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">docsite.py build</text>
<text x="102" y="264" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">pinned kit: reader, theme, checks</text>
<path d="M300 280 L300 301" stroke="#a9b4c2" stroke-width="3" fill="none"/><path d="M300 312L305.5 301.0L294.5 301.0Z" fill="#a9b4c2"/>
<rect x="130" y="312" width="462" height="84" rx="12" fill="none" stroke="#ffa657" stroke-width="2" stroke-dasharray="9 7"/>
<text x="150" y="346" font-size="28" fill="#ffa657" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.build/docs/</text>
<text x="150" y="382" font-size="25" fill="#a9b4c2" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">HTML, assets, manifest</text>
<path d="M130 354 L40 354 L40 162" stroke="#ff7b72" stroke-width="3" fill="none" stroke-dasharray="10 8"/><path d="M40 148L33.0 162.0L47.0 162.0Z" fill="#ff7b72"/>
<circle cx="40" cy="238" r="19" fill="#0d1117" stroke="#ff7b72" stroke-width="3"/><path d="M32 230L48 246M48 230L32 246" stroke="#ff7b72" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="316" cy="30" r="22" fill="#0d1117" stroke="#39d2c0" stroke-width="3"/><text x="316" y="39" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">01</text>
<circle cx="570" cy="218" r="22" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/><text x="570" y="227" font-size="25" fill="#bc8cff" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">02</text>
<circle cx="570" cy="334" r="22" fill="#0d1117" stroke="#ffa657" stroke-width="3"/><text x="570" y="343" font-size="25" fill="#ffa657" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">03</text>
</svg>
<figcaption><b>Figure 1.</b> Follow the arrows from what you write to what readers get: only tracked sources are read, and output never flows back. This illustrative SVG diagram is authored in the page source and contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-teal"><span class="bs-label">Read the figure</span><h3>Tracked sources in, a generated site out</h3><ol>
<li>read, if Git tracks them: topic pages under <code>docs/topics/</code>, Markdown records, <code>docs/site/site.toml</code>, figures and media</li>
<li>rendered by the pinned kit, with the reader, theme, fonts and math; links rewritten and checked</li>
<li>written as pages with <code>assets/</code> and <code>_media/</code> under <code>.build/docs/html/</code>, beside <code>site-build.json</code>; Git ignores <code>.build/</code></li>
</ol><p>The crosses mark what never happens. To change a page, change its source, the configuration or a generator, and rebuild.</p></div>
</div>

[Figure 1](#fig-build) is the whole pipeline. Generated output can always be deleted and rebuilt, so a reviewer only looks at sources. Only tracked files are read, so what you publish is what is in Git: a stray local file cannot leak onto the site, and a file you forgot to add fails the build instead of leaving a broken image. No web framework or JavaScript install is needed; the reader, theme, fonts and math come from the pinned kit ([tooling and ownership](authoring.html#tooling-and-ownership)).

<!-- fold: detail How links are rewritten -->

A page body links from the generated page: `records.html#numbers-and-staleness` reaches a page, `../topics/guide/guide.md` a record. A link to another repository file becomes a source link on `gh_repo`; with `gh_repo = ""` it keeps its local path. A link, include or image that leaves the project fails the build, and lint checks every link to a repository file, in Markdown or an HTML `href` ([authoring paths](authoring.html#authoring-paths)).

<!-- /fold -->

</section>

<section class="card" id="write-a-topic-page">

## A topic page explains its record, one claim per chapter

<p class="bs-lead">The record comes first; when a person asks for a page, add <code>docs/topics/&lt;name&gt;/index.md</code> beside it, write one chapter per claim and give the page a <code>[[nav]]</code> entry.</p>

<figure id="fig-topic-page">
<div class="bs-flow" role="img" aria-label="The topic record holds the facts. The page file beside it has frontmatter and a nav entry and holds one chapter per claim: a heading that states the claim, a lead sentence, a visual, optional folds and an optional slide face. The build turns each chapter into a reader chapter; text above the first chapter joins the first chapter.">
<div class="bs-node bs-teal"><span class="bs-label">Facts</span><b>Record</b><ul><li><code>docs/topics/guide/guide.md</code></li><li>written by whoever did the work</li><li>a page without one declares <code>page_only</code></li></ul></div>
<div class="bs-arrow"><span>explained by</span></div>
<div class="bs-node bs-violet"><span class="bs-label">One file</span><b>Page</b><ul><li><code>docs/topics/guide/index.md</code>, frontmatter <code>title</code>, <code>toc</code>, <code>description</code></li><li>a <code>[[nav]]</code> entry in <code>site.toml</code></li><li>one chapter per claim: a <code>##</code> heading or a <code>section.card</code>, a lead sentence, its visual, optional folds and slide face</li></ul></div>
<div class="bs-arrow"><span>build</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Generated</span><b>Reader page</b><ul><li><code>guide.html</code></li><li>one reader chapter per chapter</li><li>text above the first chapter joins it</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> From the record to the reader: the parts of a topic page and what each becomes. This diagram contains no measured results.</figcaption>
</figure>

[Figure 2](#fig-topic-page) reads left to right. The page explains its record for a person and never adds a rule, number or limit the record lacks ([record first, page on request](documentation-system.html#record-first-page-on-request)). A [chapter](page-design.html#page-design) is one `##` section, or a `<section class="card" id="…">` when you want control over its contents; its heading states the takeaway and its lead the claim, so the menu and the first line carry the argument. The reader's question decides which chapters a page needs; the [page types](page-design.html#page-types) give a default order for each kind of question.

Text above the first chapter states no point in a heading: the reader puts it into the first chapter, and strict lint warns until you move it into a chapter or keep it with `opening = "keep"`.

A minimal page, beside its record `docs/topics/release-checklist/release-checklist.md`:

```markdown
+++
title = "Release checklist"
description = "What to check before tagging a release."
components = ["toc", "nav"]
page_css = ["build-sheet.css"]
toc = []
+++

# Release checklist

<section class="card" id="tag-only-tested-commits">

## Tag only a commit whose checks passed

<p class="bs-lead">Run the full checks on the exact commit, then tag it.</p>

…the visual that shows the claim, the reason, optional folds…

</section>
```

<!-- fold: code Frontmatter keys and where a page lives -->

`title` and `toc` are required; `toc = []` takes the menu labels from the chapters, and `[label, "#id"]` pairs set short ones. `description` is the home-page card text, `components` loads shared behaviour such as `lightbox` or `carousel`, `page_css = ["build-sheet.css"]` enables the figure blocks used here, `math = true` renders formulas and `hidden = true` keeps the page out of the menu. The folder gives the address: `docs/topics/guide/index.md` becomes `guide.html`, also from a group folder that `topic_group_folders` names ([authoring paths](authoring.html#authoring-paths), [topic group folders](authoring.html#topic-group-folders)).

<!-- /fold -->

</section>

<section class="card" id="the-reader">

## Readers move chapter by chapter, keep the menu docked and pin a reference

<p class="bs-lead">Every topic page becomes a row of chapter cards; readers choose one, two or all chapters and open optional depth only when they want it.</p>

<div class="bs-grid g2">
<figure id="fig-reader">
<svg class="inline-fig" viewBox="0 0 600 440" role="img" aria-label="The reader at a wide window, drawn as a sketch with eleven numbered parts. Left, the docked sidebar: 1 the site name with the button that hides it, 2 the row of six icons, 3 navigation groups that fold, 4 the page's chapter list, 5 the Reference section, 6 Also show with its switches, 7 the foot with the repository link, the kit version and the build time. Right, the stage: 8 the chapter card with its neighbours at the edges, 9 a slide face standing alone in the chapter's first view, 10 the stepper at the bottom centre, 11 the Full chapter row with Continue reading.">
<rect x="2" y="2" width="180" height="436" rx="12" fill="#121a24" stroke="#30363d" stroke-width="2"/>
<rect x="16" y="16" width="26" height="26" rx="7" fill="#0f1d22" stroke="#39d2c0" stroke-width="2"/>
<rect x="52" y="24" width="48" height="10" rx="5" fill="#a9b4c2"/>
<rect x="140" y="14" width="30" height="30" rx="7" fill="none" stroke="#7d8896" stroke-width="2"/>
<path d="M156 23l-6 6 6 6M164 23l-6 6 6 6" fill="none" stroke="#a9b4c2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="16" y="58" width="18" height="22" rx="5" fill="#39d2c0" fill-opacity=".35" stroke="#39d2c0" stroke-width="2"/>
<g fill="none" stroke="#7d8896" stroke-width="2"><rect x="38" y="58" width="18" height="22" rx="5"/><rect x="60" y="58" width="18" height="22" rx="5"/><rect x="82" y="58" width="18" height="22" rx="5"/><rect x="104" y="58" width="18" height="22" rx="5"/><rect x="126" y="58" width="18" height="22" rx="5"/></g>
<rect x="16" y="100" width="10" height="10" rx="2" fill="none" stroke="#39d2c0" stroke-width="2"/><rect x="32" y="101" width="60" height="8" rx="4" fill="#39d2c0" fill-opacity=".75"/>
<path d="M120 102l6 6 6-6" fill="none" stroke="#39d2c0" stroke-width="2.5" stroke-linecap="round"/>
<g fill="#a9b4c2" fill-opacity=".8"><rect x="24" y="122" width="100" height="9" rx="4"/><rect x="24" y="140" width="80" height="9" rx="4"/></g>
<rect x="14" y="154" width="128" height="20" rx="5" fill="#1c2a33"/><rect x="24" y="160" width="84" height="9" rx="4" fill="#e6edf3"/>
<circle cx="30" cy="190" r="6" fill="#39d2c0"/><circle cx="30" cy="208" r="5" fill="none" stroke="#7d8896" stroke-width="2"/><circle cx="30" cy="226" r="5" fill="none" stroke="#7d8896" stroke-width="2"/><circle cx="30" cy="244" r="5" fill="none" stroke="#7d8896" stroke-width="2"/>
<g fill="#a9b4c2" fill-opacity=".7"><rect x="42" y="186" width="90" height="8" rx="4"/><rect x="42" y="204" width="70" height="8" rx="4"/><rect x="42" y="222" width="84" height="8" rx="4"/><rect x="42" y="240" width="60" height="8" rx="4"/></g>
<rect x="16" y="266" width="10" height="10" rx="2" fill="none" stroke="#bc8cff" stroke-width="2"/><rect x="32" y="267" width="56" height="8" rx="4" fill="#bc8cff" fill-opacity=".75"/>
<path d="M121 265l6 6-6 6" fill="none" stroke="#bc8cff" stroke-width="2.5" stroke-linecap="round"/>
<rect x="16" y="294" width="70" height="8" rx="4" fill="#7d8896"/><g fill="#7d8896" fill-opacity=".6"><rect x="26" y="310" width="96" height="7" rx="3.5"/><rect x="26" y="324" width="76" height="7" rx="3.5"/></g>
<path d="M10 342H174" stroke="#30363d" stroke-width="2"/>
<rect x="16" y="352" width="54" height="8" rx="4" fill="#7d8896"/><rect x="104" y="349" width="30" height="15" rx="7.5" fill="none" stroke="#7d8896" stroke-width="2"/><circle cx="112" cy="356.5" r="4" fill="#7d8896"/>
<g fill="none" stroke="#7d8896" stroke-width="2"><rect x="16" y="370" width="38" height="16" rx="8"/><rect x="60" y="370" width="38" height="16" rx="8"/><rect x="104" y="370" width="38" height="16" rx="8"/></g>
<rect x="16" y="398" width="88" height="7" rx="3.5" fill="#39d2c0"/><rect x="16" y="411" width="124" height="7" rx="3.5" fill="#39d2c0"/><rect x="16" y="424" width="100" height="7" rx="3.5" fill="#7d8896"/>
<rect x="192" y="44" width="16" height="352" rx="8" fill="#121a24" stroke="#30363d" stroke-width="2"/>
<rect x="584" y="44" width="14" height="352" rx="7" fill="#121a24" stroke="#30363d" stroke-width="2"/>
<rect x="214" y="6" width="364" height="428" rx="14" fill="#10161f" stroke="#39d2c0" stroke-width="2.5"/>
<rect x="236" y="76" width="320" height="180" rx="8" fill="#17142a" stroke="#bc8cff" stroke-width="2"/>
<rect x="254" y="94" width="60" height="7" rx="3.5" fill="#bc8cff"/><rect x="254" y="108" width="220" height="13" rx="6.5" fill="#e6edf3"/>
<rect x="258" y="146" width="76" height="76" rx="8" fill="none" stroke="#39d2c0" stroke-width="2"/><rect x="360" y="146" width="76" height="76" rx="8" fill="none" stroke="#bc8cff" stroke-width="2"/><rect x="462" y="146" width="76" height="76" rx="8" fill="none" stroke="#ffa657" stroke-width="2" stroke-dasharray="6 4"/>
<path d="M338 184h16M440 184h16" stroke="#a9b4c2" stroke-width="2.5"/>
<path d="M226 362H566" stroke="#30363d" stroke-width="2"/>
<rect x="228" y="378" width="62" height="22" rx="11" fill="none" stroke="#39d2c0" stroke-width="2"/><rect x="298" y="386" width="28" height="6" rx="3" fill="#7d8896"/>
<rect x="336" y="370" width="120" height="40" rx="20" fill="#0d1117" stroke="#7d8896" stroke-width="2"/>
<path d="M360 390h-12m5-5l-5 5 5 5M432 390h12m-5-5l5 5-5 5" fill="none" stroke="#e6edf3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="372" y="384" width="48" height="12" rx="6" fill="#a9b4c2" fill-opacity=".7"/>
<rect x="464" y="374" width="104" height="32" rx="16" fill="none" stroke="#39d2c0" stroke-width="2"/><rect x="476" y="386" width="56" height="8" rx="4" fill="#39d2c0" fill-opacity=".7"/><path d="M550 383v12m-5-5l5 5 5-5" fill="none" stroke="#39d2c0" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<g font-family="'IBM Plex Sans',system-ui,sans-serif" font-size="26" font-weight="700" fill="#ffa657" text-anchor="middle">
<g fill="#0d1117" stroke="#ffa657" stroke-width="2.5"><circle cx="120" cy="29" r="18"/><circle cx="164" cy="69" r="18"/><circle cx="164" cy="116" r="18"/><circle cx="160" cy="216" r="18"/><circle cx="160" cy="312" r="18"/><circle cx="160" cy="378" r="18"/><circle cx="160" cy="416" r="18"/><circle cx="238" cy="36" r="18"/><circle cx="556" cy="76" r="18"/><circle cx="396" cy="346" r="18"/><circle cx="259" cy="346" r="18"/></g>
<text x="120" y="37">1</text><text x="164" y="77">2</text><text x="164" y="124">3</text><text x="160" y="224">4</text><text x="160" y="320">5</text><text x="160" y="386">6</text><text x="160" y="424">7</text><text x="238" y="44">8</text><text x="556" y="84">9</text><text x="396" y="354" font-size="26">10</text><text x="259" y="354" font-size="26">11</text>
</g>
</svg>
<figcaption><b>Figure 3.</b> The reader at a wide window, on a chapter that opens with a slide face. A sketch drawn in the page source from the reader that the kit ships; it contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-teal"><span class="bs-label">Read the figure</span><h3>Sidebar on the left, one chapter on the stage</h3><ol>
<li>The site's name; <code>«</code> hides the docked menu, <code>☰</code> docks it again.</li>
<li>Icons: One chapter, Two chapters, All chapters, Presentation on a page with a slide face, About, Help.</li>
<li>Navigation groups open and close; those that <code>folded_groups</code> names start closed.</li>
<li>This page's chapters, by <code>toc</code> label.</li>
<li>Reference: the records rendered whole.</li>
<li>Also show: a switch per kind of fold, and All.</li>
<li>The foot: the repository from <code>gh_repo</code>, the kit version and the time of the last build.</li>
<li>The chapter fills 89.8% of the stage; click a neighbour at the edge, or swipe, to turn it.</li>
<li>A slide face stands alone in the first view; the headline follows below.</li>
<li>The stepper: previous, position, next.</li>
<li>Full chapter, reading time and Continue reading, while the chapter is at its top.</li>
</ol></div>
</div>

[Figure 3](#fig-reader) answers two ways long pages fail readers: the point scrolls away under detail, or a definition disappears while you read its use. One chapter keeps one claim on the stage. **Two chapters** holds a definition beside its use: choose it, press `⌖` on this chapter's strip, then <kbd>→</kbd>. **All chapters** reads as one document, its slide faces hidden until **Slides** shows them. **Presentation** fills the window with each chapter's slide, or with a title card from its headline and lead.

Depth lives in folds that start closed: a switch under Also show opens every fold of its kind, All opens every fold, those of no kind too, a reader's own click on a fold is remembered, and printing opens them all. A `[theme_colors]` table gives the reader a project's own colours; the build refuses colours below 4.5:1 for text or 3:1 for marks ([theme colours](authoring.html#theme-colours)). [Shared reading layout](reader.html#shared-reading-layout) owns all of it.

<!-- fold: code The settings and fold markers behind it -->

This site turns the reader on; `folded_groups = ["releases"]` would start that menu group closed, and `kit_link = false` would drop the kit line from the foot.

```toml source=docs/site/site.toml#L4-L7
title = "Documentation kit"
gh_repo = "https://github.com/davszi/documentation-kit"
gh_ref = "main"
chapter_reader = true
```

A fold is `<!-- fold: math Title -->` … `<!-- /fold -->`, with `experiment`, `code` or `dead-end` (shown as Not chosen) in place of `math`, or `detail` for optional detail of no kind; `(open)` after the kind starts it open ([reading layers](explanations.html#story-and-reading-layers)).

<!-- /fold -->

<!-- fold: dead-end Why not one long scroll -->

A single scroll is still there as **All chapters**, and print and readers without JavaScript get it. As the default it would lose one claim per screen and a reference beside its use; `build --check-reader` proves the reader changes none of a page's content.

<!-- /fold -->

</section>

<section class="card" id="figures-and-slides">

## Figures come from the page source; slide faces turn chapters into a deck

<p class="bs-lead">Diagrams are HTML or SVG written in the page, generated figures come from a script over tracked data, and a chapter that has something to show can open with a slide built around its figure.</p>

<figure id="fig-captures">
<div class="fig-carousel">
<img src="../topics/build-a-site/media/showcase/environment-face.webp" alt="Slide face from the adaptation project: four contributions, drawn head to tail, add up to the next velocity.">
<img src="../topics/build-a-site/media/showcase/environment-reader.webp" alt="Its chapter in the reader: the sum built over four panels, one contribution in each.">
<img src="../topics/build-a-site/media/showcase/families-face.webp" alt="Slide face from the adaptation project: one law written large, with each family under the part it rewrites.">
<img src="../topics/build-a-site/media/showcase/families-reader.webp" alt="Its chapter in the reader: the law with the catalog of families under its parts.">
<img src="../topics/build-a-site/media/showcase/supervised-face.webp" alt="Slide face from the adaptation project: supervised training as a flow from the rows of each cursor to one loss.">
<img src="../topics/build-a-site/media/showcase/supervised-reader.webp" alt="Its chapter in the reader: one supervised update, from the rows of each cursor to one loss.">
<img src="../topics/build-a-site/media/showcase/adaptation-focused-face.webp" alt="Slide face from the adaptation project: adaptation-focused training, where a copy practises before it is scored.">
<img src="../topics/build-a-site/media/showcase/adaptation-focused-reader.webp" alt="Its chapter in the reader: one adaptation-focused update, with a copy and its practice steps for each cursor.">
<img src="../topics/build-a-site/media/showcase/step-face.webp" alt="Slide face from the adaptation project: a step too large overshoots the valley, beside the values of a real failed run.">
<img src="../topics/build-a-site/media/showcase/step-reader.webp" alt="Its chapter in the reader: the error valley with steps of four sizes, and the table of their results.">
<img src="../topics/build-a-site/media/showcase/against-reference-face.webp" alt="Slide face from the adaptation project: a direct polynomial fit compared with the neural settings on six laws.">
<img src="../topics/build-a-site/media/showcase/against-reference-reader.webp" alt="Its chapter in the reader: the mean error for each of six laws, the neural settings beside the direct fit.">
</div>
<figcaption><b>Figure 4.</b> Six chapters of the adaptation project in a carousel: each slide face, then its chapter in the reader, scrolled to its main figure. They are examples of what a project can build with the kit, not templates. They were captured from that project at its commit <code>d22ef36</code>, the slide faces on 2026-11-25 and the reader pictures again on 2026-11-26 with the reader of 5.7.0, and are not maintained; the text and numbers are the project's. The carousel advances by itself and pauses on hover; click a picture to open it full screen, scroll to zoom, drag to pan, <kbd>Esc</kbd> to close.</figcaption>
</figure>

[Figure 4](#fig-captures) shows what a face is for: one finding, drawn, with the whole argument in the chapter below. The pairs show, in order: a sum built step by step, a formula's terms as the visual, twin chapters drawn in one visual language, a failed run drawn only where values were recorded, and a result beside the one law where it stops holding.

<div class="bs-grid g2">
<figure id="fig-figure-paths">
<svg class="inline-fig" viewBox="0 0 600 582" role="img" aria-label="Panel A, a generated figure: a generator reads tracked data and asserts the values its page states, then write_both writes name.svg in the dark theme, which pages show, and name.light.svg in the light theme for slides and print; --check compares both and writes nothing. Panel B, a slide face: a face between slide markers opens its chapter with one finding whose numbers the chapter also states; the reader shows the face alone first, and slides --select collects faces into a deck.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif" font-size="26">
<text x="2" y="31" fill="#39d2c0" font-weight="600" letter-spacing="1" font-family="'IBM Plex Mono',ui-monospace,monospace">A · GENERATED FIGURE</text>
<rect x="2" y="42" width="596" height="82" rx="12" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="20" y="74" fill="#e6edf3"><tspan fill="#39d2c0" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">generator</tspan> reads tracked data</text>
<text x="20" y="108" fill="#a9b4c2">and asserts the values its page states</text>
<path d="M300 124V152M147 152H453M147 152V160M453 152V160" fill="none" stroke="#a9b4c2" stroke-width="3"/><path d="M147 168l-7-10h14zM453 168l-7-10h14z" fill="#a9b4c2"/>
<text x="312" y="143" fill="#a9b4c2" font-family="'IBM Plex Mono',ui-monospace,monospace">write_both</text>
<rect x="2" y="168" width="290" height="94" rx="12" fill="none" stroke="#ffa657" stroke-width="2.5"/>
<text x="20" y="204" fill="#ffa657" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">name.svg</text>
<text x="20" y="242" fill="#e6edf3">dark: pages show it</text>
<rect x="308" y="168" width="290" height="94" rx="12" fill="none" stroke="#ffa657" stroke-width="2.5" stroke-dasharray="9 6"/>
<text x="326" y="204" fill="#ffa657" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">name.light.svg</text>
<text x="326" y="242" fill="#e6edf3">light: slides, print</text>
<text x="2" y="298" fill="#a9b4c2"><tspan fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">--check</tspan> compares both, writes nothing</text>
<path d="M2 320H598" stroke="#30363d" stroke-width="2"/>
<text x="2" y="358" fill="#bc8cff" font-weight="600" letter-spacing="1" font-family="'IBM Plex Mono',ui-monospace,monospace">B · SLIDE FACE</text>
<rect x="2" y="370" width="596" height="82" rx="12" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="20" y="402" fill="#e6edf3"><tspan fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">&lt;!-- slide --&gt;</tspan> opens the chapter</text>
<text x="20" y="436" fill="#a9b4c2">one finding; its numbers are in the chapter</text>
<path d="M300 452V476M147 476H453M147 476V484M453 476V484" fill="none" stroke="#a9b4c2" stroke-width="3"/><path d="M147 492l-7-10h14zM453 492l-7-10h14z" fill="#a9b4c2"/>
<rect x="2" y="492" width="290" height="88" rx="12" fill="none" stroke="#bc8cff" stroke-width="2.5"/>
<text x="20" y="526" fill="#bc8cff" font-weight="600">reader</text>
<text x="20" y="562" fill="#e6edf3">the face alone first</text>
<rect x="308" y="492" width="290" height="88" rx="12" fill="none" stroke="#bc8cff" stroke-width="2.5" stroke-dasharray="9 6"/>
<text x="326" y="526" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">slides --select</text>
<text x="326" y="562" fill="#e6edf3">a deck to present</text>
</g>
</svg>
<figcaption><b>Figure 5.</b> Where a figure and a face go. Panel A: a generated figure, written in both themes. Panel B: a slide face, shown in the reader and collected into a deck. This diagram contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-orange"><span class="bs-label">Slide faces</span><h3>A face is a view of its chapter</h3><ul>
<li>added last, and only after the person says yes</li>
<li>one finding and the visual that shows it; this page's face redraws Figure 1 across the canvas</li>
<li>boxes of text are not a visual: a chapter with nothing to show gets no face</li>
<li>lint fails on a second face in a chapter and warns on a number the chapter lacks, unless a <code>data-face-only</code> mark gives the reason</li>
</ul></div>
</div>

Flows and diagrams are HTML or SVG in the page source; images are tracked files that the build packages. A claim that needs a figure gets one, drawn from data, code or geometry that exists, never from invented numbers ([figures and comparisons](figures.html#figures-and-comparisons)). In Panel A of [Figure 5](#fig-figure-paths), one run of a script writes the dark file the page shows and a light one for slides and print, and its `--check` runs in the project's checks ([generated figures](authoring.html#generated-figures)). Panel B is a [slide face](page-design.html#slide-faces), written between `<!-- slide -->` and `<!-- /slide -->` at the start of its chapter:

```bash
python .docs-kit/docsite.py slides --project . --select build-a-site --out overview
python .docs-kit/docsite.py slides --project . --select guide --select other#intro,result --out review --title "Review"
```

`slides` builds the site and collects the faces of the selected chapters into `.build/slides/<name>.html`: a bare slug takes every face in reading order, `slug#a,b` those chapters in that order ([slide faces and decks](authoring.html#slide-faces-and-decks)).

<!-- fold: math How the label size of a drawing is measured -->

A drawing scales to its column, and its labels with it. A label of size $f$ in a drawing $V$ units wide, shown $w$ pixels wide, renders at

$$
s = f \cdot \frac{w}{V} \;\ge\; 11\ \text{px}
$$

which is what the [browser check](validation.html#reusable-browser-checks) reads. Figure 1 is drawn `600` units wide with labels of `25`; shown `300` pixels wide they render at half that size, above the limit, while a label of `20` would fall below it. A face's own text is exempt: it scales with the face ([page design](page-design.html#page-design)).

<!-- /fold -->

</section>

<section class="card" id="existing-markdown">

## Markdown you already have can be published as it is

<p class="bs-lead">By default every tracked Markdown file under <code>docs/</code> becomes a Reference page at an address derived from its path; a <code>[[source_pages]]</code> table publishes a file at an address you choose. The file stays where it is.</p>

<div class="bs-grid g2">
<figure id="fig-listing">
<svg class="inline-fig" viewBox="0 0 600 470" role="img" aria-label="A tracked Markdown file is listed when it lies under a reference_roots entry, docs by default, and is not inside a submodule, dot-named, a file with +++ frontmatter, a symbolic link or declared private; it then becomes a Reference page at a route from its path, such as docs.x.md.html. Otherwise it is not listed. A [[source_pages]] table that names a file registers it whatever the listing decides, with its own slug, title and pin and strict checks.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif" font-size="26">
<rect x="150" y="2" width="300" height="48" rx="24" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="300" y="34" fill="#e6edf3" text-anchor="middle">tracked <tspan font-family="'IBM Plex Mono',ui-monospace,monospace">.md</tspan> file</text>
<path d="M240 50V72" stroke="#a9b4c2" stroke-width="3"/><path d="M240 80l-7-10h14z" fill="#a9b4c2"/>
<rect x="48" y="80" width="384" height="84" rx="10" fill="#121a24" stroke="#a9b4c2" stroke-width="2"/>
<text x="64" y="114" fill="#e6edf3">listed in <tspan font-family="'IBM Plex Mono',ui-monospace,monospace">reference_roots</tspan>?</text>
<text x="64" y="148" fill="#a9b4c2">default: <tspan font-family="'IBM Plex Mono',ui-monospace,monospace">docs</tspan></text>
<path d="M432 122H480" stroke="#7d8896" stroke-width="3"/><path d="M488 122l-10-7v14z" fill="#7d8896"/>
<text x="458" y="112" fill="#a9b4c2" text-anchor="middle">no</text>
<rect x="490" y="80" width="108" height="84" rx="10" fill="none" stroke="#7d8896" stroke-width="2" stroke-dasharray="7 5"/>
<text x="544" y="114" fill="#a9b4c2" text-anchor="middle">not</text><text x="544" y="146" fill="#a9b4c2" text-anchor="middle">listed</text>
<path d="M240 164V188" stroke="#a9b4c2" stroke-width="3"/><path d="M240 196l-7-10h14z" fill="#a9b4c2"/>
<text x="254" y="186" fill="#a9b4c2">yes</text>
<rect x="48" y="196" width="384" height="116" rx="10" fill="#121a24" stroke="#a9b4c2" stroke-width="2"/>
<text x="64" y="228" fill="#e6edf3">in a submodule, dot-named,</text>
<text x="64" y="258" fill="#e6edf3"><tspan font-family="'IBM Plex Mono',ui-monospace,monospace">+++</tspan> frontmatter, a symlink,</text>
<text x="64" y="288" fill="#e6edf3">or declared private?</text>
<path d="M432 254H480" stroke="#7d8896" stroke-width="3"/><path d="M488 254l-10-7v14z" fill="#7d8896"/>
<text x="458" y="244" fill="#a9b4c2" text-anchor="middle">yes</text>
<rect x="490" y="196" width="108" height="116" rx="10" fill="none" stroke="#7d8896" stroke-width="2" stroke-dasharray="7 5"/>
<text x="544" y="246" fill="#a9b4c2" text-anchor="middle">not</text><text x="544" y="278" fill="#a9b4c2" text-anchor="middle">listed</text>
<path d="M400 312V350" stroke="#ffa657" stroke-width="3"/><path d="M400 358l-7-10h14z" fill="#ffa657"/>
<text x="414" y="342" fill="#a9b4c2">no</text>
<rect x="306" y="360" width="292" height="106" rx="12" fill="#1d1710" stroke="#ffa657" stroke-width="2.5"/>
<text x="322" y="392" fill="#ffa657" font-weight="600">Reference page</text>
<text x="322" y="422" fill="#e6edf3">named after its path</text>
<text x="322" y="452" fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">docs.x.md.html</text>
<path d="M150 26H18V352" fill="none" stroke="#bc8cff" stroke-width="3"/><path d="M18 360l-7-10h14z" fill="#bc8cff"/>
<text transform="translate(42 250) rotate(-90)" fill="#bc8cff" text-anchor="middle">a table names it</text>
<rect x="2" y="360" width="290" height="106" rx="12" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="18" y="392" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">[[source_pages]]</text>
<text x="18" y="422" fill="#e6edf3">its own slug, title,</text>
<text x="18" y="452" fill="#e6edf3">pin; strict checks</text>
</g>
</svg>
<figcaption><b>Figure 6.</b> Which tracked Markdown files become pages. The automatic listing runs down the middle; a <code>[[source_pages]]</code> table, on the left, registers the file it names whatever the listing decides. This diagram contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-orange"><span class="bs-label">Listed or registered</span><h3>Two ways a record becomes a page</h3><ul>
<li><b>Listed</b>, by default: an address from its path, which changes when the file moves. A missing link target shows as plain text and lint prints a note; a listed page never fails the build.</li>
<li><b>Registered</b> with a <code>[[source_pages]]</code> table: its own slug, title, description and pin, chapters with <code>reader = true</code>, and the strict checks of every page.</li>
</ul></div>
</div>

<figure id="fig-two-readers">
<div class="panel-switcher" data-panel-switcher data-panel-default="markdown">
<div class="panel-switcher-controls" role="group" aria-label="View of a registered record">
<button type="button" data-panel-choice="markdown" aria-pressed="false" aria-controls="view-markdown">As agents read it</button>
<button type="button" data-panel-choice="page" aria-pressed="false" aria-controls="view-page">As this site renders it</button>
</div>
<div id="view-markdown" data-panel="markdown">

```markdown source=rules/experiments/workflow.md#L39-L41
- A **qualification** gives a pass, fail or inconclusive verdict on a named
  system, build or model: platform qualification, a benchmark contract, a
  parity check, model release evaluation.
```

</div>
<div id="view-page" data-panel="page">
<div class="bs-part bs-orange"><span class="bs-label">Illustration · not the rendered page</span><ul><li>A <b>qualification</b> gives a pass, fail or inconclusive verdict on a named system, build or model: platform qualification, a benchmark contract, a parity check, model release evaluation.</li></ul><p>The site renders these lines on the page of <code>rules/experiments/workflow.md</code>, under its heading Choose the purpose. <a href="experiment-workflow.html#choose-the-purpose">Open them there</a>.</p></div>
</div>
</div>
<figcaption><b>Figure 7.</b> One registered file, two readers. The first view is an excerpt that lint checks against the file; the second is written in this page to illustrate, and its link opens the real render.</figcaption>
</figure>

A copy of a rule, a README or release notes drifts, and moving the file breaks the links and agent routes that name its path. [Figure 6](#fig-listing) shows how the kit renders the file in place instead, so [Figure 7](#fig-two-readers) is one file that agents and people read at one path. The listing is broad on purpose, and that is its risk: in a private repository with a public site, every tracked Markdown file of a listed folder is published unless it is declared private ([automatic reference listing](authoring.html#automatic-reference-listing)). Write a topic page to explain; register a record when the file itself is the thing to read.

<!-- fold: code The registry entry -->

```toml
[[source_pages]]
source = "docs/notes/decision.md"   # required: a tracked file inside the project
slug = "decision"                   # required: the page is decision.html
title = "Decision record"           # optional: defaults to the file's first # heading
description = "Why we chose …"      # optional: card text and sidebar tooltip
pinned = true                       # optional: listed first in the Reference section
reader = true                       # optional: chapter cards instead of one scroll
math = true                         # optional: render formulas
```

One slug belongs to one page. With `reader = true`, the file's opening joins its first chapter together with the source line; there is no Introduction chapter. [Registered source pages](authoring.html#registered-source-pages) owns the contract.

<!-- /fold -->

</section>

<section class="card" id="build">

## Build writes the site; check runs the whole gate before a push

<p class="bs-lead">Run <code>build</code> after changing a source, and <code>check</code> before a push: it builds, lints strictly, tries a publish and runs the project's own checks, and stops at the first failure.</p>

<div class="bs-grid g2">
<figure id="fig-check">
<svg class="inline-fig" viewBox="0 0 600 556" role="img" aria-label="git push runs hooks/pre-push, which calls docsite.py check. check runs four steps in order: 1 build, so that lint reads a fresh site; 2 lint --strict, where warnings fail too; 3 a trial publish, only with a [publication] table; 4 the project's own checks from site.toml, in the order written. A failure stops the run at that step; when all pass, the push goes on.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif" font-size="26">
<rect x="2" y="2" width="170" height="52" rx="26" fill="none" stroke="#7d8896" stroke-width="2.5"/>
<text x="87" y="37" fill="#e6edf3" text-anchor="middle" font-family="'IBM Plex Mono',ui-monospace,monospace">git push</text>
<path d="M172 28H220" stroke="#a9b4c2" stroke-width="3"/><path d="M228 28l-10-7v14z" fill="#a9b4c2"/>
<rect x="230" y="2" width="368" height="52" rx="12" fill="none" stroke="#7d8896" stroke-width="2.5"/>
<text x="248" y="37" fill="#a9b4c2"><tspan fill="#e6edf3" font-family="'IBM Plex Mono',ui-monospace,monospace">hooks/pre-push</tspan> calls</text>
<path d="M414 54V80" stroke="#a9b4c2" stroke-width="3"/><path d="M414 88l-7-10h14z" fill="#a9b4c2"/>
<rect x="2" y="88" width="596" height="388" rx="14" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="20" y="126" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">docsite.py check</text>
<g fill="#0d1117" stroke="#30363d" stroke-width="2"><rect x="18" y="142" width="564" height="74" rx="10"/><rect x="18" y="224" width="564" height="74" rx="10"/><rect x="18" y="306" width="564" height="74" rx="10"/><rect x="18" y="388" width="564" height="74" rx="10"/></g>
<g fill="#0d1117" stroke="#bc8cff" stroke-width="2.5"><circle cx="48" cy="179" r="18"/><circle cx="48" cy="261" r="18"/><circle cx="48" cy="343" r="18"/><circle cx="48" cy="425" r="18"/></g>
<g fill="#bc8cff" font-weight="600" text-anchor="middle"><text x="48" y="188">1</text><text x="48" y="270">2</text><text x="48" y="352">3</text><text x="48" y="434">4</text></g>
<g fill="#e6edf3" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace"><text x="80" y="174">build</text><text x="80" y="256">lint --strict</text><text x="80" y="338">publish, a trial</text><text x="80" y="420">[[checks]]</text></g>
<g fill="#a9b4c2"><text x="80" y="206">so lint reads a fresh site</text><text x="80" y="288">warnings fail too</text><text x="80" y="370">only with a [publication] table</text><text x="80" y="452">the project's own, in order</text></g>
<g fill="#0d1117" stroke="#ff7b72" stroke-width="2.5"><circle cx="556" cy="179" r="14"/><circle cx="556" cy="261" r="14"/><circle cx="556" cy="343" r="14"/><circle cx="556" cy="425" r="14"/></g>
<path d="M550 173l12 12M562 173l-12 12M550 255l12 12M562 255l-12 12M550 337l12 12M562 337l-12 12M550 419l12 12M562 419l-12 12" stroke="#ff7b72" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="14" cy="507" r="12" fill="#0d1117" stroke="#ff7b72" stroke-width="2.5"/><path d="M9 502l10 10M19 502l-10 10" stroke="#ff7b72" stroke-width="2.5" stroke-linecap="round"/>
<text x="36" y="516" fill="#ff7b72">a failure stops the run there</text>
<text x="2" y="548" fill="#39d2c0">all pass: the push goes on</text>
</g>
</svg>
<figcaption><b>Figure 8.</b> What <code>check</code> runs, and how the opt-in pre-push gate calls it. It runs no browser check and replaces no review by eye. This diagram contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-violet"><span class="bs-label">The pre-push gate</span><h3>Opt-in, once per clone</h3><ul>
<li>switched on by the last command below; a failing <code>check</code> stops the push</li>
<li>refuses a push while tracked files have uncommitted changes, so that the checks read what is pushed</li>
<li>runs <code>$DOCS_PYTHON</code>, else the checkout's <code>.build/docs-env/bin/python</code></li>
<li><code>git push --no-verify</code> skips it once; the project's workflow stays the check that counts</li>
</ul></div>
</div>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Site commands">

| Command | What it does |
|---|---|
| `build` | Renders every page into `.build/docs/`; removes obsolete output |
| `build --page <slug>` | Renders one page while you work; validates nothing else |
| `build --check` | Fails when the output no longer matches its sources; writes nothing and ignores the build time in `html/build-info.js` |
| `build --check-reader` | Fails when the reader changes a page's words, links, media, tables, folds, anchors or SVG figures |
| `lint --strict` | Checks the records and the built pages; [lint](#lint) |
| `check` | [Figure 8](#fig-check) |
| `slides` | A deck of slide faces; [figures and slides](#figures-and-slides) |
| `publish --out _site` | Builds and exports the public bundle that `[publication]` configures; does not deploy |
| `capability-map` | Rewrites the generated column of the project's capability map |
| `init <folder>` | Adds the starter, refusing to overwrite any file |

</div>

```bash
python .docs-kit/docsite.py build --project .
python .docs-kit/docsite.py build --project . --check
python .docs-kit/docsite.py check --project .
git config core.hooksPath "$(git rev-parse --show-toplevel)/.docs-kit/hooks"
```

`python` is the project's documentation interpreter, `.build/docs-env/bin/python` after the [README](readme.html#pin-and-upgrade) setup. The build fails instead of publishing a broken page: untracked or missing media, paths that leave the project, address collisions and wrong anchors into registered pages all stop it ([one command and a pre-push gate](validation.html#one-command-and-a-pre-push-gate)).

</section>

<section class="card" id="lint">

## Lint sorts what it finds into errors, warnings and notes; --strict fails on warnings too

<p class="bs-lead">Run <code>lint --strict</code> before you commit documentation; it reads the records and the built pages for what the build does not check.</p>

<div class="bs-grid g2">
<figure id="fig-lint">
<svg class="inline-fig" viewBox="0 0 600 472" role="img" aria-label="Three kinds of finding and the run they fail. Errors fail both lint and lint --strict: a dead link or anchor, an excerpt off its lines, a formula KaTeX rejects, two faces in one chapter. Warnings pass lint and fail lint --strict: a page without a record, text above chapter one, a number only on its face. Notes pass both: a page to reread after its record changed, a number no record states.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif" font-size="26">
<g font-family="'IBM Plex Mono',ui-monospace,monospace" fill="#e6edf3" text-anchor="middle" font-weight="600"><text x="420" y="31">lint</text><text x="536" y="31">--strict</text></g>
<rect x="2" y="42" width="596" height="166" rx="12" fill="none" stroke="#ff7b72" stroke-width="2.5"/>
<text x="20" y="74" fill="#ff7b72" font-weight="600" letter-spacing="1" font-family="'IBM Plex Mono',ui-monospace,monospace">ERROR</text>
<g fill="#e6edf3"><text x="20" y="106">a dead link or anchor</text><text x="20" y="134">an excerpt off its lines</text><text x="20" y="162">a formula KaTeX rejects</text><text x="20" y="190">two faces in one chapter</text></g>
<rect x="364" y="54" width="112" height="142" rx="8" fill="#ff7b72" fill-opacity=".16"/><rect x="484" y="54" width="112" height="142" rx="8" fill="#ff7b72" fill-opacity=".16"/>
<g fill="#ff7b72" font-weight="600" text-anchor="middle"><text x="420" y="133">fails</text><text x="540" y="133">fails</text></g>
<rect x="2" y="216" width="596" height="138" rx="12" fill="none" stroke="#ffa657" stroke-width="2.5"/>
<text x="20" y="248" fill="#ffa657" font-weight="600" letter-spacing="1" font-family="'IBM Plex Mono',ui-monospace,monospace">WARNING</text>
<g fill="#e6edf3"><text x="20" y="280">a page without a record</text><text x="20" y="308">text above chapter one</text><text x="20" y="336">a number only on its face</text></g>
<rect x="364" y="228" width="112" height="114" rx="8" fill="#39d2c0" fill-opacity=".12"/><rect x="484" y="228" width="112" height="114" rx="8" fill="#ff7b72" fill-opacity=".16"/>
<g font-weight="600" text-anchor="middle"><text x="420" y="293" fill="#39d2c0">passes</text><text x="540" y="293" fill="#ff7b72">fails</text></g>
<rect x="2" y="362" width="596" height="108" rx="12" fill="none" stroke="#7d8896" stroke-width="2.5"/>
<text x="20" y="394" fill="#a9b4c2" font-weight="600" letter-spacing="1" font-family="'IBM Plex Mono',ui-monospace,monospace">NOTE</text>
<g fill="#e6edf3"><text x="20" y="426">a page to reread</text><text x="20" y="454">a number no record states</text></g>
<rect x="364" y="374" width="112" height="84" rx="8" fill="#39d2c0" fill-opacity=".12"/><rect x="484" y="374" width="112" height="84" rx="8" fill="#39d2c0" fill-opacity=".12"/>
<g fill="#39d2c0" font-weight="600" text-anchor="middle"><text x="420" y="424">passes</text><text x="540" y="424">passes</text></g>
</g>
</svg>
<figcaption><b>Figure 9.</b> Three kinds of finding, a few examples of each, and the run each fails. This diagram contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-teal"><span class="bs-label">What lint reads</span><h3>Records, built pages, settings</h3><ul>
<li>Markdown under <code>docs/</code>, <code>AGENTS.md</code>, <code>CLAUDE.md</code>, <code>README.md</code> and what <code>record_roots</code> names: links, anchors, excerpts tagged <code>source=path#La-Lb</code></li>
<li>the built pages: links to repository files, slide faces and every formula, compiled with the kit's KaTeX where Node.js runs</li>
<li>figures against their manifest; the capability map against <code>tooling_roots</code></li>
<li>open work: every bullet links its owner; a finished line is deleted, not struck</li>
</ul></div>
</div>

[Figure 9](#fig-lint) is how to read a lint run. An error is wrong now. A warning is for the author to decide: `lint` prints it and passes, `--strict` fails. A note never fails: when a record section changes, lint lists the pages that link it so that you reread them ([rendered pages are for people](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown)), and `--since <rev>` compares with an older commit. With `page_number_notes = true` it also lists numbers in a page's prose that its linked records do not state. Two more notes keep pages from falling behind: a changed section that no page links, when a page explains the rest of its record, and a numbered figure the text never cites. [Reviewing a page against its rules](validation.html#reviewing-a-page-against-its-rules) says what to do with a page they point at.

```bash
python .docs-kit/docsite.py lint --project . --strict
python .docs-kit/docsite.py lint --project . --registry
```

`--registry` lists every `INVARIANT` and `DON'T-REDO` marker and exits. Without Node.js the formula check prints a note and passes, unless `formula_check_required = true` ([formula check](authoring.html#formula-check)). `worklog`, `open_work` and `worklog_links_checked_from` adapt the checks to a project's own history files ([resources](resources.html#resource-closure-and-evidence)).

</section>

<section class="card" id="preview">

## Look at every changed element, at each width and view, before anyone else sees it

<p class="bs-lead">Serve <code>.build/docs/</code> on 127.0.0.1, capture each changed element whole at wide and narrow widths and in each reader view it appears in, and look at every capture.</p>

<div class="bs-grid g2">
<figure id="fig-review">
<svg class="inline-fig" viewBox="0 0 600 470" role="img" aria-label="A matrix of captures. Columns: a wide window and a narrow phone window. Rows: One chapter, Two chapters and All chapters. In each of the six cells the changed element, marked in orange, is captured whole.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif" font-size="26">
<g fill="#e6edf3" font-weight="600" text-anchor="middle"><text x="300" y="28">wide</text><text x="521" y="28">narrow</text></g>
<g fill="#a9b4c2"><text x="2" y="122">One chapter</text><text x="2" y="262">Two chapters</text><text x="2" y="402">All chapters</text></g>
<g fill="#0d1117" stroke="#7d8896" stroke-width="2"><rect x="170" y="50" width="260" height="126" rx="8"/><rect x="170" y="190" width="260" height="126" rx="8"/><rect x="170" y="330" width="260" height="126" rx="8"/><rect x="484" y="46" width="74" height="134" rx="12"/><rect x="484" y="186" width="74" height="134" rx="12"/><rect x="484" y="326" width="74" height="134" rx="12"/></g>
<g fill="#121a24"><rect x="172" y="52" width="46" height="122" rx="6"/><rect x="172" y="192" width="46" height="122" rx="6"/><rect x="172" y="332" width="46" height="122" rx="6"/></g>
<g fill="#10161f" stroke="#30363d" stroke-width="2"><rect x="222" y="66" width="6" height="96" rx="3"/><rect x="418" y="66" width="8" height="96" rx="3"/></g>
<g fill="#10161f" stroke="#39d2c0" stroke-width="2"><rect x="232" y="58" width="180" height="110" rx="6"/><rect x="226" y="198" width="98" height="110" rx="6"/><rect x="328" y="198" width="98" height="110" rx="6"/><rect x="232" y="338" width="190" height="110" rx="6"/><rect x="490" y="60" width="62" height="112" rx="5"/><rect x="489" y="200" width="31" height="112" rx="4"/><rect x="522" y="200" width="31" height="112" rx="4"/><rect x="490" y="340" width="62" height="112" rx="5"/></g>
<g stroke="#30363d" stroke-width="2"><path d="M232 392H422M490 396H552"/></g>
<g fill="#a9b4c2" fill-opacity=".5"><rect x="244" y="68" width="120" height="8" rx="4"/><rect x="238" y="208" width="70" height="8" rx="4"/><rect x="340" y="208" width="70" height="8" rx="4"/><rect x="244" y="346" width="120" height="8" rx="4"/><rect x="244" y="400" width="100" height="8" rx="4"/><rect x="496" y="68" width="44" height="7" rx="3.5"/><rect x="494" y="208" width="22" height="6" rx="3"/><rect x="526" y="208" width="22" height="6" rx="3"/><rect x="496" y="348" width="44" height="7" rx="3.5"/><rect x="496" y="404" width="40" height="7" rx="3.5"/></g>
<g fill="#ffa657" fill-opacity=".18" stroke="#ffa657" stroke-width="2.5" stroke-dasharray="7 5"><rect x="244" y="88" width="156" height="66" rx="5"/><rect x="236" y="226" width="78" height="70" rx="4"/><rect x="244" y="362" width="166" height="24" rx="4"/><rect x="496" y="84" width="50" height="76" rx="4"/><rect x="492" y="224" width="25" height="74" rx="3"/><rect x="496" y="360" width="50" height="30" rx="3"/></g>
</g>
</svg>
<figcaption><b>Figure 10.</b> What a review captures: the changed element, in orange, whole in every width and reader view it appears in. A sketch with no measured results.</figcaption>
</figure>
<div class="bs-part bs-orange"><span class="bs-label">Look at each capture</span><h3>What only the eye sees</h3><ul>
<li>alignment, spacing, list markers, type, colour and overflow, against the page around it</li>
<li>what no check sees, such as a sign that reads as a minus</li>
<li>on a slide face, what draws the eye first, and any empty band</li>
<li>at the end, one pass over the page for terms, colours and links</li>
</ul></div>
</div>

```bash
python3.12 -m http.server 8321 --bind 127.0.0.1 --directory .build/docs
```

Open `http://127.0.0.1:8321/html/index.html`; the server exposes only the generated output. [Figure 10](#fig-review) is the review that a passing build, lint and browser suite still need: the kit's [browser checks](validation.html#reusable-browser-checks) measure overflow, text below 11 px and faces that do not fit, and the eye covers the rest. Review one rebuilt chapter before starting the next. The captures are [scratch files](handoffs.html#scratch-files); when a delegated agent wrote the page, the agent that delegated it looks at them itself.

Reuse a running server only after confirming who owns it and which checkout it serves, and stop only your own ([local review and browser access](validation.html#local-review-and-browser-access)). After the review, `publish` exports the public bundle; a feature branch never publishes production documentation ([publishing gate](publication.html#publishing-gate)).

</section>

<section class="card" id="upgrade">

## An upgrade moves the pin only after you read what changed

<p class="bs-lead">The submodule commit is your version. Nothing changes until you move it, rebuild, review and commit the new pin.</p>

<figure id="fig-upgrade">
<div class="bs-flow" role="img" aria-label="Read the release notes between your pinned version and the target. Move the .docs-kit submodule to the reviewed commit or tag. Rebuild and lint, run the project conformance check, review the changed pages at wide and narrow widths, then commit the pin together with any consumer changes.">
<div class="bs-node bs-teal"><span class="bs-label">Read</span><b>Release notes</b><ul><li>changes since your pin</li><li>the migration guide, for the steps since your pin</li></ul></div>
<div class="bs-arrow"><span>move</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>.docs-kit</code></span><b>Check out the target</b><ul><li>a reviewed commit or tag</li></ul></div>
<div class="bs-arrow"><span>verify</span></div>
<div class="bs-node bs-orange"><span class="bs-label">One commit</span><b>Rebuild, check, commit</b><ul><li>build and strict lint</li><li>conformance check</li><li>changed pages at both widths</li><li>pin plus consumer changes</li></ul></div>
</div>
<figcaption><b>Figure 11.</b> The upgrade sequence. This diagram contains no measured results.</figcaption>
</figure>

```bash
git -C .docs-kit fetch --tags
git -C .docs-kit checkout <reviewed-kit-commit-or-tag>
python .docs-kit/docsite.py build --project .
python .docs-kit/docsite.py lint --project . --strict
git add .docs-kit
```

[Figure 11](#fig-upgrade) is the whole upgrade. Others clone with `git clone --recurse-submodules <project-url>` and get exactly your pinned kit; after the rebuild the sidebar's foot names the new version. Share fixes upstream in the kit, not in a consumer's submodule checkout. [Release notes](releases.html), [README · Pin and upgrade](readme.html#pin-and-upgrade) and the [project conformance check](conformance.html) have the details.

</section>

<section class="card" id="reference-guides">

## Each toolkit task has one reference guide

<p class="bs-lead">This page explains how the toolkit fits together; each reference guide holds the exact contract for one task.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Toolkit reference guides by task">

| To… | Read… | It covers |
|---|---|---|
| Configure the site | [Tooling and ownership](authoring.html#tooling-and-ownership), [theme colours](authoring.html#theme-colours), [capability map settings](authoring.html#capability-map-settings) | `site.toml`, navigation, the sidebar's foot, colours, tooling |
| Write pages | [Authoring paths](authoring.html#authoring-paths), [topic group folders](authoring.html#topic-group-folders), [page design](page-design.html#page-design) | Frontmatter, link origins, includes, chapters, page types |
| Publish existing Markdown | [Registered source pages](authoring.html#registered-source-pages), [automatic reference listing](authoring.html#automatic-reference-listing), [records outside `docs/`](authoring.html#records-outside-docs) | Registered and listed records, lint beyond `docs/` |
| Shape the reader | [Reader](reader.html), [panel switcher](panel-switcher.html) | Chapter views, reading layers, the home site map, the panel switcher contract |
| Draw, derive and present | [Generated figures](authoring.html#generated-figures), [slide faces and decks](authoring.html#slide-faces-and-decks), [formula check](authoring.html#formula-check) | Generated figures, math, slide faces and decks |
| Package images, media and evidence | [Resources and evidence](resources.html) | Resource closure, local-only captures, inventories, old links in the worklog |
| Check and publish | [Validation](validation.html), [publication export](publication.html) | Validation, `check`, browser checks, the page lock, export |
| Upgrade the pin | [Project conformance check](conformance.html) | What to check in the project after the pin moves |

</div>

The writing side of a page (section design, figures, mathematics, code excerpts) is explained on [Writing pages](writing-practices.html), and where a document lives on [Records and documents](documentation-practices.html).

</section>
