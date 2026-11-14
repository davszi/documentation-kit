# Rule proposal from the ADP cleanup: a finished probe script that a change breaks

An unresolved choice for deivid, first asked on 2026-11-13 and put to him in a
narrower form on 2026-11-14. Delete this record and its line in
[KIT_OPEN.md](KIT_OPEN.md) once he has answered and nothing waits on it.

## Question

Do the two sentences below become kit rules?

- In [refactoring over compatibility](../../rules/engineering/code.md#refactoring-over-compatibility):
  a caller that is a finished probe or one-time script, which nothing else
  imports and for which no rerun is planned, is deleted in the same change
  instead of updated, once its result is recorded with a source pin. Claims
  that rest on it are historical from then on.
- In the source-pin paragraph of [numbers and staleness](../../rules/records.md#numbers-and-staleness):
  the pin still stands for the code after the code is deleted from the current
  tree.

## Why this form

The first form was "a one-off probe script is deleted once its result is
recorded, unless a rerun is planned". It had three gaps:

- The source-pin rule did not say whether code "lives in the repository" in
  the current tree or at the pinned commit. The second sentence writes out
  the pinned commit.
- The pin only stands for code when the run started from a clean tree. A
  script from a run with uncommitted code has no such pin, so it is not
  deleted this way; it is updated, or its diff is kept first.
- "One-off" was not defined. It becomes two conditions that can be checked:
  nothing imports the script, and no rerun is planned.

What ADP met was narrower than the first form: a change to an interface broke
six old probe scripts and left them broken. The refactoring rule already asks
a full refactor to update every caller in the same change. It only does not
say what happens to a caller that is a finished probe.

The narrower form creates no duty to search for old scripts that still run.

## Options

- Write the two sentences.
- Leave the rules as they are; a broken probe script is then updated like any
  other caller.

## Recommendation

Write the two sentences.

## What waits on the answer

Nothing in the next release. If accepted before the release, the sentences
join it and its review.
