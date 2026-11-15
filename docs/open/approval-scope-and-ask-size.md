# Approval scope and ask size: two questions for deivid

Open work. The [approval-failed-open record](../topics/approval-failed-open/approval-failed-open.md)
lists two ideas as under discussion and not rules. Neither is in the kit's
rules. Each is a question only the owner can answer; nothing waits on an
answer.

## Evidence from the record

All measured from ADP's Git history, `main` at `b8b80e0b`, on 2026-11-15;
[numbers.md](../topics/approval-failed-open/numbers.md) gives the source of
each number.

- In the 47 days of the build-up, 2026-09-24 to 2026-11-09, agents added
  354,333 words to plans, the worklog and session notes: 7,539 words per
  calendar day.
- The build-up's records carry 181 approval statements, 177 of them about
  "the user", "owner" or "human". Only 3 of 499 commit messages cite a
  decision; in the cleanup, 80 of 125 do. Several recorded approvals quote
  the answer itself, such as "Oke" and "yes".
- For six large builds, the harness pattern, run output in Git, the frozen
  copies, the recorder, the slot and pool, and the evidence store, the search
  found no approval in Git within seven days before the first file. The
  exception is the attended parts ("lets build it now fully", 2026-11-02).
- The resource slot and pool: two records of 2026-11-05 say "The human
  requested two simulator runs in parallel" and "The human requested updated
  budgets and isolation for two simulator runs". No statement found approves
  the pool, keeper, slot or ledger design, which grew from 751 to 8,151 lines
  that day.
- The developer: "i most probably said yes without seeing or understanding it
  all".

Limits: the approval search reads keywords; approvals given in chat and what
the developer read before answering are not in Git. [Background](../topics/approval-failed-open/background.md#yes-without-reading)
has the full finding.

## Questions for deivid

The options are proposals of the agent that landed the record, to make each
question concrete; none is a recommendation.

1. **Does an approval cover only what the ask itself said?** In the case of
   the slot and pool, a request for two parallel simulator runs was followed
   by a pool, a keeper, a slot and a ledger that no recorded statement names.
   - A: yes; anything the ask did not name needs its own ask, and the record
     of the approval quotes the ask.
   - B: an approval covers the ask and the work it plainly needs; anything
     that adds a new tool or module needs its own ask.
   - C: no rule; [name the need first](../../rules/engineering/code.md#name-the-need-first)
     already stops supporting code before it is built.
   Waits on it: nothing. Where it would live: [handoffs](../../rules/engineering/handoffs.md)
   or [delivery](../../rules/engineering/delivery.md), as the owner decides.
2. **Does an ask state the size of what it would build?** Short answers to
   long proposals approved more than the person read, and no ask stated what
   the work would add.
   - A: yes; an ask names the files and an estimate of the lines it would
     add, and the report after the work states the actual size.
   - B: only an ask for supporting code states its size, next to the running
     total that [show the total](../../rules/experiments/workflow.md#show-the-total)
     asks for.
   - C: no rule; a size estimate made before the work is often wrong.
   Waits on it: nothing.

When the owner answers, the rule goes into its owning guide, the record's
"Not solved or not known" section is updated, and this file is deleted.
