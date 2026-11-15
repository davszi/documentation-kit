+++
title = "Get started"
brand_sub = "what it provides · how it works · set up · adopt"
description = "What the kit provides, how a project routes contributors to its rules, the three practice areas, how to set it up and which adoption route fits."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["What it provides", "#what-the-kit-provides"], ["How it works", "#how-it-works"], ["Practice areas", "#practice-areas"], ["Set up", "#set-up"], ["Starter files", "#starter-files"], ["Adoption routes", "#choose-how-to-adopt-it"]]
page_only = "Explains the kit as a whole; its records are README.md and the guides in rules/."
+++

# Get started with the documentation kit

<section class="card" id="what-the-kit-provides">

<!-- slide -->
<style>
/* Local to this face: one timeline across the canvas; a tall drawing replaces it below 720 px. */
.slide-main.fx-pin {justify-content:flex-start!important;gap:0!important;}
.fx-pin > figure {flex:1 1 0!important;min-height:0!important;display:flex!important;flex-direction:column!important;gap:.4cqi!important;margin:0!important;}
.fx-pin svg {display:block!important;width:100%!important;}
.fx-pin svg.fx-wide {flex:1 1 0!important;min-height:0!important;height:100%!important;}
.fx-pin svg.fx-tall {display:none!important;}
.fx-pin figcaption {font:1cqi/1.3 "IBM Plex Mono",monospace!important;color:var(--sf-dim)!important;text-align:right!important;}
@container (max-width: 719.98px) {
  .fx-pin > figure {flex:none!important;}
  .fx-pin svg.fx-wide {display:none!important;}
  .fx-pin svg.fx-tall {display:block!important;height:auto!important;}
  .fx-pin figcaption {font-size:12px!important;text-align:left!important;}
}
</style>
<p class="slide-eyebrow">Documentation kit</p>
<p class="slide-title">A rule fixed once in the kit reaches each project that moves its pin</p>
<div class="slide-main fx-pin">
<figure>
<svg class="inline-fig fx-wide" viewBox="0 0 1200 526" role="img" aria-label="The kit repository is one line of revisions. A rule fix lands there once. Project A is still pinned to an older revision, so the fix has not reached it yet; it arrives when A moves its pin. Project B moved its pin past the fix and has it. A guide copied into a project and edited there never receives the fix. Each project keeps its own records, pages, commands and exceptions.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<text x="40" y="40" font-size="19" fill="#bc8cff" font-weight="600" letter-spacing="3" font-family="'IBM Plex Mono',ui-monospace,monospace">KIT REPOSITORY</text>
<text x="262" y="40" font-size="19" fill="#7d8896">one line of revisions</text>
<path d="M40 92H1150" stroke="#bc8cff" stroke-width="4" stroke-opacity=".45"/>
<path d="M1170 92l-20-9v18z" fill="#bc8cff" fill-opacity=".45"/>
<path d="M800 92H960" stroke="#39d2c0" stroke-width="7" stroke-linecap="round"/>
<circle cx="800" cy="92" r="40" fill="#39d2c0" fill-opacity=".13"/>
<circle cx="800" cy="92" r="18" fill="#39d2c0"/>
<text x="800" y="44" font-size="27" fill="#39d2c0" font-weight="600" text-anchor="middle">rule fix lands once</text>
<g fill="#0d1117" stroke="#bc8cff" stroke-width="4"><circle cx="150" cy="92" r="11"/><circle cx="340" cy="92" r="11"/><circle cx="530" cy="92" r="11"/><circle cx="1110" cy="92" r="11"/></g>
<circle cx="960" cy="92" r="12" fill="#0d1117" stroke="#39d2c0" stroke-width="5"/>
<path d="M150 104V196" stroke="#ff7b72" stroke-width="3" stroke-dasharray="8 7"/>
<text x="164" y="158" font-size="18" fill="#ff7b72">copied, then edited</text>
<path d="M530 104V196" stroke="#bc8cff" stroke-width="3" stroke-dasharray="8 7"/><circle cx="530" cy="196" r="6" fill="#bc8cff"/>
<text x="544" y="158" font-size="18" fill="#a9b4c2">pinned</text>
<path d="M960 105V196" stroke="#39d2c0" stroke-width="4"/><circle cx="960" cy="196" r="7" fill="#39d2c0"/>
<text x="974" y="158" font-size="18" fill="#39d2c0" font-weight="600">pin moved</text>
<rect x="30" y="196" width="340" height="320" rx="16" fill="#1a1619" stroke="#ff7b72" stroke-width="2" stroke-opacity=".7" stroke-dasharray="10 7"/>
<text x="54" y="236" font-size="17" fill="#ff7b72" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">COPIED RULE</text>
<text x="54" y="282" font-size="25" fill="#e6edf3" font-weight="600">a pasted guide</text>
<text x="54" y="312" font-size="20" fill="#a9b4c2">edited inside the project</text>
<path d="M54 344H346" stroke="#2f3b4a" stroke-width="2"/>
<text x="54" y="394" font-size="26" fill="#ff7b72" font-weight="600">never gets the fix</text>
<circle cx="330" cy="385" r="17" fill="none" stroke="#ff7b72" stroke-width="3"/><path d="M322 377l16 16M338 377l-16 16" stroke="#ff7b72" stroke-width="3.5" stroke-linecap="round"/>
<text x="54" y="430" font-size="19" fill="#a9b4c2">and nobody can tell which</text>
<text x="54" y="456" font-size="19" fill="#a9b4c2">sentences are shared</text>
<rect x="430" y="196" width="340" height="320" rx="16" fill="#121a24" stroke="#2f3b4a" stroke-width="2"/>
<text x="454" y="236" font-size="17" fill="#7d8896" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">PROJECT A</text>
<text x="454" y="282" font-size="25" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="454" y="312" font-size="20" fill="#a9b4c2">older pin</text>
<path d="M454 344H746" stroke="#2f3b4a" stroke-width="2"/>
<text x="454" y="394" font-size="26" fill="#e6edf3" font-weight="600">fix not here yet</text>
<text x="454" y="430" font-size="19" fill="#a9b4c2">it arrives when A moves its pin</text>
<text x="454" y="486" font-size="17" fill="#7d8896">own records, pages, commands</text>
<text x="454" y="508" font-size="17" fill="#7d8896">and exceptions</text>
<rect x="830" y="196" width="340" height="320" rx="16" fill="#0f1d22" stroke="#39d2c0" stroke-width="3"/>
<text x="854" y="236" font-size="17" fill="#7d8896" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">PROJECT B</text>
<text x="854" y="282" font-size="25" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="854" y="312" font-size="20" fill="#a9b4c2">moved its pin</text>
<path d="M854 344H1146" stroke="#2a5f5a" stroke-width="2"/>
<text x="854" y="394" font-size="28" fill="#39d2c0" font-weight="600">has the rule fix</text>
<circle cx="1130" cy="385" r="17" fill="#39d2c0"/><path d="M1121 385l6 6 12-12" fill="none" stroke="#0d1117" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="854" y="430" font-size="19" fill="#a9b4c2">picked up when B moved its pin</text>
<text x="854" y="486" font-size="17" fill="#7d8896">own records, pages, commands</text>
<text x="854" y="508" font-size="17" fill="#7d8896">and exceptions</text>
</g>
</svg>
<svg class="inline-fig fx-tall" viewBox="0 0 340 720" role="img" aria-label="The kit repository is one line of revisions. A rule fix lands there once. A guide copied into a project and edited there never receives the fix. Project A is still pinned to an older revision; the fix arrives when A moves its pin. Project B moved its pin past the fix and has it.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<text x="0" y="18" font-size="15" fill="#bc8cff" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">KIT REPOSITORY</text>
<path d="M14 34V692" stroke="#bc8cff" stroke-width="3" stroke-opacity=".45"/>
<path d="M14 712l-8-18h16z" fill="#bc8cff" fill-opacity=".45"/>
<path d="M14 452V530" stroke="#39d2c0" stroke-width="6" stroke-linecap="round"/>
<g fill="#0d1117" stroke="#bc8cff" stroke-width="3"><circle cx="14" cy="70" r="8"/><circle cx="14" cy="226" r="8"/><circle cx="14" cy="262" r="8"/><circle cx="14" cy="676" r="8"/></g>
<circle cx="14" cy="452" r="22" fill="#39d2c0" fill-opacity=".14"/><circle cx="14" cy="452" r="11" fill="#39d2c0"/>
<text x="40" y="458" font-size="18" fill="#39d2c0" font-weight="600">rule fix lands once</text>
<circle cx="14" cy="530" r="9" fill="#0d1117" stroke="#39d2c0" stroke-width="4"/>
<path d="M22 70H40" stroke="#ff7b72" stroke-width="2.5" stroke-dasharray="5 4"/>
<rect x="40" y="44" width="298" height="166" rx="12" fill="#1a1619" stroke="#ff7b72" stroke-width="1.5" stroke-opacity=".7" stroke-dasharray="8 6"/>
<text x="56" y="72" font-size="15" fill="#ff7b72" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">COPIED RULE</text>
<text x="56" y="100" font-size="17" fill="#a9b4c2">a pasted guide, edited</text>
<text x="56" y="122" font-size="17" fill="#a9b4c2">inside the project</text>
<text x="56" y="160" font-size="20" fill="#ff7b72" font-weight="600">never gets the fix</text>
<text x="56" y="188" font-size="16" fill="#a9b4c2">nobody can tell what is shared</text>
<path d="M22 262H40" stroke="#bc8cff" stroke-width="2.5" stroke-dasharray="5 4"/>
<rect x="40" y="236" width="298" height="184" rx="12" fill="#121a24" stroke="#2f3b4a" stroke-width="1.5"/>
<text x="56" y="264" font-size="15" fill="#7d8896" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">PROJECT A</text>
<text x="56" y="294" font-size="19" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="178" y="294" font-size="17" fill="#a9b4c2">older pin</text>
<text x="56" y="334" font-size="20" fill="#e6edf3" font-weight="600">fix not here yet</text>
<text x="56" y="360" font-size="16" fill="#a9b4c2">it arrives when A moves its pin</text>
<text x="56" y="398" font-size="15" fill="#7d8896">own records, pages, commands</text>
<path d="M23 530H40" stroke="#39d2c0" stroke-width="3"/>
<rect x="40" y="496" width="298" height="166" rx="12" fill="#0f1d22" stroke="#39d2c0" stroke-width="2"/>
<text x="56" y="524" font-size="15" fill="#7d8896" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">PROJECT B</text>
<text x="56" y="554" font-size="19" fill="#bc8cff" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="178" y="554" font-size="17" fill="#39d2c0" font-weight="600">moved its pin</text>
<text x="56" y="596" font-size="22" fill="#39d2c0" font-weight="600">has the rule fix</text>
<text x="56" y="622" font-size="16" fill="#a9b4c2">picked up with the pin</text>
<text x="56" y="648" font-size="15" fill="#7d8896">own records, pages, commands</text>
</g>
</svg>
<figcaption>Figure 1 redrawn, with the copied rule from the example below it</figcaption>
</figure>
</div>
<p class="slide-scope">Illustration of the ownership split · no measured results</p>
<!-- /slide -->

## One pinned submodule gives a project shared rules and tools

<p class="bs-lead">The kit supplies rules, a reader and a site toolchain. Your project keeps its content, its specifics and the decision when to upgrade.</p>

<div class="bs-grid g2">
<figure id="fig-kit-pin">
<svg class="inline-fig" viewBox="0 0 600 400" role="img" aria-label="Two projects share one kit. The kit repository is a line of revisions; a rule fix lands there once. Each project holds the kit as a .docs-kit submodule pinned to the revision it chose, next to its own records, pages, commands and exceptions. Project A is still pinned to an older revision; project B moved its pin and has the fix.">
<text x="8" y="30" font-size="25" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">KIT REPOSITORY</text>
<path d="M20 70H584" stroke="#bc8cff" stroke-width="3" opacity=".55"/>
<circle cx="60" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="170" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="280" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="390" cy="70" r="12" fill="#39d2c0" stroke="#39d2c0" stroke-width="3"/>
<circle cx="520" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<text x="390" y="110" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">rule fix lands once</text>
<rect x="8" y="130" width="286" height="266" rx="16" fill="none" stroke="#2f3b4a" stroke-width="2"/>
<text x="24" y="162" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">project A</text>
<rect x="24" y="176" width="254" height="84" rx="10" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="40" y="210" font-size="28" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="40" y="246" font-size="25" fill="#a9b4c2" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">older pin</text>
<rect x="24" y="272" width="254" height="110" rx="10" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="40" y="304" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">own records,</text>
<text x="40" y="333" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">pages, commands,</text>
<text x="40" y="362" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">exceptions</text>
<path d="M170 82V176" stroke="#bc8cff" stroke-width="3" stroke-dasharray="7 6"/>
<circle cx="170" cy="176" r="6" fill="#bc8cff"/>
<rect x="306" y="130" width="286" height="266" rx="16" fill="none" stroke="#2f3b4a" stroke-width="2"/>
<text x="322" y="162" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">project B</text>
<rect x="322" y="176" width="254" height="84" rx="10" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="338" y="210" font-size="28" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="338" y="246" font-size="25" fill="#39d2c0" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">moved its pin</text>
<rect x="322" y="272" width="254" height="110" rx="10" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="338" y="304" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">own records,</text>
<text x="338" y="333" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">pages, commands,</text>
<text x="338" y="362" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">exceptions</text>
<path d="M520 82V176" stroke="#bc8cff" stroke-width="3" stroke-dasharray="7 6"/>
<circle cx="520" cy="176" r="6" fill="#bc8cff"/>
<circle cx="262" cy="24" r="22" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/><text x="262" y="33" font-size="25" fill="#bc8cff" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">01</text>
<circle cx="274" cy="278" r="22" fill="#0d1117" stroke="#39d2c0" stroke-width="3"/><text x="274" y="287" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">02</text>
<circle cx="574" cy="182" r="22" fill="#0d1117" stroke="#39d2c0" stroke-width="3"/><text x="574" y="191" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">03</text>
</svg>
<figcaption><b>Figure 1.</b> Two projects share one kit. A rule fix lands in the kit once; each project picks it up when it moves its pin. This illustrative SVG diagram is authored in the page source and contains no measured results.</figcaption>
</figure>
<div class="bs-grid g1">
<div class="bs-part bs-violet"><span class="bs-label">The kit supplies · <code>.docs-kit/</code></span><h3>Shared and pinned</h3><ul>
<li><code>rules/</code>: engineering, documentation, record, page-writing and experiment guides your router points to</li>
<li><code>theme/</code>: chapter reader, build-sheet layout, fonts and math (<a href="build-a-site.html#the-reader">the reader</a>)</li>
<li><code>docsite.py</code>, <code>tooling/</code>: build, lint, slides and export (<a href="build-a-site.html">build a site</a>)</li>
<li><code>examples/starter/</code>: the project that <code>init</code> writes without overwriting</li>
</ul></div>
<div class="bs-part bs-teal"><span class="bs-label">Your project keeps</span><h3>Owned and local</h3><ul>
<li>repository map, commands and routes in <code>docs/PROJECT_CONTEXT.md</code> and <code>AGENTS.md</code></li>
<li>tools, workloads, resource profiles and acceptance thresholds</li>
<li>topic records, pages, navigation, evidence and figures</li>
<li>any exception to a shared rule, where contributors will find it</li>
<li>when to adopt a reviewed kit revision</li>
</ul></div>
</div>
</div>

[Figure 1](#fig-kit-pin) shows the split with two projects; its numbers mark the shared kit (01), the project's own content (02) and the pin each project moves (03). Each holds the kit as a `.docs-kit` submodule next to its own records, pages, commands and exceptions. Project A is still pinned to an older kit revision; project B moved its pin and has the rule fix. A rule that several projects share has one home: the kit. Without that, each project keeps its own copy, a fix lands in one copy and the others drift. The split also works the other way: a project's commands, thresholds and exceptions are facts about that project, so they stay in its own records, where its contributors look. Changing a common rule means changing the kit; a project picks the change up when it moves its pin.

<div class="bs-specs"><div><span class="bs-label">Install</span><b>One submodule</b></div><div><span class="bs-label">Needed to use the rules</span><b>Router rows</b></div><div><span class="bs-label">Site build</span><b>Optional</b></div></div>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Copy the rule and edit it locally</h3><p>A project pastes the Git guide into its own docs and adds its test command in the middle. The next kit fix never reaches it, and nobody can tell which sentences are shared and which are local.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Point at the rule, keep the specifics apart</h3><p>The project's router names <code>.docs-kit/rules/engineering/git.md</code> and the project's validation record. The guide stays shared; the test command lives in the project.</p></div>
</div>

<!-- fold: code Which paths belong to whom -->

| Shared kit | Each project |
|---|---|
| `rules/`: engineering, documentation, writing and site practices | `docs/PROJECT_CONTEXT.md`, `docs/index.md`: orientation, reading routes, project additions |
| `theme/`: HTML shell, chapter reader, CSS/JS, fonts, math | `docs/topics/`: records and optional rendered `index.md` pages |
| `tooling/`, `docsite.py`: renderer, packaging, checks | `docs/site/site.toml`, local CSS and components, `docs/figures/` |
| `examples/starter/`: the starter `init` writes | open plans, evidence, dated sessions and `docs/worklog.md` |

The full split is in [Ownership](readme.html#ownership); [canonical homes](documentation-system.html#canonical-homes) explains the one-home rule.

<!-- /fold -->

</section>

<section class="card" id="how-it-works">

## Each rule is read right before the action it governs

<p class="bs-lead">Pin the kit once; your <code>AGENTS.md</code> names, for each kind of action, the kit guide and your own record to read first.</p>

<figure id="fig-routing">
<div class="bs-flow" role="img" aria-label="Step 1: pin the kit at .docs-kit. Step 2: in AGENTS.md, add a row for each kind of action that names the kit guide and the project's own record, for example staging or committing with rules/engineering/git.md and the project's validation records. Step 3: before that action, a contributor or agent reads both, then acts.">
<div class="bs-node bs-teal"><span class="bs-label">Step 1 · once</span><b>Pin the kit</b><ul><li><code>.docs-kit</code> submodule</li><li>its commit is your version</li></ul></div>
<div class="bs-arrow"><span>route</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Step 2 · <code>AGENTS.md</code></span><b>One row per action</b><ul><li>before committing…</li><li>…read <code>rules/engineering/git.md</code> and your validation records</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Step 3 · every time</span><b>Read both, then act</b><ul><li>shared rule + project specifics</li><li>nothing is copied</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> Adoption is a pointer, not a copy: one router row joins a shared rule with the project's own specifics. This diagram contains no measured results.</figcaption>
</figure>

[Figure 2](#fig-routing) is the whole mechanism. The router is triggered by the action, not the topic: an agent about to commit reads the Git guide, not every guide. That keeps each task's reading short and makes it hard to skip the rule that applies. Read the orientation and the rules that apply to every task once at the start; route the rest by action, and recheck the routes when the task grows. Reading a route grants no permission to run or publish anything.

```markdown
| Before…                      | Read…                                                                 |
|------------------------------|-----------------------------------------------------------------------|
| Making a performance claim   | `.docs-kit/rules/engineering/performance.md` and our workload records |
| Writing or changing a record | `.docs-kit/rules/records.md`                                          |
| Staging or committing        | `.docs-kit/rules/engineering/git.md` and our validation records       |
```

Documentation work has three rows, because three different jobs need different guides. A record writer reads the records guide and the documentation system's sections on order of work and changes. Someone creating, moving or retiring a document reads the documentation system. Page work sends its author to the page and site guides: a new page only when someone asked for it, and work on an existing page when a record change needs more than a small sync of a sentence or two. A record edit therefore no longer pulls in the page guides' layout and presentation rules.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A topic list</h3><p>"Documentation: see rules/. Git: see git.md." Nothing says when to read which, so an agent either reads everything up front or nothing at the moment it matters.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>An action trigger</h3><p>"Before staging or committing: read the Git guide and our validation records." The row fires at the moment of the action and names both owners.</p></div>
</div>

<!-- fold: code How Codex and Claude Code read the same router -->

Keep one thin router in `AGENTS.md`. Codex follows its named paths and triggers directly. For Claude Code, `CLAUDE.md` contains a bare, standalone `@AGENTS.md` import, so both clients use the same router; backticks or a fence would make the import literal. Submodule consumers initialize `.docs-kit` before relying on its rules, and report a missing policy instead of working around it. The [starter's router](../../examples/starter/AGENTS.md.tmpl) has every row; see [agent entrypoints](documentation-system.html#agent-entrypoints-import-versus-point).

<!-- /fold -->

</section>

<section class="card" id="practice-areas">

## Three practice areas, each explained on its own page

<p class="bs-lead">Each page explains its guides with reasons and examples and lists the router row for every guide; the guides stay the exact reference.</p>

<div class="bs-grid g3">
<div class="bs-part bs-teal"><span class="bs-label">Code, runs and delivery</span><h3><a href="engineering-practices.html">Engineering</a></h3><ul>
<li>consumed output is an interface; generated files change at their source</li>
<li>efficient by default; a performance claim names its workload and path</li>
<li>expensive jobs run on the project's route, under a stated budget, owned through cleanup</li>
<li>the owner finishes routine work; changes to the agreement go back for a decision</li>
<li>reports lead with the outcome and say how each claim is known</li>
<li>one commit per logical deliverable, reviewed as a whole</li>
</ul><p><b>Read before:</b> changing code, running heavy jobs, handing off, committing.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Records and pages</span><h3><a href="writing-practices.html">Documentation and writing</a></h3><ul>
<li>every fact has one home; finished work moves to its subject</li>
<li>the record is written first; a new page only when a person asks</li>
<li>a record names each object once; a measured number carries its provenance</li>
<li>each section states its takeaway before the evidence</li>
<li>one visible story; optional depth in typed folds</li>
<li>figures, mathematics and code excerpts follow shared conventions</li>
</ul><p><b>Read before:</b> creating or moving a document, writing a record, making or updating a page.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">Investigations and qualifications</span><h3><a href="experiments.html">Experiments</a></h3><ul>
<li>start with the smallest experiment that can change a decision</li>
<li>classify by what the result decides: investigation or qualification</li>
<li>build on existing evidence and stop once the question is answered</li>
<li>state the plan before running; report every attempt after</li>
<li>final runs only when results depend on a learned or fitted model</li>
<li>add a check only for a named gap; never lower a failed bar</li>
</ul><p><b>Read before:</b> designing or running an experiment, choosing its checks.</p></div>
</div>

Each practice page starts with a router table for its guides, so you can copy the rows you need into your `AGENTS.md`. The bullets above summarise each page's chapter claims; open a page for the reason behind each rule and a worked example.

<!-- fold: dead-end Old links to the writing and maintenance routers -->

The [writing](writing.html) and [site maintenance](maintenance.html) entrypoints are short indexes that list the focused guides and what each one owns. The writing index now covers pages for people only. What a record must say, including naming, honest claims and measured numbers, has its own guide, [writing records](records.html), which the router names directly.

<!-- /fold -->

</section>

<section class="card" id="set-up">

## A new project needs one submodule, one environment and one init

<p class="bs-lead">Pin the kit, install its pinned Python packages, let <code>init</code> add the starter, then track what it wrote.</p>

<figure id="fig-setup">
<div class="bs-flow" role="img" aria-label="Pin the kit as a submodule at .docs-kit, then create a Python 3.12 environment with the kit's pinned requirements, then run docsite.py init with the project's title and repository, which writes the starter files. Finally track the sources in Git, because the build only publishes tracked files.">
<div class="bs-node bs-teal"><span class="bs-label">Once</span><b>Pin and install</b><ul><li><code>.docs-kit</code> submodule</li><li>Python 3.12 env, pinned packages</li></ul></div>
<div class="bs-arrow"><span>init</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>docsite.py init</code></span><b>Write the starter</b><ul><li>never overwrites a file</li><li>fills title and repository</li></ul></div>
<div class="bs-arrow"><span>track</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Git</span><b>Track the sources</b><ul><li>the build publishes tracked files only</li><li>add <code>.build/</code> to <code>.gitignore</code></li></ul></div>
</div>
<figcaption><b>Figure 3.</b> Setup in three steps. This diagram contains no measured results.</figcaption>
</figure>

```bash
git submodule add <kit-url> .docs-kit
git submodule update --init --recursive
python3.12 -m venv .build/docs-env
.build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
.build/docs-env/bin/python .docs-kit/docsite.py init . --title "My project" --repository https://github.com/owner/repo
git add docs AGENTS.md CLAUDE.md .gitmodules .docs-kit
```

<div class="bs-grid g2">
<div class="bs-part bs-violet"><span class="bs-label">What <code>init</code> writes</span><h3>Your project's entry files</h3><ul>
<li><code>AGENTS.md</code>, <code>CLAUDE.md</code>: the task router and its Claude import</li>
<li><code>docs/PROJECT_CONTEXT.md</code>, <code>docs/index.md</code>: repository map and reading routes</li>
<li><code>docs/worklog.md</code>, <code>docs/open/OPEN.md</code>: chronology and open work</li>
<li><code>docs/site/site.toml</code>: title, repository and navigation</li>
<li><code>docs/topics/</code>: a home page and a visual guide to replace</li>
</ul></div>
<div class="bs-part bs-teal"><span class="bs-label">Safe to run</span><h3>It never overwrites your work</h3><ul>
<li>checks every destination before writing</li>
<li>writes nothing if any of them already exists</li>
<li>the title defaults to the folder name</li>
<li>track what it wrote: the build publishes tracked files only</li>
</ul><p>Next: <a href="build-a-site.html">Build a site</a> covers how the build works, build, lint, preview and upgrades. A project that only adopts the rules can stop after the submodule and its router rows.</p></div>
</div>

<div class="bs-specs"><div><span class="bs-label">Python</span><b>3.12+</b></div><div><span class="bs-label">Packages</span><b>Pinned</b></div><div><span class="bs-label">JavaScript install</span><b>None</b></div></div>

</section>

<section class="card" id="starter-files">

## Every file the starter writes has one job

<p class="bs-lead">Agents start at the router, people start at the pages, and each kind of content has exactly one file to live in.</p>

```text
my-project/
├── AGENTS.md                 task router: which kit guide and project record to read before each action
├── CLAUDE.md                 one line, @AGENTS.md, so Claude Code follows the same router
├── .gitignore                keeps .build/ (environment and generated site) out of Git
├── .docs-kit/                the pinned kit (submodule); read it, never edit it here
└── docs/
    ├── PROJECT_CONTEXT.md    repository map, build and review commands, project choices
    ├── index.md              reading index: which document owns what, and the shared practices
    ├── worklog.md            append-only chronology, newest entries first
    ├── open/OPEN.md          open work: one line per item, each linking the record that owns it
    ├── site/site.toml        site title, source repository, navigation
    └── topics/
        ├── home/index.md     home page: hero and an automatic card for every page
        └── guide/
            ├── index.md      page for people: the visual guide, in reader chapters
            └── guide.md      record for agents: scope, ownership and acceptance checklist
```

<div class="bs-grid g3">
<div class="bs-part bs-teal"><span class="bs-label">Read first by agents</span><h3>Entry and orientation</h3><ul>
<li><code>AGENTS.md</code> routes each action to its guides; <code>CLAUDE.md</code> imports it</li>
<li><code>PROJECT_CONTEXT.md</code> holds the map and commands the routes point to</li>
<li><code>index.md</code> says where each kind of document lives</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">Change over time</span><h3>Records</h3><ul>
<li><code>worklog.md</code>: what landed and when, never rewritten</li>
<li><code>open/OPEN.md</code>: what is still owed, deleted when done</li>
<li><code>topics/*/*.md</code>: one record per subject, the exact contract</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">Become the website</span><h3>The site</h3><ul>
<li><code>site/site.toml</code>: title, repository and menu</li>
<li><code>topics/*/index.md</code>: pages for people, built into <code>.build/docs/</code></li>
<li>the home page lists every page automatically</li>
</ul></div>
</div>

Each file has one job so that nobody has to guess where something goes, and an agent can find the current answer without reading everything. A fact written into the wrong file is the start of a second copy: the router grows a command, the page grows a task list, and the two drift apart. The guide topic shows the pairing every later topic follows: a record (`guide.md`) for the exact contract and a page (`index.md`) that explains it.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Commands in the router</h3><p>A new build flag is added to <code>AGENTS.md</code>, and a different version of it to the guide page. Agents and readers now see two commands.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>One home, linked</h3><p>The flag goes into <code>PROJECT_CONTEXT.md</code> under build and review. The router's row and the page both link there.</p></div>
</div>

<!-- fold: code What is not in the project, and why -->

`.docs-kit/` is the kit's own repository, pinned as a submodule: its rules, theme and tools. Change a shared rule in the kit itself, never in a project's checkout of it. `.build/` holds the Python environment (`.build/docs-env/`) and the generated site (`.build/docs/`); both are recreated by commands and stay out of Git through `.gitignore`. Generated pages are never edited; change the source and rebuild. Inside the kit, the starter's entry files are stored as `*.tmpl` so none of them is active there; `init` writes them under the names above.

<!-- /fold -->

</section>

<section class="card" id="choose-how-to-adopt-it">

## Pick the adoption route that matches what you already have

<p class="bs-lead">A new project starts from the starter; existing documentation stays where it is; a project can also adopt the rules alone.</p>

<div class="bs-grid g3">
<div class="bs-part bs-teal" id="route-new"><span class="bs-label">You have no documentation yet</span><h3 id="route-new-project">New project</h3><ol>
<li>Run the commands in <a href="#set-up">set up</a>.</li>
<li>Replace the starter's guide with your topics, following <a href="authoring.html#authoring-paths">authoring paths</a>.</li>
<li>Fill <code>docs/PROJECT_CONTEXT.md</code> with your repository map and commands.</li>
<li>Keep the single task router the starter adds and trim its rows to what you need.</li>
</ol><p><b>Stays as is:</b> nothing yet; the starter gives you the full structure.</p></div>
<div class="bs-part bs-violet" id="route-existing"><span class="bs-label">You already have docs</span><h3 id="route-existing-documentation">Existing documentation</h3><ol>
<li>Add the submodule; skip <code>init</code> and add <code>docs/site/site.toml</code> deliberately.</li>
<li>Publish existing Markdown in place as <a href="build-a-site.html#existing-markdown">registered records</a>; nothing moves.</li>
<li>Keep historical public routes with the <a href="publication.html">publication exporter</a>.</li>
<li>Replace a copied shared rule only once its project-specific parts have a linked home.</li>
</ol><p><b>Stays as is:</b> your content, destinations and history; the <a href="migrate-1-1-0.html#prepare-the-deliverable">migration guide</a> shows the review steps.</p></div>
<div class="bs-part bs-orange" id="route-practices"><span class="bs-label">You want the rules, not a site</span><h3 id="route-practices-only">Practices only</h3><ol>
<li>Add the submodule.</li>
<li>Add router rows to <code>AGENTS.md</code>, as in <a href="#how-it-works">how it works</a>.</li>
<li>Pick the rows from the <a href="#practice-areas">practice pages</a>.</li>
<li>Keep concrete commands, thresholds and resource profiles in your own records.</li>
</ol><p><b>Stays as is:</b> everything; no build, no new pages.</p></div>
</div>

All three routes share the same core: a pinned submodule and router rows. They differ only in how much of the site toolchain you take. You can start with practices only and add a site later without undoing anything; the rules and the router stay the same.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Run <code>init</code> over existing docs</h3><p>If any starter file already exists, <code>init</code> refuses and writes nothing; forcing a copy by hand would overwrite or duplicate the project's own records.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Register what is already there</h3><p>The project adds <code>site.toml</code>, registers its existing records as source pages and keeps every file where it was.</p></div>
</div>

</section>
