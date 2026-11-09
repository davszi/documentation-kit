+++
title = "Get started"
brand = "Documentation kit"
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
<p class="slide-eyebrow">Documentation kit</p>
<p class="slide-title">Shared rules, pinned once, read right before each action</p>
<p class="slide-lead">A project adds the kit as one submodule and routes each kind of action to its guide. Building a website from the same Markdown is optional.</p>
<div class="slide-main"><div class="slide-row"><div class="slide-tile is-term"><h4>Pin</h4><p>.docs-kit submodule · its commit is your version</p></div><div class="slide-tile"><h4>Route</h4><p>one AGENTS.md row per action · kit guide + your record</p></div><div class="slide-tile is-held"><span class="slide-tag">optional</span><h4>Build a site</h4><p>the same Markdown as a checked website</p></div></div></div>
<p class="slide-scope">Summary of this page · no measured results</p>
<!-- /slide -->

## One pinned submodule gives a project shared rules and tools

<p class="bs-lead">The kit supplies rules, a reader and a site toolchain. Your project keeps its content, its specifics and the decision when to upgrade.</p>

<div class="bs-grid g2">
<div class="bs-part bs-violet"><span class="bs-label">The kit supplies · <code>.docs-kit/</code></span><h3>Shared and pinned</h3><ul>
<li><code>rules/</code>: engineering, documentation, writing and experiment guides your router points to</li>
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

A rule that several projects share has one home: the kit. Without that, each project keeps its own copy, a fix lands in one copy and the others drift. The split also works the other way: a project's commands, thresholds and exceptions are facts about that project, so they stay in its own records, where its contributors look. Changing a common rule means changing the kit; a project picks the change up when it moves its pin.

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
<div class="bs-flow" role="img" aria-label="Step 1: pin the kit at .docs-kit. Step 2: in AGENTS.md, add a row for each kind of action that names the kit guide and the project's own record, for example quoting a measured number with rules/writing/evidence.md and the project's benchmark records. Step 3: before that action, a contributor or agent reads both, then acts.">
<div class="bs-node bs-teal"><span class="bs-label">Step 1 · once</span><b>Pin the kit</b><ul><li><code>.docs-kit</code> submodule</li><li>its commit is your version</li></ul></div>
<div class="bs-arrow"><span>route</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Step 2 · <code>AGENTS.md</code></span><b>One row per action</b><ul><li>before quoting a number…</li><li>…read <code>rules/writing/evidence.md</code> and your benchmark records</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Step 3 · every time</span><b>Read both, then act</b><ul><li>shared rule + project specifics</li><li>nothing is copied</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> Adoption is a pointer, not a copy: one router row joins a shared rule with the project's own specifics. This diagram contains no measured results.</figcaption>
</figure>

[Figure 1](#fig-routing) is the whole mechanism. The router is triggered by the action, not the topic: an agent about to commit reads the Git guide, not every guide. That keeps each task's reading short and makes it hard to skip the rule that applies. Read the orientation and the rules that apply to every task once at the start; route the rest by action, and recheck the routes when the task grows. Reading a route grants no permission to run or publish anything.

```markdown
| Before…                   | Read…                                                           |
|---------------------------|-----------------------------------------------------------------|
| Quoting a measured number | `.docs-kit/rules/writing/evidence.md` and our benchmark records |
| Staging or committing     | `.docs-kit/rules/engineering/git.md` and our validation records |
```

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
<div class="bs-part bs-teal"><span class="bs-label">6 guides · 12 chapters</span><h3><a href="engineering-practices.html">Engineering</a></h3><ul>
<li>consumed output is an interface; generated files change at their source</li>
<li>efficient by default; a performance claim names its workload and path</li>
<li>expensive jobs run on the project's route, under a stated budget, owned through cleanup</li>
<li>the owner finishes routine work; changes to the agreement go back for a decision</li>
<li>reports lead with the outcome and say how each claim is known</li>
<li>one commit per logical deliverable, reviewed as a whole</li>
</ul><p><b>Read before:</b> changing code, running heavy jobs, handing off, committing.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">7 guides · 15 chapters</span><h3><a href="writing-practices.html">Documentation and writing</a></h3><ul>
<li>every fact has one home; finished work moves to its subject</li>
<li>records keep the contract for agents; pages explain it to people</li>
<li>each section states its takeaway before the evidence</li>
<li>one visible story; optional depth in typed folds</li>
<li>a measured number is current only with its full provenance</li>
<li>figures, mathematics and code excerpts follow shared conventions</li>
</ul><p><b>Read before:</b> creating or moving a document, writing a page, quoting a number, drawing.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">2 guides · 9 chapters</span><h3><a href="experiments.html">Experiments</a></h3><ul>
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

The [writing](writing.html) and [site maintenance](maintenance.html) entrypoints are short indexes that list the focused guides and what each one owns.

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
<figcaption><b>Figure 2.</b> Setup in three steps. This diagram contains no measured results.</figcaption>
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
<li>Keep historical public routes with the <a href="publication.html">publication exporter</a> and project <a href="resources.html#resource-closure-and-evidence">path adapters</a>.</li>
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
