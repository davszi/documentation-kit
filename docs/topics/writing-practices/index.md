+++
title = "Documentation and writing"
brand_sub = "homes · records · pages · figures"
description = "Where each kind of documentation belongs, why the record is written before any page, what a record must say, and how the page guides shape explanations, figures, math and code, with illustrative examples."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Guide per task", "#routes"], ["One home", "#homes"], ["Record first", "#record-first"], ["Open to topic", "#open-to-topic"], ["Topics", "#topics"], ["Records and pages", "#records-and-pages"], ["In step", "#page-and-record-in-step"], ["Changes and publishing", "#changes-and-publishing"], ["Honest claims", "#honest-claims"], ["Evidence", "#evidence"], ["Section design", "#page-design"], ["Build sheets", "#build-sheets"], ["Story and folds", "#explanations"], ["Figures", "#figures"], ["Mathematics", "#mathematics"], ["Code excerpts", "#code-excerpts"]]
page_only = "Explains the documentation and writing guides; they are the records, in rules/."
+++

# Documentation and writing

<section class="card" id="routes">

## Each guide owns one kind of documentation decision

<p class="bs-lead">The documentation system decides where content lives and in what order it is written; writing records decides what a record says; five page guides decide how a page for people presents it.</p>

<div class="bs-grid g3">
<div class="bs-part bs-teal"><span class="bs-label">Where and when · documentation system</span><h3>Homes and order of work</h3><ul>
<li>each fact is written once, in its home</li>
<li>the record comes first; a new page only when someone asks</li>
<li>how documents move, change and retire</li>
<li>the <code>AGENTS.md</code> router</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">What a record says · writing records</span><h3>Records for agents</h3><ul>
<li>one record per topic, in plain Markdown</li>
<li>one name per object; claims scoped to their evidence</li>
<li>measured numbers with their full provenance</li>
<li>frozen evidence and shelved work</li>
<li>claim rules for excerpts, formulas and figures</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">How a page presents it · page guides</span><h3>Pages for people</h3><ul>
<li>section design and build-sheet blocks</li>
<li>one visible story, depth in folds</li>
<li>figures, mathematics and code excerpts</li>
<li>layout and presentation, for whoever writes the page</li>
</ul></div>
</div>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Documentation and writing guides by task">

| Before… | Read… | It covers | Explained here |
|---|---|---|---|
| Creating, moving, splitting or retiring a document | [Documentation system](documentation-system.html) | Canonical homes, the order of work, the path from open work to topic, records and pages, agent entrypoints, changes and the worklog | [One home](#homes), [Record first](#record-first), [Open to topic](#open-to-topic), [Records and pages](#records-and-pages), [Changes and publishing](#changes-and-publishing) |
| Upgrading the kit pin or taking over a repository | [Project conformance check](conformance.html) | Pin, router, copied rules, homes, topics, pages and records, open work, compatibility, changed rules, site | [Topics](#topics), [In step](#page-and-record-in-step) |
| Writing or changing a record: a guide, topic record, plan, worklog or open-work entry | [Writing records](records.html), plus the [documentation system](documentation-system.html#record-first-page-on-request) from Record first through the change rules | One record per topic, format, naming and honest claims, measured numbers, excerpts, formulas and figures, frozen evidence, shelved investigations | [Topics](#topics), [Records and pages](#records-and-pages), [Honest claims](#honest-claims), [Evidence](#evidence) |
| Making a new page for people, once a person asked for one, or page work on an existing page beyond a small sync | [Record first, page on request](documentation-system.html#record-first-page-on-request) and [rendered pages are for people](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown), then the applicable page guides below and the [site guides](maintenance.html) | When page work starts, who does it, from which brief, and who checks it | [Record first](#record-first), [Records and pages](#records-and-pages), [In step](#page-and-record-in-step) |
| Laying out a rendered page | [Page design](page-design.html) | Section purpose, takeaway titles, homepages, build-sheet blocks, status boards, slide faces, review | [Section design](#page-design), [Build sheets](#build-sheets) |
| Writing an explanation on a page | [Explanations](explanations.html) | Story order, typed folds, moving detail into a record | [Story and folds](#explanations) |
| Adding a figure or comparison | [Figures](figures.html) | The visual completion gate, captions and references, comparisons, chart sizing, interaction and access, run visuals and live experiment reports | [Figures](#figures) |
| Writing mathematics | [Math](math.html) | Definitions, derivations, KaTeX use, verification of analytic claims | [Mathematics](#mathematics) |
| Showing code or a code diagram | [Code excerpts](code-excerpts.html) | Real excerpts with source metadata, rendering chrome, shared diagram semantics, diagram controls | [Code excerpts](#code-excerpts) |

</div>

Someone who only changes a record needs the first two sets: writing records and the documentation system's sections on order of work, pages and changes. From the page guides, a record writer needs only the few rules on what an excerpt, a formula or a figure may claim. The rest of the page guides matter to whoever writes a page. The chapters below follow the same split: first where content lives and in what order, then what a record says, then how a page presents it.

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
| Human explanation of a topic: current conclusions, figures, decisions and blockers | `docs/topics/<topic>/index.md`, when a person asked for a page |
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

"One fact, one home" has a single deliberate exception: `README.md`. Someone arriving cold reads the README first and may need the project's purpose, how to install it and how to run it, even though each of those facts already has a home elsewhere. So the README may repeat them, briefly. The price is a duty: when those facts change, update the README in the same deliverable. If the README and the owning document disagree, check the owning document; it wins.

The kit's rules are shared policy and are not copied into a project's entry files. What a project owns is its `docs/PROJECT_CONTEXT.md`: the repository map, the commands, the named documentation routes and the choices specific to that project.

The homes listed in the guide describe new projects. An existing project may keep its own explicit locations; whether an old route may stay is decided under [refactoring over compatibility](code-practices.html#refactoring-over-compatibility). Create a directory or document only when there is content for it, and link it from `docs/index.md`.

<!-- /fold -->

<!-- fold: dead-end Why not an archive or a second status board -->

Every other Markdown file must have a defined role: a subject record, log, experiment contract or guide, exact evidence, or unfinished plan or decision. A generic archive, review collection or second status system is not created to avoid choosing an owner; it would become another place where a fact can hide. Names explain the subject or mechanism, so vague labels such as `Info` or `Manager` are avoided.

<!-- /fold -->

Full guide: [documentation system](documentation-system.html), especially [canonical homes](documentation-system.html#canonical-homes) and [README is the bounded exception](documentation-system.html#readme-is-the-bounded-exception).

</section>

<section class="card" id="record-first">

## The record is written first; a new page is made only when a person asks for one

<p class="bs-lead">The agent that did the work writes the record. A new page waits for a person's request; an existing page follows every change to its record, even when that adds or removes a chapter. Where the runtime supports delegation, page work beyond a small sync goes to a separate page agent that takes the finished record as its brief.</p>

<figure id="fig-record-first">
<div class="bs-flow" role="img" aria-label="Step 1: the working agent, which did the work, writes the record in Markdown: what changed, what was measured and why. Step 2 starts when page work is due: a person asked for a new page, or a record change made an existing page stale, possibly adding or removing a chapter. Where the runtime supports delegation, a separate page agent receives the finished record as its brief, reads the applicable page and site guides, writes in its own words without adding anything the record lacks, and stays available for later page work in the same task. Step 3: the delegating agent looks at the captures, at every supported width and reader view, before reporting the page done. A small sync of a sentence or two needs no page guides and is not handed on; the agent that edited the record fixes it itself.">
<div class="bs-node bs-teal"><span class="bs-label">1 · Working agent</span><b>Writes the record</b><ul><li>what changed, what was measured, why</li><li>plain Markdown, under writing records</li><li>no new page unless someone asks</li></ul></div>
<div class="bs-arrow"><span>page work</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Page agent</span><b>Writes the page</b><ul><li>brief: the finished record, plus the request or the record change</li><li>reads the applicable page and site guides</li><li>own words; nothing the record lacks</li><li>kept for later page work in the task</li></ul></div>
<div class="bs-arrow"><span>captures</span></div>
<div class="bs-node bs-orange"><span class="bs-label">3 · Delegating agent</span><b>Checks the captures</b><ul><li>every element the change touched, whole</li><li>at each supported width and reader view</li><li>only then reports the page done</li></ul></div>
<div class="bs-back"><span>×</span> A small sync is not handed on: when a record edit makes a sentence or two of a page stale, the agent that edited the record fixes them itself, without the page guides.</div>
</div>
<figcaption><b>Figure 1.</b> Who writes what, and in which order. Page work starts from a person's request for a new page, or from a record change that an existing page must follow. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Writing a record and writing a page are different jobs. The agent that did the work knows what changed, what it measured and why, and that knowledge is freshest right after the work; the record is where it has to land. A page reorders, illustrates and simplifies for a reader. That takes a different set of guides, and a new page is wasted effort when nobody asked to read it. When one rule set served both jobs, an agent that only had to update a record was routed through the page guides as well. Splitting the jobs keeps the record writer's reading short and gives the page to an agent whose whole task it is.

[Figure 1](#fig-record-first) shows the order. Notice the two ways page work starts. A new page needs a person's request. An existing page needs none: it explains a record, so when the record changes, the page follows in the same deliverable, after the record, even if it gains or loses a chapter because the record did. Because the page agent begins from the record alone, anything the record leaves out shows up as a gap; the page agent reports it to the agent that delegated the work, who gets the record fixed before the page explains it.

"Page" here has a narrow meaning: a page for people, a topic's `index.md`. A [registered source page](authoring.html#registered-source-pages) only shows a record whole, so editing one is editing a record, and the record rules apply.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A page nobody asked for</h3><p>An agent fixes a slow import, then spends the rest of its turn building a new topic page. The record gets two lines; the measurement and the reason for the fix are on the page only.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Record now, page when asked</h3><p>The agent writes the fix, its measurement and the reason into the topic record. A week later the owner asks for a page. A page agent writes the chapter from the record, and the agent that delegated it looks at the captures before reporting the page done.</p></div>
</div>

<!-- fold: experiment What a page agent receives and returns -->

**The brief.** Where the runtime supports delegation, page work larger than a small sync is handed on, and the agent that did the work no longer writes the page itself. It writes a brief with five parts: the finished record; what started the work, either the person's request or the record change the page must now follow; the pages and chapters to change; the guides the page agent must read first, named one by one, because a delegated agent knows only what its brief says; and when the work counts as done. Done means the site validation that applies to the change has passed, captures at every supported width and in each reader view included.

**The page agent's part.** It reads the page guides and site guides that apply, then explains the record in its own words. It may reorder, simplify and illustrate, but a rule, number or limit on the page must already be in the record. When it finds a gap or a contradiction in the record, it does not fill it on the page; it reports it to the delegating agent, who gets the record corrected first.

**The delegating agent's part.** It looks at the captures itself before it calls the page done, as the [by-eye review](validation.html#validation-and-review) asks: each element the change touched, whole, at every supported width and in each reader view it appears in, such as one or two chapters side by side, checked for alignment, spacing, list markers and overflow. A passing build does not replace that look.

**Later page work.** Further page work in the same task goes to the same page agent. It has already read the record and the guides, so the next job starts from what it knows.

The [delivery guide](delivery.html#delegating-a-page-for-people) has the complete list.

<!-- /fold -->

<!-- fold: code Small syncs, runtimes without delegation and who reads what -->

**A small sync.** Sometimes a record edit makes a sentence or two on a page wrong. That fix needs no page guides, and handing it to a new agent costs more than the fix, so the agent that edited the record changes those sentences itself, in the same deliverable, after the record. Lint's reread notes, explained in [In step](#page-and-record-in-step), list the chapters that link a changed section; a chapter that links only the whole record is listed only when the record's opening text changed, which is why a chapter links the section it explains. Anything larger, or anything that needs layout, a figure or a new block, is page work.

**No delegation available.** Some runtimes cannot hand work to a second agent. The page is then still a separate step in the same deliverable: the same agent starts it only after the record is finished.

**Who reads which guides.** The record writer reads writing records and the documentation system's sections on order, pages, open work and changes. It needs the page guides only for the few rules on what a code excerpt, a formula or an experiment visual may claim, which apply in records too; [writing records](records.html#excerpts-formulas-and-figures) names them. The page author reads the applicable page and site guides, starting from the [writing index](writing.html) and the [site index](maintenance.html).

<!-- /fold -->

Full guide: [record first, page on request](documentation-system.html#record-first-page-on-request) and [delegating a page for people](delivery.html#delegating-a-page-for-people).

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
<figcaption><b>Figure 2.</b> Promotion moves knowledge to its subject; the producing evidence stays where it was made. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A document that mixes plans, findings and evidence becomes hard to trust: without a review, a reader cannot tell whether a sentence describes current behavior or an intention. The guide therefore reviews a mixed document section by section as work matures. It also guards against a quieter failure: assistant proposals remain proposals until explicitly accepted, and migration, silence or continued discussion does not make them accepted requirements.

[Figure 2](#fig-open-to-topic) follows content through its three owners. Notice the crossed-out way back: a closed record keeps supporting current knowledge through a link, but it does not become a second knowledge home.

Unfinished implementation, unresolved choices and prospective acceptance stay with the open owner; topic research notes may remain with their topic, and `OPEN.md` routes there. Each line in `OPEN.md` is one route that links the document owning the work. When the work is finished, the line is removed, not ticked, struck through or marked done; lint checks both. A completed source is retired only after its unique content and references are accounted for and the user approves the deletion.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A proposal promoted by silence</h3><p>An assistant suggests a naming rule in a plan. Nobody objects, so the next edit copies it into the topic as a requirement, and the plan keeps describing it as if it were still open.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Accepted, then moved and labelled</h3><p>The rule moves to the topic only after someone explicitly accepts it. The topic labels it as an accepted future specification until it is implemented, the plan keeps the remaining work, and the worklog records the landing.</p></div>
</div>

<!-- fold: dead-end Why readiness has one owner instead of several boards -->

It is tempting to track "what is ready" on several boards at once. Then two boards disagree, and neither can be trusted. The guide gives each kind of state one place instead:

- the execution owner of a workstream carries its order, prerequisites, status and the instructions for resuming it;
- an implementation plan carries the acceptance conditions agreed in advance;
- a coverage map links each obligation to its evidence.

Plans also keep two kinds of readiness apart: ready to investigate is not the same as ready to implement.

<!-- /fold -->

<!-- fold: experiment Evidence identity and frozen records -->

Sometimes a document must be kept exactly as it was, byte for byte, because something cites it, pins it as a source or needs it to reproduce a result. Keep exact originals only for such a concrete purpose.

**What is recorded.** A location manifest lists, for each frozen document, its original logical path, source revision, byte count and cryptographic hash, together with the references needed to follow it. A document that comes from a different revision than the rest of its collection gets its own revision entry. The manifest says what a document is and where it lives. It is an index, not a second home for the content.

**What is never done.** Frozen links are not rewritten, originals get no banners, and missing bytes are not quietly replaced. Current prose links to current knowledge or to an explicit evidence location.

**Reading old links.** A project may resolve the links inside frozen documents to where files live today. If it does, only origins and records that were explicitly registered are translated; current links and missing targets stay strict. A reading view shows which files are exact originals and which are current files that may still change. A symlink is neither a frozen source nor write protection, and is not described as one.

**Restoring.** Put an original back only where nothing exists yet. If a newer live file is in the way, keep it separately, and do not overwrite unrelated pending work.

**Where the manifest is described.** The [resources guide](resources.html#resource-closure-and-evidence) explains the location manifest and the path adapters a project may register for frozen records.

**What this proves.** Relocating sources, verifying hashes and offering a reading view establish that a document is intact. They do not show that an old procedure still qualifies at runtime, and they give no permission to execute it.

<!-- /fold -->

<!-- fold: experiment Shelved investigations -->

Shelving an investigation is a decision about scope, not a quiet stop. Record it in the experiment's own guide and in the topic that owns the work, and keep there what a later restart would need: the inputs, the code, the failures and the concrete conditions under which the work could resume. Resuming is not automatic; it takes a new, explicit assignment.

A shelved page can stay reachable through its direct link with `hidden = true`. Hiding does less than it may seem: it deletes no evidence, and it does not make any replacement qualified.

<!-- /fold -->

Full guide: [from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge), [evidence identity and frozen records](records.html#evidence-identity-and-frozen-records) and [shelved investigations](records.html#shelved-investigations).

</section>

<section class="card" id="topics">

## A topic is one folder: always a record for agents, and a page when people need one

<p class="bs-lead">Each subject lives in <code>docs/topics/&lt;topic&gt;/</code>. Every topic has a record agents follow; a page explains it to people once someone asks for one.</p>

<figure id="fig-topic-folder">
<div class="bs-folder" role="img" aria-label="The folder docs/topics/vehicle-model holds vehicle-model.md and tyre-fitting.md, records that agents follow; index.md, the page people read, which links to the records; and evidence, sources kept for a citation or reproduction.">
<div class="bs-folder-head"><code>docs/topics/vehicle-model/</code></div>
<div class="bs-folder-row bs-teal"><code>vehicle-model.md</code><span class="bs-badge">record</span><span><b>Agents follow it.</b> The exact spec: terms, limits, anchors other files point to.</span></div>
<div class="bs-folder-row bs-teal"><code>tyre-fitting.md</code><span class="bs-badge">record</span><span><b>More records</b> as the subject grows, each named for what it holds.</span></div>
<div class="bs-folder-row bs-violet"><code>index.md</code><span class="bs-badge">page</span><span><b>People read it.</b> The conclusion, a figure, why, the next decision; links the records.</span></div>
<div class="bs-folder-row bs-orange"><code>evidence/</code><span class="bs-badge">evidence</span><span><b>Kept for a reason:</b> sources for one citation or reproduction.</span></div>
</div>
<figcaption><b>Figure 3.</b> One topic folder and who reads each file. This diagram contains no measured results.</figcaption>
</figure>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Record and page</h3><p>Agents follow the spec and people need it explained: the record holds the exact text, the page the reasoning and figures.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">contract only</span><h3>Record, no page</h3><p>A schema, checklist or limit nobody has asked to see explained. Add a page later if someone asks.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">declared exception</span><h3>Page, no record</h3><p>For cases the rules do not foresee yet, such as the kit's own pages that explain its guides. It says why in its frontmatter, <code>page_only = "…"</code>; without that, lint warns.</p></div>
</div>

The split follows how each reader uses the text. An agent is routed to an exact file and section and must find the same words there next time; a person wants the conclusion first, a figure and an example, and is better served when the page is rearranged for reading. Putting both in one file means layout HTML in the agent's way, or a spec that moves whenever the page is improved. The two therefore cover the same subject on purpose, and that overlap is not duplication to remove; what keeps them honest is that the record decides. A page may reorder, simplify and illustrate, but a rule, number or limit it shows must be in the record. So the record comes first, as [Record first](#record-first) describes; a topic without one is a rare, declared exception that the conformance check rereads on every upgrade.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>The spec inside a fold</h3><p>A topic has only <code>index.md</code>. Its tyre limits sit in a fold between two figures. An agent routed there reads card markup to find them, and a later layout change moves them.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Spec in the record, page links it</h3><p>The limits live in <code>vehicle-model.md</code> under their own heading. The page shows the figure, says why the limits are what they are and links that heading.</p></div>
</div>

Full guide: [canonical homes](documentation-system.html#canonical-homes) · [one record per topic](records.html#one-record-per-topic) · [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown)

</section>

<section class="card" id="records-and-pages">

## Records keep the contract for agents; pages explain it to people

<p class="bs-lead">Agents read plain Markdown records through one router; a rendered page is added when a person asks for one.</p>

<figure id="fig-records-and-pages">
<div class="bs-flow" role="img" aria-label="AGENTS.md is the one thin router: it names the project context and prerequisites and routes the remaining rules by action to plain Markdown records. A rendered page, made when a person asks for one, explains current conclusions from those records and links to them instead of reproducing them. Reading a route grants no permission to execute or publish.">
<div class="bs-node bs-orange"><span class="bs-label">Router</span><b><code>AGENTS.md</code></b><ul><li>Names the project context and prerequisites</li><li>Rules every task needs</li><li>Remaining rules routed by action</li></ul></div>
<div class="bs-arrow"><span>by action</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Records for agents</span><b>Plain Markdown</b><ul><li>Headings, tables and lists</li><li>Exact file references and evidence links</li><li>Contracts, readiness and chronology</li></ul></div>
<div class="bs-arrow"><span>explain</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Page for people · on request</span><b>Conclusions and decisions</b><ul><li>Current conclusions and accepted specifications</li><li>Demonstrated behavior with its evidence scope</li><li>Useful figures and the next decisions</li></ul></div>
<div class="bs-back"><span>×</span> A page links to records instead of reproducing them. Reading a route grants no permission to execute or publish.</div>
</div>
<figcaption><b>Figure 4.</b> Agents reach records through one router; people reach an explanation through pages that link back to the records. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Agents and people need different things from the same knowledge. An agent follows exact headings, file references and anchors; a person needs the conclusion, a figure and the next decision. Without this split, layout HTML gets in an agent's way and bookkeeping buries what a person came to learn. The documentation system therefore keeps contracts, handoff and resume state, readiness boards, bookkeeping and long run chronology in records, and pages link to those records instead of reproducing them. How a record itself is written, its naming, claims and numbers, has its own guide: [writing records](records.html).

[Figure 4](#fig-records-and-pages) shows the two reading paths. Notice that the page sits downstream of the records: it explains them but does not own them.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A topic page doubling as a work log</h3><p>Below its conclusion, the rendered topic page holds a readiness board, a handoff checklist and a dated diary of every run.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Conclusion on the page, state in records</h3><p>The page states the current conclusion, shows a figure with its evidence scope and names the next decision. The readiness board, handoff state and run chronology stay in records that the page links to.</p></div>
</div>

<!-- fold: code Record format and registered source pages -->

- **One record per topic.** It starts as `docs/topics/<topic>/<topic>.md`; when it grows, split it into files named after what they describe. A subject record is never called `README.md`. Add the page, `index.md`, once a person asks for one. A page with no record says why in its frontmatter, with `page_only = "<reason>"`; otherwise lint warns.
- **Plain Markdown in records.** Headings, tables, lists, exact file references and links to evidence. Layout HTML stays out; a diagram that a record needs goes into its own file and is linked. Anchors that other documents point to are kept. Both points come from [writing records](records.html#format).
- **A record can also be shown whole.** A site may render a record as a [registered source page](authoring.html#registered-source-pages). The Markdown file remains the record and the only copy anyone edits; the rendered page adds nothing of its own, so editing it is editing a record, not page work. The guides linked from this page are rendered that way.

<!-- /fold -->

<!-- fold: code Agent entrypoints: import versus point -->

Coding agents read a repository's entry file before they act. The guide keeps that file small and makes it a router, not a rulebook.

- **One thin router.** `AGENTS.md` names the project context and the prerequisites. An agent reads the orientation, and the rules that apply to every task, once at the start of work, unless they are already loaded.
- **Everything else by action.** Each row names a trigger, the files or sections to read and when to read them. Every matching row applies before its action, and the rows are checked again when a task grows. Plans, topics and evidence for one task are found through named links in the project context or in the rule that applies.
- **Two clients, one router.** Codex follows the named paths and triggers in `AGENTS.md` directly. Claude Code gets the same router through a bare, standalone `@AGENTS.md` line in `CLAUDE.md`. An import path is relative to the file that imports, and the chain of imports stays short. Written inside backticks or a code fence, an import is plain text and imports nothing.
- **The kit must be present.** A project that uses the kit as a submodule initializes `.docs-kit` before relying on its rules. If a required policy file is missing, report that and resolve it before doing the work the policy governs.

<!-- /fold -->

<!-- fold: dead-end When a page drifts toward agents -->

When a page becomes predominantly agent-facing, its agent material moves into records and its human-facing core stays in a page. Removing the page from navigation or publication follows the deletion gate. When dated or frozen links still point to a removed page, the owner decides how they keep resolving. A hidden stub with the former anchors also keeps the published address. The project's path adapter maps the old path for lint and lets the address go. Lint rejects a frozen or dated link that neither covers.

<!-- /fold -->

Full guide: [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown), [record format](records.html#format) and [agent entrypoints](documentation-system.html#agent-entrypoints-import-versus-point).

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
<figcaption><b>Figure 5.</b> How a record change reaches the pages that explain it. This diagram contains no measured results.</figcaption>
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

Numbers get a second reminder on a site that turns it on with `page_number_notes = true`. That is one setting for the whole site, written with the other top-level settings above the first `[[nav]]` table. Lint then lists every number in a page's prose that none of the records the page links state, chapter by chapter. Such a number has three ways out: state it in its record, show it as code when it is a literal value such as a size in a sample, or take it off the page. Like the reread reminder, this is a note and never fails a run, and it does not judge whether the record's own number is right. Turn it on for a site whose pages explain Markdown records, as this kit's site does. Leave it off for a site with pages that report measurements from experiment data: their numbers are rounded or derived, match no record text, and need the project's own ledger check instead.

This update needs no new request: an existing page always follows its record, also when that adds or removes a chapter. It lands in the same deliverable, after the record. Who makes it follows from [Record first](#record-first). When the listed chapter needs a sentence or two, the agent that edited the record makes that sync itself. Anything larger, or anything that needs layout, a figure or a new block, is page work: where the runtime supports delegation, it goes to a page agent with the finished record as its brief.

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

New entries go on top, and old entries are never edited. An entry written before its commit exists may say that the hash comes with the landing commit; later, look the hash up in version history instead of going back to fill it in.

An entry says much the same as its commit message, and that is intended. The worklog is one file you can read without Git. It survives history that was squashed or rebased, and it has room for what no commit carries: probes, and decisions or events that belong to no single commit. Write the entry and the commit message in the same step, so the two agree. The duplication is worth reconsidering only if a worklog becomes slow to lint or awkward to search.

A probe is recorded in one line:

```text
probed <subject> → <verdict>, <decisive reason>, <time spent>
```

Detailed probe artifacts follow the [experiment retention rules](records.html#numbers-and-staleness).

<!-- /fold -->

<!-- fold: code Drafts kept below the page end -->

A page may carry drafts that belong to its topic below a <code>&lt;!-- page-end --&gt;</code> marker. Only what stands above the marker is rendered, so readers never see the drafts. Two things do not move into that tail: chronology, which belongs in the worklog, and owed work, which still needs a route in `OPEN.md` to its owner. Nor is the tail a dumping ground: notes that nothing leads to are not left behind.

<!-- /fold -->

<!-- fold: dead-end Why there is no archive staging layer -->

An archive folder for superseded files feels cautious. In practice it becomes one more place where facts live on without an owner. The guide skips that step: once the removal of a superseded source is approved, it goes in the same commit that lands its replacement. A byte-exact copy of a superseded document is kept only when a check or a citation needs those exact bytes. That limit is about superseded documents; what an experiment retains is a separate list in the record rules.

A related point concerns labels. The invariants of a project live in the owning records and in cross-cutting conventions. A page may still show one as a marked statement: `**INVARIANT:**` for a constraint that must survive edits, `**DON'T-REDO:**` for a settled decision. At the start of its own paragraph the marker becomes a labelled card. Inside a sentence or a list item the raw label would show on the page, so such a statement gets its own paragraph.

<!-- /fold -->

<!-- fold: experiment Local review, browser approval and publishing -->

These rules belong to the site guides: local review to [validation](validation.html#local-review-and-browser-access), the gate before deployment to [publication](publication.html#publishing-gate).

**Before review.** Work from the project root with the pinned kit, use the commands in the project's context and finish the checks in the [validation guide](validation.html#validation-and-review) first. Then show the reviewer the rendered page with its figures; add source or evidence links where they help.

**Serving the page locally.** Serve only the generated output, and only on loopback. Before reusing a server that is already running, confirm who owns it and which checkout it serves. Do not expose the repository root, and do not stop a server that belongs to another session. Stop your own temporary servers after the review, unless one is kept running for the user's preview.

**When a browser is refused.** Approval to use a browser covers the supported origin only. If access is rejected on policy grounds, keep the rejection and settle the permission with its owner. Switching transport, browser or control API to get around the block is not allowed. Opening a file URL by hand is no proof that an agent inspected the rendering.

**Publishing.** Only the project's chosen branch or environment publishes, with authorization and passing checks, and a requested review or a deletion passes its own gate first. Changing what the hosting serves is a separate, explicit operation: building the source does not mean a version is deployed. A rollback leaves unrelated work untouched, and the chosen revision is rebuilt and verified.

<!-- /fold -->

Full guide: [rules for changes and chronology](documentation-system.html#rules-for-changes-and-chronology), [local review and browser access](validation.html#local-review-and-browser-access) and the [publishing gate](publication.html#publishing-gate).

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

Two names for one object make a reader wonder whether there are two objects. A claim that outruns its evidence is worse: a smoother drawing can be read as proof of accuracy, and an estimate typed into an empty cell looks like a measurement. Writing records therefore asks for one term per object across prose, controls, legends, tables, figures and output, and separates claims that require different evidence: visual fidelity, smoothness, input preservation, correspondence with a source and physical accuracy. A local check or smoother drawing proves only its tested property.

These rules live in the records guide because a claim is first made in a record, by the agent that did the work. A page that explains the record makes the same claims and follows the same rules; it cannot claim more than its record does. The four labels above mark claims that the guide keeps apart.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An overclaim</h3><p>"The new interpolation is accurate." The only check was that the plotted curve looks smoother, and an empty error column was filled with an estimate.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A scoped claim</h3><p>"The plotted curve is smoother (visual check). Correspondence with the source: not measured." Where a supported bound exists, it is given with its source.</p></div>
</div>

<!-- fold: dead-end Decision rationale and baselines -->

A decision recorded without its reasons invites the same debate again. Put the rationale next to the decision, including why this instrument or default was chosen and why the alternatives lost.

Baselines need the same care. A baseline cited for what currently ships has to measure what ships, and a retired baseline is labelled historical. The verdict of an experiment is also a different kind of content from measurements taken in deployment, so the two are not presented as one.

<!-- /fold -->

<!-- fold: code Naming mechanisms, functions and renames -->

Name a mechanism by what the reader can see it do. Terms from inside a formulation belong only where that formulation is being explained. When something is renamed, the rename covers every surface it appears on, so that no old name lingers. For a function, say what it receives, what it returns, what it optimizes or interpolates, and which of its inputs vary and which stay fixed.

<!-- /fold -->

Full guide: [naming and honest claims](records.html#naming-and-honest-claims).

</section>

<section class="card" id="evidence">

## A measured number is current only with its full provenance

<p class="bs-lead">Quote a number as current evidence only when its source and conditions are recorded and still hold.</p>

<div class="bs-specs"><div><span class="bs-label">Source</span><b>Commit + command</b></div><div><span class="bs-label">Conditions</span><b>Runtime + workload</b></div><div><span class="bs-label">Reading</span><b>Units + baseline</b></div><div><span class="bs-label">Reach</span><b>Method + scope</b></div></div>

A number without its conditions cannot be checked, and a number whose inputs have changed can look authoritative while no longer being true. Writing records therefore requires full provenance for any current measured claim, and a rerun before quoting it as current when code, input data, method, workload or runtime conditions affecting it change. A historical label does not qualify changed inputs. Configuration values, derivations and design arithmetic are not measurements: they cite their source and are labelled accordingly.

A current measured claim records the eight items above and links its raw result and limitations. The number is recorded in the record of the work that measured it, and a page that quotes it is held to the same rule.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A number without provenance</h3><p>"The new layout loads much faster." No commit, command, workload or baseline is given, and the input data changed after the run.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A number with provenance</h3><p>The claim names its source commit, exact command, runtime and workload, units, baseline, method and scope, and links the raw result and its limitations. After the input data changed, it was rerun before being quoted as current.</p></div>
</div>

<!-- fold: experiment Number ledgers for redesigns -->

A redesign restates numbers: in new prose, in redrawn figures, on slides. Each restatement is a chance to change a number by accident. Two safeguards answer that. A ledger records the source of every number, and the evidence blocks that are kept word for word are locked so that they cannot change unnoticed. Each project keeps its own ledger format and its own checks for both.

Two rules bound what may appear. A slide face shows only numbers that its chapter also shows. And every distinct number in a redesigned chapter, labels inside figures included, has a source in the ledger.

An edit that changes presentation only may reuse captured results, but only after checking that identities, numbers and treatments are still intact.

<!-- /fold -->

<!-- fold: experiment What stays with the producing work -->

The work that produced a result keeps its own record: protocols, outputs, snapshots, failed attempts, changed settings, what actually happened, the reviews that were really performed and the uncertainty that matters. For an experiment, the experiment directory also holds the producing code, the inputs, the full result tables, the source pins and any independent reviews. Repository size decides where this material is stored, not whether it is kept: bulky files may live outside Git when the experiment directory says where they are and how to identify them. A source pin can stand for the producing code when the run started from a clean tree, the commit stays reachable and the directory records the pin, the command and the input identities; uncommitted code stays as a copy or a diff.

Other documents point there without copying. The page explains what the results establish. The worklog records the landing and its hashes and does not duplicate the tables. Retained measured content falls under the deletion gate like everything else.

A rerun does not overwrite history. The old record keeps its date, runtime, inputs and scope, and historical records keep their original source pins, inputs, runtime, settings, resource limits, deadlines and verdicts wherever those fields apply.

<!-- /fold -->

Full guide: [numbers and staleness](records.html#numbers-and-staleness). Screenshots, clips and live experiment reports are presentation and belong to the figures guide; see the [Figures](#figures) chapter.

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

A shared kit could have forced one homepage layout on every project. It does not. Each project decides how its homepage is composed: the order of information, the sections, the hero and the visual story. A research narrative, an engineering reference and a navigation dashboard can look quite different and still use the kit.

The shared visual components are optional building blocks. Using one does not hand the surrounding page over to the kit. Project illustrations, scientific figures, domain widgets and distinctive compositions stay with the project, and the starter homepage is an example, not a template to follow.

One thing is shared: navigation. It belongs to the whole site, not to any single page. A homepage that lists its own sections, where every other page shows the site tree, makes each move into a reader feel like entering a different site. Keep the same tree on every page, and let the homepage introduce the pages through cards or its own composition.

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

A page opts in with `page_css = ["build-sheet.css"]`; anything specific to one page goes into a separate local stylesheet. Cards keep the height of the reader stage. Each chapter states its claim and shows one meaningful visual block: a figure, a flow, a table or tiles. As a size check, at 1600 × 1000 a chapter should fill about half a card. A thinner chapter is merged into a neighbour, not padded.

The blocks, by what they are for:

| Block | Use it for |
|---|---|
| `bs-lead` | The chapter's claim, in one sentence |
| `bs-specs`, `bs-stats` | Key values with labels; two to four headline measurements, each with units and scope |
| `bs-chips` | Short tags for options; a rejected option keeps its reason |
| `bs-grid g1` through `g4`, `bs-part` | Rows of visuals or parallel content; lists set against each other |
| `bs-checks`, `bs-check`, `bs-badge` | Parallel claims that can be checked, each showing its state |
| `bs-board`, `bs-row`, `bs-state` | The one board that shows current status |
| `bs-flow`, `bs-node`, `bs-arrow`, `bs-back`, `bs-stack` | A one-way mechanism: labelled arrows, with prohibited feedback drawn explicitly |
| `bs-orange` through `bs-muted` | The shared tones; a tone never carries meaning on its own |

Rows are always full. The main medium takes the whole width (`bs-grid g1`). Photos and renders go at most two to a row, and paired animations sit side by side. Two, three or four items fill one row. Five split three over two (`bs-checks r32`), six go three by two, seven four over three, eight four by two. Narrow columns reflow.

In a flow, keep arrow labels to about 12 characters and box titles to about 30. Full mappings belong in the topic record.

<!-- /fold -->

<!-- fold: code Slide face details -->

- **One face per chapter.** A chapter may open with a single 16:9 slide face that states its takeaway with one visual. The chapter that follows stays the complete source and reads end to end without the slide.
- **Eyebrow and visual.** The eyebrow names the subject and carries no chapter number. The visual is built from the shared slide vocabulary or a project-local diagram, and it reuses the chapter's own figure assets.
- **Caveats travel with the claim.** A caveat that changes what a claim means goes on the slide too, not only into the chapter. The slide is the one permitted repetition of a fact: it shows the chapter and never owns the fact.
- **Too much content.** A face that does not fit 16:9 is holding too much. Move detail into the chapter; do not shrink the type. Below 720 px the face stacks into a readable column.
- **Figures.** A slide figure is a view of a numbered chapter figure. It gets a short caption and no new number.
- **Tones.** Each tone means one thing across all of a project's slides. The accent and warm tones identify the methods being compared, `is-alert` marks failures and warnings, `is-held` marks held-out, hidden or pending items, and everything else stays neutral.

<!-- /fold -->

<!-- fold: experiment Completion and review -->

Layout work is reviewed in the form the reviewer asked for: a separate prototype, or a trial made in place and left uncommitted. Either way the redesign must not lose anything. Content, evidence, media identities and public anchors all survive it. Before calling it done, pass the [documentation review gate](documentation-system.html#rules-for-changes-and-chronology) and complete [site validation](validation.html#validation-and-review), including the checks the project requires. Validation ends with a look by eye: each changed element is captured whole at every supported width and checked for alignment, spacing and overflow. When the page was delegated, the agent that delegated it looks at those captures before reporting the work done, as [Record first](#record-first) describes.

A page that exists to support a decision ends with a table that sets the options against stated criteria, and with a clear verdict.

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
<figcaption><b>Figure 6.</b> Optional depth branches from a complete visible argument. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

An explanation fails when the reader meets a number before the instrument that produced it, or a term before its definition. It also fails when the decisive step hides in an optional section that many readers never open. The guide orders by understanding: purpose, prerequisites, ingredients, mechanism, examples, evidence and limits. The complete argument, narrative figures, comparison cases and verdict must remain intelligible with every fold closed.

[Figure 6](#fig-story) shows the two reading layers. Notice that the arrow goes one way: folds deepen the Story but do not hide a separate required argument.

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

Every included figure carries the four items above.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An orphan figure</h3><p>A diagram sits under the text with the caption "Architecture". It has no number, anchor or source, and the text says only "see below".</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A referenced figure</h3><p>The text says "Figure N shows the request path; notice that a retry returns to the queue, not to the caller", with Figure N linked to its anchor. The numbered caption names its source and states that the diagram is illustrative.</p></div>
</div>

<!-- fold: experiment Designing comparisons -->

- **Design the views as a set.** Give the compared views the same orientation, scale, framing and input cases. Keep the zoom when the reader switches between them, show an overview that locates each detail, and use the same markers and colours in profiles and tables.
- **Identity does not depend on colour.** Method names in controls and legends carry it. Offer every option the comparison names, grouped by method, each with its role: current, selected, previous or rejected.
- **No duplicate gallery.** An interactive comparison replaces the static gallery that would repeat it, and keeps a useful image for loading or fallback.
- **Draw the finding.** Do not make the eye compute it. Show where the samples really are and how the result is constructed, and keep four things visibly apart: measurements, solved points, continuous geometry and the polygon used to render it.
- **Independent changes.** Show the baseline, each change alone and their combination across the relevant scenarios, next to an ablation table and the metric definitions. If an effect is zero, say so and explain it honestly.

<!-- /fold -->

<!-- fold: code Chart sizing, interaction and access -->

- **Size.** A chart fits the column it actually sits in, with labels of at least 11 px. Keep bar labels short or move them into a legend. Crop empty margins, and leave out baked-in title bars, badges and debugging chronology. Use one camera or view across a series.
- **Legibility first.** An important comparison is not shrunk to fit a screen if that makes it hard to read. Limit the height of the overview and keep full-size inspection available.
- **Interactive views.** Each loads on its own, keeps dragging, scrolling and keys inside its region and never takes focus from the page. Linked views follow one selected state. Their data comes from the exact inputs and outputs of the run, checked by hash, and a static main render shows while they load.
- **Controls in step.** SVG toggles stay synchronized with their zoomed or lightbox versions. A carousel stops autoplay once the reader engages and pauses while a lightbox is open.
- **Access.** Use the shared components instead of duplicating handlers. Controls are visible, labelled, usable from the keyboard and at least 44 px as touch targets. Scrollable tables and equations get labelled local regions. Nothing overflows the page at any viewport.

<!-- /fold -->

<!-- fold: code Numbering, unnumbered images and generated figures -->

**Numbering.** Number figures across the page, or use a named sequence such as P1. Numbers are unique and follow reading order within their sequence. A plot, a diagram, a flow, an interactive comparison and an evidence capture all count as figures. An image that only shows what something looks like gets a short caption and no number. A figure left unreferenced on purpose says so in a source comment placed next to it:

```html
<!-- unreferenced figure: reason -->
```

**Generated figures.** Each names its generator, source revision, inputs, date and output hash in a manifest or in metadata; this holds for SVG, PNG and interactive data alike. Figures use the project's shared dark-compatible style, never a style invented for one figure. An explicit manifest maps figures to generators and is checked for missing and orphaned resources.

**Flows written in the page source.** HTML flows, like the figures on this page, count as local diagrams. The page source is their generator, and their layout passes the same collision and overflow review.

<!-- /fold -->

<!-- fold: experiment Run visuals and live experiment reports -->

- **Captures.** Prefer captures made by a script, with the same provenance as any other figure. A screenshot that can only be taken interactively states its commit, date and scenario or preset. It shows what something looks like and never supports a quantitative claim.
- **Overlays and motion.** When recorded data exists, derive overlays from it, not from screenshots. Show behaviour over time with a short clip packaged for the purpose or a useful sequence of frames, captioned and sourced like any figure.
- **Reports still in progress.** A public report on a live experiment carries `ongoing = true`. The flag comes off only when findings and limits are settled. The owning topic explains the scope and links to the evidence.
- **Which visuals fit.** Good candidates are quality overlays on the actual geometry, convergence, parity with a reference, timing or scaling, and trade-off plots. Say explicitly when a view does not apply. Topic, worklog and open routing are updated in the same deliverable.
- **Where the rest lives.** The [experiment workflow](experiment-workflow.html) owns experiment kinds, baselines, stopping conditions and what every experiment must contain, its verdict included.

<!-- /fold -->

Full guide: [figures and comparisons](figures.html#figures-and-comparisons), [interaction and access](figures.html#interaction-and-access) and [run visuals and experiment lifecycle](figures.html#run-visuals-and-experiment-lifecycle).

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
<figcaption><b>Figure 7.</b> The Math layer walks from marks on the Story's picture to the equation and a worked example. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A formula that arrives with undefined symbols asks the reader to trust it rather than follow it, and a formula plot disconnected from the Story adds a second picture to decode. The guide builds from the reader's known construction. Define symbols, units, mathematical terms and prerequisites before use. Show intermediate reasoning, including product and chain rules when relevant. State structural assumptions and distinguish local conditions from global validity. A non-obvious formula needs a derivation or a precise companion-section citation.

[Figure 7](#fig-math) shows how the Math layer reuses the Story. Notice that the equation is reached through marks on the same picture, not drawn from a separate one.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A formula dropped in</h3><p>An equation appears with symbols the page never defined, followed by a plot of the formula over a range the Story never mentions.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A formula built from the picture</h3><p>The Story's diagram marks each input and the solved quantity. The math fold defines each symbol with its unit, shows the chain-rule step, states where the result holds and works the equation with the Story's example inputs.</p></div>
</div>

<!-- fold: code KaTeX syntax and rendering -->

Set `math = true` in the page frontmatter, then write mathematics with these delimiters:

```text
In Markdown:      $…$   inline     $$…$$   display
Inside raw HTML:  \(…\)
```

The kit renders math with its bundled KaTeX; nothing is fetched from a CDN. A long expression wraps or scrolls inside its own box, and the type is never shrunk until it is hard to read. Formulas written inside raw HTML are easy to overlook, so inspect those in the rendered page too.

<!-- /fold -->

<!-- fold: experiment Verifying analytic claims -->

A claim about an analytic derivative or Jacobian comes with two things: the tolerance it was verified to numerically, and the executable self-test that did the verifying. A formula that is not obvious needs either its derivation or a precise citation of the companion section that derives it.

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

A rendered excerpt has distinct colours for types, classes and functions, a copy button, a chip naming its source, a language badge and a gutter that shows the line numbers of the real source file. Reuse the shared code chrome and keep every control accessible. For diagrams, three patterns are useful: numbered sequence steps, mode views over common data, and quantitative SVGs that are generated.

<!-- /fold -->

<!-- fold: dead-end Interactive diagram controls not yet built -->

Diagrams can use the pan, fullscreen and annotation controls that exist. Edge highlighting, drill-down and semantic zoom are only planned, so no page may describe them as working. If one is built later, the choice between the last two follows the content: drill-down, with a breadcrumb, when the child diagrams stand on their own; semantic zoom when the surrounding context has to stay visible.

<!-- /fold -->

Full guide: [code and diagrams](code-excerpts.html#code-and-diagrams).

</section>
