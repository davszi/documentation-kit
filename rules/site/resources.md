# Site resources and evidence

## Resource closure and evidence

Package only allowlisted tracked inputs actually needed by pages. Do not mirror the repository, include untracked fragments, follow symlinks into unrelated files or upload large local captures automatically. Verify physical closure: referenced CSS, scripts, fonts, figures, media and nested resources must resolve inside the intended bundle or be explicitly declared source/local-evidence links.

Register intentionally retained local media in the project's supported local-artifact manifest or `local_media` configuration. Do not mask a typo or genuinely missing required resource as local evidence. Preserve large recordings and hashes with the producing experiment; publish a tracked poster/keyframe and visible local-capture notice. A deliberately tracked, approved small clip may be packaged. File-mode access to a local recording is not proof that a hosted reader can open it.

`local_artifacts_manifest` in `site.toml` selects a contained, relative regular
file without symlink components. Its default is
`docs/evidence/local-artifacts.json`. If the setting is omitted and that file
is absent, the project has no manifest. An explicitly configured missing file
fails. This setting changes the inventory location, not its schema or the
project's evidence requirements.

A link to a file that the manifest lists under `omitted_files` is a declared
state. When the file is absent, lint prints a note, which never fails, not even
under `--strict`. A missing file that the manifest does not list is an error.

The kit resolves every link with its own rules: a page body from the logical
`docs/html/` origin, a record from its own folder. It loads no project adapter
for paths or evidence, maps no old path to a current file and verifies no
kept copy of an old document. Four settings were removed in 5.0.0: the
adapters `path_resolver` and `evidence_validator`, with the latter the
evidence adapter's `document_origin`; `evidence_manifests`, which declared
collections of copies that had to stay byte for byte; and `legacy_files`,
which mapped single old paths to current files. A `site.toml` that still
names one of the four fails the build, and lint prints the build's error.
They existed so that a project could keep old documents as unedited copies in
its live tree and still pass the link check. A finished
working document is now deleted and cited from Git, as
[finished working documents](../records.md#finished-working-documents) says,
so a link names a current file or a file at its commit. Links in old worklog
entries that name a moved or deleted file stop being checked through
`worklog_links_checked_from`, described below. The
[5.0.0 migration guide](../../docs/topics/releases/migrations/5.0.0.md#remove-the-adapter-hooks) gives
the steps for a project that named one of them.

For generated or sealed content formats, `content_transform` may name a tracked
project module exporting `transform(body, *, metadata, source, root)`. The hook
runs after frontmatter parsing and returns the document body as text, before
shared rendering. It may derive ordinary metadata such as chapter navigation
from the owning source; metadata is validated again afterward. The project owns
source admission, preservation and format-specific tests. This keeps scientific
generators and their immutable outputs separate from current presentation.
Keep `slug` and `page_css` in source frontmatter; the hook cannot change those
structural declarations after page/asset registration.
Use `body_class` for plain project CSS class names when content needs scoped
styles. Common shell, typography and reader behavior stay in the kit.

An existing project may set `worklog = "docs/development/worklog.md"` to retain
its canonical history path, and `open_work` to name its open-work file. Both
remain project-owned; configured paths must stay inside the repository. New
projects use `docs/worklog.md` and `docs/open/OPEN.md`.

A project may set `worklog_links_checked_from = "YYYY-MM-DD"`. Lint then checks
links only in worklog entries dated on or after that day. Worklog entries are
append-only, so a link in an older entry cannot follow a later move or removal
of its target. An entry is a `## ` section whose heading starts with its date; a
`## ` section without a date belongs to the dated entry above it. Text above the
first dated heading is always checked. A value that is not a date fails the
build, and lint prints the build's error.

The build applies the same day when the worklog is also rendered as a
[registered source page](authoring.md#registered-source-pages). In an entry
dated before it, a link or image whose target is gone does not fail the build:
the page shows its text, or an image's alternative text, unlinked and marked
with a dotted underline, `<span class="link-gone">`. A link in such an entry
whose target exists stays a link, and a fragment that no longer matches an
anchor of a registered page is not checked. In entries from that day on, a
missing target fails the build as on any registered page.

Validate [generated-figure provenance](../writing/figures.md#figures-and-comparisons) separately from link resolution and presentation. A hash that a record states for a document is checked against the document at its commit in Git, as [finished working documents](../records.md#finished-working-documents) says.
