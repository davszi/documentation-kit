+++
title = "Set up a project with the kit"
brand_sub = "three commands · starter files · adoption routes"
description = "Set up a project: three commands, the files the starter writes and the adoption route that fits what you already have."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Set up", "#set-up"], ["Starter files", "#starter-files"], ["Adoption routes", "#choose-how-to-adopt-it"]]
page_only = "Explains setting up the kit; its records are README.md and the guides in rules/."
+++

# Set up a project with the documentation kit

<section class="card" id="set-up">

## A new project needs one submodule, one environment and one init

<p class="bs-lead">Pin the kit, install its pinned Python packages, let <code>init</code> add the starter, then track what it wrote. What the kit is and how a project uses it is on the <a href="index.html">home page</a>.</p>

<figure id="fig-setup">
<div class="bs-flow" role="img" aria-label="Pin the kit as a submodule at .docs-kit, then create a Python 3.12 environment with the kit's pinned requirements, then run docsite.py init with the project's title and repository, which writes the starter files, a .gitignore among them. Finally track the sources and that .gitignore in Git, because the build only publishes tracked files.">
<div class="bs-node bs-teal"><span class="bs-label">Once</span><b>Pin and install</b><ul><li><code>.docs-kit</code> submodule</li><li>Python 3.12 env, pinned packages</li></ul></div>
<div class="bs-arrow"><span>init</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>docsite.py init</code></span><b>Write the starter</b><ul><li>never overwrites a file</li><li>fills title and repository</li></ul></div>
<div class="bs-arrow"><span>track</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Git</span><b>Track the sources</b><ul><li>the build publishes tracked files only</li><li>the starter's <code>.gitignore</code> keeps <code>.build/</code> out</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> Setup in three steps. This diagram contains no measured results.</figcaption>
</figure>

```bash
git submodule add <kit-url> .docs-kit
git submodule update --init --recursive
python3.12 -m venv .build/docs-env
.build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
.build/docs-env/bin/python .docs-kit/docsite.py init . --title "My project" --repository https://github.com/owner/repo
git add .gitignore AGENTS.md CLAUDE.md docs .gitmodules .docs-kit
```

[Figure 1](#fig-setup) gives the order, and the commands above carry it out. The last line tracks everything `init` wrote, its `.gitignore` included, together with the submodule; the build publishes tracked files only. The [README](readme.html#start-a-project) owns these commands and the build, lint and preview that follow.

<div class="bs-grid g2">
<div class="bs-part bs-violet"><span class="bs-label">What <code>init</code> writes</span><h3>Your project's entry files</h3><ul>
<li><code>AGENTS.md</code>, <code>CLAUDE.md</code>: the task router and its Claude import</li>
<li><code>.gitignore</code>: keeps <code>.build/</code> out of Git</li>
<li><code>docs/PROJECT_CONTEXT.md</code>, <code>docs/index.md</code>: repository map and reading routes</li>
<li><code>docs/CAPABILITY_MAP.md</code>: what the project's tooling does</li>
<li><code>docs/worklog.md</code>, <code>docs/open/OPEN.md</code>: chronology and open work</li>
<li><code>docs/site/</code>: <code>site.toml</code> with title, repository and navigation, and two figure fragments the guide page includes</li>
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
    ├── CAPABILITY_MAP.md     what the project's tooling does: one need per row, with its code and state
    ├── worklog.md            append-only chronology, newest entries first
    ├── open/OPEN.md          open work: one line per item, each linking the record that owns it
    ├── site/
    │   ├── site.toml         site title, source repository, navigation
    │   └── fragments/        ownership.html, slide-anatomy.html: two figures the guide page includes
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
<li><code>CAPABILITY_MAP.md</code>: each tooling need once, with its code</li>
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

<!-- fold: detail What is not in the project, and why -->

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
<li>Publish existing Markdown in place: every tracked Markdown file under <code>docs/</code>, or under the folders <code>reference_roots</code> names, becomes a <a href="build-a-site.html#existing-markdown">source page</a> in the Reference section unless you exclude it; nothing moves.</li>
<li>Keep historical public routes with the <a href="publication.html">publication exporter</a>.</li>
<li>Replace a copied shared rule only once its project-specific parts have a linked home.</li>
</ol><p><b>Stays as is:</b> your content, destinations and history; the <a href="migrate.html#prepare-the-upgrade">migration guide</a> shows the review steps.</p></div>
<div class="bs-part bs-orange" id="route-practices"><span class="bs-label">You want the rules, not a site</span><h3 id="route-practices-only">Practices only</h3><ol>
<li>Add the submodule.</li>
<li>Add router rows to <code>AGENTS.md</code>, as in <a href="index.html#how-it-works">read before acting</a>.</li>
<li>Pick the rows from the <a href="index.html#practice-areas">practice pages</a>.</li>
<li>Keep concrete commands, thresholds and resource profiles in your own records.</li>
</ol><p><b>Stays as is:</b> everything; no build, no new pages.</p></div>
</div>

All three routes share the same core: a pinned submodule and router rows. They differ only in how much of the site toolchain you take. You can start with practices only and add a site later without undoing anything; the rules and the router stay the same.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Run <code>init</code> over existing docs</h3><p>If any starter file already exists, <code>init</code> refuses and writes nothing; forcing a copy by hand would overwrite or duplicate the project's own records.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Register what is already there</h3><p>The project adds <code>site.toml</code>, settles which existing Markdown files its Reference section lists and keeps every file where it was.</p></div>
</div>

**Optional: the owner's global agent instructions.** The rules in the kit say what a project does. How an agent works with a person in every project, such as how it reports, when it delegates, how it puts a decision to the person and how it checks a claim, sits in the person's own global agent file. The kit ships [a copy of its owner's file](global-agent-instructions.html) with personal details removed. A person may add it to their own file or replace theirs with it; the [README](readme.html#optional-the-owners-global-agent-instructions) has the two commands. The kit does not load the copy and no rule depends on it.

</section>
