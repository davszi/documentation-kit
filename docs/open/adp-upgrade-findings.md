# Findings from ADP's upgrade to 3.0.0

Open work. ADP moved from kit 1.1.0 to 3.0.0 on 2026-11-10, on its branch
`upgrade-kit-3.0.0` (first commit `05b3b110`). The upgrade
passed ADP's checks. It also showed gaps in the kit; four are open here. A
fifth, that strict lint could not pass in ADP, is fixed in 3.0.1. The evidence is
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

## The 2.0.0 guide has no step for the experiment router rows

Kit 2.0.0 added `rules/experiments/workflow.md` and
`rules/experiments/verification.md`, and the starter router has a row for each.
The [2.0.0 migration guide](../topics/releases/migrations/2.0.0.md) does not
tell an existing project to add those rows. ADP had neither row after following
the guide; the conformance check found them, and they were added in ADP's
commit `1b7e0087`.

Next step: add the step to the 2.0.0 guide, or have the conformance check name
router rows as something every upgrade adds.

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

## The ∿ mark is faint in its box

With `brand_mark = "∿"` the glyph is about 8 px wide inside a box of about
26 px. An independent reviewer judged it faint at 1600 px.

Next step: capture the mark box with one, two and three characters and adjust
the glyph size.
