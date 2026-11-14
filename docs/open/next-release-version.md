# Version number and migration guide of the next release

An unresolved choice for deivid, asked on 2026-11-14. Delete this record and
its line in [KIT_OPEN.md](KIT_OPEN.md) once he has answered and nothing waits
on it.

## Question

Is the next release 4.0.0, and does it get a migration guide?

## What the release record says

[What a version number promises](../topics/releases/releases.md#what-a-version-number-promises)
makes a release major when it "removes or renames a stable interface,
including a section anchor under `rules/`". The unreleased changes remove the
anchor `#evidence-identity-and-frozen-records` of `rules/records.md`; the
section is now "Finished working documents". By that record the release is
4.0.0.

The theme renames alone would allow a minor release for the class names,
which are a provisional interface. The removed CSS variables `--adp` and
`--ada` stand in neither column of the interface table.

The same record says each version's migration guide gives the step for every
such change. deivid decided on 2026-11-11 to
[remove all migration guides](remove-migration-guides.md) at once, after ADP's
`main` is on kit 3.2.x. That trigger is met: ADP's `origin/main` pins
`f34cf63`, which is `v3.2.1`, since ADP commit `e27e1e97` of 2026-11-11.
Checked on 2026-11-14 against a fetch of 2026-11-12; ADP's local `main`
branch is older and still pins 3.1.0.

## Options

- 4.0.0, with the migration guides removed in the same release as decided,
  and the consumer steps in the release notes.
- 4.0.0 with one more migration guide, and the removal in a later release.
- 3.3.0, which contradicts the version promise.

## Recommendation

4.0.0 with the guides removed in the same release. The removal renames or
removes pages and anchors of its own, so it needs a major release anyway, and
this one already is major.

## What waits on the answer

The release notes, the `VERSION` file, the tag and the push.
