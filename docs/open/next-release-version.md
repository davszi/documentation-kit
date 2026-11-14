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
4.0.0. The theme renames alone would allow a minor release, because theme
class names are a provisional interface.

The same record says each version's migration guide gives the step for every
such change. deivid decided earlier to
[remove all migration guides](remove-migration-guides.md) once ADP `main` is
on 3.2.x. ADP `main` is not there yet.

## Options

- 4.0.0 with a migration guide, as the release record asks today.
- 4.0.0 with the consumer steps in the release notes only, and the sentence
  about migration guides changed in the release record in the same release.
- 3.3.0, which contradicts the version promise.

## Recommendation

4.0.0 with the consumer steps in the release notes only. It follows the
version promise and the earlier decision against migration guides.

## What waits on the answer

The release notes, the `VERSION` file, the tag and the push.
