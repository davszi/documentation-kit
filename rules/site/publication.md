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
  be published.

The private checks cover admitted files, generated files and the repository
source of each generated asset or medium. A renamed project asset therefore
cannot hide a private source. Missing, untracked, duplicate or symlinked files
fail.

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
does not turn it on gets the same bundle as before, byte for byte.

The lock is not access control. The encrypted files are public, and anyone who
has a password can read and pass on everything it opens.

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
  `source_pages` of `site-build.json`, or a page whose body has the class
  `source-page`. The general password opens every other HTML file, including
  pages shown in frames.
- Every Markdown file the bundle exports, under the reference password. The
  file keeps its address and holds a short notice and the encrypted text. A
  link to it from an unlocked page opens the text.
- The kit writes no search index. Navigation and the site map are part of
  the pages and are locked with them.

Images, plots, videos, stylesheets, scripts, fonts and every other file, such
as JSON data, stay readable for anyone who has their address. `publish` ends
with a summary: how many files each password opens, and how many files stay
readable, by type. Check it for data files that should not be public.

### Reading a locked site

A reader types one password once. The browser keeps the decrypted content keys,
never the password, in `sessionStorage` for the tab. With "Remember on this
device" it also keeps them in `localStorage`. A reader with the general password
who opens a Reference page is told that it needs the reference password. A
wrong password gives one plain message, whichever password it was meant to be.
Every publish uses new keys, so readers enter a password again after each
publish. Unlocking needs JavaScript and a secure connection: HTTPS, `localhost`
or a local file.

### Keys and parameters

PBKDF2-HMAC-SHA-256 with 600,000 iterations, the recommendation of the OWASP
Password Storage Cheat Sheet, and a random 16-byte salt for each publish
derives one key from each password. Each publish also draws a random 256-bit
content key per password level. The general password's key wraps the general
content key; the reference password's key wraps both content keys. Each locked
file is encrypted with AES-256-GCM under its level's content key, with a fresh
random 96-bit nonce and its path in the bundle as authenticated data.
`tooling/page_lock.py` encrypts; `theme/components/page-lock.js` decrypts with
the browser's WebCrypto.

### Limits

- Anyone can download the encrypted files and test password guesses offline,
  as fast as their hardware allows, with no lockout and no trace. Only a long
  random passphrase protects the text; the iteration count only makes each
  guess slower.
- Each level has one shared password. There is no access per person, no way
  to shut out one reader and no record of who read what.
- Anyone with a password can save the decrypted pages and pass them on. The
  content keys the browser stores open the current publish without the
  password.
- The unlock script is not encrypted. Whoever can change the published site
  or the job that publishes it can replace the script and collect passwords
  as readers type them.
- A new password protects only later publishes. Copies downloaded earlier,
  and earlier public versions kept by caches and web archives, stay readable
  with the old password or without one.
- Images, plots, scripts and data files are not locked. Their addresses often
  follow repository paths, so they can be guessed.
- A lock page shows the size of the page it holds and which password it
  needs. Pages opened with the general password list the titles and paths of
  the Reference pages in their sidebar.
- Pages need JavaScript. A project script that fetches an HTML or Markdown
  file from the bundle receives the locked file.
- Search engines stop listing the site, because they see only lock pages.
- Remembered keys stay in the browser until the next publish replaces them or
  the reader clears the site's data. Any page served from the same origin,
  such as another GitHub Pages site of the same account, can read the stored
  keys, remembered or not.
