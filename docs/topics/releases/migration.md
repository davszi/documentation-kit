# Migrate to the current version

This is the kit's one migration guide. The current version is 6.1.0; the
[release notes](releases.md) say what each version changed. The guide holds
every step from 5.7.0 on, and each step says which versions it is for. A
project on a version before 5.7.0 reads the guides of its versions in the
kit's repository at the tag `v5.9.0`, under
`docs/topics/releases/migrations/`, oldest first, and then this one.

## Prepare the upgrade

Record the old kit commit, the intended new commit, the state of the
project's own sources and the checks that apply to it. Keep a baseline build
to compare against. Protect unrelated edits and active jobs: use a worktree
when the checkout is shared. Follow
[shared Git practices](../../../rules/engineering/git.md) and the project's
own permissions and staging workflow. An upgrade does not authorize unrelated
removals.

## Move the pin

1. Fetch the tag and check it out:

   ```bash
   git -C .docs-kit fetch --tags origin
   git -C .docs-kit checkout v6.1.0
   ```

   `requirements.txt` is unchanged, so the documentation environment needs no
   reinstall.
2. Rebuild and run lint with the project's documentation interpreter, written
   `python` here:

   ```bash
   python .docs-kit/docsite.py build --project .
   python .docs-kit/docsite.py lint --project . --strict
   ```

   The documentation interpreter is the Python 3.12 environment that has
   `.docs-kit/requirements.txt` installed. The project's context file names
   it; a checkout set up as the kit README says has it at
   `.build/docs-env/bin/python`, but a fresh clone or worktree may not. Check
   a candidate with `<python> -c "import mistune, pygments"`; without one,
   create it:

   ```bash
   python3.12 -m venv .build/docs-env
   .build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
   ```
3. In a fresh clone or worktree whose recorded pin cannot be fetched,
   `git submodule update --init` stops with `not our ref`. In the case a
   consumer reported, it still left a clone of the kit in `.docs-kit`, and the
   two commands of step 1 worked in it. When the submodule's `origin` is a local
   path that has moved, correct the URL in `.gitmodules` and run
   `git submodule sync` first.

Done when `git -C .docs-kit describe --tags` prints `v6.1.0` and the build
passes. Lint fails while the pinned commit is on none of the kit's remote
branches; a tag alone does not count. A project that comes from 5.7.0 sees
the warning of the next step until it has decided.

## Decide about the text before each first chapter

Only for a project that comes from 5.7.0; 5.8.0 brought this step.

The reader made a chapter named "Introduction" from the text a topic page has
before its first chapter. That chapter is gone: the text now opens the first
chapter, under that chapter's heading. Strict lint warns for each topic page
that has such text and gives its length in words.

For each page the warning names, look at the built page and choose:

- **Move it.** The text explains something the page needs: give it a chapter
  with a heading that states its point, or put it into the chapter it belongs
  to. The [page types](../../../rules/writing/pages.md#page-types) say what
  a page of each type starts with.
- **Remove it.** The text only repeats what the first chapter says. Removing
  content needs the approval the project's rules ask for.
- **Keep it.** The text is a good way into the first chapter as it stands:
  write `opening = "keep"` in the page's frontmatter. The warning stops for
  that page.

A link to `#reader-introduction` still lands on the text. The page has one
chapter fewer, so a check of the project that counts chapters sees the new
count. Records shown as pages get no warning.

## Repoint the offer of the owner's global instructions

For every project that comes from 5.10.0 or earlier; 6.0.0 brought this step.

The kit's copy of its owner's global agent instructions moved from
`examples/global-agent-context.md` to
`docs/topics/global-agent-instructions/global-agent-instructions.md`, and
nothing is left at the old path. The starter router's section "Offer the kit
owner's global instructions" names the file. A project whose `AGENTS.md`
lacks that section takes the [next step](#add-the-offer-of-the-owners-global-instructions)
instead. Where the project's `AGENTS.md` has that section, replace

```markdown
Once per session, offer the person the snapshot
`.docs-kit/examples/global-agent-context.md` as **Optional: the owner's
global agent instructions** in `.docs-kit/README.md` describes, unless their
global instructions already hold it or decline it.
```

with

```markdown
Once per session, offer the person the snapshot
`.docs-kit/docs/topics/global-agent-instructions/global-agent-instructions.md`
as **Optional: the owner's global agent instructions** in
`.docs-kit/README.md` describes, unless their global instructions already
hold it or decline it.
```

Neither the build nor lint checks this line, because it names the path in
code and not as a link: until it is changed, both pass, and an agent that
follows the offer finds no file at the old path. A file of the project that
links the old path does fail lint with a dead-link error; give such a link
the new path. A person
who already added the copy to their global agent file, or replaced theirs
with it, needs to do nothing for the move. A person who wants the copy now
runs the commands of [the README](../../../README.md#optional-the-owners-global-agent-instructions),
which name the new path.

The copy is now of 2026-11-28 and gains the section "Compacting a long
session". A person who took an earlier copy may replace that part with
this one, with the same commands.

## Add the offer of the owner's global instructions

For every project that comes from 6.0.0 or earlier; 6.1.0 brought this step.

The starter router has carried the section "Offer the kit owner's global
instructions" since 5.1.0. For a project that existed before, the guide of
5.1.0 made adding it optional, so some projects have the section and some do
not. A project without it offers nothing, and an agent working there never
mentions the [copy](../global-agent-instructions/global-agent-instructions.md).
Where the project's `AGENTS.md` lacks the section, add it before the router
table, the section "Read before the relevant action":

```markdown
## Offer the kit owner's global instructions

Once per session, offer the person the snapshot
`.docs-kit/docs/topics/global-agent-instructions/global-agent-instructions.md`
as **Optional: the owner's global agent instructions** in
`.docs-kit/README.md` describes, unless their global instructions already
hold it or decline it.
```

The offer stays an offer: an agent asks and writes nothing to a person's
global file without a yes. A project whose owner has decided against the
offer leaves the section out and says so in its worklog entry for the
upgrade.

Done when the project's `AGENTS.md` holds the section, or the worklog holds
the owner's decision against it. Neither the build nor lint checks this.

## Repoint links to the removed guides

For a project that comes from 5.9.0 or earlier and links a migration guide
of an earlier version; 5.10.0 removed those files.

Until 5.9.0 the kit had one guide per version, under
`.docs-kit/docs/topics/releases/migrations/`. A link from a project's own file
to one of them no longer finds its target. Lint reports each such link as a
note, not as an error, so strict lint still passes, and the build treats
such a link on a record page the same way. The link itself stays as written
and leads nowhere on the built page. Change a link in a current document to
this guide or to plain words that name the tag `v5.9.0`; leave a link in a
worklog entry as it is.

## Update the router row for upgrades

For a project that comes from 5.9.0 or earlier; 5.10.0 brought this step.
The starter router's row for upgrading the pin named
`.docs-kit/docs/topics/releases/migrations/<version>.md`. It now reads:

```markdown
| Upgrading the kit pin or taking over the repository | The kit's migration guide, `.docs-kit/docs/topics/releases/migration.md`, then `.docs-kit/rules/conformance.md` |
```

## Add the router row

Only for a project that comes from 5.7.0 or 5.8.0; 5.9.0 brought this step.

The starter router has one new row. Add it to the project's `AGENTS.md`,
before the row for assigning work:

```markdown
| Discussing a feature, an experiment or a change of direction before work starts | **Discussion before the work** in `.docs-kit/rules/engineering/delivery.md` |
```

[Conformance](../../../rules/conformance.md#checklist) asks for every
starter row that applies to the project. Lint does not check the row.

## Look at three things

Only for a project that comes from 5.7.0 or 5.8.0; 5.9.0 brought these.

- **The sidebar's foot.** Every page now ends its sidebar with a link to the
  project's repository, when `gh_repo` names one, and with a line that links
  the kit, names its version and shows when the site was last built. A
  project that does not want the kit line writes `kit_link = false` in
  `site.toml`; the site then publishes no build time. On a
  [locked site](../../../rules/site/publication.md) the sidebar is sealed
  with its page; only `html/build-info.js`, the build time, stays readable
  without a password.
- **The built site's files.** The build writes `html/build-info.js`. A check
  of the project that lists the files of the built site has to know it.
- **Styles and checks that name the menu's elements.** A menu group is now a
  `details` element with a `summary` for its label, where it was a `div` with
  a `span`. The classes `nav-section` and `nav-group` are unchanged.
  `folded_groups` now names the groups that start closed; every other group
  starts open and can be closed.

## New in 6.1.0

For a project that comes from 6.0.0 or earlier. Beyond the
[step above](#add-the-offer-of-the-owners-global-instructions), nothing a
project must do. What it meets:

- **Open work in the menu of a locked site.** The entry is on by default
  there as well. `publish` cuts it out of every page the general password
  opens and seals it with the Reference section, so it shows as the menu's
  first line once the reference password is in, and a reader with the
  general password sees neither the entry nor its count.
  - A project that does not want the entry writes `open_work_entry = false`
    in `site.toml`. A project that wrote `open_work_entry = true` for its
    locked site can delete the line.
  - A long list shows as a large number to every reader with the reference
    password: this is a good moment to delete finished lines.
  - A project check that reads the published pages a general password opens
    finds no Open work entry in their menu, `#toc > a.open-work`. A check
    that reads the unlocked copy or the built pages finds the entry and its
    link on every page: a check that lists the pages a topic page may link
    has to admit the page of the open-work list. One consuming project's
    check failed on this.

## New in 5.10.0

For a project that comes from 5.9.0 or earlier. Beyond the steps above,
nothing a project must do. What it meets:

- **Open work in the menu.** The menu of every page starts with "Open work"
  and the number of lines in the project's open-work list. A long list shows
  as a large number: this is a good moment to delete finished lines. A project
  that does not want the entry writes `open_work_entry = false` in
  `site.toml`.
  - The number stands on every page, so a changed list makes every page stale
    for `build --check` until the next build, and a `--page` build leaves the
    old number on the other pages.
  - The entry is the first element inside the menu, `a.open-work` in
    `div.toc`. Project styles or checks that take the menu's first element
    have to follow.
  - On a [locked site](../../../rules/site/publication.md) see
    [New in 6.1.0](#new-in-610).
- **Folds.** The option that read "Alternatives" reads "Not chosen". A fold
  whose content is none of math, an experiment, code or an approach not taken
  can be written `<!-- fold: detail Title -->`; moving a misfiled fold is
  optional. All opens every fold.
- **Two new lint notes.** A changed record section that no page links, and a
  numbered figure the text never cites. They list work and fail nothing;
  [reviewing a page against its rules](../../../rules/site/validation.md#reviewing-a-page-against-its-rules)
  says how to take a page through them.
- **Copying a record.** A record page can offer its Markdown to the
  clipboard: `copy_raw = true` on its `[[source_pages]]` table
  ([registered source pages](../../../rules/site/authoring.md#registered-source-pages)).
- **Moved chapters of the kit's site.** A link from a project's own files to
  a chapter of "Documentation and writing" may need the new page; the release
  notes list which chapters moved.

## Optional: the newer copy of the owner's global agent instructions

For a project that comes from 5.7.0 or 5.8.0; 5.9.0 renewed the copy.

The copy, now at `.docs-kit/docs/topics/global-agent-instructions/global-agent-instructions.md`, is renewed. A person who added
the earlier copy to their own global agent file replaces that part with the
new copy; [the README](../../../README.md#optional-the-owners-global-agent-instructions)
has the commands. It gains "Gates" and "Decisions with me".

## What needs no step

For a project that comes from 5.7.0 or 5.8.0; these came with 5.9.0.

The new and changed rule sentences apply to work from now on. The figures
guide asks for a plot where a table compared values; lint cannot check it, so
an existing page is brought in line when it is next worked on. The reader's
changes to a chapter's first view need nothing from a project.

## Land the upgrade

Run the checks in a fresh clone before landing: a link to a file that exists
on one machine but is not tracked passes lint there and fails elsewhere. A
project whose run tooling refuses to start while paths are uncommitted commits
the moved pin first and runs the checks on that commit. Commit the moved pin together with the changes above. Record the old and new
kit commits and the checks in the project's worklog, then run the
[project conformance check](../../../rules/conformance.md) and report its
findings with the decisions that are the owner's.
[Pin and upgrade](../../../README.md#pin-and-upgrade) has the commands.
