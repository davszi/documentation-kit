# Rule proposals from the ADP cleanup

An unresolved choice for deivid. Proposals 1 to 5 were asked on 2026-11-13,
proposals 6 and 7 on 2026-11-14. None is answered yet.
Delete this record and its line in [KIT_OPEN.md](KIT_OPEN.md) when he has
answered and the accepted proposals are written into the rules.

## Question

Which of the proposals below become kit rules? Proposals 5 and 7 are
answered and out, so 1, 2, 3, 4 and 6 remain.

Proposals 1 to 5 name what the ADP cleanup of 2026-11-12 and 2026-11-13 met.
Proposals 6 and 7 come from deivid's reading of an ADP page on 2026-11-14.
None is written into `rules/` yet.

## Proposals

1. **Clean up scratch before reporting completion.** An agent deletes its own
   drafts, review screenshots and test temporary folders before it reports
   completion. A record states the result of a review by eye; it does not cite
   the screenshot by path and hash.
   - Met in ADP: 264 figure drafts and review screenshots that existed only in
     the build folder, 34 of them cited by path and hash in evidence records,
     and 193 small copies of a dependency's source tree in test temporary
     folders.
2. **Dependencies are declared and installed, never loaded from a folder.**
   Every required dependency stands in the project's dependency file. Code
   does not point at a third-party checkout under build output. The setup
   guide produces the environment the project actually runs.
   - Met in ADP: Isaac Lab was not declared, lay in six copies under the build
     folder, the driving code loaded it from a dated run folder, and the setup
     guide gave an environment without it.
3. **A run records its commit and a diff, not a copy of the working tree.**
   Where a copy cannot be avoided, it holds tracked files only.
   - Met in ADP: three runs copied the whole working tree, including an
     ignored folder of old plots, and sealed the copies read-only.
4. **A one-off probe script is finished working code.** Once its result is
   recorded with the source commit, the script is deleted from the tree unless
   a rerun is planned. Git keeps it.
   - Met in ADP: six historical probe scripts break against a changed
     interface, and the project holds many more of their kind.
   - Three gaps to close before this can be a rule, put to deivid on
     2026-11-14:
     - [Numbers and staleness](../../rules/records.md#numbers-and-staleness)
       asks an experiment to retain its producing code, and lets a source pin
       stand for code that "lives in the repository". It does not say whether
       that means the current tree or the pinned commit. The proposal needs
       the second reading written out.
     - The pin only stands for the code when the run started from a clean
       tree. Several ADP runs started from uncommitted code. For those the
       script may be deleted only when a copy or a diff is kept, so this
       proposal depends on proposal 3.
     - "One-off" is not defined. In ADP other code imports probe files: the
       attended judges test imports `test_sdk_app_demo_probe`. A script that
       something else imports is not one-off. Deleting a script also turns
       every claim that rests on it into a historical one, because it can no
       longer be rerun; the rule has to say so.
5. **Withdrawn.** Pictures are chosen, not collected. deivid on 2026-11-14:
   "pictures /galery is adp specific". It is not a kit rule. Whether ADP
   writes it into its own guide is ADP's matter.
6. **A page names the role, not the person.** A page that explains how
   something works says "the developer" or another role word, one word
   throughout. A person's name stays where a record states who decided,
   approved or said something.
   - Met in ADP: the attended-sessions page named deivid in its description,
     two chapter titles, three figures and the cost chapter. deivid: "i dont
     like that its written with deivid instead of developer or similar".
7. **Dropped.** A statement that holds for one case names the case. deivid on
   2026-11-14, after a critical second look he had asked for: "Drop it". The
   reasons: the explanation order is already a rule in
   [explanations](../../rules/writing/explanations.md), an explanation may
   open with a worked example, and the proposal rested on one ADP page whose
   chapter title read as true for every session.

## Recommendation

Write 1, 2, 3 and 6. Write 4 only together with 3 and with the three gaps
closed.

## What waits on the answer

The independent review before the next kit release should see the final rule
text, so the release waits for this answer or for a decision to release
without the proposals.
