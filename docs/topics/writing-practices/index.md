+++
title = "Documentation and writing"
brand = "Documentation kit"
brand_sub = "homes · pages · evidence · figures"
description = "Where each kind of documentation belongs, why the rules exist, and how the kit's writing guides shape pages, explanations, evidence, figures, math and code, with illustrative examples."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Guide per task", "#routes"], ["One home", "#homes"], ["Open to topic", "#open-to-topic"], ["Topics", "#topics"], ["Records and pages", "#records-and-pages"], ["In step", "#page-and-record-in-step"], ["Changes and publishing", "#changes-and-publishing"], ["Section design", "#page-design"], ["Build sheets", "#build-sheets"], ["Story and folds", "#explanations"], ["Honest claims", "#honest-claims"], ["Evidence", "#evidence"], ["Figures", "#figures"], ["Mathematics", "#mathematics"], ["Code excerpts", "#code-excerpts"]]
page_only = "Explains the documentation and writing guides; they are the records, in rules/."
+++

# Documentation and writing

<section class="card" id="routes">

## Each guide owns one kind of documentation decision

<p class="bs-lead">The documentation system decides where content lives; six focused writing guides decide how a page presents it.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Documentation and writing guides by task">

| Before… | Read… | It covers | Explained here |
|---|---|---|---|
| Creating, moving or retiring a document | [Documentation system](documentation-system.html) | Canonical homes, the path from open work to topic, evidence identity, records and pages, agent entrypoints, changes, worklog and publishing | [One home](#homes), [Open to topic](#open-to-topic), [Records and pages](#records-and-pages), [Changes and publishing](#changes-and-publishing) |
| Upgrading the kit pin or taking over a repository | [Project conformance check](conformance.html) | Pin, router, copied rules, homes, topics, pages and records, open work, compatibility, changed rules, site | [Topics](#topics), [In step](#page-and-record-in-step) |
| Laying out a rendered page | [Page design](page-design.html) | Section purpose, takeaway titles, homepages, build-sheet blocks, status boards, slide faces, review | [Section design](#page-design), [Build sheets](#build-sheets) |
| Writing an explanation | [Explanations](explanations.html) | Story order, typed folds, naming, honest claims | [Story and folds](#explanations), [Honest claims](#honest-claims) |
| Quoting a measured number | [Evidence](evidence.html) | Required provenance, staleness, number ledgers, run visuals, experiment records | [Evidence](#evidence) |
| Adding a figure or comparison | [Figures](figures.html) | The visual completion gate, captions and references, comparisons, chart sizing, interaction and access | [Figures](#figures) |
| Writing mathematics | [Math](math.html) | Definitions, derivations, KaTeX use, verification of analytic claims | [Mathematics](#mathematics) |
| Showing code or a code diagram | [Code excerpts](code-excerpts.html) | Real excerpts with source metadata, rendering chrome, shared diagram semantics, diagram controls | [Code excerpts](#code-excerpts) |

</div>

The guides are records for agents and own the complete rules. This page explains them for people. Each chapter states a rule, the failure it prevents and one example of following it, puts further detail in folds and links back to the guide. The examples are invented for illustration: they describe no real project and contain no measured results.

</section>

<section class="card" id="homes">

## Every fact has one home, and other documents link to it

<p class="bs-lead">A fact is written once, in the record that owns it; every other document points there.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Main canonical homes">

| Content | Home |
|---|---|
| Project purpose, repository map, run and build instructions, named documentation routes | `docs/PROJECT_CONTEXT.md` |
| Reading routes to development guidance, topics, evidence, sessions and open work | `docs/index.md` |
| Mechanisms, accepted specifications, methods, scoped results and limits | `docs/topics/<topic>/<topic>.md` and further descriptively named records; every topic has one unless its page declares `page_only` |
| Human explanation of a topic: current conclusions, figures, decisions and blockers | `docs/topics/<topic>/index.md`, when needed |
| Unfinished delivery, prospective acceptance and unresolved choices with their owners | Named unfinished plans and decision records |
| A one-line route to every owed workstream | `docs/open/OPEN.md`, never a duplicate task board |
| Landed work, reasons, measured effects and probes | `docs/worklog.md`, append-only |
| Protocol, producing code, inputs, raw results, failures, source pins and reproduction | The producing experiment directory |
| Temporary coordination, assignments and resume state | `docs/sessions/`, when needed |

</div>

The documentation system starts from one rule: every fact has exactly one canonical home. Without it, copies drift: one is updated, another is not, and a reader cannot tell which to trust. So when copies disagree, the guide says to verify the owning source, correct the stray copy and update affected summaries in the same deliverable. The same reasoning rules out a generic archive, review collection or second status system created to avoid choosing an owner.

The table lists the homes most projects use; the guide lists every one, including the shared rules and the generated site.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>One command, three copies</h3><p>A run command is written into the project context, a topic page and an open plan. A later change updates one copy; the other two still show the old command.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>One home, linked</h3><p>The command lives in the project context, and the topic page and plan link to it. The README may repeat it briefly for a reader arriving cold and is swept in the same deliverable when the command changes.</p></div>
</div>

<!-- fold: code The README exception and project-local homes -->

`README.md` is the bounded exception. A human arriving cold may need the project's purpose, installation and run commands there, even when those facts have a canonical home elsewhere. Keep the repetition short and sweep the README in the same deliverable when those facts change; the verified canonical owner wins on conflict.

The kit's rules are shared policy. A consuming project's `docs/PROJECT_CONTEXT.md` owns its repository map, commands, named documentation routes and project-specific choices; the rules are not copied into project entrypoints.

The homes in the guide are canonical roles for new projects. Existing projects may retain explicit local destinations and compatibility routes. Create a directory or document only when content needs it, and link that owner from `docs/index.md`.

<!-- /fold -->

<!-- fold: dead-end Why not an archive or a second status board -->

Every other Markdown file must have a defined role: a subject record, log, experiment contract or guide, exact evidence, or unfinished plan or decision. A generic archive, review collection or second status system is not created to avoid choosing an owner; it would become another place where a fact can hide. Names explain the subject or mechanism, so vague labels such as `Info` or `Manager` are avoided.

<!-- /fold -->

Full guide: [documentation system](documentation-system.html), especially [canonical homes](documentation-system.html#canonical-homes) and [README is the bounded exception](documentation-system.html#readme-is-the-bounded-exception).

</section>

<section class="card" id="open-to-topic">

## Finished work moves to its subject; evidence stays where it was made

<p class="bs-lead">As work matures, each kind of content moves to the record that owns it, and the worklog records the landing.</p>

<figure id="fig-open-to-topic">
<div class="bs-flow" role="img" aria-label="Open work in a named plan, routed from OPEN.md, is investigated in producing work that keeps its evidence. Established findings move to the owning topic record, with accepted future specifications labelled apart from implemented behavior. A closed record supports current knowledge through a link and does not become a second knowledge home.">
<div class="bs-node bs-orange"><span class="bs-label">Open owner</span><b>Unfinished work</b><ul><li>Named plan or decision record</li><li>Unresolved choices and owners</li><li>Prospective acceptance</li><li>One-line route in <code>OPEN.md</code></li></ul></div>
<div class="bs-arrow"><span>investigate</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Producing work</span><b>Protocol and evidence</b><ul><li>Inputs and raw results</li><li>Failures and source pins</li><li>Reproduction instructions</li></ul></div>
<div class="bs-arrow"><span>establish</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Owning topic</span><b>Current knowledge</b><ul><li>Established behavior</li><li>Accepted requirements</li><li>Durable rationale</li><li>Accepted future specification, labelled apart</li></ul></div>
<div class="bs-back"><span>×</span> A closed record supports current knowledge through a link. It does not become a second current knowledge home.</div>
</div>
<figcaption><b>Figure 1.</b> Promotion moves knowledge to its subject; the producing evidence stays where it was made. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A document that mixes plans, findings and evidence becomes hard to trust: without a review, a reader cannot tell whether a sentence describes current behavior or an intention. The guide therefore reviews a mixed document section by section as work matures. It also guards against a quieter failure: assistant proposals remain proposals until explicitly accepted, and migration, silence or continued discussion does not make them accepted requirements.

[Figure 1](#fig-open-to-topic) follows content through its three owners. Notice the crossed-out way back: a closed record keeps supporting current knowledge through a link, but it does not become a second knowledge home.

Unfinished implementation, unresolved choices and prospective acceptance stay with the open owner; topic research notes may remain with their topic, and `OPEN.md` routes there. A completed source is retired only after its unique content and references are accounted for and the user approves the deletion.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A proposal promoted by silence</h3><p>An assistant suggests a naming rule in a plan. Nobody objects, so the next edit copies it into the topic as a requirement, and the plan keeps describing it as if it were still open.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Accepted, then moved and labelled</h3><p>The rule moves to the topic only after someone explicitly accepts it. The topic labels it as an accepted future specification until it is implemented, the plan keeps the remaining work, and the worklog records the landing.</p></div>
</div>

<!-- fold: dead-end Why readiness has one owner instead of several boards -->

Plans distinguish investigation readiness from implementation readiness. A workstream's execution owner carries order, prerequisites, status and resume instructions; implementation plans carry prospective acceptance; coverage maps obligations to evidence. The guide does not distribute this state among competing boards. Without one owner, two boards can disagree about what is ready, and neither can be trusted.

<!-- /fold -->

<!-- fold: experiment Evidence identity and frozen records -->

- Retain exact original bytes only for a specific citation, source pin or reproduction dependency.
- Preserve the necessary reference closure, original logical path, source revision, byte count and cryptographic hash in a location manifest. Record a per-document source revision when it differs from the collection default. The manifest indexes identity and location; it is not a second content home.
- Do not rewrite frozen links, add banners to originals or silently replace missing bytes. Current prose links to current knowledge or explicit evidence locations.
- If a project implements historical link resolution, it rebases only explicitly registered origins and records; current links and missing targets remain strict. A reading view distinguishes exact originals from mutable supporting current files. A symlink is not described as a frozen source or write protection.
- Restore an original only into an absent destination. Preserve a newer live file separately, and do not overwrite unrelated pending work.
- Source relocation, hash verification and a reading view establish document integrity. They do not establish runtime qualification or permission to execute old procedures.

<!-- /fold -->

<!-- fold: experiment Shelved investigations -->

Shelving is a scope decision recorded in the experiment guide and the owning topic. Inputs, code, failures and concrete recovery conditions are preserved there. Resumption requires a new explicit assignment. A hidden page may remain directly linkable with `hidden = true`; hiding neither deletes evidence nor qualifies a replacement.

<!-- /fold -->

Full guide: [from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge), [evidence identity and frozen records](documentation-system.html#evidence-identity-and-frozen-records) and [shelved investigations](documentation-system.html#shelved-investigations).

</section>

<section class="card" id="topics">

## A topic is one folder: always a record for agents, and a page when people need one

<p class="bs-lead">Each subject lives in <code>docs/topics/&lt;topic&gt;/</code>. Every topic has a record agents follow; a page explains it to people when they need one.</p>

<figure id="fig-topic-folder">
<div class="bs-folder" role="img" aria-label="The folder docs/topics/vehicle-model holds vehicle-model.md and tyre-fitting.md, records that agents follow; index.md, the page people read, which links to the records; and evidence, sources kept for a citation or reproduction.">
<div class="bs-folder-head"><code>docs/topics/vehicle-model/</code></div>
<div class="bs-folder-row bs-teal"><code>vehicle-model.md</code><span class="bs-badge">record</span><span><b>Agents follow it.</b> The exact spec: terms, limits, anchors other files point to.</span></div>
<div class="bs-folder-row bs-teal"><code>tyre-fitting.md</code><span class="bs-badge">record</span><span><b>More records</b> as the subject grows, each named for what it holds.</span></div>
<div class="bs-folder-row bs-violet"><code>index.md</code><span class="bs-badge">page</span><span><b>People read it.</b> The conclusion, a figure, why, the next decision; links the records.</span></div>
<div class="bs-folder-row bs-orange"><code>evidence/</code><span class="bs-badge">evidence</span><span><b>Kept for a reason:</b> sources for one citation or reproduction.</span></div>
</div>
<figcaption><b>Figure 2.</b> One topic folder and who reads each file. This diagram contains no measured results.</figcaption>
</figure>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Record and page</h3><p>Agents follow the spec and people need it explained: the record holds the exact text, the page the reasoning and figures.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">contract only</span><h3>Record, no page</h3><p>A schema, checklist or limit nobody needs walked through. Add a page later if someone does.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">declared exception</span><h3>Page, no record</h3><p>For cases the rules do not foresee yet, such as the kit's own pages that explain its guides. It says why in its frontmatter, <code>page_only = "…"</code>; without that, lint warns.</p></div>
</div>

The split follows how each reader uses the text. An agent is routed to an exact file and section and must find the same words there next time; a person wants the conclusion first, a figure and an example, and is better served when the page is rearranged for reading. Putting both in one file means layout HTML in the agent's way, or a spec that moves whenever the page is improved. The two therefore cover the same subject on purpose, and that overlap is not duplication to remove; what keeps them honest is that the record decides. A page may reorder, simplify and illustrate, but a rule, number or limit it shows must be in the record. So the record comes first; a topic without one is a rare, declared exception that the conformance check rereads on every upgrade.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>The spec inside a fold</h3><p>A topic has only <code>index.md</code>. Its tyre limits sit in a fold between two figures. An agent routed there reads card markup to find them, and a later layout change moves them.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Spec in the record, page links it</h3><p>The limits live in <code>vehicle-model.md</code> under their own heading. The page shows the figure, says why the limits are what they are and links that heading.</p></div>
</div>

Full guide: [canonical homes](documentation-system.html#canonical-homes) · [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown)

</section>

<section class="card" id="records-and-pages">

## Records keep the contract for agents; pages explain it to people

<p class="bs-lead">Agents read plain Markdown records through one router, and a rendered page exists only when a person has something to learn or act on.</p>

<figure id="fig-records-and-pages">
<div class="bs-flow" role="img" aria-label="AGENTS.md is the one thin router: it names the project context and prerequisites and routes the remaining rules by action to plain Markdown records. A rendered page explains current conclusions from those records and links to them instead of reproducing them. Reading a route grants no permission to execute or publish.">
<div class="bs-node bs-orange"><span class="bs-label">Router</span><b><code>AGENTS.md</code></b><ul><li>Names the project context and prerequisites</li><li>Rules every task needs</li><li>Remaining rules routed by action</li></ul></div>
<div class="bs-arrow"><span>by action</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Records for agents</span><b>Plain Markdown</b><ul><li>Headings, tables and lists</li><li>Exact file references and evidence links</li><li>Contracts, readiness and chronology</li></ul></div>
<div class="bs-arrow"><span>explain</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Page for people</span><b>Conclusions and decisions</b><ul><li>Current conclusions and accepted specifications</li><li>Demonstrated behavior with its evidence scope</li><li>Useful figures and the next decisions</li></ul></div>
<div class="bs-back"><span>×</span> A page links to records instead of reproducing them. Reading a route grants no permission to execute or publish.</div>
</div>
<figcaption><b>Figure 3.</b> Agents reach records through one router; people reach an explanation through pages that link back to the records. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Agents and people need different things from the same knowledge. An agent follows exact headings, file references and anchors; a person needs the conclusion, a figure and the next decision. Without this split, layout HTML gets in an agent's way and bookkeeping buries what a person came to learn. The guide therefore keeps contracts, handoff and resume state, readiness boards, bookkeeping and long run chronology in records, and pages link to those records instead of reproducing them.

[Figure 3](#fig-records-and-pages) shows the two reading paths. Notice that the page sits downstream of the records: it explains them but does not own them.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A topic page doubling as a work log</h3><p>Below its conclusion, the rendered topic page holds a readiness board, a handoff checklist and a dated diary of every run.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Conclusion on the page, state in records</h3><p>The page states the current conclusion, shows a figure with its evidence scope and names the next decision. The readiness board, handoff state and run chronology stay in records that the page links to.</p></div>
</div>

<!-- fold: code Record format and registered source pages -->

- Every topic has a record, `docs/topics/<topic>/<topic>.md`; split a growing record into descriptively named files. Subject records are not named `README.md`. Add `index.md` when a person has something to learn or act on. A page without a record declares `page_only = "<reason>"` in its frontmatter, or lint warns.
- Records use plain Markdown headings, tables, lists, exact file references and evidence links. Layout HTML stays out of agent records; a needed diagram is stored in a separate file and linked. Anchors that other documents reference are preserved.
- A site may render a whole record as a [registered source page](authoring.html#registered-source-pages). The Markdown file stays the record and its only editable copy; the page adds no content of its own. The guides linked from this page are rendered that way.

<!-- /fold -->

<!-- fold: code Agent entrypoints: import versus point -->

- Keep one thin repository router in `AGENTS.md`. Name the project context and prerequisites there. Read the orientation and the rules that apply to every task at the start of work, unless they are already loaded.
- Route the remaining rules by action. For each trigger, name the required files or sections and say when to read them. Apply every matching route before its action, and recheck the routes when the task expands. Find task-specific plans, topics and evidence through named links in the project context or the applicable rule.
- Codex uses the named paths and triggers in `AGENTS.md`. Claude Code uses a bare, standalone `@AGENTS.md` import in `CLAUDE.md`, so both clients use the same router. Import paths are relative to the importing file; keep the import chain short. Backticks and fences make an import literal.
- Submodule consumers must initialize `.docs-kit` before relying on its rules. If a required policy is missing, report it and resolve the prerequisite before proceeding with the work it governs.

<!-- /fold -->

<!-- fold: dead-end When a page drifts toward agents -->

When a page becomes predominantly agent-facing, its agent material moves into records and its human-facing core stays in a page. Removing the page from navigation or publication follows the deletion gate. A hidden stub and the former anchors are preserved while dated or frozen links still depend on them.

<!-- /fold -->

Full guide: [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown) and [agent entrypoints](documentation-system.html#agent-entrypoints-import-versus-point).

</section>

<section class="card" id="page-and-record-in-step">

## A page explains its record in its own words; a changed record names the pages to reread

<p class="bs-lead">Pages are written for people and do not copy the record's wording. When a record section changes, lint notes the pages that link to it so someone rereads them.</p>

<figure id="fig-page-and-record">
<div class="bs-flow" role="img" aria-label="A section of a record is edited, for example Refactoring over compatibility in rules/engineering/code.md. Lint compares the record with the last commit and finds which sections changed. It then lists every page that links to a changed section, for example the Compatibility chapter on the Engineering page, as pages to reread.">
<div class="bs-node bs-teal"><span class="bs-label">1 · Edit</span><b>A record section changes</b><ul><li><code>rules/engineering/code.md</code></li><li>section: Refactoring over compatibility</li></ul></div>
<div class="bs-arrow"><span>lint</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Compare</span><b>Changed sections</b><ul><li>diff against the last commit</li><li>each changed line belongs to a heading</li></ul></div>
<div class="bs-arrow"><span>links</span></div>
<div class="bs-node bs-orange"><span class="bs-label">3 · Remind</span><b>Pages to reread</b><ul><li>every page linking that heading</li><li>a note, never a failure</li></ul></div>
</div>
<figcaption><b>Figure 4.</b> How a record change reaches the pages that explain it. This diagram contains no measured results.</figcaption>
</figure>

An explanation for people is not the record in nicer type: it leads with the outcome, reorders, simplifies and adds an example. So a page cannot quote its record without getting worse, and two texts about one rule will drift unless something connects them. The connection already exists: every explanation links the record section it explains. Lint follows those links backwards from the sections a change touched. A link to a whole guide, as in a routes table, is noted only when the guide's opening text changes, so a routine edit names the few chapters that explain it.

```text
NOTE: rules/engineering/code.md › Refactoring over compatibility changed.
      Pages that explain it — reread them:
        docs/topics/engineering-practices/index.md  (chapter: compatibility)
```

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>The rule moves, the page stays</h3><p>A rule gains an exception. The record is updated; the page that explains the rule still states it without the exception, and nothing points at it.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>The change names its pages</h3><p>The same edit makes lint list the one chapter that explains the rule. The author rereads it, adds the exception in the page's own words and commits both.</p></div>
</div>

Full guide: [rules for changes and chronology](documentation-system.html#rules-for-changes-and-chronology)

</section>

<section class="card" id="changes-and-publishing">

## Every change passes its gate, lands whole and leaves an append-only trace

<p class="bs-lead">Deletion needs user approval, a requested review stops before adoption, the worklog records each landing and only the chosen branch publishes.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">delete</span><h3>Approval first</h3><p>Nothing is deleted without user approval. Propose a removal with the concrete material identified.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">review</span><h3>Present and stop</h3><p>A requested review or prototype is presented; work stops before adopting, committing or publishing it.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">commit</span><h3>One deliverable</h3><p>Code, owning documentation, tests and worklog land in the same logical deliverable commit. Generated output stays ignored.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">worklog</span><h3>Append-only, newest first</h3><p>Each landing records what changed, why, the measured effect with units when applicable, checks and commit identity.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">publish</span><h3>Chosen branch only</h3><p>Builds on feature branches must not publish production documentation. Publishing requires the project's chosen branch or environment, authorization and successful checks.</p></div>
</div>

Documentation loses information in quiet ways: a deleted figure, a rewritten log entry, a preview build that reaches production. The guide puts a gate before each. Nothing is deleted without user approval, whether documents, figures or content lines, and a removal is proposed with the concrete material identified. A requested review or prototype is a gate: present it and stop before adopting, committing or publishing.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A rewritten, vague log</h3><p>An older worklog entry is edited to add the commit hash it lacked, and today's entry says only "docs cleanup".</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A complete landing entry</h3><p>The new entry sits at the top. It says what changed (a rule moved from its plan to its topic), why (it was accepted), that no measured effect applies, which checks ran, and the commit identity. A pending entry may say that its landing commit assigns the hash.</p></div>
</div>

<!-- fold: code Worklog entries and probe lines -->

The worklog is append-only and newest-first. A pending entry may say the hash is assigned by its landing commit; resolve it through version history rather than rewriting dated entries.

A probe is recorded in one line:

```text
probed <subject> → <verdict>, <decisive reason>, <time spent>
```

Detailed probe artifacts follow the [experiment retention rules](evidence.html#numbers-and-staleness).

<!-- /fold -->

<!-- fold: code Drafts kept below the page end -->

A page may keep topic-owned drafts below a <code>&lt;!-- page-end --&gt;</code> marker; only the content above it is rendered. Chronology still belongs in the worklog, and owed work still needs an `OPEN.md` route to its owner. Unreachable notes tails are not left behind.

<!-- /fold -->

<!-- fold: dead-end Why there is no archive staging layer -->

Approved superseded sources are removed in the landing commit; the guide adds no archive staging layer. Exact evidence is preserved only when its identity has a concrete purpose. Current invariants live in owning records and cross-cutting conventions, and source markers such as `INVARIANT` and `DON'T-REDO` must not leak as internal labels onto rendered pages.

<!-- /fold -->

<!-- fold: experiment Local review, browser approval and publishing -->

- Use the pinned kit from the consuming project root, follow the concrete commands in the project's context and the shared [validation guide](validation.html#validation-and-review), and complete the linked validation before review. Share the rendered page with its figures first, then source or evidence links where useful.
- Serve only generated output on loopback for local browser review. Confirm the listener's owner and served checkout before reusing it. Do not expose the repository root or stop another session's server. Stop owned temporary servers after review unless they are retained for the user's preview.
- Browser approval remains scoped to the supported origin. If access is rejected on policy grounds, preserve the rejection and resolve the permission with the owner; do not change transport, browser or control API to bypass the block. A manual file URL is not evidence that an agent inspected the rendering.
- Hosting source changes are a separate explicit operation; a source build does not imply a deployed version. Rollback must preserve unrelated work and rebuild and verify the chosen revision.

<!-- /fold -->

Full guide: [rules for changes and chronology](documentation-system.html#rules-for-changes-and-chronology) and [review, build and publishing](documentation-system.html#review-build-and-publishing).

</section>

<section class="card" id="page-design">

## Each section has one purpose and states its takeaway before the evidence

<p class="bs-lead">Titles state the takeaway, a one-sentence lead states the claim, and the evidence follows.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">section</span><h3>One purpose</h3><p>Answer a question, show a construction or compare alternatives. Split when the purpose changes; merge thin sections into their concept.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">heading</span><h3>Takeaway titles</h3><p>Titles state the takeaway and a <code>bs-lead</code> states the claim. A reader's question becomes a heading, answered directly before the evidence.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">figure</span><h3>Mechanism first</h3><p>The figure follows the heading or a one-sentence takeaway, then the prose that interprets it. A table or equation may lead when it carries the explanation.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">width</span><h3>Use the width</h3><p>Text, figures and tables share a left edge. Avoid narrow centered columns and half-empty rows. Expressive details respect reduced motion and accessibility.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">navigation</span><h3>Prerequisite order</h3><p>Navigation follows prerequisite order, and important comparisons have direct entries. No page-wide audience tabs; local method, scenario and diagram-mode tabs are useful.</p></div>
</div>

A heading that only names a topic, such as "Results", makes the reader search the section for its conclusion, and a section with two purposes buries both. The guide gives each section one coherent purpose: answering a question, showing a construction or comparing alternatives. It splits a section when the purpose changes and merges thin sections into their concept; cards, tiles, tabs and callouts mark distinct roles, without arbitrary word limits or one-screen constraints. Internal registry tags, bug-hunt narratives, file-routing tables and debugging chronology stay off rendered surfaces, so the page keeps a formal, plain human voice.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Results</h3><p>The section opens with setup, walks through each measurement and states in its last sentence which option was kept and why.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Option B is kept because it needs one fewer manual step</h3><p>A one-sentence lead states the claim, the comparison figure follows, and the prose below explains what the figure shows and where the claim stops.</p></div>
</div>

<!-- fold: dead-end Why homepages are not one shared template -->

Each project chooses its homepage composition, information hierarchy, sections, hero treatment and visual story. Using the shared kit does not require matching homepages: a research narrative, an engineering reference and a navigation dashboard can use different arrangements. Shared visual components are optional building blocks, and sharing one does not transfer ownership of the surrounding page. Project illustrations, scientific figures, domain widgets and distinctive compositions stay local; the starter homepage is an example, not a required template.

Navigation is shared, not owned by one page. A homepage that lists its own sections instead of the shared site tree makes every move to a reader feel like a different site. Keep the same tree on every page and let the homepage present the pages through cards or its own composition.

<!-- /fold -->

Full guide: [page design](page-design.html#page-design) and [project-owned homepages](page-design.html#project-owned-homepages).

</section>

<section class="card" id="build-sheets">

## Build-sheet blocks keep one meaning, and status never replaces evidence

<p class="bs-lead">Every chapter carries its claim and a meaningful visual; a status board and a slide face point to evidence and never substitute for it.</p>

<div class="bs-board">
<div class="bs-row"><span class="bs-state bs-ok">Done</span><b>Work is finished</b><span>Status does not substitute for evidence; scope caveats stay beside their evidence.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Decided</span><b>A choice is made</b><span>Decided is not implemented.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Passed</span><b>A check passed</b><span>A local or CPU test is not a native runtime check.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Work remains</b><span>The Open row owns the remaining work; limits prose does not repeat it.</span></div>
<div class="bs-row"><span class="bs-state bs-off">Parked</span><b>Set aside</b><span>A Parked row includes its reopening condition.</span></div>
</div>

Shared blocks help readers only if each block means the same thing on every page. A row reading "Decided" can be mistaken for shipped work, and a number shown only on a slide has no evidence behind it. The guide closes both gaps: status does not substitute for evidence, Decided is not implemented, a local or CPU test is not a native runtime check, and no fact exists only on a slide.

The board below illustrates what each of the five states means; it reports no project's status. One `bs-board` holds a page's current status.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A slide that owns a fact</h3><p>The slide is titled "Performance". It shows a headline number that appears nowhere in the chapter below, and the caveat that limits it appears only in the chapter.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A slide that is a view</h3><p>The title states the finding as a sentence, the visual reuses the chapter's own figure, and a scope line says what the numbers cover and what remains unmeasured. Every number is restated with its evidence in the chapter and updated in the same edit.</p></div>
</div>

<!-- fold: code Block vocabulary and filling rows -->

Opt in with `page_css = ["build-sheet.css"]` and keep page-specific extras in a separate local stylesheet. Cards keep the reader stage height. Each chapter carries its claim and a meaningful visual block: figure, flow, table or tiles. At 1600 × 1000 a chapter should fill about half a card; merge a thin chapter rather than padding it.

| Block | Purpose |
|---|---|
| `bs-lead` | One-sentence chapter claim |
| `bs-specs`, `bs-stats` | Labelled key values; two to four headline measurements with units and scope |
| `bs-chips` | Short option tags; rejected options retain their reason |
| `bs-grid g1` through `g4`, `bs-part` | Visual or parallel-content rows; contrasting parallel lists |
| `bs-checks`, `bs-check`, `bs-badge` | Checkable parallel claims with explicit state |
| `bs-board`, `bs-row`, `bs-state` | Single current-status board |
| `bs-flow`, `bs-node`, `bs-arrow`, `bs-back`, `bs-stack` | One-way mechanism with labelled arrows and explicit prohibited feedback |
| `bs-orange` through `bs-muted` | Shared semantic tones, never meaning by color alone |

Main media uses full width (`bs-grid g1`); photos and renders use at most two per row; paired animations sit together. Fill every row: two, three or four items; five as three over two (`bs-checks r32`); six as three by two; seven as four over three; eight as four by two. Reflow for narrow columns. Keep flow arrow labels near 12 characters and box titles near 30, with full mappings in the topic record.

<!-- /fold -->

<!-- fold: code Slide face details -->

- A chapter may open with one 16:9 slide face that states its takeaway with one visual. The full chapter follows and remains the complete, end-to-end readable source.
- The eyebrow names the subject without a chapter number. The visual comes from the shared slide vocabulary or a project-local diagram and reuses the chapter's own figure assets.
- Caveats that change a claim's meaning belong on the slide, not only in the chapter. The slide is the one sanctioned repetition of a fact: a view of the chapter, never its owner.
- A face that does not fit 16:9 has too much content; move detail into the chapter instead of shrinking type. Below 720 px the face stacks into a readable column.
- Slide figures are views of numbered chapter figures and carry a short caption without a new number.
- Each tone keeps one meaning across a project's slides: accent and warm tones identify the compared methods, `is-alert` marks failures and warnings, `is-held` marks held-out, hidden or pending items, and everything else stays neutral.

<!-- /fold -->

<!-- fold: experiment Completion and review -->

Follow the requested review arrangement: a separate prototype or an uncommitted in-place trial. Preserve content, evidence, media identities and public anchors during layout work. Follow the [documentation review gate](documentation-system.html#rules-for-changes-and-chronology) and complete [site validation](validation.html#validation-and-review), including the project-required checks. A decision page ends with a criteria-based options table and a clear verdict.

<!-- /fold -->

Full guide: [build-sheet pages](page-design.html#build-sheet-pages), [slide faces](page-design.html#slide-faces) and [completion and review](page-design.html#completion-and-review).

</section>

<section class="card" id="explanations">

## Keep one visible story in order of understanding, with optional depth in typed folds

<p class="bs-lead">A reader can follow the complete argument and its verdict with every fold closed.</p>

<figure id="fig-story">
<div class="bs-flow n2" role="img" aria-label="The visible Story holds the complete argument in order of understanding: purpose and prerequisites, ingredients and mechanism, examples, evidence and limits, comparison cases and verdict. Typed folds for math, experiment, code and dead-end add optional depth. Folds never hide a separate required argument.">
<div class="bs-node bs-teal"><span class="bs-label">Always visible</span><b>The Story</b><ul><li>Purpose and prerequisites</li><li>Ingredients and mechanism</li><li>Examples, evidence and limits</li><li>Comparison cases and verdict</li></ul></div>
<div class="bs-arrow"><span>go deeper</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Optional</span><b>Typed folds</b><ul><li><code>math</code> derivations</li><li><code>experiment</code> detail</li><li><code>code</code> excerpts</li><li><code>dead-end</code>, shown as Alternatives</li></ul></div>
<div class="bs-back"><span>×</span> A fold never hides a separate required argument.</div>
</div>
<figcaption><b>Figure 5.</b> Optional depth branches from a complete visible argument. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

An explanation fails when the reader meets a number before the instrument that produced it, or a term before its definition. It also fails when the decisive step hides in an optional section that many readers never open. The guide orders by understanding: purpose, prerequisites, ingredients, mechanism, examples, evidence and limits. The complete argument, narrative figures, comparison cases and verdict must remain intelligible with every fold closed.

[Figure 5](#fig-story) shows the two reading layers. Notice that the arrow goes one way: folds deepen the Story but do not hide a separate required argument.

Each concept or formula is explained in one canonical place and linked elsewhere. A brief result label or scope condition stays beside the evidence whenever it affects how the reader should interpret that evidence.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>The argument in a fold</h3><p>The page opens with a table of results. The definition of the measured quantity and the reason one option lost sit in a fold titled "Details".</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Story first, depth below</h3><p>The page states the purpose, defines the quantity, explains the mechanism, then shows the results with their scope. An Alternatives fold keeps the rejected option's lesson, with its verdict up front.</p></div>
</div>

<!-- fold: code Fold syntax and choosing a layer -->

In source, a fold opens with a line such as `<!-- fold: math Derivation of the bound -->` and closes with `<!-- /fold -->`. The types are `math`, `experiment`, `code` and `dead-end`, displayed as Alternatives. A fold title is already its heading; do not repeat it inside.

Choose by narrative weight, not element type: a table or equation may carry the Story, and a plot may be supporting detail. Default to visible figures and folded reference density. Keep competing formulations together, with assumptions and verdict explicit. Add a new layer only for recurring content. The [reader tour](build-a-site.html#the-reader) shows how folds behave on a page.

<!-- /fold -->

<!-- fold: dead-end Moving detail into a record without breaking links -->

When detail moves into a record, the former page anchor stays on the summary that replaces it, and the summary links to the matching record anchor. Deep-link anchors are preserved when consolidating, and an essential repeated equation needs a back-reference. Concise lessons from rejected methods stay reachable with their verdict up front; detailed captures and reproduction remain evidence.

<!-- /fold -->

Full guide: [story and reading layers](explanations.html#story-and-reading-layers).

</section>

<section class="card" id="honest-claims">

## Name each object once, and claim only what the evidence shows

<p class="bs-lead">Use one term per object on every surface, and label each claim by the kind of evidence behind it.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-off">future</span><h3>Accepted future behavior</h3><p>Accepted but labelled apart from what is implemented.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">implemented</span><h3>Implemented behavior</h3><p>Labelled apart from accepted future behavior and from runtime observations.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">local</span><h3>CPU checks</h3><p>A local check proves only its tested property.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">runtime</span><h3>Native or runtime observations</h3><p>Labelled apart from CPU checks; a local test is not a native runtime check.</p></div>
</div>

Two names for one object make a reader wonder whether there are two objects. A claim that outruns its evidence is worse: a smoother drawing can be read as proof of accuracy, and an estimate typed into an empty cell looks like a measurement. The guide therefore uses one term per object across prose, controls, legends, tables, figures and output, and separates claims that require different evidence: visual fidelity, smoothness, input preservation, correspondence with a source and physical accuracy. A local check or smoother drawing proves only its tested property.

The four labels below mark claims that the guide keeps apart.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An overclaim</h3><p>"The new interpolation is accurate." The only check was that the plotted curve looks smoother, and an empty error column was filled with an estimate.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A scoped claim</h3><p>"The plotted curve is smoother (visual check). Correspondence with the source: not measured." Where a supported bound exists, it is given with its source.</p></div>
</div>

<!-- fold: dead-end Decision rationale and baselines -->

Decision rationale belongs beside the decision, including why an instrument or default was chosen and why the alternatives lost. A baseline cited for current shipped behavior measures what ships; retired baselines are labelled historical. An experimental verdict and deployment measurements are distinct content kinds.

<!-- /fold -->

<!-- fold: code Naming mechanisms, functions and renames -->

Name a mechanism the reader sees; use formulation internals only when explaining that formulation. A rename sweeps all surfaces. State what a function receives, returns and optimizes or interpolates, and which inputs vary or stay fixed.

<!-- /fold -->

Full guide: [naming and honest claims](explanations.html#naming-and-honest-claims).

</section>

<section class="card" id="evidence">

## A measured number is current only with its full provenance

<p class="bs-lead">Quote a number as current evidence only when its source and conditions are recorded and still hold.</p>

<div class="bs-specs"><div><span class="bs-label">Source</span><b>Commit + command</b></div><div><span class="bs-label">Conditions</span><b>Runtime + workload</b></div><div><span class="bs-label">Reading</span><b>Units + baseline</b></div><div><span class="bs-label">Reach</span><b>Method + scope</b></div></div>

A number without its conditions cannot be checked, and a number whose inputs have changed can look authoritative while no longer being true. The guide therefore requires full provenance for any current measured claim, and a rerun before quoting it as current when code, input data, method, workload or runtime conditions affecting it change. A historical label does not qualify changed inputs. Configuration values, derivations and design arithmetic are not measurements: they cite their source and are labelled accordingly.

A current measured claim records the eight items below and links its raw result and limitations.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A number without provenance</h3><p>"The new layout loads much faster." No commit, command, workload or baseline is given, and the input data changed after the run.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A number with provenance</h3><p>The claim names its source commit, exact command, runtime and workload, units, baseline, method and scope, and links the raw result and its limitations. After the input data changed, it was rerun before being quoted as current.</p></div>
</div>

<!-- fold: experiment Number ledgers for redesigns -->

When a redesign restates numbers in new prose, figures or slides, record each number's source in a ledger and lock the evidence blocks kept verbatim. Each project keeps its own ledger format and the checks for both. A slide face may show only numbers that its chapter also shows. Every distinct number a redesigned chapter shows, figure labels included, has a ledger source. Presentation-only edits may reuse captured results only after checking that identities, numbers and treatments remain intact.

<!-- /fold -->

<!-- fold: experiment What stays with the producing work -->

Protocols, outputs, snapshots, failed attempts, changed settings, actual outcomes, reviews actually performed and relevant uncertainty stay with the work that produced them. Experiments also retain producing code, inputs, full result tables, source pins and any independent reviews performed in the experiment directory. The page explains what they establish; the worklog records the landing and hashes without duplicating tables. Retained measured content remains subject to the deletion gate.

When a claim is rerun, the old record keeps its date, runtime, inputs and scope. Historical records preserve their original source pins, inputs, runtime, settings, resource limits, deadlines and verdicts where those fields apply.

<!-- /fold -->

<!-- fold: experiment Run visuals and live experiment reports -->

- Prefer scripted captures with the same provenance as other figures. An inherently interactive screenshot states commit, date and scenario or preset; it illustrates appearance, never a quantitative claim.
- Derive overlays from recorded artifacts rather than screenshots when data exists. Show dynamic behavior through an intentionally packaged short clip or useful frame sequence, with normal captions and provenance.
- A live public experiment report uses `ongoing = true`, removed only when findings and limits are settled. The owning topic explains scope and links to evidence.
- Suitable experiment visuals include actual-geometry quality overlays, convergence, reference parity, timing or scaling and trade-off plots; inapplicable views are omitted explicitly. Topic, worklog and open routing are updated in the same deliverable.
- The [experiment workflow](experiment-workflow.html) owns experiment kinds, baselines, stopping conditions and the required content of every experiment, including its verdict.

<!-- /fold -->

Full guide: [numbers and staleness](evidence.html#numbers-and-staleness) and [run visuals and experiment lifecycle](evidence.html#run-visuals-and-experiment-lifecycle).

</section>

<section class="card" id="figures">

## Every mechanism, spatial claim and measurement needs a visual

<p class="bs-lead">A section is not done until a mechanism has a diagram, a spatial claim a picture and a measured claim a plot or table.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">anchor</span><h3>Number and caption</h3><p>A stable HTML anchor and a visible numbered caption, unique and in reading order.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">prose</span><h3>Prose reference</h3><p>Text links the number to the anchor and says what to notice and why it supports the claim. A caption or alt text alone is not enough.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">links</span><h3>Clickable references</h3><p>Every reference is a link, including in table cells, panel labels and other captions.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">source</span><h3>Provenance and alt text</h3><p>Name the source and give useful alternative text. Generated figures record generator, source revision, inputs, date and output hash.</p></div>
</div>

Prose alone leaves each reader to build the picture in their head, and different readers build different pictures. The guide treats visuals as a completion gate: budget visual production before declaring a section done, so that figures, tables and headings alone convey the story. It also rules out the opposite failure: a visual must answer an actual understanding or evidence need, so no decorative plot is added because a formula exists. Diagrams show structure, ownership, flow or sequence; tables give exact lookup; plots show patterns, variation or trade-offs. Pair formats when they answer different questions.

Every included figure carries the four items below.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An orphan figure</h3><p>A diagram sits under the text with the caption "Architecture". It has no number, anchor or source, and the text says only "see below".</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A referenced figure</h3><p>The text says "Figure N shows the request path; notice that a retry returns to the queue, not to the caller", with Figure N linked to its anchor. The numbered caption names its source and states that the diagram is illustrative.</p></div>
</div>

<!-- fold: experiment Designing comparisons -->

- Design comparisons together: matched orientation, scale, framing and input cases; persistent zoom across switching; an overview locating a detail; consistent markers and colors across profiles and tables.
- Method names in controls and legends carry identity independently of color. Offer every option named in the comparison, grouped by method with roles such as current, selected, previous or rejected.
- An interactive comparison replaces its redundant static gallery while retaining a useful loading or fallback image.
- Draw the finding directly rather than making the eye compute it. Show the actual sample locations and construction; distinguish measurements, solved points, continuous geometry and its rendering polygon.
- For independent changes, show the baseline, each change alone and their combination across relevant scenarios, with a neighboring ablation table and metric definitions. Explain a zero effect honestly.

<!-- /fold -->

<!-- fold: code Chart sizing, interaction and access -->

- Charts fit their actual column with labels at least 11 px. Keep bar labels short or move them into a legend. Crop empty margins; avoid baked title bars, badges and debugging chronology. Use one camera or view across a series.
- Do not shrink an important comparison to fit a screen at the cost of legibility. Bound overview height and retain full-size inspection.
- Interactive views load independently, confine drag, scroll and keys to their region and never steal page focus. Linked views follow the same selected state. Data comes from the exact run inputs and outputs, checked by hash; a static main render shows while loading.
- SVG toggles and their zoomed or lightbox controls stay synchronized. Carousel autoplay stops on engagement and pauses while a lightbox is open.
- Use shared components rather than duplicating handlers. Keep controls visible, labelled, keyboard accessible and at least 44 px touch targets. Give scrollable tables and equations labelled local regions. Nothing may overflow the page at any viewport.

<!-- /fold -->

<!-- fold: code Numbering, unnumbered images and generated figures -->

Use page-wide numbers or a named sequence such as P1; numbers are unique and follow reading order within a sequence. A plot, diagram, flow, interactive comparison or evidence capture is a figure. An appearance-only image gets a short caption without a number. A deliberate unreferenced figure needs an adjacent source comment:

```html
<!-- unreferenced figure: reason -->
```

Generated figures name their generator, source revision, inputs, date and output hash in a manifest or metadata, for SVG, PNG and interactive data alike. Use the project's shared dark-compatible figure style, never ad hoc per-figure styles, and keep an explicit figure-to-generator manifest checked for missing or orphaned resources. Source-authored HTML flows, like the figures on this page, count as local diagrams: their page source is the generator, and their layout passes the same collision and overflow review.

<!-- /fold -->

Full guide: [figures and comparisons](figures.html#figures-and-comparisons) and [interaction and access](figures.html#interaction-and-access).

</section>

<section class="card" id="mathematics">

## Derive mathematics from a construction the reader already has

<p class="bs-lead">Define every symbol before use, show the intermediate steps and tie the equation back to the Story's picture.</p>

<figure id="fig-math">
<div class="bs-flow" role="img" aria-label="Math reuses the Story's geometry, orientation, colors and example inputs. Variables, vectors, constraints and error terms are marked where they act, identifying inputs, geometry-derived values and solved quantities. From those marks the explanation walks to the equation and a worked numerical example. A disconnected formula plot or a duplicate picture without useful annotations is not added.">
<div class="bs-node bs-teal"><span class="bs-label">From the Story</span><b>The same picture</b><ul><li>Same geometry and orientation</li><li>Same colors</li><li>Same example inputs</li></ul></div>
<div class="bs-arrow"><span>mark</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Marked where they act</span><b>Named quantities</b><ul><li>Variables, vectors and constraints</li><li>Error terms</li><li>Inputs, geometry-derived values, solved quantities</li></ul></div>
<div class="bs-arrow"><span>derive</span></div>
<div class="bs-node bs-blue"><span class="bs-label">Result</span><b>Equation and example</b><ul><li>Intermediate steps</li><li>Worked numerical example</li></ul></div>
<div class="bs-back"><span>×</span> No disconnected formula plot or duplicate picture without useful annotations.</div>
</div>
<figcaption><b>Figure 6.</b> The Math layer walks from marks on the Story's picture to the equation and a worked example. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A formula that arrives with undefined symbols asks the reader to trust it rather than follow it, and a formula plot disconnected from the Story adds a second picture to decode. The guide builds from the reader's known construction. Define symbols, units, mathematical terms and prerequisites before use. Show intermediate reasoning, including product and chain rules when relevant. State structural assumptions and distinguish local conditions from global validity. A non-obvious formula needs a derivation or a precise companion-section citation.

[Figure 6](#fig-math) shows how the Math layer reuses the Story. Notice that the equation is reached through marks on the same picture, not drawn from a separate one.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A formula dropped in</h3><p>An equation appears with symbols the page never defined, followed by a plot of the formula over a range the Story never mentions.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A formula built from the picture</h3><p>The Story's diagram marks each input and the solved quantity. The math fold defines each symbol with its unit, shows the chain-rule step, states where the result holds and works the equation with the Story's example inputs.</p></div>
</div>

<!-- fold: code KaTeX syntax and rendering -->

With `math = true` in the page frontmatter, write mathematics with these delimiters:

```text
In Markdown:      $…$   inline     $$…$$   display
Inside raw HTML:  \(…\)
```

Math uses bundled KaTeX without a CDN. Wrap long expressions or provide contained scrolling; never make type unreadably small. Inspect rendered raw-HTML formulas too.

<!-- /fold -->

<!-- fold: experiment Verifying analytic claims -->

Analytic derivative and Jacobian claims name their numerical verification tolerance and executable self-test. A non-obvious formula needs a derivation or a precise companion-section citation.

<!-- /fold -->

Full guide: [mathematical explanation](math.html#mathematical-explanation).

</section>

<section class="card" id="code-excerpts">

## Excerpt only real code, and draw code diagrams with shared meanings

<p class="bs-lead">A snippet shows real repository lines with source metadata that drift checks can verify; a diagram's boxes, edges and dashes mean the same on every page.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">excerpt</span><h3>Real lines</h3><p>Usually a signature and 3–10 decisive lines; link the rest. Concise design rationale sits beside the code.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">source</span><h3>Verifiable metadata</h3><p>Source metadata such as <code>python source=src/example.py#L42-L49</code> lets drift checks verify content and real line numbers.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">boxes</span><h3>Named components</h3><p>In diagrams, boxes denote named components and edges explicitly mean ownership, calls or data flow.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">dashes</span><h3>Optional paths</h3><p>Dashed lines mean a documented optional path. Include a legend and name the data source in the caption.</p></div>
</div>

Code on a page can go stale silently: the file changes and the excerpt does not. Idealized pseudocode presented as an excerpt is worse, because it looks verified. The guide uses a snippet only when it explains a seam or difficult contract better than prose, excerpts real repository code and attaches source metadata so drift checks can verify content and real line numbers. Diagrams come from data or explicit local source and include overflow and collision checks or rendered QA.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An unverifiable snippet</h3><p>A tidy function is shown as if copied from a source file, but it was rewritten for the page, carries no source metadata and no longer matches the file.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A verified excerpt</h3><p>The code fence names its source range, the shown lines are copied from that range, and a link leads to the rest of the file. A sentence beside it explains the design choice.</p></div>
</div>

<!-- fold: code Rendering chrome and diagram patterns -->

Render excerpts with distinct type, class and function colors, a copy button, a source chip, a language badge and a line-number gutter showing actual source lines. Reuse shared code chrome and keep every control accessible. Numbered sequence steps, common-data mode views and quantitative generated SVGs are useful diagram patterns.

<!-- /fold -->

<!-- fold: dead-end Interactive diagram controls not yet built -->

Reuse supported pan, fullscreen and annotation controls where relevant. Do not claim planned edge highlighting, drill-down or semantic zoom as implemented. If one is added, choose drill-down for independent child diagrams with a breadcrumb, or semantic zoom when the surrounding context must remain visible.

<!-- /fold -->

Full guide: [code and diagrams](code-excerpts.html#code-and-diagrams).

</section>
