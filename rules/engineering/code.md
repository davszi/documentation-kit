# Code and repository practices

## Logging and program output

Use the project's logging conventions for diagnostics.

When another program consumes stdout or stderr, treat the consumed output as an interface. Keep diagnostics from corrupting that stream and preserve its expected format unless an interface change is agreed.

## Generated files

Identify the source or generator before changing a generated file. Make the change there and regenerate the affected outputs.

Follow the project's toolchain, reproducibility and validation requirements. Keep its rules for which generated outputs are tracked or ignored.

## Dependencies

Declare every dependency the code needs in the project's dependency file and
install it into the environment. Code does not load a third-party library from
a path outside the environment, such as an untracked checkout or a folder
under build output. A copy tracked in the repository is vendored: it carries
its license and a notice of its source and version. A Git submodule pinned to
a commit is a declared dependency that code may load from its checkout, and a
dependency file inside it counts as declared. The environment itself may live in an ignored folder, including one
under build output.

The project's setup guide, followed from a fresh clone, produces the
environment the project runs. When the two differ, correct the dependency file
or the guide.

## Where code lives

An experiment's folder holds only that experiment's own code, inputs and
records. Code that other experiments or tools reuse, such as a run harness, a
supervisor or a judge, lives in the project's tooling or source tree, and the
experiment imports it from there. When a second user appears, move the code
before adding the second import. From a finished experiment, copy it into the
tooling tree instead: the finished experiment keeps its copy, its links and
its [source pin](../records.md#numbers-and-staleness).

## Name the need first

Supporting code is code that runs, supervises, records, judges or prepares
work instead of answering the work's question: a harness, a supervisor, a run
recorder, a judge, a preparation step or a reusable tool. Before building
supporting code, write the need it serves in one sentence that does not
mention the experiment or task at hand, such as "record what a native run
did". Then read the project's [capability map](#the-capability-map).

- When the map lists the need as `exists`, use that code.
- When the need is `partly` met or not listed, add it to the map's list of
  needs seen but not built, with the date and where it came up. Stop building
  and bring the person three options: build it once as a tool in the tooling
  tree, build the minimum inside the experiment, or do not build it. Give for
  each option what it would take and what it leaves out.

In a project without tooling, whose `tooling_roots` is `[]`, no need is
listed yet, so every need goes to the person; the first one recorded starts
the map from the kit's starter template.

Building stays the person's decision; noticing the need is the agent's duty.
Record the decision beside the need in the map. A need the person decided to
build becomes a row; it is `missing` until its code exists.

## The capability map

The capability map lists what the project's tooling does, so that each need is
solved once and found again: a table of needs with their code, state and
importers, and the needs seen but not built with the person's decisions. A
project with tooling keeps it at `docs/CAPABILITY_MAP.md`, or where its
`capability_map` setting names, and every project sets `tooling_roots` in
`docs/site/site.toml` to its tooling folders, or to `[]` while it has none.
Lint fails when the setting is missing, when a file or folder directly under a
tooling root has no row and when the generated column is stale.
[Capability map settings](../site/authoring.md#capability-map-settings) give
the columns, what lint reports and how imports are read.

## Refactoring over compatibility

The project prefers clean refactors to keeping old interfaces working.

Before changing a name, path, format, API, URL or configuration key that
something outside the change may still use, ask the project owner. Such users
include published URLs or packages, other repositories that consume this one,
saved data or historical records that refer to it, and running jobs. Give the
owner what the decision needs:

- what changes and why;
- who or what uses the old form, with evidence;
- what would break, and whether it can be updated in the same change;
- what keeping the old form would cost.

Then wait for the decision.

If the owner decides compatibility is not needed, or nothing outside the change
uses the old form, refactor fully: update every caller and reference in the
same change and remove the old form. Add no aliases, shims, fallbacks, redirects
or deprecation periods.

A caller that is a finished probe or one-time script is deleted in the same
change instead of updated, when nothing else imports it, no rerun is planned
and its result is recorded with a
[source pin](../records.md#numbers-and-staleness) that stands for it. Claims
that rest on it are historical from then on. The deletion is part of the
refactor and needs no separate approval. This holds for a script kept in an
experiment directory too: the pin stands for it, so the directory need not hold
it.

If the owner decides to keep compatibility, record why it exists and when it
can be removed.
