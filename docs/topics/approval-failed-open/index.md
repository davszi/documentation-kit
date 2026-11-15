+++
title = "Approval that failed open"
brand_sub = "a measured case · ADP · why several kit rules exist"
description = "How supporting code piled up in the project the kit was extracted from: agents wrote more than one person can read, approval let work through, and nothing added up the total. Measured from Git, with the developer's own words and the kit rules that answer each pile."
components = ["toc", "nav", "filelinks", "lightbox"]
page_css = ["build-sheet.css", "approval-failed-open/approval-failed-open.css"]
toc = [["Result", "#result"], ["Timeline", "#timeline"], ["The piles", "#piles"], ["Why", "#why"], ["Cleanup", "#cleanup"], ["Kit changes", "#kit"], ["Early signs", "#early"], ["Not solved", "#open"]]
+++

# Approval that failed open

<section class="card" id="result">

## Agents wrote more than one person could read, and approval let the pile through

<p class="bs-lead">ADP's approval step existed but failed open: the developer said yes to proposals he had not read in full, work went ahead, nothing was removed and nobody added up the total, until supporting code was three times the product.</p>

<ul class="afo-kinds" aria-label="Three kinds of statement on this page">
<li class="afo-measured"><b>Measured</b>counted from ADP's Git history, <code>main</code> at <code>b8b80e0b</code>, on 2026-11-15</li>
<li class="afo-said"><b>The developer</b>his own words, as he wrote them</li>
<li class="afo-reading"><b>Interpretation</b>a reading that may be wrong</li>
</ul>

<!-- include: fragments/approval-failed-open/fig-scale.html -->

<div class="bs-stats">
<div><b>354,333</b><span>words of plans, worklog and notes in 47 days</span></div>
<div><b>269,241</b><span>lines of supporting Python at the peak, 2026-11-10</span></div>
<div><b>145,353</b><span>lines deleted by the cleanup</span></div>
<div><b>132,638</b><span>lines of run harnesses still in the repository</span></div>
</div>

ADP is the project this kit was extracted from. "The developer" owns ADP and the kit; "agents" are the AI sessions that did the work. <a href="#fig-scale">Figure 1</a> shows the result on three days: on 1 October supporting code was 7,976 lines against 40,254 lines of product; at the peak it was three times the product; after the cleanup it is still 2.74 times. Each step was reasonable on its own. The page explains how that happened, so that people in other projects can see the same pattern early. It blames nobody.

The [record](../topics/approval-failed-open/approval-failed-open.md) holds the exact wording, [background](../topics/approval-failed-open/background.md) the long form, and [numbers](../topics/approval-failed-open/numbers.md) the source of every number on this page.

</section>

<section class="card" id="timeline">

## Supporting code passed the product within two weeks and only grew until the cleanup

<p class="bs-lead">The words came first, the code followed, and the total had no downward step until 2026-11-11.</p>

<!-- include: fragments/approval-failed-open/fig-pileup.html -->

<div class="afo-kind afo-measured"><span class="afo-tag">Measured</span>
<p>Notice three things in <a href="#fig-pileup">Figure 2</a>. The product grows too, from 40,254 to 90,261 lines, but the stack passes it on 2026-10-11, two weeks after the first qualification code (turning point 1). The words panel peaks before most of the code was written: 42,773 words on 09-24 and 09-25, and 51,556 on 10-08 alone. And after the cleanup the stack is still almost as high: it is 8.2 % below its peak.</p>
</div>

<!-- fold: experiment The eight turning points -->

| # | Date | What happened (measured) |
|---|---|---|
| 1 | 2026-09-27 | First qualification code: supporting code 832 → 7,976 lines, after 42,773 words of plans on 09-24 and 09-25. |
| 2 | 2026-10-05 | One commit adds 22,378 run-output files, 1.59 GB. |
| 3 | 2026-10-08 | The per-question harness pattern appears. Largest day of writing: 51,556 words. |
| 4 | 2026-10-17 | Plans, 15,785 lines the day before, move into frozen copies. |
| 5 | 2026-10-28 | The attended-session recorder. |
| 6 | 2026-11-04 – 11-05 | Attended parts and the resource slot and pool land. ADP adopts the kit. |
| 7 | 2026-11-10 | Peak: 269,241 lines. The first of 34 net-removal commits. |
| 8 | 2026-11-15 | Attended evidence retired. Supporting code: 247,082 lines. |

Code means Python files only, and a day is the day a commit reached `main`. [The record's timeline](../topics/approval-failed-open/approval-failed-open.md#timeline) has these rows; [background](../topics/approval-failed-open/background.md#timeline) adds the dates between them and the limits of the measurement.

<!-- /fold -->

</section>

<section class="card" id="piles">

## The cleanup took the documents; the two largest code piles are still there

<p class="bs-lead">Attended evidence is retired and the frozen copies are deleted; the per-question run harnesses and the other qualification code, 132,638 and 101,630 lines, are still in the repository.</p>

<!-- include: fragments/approval-failed-open/fig-piles.html -->

<a href="#fig-piles">Figure 3</a> puts each pile's peak beside its size today. The two longest bars are filled to the end: the cleanup removed 14 harness lines. Attended evidence fell to 4,588 lines, parked for a later run journal. The frozen copies and the evidence store, 92,813 lines, were deleted on 2026-11-11. Run output in Git barely moved: 6.25 GB in 83,428 files.

One pile is not drawn: agents used a branch and a worktree for every task, also when they worked alone. Git keeps no record of deleted branches, so it was not measured.

<!-- fold: experiment What each pile was -->

| Pile | What it was | Peak | Today |
|---|---|---|---|
| Per-question run harnesses | A probe, run, supervision and review module, with tests, for every question | 132,652 lines, 480 files (11-05) | 132,638 lines, still there |
| Other qualification code | Probes, plots, preview app, runtime environment | 101,630 lines (11-15) | 101,630 lines, still there |
| Attended evidence | Prepares, launches, records and judges a session in which the developer clicks | 25,330 lines, 48 files (11-13) | Retired; 4,588 lines parked |
| Frozen copies and evidence store | Byte-exact copies of finished plans, 53 manifest entries, a path translator; a central evidence store | 6,225 lines in 42 copies (11-09); store 92,813 lines | Deleted 11-11 |
| Plans that never ended | `docs/open/` | 15,785 lines, 76 files (10-16) | 5,202 lines, 21 files |
| Run output in Git | Whole run folders, source copies included | 6.26 GB (11-12) | 6.25 GB, 83,428 files, still there |
| Resource slot and pool | A memory-capped slot, a native pool, an older slot and a usage cache | 8,151 lines (11-05) | 8,063 lines; older slot and cache use removed 11-15 |

[The piles](../topics/approval-failed-open/approval-failed-open.md#the-piles) in the record; each one in detail, with what it bought, in [background](../topics/approval-failed-open/background.md#the-piles).

<!-- /fold -->

</section>

<section class="card" id="why">

## Approval depended on reading, and the reading could not keep up

<p class="bs-lead">Four causes worked together: more text than one person can read, yes without reading, a general need solved inside one experiment, and no running total.</p>

<!-- include: fragments/approval-failed-open/fig-gate.html -->

<a href="#fig-gate">Figure 4</a> is the mechanism as this page reads it: an approval step that needs reading should slow work when the text grows; this one let work through.

### More text than one person can read

<div class="afo-kind afo-measured"><span class="afo-tag">Measured</span><p>In the 47 days from 2026-09-24 to 2026-11-09 agents added 354,333 words to plans, the worklog and session notes: 7,539 words per calendar day.</p></div>

<blockquote class="afo-kind afo-said"><span class="afo-tag">The developer</span><p>we can also clearly say that I didnt maange to read all the agents proposals cuz its too mcuh for a human and they ended up building this mess under mynose</p></blockquote>

<div class="afo-kind afo-reading"><span class="afo-tag">Interpretation</span><p>Approval depended on reading, so when the text outgrew reading, the step let work through.</p></div>

### Yes without reading

<blockquote class="afo-kind afo-said"><span class="afo-tag">The developer</span><p>i most probably said yes without seeing or understanding it all</p></blockquote>

<!-- include: fragments/approval-failed-open/fig-approvals.html -->

<div class="afo-kind afo-measured"><span class="afo-tag">Measured</span><p><a href="#fig-approvals">Figure 5</a>, first half: the build-up's records carry 181 approval statements, 177 of them about "the user", "owner" or "human", yet only 3 of 499 commit messages cite a decision; in the cleanup, 80 of 125 do. Second half: for six builds, the search found no approval in Git within seven days before the first file. The exception is the attended parts ("lets build it now fully", 11-02).</p></div>

<div class="afo-kind afo-reading"><span class="afo-tag">Interpretation</span><p>Records and memory differ, and Git cannot settle it. Agents wrote the approval statements, approvals given in chat are not in Git, and Git does not show what the developer read.</p></div>

### A general need solved inside one experiment

<blockquote class="afo-kind afo-said"><span class="afo-tag">The developer</span><p>i think another failure is that we build something for a single experiment instead of looking for the big picture</p></blockquote>

<div class="afo-kind afo-measured"><span class="afo-tag">Measured</span><p>Every question got its own harness modules, 480 files by 2026-11-05.</p></div>

<div class="afo-kind afo-reading"><span class="afo-tag">Interpretation</span><p>A need met once was met again, because nothing showed it had been met before.</p></div>

### Nothing removed, no total

<div class="afo-kind afo-measured"><span class="afo-tag">Measured</span><p>The supporting code total did not fall on any day before 2026-11-11.</p></div>

<div class="afo-kind afo-reading"><span class="afo-tag">Interpretation</span><p>Each addition answered a real problem of its day, and no record showed the running total that would make someone ask whether the whole was worth its cost.</p></div>

<!-- fold: experiment The kit spread some of the habits -->

The kit was extracted from ADP on 2026-11-04 and carried some habits as shared rules and tools. Measured in the kit's history: its first commit had a rule for frozen records, replaced on 2026-11-11; three adapter hooks let old copies pass the link check, and a second project came to use two of them; a number-ledger tool that no project imported lived from 2026-11-06 to 11-09; and a fixed slide-face arrangement drawn from one deck lasted from 2026-11-12 to 11-14, met by none of 36 faces on another project. The same pattern, one project's solution written down as a rule for every project, ran inside the kit. [Why it happened](../topics/approval-failed-open/approval-failed-open.md#why-it-happened) in the record.

<!-- /fold -->

</section>

<section class="card" id="cleanup">

## The cleanup deleted 145,353 lines, but supporting code fell only 8.2 %

<p class="bs-lead">Most deleted lines were documents and generated lists; the largest code piles stayed.</p>

<!-- include: fragments/approval-failed-open/fig-cleanup.html -->

<div class="bs-stats">
<div><b>125</b><span>commits from 2026-11-10 to 11-15, on 6 days</span></div>
<div><b>40,447</b><span>more words written by agents in those 6 cleanup days</span></div>
<div><b>325 MB</b><span>of run output stored during the cleanup</span></div>
<div><b>243,416</b><span>lines deleted by 40 net-removal commits from 2026-11-04</span></div>
</div>

<a href="#fig-cleanup">Figure 6</a> sets the deletions beside the fall of the supporting code on one scale. The evidence store alone was 92,813 of the 145,353 deleted lines. This is from Git only; the developer's hours were not recorded, and "two weeks" is his account. Building and cleanup overlapped from 2026-11-04, when ADP adopted the kit, until 11-09. Run output even grew: one cleanup commit stored 325 MB more, on the developer's word ("Yes, store it"). [What the cleanup took](../topics/approval-failed-open/approval-failed-open.md#what-the-cleanup-took) in the record.

</section>

<section class="card" id="kit">

## Each pile now has a kit rule that answers it

<p class="bs-lead">The rules were written between 2026-11-11 and 2026-11-15; whether they change what agents build has not been observed yet.</p>

<figure id="fig-kit-rules">
<div class="scroll afo-matrix" role="region" aria-label="Kit rules against the piles they answer" tabindex="0" data-reader-horizontal>
<table>
<thead><tr><th scope="col">Kit rule</th><th scope="col">Run harnesses</th><th scope="col">Other qualification code</th><th scope="col">Attended evidence</th><th scope="col">Frozen copies, evidence store</th><th scope="col">Plans never ended</th><th scope="col">Run output in Git</th><th scope="col">Slot and pool</th><th scope="col">Branch per task</th></tr></thead>
<tbody>
<tr><th scope="row"><a href="code-practices.html#name-the-need-first">Name the need first</a></th><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td></tr>
<tr><th scope="row"><a href="code-practices.html#the-capability-map">The capability map</a></th><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><th scope="row"><a href="code-practices.html#where-code-lives">Where code lives</a></th><td class="on">●<span class="afo-sr"> answers</span></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td><td></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td></tr>
<tr><th scope="row"><a href="experiment-workflow.html#step-back-across-experiments">Step back across experiments</a></th><td class="on">●<span class="afo-sr"> answers</span></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><th scope="row"><a href="experiment-workflow.html#show-the-total">Show the total</a></th><td></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><th scope="row"><a href="records.html#finished-working-documents">Finished working documents</a></th><td></td><td></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td><td></td></tr>
<tr><th scope="row"><a href="records.html#numbers-and-staleness">Numbers and staleness</a></th><td></td><td></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td><td></td><td></td></tr>
<tr><th scope="row"><a href="delivery.html#parallel-work">Parallel work</a></th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td class="on">●<span class="afo-sr"> answers</span></td></tr>
</tbody>
</table>
</div>
<figcaption><b>Figure 7.</b> Which rule answers which pile, as the record and its background name them. Read a column to see which rules now apply to a pile; read a row to see why a rule exists.</figcaption>
</figure>

<a href="#fig-kit-rules">Figure 7</a> maps the rules to the piles. A finished plan is deleted and cited from Git instead of frozen. Run output that a stated number rests on is kept, and a source pin replaces copies of the source. Before building supporting code, an agent writes the need without the experiment, looks it up in the capability map and brings the person the options. Each attempt shows the running total, and after every third experiment someone reads the whole again. Work done alone stays in the checkout. One more rule answers no single pile: [reporting completion](handoffs.html#reporting-completion) now asks for full paths in reports. [What changed in the kit](../topics/approval-failed-open/approval-failed-open.md#what-changed-in-the-kit) in the record.

</section>

<section class="card" id="early">

## Five signs showed the pattern before anyone counted the total

<p class="bs-lead">All five appeared in ADP during the build-up, before the cleanup began on 2026-11-10.</p>

<div class="afo-kind afo-reading"><span class="afo-tag">Interpretation</span><p>Read from ADP's timeline. The values under each sign are measured.</p></div>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-wait">plans</span><h3>Plans grow by thousands of words a day for weeks</h3><p>In ADP: 7,539 words per calendar day for 47 days.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">approvals</span><h3>Approvals are labels or one-word answers, and commits do not cite them</h3><p>In ADP: 177 of 181 statements say "the user", "owner" or "human"; 3 of 499 commit messages cite a decision.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">total</span><h3>Supporting code passes the product, and no record states its total</h3><p>In ADP: passed on 2026-10-11, three times the product at the peak.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">reuse</span><h3>A second experiment builds its own harness instead of reusing one</h3><p>In ADP: 480 harness files by 2026-11-05.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">copies</span><h3>A finished plan is frozen instead of deleted, and tools appear to keep the copies working</h3><p>In ADP: 53 manifest entries and a path translator.</p></div>
</div>

[Recognising it early](../topics/approval-failed-open/approval-failed-open.md#recognising-it-early) in the record.

</section>

<section class="card" id="open">

## The largest piles, the new rules and two ideas about approval remain open

<p class="bs-lead">The largest piles are still in ADP, nobody has seen the new rules at work yet, and the two ideas about approval are questions, not rules.</p>

<div class="bs-board">
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Code still in ADP</b><span>The run harnesses, 132,638 lines; the other qualification code, 101,630; 8,063 lines of pool code.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Run output in Git</b><span>6.25 GB in 83,428 files. The rule narrows what is kept; it does not shrink this pile by itself.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Whether the new rules work</b><span>Nobody has yet observed whether they change what agents build.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Two ideas, not rules</b><span>An approval covers only what the ask itself said; an ask states the size of what it would build. Both are <a href="../open/approval-scope-and-ask-size.md">questions for the developer</a>.</span></div>
</div>

<div class="bs-grid g2">
<div class="bs-part bs-muted"><span class="bs-label">Not known</span><ul>
<li>The developer's hours were never recorded. The 18 attended sessions ran 13,640.3 s in total; that is their run time, not his time.</li>
<li>The approval search reads keywords; a hand check found 24 of 25 matches to be real approvals. Approvals given in chat are not in Git.</li>
</ul></div>

<div class="bs-part bs-green"><span class="bs-label">What worked</span><ul>
<li>The core of the resource slot, a memory-capped user scope, stays ADP's supported way to run checks and recorded successful runs.</li>
<li>Three attended sessions passed their smaller question.</li>
<li>The cleanup recorded its decisions in 80 of 125 commit messages.</li>
</ul></div>
</div>

[Not solved or not known](../topics/approval-failed-open/approval-failed-open.md#not-solved-or-not-known) and [what worked](../topics/approval-failed-open/approval-failed-open.md#what-worked) in the record.

</section>
