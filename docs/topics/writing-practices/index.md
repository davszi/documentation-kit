+++
title = "Documentation and writing"
brand_sub = "homes · records · pages · figures"
description = "Where each kind of documentation belongs, why the record is written before any page, what a record must say, and how the page guides shape chapters, figures, math and code, with illustrative examples."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css", "writing-practices/writing-practices.css"]
toc = [["Guide per task", "#routes"], ["One home", "#homes"], ["Record first", "#record-first"], ["Open to topic", "#open-to-topic"], ["Topics", "#topics"], ["Records and pages", "#records-and-pages"], ["In step", "#page-and-record-in-step"], ["Changes", "#changes-and-publishing"], ["Honest claims", "#honest-claims"], ["Evidence", "#evidence"], ["Chapters", "#page-design"], ["Build sheets", "#build-sheets"], ["Story and folds", "#explanations"], ["Figures", "#figures"], ["Mathematics", "#mathematics"], ["Code excerpts", "#code-excerpts"]]
page_only = "Explains the documentation and writing guides; they are the records, in rules/."
+++

# Documentation and writing

<section class="card" id="routes">

## Each guide owns one kind of documentation decision

<p class="bs-lead">The documentation system decides where content lives and in what order it is written; writing records decides what a record says; five page guides decide how a page for people presents it.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Documentation and writing guides by task">

| Before… | Read… | Explained here |
|---|---|---|
| Creating, moving, splitting or retiring a document | [Documentation system](documentation-system.html) | [One home](#homes), [Record first](#record-first), [Open to topic](#open-to-topic), [Records and pages](#records-and-pages), [Changes](#changes-and-publishing) |
| Upgrading the kit pin or taking over a repository | [Project conformance check](conformance.html) | [Topics](#topics), [In step](#page-and-record-in-step) |
| Writing or changing a record: a guide, topic record, plan, worklog or open-work entry | [Writing records](records.html), plus the [documentation system](documentation-system.html#record-first-page-on-request) from Record first through the change rules | [Topics](#topics), [Records and pages](#records-and-pages), [Honest claims](#honest-claims), [Evidence](#evidence) |
| Making a new page for people, once a person asked for one, or page work on an existing page beyond a small sync | [Record first, page on request](documentation-system.html#record-first-page-on-request) and [rendered pages are for people](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown), then the page guides below and the [site guides](maintenance.html) | [Record first](#record-first), [In step](#page-and-record-in-step) |
| Laying out a rendered page | [Page design](page-design.html) | [Chapters](#page-design), [Build sheets](#build-sheets) |
| Writing an explanation on a page | [Explanations](explanations.html) | [Story and folds](#explanations) |
| Adding a figure or comparison | [Figures](figures.html) | [Figures](#figures) |
| Writing mathematics | [Math](math.html) | [Mathematics](#mathematics) |
| Showing code or a code diagram | [Code excerpts](code-excerpts.html) | [Code excerpts](#code-excerpts) |

</div>

The table is a lookup: find the action, read the guide, then the chapter here that explains it. A record writer stops after the first three rows; of the page guides it needs only the few rules on what an excerpt, a formula or a figure may claim, which [writing records](records.html#excerpts-formulas-and-figures) names. Everything from Page design down concerns whoever writes a page.

The chapters follow the table's order. Each says why a rule exists, shows it and links the section that holds the exact text; the path of work from discussion to record has its own page, [Discuss, build, record](discuss-build-record.html). The examples are invented and contain no measured results.

</section>

<section class="card" id="homes">

## Every fact has one home, and other documents link to it

<p class="bs-lead">A fact is written once, in the record that owns it; every other document points there.</p>

<figure id="fig-one-home">
<div class="wp-fig wp-pair">
<div class="wp-panel wp-bad"><span class="wp-tag">Copies</span><b class="wp-head">One command in three files</b>
<div class="wp-file"><code>docs/PROJECT_CONTEXT.md</code><span><code>make sim PROFILE=fast</code></span><em class="wp-ok">updated</em></div>
<div class="wp-file"><code>topics/sim/index.md</code><span><code>make sim</code></span><em class="wp-no">stale</em></div>
<div class="wp-file"><code>plans/faster-sim.md</code><span><code>make sim</code></span><em class="wp-no">stale</em></div>
<p class="wp-foot">Which copy is true? The reader cannot tell.</p>
</div>
<div class="wp-panel wp-good"><span class="wp-tag">One home</span><b class="wp-head">One copy; the others link to it</b>
<div class="wp-file wp-home"><code>docs/PROJECT_CONTEXT.md</code><span><code>make sim PROFILE=fast</code></span><em class="wp-ok">home</em></div>
<div class="wp-file wp-link"><code>topics/sim/index.md</code><span>links the home</span><em>link</em></div>
<div class="wp-file wp-link"><code>plans/faster-sim.md</code><span>links the home</span><em>link</em></div>
<div class="wp-file wp-link"><code>README.md</code><span>short repeat, swept with the home</span><em class="wp-held">exception</em></div>
<p class="wp-foot">A change is made once; every link shows it.</p>
</div>
</div>
<figcaption><b>Figure 1.</b> One command, copied and then linked. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 1](#fig-one-home) shows the failure the rule prevents. Under Copies, one of three copies was updated and two were not, and nothing says which to trust. Under One home there is nothing to keep in step: the topic page and the plan point at the home. When copies do disagree anyway, the guide says to check the owning source, correct the stray copy and fix any summary that repeated it, all in the same deliverable.

The README is the one bounded exception. A person arriving cold reads it first and needs the purpose, the install and the run commands, so it may repeat them briefly; in exchange, it is swept whenever they change, and the owner wins when the two disagree. There is one `README.md`, at the root. A folder that needs a guide gets a file named after its subject, so a search result or a link says which guide it is.

Every other Markdown file has a defined role, such as a subject record, a log or an unfinished plan. A generic archive or a second status board is not created to avoid choosing an owner: it would become another place where a fact can hide. Which file owns which kind of fact is a lookup; the guide's [canonical homes](documentation-system.html#canonical-homes) table lists them, and an existing project may keep its own explicit locations under [refactoring over compatibility](code-practices.html#refactoring-over-compatibility).

Full guide: [canonical homes](documentation-system.html#canonical-homes) and [README is the bounded exception](documentation-system.html#readme-is-the-bounded-exception).

</section>

<section class="card" id="record-first">

## The record is written first; a new page is made only when a person asks for one

<p class="bs-lead">The agent that did the work writes the record. A new page waits for a person's request; an existing page follows every change to its record, and page work beyond a small sync goes to an agent whose whole task it is.</p>

<figure id="fig-record-first">
<div class="bs-flow" role="img" aria-label="Step 1: the working agent, which did the work, writes the record in Markdown: what changed, what was measured and why. Step 2 starts when page work is due: a person asked for a new page, or a record change made an existing page stale, possibly adding or removing a chapter. Where the runtime supports delegation, a separate page agent receives the finished record as its brief, reads the applicable page and site guides and writes in its own words without adding anything the record lacks. Step 3: the delegating agent looks at the captures, at every supported width and reader view, before reporting the page done. A small sync of a sentence or two is not handed on; the agent that edited the record fixes it itself.">
<div class="bs-node bs-teal"><span class="bs-label">1 · Working agent</span><b>Writes the record</b><ul><li>what changed, what was measured, why</li><li>plain Markdown, under writing records</li><li>no new page unless someone asks</li></ul></div>
<div class="bs-arrow"><span>page work</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Page agent</span><b>Writes the page</b><ul><li>brief: the finished record, plus the request or the record change</li><li>reads the applicable page and site guides</li><li>own words; nothing the record lacks</li></ul></div>
<div class="bs-arrow"><span>captures</span></div>
<div class="bs-node bs-orange"><span class="bs-label">3 · Delegating agent</span><b>Checks the captures</b><ul><li>every element the change touched, whole</li><li>at each supported width and reader view</li><li>only then reports the page done</li></ul></div>
<div class="bs-back"><span>×</span> A small sync is not handed on: when a record edit makes a sentence or two of a page stale, the agent that edited the record fixes them itself, without the page guides.</div>
</div>
<figcaption><b>Figure 2.</b> Who writes what, and in which order. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Writing a record and writing a page are different jobs. The agent that did the work knows what changed and why, and that knowledge belongs in the record while it is fresh. A page reorders, illustrates and simplifies for a reader; that needs other guides, and a page nobody asked for is wasted work. Splitting the jobs keeps the record writer's reading short.

[Figure 2](#fig-record-first) shows two ways page work starts. A new page needs a person's request. An existing page needs none: when its record changes, the page follows in the same deliverable, after the record, also when it gains or loses a chapter. Because the page agent starts from the record alone, anything the record leaves out shows up as a gap; it goes back to the delegating agent, who gets the record fixed before the page explains it. What the brief holds is set out on the [Engineering page](engineering-practices.html#delivery) and in [delegating a page for people](delivery.html#delegating-a-page-for-people). Without delegation, the same agent does the page as a separate step, after the record is finished.

The last step is a look by eye. The review keeps content, evidence, media and public anchors through any layout change, and work on several chapters is reviewed one chapter at a time, under [completion and review](page-design.html#completion-and-review).

One kind of page comes before any record: a page built while a proposal is still discussed. It exists to help the person decide, and its work has not started; [Discuss, build, record](discuss-build-record.html#discuss) follows it from the discussion to the person's yes. "Page" here means a topic's `index.md`. A [registered source page](authoring.html#registered-source-pages) shows a record whole, so editing one is editing a record.

Full guide: [record first, page on request](documentation-system.html#record-first-page-on-request).

</section>

<section class="card" id="open-to-topic">

## Finished work moves to its subject; evidence stays where it was made

<p class="bs-lead">As work matures, each kind of content moves to the record that owns it, the open route is deleted and the worklog records the landing.</p>

<figure id="fig-open-to-topic">
<div class="bs-flow" role="img" aria-label="Open work in a named plan, routed from OPEN.md, is investigated in producing work that keeps its evidence. Established findings move to the owning topic record, with accepted future specifications labelled apart from implemented behavior. A closed record supports current knowledge through a link and does not become a second knowledge home.">
<div class="bs-node bs-orange"><span class="bs-label">Open owner</span><b>Unfinished work</b><ul><li>Named plan or decision record</li><li>Unresolved choices and owners</li><li>Prospective acceptance</li><li>One-line route in <code>OPEN.md</code></li></ul></div>
<div class="bs-arrow"><span>investigate</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Producing work</span><b>Protocol and evidence</b><ul><li>Inputs and raw results</li><li>Failures and source pins</li><li>Reproduction instructions</li></ul></div>
<div class="bs-arrow"><span>establish</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Owning topic</span><b>Current knowledge</b><ul><li>Established behavior</li><li>Accepted requirements</li><li>Durable rationale</li><li>Accepted future specification, labelled apart</li></ul></div>
<div class="bs-back"><span>×</span> A closed record supports current knowledge through a link. It does not become a second current knowledge home.</div>
</div>
<figcaption><b>Figure 3.</b> Promotion moves knowledge to its subject; the producing evidence stays where it was made. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A document that mixes plans, findings and evidence becomes hard to trust: a reader cannot tell whether a sentence describes current behavior or an intention. So a mixed document is reviewed section by section as work matures, and [Figure 3](#fig-open-to-topic) follows its content to three owners. Notice the crossed-out way back: a closed record keeps supporting current knowledge through a link, but it does not become a second knowledge home. A proposal moves only after the person accepts it in words; silence or continued discussion is not acceptance, as [the yes](discuss-build-record.html#the-yes) explains.

`OPEN.md` holds one line per owed workstream, each linking the document that owns it. When the work lands, the line is deleted, not ticked or struck through; lint checks both. Readiness gets one owner too: a workstream's execution owner holds order, status and resume instructions, an implementation plan holds its acceptance, and a coverage map links obligations to evidence. Two boards that track the same state end up disagreeing.

A plan, decision record, review or coordination note exists to get one piece of work done. Once that work has landed and its lasting content is in the owning record, the document is deleted with the person's approval. Nothing is lost: Git keeps the bytes, a recorded hash stays valid, and whatever still needs the document cites its commit and path. Keeping an unedited copy, or moving it into an evidence folder, would leave an old rule looking current.

Shelving an investigation is a scope decision, not a quiet stop. It is recorded in the experiment's guide and the owning topic, with the inputs, code, failures and the conditions under which it could resume; resuming takes a new assignment. A page hidden with `hidden = true` stays reachable by link, but hiding deletes no evidence and qualifies no replacement.

Full guide: [from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge), [finished working documents](records.html#finished-working-documents) and [shelved investigations](records.html#shelved-investigations).

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
<figcaption><b>Figure 4.</b> One topic folder and who reads each file. This illustrative diagram contains no measured results.</figcaption>
</figure>

[Figure 4](#fig-topic-folder) reads from the top: records first, the page after them, evidence kept only for a concrete citation. The split follows how each reader uses the text. An agent is routed to an exact file and section and must find the same words there next time; a person wants the conclusion first, a figure and an example. One file for both would put layout markup in the agent's way, or move the spec whenever the page is improved. So the two cover the same subject on purpose, and the record decides: a page may reorder, simplify and illustrate, but a rule, number or limit it shows must be in the record. [Discuss, build, record](discuss-build-record.html#three-words) sets the record, the page and the chapter side by side.

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Record and page</h3><p>Agents follow the spec and people need it explained: the record holds the exact text, the page the reasoning and figures.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">contract only</span><h3>Record, no page</h3><p>A schema, checklist or limit nobody has asked to see explained. A page follows if someone asks.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">declared exception</span><h3>Page, no record</h3><p>The kit's own pages that explain its guides, and a page built while a proposal is discussed, until its work lands. The page says why with <code>page_only = "…"</code>; without it, lint warns.</p></div>
</div>

Which cases may have a page without a record is not settled yet; the two above are the known ones. Once such a page gains a rule, specification or limit, that part moves into a record.

Full guide: [one record per topic](records.html#one-record-per-topic) and [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown).

</section>

<section class="card" id="records-and-pages">

## Records keep the contract for agents; pages explain it to people

<p class="bs-lead">Agents reach plain Markdown records through one thin router; a page explains current conclusions and links the records instead of reproducing them.</p>

<figure id="fig-records-and-pages">
<div class="bs-flow" role="img" aria-label="AGENTS.md is the one thin router: it names the project context and prerequisites and routes the remaining rules by action to plain Markdown records. A rendered page, made when a person asks for one, explains current conclusions from those records and links to them instead of reproducing them. Reading a route grants no permission to execute or publish.">
<div class="bs-node bs-orange"><span class="bs-label">Router</span><b><code>AGENTS.md</code></b><ul><li>Names the project context and prerequisites</li><li>Rules every task needs</li><li>Remaining rules routed by action</li></ul></div>
<div class="bs-arrow"><span>by action</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Records for agents</span><b>Plain Markdown</b><ul><li>Headings, tables and lists</li><li>Exact file references and evidence links</li><li>Contracts, readiness and chronology</li></ul></div>
<div class="bs-arrow"><span>explain</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Page for people · on request</span><b>Conclusions and decisions</b><ul><li>Current conclusions and accepted specifications</li><li>Demonstrated behavior with its evidence scope</li><li>Useful figures and the next decisions</li></ul></div>
<div class="bs-back"><span>×</span> A page links to records instead of reproducing them. Reading a route grants no permission to execute or publish.</div>
</div>
<figcaption><b>Figure 5.</b> Agents reach records through one router; people reach an explanation through pages that link back to the records. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 5](#fig-records-and-pages) shows two reading paths that meet at the records. The page sits downstream: it explains the records and does not own them. That is why contracts, handoff and resume state, readiness boards, bookkeeping and long run chronology stay in records, where an agent is routed to them, and why a topic page that grows a readiness board or a run diary has drifted toward agents. Its agent material then moves into records, and its human core stays a page.

A record is plain Markdown: headings, tables, lists, exact file references and evidence links, with no layout HTML. A diagram a record needs goes into its own file and is linked, and anchors other documents use are kept. A site may also render a whole record as a [registered source page](authoring.html#registered-source-pages); the Markdown file stays the only copy anyone edits.

<!-- fold: code Agent entrypoints: one router for two clients -->

An agent reads the orientation and the rules every task needs at the start; everything else is routed by action, each row naming a trigger and what to read before it. Codex reads the paths in `AGENTS.md`; Claude Code gets the same router through a bare, standalone `@AGENTS.md` line in `CLAUDE.md`. Inside backticks or a code fence, an import is plain text and imports nothing.

<!-- /fold -->

<!-- fold: dead-end When a removed page still has dated links -->

Removing a page from navigation or publication passes the deletion gate. Dated links to it, such as those in old worklog entries, keep resolving in one of two ways the owner chooses: a hidden stub with the former anchors, which also keeps the published address, or a later `worklog_links_checked_from` date, which stops lint checking the entries before it and lets the address go. Lint rejects a dated link that neither covers.

<!-- /fold -->

Full guide: [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown), [record format](records.html#format) and [agent entrypoints](documentation-system.html#agent-entrypoints-import-versus-point).

</section>

<section class="card" id="page-and-record-in-step">

## A page explains its record in its own words; a changed record names the pages to reread

<p class="bs-lead">Pages do not copy the record's wording, so lint connects them another way: a changed record section lists the pages that link to it.</p>

<figure id="fig-page-and-record">
<div class="bs-flow" role="img" aria-label="A section of a record is edited, for example Refactoring over compatibility in rules/engineering/code.md. Lint compares the record with the last commit and finds which sections changed. It then lists every page that links to a changed section, for example the Compatibility chapter on the Engineering page, as pages to reread.">
<div class="bs-node bs-teal"><span class="bs-label">1 · Edit</span><b>A record section changes</b><ul><li><code>rules/engineering/code.md</code></li><li>section: Refactoring over compatibility</li></ul></div>
<div class="bs-arrow"><span>lint</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Compare</span><b>Changed sections</b><ul><li>diff against the last commit</li><li>each changed line belongs to a heading</li></ul></div>
<div class="bs-arrow"><span>links</span></div>
<div class="bs-node bs-orange"><span class="bs-label">3 · Remind</span><b>Pages to reread</b><ul><li>every page linking that heading</li><li>a note, never a failure</li></ul></div>
</div>
<figcaption><b>Figure 6.</b> How a record change reaches the pages that explain it. This illustrative diagram contains no measured results.</figcaption>
</figure>

An explanation leads with the outcome, reorders and adds an example, so it cannot quote its record without getting worse, and two texts about one rule drift unless something connects them. [Figure 6](#fig-page-and-record) shows the connection: every chapter links the record section it explains, and lint follows those links backwards from the sections an edit touched. A link to a whole record is listed only when its opening text changes, which is why a chapter links its section rather than the file.

```text
NOTE: rules/engineering/code.md › Refactoring over compatibility changed.
      Pages that explain it — reread them:
        docs/topics/engineering-practices/index.md  (chapter: compatibility)
```

The listed page is updated in the same deliverable, after the record, without a new request; who does it depends on its size, as [Record first](#record-first) shows. `--since <rev>` compares with an older commit.

Numbers get a second reminder when a site sets `page_number_notes = true`, one setting for the whole site. Lint then lists every number in a page's prose that none of its linked records state. Each such number is stated in its record, shown as code when it is a literal value, or taken off the page. The note does not judge whether the record's number is right. The setting suits a site whose pages explain Markdown records, as this one does, and not a site whose pages report rounded or derived measurements, which need the project's own ledger check.

Full guide: [rendered pages are for people; records stay Markdown](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown).

</section>

<section class="card" id="changes-and-publishing">

## Every change passes its gate, lands whole and leaves an append-only trace

<p class="bs-lead">A deletion waits for the user's approval, a landing puts code, records, tests and its worklog entry in one commit, and the worklog only grows at the top.</p>

<figure id="fig-landing">
<div class="wp-fig wp-landing">
<div class="wp-gates"><span class="wp-tag">Gates first</span>
<div class="wp-gate"><b>Deletion</b><span>waits for the user's approval, with the material named</span></div>
<div class="wp-gate"><b>Requested review</b><span>is presented; work stops before adopting it</span></div>
</div>
<div class="wp-commit"><span class="wp-tag">One landing commit</span>
<ul class="wp-chips"><li>code</li><li>owning records</li><li>tests</li><li class="wp-hot">worklog entry</li></ul>
<span class="wp-note">generated output stays ignored</span>
</div>
<div class="wp-log"><span class="wp-tag"><code>worklog.md</code> · newest first</span>
<div class="wp-entry wp-new"><b>New entry, on top</b><span>what changed · why · measured effect with units · checks · commit</span></div>
<div class="wp-entry wp-probe"><code>probed &lt;subject&gt; → &lt;verdict&gt;, &lt;decisive reason&gt;, &lt;time spent&gt;</code></div>
<div class="wp-entry wp-old"><b>Older entries</b><span>never edited; links correct on their own date</span></div>
</div>
</div>
<figcaption><b>Figure 7.</b> One change from its gates to its worklog entry. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Documentation loses information in quiet ways: a deleted figure, a rewritten log entry, a fix whose reason sits in no commit. [Figure 7](#fig-landing) follows one change along its arrows. Nothing is deleted without the user's approval, documents, figures and content lines alike; the exceptions are scratch files and a finished probe script that a refactor deletes. A requested review or prototype is a gate of its own.

The worklog entry and the commit message say much the same, on purpose: the worklog reads without Git, survives squashed history and holds what no commit carries, such as probes and decisions that belong to no single commit. Both are written in the same step, so they agree. An entry written before its commit exists may say the landing commit assigns the hash; nobody goes back to fill it in. When later moves break links in old entries, a project sets [`worklog_links_checked_from`](resources.html#resource-closure-and-evidence) instead of rewriting them.

<!-- fold: code Marked statements and drafts below the page end -->

A page may show a project invariant as a marked statement: an unindented paragraph that starts with `**INVARIANT:**` for a constraint that must survive edits or `**DON'T-REDO:**` for a settled decision, followed by a blank line. The build renders it as a labelled card and `lint --registry` lists it. Inside a sentence, a list item or a quote the raw label would show, and inside a code span or fence it stays an example. The invariant itself lives in its owning record.

Drafts that belong to a topic may sit below a <code>&lt;!-- page-end --&gt;</code> marker, where nothing is rendered. Chronology still goes to the worklog and owed work still needs its `OPEN.md` route; notes that nothing leads to are not left there.

<!-- /fold -->

Publishing is a site matter: the built pages are reviewed on loopback first, as [Build a site](build-a-site.html#preview) shows, and only the project's chosen branch publishes, under the [publishing gate](publication.html#publishing-gate).

Full guide: [rules for changes and chronology](documentation-system.html#rules-for-changes-and-chronology).

</section>

<section class="card" id="honest-claims">

## Name each object once, and claim only what the evidence shows

<p class="bs-lead">One term per object on every surface, and each claim labelled by the evidence that supports it: a check proves the property it tested and nothing more.</p>

<figure id="fig-claim-scope">
<div class="wp-fig wp-claims">
<div class="wp-evidence"><span class="wp-tag">Evidence in hand</span><b>A visual check</b><span>the new interpolation's plotted curve looks smoother</span></div>
<ul class="wp-claimlist">
<li class="wp-yes"><b>Smoothness</b><em>shown, visual check</em></li>
<li><b>Visual fidelity</b><em>not measured</em></li>
<li><b>Input preservation</b><em>not measured</em></li>
<li><b>Correspondence with the source</b><em>not measured</em></li>
<li><b>Physical accuracy</b><em>not measured</em></li>
</ul>
<div class="wp-labels"><span class="wp-tag">Labelled apart</span><span>accepted future behavior</span><span>implemented behavior</span><span>CPU check</span><span>native or runtime observation</span></div>
</div>
<figcaption><b>Figure 8.</b> What one check supports, and what the claim must say it does not. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Two names for one object make a reader wonder whether there are two objects, so one term holds across prose, controls, legends, tables, figures and output, and a rename sweeps all of them. A project whose pages use simpler words than its records keeps one list of those terms in its development conventions, and a rename changes that list first.

A claim that outruns its evidence is worse. [Figure 8](#fig-claim-scope) takes one check and five kinds of claim that each need different evidence. The smoother curve supports smoothness only; the other four are written as not measured, with a supported bound where one exists. An estimate typed into the empty cell would read as a measurement, so it is never made. The four labels underneath are kept apart for the same reason: something decided is not implemented, and a local CPU test is not a runtime observation.

A decision is kept beside its reasons: why this instrument or default, and why the alternatives lost. When a person made it, the record also keeps the date, who decided, the person's words and the decision's known weakness, so a later reader can tell a choice from a measurement. A baseline cited for what ships measures what ships, and a retired one is labelled historical.

These rules sit in the records guide because a claim is first made in a record; a page that explains it makes the same claim and cannot claim more.

Full guide: [naming and honest claims](records.html#naming-and-honest-claims).

</section>

<section class="card" id="evidence">

## A measured number is current only with its full provenance

<p class="bs-lead">A number is quoted as current only while its source and conditions are recorded and still hold; a change to any of them sends it back to a rerun.</p>

<figure id="fig-provenance">
<div class="wp-fig wp-prov">
<div class="wp-number"><span class="wp-tag">A current measured claim</span>
<b class="wp-value">the number <small>and its unit</small></b>
<ul class="wp-chips"><li>source commit</li><li>exact command</li><li>runtime and environment</li><li>workload</li><li>units</li><li>baseline</li><li>method</li><li>scope</li></ul>
<span class="wp-note">links its raw result and limitations</span>
</div>
<div class="wp-stale"><span class="wp-tag">When an input changes</span>
<ol class="wp-steps"><li><b>Code, input data, method, workload or runtime</b> that affect it change</li><li><b>Rerun</b> before quoting it as current; a historical label does not cover changed inputs</li><li><b>The old record stays</b> with its date, runtime, inputs and scope</li></ol>
</div>
</div>
<figcaption><b>Figure 9.</b> What travels with a measured number, and what happens when its inputs change. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A number without its conditions cannot be checked, and a number whose inputs changed can look authoritative while no longer being true. [Figure 9](#fig-provenance) shows both halves of the rule: the items a current measured claim records, and the rerun a changed input forces. Configuration values, derivations and design arithmetic are not measurements; they cite their source and say what they are.

A new reading of saved results is a result too: a breakdown the record does not give, a count across settings, a pattern found while drawing a figure. Before a page shows it, the record that owns the results gets a dated addition with the reading, how it is computed and its scope, and says so when it reruns nothing.

<!-- fold: experiment What stays with the producing work -->

The work that produced a result keeps its protocol, failed attempts, changed settings, actual outcomes, the reviews actually performed and the uncertainty that matters. An experiment directory also keeps the producing code, inputs, full result tables, source pins and its run output: the raw data, summaries and logs a person needs to check a claim again, tracked before the experiment is reported complete. A claim that rests on output in an untracked folder is not measured. Keeping run output outside Git is the person's decision, asked with the size and the options. A source pin may stand for producing code under the conditions the guide lists. The page explains what these results establish; the worklog records the landing without copying tables.

<!-- /fold -->

<!-- fold: experiment Number ledgers for redesigns -->

A redesign restates numbers in new prose, redrawn figures and slides, and each restatement is a chance to change one by accident. A ledger records the source of every number a redesigned chapter shows, figure labels included, and evidence blocks kept word for word are locked. The project owns both and their checks; the kit's lint checks only that a slide face shows no number its chapter lacks. A presentation-only edit may reuse captured results after checking that identities, numbers and treatments are intact.

<!-- /fold -->

Full guide: [numbers and staleness](records.html#numbers-and-staleness). How a number is drawn on a page is in [Figures](#figures).

</section>

<section class="card" id="page-design">

## Each chapter carries one claim; the page's question sets their order

<p class="bs-lead">A chapter is one <code>##</code> section or card with one claim: its title states the takeaway, a one-sentence lead states the claim, and the evidence follows. The page as a whole answers one question of its reader.</p>

<figure id="fig-page-types">
<div class="wp-fig wp-types">
<div class="wp-type"><b>Design</b><em>How does this system, or this part, work?</em><ol><li>purpose</li><li>parts</li><li>one step from start to end</li><li>settings</li><li>how it was checked</li><li>limits</li></ol></div>
<div class="wp-type"><b>Method</b><em>How is this problem solved, and why this way?</em><ol><li>problem</li><li>formulation</li><li>solution</li><li>whether it worked</li><li>alternatives</li><li>limits</li></ol></div>
<div class="wp-type"><b>Specification</b><em>What is agreed, or what exists, item by item?</em><ol><li>scope</li><li>each item with its status or guarantee</li><li>origin and checks</li><li>what is left out</li></ol></div>
<div class="wp-type"><b>Investigation</b><em>What is the answer to this question?</em><ol><li>question</li><li>answer</li><li>what was run</li><li>evidence</li><li>limits</li><li>next step</li></ol></div>
<div class="wp-type"><b>Qualification</b><em>Is this system accepted against its bar?</em><ol><li>system and bar</li><li>status at a glance</li><li>verdict for each gate</li><li>exceptions</li><li>what remains</li></ol></div>
<div class="wp-type"><b>Related work</b><em>What did others do, and what does it mean for us?</em><ol><li>what the other work does</li><li>what matches ours</li><li>what it means for us</li><li>sources</li></ol></div>
</div>
<figcaption><b>Figure 10.</b> Six page types: the reader's question, and the default order of chapters that answers it. Drawn from the table in <a href="page-design.html#page-types">page types</a>.</figcaption>
</figure>

A heading that only names a topic, such as "Results", makes the reader search the chapter for its point, and a chapter with two purposes buries both. So each chapter answers a question, shows a construction or compares alternatives, and splits when its purpose changes. A chapter that would only repeat what another chapter or page shows gives its point to the one that owns the subject, and its anchor still leads there.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">A topic title</span><h3>Results</h3><p>The chapter opens with setup, walks through each measurement and says in its last sentence which option was kept.</p></div>
<div class="bs-part bs-green"><span class="bs-label">A takeaway title</span><h3>Option B is kept because it needs one fewer manual step</h3><p>The lead states the claim, the comparison figure follows, and the prose says what the figure shows and where the claim stops.</p></div>
</div>

[Figure 10](#fig-page-types) moves up one level. A page answers one question, and the question sets a default order of chapters. The order is a starting point: a part with nothing to say is left out, and the subject may reorder the rest. A page that needs two types is usually two pages. A project may name one of its pages as the reference for a type, or name its own type with one reference page; nothing checks a page's type. A page that supports a decision ends with an options table against stated criteria and a clear verdict.

A page starts with its first chapter. Text above it has no heading that states its point, and in the reader it opens the first chapter anyway; strict lint warns with its length, and the author moves it into a chapter or keeps it on purpose with `opening = "keep"` in the frontmatter. A page that explains how something works names the people who do it by role, one role word each; a name stays only where the page says who decided, approved or said something. Text and figures share a left edge, use the available width and render at 11 px or more, small labels included.

<!-- fold: dead-end Why homepages are not one shared template -->

Each project composes its own homepage: the order of information, the sections, the hero and the visual story. A research narrative and a navigation dashboard can look quite different and still use the kit, and the starter's homepage is an example. Navigation is the shared part: the same site tree on every page, so that moving from the homepage into a reader page does not feel like entering a different site.

<!-- /fold -->

Full guide: [page design](page-design.html#page-design), [page types](page-design.html#page-types), [project-owned homepages](page-design.html#project-owned-homepages) and, for the frontmatter, [authoring paths](authoring.html#authoring-paths).

</section>

<section class="card" id="build-sheets">

## Build-sheet blocks keep one meaning, and status never replaces evidence

<p class="bs-lead">Each shared block means the same on every page; a status board and a slide face point to evidence and never stand in for it.</p>

<div class="bs-board">
<div class="bs-row"><span class="bs-state bs-ok">Done</span><b>Work is finished</b><span>Status does not substitute for evidence; scope caveats stay beside their evidence.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Decided</span><b>A choice is made</b><span>Decided is not implemented.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Passed</span><b>A check passed</b><span>A local or CPU test is not a native runtime check.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Work remains</b><span>The Open row owns the remaining work; limits prose does not repeat it.</span></div>
<div class="bs-row"><span class="bs-state bs-off">Parked</span><b>Set aside</b><span>A Parked row includes its reopening condition.</span></div>
</div>

The board above is the real block, filled with what each of its five states means; it reports no project's status. Shared blocks help only if each means the same thing everywhere: a row reading "Decided" can be mistaken for shipped work, so the board says what each state does not prove. A page has one board. The other blocks, from the one-sentence `bs-lead` to flows, tiles and checks, are listed by purpose in [build-sheet pages](page-design.html#build-sheet-pages), with the rule that every row is filled: two, three or four items, or a fixed split for more.

<!-- fold: code Slide faces -->

A chapter may open with one 16:9 slide face, a summary that states its takeaway and shows it; the chapter below stays the complete source. Faces are added last and only on request: build the chapters, then ask the person, and add none without a yes. A face earns its place by its visual, drawn from the chapter's own figures and numbers and laid out for the shape of its finding. Boxes of text are not a visual, except the terms of a formula the chapter explains or a grid that compares options factor by factor; a chapter with nothing to show gets no face. No fact lives only on a face: lint warns about a number a face shows and its chapter does not. A review of existing faces sorts each into redraw or remove, redesign, or keep, with a reason. Examples are on [Build a site](build-a-site.html#figures-and-slides).

<!-- /fold -->

Full guide: [build-sheet pages](page-design.html#build-sheet-pages) and [slide faces](page-design.html#slide-faces).

</section>

<section class="card" id="explanations">

## Keep one visible story in order of understanding, with optional depth in typed folds

<p class="bs-lead">A reader can follow the complete argument and its verdict with every fold closed; a fold the author marks open shows depth that most readers of the chapter need.</p>

<figure id="fig-story">
<div class="bs-flow n2" role="img" aria-label="The visible Story holds the complete argument in order of understanding: purpose and prerequisites, ingredients and mechanism, examples, evidence and limits, comparison cases and verdict. Typed folds for math, experiment, code and dead-end add optional depth. A fold starts closed unless its author marks it open for depth most readers of the chapter need. Folds never hide a separate required argument.">
<div class="bs-node bs-teal"><span class="bs-label">Always visible</span><b>The Story</b><ul><li>Purpose and prerequisites</li><li>Ingredients and mechanism</li><li>Examples, evidence and limits</li><li>Comparison cases and verdict</li></ul></div>
<div class="bs-arrow"><span>go deeper</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Optional</span><b>Typed folds</b><ul><li><code>math</code>, <code>experiment</code>, <code>code</code>, <code>dead-end</code> (Alternatives)</li><li>closed by default</li><li><code>(open)</code>: depth most readers of the chapter need</li><li>a reader's own click is remembered</li></ul></div>
<div class="bs-back"><span>×</span> A fold never hides a separate required argument.</div>
</div>
<figcaption><b>Figure 11.</b> Optional depth branches from a complete visible argument. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

An explanation fails when the reader meets a number before the instrument that produced it, or a term before its definition, so the Story runs in order of understanding: purpose, prerequisites, ingredients, mechanism, examples, evidence and limits. It also fails when the decisive step hides in a section many readers never open. [Figure 11](#fig-story) shows the guard: the arrow goes one way, and the argument, its narrative figures, comparison cases and verdict stay readable with every fold closed.

A fold is chosen by narrative weight, not by element type: a table may carry the Story and a plot may be supporting detail. It starts closed. Writing `(open)` after its kind, as in `<!-- fold: math (open) Derivation -->`, starts it open, for depth that most readers of that chapter need. The reader's section options open every fold of one kind across the page, and a reader's own click on a fold is remembered until an option sets its kind again, as the [reader guide](reader.html#shared-reading-layout) describes. A fold's title is already its heading and is not repeated inside.

Each concept or formula is explained in one place and linked elsewhere, and a short scope label stays beside any evidence it changes the reading of. When detail moves into a record, the former page anchor stays on the summary that replaces it, and the summary links the record. A new kind of fold is added only for recurring content the four kinds cannot express, through a shared [kit change](reader.html#extending-reading-layers).

Full guide: [story and reading layers](explanations.html#story-and-reading-layers).

</section>

<section class="card" id="figures">

## Draw what can be drawn: every mechanism, spatial claim and measured comparison needs a visual

<p class="bs-lead">A chapter is not done until a mechanism has a diagram, a spatial claim a picture and a measured comparison, ranking or trend a plot; a single value or an exact lookup may stand in text or a table.</p>

<figure id="fig-forms">
<div class="wp-fig wp-forms">
<div class="wp-chooser">
<div class="wp-form"><svg viewBox="0 0 64 40" aria-hidden="true"><rect x="2" y="12" width="18" height="16" rx="3"/><rect x="44" y="12" width="18" height="16" rx="3"/><path d="M20 20h20M36 16l5 4-5 4"/></svg><b>Diagram</b><span>a mechanism, structure, ownership or flow</span></div>
<div class="wp-form"><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M4 34 L24 8 L44 30 L60 18"/><circle cx="24" cy="8" r="3"/><circle cx="44" cy="30" r="3"/></svg><b>Picture</b><span>a geometric or spatial claim</span></div>
<div class="wp-form wp-hot"><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M6 4v32h54"/><path d="M10 30 L24 22 L38 16 L54 8"/><circle cx="24" cy="22" r="2.5"/><circle cx="38" cy="16" r="2.5"/></svg><b>Plot</b><span>values compared, ranked or changing over a setting</span></div>
<div class="wp-form"><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M4 6h56M4 18h56M4 30h56M28 6v28"/></svg><b>Text or table</b><span>a single value or an exact lookup; a table may sit beside a figure</span></div>
</div>
<div class="wp-schematic"><span class="wp-tag">Numbers on a page · schematic, no data</span>
<svg viewBox="0 0 240 120" aria-hidden="true"><path class="wp-axis" d="M24 8v96h208"/><path class="wp-line" d="M40 88 L84 70 L128 52"/><circle cx="40" cy="88" r="4"/><circle cx="84" cy="70" r="4"/><circle cx="128" cy="52" r="4"/><circle class="wp-gap" cx="172" cy="36" r="9"/><path class="wp-dash" d="M128 52 L172 36"/></svg>
<ul class="wp-keys"><li><b>x</b> the setting that changes the value</li><li><b>y</b> in the unit of the claim</li><li><b class="wp-gapkey">○</b> not run, where its point would stand</li></ul>
</div>
</div>
<figcaption><b>Figure 12.</b> What the claim shows decides its form; a value that depends on a setting is drawn over that setting. This illustrative diagram is authored in the page source; the plot is a schematic and carries no data.</figcaption>
</figure>

Prose alone leaves each reader to build the picture, and different readers build different ones; a visual that only repeats the text has not earned its place either. The four tiles of [Figure 12](#fig-forms) show the choice: what the claim shows sets the form, and a table is for reading off single values, not for comparing them. Within that, aim for the most telling picture the claim allows, and vary the forms across a page; this page uses flows, a folder, panels, a matrix and a real excerpt.

The schematic beside them applies the same idea to numbers. A value shown at one setting alone hides how it depends on that setting, so it becomes a plot over the settings that change it. The axis stays in the unit of the claim: a claim about accuracy is not restated in seconds. A setting that has not run is named as not run in the place its result would take, and a result that carries no pass or fail says so in its heading.

A missing figure is work to do. The page author makes it from what exists, measured data for a plot, code and configuration for a flow, geometry for a picture, records its generator and inputs, and puts any number it computes into the record first. A claim stays without its figure only when nothing true can be drawn, and the completion report then says which figure is missing and what it would take. Invented data is never drawn, and a sketch never reads as a measurement; the schematic above has no numbers for that reason.

Every figure has a stable anchor, a numbered caption, a prose reference like the one above that links its number and says what to notice, a named source and useful alternative text; an image that only shows appearance gets a caption and no number. Chart labels stay at 11 px or more, controls are at least 44 px as touch targets, and nothing overflows the page at any width.

<!-- fold: experiment Comparisons, captures and live reports -->

Compared views share orientation, scale, framing and input cases, keep their zoom while switching and use one set of markers and colours; method names, not colours alone, carry identity. For independent changes, show the baseline, each change alone and their combination, beside an ablation table, and explain a zero effect honestly. Prefer scripted captures with their generator and inputs; an interactive screenshot states its commit, date and scenario and never supports a quantitative claim. A public report on a live experiment carries `ongoing = true` until its findings and limits are settled.

<!-- /fold -->

<!-- fold: code Generated figures, palettes and colour meanings -->

A generated figure names its generator and input data in a manifest or metadata; Git holds its revision, date and bytes. It takes its colours from the kit's figure palettes and is written in a dark file for pages and a light file for slides and print. A project whose figures give a colour a meaning keeps those meanings in one table in its development conventions, and a new meaning gets its row before its first figure. Flows written in the page source, like the figures here, count as local diagrams: the page source is their generator, and their layout passes the same overflow review. A figure left unreferenced on purpose carries a source comment beside it:

```html
<!-- unreferenced figure: reason -->
```

<!-- /fold -->

Full guide: [figures and comparisons](figures.html#figures-and-comparisons), [interaction and access](figures.html#interaction-and-access), [run visuals and experiment lifecycle](figures.html#run-visuals-and-experiment-lifecycle) and, for numbers, [page design](page-design.html#page-design).

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
<figcaption><b>Figure 13.</b> The Math layer walks from marks on the Story's picture to the equation and a worked example. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A formula with undefined symbols asks the reader to trust it rather than follow it, and a formula plot unconnected to the Story adds a second picture to decode. [Figure 13](#fig-math) shows the alternative: the equation is reached through marks on the picture the reader already has, then worked with the Story's own inputs. Along the way, symbols, units and prerequisites are defined before use, intermediate steps such as a chain rule are shown, and local conditions are kept apart from global validity. A non-obvious formula gets its derivation or a precise citation of the section that derives it; a claim about an analytic derivative or Jacobian names its numerical tolerance and the self-test that checked it.

<!-- fold: math KaTeX syntax and the formula check -->

With `math = true` in the frontmatter, write `$…$` and `$$…$$` in Markdown and `\(…\)` inside raw HTML. The kit renders with its bundled KaTeX, fetches nothing, and lint compiles every formula of the built pages, naming each one that would show as raw text. A long expression wraps or scrolls in its own box; the type is never shrunk until it is hard to read.

<!-- /fold -->

Full guide: [mathematical explanation](math.html#mathematical-explanation) and the [formula check](authoring.html#formula-check).

</section>

<section class="card" id="code-excerpts">

## Excerpt only real code, and draw code diagrams with shared meanings

<p class="bs-lead">A snippet shows real repository lines with source metadata that drift checks verify; a diagram's boxes, edges and dashes mean the same on every page.</p>

<figure id="fig-excerpt">

```python source=tooling/build.py#L96-L103
# `<!-- fold: math (open) The route-level problem -->` makes the fold start open.
# Types drive the color + the reader's "Also show" options (fold-controls.js).
FOLD_TYPES = ("math", "experiment", "code", "dead-end")
# The markers match to the end of their own line only. Matching further would
# swallow the blank line after a closing marker, and Markdown would then read
# the next paragraph as part of the HTML block and show it as raw text.
_FOLD_OPEN_RE = re.compile(
    r"^<!--\s*fold:\s*(" + "|".join(FOLD_TYPES) + r")\s+(\(open\)\s+)?(.+?)\s*-->[ \t]*$", re.M)
```

<div class="wp-legend">
<span><svg viewBox="0 0 40 20" aria-hidden="true"><rect x="2" y="3" width="36" height="14" rx="3"/></svg>a box is a named component</span>
<span><svg viewBox="0 0 40 20" aria-hidden="true"><path d="M2 10h30M28 5l7 5-7 5"/></svg>a solid edge is ownership, a call or data flow</span>
<span><svg viewBox="0 0 40 20" aria-hidden="true"><path class="wp-dash" d="M2 10h30"/><path d="M28 5l7 5-7 5"/></svg>a dashed edge is a documented optional path</span>
</div>
<figcaption><b>Figure 14.</b> A real excerpt from the kit's builder, where the four fold kinds of <a href="#fig-story">Figure 11</a> and the open marker are defined, and the shared meanings of a code diagram. The excerpt is checked against <code>tooling/build.py</code> on every lint.</figcaption>
</figure>

Code on a page can go stale silently: the file changes and the excerpt does not. Idealized pseudocode shown as an excerpt is worse, because it looks verified. [Figure 14](#fig-excerpt) is the remedy at work: eight real lines, usually a signature and 3–10 decisive ones, tagged with their source range so lint fails if they drift, shown with the shared chrome: the real line numbers, a source chip, a language badge and a copy button. A snippet earns its place only when it explains a seam or a difficult contract better than prose, here the exact fold kinds the builder accepts.

Diagrams come from data or explicit local source and pass an overflow and collision check. Their parts keep the meanings in the legend of Figure 14 on every page, with a legend and a named source in the caption. Numbered sequence steps, mode views over common data and generated quantitative SVGs are useful patterns.

<!-- fold: dead-end Interactive diagram controls not yet built -->

Pan, fullscreen and annotation controls exist and may be used. Edge highlighting, drill-down and semantic zoom are only planned, so no page describes them as working. If one is built, drill-down with a breadcrumb suits independent child diagrams, and semantic zoom suits a diagram whose context must stay visible.

<!-- /fold -->

Full guide: [code and diagrams](code-excerpts.html#code-and-diagrams).

</section>
