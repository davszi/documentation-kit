# One project's plot labels in the shared theme

Found by the independent review on 2026-11-14. Delete this record and its line
in [KIT_OPEN.md](KIT_OPEN.md) when the point is closed.

- **Series labels of one project.** `theme/components/plot-toggles.js` holds a
  fixed table of labels such as "Menger joints (default)", "road corridor" and
  "κ=0 joints". They look like ADP's plot series. Whether ADP still uses the
  component with these keys is not checked. Next step: check ADP's use, then
  move the labels to the project or let the page supply them.
