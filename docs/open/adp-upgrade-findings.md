# Findings from ADP's upgrade to 3.0.0

Open work. ADP moved from kit 1.1.0 to 3.0.0 on 2026-11-10, on its branch
`upgrade-kit-3.0.0` (commits `05b3b110`, `9123c3ce`, `b44a55d2`). The upgrade
passed ADP's checks. It also showed four gaps in the kit. The evidence is
verified in ADP's upgrade record,
`docs/topics/documentation-site/documentation-site.md`; no fix is decided.

## The 3.0.0 guide sends one link to the wrong guide

The [3.0.0 migration guide](../topics/releases/migrations/3.0.0.md#router-anchors)
maps the old anchor `#run-visuals-and-experiment-lifecycle` to
`rules/writing/figures.md`. In kit 1.1.0 that section also held the experiment
floor: reproduction command, baseline, acceptance bar and regression gate. The
floor now lives in
[required content](../../rules/experiments/workflow.md#required-content). ADP
had a sentence about the floor behind that anchor; following the table pointed
it at a section that only forwards. Lint passed, and an independent reviewer
found it.

Next step: say in the guide that a link about the experiment floor goes to the
experiment workflow guide.

## The reader header shows each page's `brand`

Since the sidebar redesign, the reader's header repeats the sidebar brand, which
is the page's `brand` frontmatter. The kit's own pages all set the project name
there. ADP sets a different value on each page, so its header reads
"track-geometry" or "Shelved vehicle research" where kit 1.1.0 showed the site's
`home_label`, "ADP docs". The header links to the home page.

The guide says only that the drawer shows the project mark and name. No kit
guide defines `brand`.

Open choice, for deivid: the header names the site, from `home_label` or
`title`, and page `brand` goes away; or `brand` stays and the guides define it
as the project name.

## Strict lint cannot pass in ADP

The [conformance check](../../rules/conformance.md) asks that
`lint --strict` passes. In ADP it fails on 19 worklog entries without a commit
hash and on 2 registered local-artifact notices, apart from the topic pages
without a record. The worklog is append-only, so those 19 entries cannot be
changed, and the 2 notices report an intended state.

Next step: decide whether intended notices should count as warnings, and how a
project accepts historical worklog entries.

## The ∿ mark is faint in its box

With `brand_mark = "∿"` the glyph is about 8 px wide inside a box of about
26 px. An independent reviewer judged it faint at 1600 px.

Next step: capture the mark box with one, two and three characters and adjust
the glyph size.
