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
before adding the second import. A finished experiment is not edited for the
move: its [source pin](../records.md#numbers-and-staleness) stands for the
code it ran.

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

Building stays the person's decision; noticing the need is the agent's duty.
Record the decision beside the need in the map. A need the person decided to
build becomes a row; it is `missing` until its code exists.

## The capability map

The capability map is a record each project keeps at `docs/CAPABILITY_MAP.md`,
or at the path that its `capability_map` setting names. It lists what the project's tooling does, so that each need is solved once and
found again. It has two parts.

The first is one table with the columns Need, Code, State and Imported by.
Each row is one need:

- **Need:** one sentence that names no experiment, such as "record what a
  native run did".
- **Code:** a Markdown link to each file or folder that meets the need, or
  `—` when no code exists.
- **State:** `exists`, `partly` or `missing`. A `missing` row links no code;
  the other two link at least one path.
- **Imported by:** generated, never typed. The tracked Python files that
  import the linked code, each named by its path. A user inside a tooling
  root is named by the file or folder directly under that root, and a user
  inside an experiment folder by that folder. `no Python imports` means no
  Python file imports it; `not scanned: no Python code` marks a row whose
  code has no Python file. `python .docs-kit/docsite.py capability-map
  --project .` rewrites this column and changes nothing else in the file.
  Run it after adding a row or changing an import.

The second is a list of the needs that were seen but not built. Each entry
gives the need in one sentence, when and where it was seen, and the person's
decision with its date. An entry whose decision is still open says where the
question waits.

### The check

The check is off until a project names its tooling folders in
`docs/site/site.toml`; the [settings](../site/authoring.md#capability-map-settings)
say how. A project that sets none of them is not checked. When it is on,
`docsite.py lint` fails on each of these as an error, and so does every check
that runs lint, such as a project's build workflow:

- the map is missing or not tracked by Git;
- a tracked file or folder directly under a tooling root is linked from no row
  of the table; names that start with a dot and `__init__.py` are exempt;
- a link in the map is dead, wherever the project keeps the map;
- the Imported by column differs from what the command would write;
- a row has a state other than the three above, or a state that does not
  match its Code column.

A Python file under a tooling root that imports from a folder under an
experiment root is a warning, which fails `lint --strict`. The warning names
the importing file and line and the imported path. Move the reused code into
the tooling tree, as [where code lives](#where-code-lives) says.

The Imported by column and the import warning read Python `import` and
`from … import` statements only, those inside functions included. A name
resolves against the importing file's folder, the project root and each
tooling root, in that order, and a relative import against its package. Not
covered: code loaded by file path, as with `importlib` or `__import__`; code
run as a command or a subprocess; imports that resolve only through some
other `sys.path` change; and every language other than Python, such as shell scripts, Node or C++.
When such users matter, name them in the map's opening text.

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
