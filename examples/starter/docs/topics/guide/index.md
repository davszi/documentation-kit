+++
toc = []
title = "A shared kit keeps each project in control"
brand_sub = "source ownership · evidence · optional depth"
components = ["toc", "nav", "code", "filelinks", "lightbox"]
page_css = ["build-sheet.css"]
math = true
+++

# A shared kit keeps each project in control

<section class="card" id="pipeline">

<!-- slide -->
<style>
/* Local to this face: a three-by-three matrix of the folders against who writes them and how they change; below 720 px each row becomes a labelled card. */
.slide-main.fx-own {justify-content:stretch!important;gap:.5cqi!important;}
.fx-matrix {flex:1 1 0!important;min-height:0!important;display:grid!important;grid-template-columns:22cqi minmax(0,1fr) minmax(0,1fr) minmax(0,1.25fr)!important;grid-template-rows:auto 1fr 1fr auto 1fr!important;column-gap:0!important;margin:1.4cqi 0 0!important;}
.fx-matrix > [role=row] {display:contents!important;}
.fx-matrix [role=columnheader] {padding:0 1.4cqi .7cqi!important;font:500 1.1cqi/1.2 "IBM Plex Mono",monospace!important;letter-spacing:.08em!important;text-transform:uppercase!important;color:var(--sf-dim)!important;border-bottom:1px solid var(--sf-line)!important;}
.fx-matrix [role=columnheader]:first-child {padding-left:1.2cqi!important;}
.fx-matrix [role=rowheader],.fx-matrix [role=cell] {display:flex!important;flex-direction:column!important;justify-content:center!important;gap:.3cqi!important;padding:.8cqi 1.4cqi!important;border-bottom:1px solid var(--sf-line)!important;font-size:1.5cqi!important;line-height:1.35!important;color:var(--sf-sub)!important;}
.fx-matrix .fx-k {display:none!important;}
.fx-matrix [role=cell] {color:var(--sf-ink)!important;}
.fx-matrix [role=cell]:has(b) {color:var(--sf-sub)!important;}
.fx-matrix [role=rowheader]:has(.is-docs) {background:linear-gradient(90deg,color-mix(in srgb,var(--sf-accent) 7%,transparent),transparent)!important;}
.fx-matrix [role=rowheader]:has(.is-kit) {background:linear-gradient(90deg,color-mix(in srgb,var(--sf-alt) 8%,transparent),transparent)!important;}
.fx-matrix [role=rowheader]:has(.is-out) {background:linear-gradient(90deg,color-mix(in srgb,var(--sf-warm) 6%,transparent),transparent)!important;}
.fx-matrix [role=rowheader] {padding-left:1.2cqi!important;}
.fx-matrix [role=cell] b {font:600 2.1cqi/1.15 "IBM Plex Sans",sans-serif!important;color:var(--sf-ink)!important;}
.fx-matrix [role=cell].is-key {background:linear-gradient(90deg,color-mix(in srgb,var(--sf-accent) 13%,transparent),color-mix(in srgb,var(--sf-accent) 4%,transparent))!important;box-shadow:inset .3cqi 0 0 var(--sf-accent)!important;}
.fx-matrix [role=cell].is-key b {color:var(--sf-accent)!important;}
.fx-matrix [role=cell].is-alert b {color:var(--sf-alert)!important;}
.fx-matrix [role=cell].is-alert b::before {content:"\00d7  "!important;font-weight:700!important;}
.fx-folder {position:relative!important;display:inline-flex!important;align-items:center!important;align-self:flex-start!important;margin-top:1cqi!important;padding:.9cqi 1.3cqi!important;border:2px solid var(--fx-tone)!important;border-radius:0 1cqi 1cqi 1cqi!important;background:color-mix(in srgb,var(--fx-tone) 10%,var(--sf-tile))!important;font:600 2.2cqi/1 "IBM Plex Mono",monospace!important;color:var(--fx-tone)!important;}
.fx-folder::before {content:""!important;position:absolute!important;left:-2px!important;top:calc(-1cqi - 2px)!important;width:6cqi!important;height:1cqi!important;border:2px solid var(--fx-tone)!important;border-bottom:0!important;border-radius:.6cqi .6cqi 0 0!important;background:color-mix(in srgb,var(--fx-tone) 10%,var(--sf-tile))!important;}
.fx-folder.is-docs {--fx-tone:var(--sf-accent)!important;}
.fx-folder.is-kit {--fx-tone:var(--sf-alt)!important;}
.fx-folder.is-out {--fx-tone:var(--sf-warm)!important;border-style:dashed!important;background:transparent!important;}
.fx-folder.is-out::before {border-style:dashed!important;background:transparent!important;}
.fx-folder-note {white-space:nowrap!important;font:1.15cqi/1.3 "IBM Plex Mono",monospace!important;color:var(--sf-dim)!important;}
.fx-build-row [role=cell] {padding:.5cqi 1.4cqi!important;border-bottom:1px dashed var(--sf-line)!important;}
.fx-build-row [role=rowheader] {padding:.5cqi 1.2cqi!important;background:none!important;border-bottom:1px dashed var(--sf-line)!important;flex-direction:row!important;justify-content:flex-start!important;align-items:center!important;gap:.8cqi!important;}
.fx-pill {display:inline-block!important;padding:.25cqi 1.1cqi!important;border:2px solid var(--sf-sub)!important;border-radius:999px!important;font:600 1.5cqi/1.2 "IBM Plex Mono",monospace!important;color:var(--sf-ink)!important;}
.fx-arrow {font:600 1.8cqi/1 "IBM Plex Sans",sans-serif!important;color:var(--sf-sub)!important;}
.fx-own figcaption {font:1cqi/1.3 "IBM Plex Mono",monospace!important;color:var(--sf-dim)!important;text-align:right!important;margin:0!important;}
@container (max-width: 719.98px) {
  .fx-matrix {display:flex!important;flex-direction:column!important;gap:12px!important;flex:none!important;}
  .fx-matrix > [role=row] {display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:6px!important;padding:0 0 12px!important;border-bottom:1px solid var(--sf-line)!important;}
  .fx-matrix > [role=row].fx-head {display:none!important;}
  .fx-matrix [role=rowheader],.fx-matrix [role=cell] {padding:4px 0!important;border:0!important;font-size:14px!important;background:none!important;}
  .fx-folder-note {white-space:normal!important;}
  .fx-matrix [role=cell].is-key {padding:6px 10px!important;box-shadow:inset 3px 0 0 var(--sf-accent)!important;}
  .fx-matrix .fx-k {display:block!important;font:500 11px/1.3 "IBM Plex Mono",monospace!important;letter-spacing:.08em!important;text-transform:uppercase!important;color:var(--sf-dim)!important;}
  .fx-matrix [role=cell] b {font-size:17px!important;}
  .fx-folder {margin-top:12px!important;padding:8px 12px!important;border-radius:0 10px 10px 10px!important;font-size:20px!important;}
  .fx-folder::before {top:-12px!important;width:60px!important;height:10px!important;border-radius:6px 6px 0 0!important;}
  .fx-folder-note {font-size:12px!important;}
  .fx-matrix > .fx-build-row {display:flex!important;padding:0 0 12px!important;border-bottom:1px dashed var(--sf-line)!important;}
  .fx-build-row [role=cell] {display:none!important;}
  .fx-build-row [role=rowheader] {border:0!important;padding:0!important;gap:8px!important;}
  .fx-pill {font-size:14px!important;padding:2px 10px!important;}
  .fx-arrow {font-size:18px!important;}
  .fx-own figcaption {font-size:12px!important;text-align:left!important;}
}
</style>
<p class="slide-eyebrow">Ownership</p>
<p class="slide-title">The project owns its content; the kit is a pinned tool</p>
<figure class="slide-main fx-own">
<div class="fx-matrix" role="table" aria-label="Three folders: who writes each and how it changes">
<div role="row" class="fx-head"><span role="columnheader">Folder</span><span role="columnheader">Holds</span><span role="columnheader">Written by</span><span role="columnheader">Changes when</span></div>
<div role="row"><span role="rowheader"><span class="fx-folder is-docs">docs/</span></span><span role="cell"><span class="fx-k">Holds</span>pages, records, site.toml, evidence</span><span role="cell" class="is-key"><span class="fx-k">Written by</span><b>the project</b>in its own repository</span><span role="cell"><span class="fx-k">Changes when</span><b>the project writes it</b>its review stays there too</span></div>
<div role="row"><span role="rowheader"><span class="fx-folder is-kit">.docs-kit/</span><span class="fx-folder-note">submodule</span></span><span role="cell"><span class="fx-k">Holds</span>rules, theme, reader, validation</span><span role="cell"><span class="fx-k">Written by</span><b>the shared kit</b>one pinned revision</span><span role="cell" class="is-key"><span class="fx-k">Changes when</span><b>the project moves its pin</b>to a reviewed revision it chose</span></div>
<div role="row" class="fx-build-row"><span role="rowheader"><span class="fx-arrow" aria-hidden="true">↓</span><span class="fx-pill">build</span><span class="fx-folder-note">reads both folders</span></span><span role="cell"></span><span role="cell"></span><span role="cell"></span></div>
<div role="row"><span role="rowheader"><span class="fx-folder is-out">.build/docs/</span></span><span role="cell"><span class="fx-k">Holds</span>the generated HTML</span><span role="cell"><span class="fx-k">Written by</span><b>the build</b>from both folders</span><span role="cell" class="is-alert"><span class="fx-k">Changes when</span><b>never edited</b>rebuilt from source instead</span></div>
</div>
<figcaption>Drawn from Figure 1 and its three steps</figcaption>
</figure>
<p class="slide-scope">Illustration of ownership · no measured results</p>
<!-- /slide -->

## Pin the tools, own the content

<p class="bs-lead">A project chooses its shared-kit revision while keeping its pages and configuration in its own repository.</p>

[Figure 1](#fig-pipeline) separates what a project authors from what the kit supplies. Follow the numbers: the project pins a kit revision, writes its own content, and builds a site from both. The dashed red path is the one that does not exist: editing output does not update either source.

<div class="bs-grid g2">
<figure id="fig-pipeline">
<!-- include: fragments/ownership.html -->
<figcaption><b>Figure 1.</b> The project folder holds what the project writes and the pinned kit; the build writes generated output outside both. This hand-authored SVG diagram illustrates ownership; it contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-teal"><span class="bs-label">Read the figure</span><h3>Three steps, one way</h3><ol>
<li><b>Pin a kit revision.</b> The <code>.docs-kit</code> submodule holds rules and templates, the build-sheet theme, the reader and validation. The project chooses the reviewed revision and when to move it.</li>
<li><b>Write in the project.</b> Topic records and pages, navigation, local assets, evidence and review stay in its repository.</li>
<li><b>Build.</b> One command reads both folders and writes the site: HTML and local resources, stable public anchors and source links.</li>
</ol><p><b>Never edit the output.</b> Generated pages do not flow back into source. Change the record, page, configuration or generator, then rebuild.</p></div>
</div>

<div class="bs-specs"><div><span class="bs-label">Shared rules</span><b>One pinned revision</b></div><div><span class="bs-label">Project content</span><b>Local ownership</b></div><div><span class="bs-label">Generated site</span><b>Rebuilt from source</b></div></div>

</section>

<section class="card" id="knowledge">

## Let a finding settle into one home

<p class="bs-lead">Move durable knowledge to its subject, keep evidence with its producer, and route unfinished work to its owner.</p>

[Figure 2](#fig-knowledge) shows the promotion path. An accepted design still needs an implementation and evidence before it describes tested behavior.

<figure id="fig-knowledge">
<div class="bs-flow" role="img" aria-label="An open question is investigated with retained evidence. Established findings move to a topic record and are explained to human readers.">
<div class="bs-node bs-orange"><span class="bs-label">Unresolved</span><b>Question and acceptance</b><p>One open owner holds the decision and prospective checks.</p></div>
<div class="bs-arrow"><span>investigate</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Producing work</span><b>Protocol and evidence</b><p>Keep inputs, outputs, failures, source pins and reproduction together.</p></div>
<div class="bs-arrow"><span>establish</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Current knowledge</span><b>Record and explanation</b><p>The topic owns the finding. Its page explains the consequence and links to evidence.</p></div>
</div>
<figcaption><b>Figure 2.</b> Promotion changes the knowledge owner without rewriting original evidence. Chronology belongs in the worklog, outside this flow.</figcaption>
</figure>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Record for agents</span><h3>Preserve the exact contract</h3><p>Use plain Markdown for assumptions, accepted requirements, file references and scoped checks.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Page for people</span><h3>Explain what the finding means</h3><p>Lead with a claim, draw the mechanism and make the evidence useful without exposing a task board.</p></div>
</div>

</section>

<section class="card" id="evidence">

## A check proves the property it exercised

<p class="bs-lead">Keep design decisions, implemented behavior and runtime observations visibly distinct.</p>

The comparison below names the boundary of each evidence kind. A local unit test cannot establish an untested deployment workload.

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-wait">Decided</span><h3>Accepted design</h3><p>Records a chosen requirement and its rationale. It still needs an implementation and acceptance evidence.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Local</span><h3>CPU check</h3><p>Establishes the asserted property for its cases and environment. Name its command, inputs and limits.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Runtime</span><h3>Observed behavior</h3><p>Qualifies the recorded workload and runtime. It does not automatically cover changed inputs or another environment.</p></div>
</div>

<!-- fold: experiment What a complete experiment records -->

State measured motivation, a strong cheap baseline and acceptance criteria before results. Retain the reproduction command, source revision, environment, input identities, output table with units, verdict, caveats and next step. A failed acceptance check is a result worth preserving.

No benchmark has been run for this starter. These are authoring requirements, not sample performance results.

<!-- /fold -->

</section>

<section class="card" id="layers">

## Keep the argument visible and depth optional

<p class="bs-lead">A reader should understand the claim and verdict with every supporting fold closed.</p>

[Figure 3](#fig-layers) puts the explanation on the visible path. Math, Experiments, Code and Alternatives add detail without becoming prerequisites hidden from the reader.

<figure id="fig-layers">
<div class="bs-flow n2" role="img" aria-label="Visible story contains the question, mechanism, evidence and verdict. Optional layers add derivation, reproduction, source and alternatives.">
<div class="bs-node bs-teal"><span class="bs-label">Always readable</span><b>Question to verdict</b><ul><li>Define the problem</li><li>Draw the mechanism</li><li>Show decisive evidence</li><li>State the consequence</li></ul></div>
<div class="bs-arrow"><span>go deeper</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Optional layers</span><b>Inspect the supporting work</b><ul><li>Derivation and assumptions</li><li>Protocol and raw results</li><li>Real source excerpts</li><li>Rejected alternatives</li></ul></div>
</div>
<figcaption><b>Figure 3.</b> Optional depth branches from a complete visible argument. Both reader columns keep independent layer preferences.</figcaption>
</figure>

<!-- fold: math Count resources without counting copies -->

Let $P$ be the set of resources referenced by pages and $S$ the shared resources needed by the reader. Their union defines the required bundle:

$$
R = P \cup S
$$

A resource used in both sets appears once. This is set notation for packaging, not a measured size or timing claim.

<!-- /fold -->

<!-- fold: code Configure the project identity once -->

`init` writes the title and source repository into the first lines of `docs/site/site.toml` (`--title`, `--repository`); the home label is a project choice. The two lines after them are a real source excerpt: the revision that source links use, and the switch that turns on the chapter reader.

```toml source=docs/site/site.toml#L3-L4
gh_ref = "main"
chapter_reader = true
```

<!-- /fold -->

</section>

<section class="card" id="slides">

<!-- slide -->
<style>
/* Local to this face: the slide drawn large beside the chapter it opens; a tall drawing replaces it below 720 px. */
.slide-main.fx-zoom {justify-content:flex-start!important;gap:0!important;}
.fx-zoom > figure {flex:1 1 0!important;min-height:0!important;display:flex!important;flex-direction:column!important;gap:.4cqi!important;margin:0!important;}
.fx-zoom svg {display:block!important;width:100%!important;}
.fx-zoom svg.fx-wide {flex:1 1 0!important;min-height:0!important;height:100%!important;}
.fx-zoom svg.fx-tall {display:none!important;}
.fx-zoom figcaption {font:1cqi/1.3 "IBM Plex Mono",monospace!important;color:var(--sf-dim)!important;text-align:right!important;}
@container (max-width: 719.98px) {
  .fx-zoom > figure {flex:none!important;}
  .fx-zoom svg.fx-wide {display:none!important;}
  .fx-zoom svg.fx-tall {display:block!important;height:auto!important;}
  .fx-zoom figcaption {font-size:12px!important;text-align:left!important;}
}
</style>
<p class="slide-eyebrow">Slide faces</p>
<p class="slide-title">A face shows the finding; its chapter keeps every fact</p>
<div class="slide-main fx-zoom">
<figure>
<svg class="inline-fig fx-wide" viewBox="0 0 1200 536" role="img" aria-label="A slide face drawn large beside the chapter it opens. The face has a label row that names the subject, the finding as a sentence, a visual that is a view of the chapter's figure, laid out for this finding, and a scope line. In the reader the face sits at the top of the chapter card; the full chapter follows with its heading, its figure and every fact with its evidence. A chapter with nothing to show gets no face.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<text x="8" y="26" font-size="16" fill="#7d8896" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">THE FACE, AT 16:9</text>
<path d="M890 60L832 44M890 218L832 508" stroke="#39d2c0" stroke-width="1.5" stroke-opacity=".45" stroke-dasharray="4 5"/>
<g transform="translate(0 26)">
<rect x="8" y="18" width="824" height="464" rx="18" fill="#0f1620" stroke="#39d2c0" stroke-width="3"/>
<rect x="44" y="50" width="120" height="10" rx="5" fill="#39d2c0"/>
<text x="180" y="60" font-size="18" fill="#a9b4c2">label row: the subject</text>
<text x="44" y="112" font-size="38" fill="#e6edf3" font-weight="600">The finding, as a sentence</text>
<rect x="44" y="138" width="752" height="270" rx="14" fill="#39d2c0" fill-opacity=".07" stroke="#39d2c0" stroke-width="2.5"/>
<g stroke="#39d2c0" stroke-opacity=".22" stroke-width="2" fill="none"><path d="M84 360C180 300 250 330 330 270S470 200 540 230 680 170 756 180"/><path d="M84 330h672M84 270h672M84 210h672" stroke-dasharray="3 7"/></g>
<text x="420" y="262" font-size="30" fill="#39d2c0" font-weight="600" text-anchor="middle">a view of the chapter's figure</text>
<text x="420" y="298" font-size="21" fill="#a9b4c2" text-anchor="middle">laid out for this finding, filling the canvas</text>
<text x="44" y="446" font-size="17" fill="#7d8896" letter-spacing="1" font-family="'IBM Plex Mono',ui-monospace,monospace">scope line</text>
<path d="M162 440H796" stroke="#2f3b4a" stroke-width="2"/>
</g>
<g transform="translate(0 2)">
<text x="880" y="24" font-size="16" fill="#7d8896" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">IN THE READER</text>
<rect x="880" y="42" width="312" height="350" rx="14" fill="#121a24" stroke="#2f3b4a" stroke-width="2"/>
<rect x="890" y="56" width="292" height="158" rx="8" fill="#0f1620" stroke="#39d2c0" stroke-width="2.5"/>
<rect x="904" y="70" width="40" height="5" rx="2.5" fill="#39d2c0"/>
<rect x="904" y="82" width="190" height="11" rx="3" fill="#e6edf3"/>
<rect x="904" y="102" width="264" height="86" rx="5" fill="#39d2c0" fill-opacity=".1" stroke="#39d2c0" stroke-width="1.5"/>
<rect x="904" y="198" width="110" height="4" rx="2" fill="#7d8896"/>
<path d="M1036 224v16m-7-7 7 7 7-7" fill="none" stroke="#a9b4c2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="1054" y="238" font-size="16" fill="#a9b4c2">read on</text>
<text x="896" y="270" font-size="18" fill="#e6edf3" font-weight="600">the full chapter</text>
<rect x="896" y="282" width="236" height="6" rx="3" fill="#a9b4c2" fill-opacity=".5"/>
<rect x="896" y="300" width="128" height="52" rx="6" fill="#0f1d22" stroke="#39d2c0" stroke-width="2"/>
<text x="960" y="332" font-size="17" fill="#39d2c0" font-weight="600" text-anchor="middle" font-family="'IBM Plex Mono',ui-monospace,monospace">Figure</text>
<rect x="1036" y="304" width="140" height="6" rx="3" fill="#a9b4c2" fill-opacity=".5"/>
<rect x="1036" y="318" width="120" height="6" rx="3" fill="#a9b4c2" fill-opacity=".5"/>
<rect x="1036" y="332" width="134" height="6" rx="3" fill="#a9b4c2" fill-opacity=".5"/>
<text x="896" y="378" font-size="16" fill="#a9b4c2">every fact, with its evidence</text>
</g>
<path d="M896 330H806" fill="none" stroke="#39d2c0" stroke-width="2.5" stroke-dasharray="7 5"/><path d="M798 330l14-7v14z" fill="#39d2c0"/>
<g transform="translate(0 26)">
<rect x="880" y="414" width="118" height="66" rx="8" fill="none" stroke="#7d8896" stroke-width="2" stroke-dasharray="7 5"/>
<path d="M892 424l94 46M986 424l-94 46" stroke="#ff7b72" stroke-width="2.5" stroke-linecap="round"/>
<text x="1012" y="440" font-size="18" fill="#e6edf3" font-weight="600">nothing to show</text>
<text x="1012" y="468" font-size="18" fill="#ff7b72" font-weight="600">no face</text>
</g>
</g>
</svg>
<svg class="inline-fig fx-tall" viewBox="0 0 340 624" role="img" aria-label="A slide face: a label row that names the subject, the finding as a sentence, a visual that is a view of the chapter's figure, laid out for this finding, and a scope line. In the reader the face sits at the top of the chapter card and the full chapter follows with its figure and every fact with its evidence. A chapter with nothing to show gets no face.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<rect x="2" y="2" width="336" height="250" rx="12" fill="#0f1620" stroke="#39d2c0" stroke-width="2.5"/>
<rect x="18" y="20" width="56" height="6" rx="3" fill="#39d2c0"/>
<text x="84" y="27" font-size="14" fill="#a9b4c2">label row: the subject</text>
<text x="18" y="58" font-size="21" fill="#e6edf3" font-weight="600">The finding, as a sentence</text>
<rect x="18" y="72" width="304" height="136" rx="8" fill="#39d2c0" fill-opacity=".07" stroke="#39d2c0" stroke-width="2"/>
<text x="170" y="134" font-size="17" fill="#39d2c0" font-weight="600" text-anchor="middle">a view of the chapter's figure</text>
<text x="170" y="160" font-size="15" fill="#a9b4c2" text-anchor="middle">laid out for this finding</text>
<text x="18" y="234" font-size="14" fill="#7d8896" font-family="'IBM Plex Mono',ui-monospace,monospace">scope line</text>
<path d="M104 230H322" stroke="#2f3b4a" stroke-width="1.5"/>
<path d="M170 262v22m-8-8 8 8 8-8" fill="none" stroke="#a9b4c2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="190" y="280" font-size="15" fill="#a9b4c2">read on</text>
<rect x="2" y="296" width="336" height="232" rx="12" fill="#121a24" stroke="#2f3b4a" stroke-width="1.5"/>
<text x="18" y="326" font-size="14" fill="#7d8896" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">IN THE READER</text>
<text x="18" y="356" font-size="18" fill="#e6edf3" font-weight="600">the full chapter</text>
<rect x="18" y="370" width="260" height="6" rx="3" fill="#a9b4c2" fill-opacity=".5"/>
<rect x="18" y="390" width="140" height="64" rx="6" fill="#0f1d22" stroke="#39d2c0" stroke-width="2"/>
<text x="88" y="428" font-size="16" fill="#39d2c0" font-weight="600" text-anchor="middle" font-family="'IBM Plex Mono',ui-monospace,monospace">Figure</text>
<text x="176" y="418" font-size="15" fill="#39d2c0" font-weight="600">the face is</text>
<text x="176" y="438" font-size="15" fill="#39d2c0" font-weight="600">a view of it</text>
<text x="18" y="490" font-size="15" fill="#a9b4c2">every fact, with its evidence</text>
<rect x="18" y="502" width="220" height="6" rx="3" fill="#a9b4c2" fill-opacity=".5"/>
<rect x="2" y="552" width="120" height="68" rx="8" fill="none" stroke="#7d8896" stroke-width="1.5" stroke-dasharray="6 4"/>
<path d="M14 562l96 48M110 562l-96 48" stroke="#ff7b72" stroke-width="2.5" stroke-linecap="round"/>
<text x="140" y="580" font-size="17" fill="#e6edf3" font-weight="600">nothing to show</text>
<text x="140" y="606" font-size="17" fill="#ff7b72" font-weight="600">no face</text>
</g>
</svg>
<figcaption>Figure 4 redrawn: the face enlarged beside the chapter it opens</figcaption>
</figure>
</div>
<p class="slide-scope">Wireframe of a face · no measured results</p>
<!-- /slide -->

## Open a chapter with one slide, then read on

<p class="bs-lead">A slide face shows its chapter's finding with one real visual; the chapter remains the complete, readable source of every claim.</p>

[Figure 4](#fig-slide-anatomy) shows the parts of a face and where its content comes from. Follow the numbers: the title states the finding (01), a visual drawn from the chapter's figure fills most of the canvas (02), a scope line closes the face (03), and the full chapter follows (04).

<div class="bs-grid g2">
<figure id="fig-slide-anatomy">
<!-- include: fragments/slide-anatomy.html -->
<figcaption><b>Figure 4.</b> A face is a 16:9 view of its chapter: the finding as the title, a view of the chapter's figure laid out for that finding, and a scope line. A chapter with nothing to show gets no face. This hand-authored SVG wireframe contains no measured results.</figcaption>
</figure>
<div class="bs-part bs-orange"><span class="bs-label">Read the figure</span><h3>What a face holds</h3><ol>
<li><b>The title states the finding.</b> A sentence, not a topic. The label row above it names the subject.</li>
<li><b>A visual fills the canvas.</b> The chapter's figures and numbers are its material: the face may crop, combine, annotate or redraw them, and shows nothing the chapter does not state. When the chapter has no figure yet, make one for the chapter first from what exists; never draw invented data.</li>
<li><b>The scope line closes it.</b> Between the title and the scope line, the shape of the finding sets the layout: this page's two faces are a matrix of folders and the face drawn large beside its chapter; another face may be a timeline or a row of steps. Labels sit on the parts they name, and only what the title names is emphasised. Boxes that only repeat the title are not a visual.</li>
<li><b>The chapter follows in full.</b> Every fact on the face is also stated, with its evidence, in the chapter below.</li>
</ol></div>
</div>

**Faces come last.** Build the chapters first, so each one is complete before any slide exists. Then ask the person whether the page should get faces, and add them only after a yes. A chapter with nothing to show gets no face; on this page only the first chapter and this one have faces.

Write the face between `<!-- slide -->` and `<!-- /slide -->` at the start of a chapter. The reader shows it as a 16:9 slide at the top of the card, followed by the full chapter. Neither face here repeats its chapter's figure unchanged: the first sets the three folders of Figure 1 against who writes them and how they change, and this one draws Figure 4's face large beside the chapter it opens. Every word on a face is also in its chapter, so a change updates both in the same edit. `python docsite.py slides --project . --select guide --out guide` collects the faces into a deck that can be presented or printed. The <a href="../topics/guide/guide.md#slide-faces">agent record</a> lists these rules.

</section>

<section class="card" id="review">

## Review the page where people will read it

<p class="bs-lead">A successful source check still needs a rendered review of the changed layout.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Wide and paired</span><h3>Use the available width</h3><p>Check readable chart labels, balanced rows, full-width evidence and two-column comparisons. Keep controls next to their result.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">Narrow and accessible</span><h3>Keep every action reachable</h3><p>Check contained tables and equations, keyboard focus, clear labels, touch targets, reduced motion, print and no-JavaScript reading.</p></div>
</div>

### What remains for this adoption

<div class="bs-board">
<div class="bs-row"><span class="bs-state bs-ok">Decided</span><b>Ownership model</b><span>Use a version-pinned shared kit, with project-owned content and navigation.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Project identity</b><span>Replace the example repository and choose the source revision used by source links.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Integration checks</b><span>Build, check freshness, lint and inspect the consumer's actual output before adoption.</span></div>
</div>

This board describes starter adoption, not completed test execution. The <a href="../topics/guide/guide.md#acceptance-checklist">agent record</a> owns the exact checklist; <a href="../open/OPEN.md">open routing</a> points to it.

</section>

<section class="card" id="choice">

## Choose shared maintenance with a deliberate update point

<p class="bs-lead">A pinned submodule fits projects that need the same visual language without surrendering their own release schedule.</p>

<div class="scroll" role="region" aria-label="Maintenance options; scroll horizontally" tabindex="0" data-reader-horizontal>

| Option | Shared fixes | Project control | Maintenance cost | Verdict |
|---|---|---|---|---|
| Copy the theme into every project | Reapply each fix separately | Direct local edits | Copies can drift | Suitable only for an intentionally independent fork |
| Pinned shared-kit submodule | Adopt a reviewed kit revision | Content, overrides and update timing stay local | Initialize and review each upgrade | Selected for this starter |
| Independently build each site's engine | No common update path | Complete freedom | Maintain reader, checks and theme per project | Use when requirements differ enough to justify it |

</div>

The verdict follows ownership and update behavior, not a measured speed comparison. Keep a kit upgrade reviewable: change the pin, rebuild the consumer and inspect its actual pages.

<!-- fold: dead-end Why a copied reader creates more owners -->

A local copy can be appropriate for a deliberate fork. It stops being a shared component: fixes to keyboard behavior, deep links and saved reading positions must be integrated independently. Record that ownership decision rather than treating the fork as an automatic shared-kit update.

<!-- /fold -->

</section>
