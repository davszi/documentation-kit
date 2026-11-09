# Publication export

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
