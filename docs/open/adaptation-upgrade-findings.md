# Kit gaps found by adaptation's upgrade to 3.2.0

Adaptation moved from kit 1.1.0, with a pin to the unpushed kit commit
`101cea4`, to 3.2.0 on 2026-11-11. Its session reported six cases where the
kit or a migration guide did not cover what it met. None blocked the upgrade.
Not fixed.

"Checked here" means the kit owner compared the claim with the kit's files.
The failures themselves were run by adaptation's session, not here.

## The cases

1. **2.0.0 guide, configured publication.** A consumer that used the
   publication keys of `101cea4` gets no steps. The build stops with
   `Unsupported [publication] keys: files, page_routes, retired_routes`, then
   with `Publication pages must name generated HTML outputs`. Kit commit
   `844c665` says "The migration guide lists adapt's steps"; the released
   guide does not. Checked here: `retired_routes` and `[publication.files]`
   are absent from the guide, and `page_routes` appears once, under
   publication export. Steps that worked for adaptation: remove the three
   keys, make `pages` name generated files, list each relocated file in the
   asset manifest at its repository path, delete the entry page and the
   retired-route file, and update project checks and prose that name the old
   public paths. The owner approves the address changes first.
2. **2.0.0 guide, kit changes and the pin.** No advice for a fresh clone or
   worktree whose old pin cannot be fetched. `git submodule update --init`
   fails with `not our ref`, yet leaves a clone in which
   `git -C .docs-kit checkout <tag>` works. A submodule whose `origin` is a
   local path also needs `git submodule sync`. The guide says "pin v2.0.0";
   with cumulative guides a consumer pins the target release directly.
3. **3.0.0 guide, versioned asset URLs.** The note on
   `assets/<file>?v=<hash>` speaks of generated-page diffs only. A project
   check that compares asset names fails; it should compare the URL path.
4. **Release notes, `assets/home.css`.** The stylesheet was in every bundle
   built with 1.1.0 and is packaged in 3.2.0 only for a page that selects it.
   No release note says so. Checked here: no file under
   `docs/topics/releases/` mentions `home.css`. Not checked: which release
   changed it.
5. **Tooling imported as a library.** `tooling/site_paths.py` takes the
   project root from `DOCSITE_PROJECT_ROOT` or the working directory, and
   `expand_includes` records a missing include without raising. A project
   test that imports `build` passes from the repository root and fails from a
   subfolder. Checked here: the variable is set by `docsite.py` and is not
   mentioned in `rules/`, the README or the release pages. Importing the
   tooling is not among the stable interfaces; the choice is to say so, to
   document the variable, or to make the library path fail loudly.
6. **3.0.0 guide, topic records.** "A sentence or two is a small sync"
   assumes a page can take a link to its record freely. Adaptation locks page
   words by hash in a project baseline, so the link needs an approved content
   revision. A clause for projects that lock page content would cover it.

## What worked

The 3.0.0 link searches found the same broken anchors as lint; the
topic-record warning and the `page_only` text were clear; the 3.1.0 header
name and the 3.2.0 "without the new settings" steps matched the build; the
shallow-checkout exemption let the hosted lint pass.

## Next step

Cases 1, 2, 3 and 6 are guide text. Case 4 is a release note that first
needs the release found. Case 5 is a decision about an interface. Each
change waits for deivid's word.
