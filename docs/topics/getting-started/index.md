+++
title = "Get started"
brand = "Documentation kit"
brand_sub = "what it provides · install · adopt"
description = "What the kit provides, how a project pins it and which adoption route fits."
reader = false
body_class = "reference-page"
components = ["toc", "nav", "filelinks", "panel-switcher"]
page_css = ["build-sheet.css"]
toc = [["What the kit provides", "#what-the-kit-provides"], ["Set it up", "#set-it-up"], ["Choose how to adopt it", "#choose-how-to-adopt-it"]]
+++

# Get started with the documentation kit

<p class="bs-lead">A project adds the kit as one pinned Git submodule. The kit supplies shared practices and tools; the project keeps its content and decides when to upgrade.</p>

This page orients you. Commands and exact contracts stay in the guides it links,
so each instruction has one place to change.

## What the kit provides

| Folder | What it is | Guide |
|---|---|---|
| `rules/` | Engineering, documentation, writing and experiment rules your router points to | [Project practices](project-practices.html) |
| `theme/` | Chapter reader, build-sheet layout, components, fonts and local math | [Reader](reader.html) |
| `docsite.py`, `tooling/` | Build, freshness check, lint, slide decks and publication export; no JavaScript install | [Authoring](authoring.html) |
| `examples/starter/` | A neutral project that `init` copies in without overwriting files | [Start a project](readme.html#start-a-project) |

Your project keeps its orientation, task routes, topic records, pages,
navigation, figures, evidence and upgrade timing.
[Ownership](readme.html#ownership) lists the paths on each side.

## Set it up

1. **Pin the kit.** From your repository root:

   ```bash
   git submodule add <kit-url> .docs-kit
   git submodule update --init --recursive
   ```

   The submodule commit is the version you use. Nothing changes until you move it.

2. **Route actions to guides.** Add a table to your `AGENTS.md` with one row per
   action. Each row names the kit guide, plus the project record that holds your
   specifics:

   ```markdown
   | Before…                   | Read…                                                          |
   |---------------------------|----------------------------------------------------------------|
   | Quoting a measured number | `.docs-kit/rules/writing/evidence.md` and our benchmark records |
   ```

   The [starter's router](../../examples/starter/AGENTS.md) has every row; keep
   the ones you need. [Project practices](project-practices.html) explains each guide.

3. **Optional: build a site.** Create the documentation environment, run
   `docsite.py init .`, set `docs/site/site.toml`, then build and lint. The
   [README commands](readme.html#start-a-project) list each step;
   [validation](validation.html#validation-and-review) says what the checks cover.

4. **Upgrade deliberately.** Read the [release notes](releases.html), move the
   submodule to the new commit and apply any consumer changes in the same commit.
   See [pin and upgrade](readme.html#pin-and-upgrade).

## Choose how to adopt it

<p class="bs-lead">Pick the route that matches what the project already has.</p>

<div class="panel-switcher" data-panel-switcher data-panel-default="new">
<div class="panel-switcher-controls" role="group" aria-label="Adoption route">
<button type="button" data-panel-choice="new" aria-pressed="false" aria-controls="route-new">New project</button>
<button type="button" data-panel-choice="existing" aria-pressed="false" aria-controls="route-existing">Existing documentation</button>
<button type="button" data-panel-choice="practices" aria-pressed="false" aria-controls="route-practices">Practices only</button>
</div>
<div id="route-new" data-panel="new">
<h3 id="route-new-project">New project</h3>
<p>Start from the starter. <code>docsite.py init</code> checks every destination first and refuses to overwrite existing files.</p>
<ul>
<li>Run the steps in <a href="readme.html#start-a-project">Start a project</a>.</li>
<li>Replace the starter's guide with your topics, following <a href="authoring.html#authoring-paths">authoring paths</a>.</li>
<li>Keep the single task router the starter adds; see <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</li>
</ul>
</div>
<div id="route-existing" data-panel="existing">
<h3 id="route-existing-documentation">Existing documentation</h3>
<p>Keep the existing content and destinations. Add the configuration deliberately, page by page.</p>
<ul>
<li>Render existing Markdown in place with <a href="authoring.html#registered-source-pages">registered source pages</a>; nothing moves.</li>
<li>Keep historical public routes with the <a href="publication.html">publication exporter</a> and project <a href="resources.html#resource-closure-and-evidence">path adapters</a>.</li>
<li>Replace copied shared rules only after their project-specific parts have a linked home, as the <a href="migrate-1-1-0.html#prepare-the-deliverable">migration guide</a> describes.</li>
</ul>
</div>
<div id="route-practices" data-panel="practices">
<h3 id="route-practices-only">Practices only</h3>
<p>The rules are plain Markdown. A project can route contributors to them without building a site.</p>
<ul>
<li>Add one task-triggered router that names the guide to read before each action; see <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</li>
<li>Start from the <a href="project-practices.html">practices overview</a>.</li>
<li>Keep concrete commands, thresholds and resource profiles in the project's own records.</li>
</ul>
</div>
</div>
