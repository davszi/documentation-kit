# Publication export

## Exporting into an existing publication

`tooling/publication.py` exports an already-generated kit bundle into a
project-owned publication directory. It does not build a second site or choose
which repository files are public. Import `export_pages` from the pinned kit's
`tooling` directory after building. Supply:

- `generated_root`, `destination` and repository `root` as explicit paths.
- `tracked` repository paths and `public_files`, a repository-to-public path
  mapping admitted by the project and already present in the publication.
- `page_routes` for generated-to-public paths and `pages` for output HTML to
  rewrite. Unmapped generated outputs retain their names. Relative links account
  for moved pages and their unchanged siblings.
- `private_suffixes`, `private_prefixes` and `local_notice` for the project's
  source-link and unavailable-evidence policy.
- `replace` for the exact existing output paths that may be overwritten.
  Byte-identical copies need no replacement permission.

The exporter validates paths, symlinks, mapped resources and collisions before
writing. It modifies actual HTML attributes and unavailable-evidence anchors;
embedded JavaScript/JSON and unrelated source bytes remain opaque. The shared
source-span parser counts LF exactly as `HTMLParser` does. Keep output selection,
historical guide packaging, source URLs, privacy decisions and deployment
credentials in the consuming project. The generated input is the trusted kit
build, not an arbitrary repository directory.
