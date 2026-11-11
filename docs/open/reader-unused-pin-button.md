# The reader script builds a pin button that is never shown

Open work. Found on 2026-11-11 while porting ADP's reader checks into the kit.

## What is there

Verified by reading `theme/components/chapter-reader.js` at `deaac62`:

- Line 193 creates `pinDrawerButton` with the class `reader-drawer-pin`, and
  lines 194 to 197 give it a click handler that toggles docked navigation.
- Lines 260 to 263 update its pressed state, text, title and label on every
  navigation sync.
- No line adds the button to the page. The comment at line 198 says one
  control was chosen: the close button hides navigation and the menu button
  brings it back.

So the button and its updates run on every page and no reader can reach them.
A test that changed the button's pressed state did not fail, which is how this
was found.

## Not decided

Whether to delete the button and its updates, or to show it. Deleting changes
no behaviour a reader sees. It changes the bytes of a shared script, so the
logic tests and the browser suites run before it lands.

## Next step

deivid decides. Until then nothing changes.
