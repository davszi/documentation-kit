# Publication export

## Publishing gate

A requested review and any deletion pass their gates first; see [rules for changes and chronology](../documentation.md#rules-for-changes-and-chronology).

Builds on feature branches must not publish production documentation. Publishing requires the consuming project's chosen branch/environment, authorization and successful checks. Hosting source changes are a separate explicit operation; a source build does not imply a deployed version. Rollback must preserve unrelated work and rebuild/verify the chosen revision.

## Configured publication

Run `python .docs-kit/docsite.py publish --project . --out _site` to build the
site and export a fresh public bundle. It builds through the same engine as
`build`. It does not deploy the bundle. Preview only the resulting directory.

Configure publication in the `[publication]` table of `docs/site/site.toml`:

```toml
[publication]
assets_manifest = "docs/site/public-assets.json"
pages = ["index.html", "guide.html"]
private_suffixes = [".md", ".py", ".toml"]
private_prefixes = ["configs/"]
```

All keys are optional. Any other key fails with an error that names the
supported keys. A fifth key, `lock = true`, turns on the
[page lock](#page-lock).

- `pages` names the generated HTML files whose source links and media are
  rewritten for the public bundle. Every generated file keeps its name.
- `assets_manifest` names a tracked JSON file with a `files` array of
  repository paths. Each file is published at the same path.
- `private_suffixes` and `private_prefixes` mark repository paths that must not
  be published. A page rendered from such a file is private too: `publish`
  fails when a `[[source_pages]]` table registers one, and the automatic
  listing skips them.

The private checks cover admitted files, generated files and the repository
source of each generated asset or medium. A renamed project asset therefore
cannot hide a private source. Missing, untracked, duplicate or symlinked files
fail.

Every generated page is published, the pages of the
[automatic reference listing](authoring.md#automatic-reference-listing)
included, with the media they package. That listing skips files that the
private prefixes or suffixes cover, and its pages do not package media they
cover, so it cannot make a publication fail. With `private_suffixes` holding
`.md`, as in the example above, it lists no file at all. It still publishes
every other tracked Markdown file as a page: exclude private files with
`reference_exclude`, or set `reference_listing = false`. Without a source
remote, `publish` also rewrites the source links of pages not named in
`pages`; see [a project without a source remote](authoring.md#tooling-and-ownership).

The output directory must not exist yet. The bundle is written to a temporary
directory next to it and moved into place only after every check passes.
Failed publications leave no output directory.

## Exporting into an existing publication

`tooling/publication.py` exports an already-generated kit bundle into a
project-owned publication directory. It does not build a second site or choose
which repository files are public. Import `export_pages` from the pinned kit's
`tooling` directory after building. Supply:

- `generated_root`, `destination` and repository `root` as explicit paths.
- `tracked` repository paths.
- `public_files`, the tracked repository paths the project publishes at the
  same path. Each must already be in the publication or among the generated
  outputs.
- `pages`, the generated HTML files to rewrite. Every generated file keeps its
  generated name.
- `private_suffixes`, `private_prefixes` and `local_notice` for the project's
  source-link and unavailable-evidence policy.
- `replace` for the exact existing output paths that may be overwritten.
  Byte-identical copies need no replacement permission.

The exporter validates paths, symlinks, public files and collisions before
writing. It points `_media/` sources and source links of public files to their
published path, relative to the page. It modifies actual HTML attributes and
unavailable-evidence anchors; embedded JavaScript/JSON and unrelated source
bytes remain opaque. The shared source-span parser counts LF exactly as
`HTMLParser` does. Keep output selection, historical guide packaging, source
URLs, privacy decisions and deployment credentials in the consuming project.
The generated input is the trusted kit build, not an arbitrary repository
directory.

## Page lock

The page lock is an optional last step of `publish`. It stores the text of the
public bundle encrypted, and a reader unlocks it in the browser with a
password. Local `build` output and `export_pages` stay plain. A project that
does not turn it on gets, byte for byte, the bundle an unlocked `publish` of
the same kit version writes.

The lock is not access control. The encrypted files are public, and anyone who
has a password can read and pass on everything it opens.

The lock protects only the published bundle. The source repository, its
Actions logs and its workflow artifacts hold the same text unencrypted, so all
of them must stay private; with a public source the lock is pointless. GitHub's
[plan overview](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
lists GitHub Pages in public repositories for GitHub Free, and in private
repositories under GitHub Pro and GitHub Team; publishing a site privately, with
access control, needs an organization on GitHub Enterprise Cloud.

### Turn it on

1. Install the optional dependency wherever `publish` runs:
   `python -m pip install -r .docs-kit/requirements-lock.txt`. It pins the
   `cryptography` package. Without it, `publish` fails and names this command.
2. Set `lock = true` in the `[publication]` table.
3. Give the `publish` step two passwords as environment variables:
   - `DOCSITE_GENERAL_PASSWORD` opens the topic pages and every other page.
   - `DOCSITE_REFERENCE_PASSWORD` opens everything, including the Reference
     pages and the exported Markdown files.

In GitHub Actions, store both passwords as repository secrets and pass them to
the publish step only:

```yaml
- name: Publish the locked bundle
  env:
    DOCSITE_GENERAL_PASSWORD: ${{ secrets.DOCSITE_GENERAL_PASSWORD }}
    DOCSITE_REFERENCE_PASSWORD: ${{ secrets.DOCSITE_REFERENCE_PASSWORD }}
  run: python .docs-kit/docsite.py publish --project . --out _site
```

Deploy the `--out` directory. The build output under `.build/docs/` stays
plain, so deploying it publishes every page unlocked.

The passwords never go into the repository, `site.toml`, the bundle or the
command output. `publish` fails before it builds when a password is missing,
when the two are equal, when one is shorter than 20 characters, or when one
starts or ends with whitespace or holds a character a reader cannot type. The
length check cannot tell a random passphrase from a guessable one. Generate
each password, for example with
`python -c "import secrets; print(secrets.token_urlsafe(24))"`, and give it to
readers through a separate channel.

### What is locked

- Every HTML file in the bundle, whole: text, sidebar, inline figures and
  embedded data. A lock page with the title "Locked page" and a `noindex`
  robots tag is served at its address instead. The reference password is
  needed for every page the build records as a Reference page: a route in
  `source_pages` of `site-build.json`, which includes the
  [automatically listed](authoring.md#automatic-reference-listing) files, the
  Reference index page, or a page whose body has the class `source-page`. HTML
  without the kit's sidebar, such as a frame or an exported HTML file, needs
  the reference password when only Reference pages embed or link it. The
  general password opens every other HTML file, including a frame that a
  general page uses or no page uses. `publish` refuses `.xhtml`, `.xht`,
  `.shtml` and `.shtm` files: the unlock rewrites the page with
  `document.write`, which an XML page lacks, and a server-side-include page may
  not be served as HTML. Rename such a file to `.html` or leave it out.
- The site's root `404.html`, which GitHub Pages serves at every missing
  address. Its lock page opens at any address, so keep it free of Reference
  content; the general password opens it. Any other locked page served at an
  address it was not sealed for says so and leaves the reader's keys in place.
- The sidebar's Reference section. With the lock on, the build writes the
  folder tree once as `reference.tree.js`, whatever its size, and `publish`
  cuts the section out of every page the general password opens. The tree
  file holds the tree and that section, encrypted for the reference password
  and padded to a power of two of at least 64 KiB; the Reference index page is
  padded to the same size. A reader with the reference password gets the
  section back on every page, with the current file marked; a reader with the
  general password sees no Reference section.
- Every Markdown file the bundle exports, under the reference password. The
  file keeps its address and holds a short notice and the encrypted text. A
  link to it from an unlocked page opens the text; `filelinks.js` leaves
  links the exporter pointed at a published file alone, with or without a
  source remote.
- The kit writes no search index. Navigation and the site map are part of
  the pages and are locked with them.

Images, plots, videos, stylesheets, scripts, fonts and every other file, such
as JSON data, stay readable for anyone who has their address. `publish` ends
with a summary: how many files each password opens,
and how many files stay readable, by type. Check it for data files that should
not be public. When pages that the general password opens name Reference files,
the summary counts those files: readers with the general password see their
names. It counts every Reference page route, repository path or exported
Markdown path that appears anywhere in such a page, in a link, a source link
to a source host, any attribute or the text, so a `[[nav]]` entry, a site-map
card and a source link all count.

### Reading a locked site

A reader types one password once. The browser keeps the content keys of the
current publish, never the password, in `sessionStorage` for the tab; after the
next publish, a tab asks again. With "Remember on this device" the browser also
keeps the key derived from the password in `localStorage`. That key opens every
later publish without asking, until either password changes. A reader with the
general password who opens a Reference page is told that it needs the reference
password. A wrong password gives one plain message, whichever password it was
meant to be. Unlocking needs JavaScript and a secure connection: HTTPS,
`localhost` or a local file.

### Keys and parameters

PBKDF2-HMAC-SHA-256 with 600,000 iterations, the recommendation of the OWASP
Password Storage Cheat Sheet, derives one key from each password. Its 16-byte
salt is itself PBKDF2-HMAC-SHA-256 of both passwords with the same iteration
count: it stays the same from publish to publish and changes when either
password changes, which locks out every remembered reader. Each publish draws
a random 256-bit content key per password level. The general password's key
wraps the general content key; the reference password's key wraps both
content keys. Each locked file is encrypted with AES-256-GCM under its level's
content key, with a fresh random 96-bit nonce and its path in the bundle as
authenticated data. `tooling/page_lock.py` encrypts;
`theme/components/page-lock.js` decrypts with the browser's WebCrypto.

### Limits

- The lock covers only the bundle. A public source repository, or readable
  Actions logs or workflow artifacts, give the text away unencrypted.
- Anyone can download the encrypted files and test password guesses offline,
  as fast as their hardware allows, with no lockout and no trace. Only a long
  random passphrase protects the text; the iteration count only makes each
  guess slower.
- Each level has one shared password. There is no access per person, no way
  to shut out one reader and no record of who read what.
- Anyone with a password can save the decrypted pages and pass them on. The
  content keys the browser stores open the current publish without the
  password. A remembered key opens every publish until a password changes:
  whoever copies it from a browser profile reads every later version as well.
- The unlock script is not encrypted. Whoever can change the published site
  or the job that publishes it can replace the script and collect passwords
  as readers type them.
- A new password protects only later publishes. Copies downloaded earlier,
  and earlier public versions kept by caches and web archives, stay readable
  with the old password or without one.
- Images, plots, scripts and data files are not locked. Their addresses often
  follow repository paths, so they can be guessed.
- `assets/filelinks.js` stays readable. With a source remote configured it
  carries the repository's address.
- A lock page shows the size of the page it holds and which password it
  needs. The salt changes exactly when a password changes, so anyone can see
  that it changed.
- Reference addresses follow repository paths. Anyone can ask for a guessed
  address, such as `readme.md.html`, and learn from the lock page that the
  file exists. Above 64 KiB, the size of the tree file shows the size of the
  tree within a factor of two.
- Names of Reference files in pages the general password opens stay visible
  to those readers; `publish` counts them.
- A lock page that holds a page with the shared sidebar carries
  `data-section-at`, a byte offset in the page as built. It shows how long the
  page's head and sidebar are, on every such page, whether or not the site has
  a Reference section.
- Pages need JavaScript. A project script that fetches an HTML or Markdown
  file from the bundle receives the locked file.
- Search engines stop listing the site, because they see only lock pages.
- Remembered keys stay in the browser until a password changes or the reader
  clears the site's data. Any page served from the same origin, such as
  another GitHub Pages site of the same account, can read the stored keys,
  remembered or not.
- The kit's checks run the lock in Chromium. With `DOCS_BROWSER=firefox`, the
  same browser suite passes in the Firefox 153 that Playwright 1.62.1 installs
  on Linux: unlocking, the Reference tree after the page is rewritten,
  Markdown opened as text, fragments, the Presentation view, back and forward,
  remembered keys across publishes, and pages opened from disk. WebKit, the
  engine behind Safari, could not start on the test machine for lack of system
  libraries, so the lock is untested in WebKit. Safari on macOS or iOS is not
  WebKit on Linux and is untested as well. Safari may delete remembered keys of
  a site that a reader has not visited for some days; that is untested too.
