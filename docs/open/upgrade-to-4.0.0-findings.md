# Slide-face rule and guide gaps found by the upgrades to 4.0.0

Open work. Adaptation and ADP moved to kit 4.0.0 on 2026-11-14, and
adaptation's session evaluated the [slide-face rule](../../rules/writing/pages.md#slide-faces)
on its 36 faces. On deivid's word "Fix them now", the gaps in the guides and
rules that the two upgrades reported were closed on 2026-11-15; the
[worklog](../KIT_WORKLOG.md) entry "Close the gaps the upgrades reported in
the guides and rules" lists each case and what was done. The full report of
the evaluation, with the cases as reported, is in Git at this file's path at
the commit before that entry.

What remains: nine questions only the owner can answer, and one trial.

## Questions for deivid

Each question is the owner's; nothing in the kit waits on an answer before
the 5.0.0 release. The recommendation is the kit owner's.

1. **A checkout out of step with its remote.**
   [Parallel work](../../rules/engineering/delivery.md#parallel-work) names
   four cases for a separate branch or worktree. Adaptation's local `main` was
   one commit behind `origin/main` while its working tree already held that
   commit's content; bringing it in step needed a reset, which an agent may not
   run in a shared folder.
   - A: not a case for a worktree; the agent reports the state and asks the
     person to bring the checkout in step.
   - B: a fifth case: work in a worktree from the remote branch.
   - C: the agent moves the branch itself when the working tree already equals
     the remote commit, so nothing is lost.
   Recommendation: A. Moving a shared branch is the person's call, and the case
   is rare. Waits on it: the parallel-work rule.
2. **A workstation path with a user name inside data a page carries.** The
   rule on [names on pages](../../rules/writing/pages.md#page-design) asks for
   role words where a page explains how work is done. Adaptation's session
   asked whether a workstation path with a user name, such as
   `/home/<user>/…`, inside a data payload that a page carries is such a name.
   - A: it is a name on a page; replace the path and regenerate the data.
   - B: it is provenance, not a name in the explanation; the rule does not
     reach it.
   - C: B for the rule, and a separate publication question whether a public
     site shows such paths.
   Recommendation: C. Waits on it: the 4.0.0 guide's step on names, which now
   asks the upgrading agent to report such a case.
3. **What bounds "each experiment the project reports as complete".** The
   4.0.0 step on [run output](../../rules/records.md#numbers-and-staleness)
   asks for each such experiment to have its output tracked; adaptation has
   more than fifteen.
   - A: every experiment ever reported complete.
   - B: the experiments whose numbers or verdicts a current page or record
     states.
   - C: the experiments completed after the project's upgrade to 4.0.0; older
     ones are labelled historical.
   Recommendation: B; a reader relies on those numbers now. Waits on it: the
   run-output step of the 4.0.0 guide.
4. **Whether "two faces share a layout only for content of the same shape"
   holds per page or per project.** The [slide-face rule](../../rules/writing/pages.md#slide-faces)
   says "two faces of a page"; the kit's four example faces were redesigned
   to differ across the whole project. Adaptation's session also met ten faces
   that share "figure across the canvas above one row of text" because a wide
   chapter figure leaves one place to put it.
   - A: per page, as written; a wide figure is a shape, so faces that carry one
     may share the layout.
   - B: across the project.
   - C: per page, and across any deck that combines pages.
   Recommendation: A. The rule stays as it is until deivid decides.
5. **Tones on faces and figures.** The slide rule gives the accent and warm
   tones to the compared methods, `is-alert` to failures and `is-held` to
   held-out items. The kit's own figures use teal for project content, purple
   for the kit and orange for generated output.
   - A: keep both; the slide rule covers faces that compare methods.
   - B: change the rule so that each project assigns its tones one meaning
     each, with `is-alert` and `is-held` fixed.
   - C: change the kit's figures to the rule's meanings.
   Recommendation: B; the rule's aim is one meaning per tone across a
   project. Neither is changed until deivid decides.
6. **A question as the title of a face.** The rule says a title states the
   finding as a sentence; a chapter that teaches now states how something
   works. An opening chapter that poses the page's question is not covered.
   - A: the face states the answer the page gives, never the question.
   - B: an opening face may carry the question.
   - C: a chapter that only poses a question gets no face.
   Recommendation: A, as the page rule asks titles to state the takeaway.
7. **A supported way to put a chapter figure on a face.** A chapter figure
   carries ids and a face may not, so a project writes a second fragment
   through `slide_svg` in `tooling/svg_figures.py`.
   - A: build a marker in the kit that places a chapter figure on its face
     with the ids rewritten.
   - B: name `slide_svg` the supported way, as a provisional interface.
   - C: build nothing.
   Recommendation: B now, A when a second project needs it. Listed among the
   needs seen but not built in the [capability map](../KIT_CAPABILITY_MAP.md).
8. **Project slide classes need `!important`.** Canvas declarations are marked
   `!important` so that page-wide element rules cannot change the layout, and
   a project class must do the same to win.
   - A: move the shared canvas rules into a CSS cascade layer, so that project
     classes win without `!important`.
   - B: keep the rule as documented.
   - C: a scoping class that projects use instead.
   Recommendation: B for 5.0.0, A as a later minor release after a trial on
   adaptation's faces. Listed in the capability map.
9. **The home card picture.** A site-map card falls back to the first image
   of the page body, so removing or changing a face can change a card
   silently.
   - A: a lint note for each card that uses the fallback picture.
   - B: require a `thumbnail` on every page with slide faces.
   - C: nothing; the review by eye covers it.
   Recommendation: A. Listed in the capability map.

## Tooling a project had to build itself for slide faces

Adaptation's session compared the kit at `3dd3e1f` with what the project wrote
for its faces, on 2026-11-15. Built for 5.0.0: the number check and the
one-face-per-chapter check in lint, and the measurements of stacked faces in
`slideFaces`. Still open, as questions 7, 8 and 9 above: a supported way to put
a chapter figure on a face, project slide classes without `!important`, and a
warning when a home card's picture changes.

## Decided and still owed

deivid decided on 2026-11-14 that faces need a layout of their own, "made as
if the creator was an expert designer", and the rule says so. Done: the rule,
the pages that described the old arrangement, and the kit's four example
faces, which deivid accepted on 2026-11-15.

Owed: a trial of the changed rule on a few of adaptation's faces, to see
whether it produces better faces and not only finds weak ones.
