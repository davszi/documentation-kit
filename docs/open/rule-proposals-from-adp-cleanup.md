# Rule proposal from the ADP cleanup: delete one-off probe scripts

An unresolved choice for deivid, first asked on 2026-11-13. Delete this record
and its line in [KIT_OPEN.md](KIT_OPEN.md) when he has answered and, if he
accepts, the rule is written.

## Question

Does this proposal become a kit rule?

**A one-off probe script is finished working code.** Once its result is
recorded with the source commit, the script is deleted from the tree unless a
rerun is planned. Git keeps it.

- Met in ADP: six historical probe scripts break against a changed interface,
  and the project holds many more of their kind.

## Three gaps to close first

Put to deivid on 2026-11-14.

- [Numbers and staleness](../../rules/records.md#numbers-and-staleness) asks
  an experiment to retain its producing code, and lets a source pin stand for
  code that "lives in the repository". It does not say whether that means the
  current tree or the pinned commit. The proposal needs the second reading
  written out.
- The pin only stands for the code when the run started from a clean tree.
  Several ADP runs started from uncommitted code. For those the script may be
  deleted only when its diff against the pinned commit is kept, as the same
  section now requires.
- "One-off" is not defined. In ADP other code imports probe files: the
  attended judges test imports `test_sdk_app_demo_probe`. A script that
  something else imports is not one-off. Deleting a script also turns every
  claim that rests on it into a historical one, because it can no longer be
  rerun; the rule has to say so.

## Recommendation

Decide it after the next release. The release does not need it, and the
wording needs a draft that closes the three gaps.

## Answered proposals

This record held seven proposals. deivid answered six on 2026-11-14; the
[worklog](../KIT_WORKLOG.md) has the chronology.

- Written into the rules: [scratch files](../../rules/engineering/handoffs.md#scratch-files),
  [dependencies](../../rules/engineering/code.md#dependencies), the commit and
  diff a run records in [numbers and staleness](../../rules/records.md#numbers-and-staleness),
  and roles instead of names in [page design](../../rules/writing/pages.md#page-design).
- Withdrawn as specific to ADP: pictures are chosen, not collected.
- Dropped: a statement that holds for one case names the case.
