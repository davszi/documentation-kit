# Simplify the frozen-record machinery inherited from ADP

Open work. Nothing here is decided except the direction and the removal already
landed. Statements are labelled as deivid's direction, verified evidence or
proposal.

## Direction

deivid, 2026-11-09: parts of ADP's documentation system became too complicated,
and simplifying them is our work. The frozen-record chain described below is one
of those parts; the others are not listed yet.

## The chain

Verified on 2026-11-09 by reading ADP at `60834b06` (kit pin `v1.1.0`) and
adapt at `99ef9cc`.

1. ADP moved its documentation several times, for example `docs/src/pages` to
   `docs/topics` and `docs/project/*` to other homes.
2. ADP keeps old documents inside the live `docs/` tree as frozen records that
   are never edited or deleted.
3. Their links name paths that no longer exist, and lint still checks those
   links. That needs a path translator.
4. Frozen must be provable. That needs hash manifests and a validator.
5. The kit supports all of it through adapter hooks and rule text.

One choice drives the chain: old documents stay byte-exact inside the live docs
tree and stay link-checked.

## What it costs

| Where | Part | Size |
|---|---|---|
| ADP | `tools/docs/site_paths.py`: 4 directory aliases and 22 single-file mappings | 225 lines |
| ADP | `tools/docs/evidence_documents.py`: hashes, byte counts, original paths | 307 lines |
| ADP | `tools/docs/test_sdk_evidence_links.py` | 493 lines |
| ADP | `tools/docs/` in total | 1,201 lines |
| ADP | `docs/evidence/locations.json` and `experiments/platform_qualification/sdk_reuse/evidence/locations.json` | 18 and 35 documents |
| ADP | Tracked files under `docs/`, and those under `evidence/` folders | 951, of which 412 |
| adapt | `docs/site/layout_paths.py`, the same pattern | 291 lines |
| Kit | `tooling/site_paths.py`, `tooling/evidence_documents.py`, `tooling/project_extensions.py` | 180 lines |
| Kit | Path and evidence resolution in `tooling/lint.py` | about 70 lines |
| Kit | [Evidence identity and frozen records](../../rules/records.md#evidence-identity-and-frozen-records) | 177 words |
| Kit | [Resource closure and evidence](../../rules/site/resources.md#resource-closure-and-evidence) | 595 words |

## Constraint on order

The kit hooks `path_resolver`, `evidence_validator` and `document_origin` cannot
be removed before ADP and adapt stop using them: their builds would fail at the
next kit upgrade. The target shape is decided first and carried out during each
project's migration to the current kit.

## What the chain serves, measured on 2026-11-11

Verified on ADP `origin/main` at `7d85f2a4`, by this session and by ADP's
documentation session independently, with matching counts:

- Lint checks 3,946 Markdown links that leave their own file. 164 need a row of
  ADP's path adapter: 96 in 25 exact-byte documents and 68 in the worklog. No
  current document needs one.
- ADP holds 53 exact-byte documents. Git returns the exact bytes of 52 at the
  recorded commit and original path; the 53rd entered Git only as its copy.
- The files that record a document's hash name its original path, not the copy.
- No ADP record states why the copies are kept as live files or why their links
  are checked. The only stated purpose, from 2026-10-17, is to reproduce source
  hashes and to interpret frozen review links.

## Decided by deivid on 2026-11-11

- A replaced document is deleted by default. Whatever needs it cites the commit
  and path in Git.
- A copy kept in the tree needs deivid's approval for that file, with the named
  thing that depends on it.
- A kept copy is guarded, not untouchable. Its recorded hash stays and a change
  fails the check. The check passes again only when the recorded hash changes
  in the same commit, and that happens only after deivid approved the exact
  diff. There is no enforcement on the hosting side.
- The rule also applies backwards: ADP's 53 documents are reviewed one by one.

Later the same day deivid decided the 53 documents in one answer, "delete all",
to this proposal:

- All 53 are deleted from ADP's tree. None has a dependant that needs the file
  itself; each needs only the bytes, and Git holds them.
- Two of them state rules that are in force,
  `physx-vehicle-sdk-performance-contract.md` and probably
  `physx-vehicle-sdk-environment-profiles.md`. Their rule text moves into ADP's
  current record `docs/topics/physx-sdk-runtime-cost/physx-sdk-runtime-cost.md`
  before the old files go.
- Links that cite a deleted document become links to the file at its commit.
- One list of old path, commit and hash for each of the 53 replaces the two
  location manifests, so a recorded hash can still be traced to its bytes.
- ADP then removes its path translator, the manifests, the validator and their
  tests.
- Lint stops checking links in worklog entries older than a date the project
  records. Old entries link to these documents and are never rewritten, so
  without this no document could be deleted.

The worklog date is implemented as `worklog_links_checked_from` in
`docs/site/site.toml`; [resources](../../rules/site/resources.md) describes it.
It is not released yet.

Not decided: the wording of the forward rule in `rules/records.md`,
`rules/documentation.md` and `rules/site/resources.md`. A draft goes to deivid
for approval.

## Other kit checks only ADP uses

Verified, and not judged a problem: the figure-manifest check
(`docs/figures/manifest.json` and two topic manifests) and the `INVARIANT` and
`DON'T-REDO` marker check (64 markers in 17 files). Both do nothing in a project
without a manifest or markers.

## Couplings found by ADP's upgrade to 3.0.0

Verified on 2026-11-10 in ADP at its commit `1b7e0087`. They can break at an
upgrade even when the kit's adapter hooks stay unchanged:

- ADP's `tools/docs/_kit.py` loads the kit's build and lint modules, and two
  ADP test modules use the private names `_errors`, `_check_chunk_links` and
  `_evidence`.
- Four ADP Node checks read kit theme sources from `.docs-kit/theme`. One of
  them matched exact kit HTML and failed in the 3.0.0 upgrade.
- ADP's navigation group names are hard-coded in four kit stylesheets:
  `theme/components/base.css`, `theme/components/chapter-reader.css`,
  `theme/assets/home.css` and `theme/assets/build-sheet.css`. The accent
  variable is named `--adp`.

deivid decided on 2026-11-10 to keep ADP's five compatibility layers until the
frozen-record choice was made. ADP's record
`docs/open/documentation-compatibility-layers.md` holds their sizes, their
dependents and the order of work.

## Already removed

Two shared modules that no project imported are gone; the
[worklog](../KIT_WORKLOG.md#2026-11-09--remove-the-unused-number-ledger-and-verbatim-lock-modules)
records it. `tooling/svg_figures.py` stays because adapt and adaptation import it.

## Next step

1. deivid approves the rule wording, and the kit releases it together with
   `worklog_links_checked_from`.
2. ADP's session moves the two rules, rewrites the citing links, adds the list
   and deletes the 53 documents, then removes ADP's translator, manifests,
   validator and their tests. ADP adopts the release that carries the worklog
   date before its lint can pass.
3. adapt follows the same rule for its own frozen documents.
4. The kit removes a hook once neither project names it, and with it the
   worklog-specific historical link handling in `tooling/lint.py`.
