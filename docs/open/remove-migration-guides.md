# Remove the migration guides once ADP is on 3.2.x

deivid decided on 2026-11-11: remove all migration guides at once, after
ADP's `main` is on kit 3.2.x. The trigger is met since 2026-11-11; the removal
is not done yet and is proposed for the
[next release](next-release-version.md).

## Why

The kit has two consumers, ADP and adaptation, and one coordinator moves
both. A guide per release has no other reader. The five guides hold 628
lines, and each release adds a guide file, a navigation entry, a registered
source page and a browser-test entry. Four of the six gaps that adaptation's
upgrade met are text in old guides; see
[adaptation's findings](adaptation-upgrade-findings.md).

The public repository shows no fork, star or watcher on 2026-11-11. Clones
are not visible.

## Trigger

ADP `main` pins a 3.2.x kit commit. ADP's `origin/main` pins `f34cf63`
(`v3.2.1`) since ADP commit `e27e1e97` of 2026-11-11, checked on 2026-11-14.
An earlier version of this record read ADP's stale local `main` branch, which
still pins `f970494` (3.1.0), and so called the trigger unmet.
Adaptation is on 3.2.0 and pushed.

## What changes in the kit

- Delete `docs/topics/releases/migrations/1.1.0.md` to `3.2.0.md`. They stay
  at tag `v3.2.1`.
- Release notes keep what each version changed. From then on a release that
  needs steps lists them in its own release-notes section.
- Remove or reword the references: `README.md`, `docs/KIT_CONTEXT.md`,
  `docs/KIT_INDEX.md`, `docs/site/site.toml` (navigation and source pages),
  `docs/topics/releases/releases.md`, the router row in
  `examples/starter/AGENTS.md.tmpl`, the release routes in
  `tests/own_site_review.cjs`, and the sentence in "What a version number
  promises" that names the version's migration guide.
- Decide the version. Consumers link to the guide files, so a pin move to a
  kit without them makes their lint report dead links. Under the kit's own
  promise that is not a patch.

## What changes in each consumer, in the same pin move

Consumers link to the guides for two reasons, both of the kit's making:

- The router row "Upgrading the kit pin", which the starter template gave
  them: ADP `AGENTS.md:25`, adaptation `AGENTS.md:26`. Reword it to name the
  release notes.
- The adoption record, which cites the guide each upgrade followed: ADP
  `docs/topics/documentation-site/documentation-site.md` (five links),
  adaptation `docs/development/documentation.md:84` (one link). Repoint each
  to the tagged copy on GitHub, or name the guide and its tag in plain text.

ADP's frozen `docs/evidence/history/2026-11-09-retention-review.json` lists a
guide path as data. It is a frozen record and stays as it is.

## Not checked

Whether lint treats the path in that JSON file as a link. Whether the stale
clone `/home/deivid/dev/adaptation`, detached on kit 0.1.0, is still needed.
