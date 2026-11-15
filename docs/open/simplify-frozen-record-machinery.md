# Simplify the frozen-record machinery inherited from ADP

Open work. The kit's side is finished for 5.0.0; adaptation's cleanup at its
upgrade remains.

## What is done

deivid, 2026-11-09: parts of ADP's documentation system became too complicated,
and simplifying them is our work. The frozen-record chain was one of those
parts: old documents kept byte-exact inside the live docs tree, a path
translator so that their old links still passed lint, and hash manifests with a
validator to prove that they stayed unchanged.

- 2026-11-11: deivid decided the rule that ends the practice, now
  [finished working documents](../../rules/records.md#finished-working-documents):
  a finished plan, decision record, review or coordination note is deleted and
  cited from Git. For ADP's 53 copies he answered "delete all".
- 2026-11-15: the adapter hooks `path_resolver`, `evidence_validator` and
  `document_origin` are removed in 5.0.0 ("remove all 3").
- 2026-11-15: the kit's own settings `evidence_manifests` and `legacy_files`
  are removed in 5.0.0 ("Yes, remove both"), with `tooling/evidence_documents.py`
  and the relocation handling in lint. `worklog_links_checked_from` stays.

The [worklog](../KIT_WORKLOG.md) records each landing. The full record of the
measurements, ADP's branch state and the couplings found by ADP's upgrade is
in Git at this file's path, at the commit before the one that reduced it on
2026-11-15.

## What remains

Verified on 2026-11-15 by reading each `docs/site/site.toml`: ADP and Tempo
name none of the removed settings; adaptation names `path_resolver` and
`evidence_validator`, both `docs/site/layout_paths.py`; none sets
`evidence_manifests` or `legacy_files`.

adaptation removes its two settings at its upgrade to 5.0.0, and
`docs/site/layout_paths.py` once a search finds no other user (its own tests
import it), deletes the frozen copies its owner approves, and repoints or
removes the links that needed the adapter, following the
[migration step](../topics/releases/migrations/5.0.0.md#remove-the-adapter-hooks).
The size of that cleanup, measured on a clone, is in the worklog entry of
2026-11-15 on the HTML link check: 42 of adaptation's 78 HTML links to
repository files fail once its path adapter is gone.

Done when adaptation's upgrade to 5.0.0 has landed without the settings;
then delete this record and its route.
