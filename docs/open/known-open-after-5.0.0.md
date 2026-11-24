# Known open after 5.0.0

Open points, for the kit owner. Raised on 2026-11-15, at the release of
[5.0.0](../topics/releases/releases.md#500--reference-section-by-default-page-lock-and-presentation-view).
None blocked the release. Each closes on its own; delete its item when it
does, and this record with its route when the last one goes.

## Not tested

- **Safari and the real host.** The kit's checks run in Chromium only. The
  page lock's browser suite was also run by hand in Firefox 153 and WebKit
  26.5 on Linux and passes there. Safari on macOS or iOS, real phones and
  screen readers are not tested. The lock runs on a GitHub Pages host:
  deivid unlocked adaptation's live site in Firefox on a Windows PC and
  reported on 2026-11-23 "the unlocking works". Which of the two passwords
  he used, and the Firefox version, are not recorded. The Presentation view
  and the Reference tree outside the lock suite were run in Chromium only.
  Closes with one pass in real Safari on a locked site that is live.
- **Lint and the build find headings differently.** The build reads
  Markdown; lint's anchor list and the record notes match lines that start
  with `#`. They disagree on a setext heading, a heading indented or inside
  a quote or list, a heading inside an HTML block, and a heading whose text
  holds a link; the record notes also count a heading inside an HTML
  comment. From 5.4.1 a repeated heading is numbered, so on a page with
  repeated headings one such disagreement shifts the ids after it: lint can
  then reject a fragment the page has, or accept one it lacks. Closes when
  the three read headings through one function.
- **Text size on a project's pages.** From 5.5.0 the theme keeps all its
  text at 11 px or more and `tests/test_text_size.cjs` checks the kit's own
  site. No project was checked: how much of a project's own text is smaller
  is not known, and `sub` and `sup` outside formulas count as small text.
  Closes when one project runs `assertTextSize` on its pages.
- **ADP with the automatic listing.** ADP's tracked files hold about 6.6 GB
  (6,591,531,630 bytes in the local checkout on 2026-11-15), and its site
  has not been built with the automatic listing on. Only its 331 tracked
  Markdown files were used, in a scale test of the 5.0.0 default. From 5.1.0
  the default lists `docs/` only; ADP's 230 experiment records are listed
  when it names `experiments`. Closes at ADP's upgrade, which starts with
  the first step of the
  [5.1.0 migration guide](../topics/releases/migrations/5.1.0.md).

## Known limits, not fixed

- **A heading can take an id of the page shell.** The build numbers a
  repeated heading against the other headings of its page, not against the
  shell's ids: `top`, `menu`, `sidebar`, `toc`, `backdrop`,
  `repo-tree-label` and `chapter-reader`. A heading "Top" then shares
  `#top` with the shell, and a link to it reaches the shell. From 5.5.0
  lint warns. Reserving the ids would rename such a heading's id, so it
  needs its own decision.
- **A tracked file whose name is not UTF-8.** `build` and `lint` stop with a
  traceback, `UnicodeDecodeError`, when the project tracks such a file
  (measured on a starter project with kit 5.4.0). `tooling/page_source.py`
  reads such names and the capability map skips them; other places that
  read Git's output do neither.
- **Reference titles for general-password readers.** A page that the general
  password opens can still link to a Reference page, through a `[[nav]]`
  entry, a site-map card or a link in the text. The link's text and address
  stay visible. `publish` counts such pages in its summary;
  [page lock](../../rules/site/publication.md#page-lock) lists it among the
  limits.
- **Links outside the bundle without a remote.** With `gh_repo = ""`, a link
  to a tracked file that is not admitted keeps its local path, which leads
  outside the published bundle. See
  [tooling and ownership](../../rules/site/authoring.md#tooling-and-ownership).
- **Raw HTML on registered pages.** Only automatically listed pages are
  filtered for raw HTML. A `[[source_pages]]` file can still carry a script
  or load outside content, and so can a tracked file under `docs/figures` or
  `docs/site/fragments`. A project authors these itself.
- **Tags shown as text on listed pages.** The allowlist for automatically
  listed pages does not admit `<center>`, `<figure>` or `<picture>`; a
  record that uses one shows the tag as literal text. Admitting them is a
  product choice for deivid.
- **Image files with a second format inside.** A listed page packages a
  raster image whose first bytes match its suffix. A file that is also valid
  in a second format is packaged; in the final review none ran in Chromium,
  Firefox or WebKit.
- **The list of protected ids.** The allowlist keeps a listed file from
  using an `id` that the kit's own components look up. The list is written
  by hand in `tooling/source_pages.py` and can go stale when a component
  gains an id.

## Owed by a project

- **adaptation's drawing labels.** The browser check fails a face whose
  drawing labels render below 11 px. On a clone of adaptation at `e28472e`,
  built with this kit, 14 of its 33 faces carry inline SVG labels: 7 fail at
  1600 px, the smallest label at 7.4 px, and all 14 fail at 390 px, the
  smallest at 2.3 px. adaptation meets this at its upgrade, in the migration
  step on slide-face checks.
