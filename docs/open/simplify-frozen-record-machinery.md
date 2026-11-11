# Simplify the frozen-record machinery inherited from ADP

Open work. The rule is decided and ADP's change is applied on a branch; the
kit release, adapt and the removal of the kit hooks remain. Statements are
labelled as deivid's direction, verified evidence or proposal.

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
| Kit | The section "Evidence identity and frozen records" in `rules/records.md`, replaced on 2026-11-11 by [finished working documents](../../rules/records.md#finished-working-documents) | 177 words |
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

The rule, as it now stands in the kit:

- A plan, decision record, review or coordination note is deleted once its work
  has landed and its lasting content is in the owning record. Whatever still
  needs it cites the commit and path in Git.
- No finished working document is kept in the tree as an unedited file. deivid
  first considered a kept copy guarded by its recorded hash and dropped it the
  same day: Git already keeps every old version with its exact bytes.
- For a document that a run recorded by hash, the commit, path and hash stand
  for the document, as a source pin stands for code.
- Topic records, guides, the worklog and what an experiment retains are not
  touched by this rule.

[Finished working documents](../../rules/records.md#finished-working-documents)
and [rules for changes and chronology](../../rules/documentation.md#rules-for-changes-and-chronology)
hold the wording deivid approved as an exact diff.

The rule applies backwards. To the proposal for ADP's 53 documents deivid
answered "delete all":

- All 53 leave ADP's tree. None has a dependant that needs the file itself;
  each needs only the bytes, and Git holds them.
- A rule still in force moves into a current record before its old document
  goes. ADP found one, `physx-vehicle-sdk-performance-contract.md`.
- Links that cite a deleted document become links to the file at its commit.
- One list of old path, commit and hash for each document replaces the two
  location manifests, so a recorded hash can still be traced to its bytes.
- ADP then removes its path translator, the manifests, the validator and their
  tests.
- Lint stops checking links in worklog entries older than a date the project
  records. Old entries link to these documents and are never rewritten, so
  without this no document could be deleted.

The worklog date is `worklog_links_checked_from` in `docs/site/site.toml`;
[resources](../../rules/site/resources.md#resource-closure-and-evidence)
describes it.

State on 2026-11-11: ADP's documentation session applied all of this on its
branch `claude/topic-records-1786aa`, not pushed. The branch ends at ADP's
commit `54bcf9a0`. Since the deletion it also holds, each decided by deivid:

- The five compatibility layers are gone: two delegate commands, 47 forwarding
  stubs, 21 unused link ids, `tools/docs/test_content.py` with `_kit.py`, and
  the kit-logic part of the Node checks.
- 100 guides named `README.md` below the root are renamed to
  `<folder>/<folder>.md`. Six that run records pin by hash still carry the old
  name.
- Each experiment keeps its stored data in its own `data/` folder. ADP's
  central store `docs/evidence/artifacts.json` went from 228 rows to 1. Checked
  from the kit session for the last 170 files: each unpacks to the size and
  hash its old row recorded.

ADP reports that its lint fails on 97 links against kit 3.2.1, and only on the
link to the renamed kit section against the kit's unreleased `main`. Neither
the kit setting nor the rule wording is released. deivid holds the release
until more of ADP's cleanup is done.

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
  `_evidence`. ADP deleted the chain tests on 2026-11-11. For the
  remaining module, `tools/docs/test_content.py`, the kit now offers
  `build --check-reader`; ADP deleted it and `_kit.py` on its branch.
- Four ADP Node checks read kit theme sources from `.docs-kit/theme`. One of
  them matched exact kit HTML and failed in the 3.0.0 upgrade. The kit now
  tests that logic itself, and ADP's checks on its branch cover only ADP
  content.
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

1. ADP finishes the cleanup deivid wants before a release. Open on its branch:
   the hash pins, the six pinned `README.md` files, and the deletion of the old
   store's tools and its last row.
2. The kit releases the rule wording together with
   `worklog_links_checked_from`, after an independent review of the rule
   change.
3. ADP pins that release, fixes its links to the renamed kit section, and
   deivid decides in ADP's session when its branch is pushed.
4. adapt follows the same rule for its own frozen documents.
5. The kit removes a hook once neither project names it, and with it the
   worklog-specific historical link handling in `tooling/lint.py`.
