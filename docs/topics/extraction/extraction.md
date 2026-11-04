# Shared documentation extraction

## Result and ownership

The kit is a standalone Git repository intended for a version-pinned `.docs-kit`
submodule. Each consumer owns its content, navigation, local assets, evidence
and update timing. Shared rules, the renderer and the presentation live here.
This is the user-selected dependency model, not an automatic upgrade mechanism.

The [extraction map](../../../rules/extraction-map.md) accounts for the source
policy sections and project-owned exclusions. [Provenance](../../../provenance.json)
pins source and extracted bytes from the inspected source revision `9930b919`.
The source project was not migrated, deleted or retired during extraction.

## Implemented boundary

- An explicit consumer root separates project content from the kit installation.
- Existing HTML shell, chapter adaptation, one/two/all-chapter reader, navigation,
  independent layers, source links, code chrome, diagrams, plots, carousels,
  lightbox, fonts and KaTeX are retained. Home styling is shared separately.
- The starter demonstrates records/pages, three numbered flows, four fold types,
  one status board, source excerpts and an options/verdict table.
- Local configuration, pages, fragments, SVG, CSS and extension scripts require
  tracked, contained project inputs. Local CSS cannot replace shared assets.
- Initialization checks all destinations before writing and refuses collisions
  or symlink escapes. Media packaging and output containment remain explicit.
- Evidence manifests and historical filename mappings are consumer-configured;
  no application-specific collection is mandatory.

## Verification — 2026-11-04

The final combined invocation is recorded in [check output](../../../verification/checks.log),
[GNU time receipt](../../../verification/time.txt),
[resource samples](../../../verification/resources.json) and
[verification summary](../../../verification/initial.json).

| Check | Observed result |
|---|---|
| Starter build and strict lint | Pass; zero lint warnings |
| Python regression suite | 21 pass, including an actual Git submodule consumer and exact pointer check |
| Content preservation | Starter reader retains original text, code, links, media, anchors, folds, tables and SVG geometry |
| JavaScript math runtime | Inline/display rendering and split-text integration pass; currency and code stay literal |
| Source links | Local/hosted roots, encoded spaces, source lines, Markdown anchors and local captures pass |
| Browser | Six guide chapters and home at 1600×1000 and 390×844; no page overflow, broken images or recorded page errors |
| Reader modes | Paired layout, all-chapter layout, keyboard navigation, mobile table scrolling and no-JavaScript reading exercised |
| Independent source review | Sol high; asset-boundary findings fixed, regression cases added, no remaining actionable findings in fix-round scope |

The combined checks held the session's shared expensive-job lock. GNU time reports
7.05 s elapsed and 143.3 MiB maximum RSS for this invocation; this is not total
host or aggregate concurrent-process memory. Minimum sampled host available
memory was 48.3 GiB; peak ten-second memory-pressure averages were 0.00. These
figures characterize this validation invocation, not site performance.

The browser screenshots were also inspected visually: all six guide chapters,
paired reading, the mobile table's final columns and both home widths. The
[desktop](../../../preview/desktop.png), [phone](../../../preview/mobile.png)
and [home](../../../preview/home.png) captures are illustrations of the checked
layout. Their hashes are in the summary.

## Limits and adoption

The evidence qualifies the neutral starter and temporary independent consumers.
It does not establish compatibility with every existing project or complete the
original project's migration. Consumer-specific archival evidence validators,
domain viewers and historical aliases remain with their project. Screen-reader,
print, exhaustive assistive-technology and every browser/version combination
were not separately qualified in this extraction.

The repository is initially local; no hosted remote or first-party license was
selected. Vendor licenses and source notes are retained. A consuming project
must choose its real source repository/ref and review its own generated pages.
