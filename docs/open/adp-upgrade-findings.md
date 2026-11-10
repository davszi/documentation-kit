# Findings from ADP's upgrade to 3.0.0

Open work. ADP moved from kit 1.1.0 to 3.0.0 on 2026-11-10, on its branch
`upgrade-kit-3.0.0` (first commit `05b3b110`). The upgrade
passed ADP's checks. It also showed five gaps in the kit. Two are open here.
Three are fixed in 3.0.1: strict lint could not pass in ADP, and each of the
2.0.0 and 3.0.0 migration guides lacked one instruction. The evidence is
verified in ADP's upgrade record,
`docs/topics/documentation-site/documentation-site.md`; no fix is decided.

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
