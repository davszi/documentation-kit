# Site resources and evidence

## Resource closure and evidence

Package only allowlisted tracked inputs actually needed by pages. Do not mirror the repository, include untracked fragments, follow symlinks into unrelated files or upload large local captures automatically. Verify physical closure: referenced CSS, scripts, fonts, figures, media and nested resources must resolve inside the intended bundle or be explicitly declared source/local-evidence links.

Register intentionally retained local media in the project's supported local-artifact manifest or `local_media` configuration. Do not mask a typo or genuinely missing required resource as local evidence. Preserve large recordings and hashes with the producing experiment; publish a tracked poster/keyframe and visible local-capture notice. A deliberately tracked, approved small clip may be packaged. File-mode access to a local recording is not proof that a hosted reader can open it.

Projects with existing historical-path or evidence schemas can register local
Python adapters using `path_resolver = "tools/docs/site_paths.py"` and
`evidence_validator = "tools/docs/evidence_documents.py"` in `site.toml`.
Adapter files must be tracked, contained regular Python files without symlink
components. They execute as project tooling, so review them with configuration.
The path adapter exports `resolve_legacy_path(path, root, *, recorded_roots=())`
and owns the complete mapping, including generated documentation paths. The
evidence adapter exports `MANIFESTS`, `manifest_documents(root, *, require_all_manifests=False)`
returning `(documents, revisions)`, and `verify` with the same arguments; invalid
evidence raises `ValueError`. Projects keep adapter tests and schema policy;
the kit keeps one build/lint engine and uses the adapters consistently.

The evidence adapter may also export `document_origin(path, *, root)`. Return
the registered repository origin for an exact source snapshot, or `None` to
retain the normal manifest/current-file origin. The project validates the
snapshot's identity and recorded origin before returning it; the kit rejects
origins outside the project or through symlinks. This supports several saved
copies of one source without changing their original bytes. Links, anchors and
snippets remain checked from the recorded source location; this hook does not
exclude a file from lint or grant historical execution permission.

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
its canonical history path. The worklog remains project-owned; the configured
path must stay inside the repository. New projects use `docs/worklog.md`.

Validate [generated-figure provenance](../writing/figures.md#figures-and-comparisons) and [frozen-document identities](../documentation.md#evidence-identity-and-frozen-records) separately from link resolution and presentation. Follow the frozen-record preservation rules when resolving lint failures.
