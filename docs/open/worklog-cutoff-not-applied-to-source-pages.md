# The worklog link cut-off does not reach a rendered worklog

Found by the independent review on 2026-11-14 and reproduced by it. Delete
this record and its line in [KIT_OPEN.md](KIT_OPEN.md) when the build applies
the cut-off or the limit is accepted as final.

## Defect

`worklog_links_checked_from` makes lint skip links in worklog entries dated
before the given day. The check sits only in `tooling/lint.py`
(`check_md_links`). A worklog that is also a
[registered source page](../../rules/site/authoring.md#registered-source-pages)
has its links resolved by the build, in `tooling/source_pages.py`, which knows
nothing of the setting. The build then fails with `link target not found` on a
missing target in any entry, old ones included.

## Reach

The setting is new in the unreleased changes after `v3.2.1`. On 2026-11-14 no
`site.toml` of ADP, adaptation or Tempo registers its worklog as a source
page, so no known project meets the defect.
[Resources](../../rules/site/resources.md#resource-closure-and-evidence) now
states the limit.

## Next step

Apply the cut-off in the build's link resolution for the worklog source page.
Open point: what the rendered page shows for a skipped link whose target is
gone, plain text or a link marked as dated.
