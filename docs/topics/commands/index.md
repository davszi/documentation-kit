+++
title = "Setup and commands"
brand = "Documentation kit"
brand_sub = "init · build · lint · preview · slides · upgrade"
description = "Every docsite.py command a project runs, what each one checks or writes, and how to upgrade the pinned kit."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Start a project", "#start-a-project"], ["Build", "#build"], ["Lint", "#lint"], ["Preview", "#preview"], ["Slides", "#slides"], ["Upgrade", "#upgrade"]]
+++

# Setup and commands

<section class="card" id="start-a-project">

## A new project needs one submodule, one environment and one init

<p class="bs-lead">Pin the kit, install its pinned Python packages, then let <code>init</code> add the starter without overwriting anything.</p>

<figure id="fig-setup">
<div class="bs-flow" role="img" aria-label="First add the kit as a submodule at .docs-kit. Then create a Python 3.12 environment and install the kit's pinned requirements. Then run docsite.py init, which writes the starter with the project's title and repository.">
<div class="bs-node bs-teal"><span class="bs-label">Once</span><b>Pin the kit</b><ul><li><code>git submodule add</code></li><li>path <code>.docs-kit</code></li></ul></div>
<div class="bs-arrow"><span>then</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Once per checkout</span><b>Create the environment</b><ul><li>Python 3.12 venv in <code>.build/docs-env</code></li><li>pinned <code>requirements.txt</code></li></ul></div>
<div class="bs-arrow"><span>then</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Once</span><b>Add the starter</b><ul><li><code>docsite.py init</code></li><li><code>--title</code>, <code>--repository</code></li></ul></div>
</div>
<figcaption><b>Figure 1.</b> The three setup steps, in order. This diagram contains no measured results.</figcaption>
</figure>

```bash
git submodule add <kit-url> .docs-kit
git submodule update --init --recursive
python3.12 -m venv .build/docs-env
.build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
.build/docs-env/bin/python .docs-kit/docsite.py init . --title "My project" --repository https://github.com/owner/repo
```

`init` checks every destination first and writes nothing if any starter file already exists. It writes the project's `AGENTS.md`, `CLAUDE.md`, `docs/PROJECT_CONTEXT.md`, reading index, worklog, open-work file and `docs/site/site.toml`, with the title (default: the folder name) and repository filled in. Then add `.build/` to `.gitignore` and track the sources: the build only publishes tracked files.

```bash
git add docs AGENTS.md CLAUDE.md .gitmodules .docs-kit
```

<div class="bs-specs"><div><span class="bs-label">Python</span><b>3.12+</b></div><div><span class="bs-label">Packages</span><b>Pinned</b></div><div><span class="bs-label">JavaScript install</span><b>None</b></div></div>

An existing documentation system keeps its content: skip `init`, add `docs/site/site.toml` deliberately and follow [adoption](maintenance.html). Full details: [README · Start a project](readme.html#start-a-project).

</section>

<section class="card" id="build">

## Build writes the site; --check proves it is current without writing

<p class="bs-lead">Run <code>build</code> after changing a source; run <code>build --check</code> to confirm nothing is stale.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">writes</span><h3><code>build</code></h3><p>Renders every page into <code>.build/docs/</code> from tracked sources and the pinned kit, and removes obsolete output.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">writes</span><h3><code>build --page &lt;slug&gt;</code></h3><p>Renders only that page while you work on it; shared assets still sync.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">reads</span><h3><code>build --check</code></h3><p>Renders in memory and fails if the generated site no longer matches its sources. Writes nothing.</p></div>
</div>

```bash
.build/docs-env/bin/python .docs-kit/docsite.py build --project .
.build/docs-env/bin/python .docs-kit/docsite.py build --project . --page guide
.build/docs-env/bin/python .docs-kit/docsite.py build --project . --check
```

The build fails instead of publishing a broken page: untracked or missing media, paths that leave the project, route collisions and wrong anchors into registered pages all stop it. Generated output is never edited; change the source, configuration or generator and rebuild. [Site toolkit](site-toolkit.html#checks-before-publishing) explains each check.

</section>

<section class="card" id="lint">

## Lint checks the records behind the site; --strict makes warnings fail

<p class="bs-lead">Run <code>lint --strict</code> before you commit documentation; it covers what the build cannot see.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">links</span><h3>Links and anchors</h3><p>Markdown links and anchors in <code>docs/</code>, <code>AGENTS.md</code>, <code>CLAUDE.md</code> and <code>README.md</code> resolve, and so do links in the built HTML.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">excerpts</span><h3>Code excerpts</h3><p>A fenced block tagged <code>source=path#La-Lb</code> must still appear in its file, at the stated lines.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">figures</span><h3>Figure manifest</h3><p>Figure files and manifest entries match both ways, and their generators exist.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">records</span><h3>Worklog and open work</h3><p>Worklog dates run newest first; every open-work bullet links its owner, with no struck or ticked lines.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">site</span><h3>Fresh, self-contained output</h3><p>The built site is fresh and loads no external resources.</p></div>
</div>

```bash
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --registry
```

Without `--strict`, warnings print but the run passes; with it, any warning fails. `--registry` lists every `INVARIANT` and `DON'T-REDO` marker in the project and exits. A project with established file names sets `worklog` or `open_work` in `site.toml`; see [resources](resources.html).

</section>

<section class="card" id="preview">

## Review the built site on loopback before anyone else sees it

<p class="bs-lead">Serve <code>.build/docs/</code> on 127.0.0.1 and read the changed pages at wide and narrow widths.</p>

```bash
python3.12 -m http.server 8321 --bind 127.0.0.1 --directory .build/docs
```

Open `http://127.0.0.1:8321/html/index.html`. The server exposes only the generated output, not the repository. A successful build and lint still need a look at the rendered page: check the changed layout at wide and narrow widths before committing or publishing. [Validation](validation.html#validation-and-review) lists what a complete review covers, including the reusable browser checks.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>"Lint passed, so it looks fine"</h3><p>The new table is never opened on a phone; it pushes the page sideways for every narrow reader.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Open the changed page at both widths</h3><p>The table is checked at desktop and phone width before the commit, and the review is mentioned in the handoff.</p></div>
</div>

</section>

<section class="card" id="slides">

## One command turns chapter slide faces into a presentable deck

<p class="bs-lead"><code>slides</code> builds the site, then collects the slide faces of the chapters you select into one HTML deck.</p>

```bash
.build/docs-env/bin/python .docs-kit/docsite.py slides --project . --select guide --out guide
.build/docs-env/bin/python .docs-kit/docsite.py slides --project . --select guide --select other#intro,result --out review --title "Review"
```

<div class="bs-specs"><div><span class="bs-label">Select a page</span><b><code>--select slug</code></b></div><div><span class="bs-label">Select chapters</span><b><code>slug#a,b</code></b></div><div><span class="bs-label">Output</span><b><code>.build/slides/</code></b></div></div>

Repeat `--select` to combine pages; listed chapters keep the order you give. Each face stays tied to the chapter that backs its claims, so the deck never holds a fact the page does not. See [slide faces and decks](authoring.html#slide-faces-and-decks) and the live example in the [reader tour](reader-tour.html#slides-and-print).

</section>

<section class="card" id="upgrade">

## An upgrade moves the pin only after you read what changed

<p class="bs-lead">The submodule commit is your version. Nothing changes until you move it, rebuild, review and commit the new pin.</p>

<figure id="fig-upgrade">
<div class="bs-flow" role="img" aria-label="Read the release notes between your pinned version and the target. Move the .docs-kit submodule to the reviewed commit or tag. Rebuild and lint, review the pages, then commit the pin together with any consumer changes.">
<div class="bs-node bs-teal"><span class="bs-label">Read</span><b>Release notes</b><ul><li>changes since your pin</li><li>migration guide if any</li></ul></div>
<div class="bs-arrow"><span>move</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>.docs-kit</code></span><b>Check out the target</b><ul><li>a reviewed commit or tag</li></ul></div>
<div class="bs-arrow"><span>verify</span></div>
<div class="bs-node bs-orange"><span class="bs-label">One commit</span><b>Rebuild, review, commit</b><ul><li>build and lint</li><li>pin plus consumer changes</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> The upgrade sequence. This diagram contains no measured results.</figcaption>
</figure>

```bash
git -C .docs-kit fetch --tags
git -C .docs-kit checkout <reviewed-kit-commit-or-tag>
.build/docs-env/bin/python .docs-kit/docsite.py build --project .
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
git add .docs-kit
```

Others clone with `git clone --recurse-submodules <project-url>` and get exactly your pinned kit. Share fixes upstream in the kit, not by editing a consumer's submodule checkout. [Release notes](releases.html) list what each version changes for consumers; [README · Pin and upgrade](readme.html#pin-and-upgrade) has the details.

</section>
