# Plot toggle chips in the zoomed figure

Seen on 2026-11-14 in the review captures for the `[plot_toggle_labels]`
change, on a test page at 1600 and 390 pixels wide. Both points are older than
that change. Delete this record and its line in [KIT_OPEN.md](KIT_OPEN.md)
when both are closed.

- **Grey dots.** On the page each chip's dot has the colour of its series. In
  the zoomed figure every dot is grey, the fallback `#9aa4b2` of `strokeOf` in
  `theme/components/plot-toggles.js`. Likely cause, not confirmed: the
  lightbox builds the chips from its copy of the figure before the copy is in
  the page, so the computed stroke is empty. Next step: confirm, then read the
  colour from the page figure or build the chips after the copy is attached.
- **A long label wraps.** At 390 pixels the chip "Menger joints (default)"
  breaks into two lines in the zoomed figure's chip bar. Next step: decide
  whether the chip keeps one line and the bar scrolls, or the wrap stays.

ADP is the only known project that uses the component, on four pages.
