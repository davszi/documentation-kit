# Site tooling and authoring

## Tooling and ownership

| Location in consuming repository | Responsibility |
|---|---|
| `.docs-kit/` | Git submodule at a reviewed commit: shared rules, engine, templates, components, dependencies and checks |
| `docs/topics/<topic>/index.md`, or one level deeper in a [topic group folder](#topic-group-folders) | Editable rendered page, with supporting records beside it |
| `docs/site/site.toml` | Project title, source repository/ref, navigation, reader and project resource configuration |
| `docs/site/assets/`, `docs/site/fragments/` | Project-owned assets and explicit overrides; do not copy the entire theme |
| `docs/figures/` | Shared project figures with declared provenance |
| `.build/docs/` | Reproducible generated output, ignored by Git |

Initialize the submodule before building. The kit is versioned in `VERSION` and
tagged `v<version>`; [release notes](../../docs/topics/releases/releases.md) list each
version's changes and its migration steps. Upgrade the pin as a reviewed deliverable and run the [project conformance check](../conformance.md), run the shared and consumer checks, and record the adopted revision and compatibility evidence. Change the kit only in its own repository, following [the shared kit submodule](../engineering/git.md#the-shared-kit-submodule). Engine and shared-theme changes belong upstream; project content and optional extensions stay local.

From the consuming project root, use the pinned kit directly:

```bash
python -m pip install -r .docs-kit/requirements.txt
python .docs-kit/docsite.py build --project .
python .docs-kit/docsite.py build --project . --check
python .docs-kit/docsite.py lint --project .
```

Use `--page <slug>` with build for targeted iteration. Lint supports `--strict` and `--registry`. The `capability-map` command rewrites the generated column of the project's capability map; see [capability map settings](#capability-map-settings). The kit README owns installation and shared-engine development checks. The project's `docs/PROJECT_CONTEXT.md` records its tested environment and additional checks. Pin dependency versions; documentation builds must not require importing the consuming application's runtime or initializing a GPU.

Set `gh_repo = ""` when the project has no source remote. Source links then
keep their local identity relative to the logical `docs/html/` origin, and
registered pages omit remote edit links. HTTP previews do not rewrite those
links to GitHub. Building still packages only declared resources; it does not
expose the source checkout. To make source files available in an HTTP bundle,
admit them through the [publication exporter](publication.md#configured-publication).
Without a source remote, `publish` rewrites the source links of every generated
page, not only the pages named in `[publication] pages`: a link to an admitted
file points at its published copy, and a link to an untracked file shows as
unavailable local evidence. A link to a tracked file that is not admitted keeps
its local path, which leads outside the bundle.

## Authoring paths

Two kinds of page render: topic entry pages at `docs/topics/*/index.md`, or inside a [topic group folder](#topic-group-folders), and [registered source pages](#registered-source-pages). Every new entry page needs frontmatter with `title` and `toc` (an empty list is valid with automatic chapters), plus a corresponding `[[nav]]` entry in `docs/site/site.toml`. The folder supplies its public slug; set `slug = "index"` on the home page. Slugs are lowercase filename stems without directories. Use `hidden = true` for a built, directly reachable page outside navigation, subject to the documentation deletion policy.

A rendered page body above `<!-- page-end -->` uses the logical public `docs/html/` URL origin, mapped to `.build/docs/html/`. Its source-only notes tail resolves from the actual source folder. Normal Markdown records resolve links from their own folder.

| Context | Example | Meaning |
|---|---|---|
| Rendered page body | `guide.html#publish` | Generated page and stable anchor |
| Rendered page body | `../figures/example.svg` | Shared project figure |
| Rendered page body | `../../experiments/example/results.json` | Repository evidence/source |
| Rendered page body | `../topics/guide/guide.md` | Explicit agent record/source |
| Notes tail | `../other/other.md` | Sibling topic record, source-relative |
| Notes tail | `evidence/source.md` | Supporting record in the current topic |

Prefer `.html` links when the purpose is reading a page and explicit source links when inspecting source is intended. Raw Markdown viewing does not apply generated-origin interpretation. Preserve source path and fragment metadata so local and hosted source links retain identity.

Lint checks every link to a repository file, whether written in Markdown or as
HTML with a double-quoted `href`, `<a href="…">`; other quoting is not checked. A Markdown link is checked in its source file. An HTML
link is checked in the built page, where the build has resolved it, with a
source remote or without one: this covers the body of a topic page, the
fragments it includes and a registered source page. The target must exist, and
a fragment into a Markdown file must match one of its anchors, as for a
Markdown link. Each failure is an error that names the page's source, the
built page and the repository path. On an automatically listed page it is a
note, and links in worklog entries dated before `worklog_links_checked_from`
are not checked. A file the local-artifact manifest lists under
`omitted_files` gets a note when it is absent. An existing file that Git does
not track passes, as for a Markdown link, although the published source link
to it leads nowhere.

Includes select a matching shared theme file first (for example,
`components/chapter-reader.html`); project fragments otherwise resolve from
`docs/site/`. Include paths stay relative and contained. `page_css = ["build-sheet.css"]`
selects the kit's shared theme resource. Local stylesheet entries such as
`../site/assets/example.css` resolve from the shared `docs/topics/` configuration
base. Do not introduce machine-specific absolute paths or remote media dependencies.
Fonts follow the [shared dependency rules](reader.md#shared-reading-layout).

An included fragment may include further fragments, up to eight levels; a cycle
fails the build. A `[[nav]]` table accepts only `label`, `file`, `group`, `short`
and `hidden`. TOML assigns every key written after a table header to that table,
so keep top-level settings such as `extra_components` above the first `[[nav]]`;
the build rejects any other key inside a nav entry.

`brand_mark` sets the project's mark beside its name in the sidebar: up to three
characters, such as `brand_mark = "∿"`, or a tracked SVG file, such as
`brand_mark = "docs/site/brand-mark.svg"`, drawn with `currentColor`. Without it
the mark is the initials of `title`. Each project uses its own mark.

The sidebar header shows the site's name beside the mark on every page and
links to the home page. The name is `title`; set `home_label` when the header
needs a shorter name; a blank value counts as unset. The browser stores a
reader's open navigation groups and pinned drawer under this name, so changing
it resets them once. A page cannot change the name: the `brand` frontmatter key
is deprecated, accepted and not read. `brand_sub` stays a page's own line. It appears under the
name on a page without the chapter reader and on the page's site-map card when
the page has no `description`.

The browser tab names the site first, then the page: "`title` · short name".
The short name is the page's `[[nav]]` label when an entry lists the page,
otherwise the page's title; Reference pages, automatically listed files and the
Reference index use their titles. The home page's tab shows `title` alone,
since its label would only repeat that it is the start. A deck from `slides`
shows "`title` · deck title", and a lock page from `publish` shows
"`title` · Locked" and nothing of the page it locks. A site without `title`
keeps the page title alone, and a lock page "Locked page". The heading and the
title in the page's top bar stay the page's own title.

Navigation groups take their colour from `--g`. A `[group_colors]` table in
`site.toml` sets it for the whole site, one hex colour per group, such as
`"guide" = "#6ee7c5"`: the group's sidebar header and page links, its home-page
map cards and the build-sheet chapter numbers of its pages take that colour.
Each name must be the `group` of a visible `[[nav]]` entry, written exactly.
Project CSS on a page may still set `--g`. A group without a colour gets the
next shared tone in order.

A page that lists `plot-toggles` in its `components` gives every inline SVG
figure (class `inline-fig`) one chip per group of elements whose `id` is
`tg-<group>--<n>`; a chip hides and shows its group, on the page and in the
lightbox. The chip shows the group key and a dot in the colour of its series,
in the lightbox too. A chip keeps its label on one line; when the chips do not
fit beside each other, the bar wraps whole chips onto a new row. A `[plot_toggle_labels]` table in
`site.toml` gives a key a label for the whole site, such as
`"corridor" = "road corridor"`; each value must be text. The build writes the
table into each page that loads the component, and a key the table does not
name keeps showing the key.

`page_number_notes = true` turns on lint notes, for the whole site, for numbers
in a topic page's prose that none of the page's linked records state, as
[rendered pages are for people](../documentation.md#rendered-pages-are-for-people-records-stay-markdown)
describes. The default is off. Like every top-level setting it goes above the
first `[[nav]]` table. The check does not read frontmatter, comments, code,
inline SVG, HTML attributes, link targets, version numbers, dates, ratios such
as 16:9 or labels such as "Figure 3", and it skips a page that links no record.
Show a literal value as code to keep it out of the notes.

`nested_nav = true` folds each navigation group into a native disclosure,
opens the current page's group (the first group on a page outside every
group) and places the current page's sections directly under its entry. It
applies to pages without the chapter reader, which nests chapters itself, and
keeps working without JavaScript. Groups a reader opens stay open on later
pages through browser storage, and open or close with a short transition that
respects reduced motion. The default is the flat site tree.

`folded_groups = ["parked"]` folds the named navigation groups, one disclosure
per group, and leaves the other groups as they are. The `[[nav]]` entries of a
folded group stand together; the build rejects a folded group that other
entries split. A folded group is closed
unless it holds the current page. A group the reader opens stays open on later
pages through browser storage. The setting applies to the flat site tree, so it
works on pages with the chapter reader, and it keeps working without
JavaScript. Each name must be the `group` of a visible `[[nav]]` entry. With
`nested_nav = true`, pages without the chapter reader already fold every group
and the setting changes nothing there.

Register project-specific script components with `extra_components = ["viewer"]`;
each uses a tracked `docs/site/components/<name>.js`. For dynamically loaded
dependencies, `[extra_assets]` maps output names below `html/assets/` to tracked
project files, for example `"viewer/renderer.js" = "docs/site/assets/vendor/renderer.js"`.
List licenses/source notices alongside their dependencies. Paths must stay
inside the project, and project assets cannot overwrite shared kit assets.

The starter's reader-free home page selects shared `home.css` for its hero,
links and generated topic cards. That stylesheet and arrangement are optional;
projects may author their own homepage and local styles. Follow
[project-owned homepage composition](../writing/pages.md#project-owned-homepages).

Wrap a wide comparison table in `.scroll` with `role="region"`, a useful
`aria-label`, `tabindex="0"` and `data-reader-horizontal`. This keeps scrolling
and keyboard arrows inside the table instead of changing chapters. Pages with
`body_class = "reference-page"` get this region on every Markdown table
automatically.

### Topic group folders

A project may keep some topic folders one level deeper, inside a group folder:
`docs/topics/<group>/<topic>/index.md`. Name each group folder in
`docs/site/site.toml`, above the first `[[nav]]` table:

```toml
topic_group_folders = ["parked"]
```

A topic inside a group folder counts like any other topic: its page builds, it
needs a record or `page_only`, and the lint notes cover it. The page's address
stays `<topic>.html`. The folder says where the source lives; the `group` of
the page's `[[nav]]` entry says where a reader finds it. Moving a topic into or
out of a group folder therefore changes no published address. Two topics with
the same folder name would share one address, so the build rejects them.

A group folder only groups. It holds topic folders and no Markdown file of its
own, and there is exactly one group level. A page two levels down in a folder
that the setting does not name is not built; lint prints a note for it.

Moving a topic changes these paths in the same change:

- Links in the page body, above `<!-- page-end -->`, resolve from the built
  page. A link to another page or to a shared figure stays as it is. A link
  into the moved folder itself, such as `../topics/<topic>/<topic>.md`, gains
  the group folder: `../topics/<group>/<topic>/<topic>.md`.
- Links in the topic's records, and in notes below `<!-- page-end -->`,
  resolve from the file, so each relative link that leaves the folder gains or
  loses one `../`.
- Paths written from another base name the folder too: a `page_css` entry
  inside the topic folder, a `[[source_pages]]` `source`, an `[extra_assets]`
  source, and links from other files such as `docs/open/OPEN.md`.

Lint reports a link it can no longer resolve as a dead link, and the build
rejects a registered source or stylesheet that is missing.

### Capability map settings

Every project sets `tooling_roots` for its
[capability map](../engineering/code.md#the-capability-map), above the first
`[[nav]]` table like every top-level setting; lint fails without it. A project
without tooling writes `tooling_roots = []`, and nothing else is checked. A
project with tooling names its folders:

```toml
tooling_roots = ["tools/"]
capability_map = "docs/CAPABILITY_MAP.md"
experiment_roots = ["experiments/"]
```

- `tooling_roots` lists the project's tooling folders. Every tracked file or
  folder directly under one of them needs a row in the map; names that start
  with a dot and `__init__.py` are exempt.
- `capability_map` names the map when it is not at the default
  `docs/CAPABILITY_MAP.md`. It must be a Markdown file inside the project.
  Lint checks its links wherever it lies.
- `experiment_roots` lists the folders whose subfolders are experiments.

Each folder is a path relative to the project root, with or without a
trailing slash, and no folder may lie inside another named folder. The build
fails with a `site.toml:` error for a wrong type or path, and for
`capability_map` or `experiment_roots` set while `tooling_roots` names no
folder. Lint fails when a named folder holds no tracked file.

The map holds one table with the columns Need, Code, State and Imported by,
one row per need, then the list of needs seen but not built, each with when
and where it was seen and the person's decision with its date, or where the
open question waits:

- **Need:** one sentence that names no experiment.
- **Code:** a Markdown link to each file or folder that meets the need, or
  `—` when no code exists.
- **State:** `exists`, `partly` or `missing`. A `missing` row links no code;
  the other two link at least one path.
- **Imported by:** generated, never typed: the tracked Python files that
  import the linked code. A user inside a tooling root is named by the entry
  directly under that root, and a user inside an experiment folder by that
  folder. `no Python imports` and `not scanned: no Python code` mark the two
  empty cases. `python .docs-kit/docsite.py capability-map --project .`
  rewrites this column and nothing else; run it after adding a row or
  changing an import.

Lint fails when the map is missing or untracked, when an entry directly under
a tooling root has no row, when a link in the map is dead, when the Imported
by column differs from what the command writes, and when a state is unknown
or does not match its Code column. It warns, which fails `--strict`, when a
Python file under a tooling root imports from a folder under an experiment
root, naming the file, the line and the imported path, when a Python file
under either root does not parse, and when a file that is not tracked yet
would make lint fail once it is committed: an entry under a tooling root
without a row, or an import that changes the Imported by column.

The column and the warning read Python `import` and `from … import`
statements, those inside functions included. A name resolves against the
importing file's folder, the project root and each tooling root, in that
order, and a relative import against its package. A folder without
`__init__.py` counts as a package only when Python files lie below it, and
never under a name of the standard library. Not covered: code loaded by file
path or with `__import__`, code run as a command, imports that need another
`sys.path` change, and every language other than Python. When such users
matter, name them in the map's opening text.

### Registered source pages

A `[[source_pages]]` table renders an existing, tracked Markdown file as one
whole-file page without moving or copying it. Use it for records and guides
whose Markdown must stay the canonical source:

```toml
[[source_pages]]
source = "rules/engineering/git.md"  # contained, tracked .md file without +++ frontmatter
slug = "git"                         # public route: git.html
description = "Commits, shared checkouts and history."  # optional
pinned = true                        # optional: list first in the sidebar
```

`title` defaults to the file's first level-one heading. `description` supplies
the site-map card text and the sidebar tooltip. `math = true` enables formulas.
`reader = true` uses the chapter reader when the site enables it; otherwise the
page scrolls. In the
reader, a short opening (under 600 characters, without subheadings, figures or
tables) joins the first chapter with the source line instead of becoming a
nearly empty Introduction chapter; a longer opening stays its own chapter. One
slug belongs to one page. Topic entry pages keep their own frontmatter path and
cannot be registered.

Every sidebar ends with a **Reference** section that lists the site's source
pages: the registered files and the files the
[automatic reference listing](#automatic-reference-listing) adds. A site
without either shows no section. `pinned = true` lists a file at the top
of the section by its title, always visible, in the order the tables are
declared. Below the pinned files, one **Browse by folder** disclosure holds every
registered file in a folder tree at its repository path, pinned files included.
Each file shows its name and title.

The disclosure starts closed on pages for people, on pinned pages and on
registered pages listed in the navigation, because their entry already marks
them. On any other registered page it starts open, with only the folders that
lead to that page unfolded. The section follows the navigation in the menu's
normal flow.

Up to 60 listed files (`INLINE_TREE_LIMIT` in `tooling/source_tree.py`) every
page carries the whole folder tree; with the [page lock](publication.md#page-lock)
on, the tree is always written once. Above that, the tree is written once, as
`reference.tree.js` next to the pages, and as the page `reference.index.html`;
`site-build.json` names both under `reference_tree`, which is `null` for an
inline tree. Each page then carries the pinned files, the **Browse by folder**
disclosure with its count, a link to `reference.index.html` and, on a listed
page, the folders that lead to that page, with their full counts. The shared
`nav.js` loads `reference.tree.js` when the disclosure opens, or at load on a
listed page, and marks and unfolds the current file as the inline tree does.
It loads through a `<script>` element, because a page opened from disk cannot
`fetch` a neighbouring file. Without JavaScript the link opens the whole tree on
`reference.index.html`. At 81 files the inline tree added 29.8 KB to every page
of a measured site; at 400 files it added 199 KB to every page.

A registered file needs no `[[nav]]` entry, because the section lists it. Keep
`[[nav]]` for pages written for people, and for records every reader needs,
such as release notes and migration guides; such an entry lists the record
among those pages. A scrolling source page's sidebar shows the
site navigation and the repository section, not the page's own headings. With
`nested_nav = true`, a page that has a visible `[[nav]]` entry lists its
headings under that entry.

Links and media resolve from the file's own folder, exactly as when reading the
Markdown. A link to another source page, registered or listed automatically,
becomes that page's route. Other
repository files become source links, and tracked media are packaged. Absolute
paths, links that leave the project and missing targets fail the build. Every
fragment that points into a registered page, from any page, must match an
anchor of the rendered target. The worklog's entries dated before
[`worklog_links_checked_from`](resources.md#resource-closure-and-evidence) are
the exception: there a link whose target is gone renders as unlinked text. The page opens with its source path and an edit
link built from `gh_repo` and the configured `gh_ref`; `site-build.json` maps
each such route to its source file. Wide tables scroll inside
labelled regions. The page body carries the classes `source-page` and
`reference-page`; another scrolling page can opt into the same reading layout
with `body_class = "reference-page"`.

Topic-page markers are not interpreted in a registered file: includes, typed
folds, registry callouts and `<!-- page-end -->` stay literal, so a record can
show them as examples. Lint checks a registered file's Markdown links as an
ordinary record, and its HTML links to repository files in the built page, as
[authoring paths](#authoring-paths) describes.

### Automatic reference listing

By default every tracked Markdown file under `docs/` is a source page and
appears in the Reference section, without a `[[source_pages]]` table. A
project that keeps records elsewhere names those folders or single files in
`reference_roots`. **Every tracked Markdown file under a listed folder becomes
a page of the site.** A private repository with a public site thereby
publishes those files, unless it declares them private or turns the listing
off. A folder that no entry names is never listed, so a new folder publishes
nothing until the project names it. Root files such as `README.md` and
`AGENTS.md` are listed only when an entry names them.

A tracked `.md` file is not listed automatically when it:

- lies inside a Git submodule, the kit's `.docs-kit/` included, or inside the
  kit's own folder;
- has a folder or file name that starts with a dot, such as
  `.github/pull_request_template.md` or anything under `.claude/`; a
  `[[source_pages]]` table can still register it;
- starts with `+++` frontmatter, as topic entry pages do, or is a topic entry
  page;
- is a symbolic link or lies below one;
- lies outside every `reference_roots` entry;
- starts with a `private_prefixes` entry or ends with a `private_suffixes`
  entry of the [`[publication]` table](publication.md#configured-publication),
  which declare the file private. With `.md` among the private suffixes the
  listing lists no file, and `publish` refuses a `[[source_pages]]` table
  whose file is private.

A file that starts with `---` YAML frontmatter is listed and rendered as
ordinary Markdown: the frontmatter shows as text, and its closing `---` turns
the lines above it into a heading. Declare such a file private, or keep it
outside the listed folders, when its frontmatter should not show.

Two settings in `docs/site/site.toml`, above the first `[[nav]]` table,
control the listing:

```toml
reference_roots = ["docs", "experiments", "README.md"]   # default: ["docs"]
reference_listing = false   # list only [[source_pages]] tables
```

`reference_roots` names what is listed: each entry is a folder, whose tracked
Markdown files are listed at any depth, or one Markdown file. An entry is a
plain path from the project root, not a glob: distinct, with no leading `/`,
no `\`, no `*`, `?` or `[`, and no `.` or `..` parts. A set value replaces the
default, so it names `docs` too when `docs/` stays listed. An entry that lists
no file gets a note in lint. To keep one file of a listed folder off the site,
name it in `private_prefixes`.
`reference_listing = false` turns the automatic listing off; the site then
lists only its `[[source_pages]]` tables. A wrong type or entry fails the
build with an error such as `site.toml: reference_listing must be true or
false`.

A `[[source_pages]]` table still wins: it keeps every meaning above and sets
the slug, title, description, `math`, `reader` and `pinned` of its file. It
registers a file outside every listed folder too. Only a table can pin a file.

An automatically listed file is published as a route derived from its path.
Each folder and the file name are lowercased; every run of characters other
than `a-z`, `0-9`, `_` and `-` becomes one `-`; the parts join with `.`, and the
name keeps `.md` before `.html`. `docs/Design Notes/API v1.2.md` becomes
`docs.design-notes.api-v1-2.md.html`, and `README.md` becomes
`readme.md.html`. A slug cannot contain `.`, so these routes never meet a
registered slug. When two files reach the same route, a file whose path already
has that form keeps it; every other file, and any file whose route another page
already has, gets the first eight hexadecimal digits of the SHA-256 of its
path before `.md`, such as `readme-0123abcd.md.html`. A name longer than 180
characters is cut and gets the same suffix. A collision never fails the build;
lint prints a note for it. The route stays the same while the file keeps its
path and no other file reaches its route; moving or renaming the file changes
its public address.

An automatically listed page never fails the build and never adds a lint
warning or error. What a registered page would reject is shown tolerantly, and
lint prints each case as a note, which never fails, not even under `--strict`:

- a link or image whose target is missing, untracked, absolute or outside the
  project renders as its text, unlinked, inside `<span class="link-gone">`, as
  in old worklog entries; only tracked files and folders, files of a
  checked-out submodule such as the kit, and declared local evidence count as
  present, so the page does not depend on one checkout's untracked files;
- only PNG, JPEG, GIF, WebP and AVIF images show, as files or `data:`
  addresses; another type, such as SVG, or a symlinked or private image is
  not packaged and renders the same way. To show more, such as SVG figures,
  register the file with a `[[source_pages]]` table;
- an external image becomes a link to it, or its text inside a link; a link
  with a scheme other than `http`, `https`, `mailto` or `vscode` renders as
  text;
- a same-page link to a missing anchor renders as text; a link from or into an
  automatically listed page whose fragment matches no anchor stays a link to
  the page;
- raw HTML keeps only the tags `a`, `abbr`, `b`, `blockquote`, `br`, `code`,
  `del`, `details`, `div`, `dl`, `dt`, `dd`, `em`, `h1` to `h6`, `hr`, `i`,
  `img`, `ins`, `kbd`, `li`, `mark`, `ol`, `p`, `pre`, `s`, `small`, `span`,
  `strong`, `sub`, `summary`, `sup`, `table`, `caption`, `thead`, `tbody`,
  `tfoot`, `tr`, `th`, `td`, `u` and `ul`, and only the attributes `id`,
  `title` and `align`, `href` and `name` on `a`, `src`, `alt`, `width` and
  `height` on `img`, `open` on `details`, `width` on `table`, `th` and `td`,
  and `colspan` and `rowspan` on `th` and `td`. Any other tag and an unclosed
  comment show as text. Any other attribute, a comment, an `id` or `name` that
  the kit's page uses and an end tag that closes nothing the file opened are
  dropped. Addresses are read as browsers read them and then checked like
  Markdown links, so no script runs and nothing loads from outside the bundle;
- a file without a level-one heading takes its file name, without `.md`, as
  title;
- bytes that are not UTF-8 show as the replacement character.

Registered pages keep their strictness. They and topic pages are not
filtered: the promise about raw HTML covers automatically listed files only.
The build prints how many problems it tolerated; `build --check` and lint
list them.

The page's source line links the file in the configured `gh_repo`. A reader
without access to a private repository cannot open that link or the edit link,
although the page itself is public.

### Records outside `docs/`

Lint checks the links, anchors, snippets and figure references of the
Markdown under `docs/` and of `AGENTS.md`, `CLAUDE.md` and `README.md`. A
project that keeps records elsewhere, such as study notes beside their data,
names them in `docs/site/site.toml`, above the first `[[nav]]` table:

```toml
record_roots = ["studies", "CHANGELOG.md"]
record_roots_exclude = ["studies/*/results"]   # optional
```

- `record_roots` lists folders and single Markdown files, as paths from the
  project root. Every tracked `.md` file under them is checked like a record
  under `docs/`: a dead link or anchor and a snippet that left its source are
  errors. So is an image from a folder named `figures/` that has no
  `manifest.json` beside it, in a project that keeps
  [`docs/figures/manifest.json`](#generated-figures). Untracked files,
  symbolic links and tracked files that are absent from the checkout are not
  read. A record that is not UTF-8 text is an error.
- `record_roots_exclude` lists folders, with everything below them, and
  single files that stay out. In an entry `*` stands for one name or part of
  one, so `studies/*/results` leaves out the `results` folder of every study;
  it never spans several folders.

The setting only adds files to these checks. It lists no page: what the site
shows stays with [`reference_roots`](#automatic-reference-listing). Without
`record_roots` nothing outside `docs/` is read. An entry that is no folder or
Markdown file of the project is an error, and so is `record_roots_exclude`
without `record_roots`. A root without tracked Markdown and an exclusion that
leaves nothing out are notes.

### Theme colours

A `[theme_colors]` table in `site.toml` gives the whole site a project's own
colours. Each key is one of the reader's fifteen base colours and each value a
3 or 6 digit hex colour:

```toml
[theme_colors]
bg = "#2b211b"      # the page
bg2 = "#30251e"     # code blocks and panels
panel = "#3a2c23"   # cards
panel2 = "#44342a"  # raised cards
border = "#59493a"
text = "#e6dccd"
bright = "#f2e9dc"  # headings and strong text
muted = "#b3a593"
```

The keys are `bg`, `bg2`, `panel`, `panel2`, `border`, `text`, `bright`,
`muted`, `accent`, `secondary`, `blue`, `link`, `orange`, `red` and `green`; a
key left out keeps the kit's colour. The build writes
`assets/theme-colors.css`, which sets those colours on `:root`, and links it
right after `base.css` on every page: topic pages with and without the reader,
registered and automatically listed Reference pages and the Reference index.
The lock page that `publish` writes and the decks of `slides` link it too.
Without the table, or with an empty one, nothing is written and the site
builds as before.

The theme's other colours, such as the sidebar, the slide faces, the code
block edges, the steps of the sidebar text and the controls that scripts draw
(the lightbox, carousel arrows and dots, plot-toggle chips and the lock page's
notice), are derived: each is a mix of two base colours, listed in
`tooling/theme_colors.py`. The six tones that navigation groups without a
`[group_colors]` colour take in order, and the reader's chapter parts, are
lighter steps of `accent`, `secondary`, `orange`, `blue`, `red` and `green`.
A derived colour keeps the kit's exact value until the project sets one of the
two colours it mixes, so a table that sets only `accent` changes the accent and
the first group tone. The table sets base colours only.

The build checks that the colours keep text readable, with the ratios of the
[figure palettes](#generated-figures): 4.5:1 for text and 3:1 for marks. It
checks the text colours on the page, panel and card surfaces, the accent
colours on the page and on cards, the sidebar text on the sidebar, the
`is-alert` and `is-held` slide tones on a slide tile, and the dark figure
palette on the project's surfaces. A table that fails stops the build and lint
and names each failing pair with its colours and its ratio. The reader is dark,
so a light `bg` fails these checks.

### Generated figures

A figure generator reads tracked data, asserts the values its page states and
writes fragments the page includes; a `--check` mode compares without writing and
runs in the project's checks. `tooling/svg_figures.py` supplies the shared markup:
`figure` (numbered caption and a labelled, keyboard-scrollable region), `slide_svg`
(a face without ids), `standalone` (a file usable as `<img>`, such as a slide
shown as an image) and drawing helpers with a literal colour palette. Generated
SVG uses literal colours: surrounding cards may redefine page variables, and an
SVG loaded as an image cannot read them.

`tooling/figure_themes.py` holds the colours as a dark and a light palette.
The dark one matches the reader; the light one is for slides and print. A
generator writes each figure file in both themes, under fixed names:

| File | Theme | Use |
|---|---|---|
| `<name>.<ext>` | dark | The file a page shows |
| `<name>.light.<ext>` | light | Beside it, for slides and print; no page shows it |

`write_both(path, draw)` calls `draw(colors)` once per theme and writes both
files; `draw` returns SVG text or a matplotlib figure. For matplotlib it runs
inside `matplotlib_rc(theme)`, the settings that colour surfaces, text, axes,
grid, legend and the series cycle, so a generator copies no hex value. Series
take `colors.series` in its order and do not cycle past it; `colors.alert`
marks a problem and is not a series colour. The kit does not depend on
matplotlib.

Both files are generated files: the manifest lists both with the same
script, and `--check` covers both. Lint then counts the light file of a shown
figure as kept, like its raster export; it does not demand one. A fragment
with inline SVG that a page includes stays dark and has no light file;
neither has a hand-drawn figure. `publish` exports only what a page shows;
the local build output copies all of `docs/figures/`, light files included.
In the dark palette violet and blue, the second and fourth series, are close
for a reader with a colour deficiency: label the lines of a chart that shows
both.

A project with [theme colours](#theme-colours) gets dark figures on its own
surfaces: `palette("dark")`, `matplotlib_rc("dark")`, `write_both` and the
`svg_figures` colours take the background, panel, lines and text from the
project's colours. They read `docs/site/site.toml` of the project at
`DOCSITE_PROJECT_ROOT`, or of the working directory, so run a generator from
the project root. The series and alert colours stay the kit's.
`figure_themes.problems` runs the contrast checks above on a palette, and a
project palette that fails them raises an error before any file is written.
`figure_themes.DARK` stays the kit's palette, and the light palette does not
change. After changing the table, run the generators again; until then their
`--check` reports the figures drawn in the old colours.

### Slide faces and decks

Write a chapter's slide face between standalone `<!-- slide -->` and `<!-- /slide -->` lines at the start of the chapter: inside its `section.card`, or directly before its `##` heading on a flat Markdown page. The build converts it into `<div class="slide-face" data-slide-face><div class="slide-canvas">…</div></div>` and loads the shared `slide-face` component automatically. Markdown pages match markers after rendering, so examples inside code blocks stay literal. Unbalanced or nested markers fail the build. Use `p.slide-eyebrow` and `p.slide-title`, not headings: the reader names a chapter by its first heading, which opens the full chapter below the slide.

| Class | Use |
|---|---|
| `slide-lead`, `slide-main`, `slide-scope` | Lead sentence, the flexible visual area, closing scope line |
| `slide-tile` (`is-term`, `is-accent`, `is-warm`, `is-alert`, `is-held`), `slide-tag` | Labelled boxes; emphasised term; dashed held-out or generated item |
| `slide-row`, `slide-steps` | Equal tiles in one row; numbered argument steps |
| `slide-equation`, `slide-column`, `slide-op`, `slide-note` | Terms of a formula with variants listed under each term |
| `slide-factors`, `slide-chip` (`is-key`, `is-alt`, `is-warm`, `is-alert`, `is-held`, `is-mono`) | Labelled rows of options |
| `slide-split` (`is-wide-side`), `slide-figure`, `slide-stats`, `slide-stat` (`is-alt`, `is-warm`, `is-alert`, `is-plain`), `slide-big` | Figure or grid beside headline numbers |
| `slide-points` (`li.is-key`, `li.is-alert`) | Ruled points beside a visual: a bold claim and one or two explaining sentences per `li`, numbered 01, 02 … to match markers on the figure; `is-key` tints the points the title names, `is-alert` marks a warning with a cross |
| `slide-facts` | Closing row of facts, a `dl` of `<div><dt>label</dt><dd>value</dd></div>` |
| `slide-legend` | Line and border keys; on the `figcaption` of a `slide-figure`, the figure's keyed caption |

The outer face is the size container and every size inside the canvas is a container unit of it, so a face fits identically at every width or not at all. Below 720 px a CSS container query stacks the canvas into a readable column, without JavaScript. Canvas declarations are marked `!important` so page-wide element rules (for example an id-scoped `p` style) cannot change the fixed layout; local slide classes must do the same. Open a page with `?slide-check` to outline faces that do not fit; the deck always shows the outline. Projects add local classes for domain diagrams under the same rule. In the reader, the first heading after the face becomes the chapter's bridge title; an eyebrow immediately before it stays only for assistive technology. A Continue/Back control moves between the slide and the full chapter. The reader's Presentation view and the All chapters Slides switch are described under [shared reading layout](reader.md#shared-reading-layout).

`docsite.py lint` reads the built pages and checks two parts of the [slide-face rule](../writing/pages.md#slide-faces). A chapter with more than one face, a face that does not open its chapter and a face outside every chapter are errors that name the page and the chapter. A face opens its chapter when nothing readable comes before it in the chapter; a wrapper element around the face does not count. A number that a face shows and its chapter does not show outside the face is a warning, which fails `lint --strict`, with the page, the chapter and the numbers. The check needs no list from the project: it compares the text a reader sees on the face with the chapter's text, tables, code, figures' SVG text, `noscript` fallbacks and `alt`, `aria-label` and `title` attributes. It treats as one number the same value written with or without thousands separators, with a Unicode or ASCII minus, with or without trailing zeros after the point, and with a percent sign directly after it or after a space; 12% and 12 differ. It does not count integers written with a leading zero such as `01`, numbers after Figure, Fig., Table, Chapter, Section or Appendix, versions such as 1.2.3, and digits that follow a letter, such as `H100`. The [module's description](../../tooling/slide_face_checks.py) gives every case. Numbers in pictures, numbers that a script writes into the page and rounding are not compared.

When a face shows a number on purpose that the chapter does not, wrap exactly that number in an element with the reason, such as `<span data-face-only="rounded from Table 3">0.47</span>`. Lint prints it as a note instead of a warning. A mark that holds no number or more than one, that gives no reason, or whose number the chapter now shows is a warning. The mark is there so that a false finding never forces a rewording; a number the chapter truly lacks belongs in the chapter.

Extract a deck with `python .docs-kit/docsite.py slides --project . --select <slug>[#chapter,…] --out <name> [--title …]`. Repeat `--select` to combine pages; listed chapters keep the given order, a bare slug takes every face in reading order. Chapters are the reader's chapter sections, or the outermost `section.card` elements on pages without the reader. Slide ids are prefixed per slide so pages can share one deck; relative URLs (including `srcset`, `xlink:href` and CSS `url()`) point back into the built site, and links to the rest of a page open that page. Faces from math pages render with the vendored KaTeX. The command builds the site first and writes `.build/slides/<name>.html`, which reuses the built site's assets and stays outside the published bundle. The deck offers an overview, a presentation mode (`P`, arrow keys, `F`, `Esc`) and one-slide-per-page printing for PDF export. Serve `.build/` on loopback to open it.

### Formula check

`docsite.py lint` compiles every formula on the built pages with the KaTeX the
kit ships, the same `katex.min.js` the pages load. It reads each built page
that loads the kit's math renderer and finds the formulas as that renderer
finds them in a browser: in the page's content, outside `pre`, `code`,
`script` and `style`, between `$$` and `$$` or `\(` and `\)`. Three cases are
errors, because each shows as raw text on the page, and each message names the
page's source, the built page and the formula:

- a formula that KaTeX cannot compile, with KaTeX's message;
- a formula that Markdown split with markup, such as an `<em>` that an
  underscore made inside `$…$`;
- an opening delimiter whose closing one is not in the same text, for example
  because a tag or an unbalanced brace comes between them. Write a literal
  `$$` in prose as `$<!-- -->$`.

KaTeX is JavaScript, and building a site needs no Node.js. The check is
therefore the one part of lint that runs Node: `DOCS_NODE` when it is set,
otherwise `node` on `PATH`. A `DOCS_NODE` that names no program is an error.
Without Node, or with a Node that cannot run the compiler, lint prints a note
that says how many formulas were not compiled, and the run passes. A project whose checks must not pass without the formula
check sets, above the first `[[nav]]` table:

```toml
formula_check_required = true
```

Lint then fails in both cases. A value other than `true` or `false`
fails the build. After the check, lint prints how many formulas compiled and
with which KaTeX version. The [module's description](../../tooling/formula_checks.py)
gives the details.
