+++
title = "Global agent instructions"
brand_sub = "your global file · the owner's copy · add or replace"
description = "What a person's global agent file sets that no project rule can, what the kit owner's copy of his file holds, how to take it into your own and where it needs your edits."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css", "../site/assets/global-instructions.css"]
toc = [["Two layers", "#two-layers"], ["What it holds", "#what-it-holds"], ["One instruction", "#one-instruction"], ["Take it", "#take-it"], ["Limits", "#limits"]]
+++

# Global agent instructions

<section class="card" id="two-layers">

## Your global file sets how an agent works with you; the project sets what it does there

<p class="bs-lead">Every agent session reads two layers: your own global file, in every project on your machine, and the project's router with the kit's rules, only in that project. How an agent reports to you, asks you and checks a claim belongs to the first layer, and no project rule can set it for you.</p>

<figure id="fig-two-layers">
<div class="ga-layers" role="img" aria-label="One person's machine. At the top, the person layer: the global file, read from ~/.codex/AGENTS.md by Codex and from ~/.claude/CLAUDE.md by Claude Code, owned by the person alone and read at the start of every session in every project. Its example line: Commit autonomously at coherent deliverable boundaries unless I have asked to hold commits. Arrows lead from it into two projects, vehicle-sim and thesis. Each project has its own layer: an AGENTS.md router and the kit's rules under .docs-kit/rules, read only in that project and shared by everyone who works on it. In vehicle-sim, the router row for staging, committing or rewriting Git history points to .docs-kit/rules/engineering/git.md, whose example line is: Use a short imperative subject and an explanatory body. Nothing in one project reaches the other. At the bottom, one commit in vehicle-sim as the agent holds it: when to commit comes from the person's file, how the message reads comes from the project's rule.">
<div class="ga-machine"><b>one person's machine</b><span>two layers in every agent session</span></div>
<div class="ga-band ga-person-tone">
<div class="ga-band-head"><span class="ga-tag">Person layer · how the agent works with you</span><span class="ga-scope">read in every project · owned by you alone</span></div>
<div class="ga-person-body">
<div><span class="ga-k">Loaded from your home folder</span><div class="ga-files">
<div class="ga-file"><code>~/.codex/AGENTS.md</code><span>read by Codex</span></div>
<div class="ga-file"><code>~/.claude/CLAUDE.md</code><span>read by Claude Code</span></div>
</div></div>
<blockquote class="ga-quote"><p>Commit autonomously at coherent deliverable boundaries unless I have asked to hold commits</p><cite>the owner's global file · Commit preferences</cite></blockquote>
</div>
</div>
<div class="ga-rail" aria-hidden="true"><span><b>read here</b></span><span><b>and here</b></span></div>
<div class="ga-projects">
<div class="ga-band ga-project-tone">
<div class="ga-band-head"><span class="ga-tag">Project layer · <code>vehicle-sim/</code></span><span class="ga-scope">read only here · shared by everyone on it</span></div>
<ul class="ga-tree">
<li><code>AGENTS.md</code><span>router: which rule to read before which action</span></li>
<li><code>.docs-kit/rules/</code><span>the kit's rules, at the project's pin</span></li>
</ul>
<div class="ga-route"><p><b>Before</b>Staging, committing or rewriting Git history</p><p><b>Read</b><code>.docs-kit/<wbr>rules/<wbr>engineering/<wbr>git.md</code></p></div>
<blockquote class="ga-quote"><p>Use a short imperative subject and an explanatory body</p><cite>kit rule · git.md, Commit messages</cite></blockquote>
</div>
<div class="ga-band ga-project-tone ga-other">
<div class="ga-band-head"><span class="ga-tag">Project layer · <code>thesis/</code></span><span class="ga-scope">read only here</span></div>
<ul class="ga-tree">
<li><code>AGENTS.md</code><span>its own router, its own rows</span></li>
<li><code>.docs-kit/rules/</code><span>the same kit, at its own pin</span></li>
</ul>
<p class="ga-note">Nothing in <code>thesis/</code> reaches <code>vehicle-sim/</code>, and nothing in <code>vehicle-sim/</code> reaches here. Only the person layer is read in both.</p>
</div>
</div>
<div class="ga-join" aria-hidden="true"><span></span><span></span></div>
<div class="ga-session">
<span class="ga-k">One commit in vehicle-sim/, as the agent holds it</span>
<ol>
<li class="ga-person-tone"><b>When to commit</b><span>at the end of a finished deliverable, unless you asked it to hold</span><i>from your global file</i></li>
<li class="ga-project-tone"><b>How the message reads</b><span>a short imperative subject and a body that explains</span><i>from the project's kit rule</i></li>
</ol>
</div>
</div>
<figcaption><b>Figure 1.</b> The two layers of instructions an agent session reads, and where each is loaded from. The project names <code>vehicle-sim/</code> and <code>thesis/</code> are invented examples. The two quoted lines are real: the first from the owner's global file, the second from the kit's <a href="git.html#commit-messages">commit messages</a> rule; the router row is the starter's. This diagram contains no measured results.</figcaption>
</figure>

[Figure 1](#fig-two-layers) follows one commit. The project's layer is its `AGENTS.md` router and the kit's rules it routes to: before a commit, the router sends the agent to the kit's Git guide, which says how the message reads. That layer lives in the project's repository, so everyone who works on the project gets the same rules, and it is read only there.

The person's layer is one file on your machine: Codex reads `~/.codex/AGENTS.md` and Claude Code reads `~/.claude/CLAUDE.md`. The agent reads it at the start of every session, in every project, before any project file. It holds what is about you rather than about the project: when the agent may commit without asking, how it reports, when it hands work to another agent, how it puts a decision to you, how it checks a claim and what it never does without your yes.

A project rule cannot carry that layer. Every contributor reads the project's rules, so they cannot say how one person wants to be asked; and they stop at the project's folder, so a habit set there is gone in the next project. The kit's owner keeps his habits in his global file, and the kit ships a copy of it, with personal details removed, for anyone who wants to start from it.

<a class="ga-full" href="global-agent-instructions-text.html"><span><b>The full text of the owner's file</b><span>Every section as the owner wrote it, with a button that copies the whole file.</span></span><i>Read and copy →</i></a>

</section>

<section class="card" id="what-it-holds">

## The copy holds habits for every project: gates, decisions, delegation, reports, commits and checks

<p class="bs-lead">Each section of the copy tells an agent how to act at one kind of moment. Grouped by what they do for you, they fall into six kinds and a remainder.</p>

<figure id="fig-sections">
<div class="ga-map" role="img" aria-label="The sections of the owner's file in seven groups, each with a real line from the file. Gates, checks at fixed moments: section Gates; line: Before saying something already exists: quote it with its location. Decisions with you: sections Decisions with me and Interaction preferences; line: Silence or continued discussion is not approval. Delegation: sections Models and delegation, to edit for your setup, and Delivery and coordination preference; line: Keep simple tasks inline. Reports: sections Caveman subagent reporting and Default response style, both to edit for your setup; line: Clearly distinguish verified facts, reasoned inferences and unchecked points. Commits: section Commit preferences; line: Authorization to commit does not by itself authorize pushing, merging or rewriting shared history. Checking and pushback: section Fact-checking and pushback; line: When evidence contradicts my claim, say so directly. The rest: sections Scope, Memory discipline, Usage-efficient execution, Design preferences, Engineering preferences, Long-running jobs and shared resources, Compacting a long session, and Graphify and NVIDIA GPU driver changes, both to edit for your setup; line: Use agent memory only to resume unfinished work.">
<div class="ga-group ga-person-tone"><span class="ga-tag">Gates</span><h3>Checks at fixed moments</h3><p>Before visual work is called done, before a push, before a deletion and before claiming that something exists.</p><ul class="ga-heads"><li>Gates</li></ul><blockquote class="ga-quote"><p>Before saying something already exists: quote it with its location.</p><cite>Gates</cite></blockquote></div>
<div class="ga-group ga-person-tone"><span class="ga-tag">Decisions with you</span><h3>Explain, ask, wait for the yes</h3><p>How a question is put to you, and what does not count as your approval.</p><ul class="ga-heads"><li>Decisions with me</li><li>Interaction preferences</li></ul><blockquote class="ga-quote"><p>Silence or continued discussion is not approval.</p><cite>Interaction preferences</cite></blockquote></div>
<div class="ga-group ga-person-tone"><span class="ga-tag">Delegation</span><h3>When to hand work on, and to which model</h3><p>What another agent gets, and a ladder of models from mechanical counts to consequential reviews.</p><ul class="ga-heads"><li class="is-edit">Models and delegation</li><li>Delivery and coordination preference</li></ul><blockquote class="ga-quote"><p>Keep simple tasks inline.</p><cite>Models and delegation</cite></blockquote></div>
<div class="ga-group ga-person-tone"><span class="ga-tag">Reports</span><h3>What you are told, and how</h3><p>Short answers that keep every path, number and caveat, and the line between checked and assumed.</p><ul class="ga-heads"><li class="is-edit">Caveman subagent reporting</li><li class="is-edit">Default response style</li></ul><blockquote class="ga-quote"><p>Clearly distinguish verified facts, reasoned inferences and unchecked points.</p><cite>Caveman subagent reporting</cite></blockquote></div>
<div class="ga-group ga-person-tone"><span class="ga-tag">Commits</span><h3>Commit freely, push only when asked</h3><p>Your own Git identity, no tool credit lines, and commits at the end of a finished piece of work.</p><ul class="ga-heads"><li>Commit preferences</li></ul><blockquote class="ga-quote"><p>Authorization to commit does not by itself authorize pushing, merging or rewriting shared history.</p><cite>Commit preferences</cite></blockquote></div>
<div class="ga-group ga-person-tone"><span class="ga-tag">Checking and pushback</span><h3>Check claims, yours included</h3><p>Behaviour against code and runs, numbers against data, history against Git, and a plain answer when you are wrong.</p><ul class="ga-heads"><li>Fact-checking and pushback</li></ul><blockquote class="ga-quote"><p>When evidence contradicts my claim, say so directly.</p><cite>Fact-checking and pushback</cite></blockquote></div>
<div class="ga-group ga-person-tone"><span class="ga-tag">The rest</span><h3>Memory, context, pages, code and the machine</h3><p>Where a preference is kept, how much an agent reads, when it asks you to compact, how pages and code are made, and what to protect on the machine.</p><ul class="ga-heads"><li>Scope</li><li>Memory discipline</li><li>Usage-efficient execution</li><li>Design preferences (pages, artifacts, UI)</li><li>Engineering preferences</li><li>Long-running jobs and shared resources</li><li>Compacting a long session</li><li class="is-edit">Graphify</li><li class="is-edit">NVIDIA GPU driver changes</li></ul><blockquote class="ga-quote"><p>Use agent memory only to resume unfinished work.</p><cite>Memory discipline</cite></blockquote></div>
</div>
<div class="ga-legend" aria-hidden="true"><span>a section heading of the file</span><span class="is-edit">names the owner's tools or machine: edit it for your setup</span></div>
<figcaption><b>Figure 2.</b> Every section heading of the owner's file, grouped by what it does for you, with one line quoted from each group exactly as the file has it. The grouping is this page's; the file lists the sections in its own order. This diagram contains no measured results.</figcaption>
</figure>

[Figure 2](#fig-sections) sorts the file by what each part does for you. The quoted lines show its voice: short instructions in the first person, written by one person to the agents that work for him.

**Gates** come first in the file. [Gates](global-agent-instructions-text.html#gates) are checks at fixed moments: before calling visual work done, the agent opens the page at a narrow and a wide width and sends the capture it checked; before a push, it runs the repository's full checks on the final commit; before a deletion, it lists the exact paths and checks what Git or a record keeps; before saying that something already exists, it quotes it with its location.

**Decisions with you** cover how a question reaches you. [Decisions with me](global-agent-instructions-text.html#decisions-with-me) asks the agent to explain before asking, to put one decision in each question with the options, the measured cost of each and its recommendation, and to report the whole state rather than the change since the last message. [Interaction preferences](global-agent-instructions-text.html#interaction-preferences) says what is not approval, and that a request to "propose" or "draft" stops before anything is applied.

**Delegation** says when an agent hands work to another one and what it states when it does. [Models and delegation](global-agent-instructions-text.html#models-and-delegation) gives a ladder of models, from mechanical inventories to planning and security reviews; [Delivery and coordination preference](global-agent-instructions-text.html#delivery-and-coordination-preference) lets the agent that builds something also run its checks and write its documentation.

**Reports** are short and lead with the outcome, but keep every path, number, error and caveat. [Caveman subagent reporting](global-agent-instructions-text.html#caveman-subagent-reporting) and [Default response style](global-agent-instructions-text.html#default-response-style) set that voice through a plugin the owner uses.

**Commits** follow [Commit preferences](global-agent-instructions-text.html#commit-preferences): the agent commits on its own at the end of a finished piece of work, with your Git identity and no credit line for the tool, and a yes to commit is not a yes to push. **Checking and pushback**, in [Fact-checking and pushback](global-agent-instructions-text.html#fact-checking-and-pushback), asks the agent to check your claims as well as its own and to say so when the evidence contradicts you.

**The rest** keeps memory for unfinished work only, keeps reads and outputs small, has the agent ask you to compact a long session before a new task, which [the next chapter](#one-instruction) follows from problem to wording, asks for pages that lead with the result and for careful engineering, protects running jobs, and holds two sections about the owner's own tools and machine.

<a class="ga-full" href="global-agent-instructions-text.html"><span><b>Read every section in full</b><span>The registered source page shows the whole file and copies it with one button.</span></span><i>Full text →</i></a>

</section>

<section class="card" id="one-instruction">

## One instruction from problem to wording: ask to compact before a new task

<p class="bs-lead">The copy's newest section shows how a line gets into the file: a problem seen in a real session, evidence read together with its limits, and wording that says exactly when the agent acts and what it writes.</p>

<figure id="fig-compact">
<div class="ga-time" role="img" aria-label="Two lanes show how full a session's context is over time, while task A and then task B run. Illustrative values, not a measurement. In the first lane the harness decides: the context fills during task B, the window is full in the middle of it, and the harness compacts there; the detail task B had in flight is lost and the summary may carry a wrong fact. In the second lane the agent asks: task A is finished, task B arrives, the agent ends its message with Compact before I start? and the ready /compact command; the person compacts and writes go, and task B starts on a packed summary of the finished work and runs without reaching the full window.">
<div class="ga-lane is-harness"><span class="ga-tag">Today · the harness decides</span><h3>Compacted when the window is full</h3>
<div class="ga-plot"><div class="ga-axis" aria-hidden="true"><span>full</span><span>half</span><span>empty</span></div><div class="ga-cols">
<div class="ga-track is-a" style="grid-column:1"><i style="--h:8%"></i></div>
<div class="ga-track is-a" style="grid-column:2"><i style="--h:18%"></i></div>
<div class="ga-track is-a" style="grid-column:3"><i style="--h:30%"></i></div>
<div class="ga-track is-a" style="grid-column:4"><i style="--h:42%"></i></div>
<div class="ga-track is-a" style="grid-column:5"><i style="--h:55%"></i></div>
<div class="ga-track is-b" style="grid-column:6"><i style="--h:66%"></i></div>
<div class="ga-track is-b" style="grid-column:7"><i style="--h:78%"></i></div>
<div class="ga-track is-b" style="grid-column:8"><i style="--h:90%"></i></div>
<div class="ga-track is-full" style="grid-column:9"><i style="--h:100%"></i></div>
<div class="ga-track is-sum" style="grid-column:10"><i style="--h:22%;--s:73%"></i></div>
<div class="ga-track is-sum" style="grid-column:11"><i style="--h:34%;--s:47%"></i></div>
<div class="ga-track is-sum" style="grid-column:12"><i style="--h:46%;--s:35%"></i></div>
<div class="ga-cut" style="grid-column:10"></div>
<span class="ga-seg" style="grid-column:1 / 6">task A</span>
<span class="ga-seg is-b" style="grid-column:6 / 13">task B</span>
<p class="ga-event" style="grid-column:8 / 13"><b>Window full</b>The harness compacts in the middle of task B.</p>
</div></div><p class="ga-result"><b>Lost:</b> the detail task B had in flight; the summary may carry a wrong fact.</p></div>
<div class="ga-lane is-ask"><span class="ga-tag">The instruction · the agent asks</span><h3>Compacted before the new task starts</h3>
<div class="ga-plot"><div class="ga-axis" aria-hidden="true"><span>full</span><span>half</span><span>empty</span></div><div class="ga-cols">
<div class="ga-track is-a" style="grid-column:1"><i style="--h:8%"></i></div>
<div class="ga-track is-a" style="grid-column:2"><i style="--h:18%"></i></div>
<div class="ga-track is-a" style="grid-column:3"><i style="--h:30%"></i></div>
<div class="ga-track is-a" style="grid-column:4"><i style="--h:42%"></i></div>
<div class="ga-track is-a" style="grid-column:5"><i style="--h:55%"></i></div>
<div class="ga-track is-packed" style="grid-column:6"><i style="--h:20%;--s:70%"></i></div>
<div class="ga-track is-packed" style="grid-column:7"><i style="--h:32%;--s:44%"></i></div>
<div class="ga-track is-packed" style="grid-column:8"><i style="--h:44%;--s:32%"></i></div>
<div class="ga-track is-packed" style="grid-column:9"><i style="--h:56%;--s:25%"></i></div>
<div class="ga-track is-packed" style="grid-column:10"><i style="--h:68%;--s:21%"></i></div>
<div class="ga-track is-packed" style="grid-column:11"><i style="--h:80%;--s:18%"></i></div>
<div class="ga-track is-packed" style="grid-column:12"><i style="--h:92%;--s:15%"></i></div>
<div class="ga-cut" style="grid-column:6"></div>
<span class="ga-seg" style="grid-column:1 / 6">task A</span>
<span class="ga-seg is-b" style="grid-column:6 / 13">task B</span>
<p class="ga-event" style="grid-column:4 / 9"><b>New task after a finished one</b><strong>Compact before I start?</strong> You type <code>/compact</code> with the note, then go.</p>
</div></div><p class="ga-result"><b>Kept:</b> task B starts on a packed summary of finished work and runs without a cut.</p></div>
<div class="ga-legend" aria-hidden="true"><span class="is-a">task A in the context</span><span class="is-b">task B in the context</span><span class="is-sum">packed summary</span><span class="is-cut">compaction</span><span class="is-full">window full</span></div>
</div>
<figcaption><b>Figure 4.</b> A session's context over time under the two ways of compacting. The heights are an illustration, not a measurement: they show where a compaction falls, not how often. Tasks A and B are invented examples.</figcaption>
</figure>

**The problem.** [Figure 4](#fig-compact) puts the two ways side by side. A harness compacts a session on its own when the context window fills, and that can fall in the middle of a task: the detail the task had in flight goes into a summary that nobody checks at that moment. In the owner's own session on the kit on 2026-11-27, the automatic summary carried two wrong facts about which kit version two projects were on: 3.2.1 where the pin was 5.6.1, and 5.0.0 where it was 5.7.0. Both were caught and corrected in the open. That is one session, an observation and not a study.

**The evidence, with its limits.** A preprint, [Letting Models Manage Their Own Context: Where We Stand](https://arxiv.org/abs/2611.34147) (NVIDIA, submitted 25 November 2026), reports in its abstract that models which decide when and what to compact reach higher accuracy, most at tight budgets; one model's score on OfficeQA Pro v2 rises from 21% to 56% at a 32K-token budget, and models differ widely in how they use the interface. Only the abstract was read. The paper tested a model compacting by itself, not an agent asking a person, and what was read does not establish a gain at large context budgets. It supports the direction, not the size of any effect here.

**The wording.** An agent in this harness cannot compact by itself: the person types `/compact`, with a note of what to keep if they want one. So the [instruction](global-agent-instructions-text.html#compacting-a-long-session) has the agent ask, at the one moment it can judge: when a new task arrives after a finished one. At the finish it cannot know whether a task follows. It asks only when the session is long, the earlier work is done and the new task does not need its detail; not before a quick answer, not for a follow-up to work in flight, and never from a subagent. The ask closes the message, so the person cannot miss it: a bold "Compact before I start?" and the ready `/compact` command, whose note names what to keep, repeats the new task and names every job and agent still running. Running work does not forbid the ask; the note carries it across. The person compacts and writes "go", or writes "go" alone, and the agent starts without asking again.

<div class="bs-grid g3">
<div class="bs-part bs-orange"><span class="bs-label">Weakness</span><h3>"Long" is a judgment</h3><p>The agent has no meter of how full its context is; it judges from the session it remembers.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">Weakness</span><h3>It waits for a word</h3><p>An agent cannot wait on a clock, so after the ask it stays stopped until the person writes.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">Weakness</span><h3>One word each time</h3><p>Every ask costs the person a reply, even when compacting turns out not to matter.</p></div>
</div>

The [worklog entry](../KIT_WORKLOG.md#2026-11-28--the-copy-renewed-with-compacting-a-long-session-and-a-chapter-on-it) records the decision, the owner's words, the observation and what was read of the paper.

</section>

<section class="card" id="take-it">

## You choose whether it goes into your file; a project only offers it

<p class="bs-lead">Add the copy below your own instructions, replace yours with it, or leave it out. The choice is yours, because the file steers every project on your machine.</p>

<figure id="fig-ways">
<div class="ga-ways" role="img" aria-label="Three ways to take the copy, and what each does to your global file, named target. Add: your own lines stay, a blank line follows, then the owner's copy. Replace: the old file is first kept as target.before-kit-snapshot, then target holds only the owner's copy; replace needs an existing file and does nothing while a kept old file is there. Neither: your file stays as it is; on your yes the agent adds the line Documentation kit global-context snapshot: declined, so that later sessions do not ask again.">
<div class="ga-way"><span class="ga-tag ga-person-tone">Add</span><h3>Below your own lines</h3><div class="ga-doc"><code>$target</code><ol><li class="is-yours">your own instructions, unchanged</li><li class="is-gap">blank line</li><li class="ga-person-tone">the owner's copy, whole</li></ol></div><p>The command only appends: where your lines and the copy say different things, both stay until you edit one.</p></div>
<div class="ga-way"><span class="ga-tag ga-person-tone">Replace</span><h3>The copy instead of yours</h3><div class="ga-doc"><code>$target.before-kit-snapshot</code><ol><li class="is-yours">your old file, kept</li></ol></div><div class="ga-down"><span>then</span></div><div class="ga-doc"><code>$target</code><ol><li class="ga-person-tone">the owner's copy only</li></ol></div><p>Needs an existing file, and does nothing while a kept old file is there.</p></div>
<div class="ga-way"><span class="ga-tag">Neither</span><h3>Your file stays as it is</h3><div class="ga-doc"><code>$target</code><ol><li class="is-yours">your own instructions, unchanged</li><li class="is-yours"><code>Documentation kit global-context snapshot: declined.</code></li></ol></div><p>The last line is added only on your yes; without it, a later session asks again.</p></div>
</div>
<figcaption><b>Figure 3.</b> What each way does to your global file, named <code>$target</code> as in the commands. Blue marks your own lines, violet the owner's copy. This diagram contains no measured results.</figcaption>
</figure>

[Figure 3](#fig-ways) shows the three ways. Set `target` to your global file first: `~/.codex/AGENTS.md` for Codex, `~/.claude/CLAUDE.md` for Claude Code. If that file only imports or links to another file, set `target` to that other file. Then run one of the two commands from the root of a project that pins the kit as `.docs-kit`:

```bash
{ printf '\n'; cat .docs-kit/docs/topics/global-agent-instructions/global-agent-instructions.md; } >> "$target"   # add
```

```bash
[ ! -e "$target.before-kit-snapshot" ] && cp "$target" "$target.before-kit-snapshot" && cp .docs-kit/docs/topics/global-agent-instructions/global-agent-instructions.md "$target"   # replace, keeping the old file
```

The [README](readme.html#optional-the-owners-global-agent-instructions) owns these two commands. The copy's first lines say what it is and which tools it assumes; read them, and the [full text](global-agent-instructions-text.html), before you choose.

A project does not choose for you. A project whose `AGENTS.md` asks for it, as the starter's router does, has its agent offer the copy once per session and write nothing to your global file without your yes. When the agent asks, what it shows you first and how a no is remembered are in the [README section](readme.html#optional-the-owners-global-agent-instructions).

</section>

<section class="card" id="limits">

## It is one person's way of working on one day, and parts of it fit only his setup

<p class="bs-lead">Take the copy as a starting point: it is optional, the kit never loads it, and the sections that name the owner's tools need your edit.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-off">whose</span><h3>One person's preferences</h3><p>The owner's habits with his agents, not a rule of the kit. Your project's rules do not depend on any of it.</p></div>
<div class="bs-check"><span class="bs-badge bs-off">when</span><h3>A copy of 2026-11-28</h3><p>The owner's file changes; the copy does not follow it until the kit renews it.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">optional</span><h3>Not loaded by the kit</h3><p>No build, check or router row reads it. It acts only once you put it in your own global file.</p></div>
</div>

<div class="bs-grid g2">
<div class="bs-part bs-orange"><span class="bs-label">Edit for your setup</span><h3>Sections that name the owner's tools</h3><ul>
<li><a href="global-agent-instructions-text.html#models-and-delegation">Models and delegation</a> names the models and effort levels the owner uses in Codex and Claude Code; replace them with yours.</li>
<li><a href="global-agent-instructions-text.html#caveman-subagent-reporting">Caveman subagent reporting</a> and <a href="global-agent-instructions-text.html#default-response-style">Default response style</a> assume the Caveman plugin.</li>
<li><a href="global-agent-instructions-text.html#graphify">Graphify</a> assumes the Graphify skill.</li>
<li><a href="global-agent-instructions-text.html#nvidia-gpu-driver-changes">NVIDIA GPU driver changes</a> protects the owner's machine; keep it only if yours needs the same protection.</li>
</ul></div>
<div class="bs-part bs-teal"><span class="bs-label">Fits any setup</span><h3>Sections you can take as they are</h3><ul>
<li>Gates, decisions with you, commits, and checking and pushback.</li>
<li>Delivery, reports in general, memory, usage, design and engineering habits.</li>
<li>Where a line says "me" or "I", it means you once the file is yours.</li>
</ul></div>
</div>

The copy is the owner's file of 2026-11-28, with personal details removed; its first lines name the tools it assumes. When the kit renews the copy, its release notes say so, as 5.9.0 did, and the [migration guide](migrate.html) tells a person who added the earlier copy to replace that part. A copy you added does not update itself: your global file keeps what you put there until you change it.

</section>
