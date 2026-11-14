# Release 4.0.0 waits for the go to tag and push

Delete this record and its line in [KIT_OPEN.md](KIT_OPEN.md) when the release
is tagged and pushed.

## Settled

- **Migration guides stay.** On 2026-11-14 deivid was asked whether to release
  as 4.0.0 with the migration guides removed in it. His answer: "no we still
  need migrations sadly". The removal he had decided on 2026-11-11 is
  withdrawn, and the next release gets a migration guide like the ones
  before it.
- **The version is 4.0.0.** [What a version number promises](../topics/releases/releases.md#what-a-version-number-promises)
  makes a release major when it "removes or renames a stable interface,
  including a section anchor under `rules/`". The unreleased changes remove
  the anchor `#evidence-identity-and-frozen-records` of `rules/records.md`.
  deivid has not named the number himself; it follows from that record.

## What waits

deivid's go for the tag and the push. A push to `main` publishes the kit's
site. Before asking: the release notes and the 4.0.0 migration guide, the
`VERSION` file, and the full check run with the browser suites on the final
state.
