# Handoffs and progress reports

## Reporting completion

State the outcome first. Include the information the recipient needs to
assess and continue the work:

- What changed and where.
- Checks actually run, their results, and relevant skipped checks.
- Failures, limitations and unresolved questions, with those for the person
  [recorded as unresolved choices](delivery.md#decisions-and-blockers).
- Links to the delivered changes and owning records.
- The next owner and action, when further work remains.

Distinguish work completed from behavior verified. State whether a claim
comes from an executed check, source inspection or an inference.

## Scratch files

Before reporting completion, delete the scratch files the work created.
Scratch is an untracked file, never committed, that the work made for its own
use and that no record, claim, person or delegating agent still needs: a
draft, a capture taken for a review by eye, or a temporary folder of its tests
and tools. Deleting it needs no approval; this is an exception to the
[deletion gate](../documentation.md#rules-for-changes-and-chronology).

These are not scratch:

- The output of an experiment or measurement run, whether or not a stated
  number or verdict rests on it.
  [Numbers and staleness](../records.md#numbers-and-staleness) says which
  output is tracked and which is named in the report with a proposal to delete
  it.
- A tracked file, and a plan, review or other
  [working document](../records.md#finished-working-documents).
- The fixed output folder of a build or check, and the files in it that its
  next run overwrites. A capture written there for a review by eye is still
  scratch.
- A capture that a page uses as a figure.

Keep a capture that the person or a delegating agent is still to look at, and
name it in the report. The agent that reports to the person deletes it once
it has been seen.

Delete only what this work created, delegated work included. Name anything
else that looks unneeded in the report and propose its deletion.

A record does not cite a scratch file by path or hash. It states what the
draft or the review established.

## Reporting blockers

Send blockers through the agreed return channel. Explain what is blocked,
the decisive evidence, what was attempted, and the decision or dependency
needed to proceed.

Report completion through that channel too. A final message in another chat
does not establish that the intended recipient received it.

Follow the [delivery guide](delivery.md#decisions-and-blockers) for escalation
and independent work that can continue.

## Evidence and durable records

Keep detailed results and reproduction information in their owning records,
following the [documentation](../documentation.md) and
[evidence rules](../records.md#numbers-and-staleness). Link those records from
the handoff.

Chat, temporary coordination state and temporary files must not be the only
retained copy of evidence needed for subsequent work.

## Receiving a handoff

Before relying on a consequential claim, check its supporting evidence and
whether its source, inputs and scope match the work being integrated.

Acknowledge receipt when the sender needs confirmation to proceed. Make the
next owner and action explicit when responsibility changes.
