# Ownership and delivery

## Assigning work

For delegated or parallel work, define the deliverable, scope, required inputs,
file or module ownership, and completion condition. Identify the recipient and
agreed return channel.

Scale the assignment detail to the work. A small, self-contained task can use
a short brief.

## Owner responsibility

The assigned owner completes implementation, focused checks, routine fixes,
associated documentation and evidence, and any review required by the project.

Routine work within the agreed scope needs no separate coordinator approval.

## Delegating a page for people

A page for people follows its record, as [record first, page on request](../documentation.md#record-first-page-on-request) describes. Where the runtime supports delegation, page work larger than a small sync is delegated, and this assignment replaces the working agent's own page writing:

- The brief holds the finished record, the person's request or the record change the page must follow, the pages and chapters to change, and the completion condition: the [validation](../site/validation.md#validation-and-review) that applies to the change, including captures at the supported widths and reader views.
- The brief also names the guides the page author must read before writing. A delegated agent knows only what its brief says, so name them: [rendered pages are for people](../documentation.md#rendered-pages-are-for-people-records-stay-markdown), and the applicable [page guides](../writing.md) and [site guides](../maintenance.md).
- The page author reads those guides and writes in its own words, within [what a page may add](../documentation.md#rendered-pages-are-for-people-records-stay-markdown). A gap or contradiction it finds in the record goes back to the delegating agent, who gets the record fixed first.
- The delegating agent looks at the captures before reporting the work done, under the [by-eye review](../site/validation.md#validation-and-review).
- Keep the same page agent for further page work in the same task, so it keeps what it has read.

## Coordination and integration

When a coordinator is needed, it handles overall goals, priorities,
dependencies, questions and ownership conflicts.

When changes from several owners need integration, identify who combines them,
checks the integration and handles landing. Apply the shared Git rules.

## Parallel work

Preserve other contributors' changes. Coordinate overlapping edits and protect
active work from conflicting changes to its source, inputs, dependencies,
execution settings and outputs.

Work alone happens in the project's checkout on its current branch. Use a
separate branch or worktree only when other work changes the same repository
at the same time, when a running job depends on files the work would change,
when the project's workflow asks for one, or when the person asks for one. Coordinate restrictions around the actual conflict so unrelated
work can continue.

## Decisions and blockers

Escalate changes to agreed goals, design, scope or acceptance requirements.
Resolve ownership conflicts with the affected owners.

Report resource-limit hits and recurring unexplained failures. Seek a decision
when the next approach exceeds agreed scope or limits.

Respect explicit stops and required approvals. Continue independent authorized
work where possible. Obtain the relevant decision before reopening deferred
work.

A question for the person must not exist only in chat. Before stopping work
or reporting completion, write each question the person has not answered into
the open owner as an unresolved choice, under
[open work](../documentation.md#from-open-work-to-subject-knowledge): the
question, the options, the recommendation and what waits on the answer, routed
from `OPEN.md`. A delegated owner sends such a question through the agreed
return channel; the agent that reports to the person records it. When the
person answers, record the answer where the work continues and delete the
entry once nothing waits on it.

Ask only what changes the work. Routine choices within the agreed scope are
made and reported, as [owner responsibility](#owner-responsibility) states.
