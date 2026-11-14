# Rule proposals from the ADP cleanup

An unresolved choice for deivid. Proposals 1 to 5 were asked on 2026-11-13,
proposals 6 and 7 on 2026-11-14. None is answered yet.
Delete this record and its line in [KIT_OPEN.md](KIT_OPEN.md) when he has
answered and the accepted proposals are written into the rules.

## Question

Which of the seven proposals below become kit rules?

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
   - Needs care: [numbers and staleness](../../rules/records.md#numbers-and-staleness)
     asks an experiment to retain its producing code, and lets a source pin
     stand for code that lives in the repository. The proposal has to say that
     the pinned commit, not the current tree, is what retains it.
5. **Pictures are chosen, not collected.** A run captures only the frames a
   claim or a chosen picture needs. Appearance pictures go into a gallery
   record, each with its description, date, run and commit.
   - Met in ADP: 188 near-identical viewport frames from one run, and 1,659
     images outside Git.
   - Partly covered by [run visuals](../../rules/writing/figures.md#run-visuals-and-experiment-lifecycle).
6. **A page names the role, not the person.** A page that explains how
   something works says "the developer" or another role word, one word
   throughout. A person's name stays where a record states who decided,
   approved or said something.
   - Met in ADP: the attended-sessions page named deivid in its description,
     two chapter titles, three figures and the cost chapter. deivid: "i dont
     like that its written with deivid instead of developer or similar".
7. **The general rule comes before the example, and the example is labelled.**
   A chapter states what holds in every case first. One run, one session or
   one largest case is then shown as an example and named as such in its title
   and caption.
   - Met in ADP: a chapter titled with the 14 steps of the all-parts session
     and a timeline of one session read as what every session requires. The
     code composes a session from the parts it needs. deivid: "u give a
     concrete example which i hopefully dont repeat every time as if it was
     the general case".

## Recommendation

Write 1, 2 and 3: they address the causes of most of the cleanup. Write 4
after its wording is settled against the retention rule. Fold 5 into the
existing run-visuals paragraph as one sentence. Write 6 and 7 into the page
rules: each is one or two sentences and states a correction deivid made.

## What waits on the answer

The independent review before the next kit release should see the final rule
text, so the release waits for this answer or for a decision to release
without the proposals.
