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
5. **Capability map.** `docs/CAPABILITY_MAP.md`, or the file that
   `capability_map` in `docs/site/site.toml` names, lists each need the
   project's tooling meets, with its code, state and importers, and the needs
   seen but not built with the person's decisions. Where `tooling_roots` is
   set, lint checks that every entry under a tooling root has a row and that
   the Imported by column is current, and warns when a tool imports from an
   experiment folder **(lint)**. Where it is not set, read the tooling
   folders against the map, and propose the setting to the owner. Follow
   [the capability map](engineering/code.md#the-capability-map).
6. **Topics.** Every topic page has a record in its folder or declares
   `page_only` with a reason **(lint)**. No `README.md` exists below the repository root, apart from files that arrive with third-party code ([README is the bounded exception](documentation.md#readme-is-the-bounded-exception)).
   Read each `page_only` reason: if the page states a rule, specification or
   limit, that part belongs in a record. Follow
   [rendered pages are for people](documentation.md#rendered-pages-are-for-people-records-stay-markdown).
7. **Pages and records.** No contract, handoff state, readiness board or long
   chronology sits on a rendered page, and no layout HTML sits in a record.
   Where the site sets `page_number_notes = true`, lint notes list page
   numbers that no linked record states **(lint)**; settle each one.
8. **Open work.** `OPEN.md` holds one-line routes only, each linking its
   owner.
9. **Compatibility layers.** Each kept compatibility form, such as a path
   adapter or an old route, records why it exists and when it can be removed.
   Follow [refactoring over compatibility](engineering/code.md#refactoring-over-compatibility).
10. **Pages that explain changed rules.** For the project's own records,
    `docsite.py lint --since <commit before the upgrade>` lists the pages that
    link to changed sections **(lint)**. For kit guides, the release notes name
    what changed; reread the project pages that link to those guides. Update
    each explanation in the page's own words.
11. **Site.** If the project publishes a site, the build, strict lint and its
    rendered review pass at the widths it supports. Follow the
    [site guides](maintenance.md).

## Report

State the old and new kit commits, each item's result, the files behind each
finding, what was fixed in the upgrade and which open-work routes were added.
Follow [handoffs](engineering/handoffs.md).
