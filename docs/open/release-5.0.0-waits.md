# Release 5.0.0 waits for deivid

Open decision, for deivid. Raised on 2026-11-15. The release is prepared on
the branch `integration-next`: [release notes](../topics/releases/releases.md#500--reference-section-by-default-page-lock-and-presentation-view),
[migration guide](../topics/releases/migrations/5.0.0.md) and `VERSION`
5.0.0. Nothing is tagged or pushed.

## What waits on deivid

1. **The go to tag and push.** The tag `v5.0.0` and the push of the kit to
   `main` wait for deivid's go. The push publishes the kit's own site.
2. **The version number.** 5.0.0 is the kit owner's recommendation. deivid has
   not confirmed it. The reasons are in the release notes: the automatic
   Reference listing changes a default so that a site publishes content it did
   not publish before, and `publish` now refuses a `[[source_pages]]` table
   whose file the private prefixes or suffixes cover. Two of deivid's own
   decisions of 2026-11-15 add major changes on their own: the removed path
   and evidence adapter hooks ("remove all 3"), and the new lint error for a
   dead HTML link to a repository file ("add it"). With them a 4.1.0 is no
   longer possible under the promise as written.
   - If deivid chooses 4.1.0, the rename touches `VERSION`, the release notes
     section and its anchor, the migration guide's file name and title, and
     the links to them in `README.md`, `docs/KIT_CONTEXT.md`,
     `docs/KIT_INDEX.md`, this record and the worklog entry "Prepare release
     5.0.0".
   - The publish refusal is a new failure for a project that passed before.
     Under [what a version number promises](../topics/releases/releases.md#what-a-version-number-promises)
     that alone makes a release major. A 4.1.0 therefore also needs a decision
     that the refusal corrects a defect: `private_suffixes` and
     `private_prefixes` already said that such files must not be published.
3. **The source-link fix branch.** `fix/local-source-links-20261114` (commit
   `108ea6b`) is merged into `integration-next` in `ee5ae78` and is part of
   the release state. deivid approved publishing that branch and pinning a
   consuming project to it on 2026-11-14. He has been told that it is merged
   into the release, but he has not said in words to merge it. If he does not
   want it in the release, the merge is undone before the tag.

## Points known open

These are known on 2026-11-15 and are not fixed in 5.0.0:

- **Reference titles for general-password readers.** With the page lock, a
  page that the general password opens can still link to a Reference page,
  through a `[[nav]]` entry, a site-map card or a link in the text. The link's
  text and address stay visible. `publish` counts such Reference pages in its
  summary; [page lock](../../rules/site/publication.md#page-lock) lists it
  among the limits.
- **Links outside the bundle without a remote.** With `gh_repo = ""`, a link
  to a tracked file that is not admitted keeps its local path, which leads
  outside the published bundle. See
  [tooling and ownership](../../rules/site/authoring.md#tooling-and-ownership).
- **Raw HTML on registered pages.** Only automatically listed pages are
  filtered for raw HTML. A `[[source_pages]]` file can still carry a script or
  load outside content.
- **Browsers.** The kit's checks run in Chromium only. The page lock's
  browser suite was also run by hand in Firefox 153 and WebKit 26.5 on Linux
  and passes there. Safari on macOS or iOS, real phones and screen readers are
  not tested, and the Presentation view and the Reference tree outside the
  lock suite were run in Chromium only.
- **The kit's own example faces.** The four slide faces of the kit, one on
  "Get started", one on "Build a site" and two on the starter guide, still
  follow the old prescribed arrangement. The
  [findings record](upgrade-to-4.0.0-findings.md#decided-and-still-owed)
  keeps this as owed.
- **ADP was not built with the new default.** ADP's tracked files hold about
  6.6 GB (6,591,531,630 bytes in the local checkout on 2026-11-15), and its
  site has not been built with the automatic listing on. The kit owner reports
  that only its 331 tracked Markdown files were used, in a scale test; that
  count matches `git ls-files '*.md'` in the local checkout. ADP's upgrade
  starts with the first step of the migration guide.

## Done when

deivid has given the go, the number is settled, the merge of the fix branch
is confirmed or reverted, and the tag is pushed. The open points above then
move to their own records or are fixed; delete this record and its route in
the landing commit.
