# Slide-face rule and guide gaps found by the upgrades to 4.0.0

Adaptation moved from kit 3.2.0 to 4.0.0 on 2026-11-14, as three local commits
on its branch `docs-kit-4.0.0`. deivid asked to evaluate what the
[slide-face rule](../../rules/writing/pages.md#slide-faces) does there. The
session followed the rule and the
[guide step](../topics/releases/migrations/4.0.0.md#slide-faces) as written,
with no further direction, and judged every face. Nothing here is fixed.

"Checked here" means the kit owner looked at the session's captures or
compared the claim with the kit's files. The session's full report and its 36
captures are local files outside any repository, in
`~/.config/Claude/side-session-notes/local_bb11e441-a6c1-4093-95f3-b914a9daec12/adaptation-kit-upgrade/`.

## What the rule did

- Adaptation has 36 slide faces: 27 on its Cursor study page and 9 on its
  robotics page. Checked here: the count matches the source.
- The session failed 12 and passed 24. It removed and redrew nothing and
  wrote the decision for its owner as an open decision in adaptation.
- Checked here by eye on all 36 captures: the 12 verdicts hold. Ten failing
  faces show two or three text tiles or boxes on a canvas that is otherwise
  empty; one shows four number tiles and no figure; one lists file names in
  boxes. The 24 passing faces each show a plot, a diagram or a drawing.
- All seven faces that adaptation added between 2026-11-11 and 2026-11-13
  fail. They were written under kit 3.2.0, which asked for "one visual" but
  did not yet say that boxes do not replace it. So this run shows that the
  rule finds such faces at an upgrade. It does not show that the rule stops
  an author from writing them.
- The session decided the 12 by one sentence of the rule, "Boxes do not
  replace the visual". It set the composition requirements aside as notes,
  because read strictly they fail almost every face: 34 of 36 have no lead
  sentence and none uses ruled points or a closing row of facts.

## Where the rule gave two readings

1. **Which requirements make a face fail.** The guide says "list the faces
   that fail with the reason". The rule has two removal conditions and about
   fifteen composition requirements, and neither text says which count.
2. **"Only repeats the title and lead in boxes."** The failing boxes add
   counts such as "12 of 12" and "381 / 432", so the removal sentence, read
   literally, does not reach them.
3. **Number tiles without a figure.** The rule allows "a figure beside
   headline measurements" and is silent on measurements alone.
4. **Drawn boxes.** The rule allows "a project-local drawing" and does not
   say when a drawing whose content is text in boxes is a visual. The session
   passed process flows and failed lists in boxes, a line it drew itself.
5. **The grid exception.** A face that lists each factor's levels in rows
   names options and compares nothing. The session passed it under "a grid
   that compares options factor by factor"; another reader could fail it.
6. **Title as a finding.** A teaching chapter states how something works, and
   an opening chapter may ask a question. The rule covers neither.
7. **"Readable from the back of a room" and "half empty".** Neither has a
   measure. Nine faces carry text of 10.88 px on the 1280 px canvas, and
   several passing faces leave the lower quarter empty.
8. **Existing faces and the person's yes.** Nothing records whether a person
   asked for an existing face, so a review cannot test that part.

## What the guide step leaves out

- A project may bind its faces in checks. Adaptation fixes the face counts in
  a test and hashes the pages in a content baseline; the step does not say
  that removing a face changes those.
- Neither text says where a face is looked at for the review. The session
  used the extracted deck at 1280×720.
- `?slide-check` outlines overflow of the canvas only. Legend text cut off
  inside a figure, on adaptation's face 8, is not flagged.

## Other gaps in the 4.0.0 guide and rules

Reported by the session; only the two marked points are checked here.

1. **Branches and worktrees.** The rule names four cases for a separate
   branch or worktree. Adaptation's checkout was one commit behind its remote
   while its working tree already held that commit's content, so bringing it
   in step needed a reset the session may not run in a shared folder. No case
   covers a checkout that is out of step. Checked here: the working tree
   equals `origin/main` and local `main` is one commit behind.
2. **Move the pin, step 3** calls `.build/docs-env/bin/python`, which a fresh
   worktree does not have.
3. **Finished working documents.** An archived earlier publication and copied
   tool sources are not named, and an experiment plan that a run copies and
   hashes sits between "delete a plan" and "keep protocols".
4. **Run output.** "Each experiment the project reports as complete" has no
   bound; adaptation has more than fifteen.
5. **Tooling imports.** The guide says imports from `.docs-kit/tooling` are
   not stable, while `rules/site/authoring.md` tells projects that
   `tooling/svg_figures.py` supplies the shared figure markup. Five of
   adaptation's generators import it. Checked here: the release notes list
   `tooling/svg_figures.py` as kept, so the two texts disagree.
6. **Names on pages.** No search is given, and the step does not say whether
   a workstation path with a user name inside a data payload is a name on a
   page.
7. **Scratch files.** About thirty preview and review folders of other
   sessions sit in adaptation's `.build/`, and the rule gives no way to tell
   which are still needed.
8. **`--check-reader`.** The guide does not say whether a project without a
   comparison test should add the command.

## Gaps reported by ADP's upgrade

ADP moved from 3.2.1 to 4.0.0 on 2026-11-14 in one local commit. It has no
slide faces, so it adds nothing to the evaluation above. Its session reported
these; only the first is checked here.

1. **Colour navigation groups.** The step does not say what happens to a
   group outside the table. A group whose colour the project sets itself keeps
   it with or without the table; ADP's `Parked` group did. Checked here: the
   kit owner had told ADP that `Parked` needs a line, which was wrong.
2. **Move the pin, step 3.** The same hard-coded `.build/docs-env/bin/python`
   that adaptation met; ADP has no such environment either.
3. **Generated output.** "Change its generator and run it again" gives no
   route when the generator's environment no longer exists.
4. **Search for imports of kit tooling.** The search also finds scripts kept
   as historical evidence, and the step does not say to leave them, as the
   theme step does.
5. **One README.** "Files that arrive with third-party code keep their names"
   does not clearly cover a notice the project wrote itself for vendored data.
6. **Runners that hash changed files.** ADP's resource slot refuses a run
   while the pin move is uncommitted, because the changed path is a directory.
   The session committed the pin first, ran the checks and amended. A note for
   such consumers may help; the cause is ADP's tooling.

## What a redraw under the 4.0.0 rule showed

deivid decided in adaptation's session to redraw six of the failing faces and
remove six. The session did so on 2026-11-14 in its commit `b6e9431`, under
the rule as released in 4.0.0, before the change recorded below reached it.

- Checked here by eye on the six redrawn faces: each now shows its chapter's
  figure, and all six have the same arrangement, a lead, the figure in a box
  on the left and three numbered points on the right. One figure, a grid of
  small cells, cannot be read at slide size, and one is itself a drawing of
  number tiles. The prescribed arrangement produced six faces that look alike.
- Reported by the session, not checked here:
  1. "Reuse the chapter's own figure" has no mechanism. A chapter figure
     carries ids and a face may not, so the session wrote a second fragment
     through `slide_svg` in the kit's tooling, which the 4.0.0 guide calls not
     stable.
  2. A full-width chapter figure drops below 8 px label size in the default
     `slide-split`. `is-wide-side` keeps it readable, but its narrow column
     cannot hold a point of one or two sentences.
  3. A two-line title, a two-line lead, a figure with a legend and three
     points overflow 16:9. Three of six first drafts overflowed.
  4. A figure taller than wide fits no shared layout; the project needed its
     own class.
  5. Removing a face cost a generator change, a fragment, the expected count
     of a check and a hash in the project's location manifest.

## Decided and still owed

deivid decided on 2026-11-14, when asked whether a face with a real visual but
without the prescribed layout is fine: "B must be reworked too cuz we dont want
fixed layouts", and each face needs a "cool and unique layout made as if the
creator was an expert designer". His reference is his own deck "CORE Labs".
Checked here on eight of its slides: label row, title, footer, type and colours
are the same on every slide, and the body differs on seven of the eight.

Done: the slide-face rule no longer prescribes one arrangement. It asks for a
layout that follows the shape of the content, names what the faces share, sets
a designer's standard and says how a review sorts existing faces. This answers
case 1 above.

Owed:

- An independent review of the changed rule before the next release.
- The kit's own four example faces were built to the old prescribed
  arrangement and need the same review.
- Four places still describe the old arrangement and wait for a page agent:
  `docs/topics/writing-practices/index.md` ("Composed from top to bottom"),
  `docs/topics/build-a-site/index.md`, and in the starter
  `docs/topics/guide/guide.md` and `docs/topics/guide/index.md`.
- Cases 2 to 8 above, the three omissions of the guide step and the fourteen
  other gaps.
- A trial of the changed rule on a few of adaptation's faces, to see whether
  it produces better faces and not only finds weak ones.
