# Migrate to the next release

This guide applies the [unreleased changes](../releases.md#unreleased--source-pages-kit-website-and-experiment-guides)
to an existing 1.1.0 consumer. The release number is not yet decided. Prepare
the upgrade as in the [1.1.0 guide](1.1.0.md#prepare-the-deliverable): record
the old and new kit commits, keep a baseline build and follow the project's
permissions and staging workflow.

Two compatibility forms are removed, following
[refactoring over compatibility](../../../../rules/engineering/code.md#refactoring-over-compatibility).
A consumer that uses neither needs no change.

## Local-artifact manifest location

The build no longer reads `docs/project/local-artifacts.json` when
`docs/evidence/local-artifacts.json` is absent.

1. Check whether the project has `docs/project/local-artifacts.json` and no
   `local_artifacts_manifest` setting in `docs/site/site.toml`.
2. If so, move the file with `git mv docs/project/local-artifacts.json docs/evidence/local-artifacts.json`
   and update every reference to the old path.
3. Run the build and lint; both must find the manifest at its new path.

## Publication export

`export_pages` no longer renames generated files or relocates public files.

1. Remove the `page_routes` argument. Every generated file is published under
   its generated name; the site's front page is `index.html`.
2. Pass `public_files` as a list of tracked repository paths. Each is published
   at that same path. Move or stop publishing files that were published under
   another name, and update links and tests that used the old public paths.
3. Run the project's packaging and its rendered-page checks.
