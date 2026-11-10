# An invariant marker inside a code block is rendered as a card

Found by the independent review of the 3.2.1 rule changes on 2026-11-11. Not
fixed.

## The defect

`markers_to_callouts` in `tooling/build.py` rewrites a `**INVARIANT:**` or
`**DON'T-REDO:**` marker wherever it stands at the start of a line. It runs on
the page source before Markdown is rendered, so it does not know about code
fences. A marker at line start inside a fenced code block is turned into a
card, which breaks the block: the reviewer's run of the pattern through the
renderer showed a broken `<pre>` and a stray `</div>`.

The same pattern explains two limits that the rule text now states: an
indented marker, as in a list item or a quote, is not converted, and a marker
without a blank line after it pulls the following lines into its card.

## Why it matters now

Until 3.2.1 the rule said markers must not appear on pages, so nobody had a
reason to show one as an example. The rule now allows marked statements, and
a page that explains the convention may want to show the source form.

Until this is fixed, show an example marker as inline code, not in a fenced
block.

## Related

`lint --registry` lists every line under `docs/` that contains a marker in
its bold form, including a mention inside inline code or a code block. It
over-counts and misses no marker on a page.

## Next step

Decide whether to make the conversion skip code fences, or to do it after
Markdown rendering. Either is a tooling change with a test for a marker in a
fence, in a list item and at paragraph start. Not checked: whether any
consumer page has a marker inside a code block today.
