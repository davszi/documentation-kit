# Project conformance check

Run this check when you move a project's kit pin, and when you take over a
repository that uses the kit. It finds where the project has drifted from the
shared rules. Release-specific steps stay in each version's migration guide;
this list applies to every upgrade.

Lint covers the items marked **(lint)**. Check the others by reading the
named files. Report each finding to the project owner with file references.
Fix what the upgrade itself requires. Route other fixes through `OPEN.md` to
their owner instead of changing them in the same deliverable.

## Checklist

1. **Pin.** `.docs-kit` is at a commit on one of the kit's remote branches,
   normally the commit of a release tag, and
   `python .docs-kit/docsite.py lint --project . --strict` passes **(lint:
   pin, links, worklog and open-work format, topic structure)**. Follow
   [the shared kit submodule](engineering/git.md#the-shared-kit-submodule).
2. **Router.** `AGENTS.md` has a row for every row of the starter router
   (`.docs-kit/examples/starter/AGENTS.md.tmpl`) that applies to the project,
   and every path in it resolves. Follow
   [agent entrypoints](documentation.md#agent-entrypoints-import-versus-point).
3. **No copied rules.** Project files hold only project specifics, such as
   commands, thresholds and resource profiles, and link to the kit guide for
   the shared rule. Remove a copied rule only after its project parts have a
   linked home.
4. **Canonical homes.** `docs/PROJECT_CONTEXT.md` and `docs/index.md` exist,
   and the worklog and open work exist where `docs/site/site.toml` names them
   or at their default paths. Follow
   [canonical homes](documentation.md#canonical-homes).
5. **Topics.** Every topic page has a record in its folder or declares
   `page_only` with a reason **(lint)**. No subject record is named `README.md` ([writing records](records.md#one-record-per-topic)).
   Read each `page_only` reason: if the page states a rule, specification or
   limit, that part belongs in a record. Follow
   [rendered pages are for people](documentation.md#rendered-pages-are-for-people-records-stay-markdown).
6. **Pages and records.** No contract, handoff state, readiness board or long
   chronology sits on a rendered page, and no layout HTML sits in a record.
   Where the site sets `page_number_notes = true`, lint notes list page
   numbers that no linked record states **(lint)**; settle each one.
7. **Open work.** `OPEN.md` holds one-line routes only, each linking its
   owner.
8. **Compatibility layers.** Each kept compatibility form, such as a path
   adapter or an old route, records why it exists and when it can be removed.
   Follow [refactoring over compatibility](engineering/code.md#refactoring-over-compatibility).
9. **Pages that explain changed rules.** For the project's own records,
   `docsite.py lint --since <commit before the upgrade>` lists the pages that
   link to changed sections **(lint)**. For kit guides, the release notes name
   what changed; reread the project pages that link to those guides. Update
   each explanation in the page's own words.
10. **Site.** If the project publishes a site, the build, strict lint and its
    rendered review pass at the widths it supports. Follow the
    [site guides](maintenance.md).

## Report

State the old and new kit commits, each item's result, the files behind each
finding, what was fixed in the upgrade and which open-work routes were added.
Follow [handoffs](engineering/handoffs.md).
