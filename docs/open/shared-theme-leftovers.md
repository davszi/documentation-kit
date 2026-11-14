# Leftovers in the shared theme

Found by the independent review on 2026-11-14. Delete this record and its line
in [KIT_OPEN.md](KIT_OPEN.md) when both points are closed.

- **Series labels of one project.** `theme/components/plot-toggles.js` holds a
  fixed table of labels such as "Menger joints (default)", "road corridor" and
  "κ=0 joints". They look like ADP's plot series. Whether ADP still uses the
  component with these keys is not checked. Next step: check ADP's use, then
  move the labels to the project or let the page supply them.
- **Font notices without a version.** The notices for IBM Plex Mono, IBM Plex
  Sans and Saira Condensed under `theme/assets/vendor/` give the source and
  the download date, 2026-11-01, but no font version. The
  [dependencies rule](../../rules/engineering/code.md#dependencies) and the
  [reader rule](../../rules/site/reader.md#shared-reading-layout) ask for
  source and version. Next step: find each version, from the font files'
  name tables or the Google Fonts listing, and add it.
