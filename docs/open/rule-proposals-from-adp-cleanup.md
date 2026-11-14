# Rule proposals from the ADP cleanup

An unresolved choice for deivid. Proposals 1 to 5 were asked on 2026-11-13,
proposals 6 and 7 on 2026-11-14. None is answered yet.
Delete this record and its line in [KIT_OPEN.md](KIT_OPEN.md) when he has
answered and the accepted proposals are written into the rules.

## Question

Which of the proposals below become kit rules? Proposal 5 is withdrawn, so
six remain.

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
7. **A statement that holds for one case names the case.** Reworked on
   2026-11-14 after deivid asked for a critical second look ("7 im not sure
   yet iterate on it think ciritcally").
   - First wording, now dropped: "The general rule comes before the example,
     and the example is labelled."
   - Why it was dropped:
     - The order is already a rule. [Explanations](../../rules/writing/explanations.md)
       orders a page as purpose, prerequisites, ingredients, mechanism,
       examples, evidence and limits. The ADP page did not misorder the
       mechanism; it left it out.
     - "Rule first" is wrong as a general demand. An explanation may open
       with a worked example, and [figures](../../rules/writing/figures.md#figures-and-comparisons)
       prefers a worked construction.
     - The caption in ADP did name its case ("an all-parts session"). The
       chapter title did not: it said "clicks 14 required steps" as if that
       held for every session.
   - What remains, as one sentence for
     [naming and honest claims](../../rules/records.md#naming-and-honest-claims):
     a heading, lead or caption that holds for one case names that case, and
     where cases differ the text says what decides the difference.
   - Against even that: it rests on one page, and a writer who skipped the
     existing order rule may skip this one too. Dropping proposal 7 entirely
     is a defensible answer.
   - Met in ADP: a chapter titled with the 14 steps of the all-parts session.
     The code composes a session from the parts it needs. deivid: "u give a
     concrete example which i hopefully dont repeat every time as if it was
     the general case".

## Recommendation

Write 1, 2, 3 and 6. Write 4 only together with 3 and with the three gaps
closed. Write 7 as the one sentence above, or drop it.

## What waits on the answer

The independent review before the next kit release should see the final rule
text, so the release waits for this answer or for a decision to release
without the proposals.
