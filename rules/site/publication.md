# Publication export

## Publishing gate

A requested review and any deletion pass their gates first; see [rules for changes and chronology](../documentation.md#rules-for-changes-and-chronology).

Builds on feature branches must not publish production documentation. Publishing requires the consuming project's chosen branch/environment, authorization and successful checks. Hosting source changes are a separate explicit operation; a source build does not imply a deployed version. Rollback must preserve unrelated work and rebuild/verify the chosen revision.

## Configured publication

Run `python .docs-kit/docsite.py publish --project . --out _site` to build the
site and export a fresh public bundle. It builds through the same engine as
`build`. It does not deploy the bundle. Preview only the resulting directory.

Configure publication in the `[publication]` table of `docs/site/site.toml`:

```toml
[publication]
assets_manifest = "docs/site/public-assets.json"
pages = ["index.html", "guide.html"]
private_suffixes = [".md", ".py", ".toml"]
private_prefixes = ["configs/"]
```

All four keys are optional. Any other key fails with an error that names the
supported keys.

- `pages` names the generated HTML files whose source links and media are
  rewritten for the public bundle. Every generated file keeps its name.
- `assets_manifest` names a tracked JSON file with a `files` array of
  repository paths. Each file is published at the same path.
- `private_suffixes` and `private_prefixes` mark repository paths that must not
  be published.

The private checks cover admitted files, generated files and the repository
source of each generated asset or medium. A renamed project asset therefore
cannot hide a private source. Missing, untracked, duplicate or symlinked files
fail.

The output directory must not exist yet. The bundle is written to a temporary
directory next to it and moved into place only after every check passes.
Failed publications leave no output directory.

## Exporting into an existing publication

`tooling/publication.py` exports an already-generated kit bundle into a
project-owned publication directory. It does not build a second site or choose
which repository files are public. Import `export_pages` from the pinned kit's
`tooling` directory after building. Supply:

- `generated_root`, `destination` and repository `root` as explicit paths.
- `tracked` repository paths.
- `public_files`, the tracked repository paths the project publishes at the
  same path. Each must already be in the publication or among the generated
  outputs.
- `pages`, the generated HTML files to rewrite. Every generated file keeps its
  generated name.
- `private_suffixes`, `private_prefixes` and `local_notice` for the project's
  source-link and unavailable-evidence policy.
- `replace` for the exact existing output paths that may be overwritten.
  Byte-identical copies need no replacement permission.

The exporter validates paths, symlinks, public files and collisions before
writing. It points `_media/` sources and source links of public files to their
published path, relative to the page. It modifies actual HTML attributes and
unavailable-evidence anchors; embedded JavaScript/JSON and unrelated source
bytes remain opaque. The shared source-span parser counts LF exactly as
`HTMLParser` does. Keep output selection, historical guide packaging, source
URLs, privacy decisions and deployment credentials in the consuming project.
The generated input is the trusted kit build, not an arbitrary repository
directory.
