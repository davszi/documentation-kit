# Known open after 5.0.0

Open points, for the kit owner. Raised on 2026-11-15, at the release of
[5.0.0](../topics/releases/releases.md#500--reference-section-by-default-page-lock-and-presentation-view).
None blocked the release. Each closes on its own; delete its item when it
does, and this record with its route when the last one goes.

## Not tested

- **Safari and the real host.** The kit's checks run in Chromium only. The
  page lock's browser suite was also run by hand in Firefox 153 and WebKit
  26.5 on Linux and passes there. Safari on macOS or iOS, real phones and
  screen readers are not tested. The lock has not run on a GitHub Pages
  host. The Presentation view and the Reference tree outside the lock suite
  were run in Chromium only. Closes with one pass in real Safari on the
  first locked site that is live.
- **ADP with the automatic listing.** ADP's tracked files hold about 6.6 GB
  (6,591,531,630 bytes in the local checkout on 2026-11-15), and its site
  has not been built with the automatic listing on. Only its 331 tracked
  Markdown files were used, in a scale test of the 5.0.0 default. From 6.0.0
  the default lists `docs/` only; ADP's 230 experiment records are listed
  when it names `experiments`. Closes at ADP's upgrade, which starts with
  the first step of the
  [6.0.0 migration guide](../topics/releases/migrations/6.0.0.md).

## Known limits, not fixed

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
