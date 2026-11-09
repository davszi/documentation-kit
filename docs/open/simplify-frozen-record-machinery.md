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

## Open choices

Proposals, not accepted:

- Cite a frozen document by commit hash and path, since Git already keeps its
  exact bytes, and remove the copy from the live tree.
- Keep frozen documents in a folder that lint skips, without translating their
  links.
- Keep the chain as it is.

Not yet known: why ADP needs byte-exact copies inside the tree with live link
checks. That reason decides which choice is possible.

## Other kit checks only ADP uses

Verified, and not judged a problem: the figure-manifest check
(`docs/figures/manifest.json` and two topic manifests) and the `INVARIANT` and
`DON'T-REDO` marker check (64 markers in 17 files). Both do nothing in a project
without a manifest or markers.

## Already removed

Two shared modules that no project imported are gone; the
[worklog](../KIT_WORKLOG.md#2026-11-09--remove-the-unused-number-ledger-and-verbatim-lock-modules)
records it. `tooling/svg_figures.py` stays because adapt and adaptation import it.

## Next step

deivid chooses the target shape for frozen documents. The reason ADP needs
in-tree copies is checked in ADP's records before that choice.
