# Source extraction map

This map accounts for the headings in the source documents used to extract this kit. It records policy transfer, not a claim that the source project's behavior or runtime is portable. The kit's provenance manifest records original file identities separately.

**Transferred** means retained as shared policy. **Genericized** means the mechanism/rule remains, with project names, exact local commands or source-specific paths removed. **Project-owned** means the content remains outside the kit because it describes that project's facts, history, environment or implementation.

## Current guide locations

The source-heading tables retain their extraction-time entrypoint names.
[Writing](writing.md) now routes to focused guides in `writing/`;
[maintenance](maintenance.md) routes to focused site guides in `site/`.
Their original headings remain linkable. The [engineering guides](../docs/index.md#engineering-practices)
record later portable code, performance, execution, Git, delivery and handoff
policy; source-specific tools, limits and project facts stay with consumers.

The [experiment guides](../docs/index.md#experiments) now own shared workflow
and proportionate verification. [Evidence reporting](writing/evidence.md)
retains provenance, outcomes, visuals and reviews actually performed;
[performance guidance](engineering/performance.md) owns production benchmarks
and engineering quick modes. This ownership refinement preserves numerical
implementation checks without applying them to every research comparison.

## Source: `docs/project/documentation.md`

| Source heading | Disposition and kit home |
|---|---|
| Documentation system | Transferred: `documentation.md`, canonical-home rule |
| Canonical homes | Genericized: canonical table; project refactor suite, runtime qualification, SDK experiment, codegen/testing ownership and domain development guide remain project-owned |
| Rendered pages are for people; agent records stay Markdown | Transferred: audience split, topic-first authoring, hidden anchor stubs, plain records and subject-grouped history |
| From open work to subject knowledge | Transferred: lifecycle, accepted-versus-implemented distinction, experiment ownership, no duplicate archive/status homes |
| Frozen source and experiment documentation | Genericized: exact bytes/reference closure, per-file revision, manifests, strict current links, reading views and absent-destination restoration; exact manifests, resolver prefixes, snapshots, old runtime permissions and commands remain project-owned |
| Shelved investigations | Genericized: scope/reopening/hidden-page rules; named shelved experiments and replacement requirements remain project-owned |
| Opening a page for review | Genericized: rendered-first review, own-checkout/loopback server, owner checks and browser permission gate; exact launch profile, port and current browser settings UI remain project-owned |
| Building and publishing | Genericized: reproducible ignored output, tracked closure, source identity, default-branch publishing and separately authorized hosting configuration; exact Python/Node pins are kit implementation choices, source deployment date/history/cutover/rollback commit remain project-owned |
| Shared reading layout | Transferred: route implementation ownership to `maintenance.md` |
| Rules | Transferred: deletion approval, same-deliverable documentation/tests/worklog, append-only newest-first worklog, invariant ownership, rerun rule, figure provenance, source/page distinction, ongoing reports, notes tails and no archive staging; source hook installation and application commands remain project-owned |
| Resuming refactor work | Genericized: single execution owner, prerequisite outputs, knowledge/choice/status/chronology split, readiness distinctions; named suite and assignments remain project-owned |
| Agent entrypoints: import vs point | Transferred: thin routers, bare Claude imports, explicit Codex named paths, orientation-only loading; starter points at pinned shared rules |
| README is the exception | Transferred: bounded human summary, canonical owner wins and same-deliverable sweep |

## Source: `docs/project/writing-docs.md`

| Source heading | Disposition and kit home |
|---|---|
| Documentation content style guide | Transferred: `writing.md` scope and system separation |
| Page design | Transferred: coherent cards, reachability, human labels, chronology separation, first-class pedagogy, rich code, viewport/accessibility robustness and mechanism naming |
| Build-sheet pages | Transferred: typography, full-stage/full-width chapters, filled grids, chart label size, claim-first story, status board, flows, complete comparisons and data identity; stylesheet entry genericized to shared resource name |
| Story & structure | Transferred: prerequisite order, one concept/formula home, instrument-before-results, evidence-before-shipping, experiment/deployment distinction; source topic names removed |
| Sections and reading layers | Transferred: complete visible spine, optional typed folds, weight-based placement, no duplicated headings, competing methods together and coordinated layer extension |
| Naming & honesty on pages | Transferred: one term, current baseline, visible rationale, jargon/roles/inputs and separate evidence scopes |
| Numbers & staleness | Transferred: reproducible current claims, changed-input reruns, historical retention, arithmetic distinction and experiment ownership |
| Figure & interaction rules | Transferred: earned figures, numbered captions/anchors/prose references, matched comparisons, actual construction, Math continuity, ablations, direct findings, column sizing, shared dark style and interactive provenance; source plotting helper path and source-specific artist ID syntax are project-owned implementation details |
| Layout process | Transferred: requested review gate, content/evidence/anchor parity and reachable rejected-method lessons |
| Visuals first | Transferred: visual completion gate, readable figure story, dynamic-media evidence and local capture handling |
| Math docs | Transferred: prerequisites, intermediate derivations, annotated constructions, local/global distinction, bundled math rendering, formula citation, derivative verification and applicable experiment plot set |
| Code & design docs | Transferred: real minimal source excerpts, source/line drift verification and local rationale; source package example genericized |
| Diagrams | Genericized: generated/self-checking or explicit local HTML source, semantics, legends and data source; source component naming/colors and exact live/backlog feature claims remain project-owned; future zoom/highlight features are explicitly not guaranteed |
| Sim & run visuals | Genericized to Run visuals: scripted capture, labelled illustrative screenshots and artifact-derived overlays; no simulator requirement transferred |
| Experiments: lifecycle, floor, workflow | Genericized: the required experiment content (floor), including a pre-stated bar and verdict for confirmatory investigations and qualifications, in `experiments/workflow.md`; reporting/lifecycle and same-deliverable bookkeeping in `writing/evidence.md`; production benchmarks and quick-mode guidance in `engineering/performance.md`; independent derivation/reference, production comparison, optional native comparison and exit self-check whenever results depend on custom numerical code, and regression gates, in `experiments/verification.md`; source benchmark paths and application dependency lists remain project-owned |

## Source: `docs/site/maintenance.md`

| Source heading | Disposition and kit home |
|---|---|
| Documentation site maintenance | Transferred: implementation/content/system ownership split |
| Tooling and ownership | Genericized: `.docs-kit` engine versus consumer configuration/content and ignored output; source relocation history and old executable paths remain project-owned |
| Authoring paths | Transferred: generated-origin body/source-origin tail, source identity, includes/CSS bases, registered index pages and hidden navigation; source page names genericized |
| Validation | Genericized: complete build/freshness/lint/regression/evidence/browser gates, quick-check limitations, strict warnings and tracked/local media closure; source-specific tests, runtimes and pending hosting cutover remain project-owned |
| Shared reading layout | Transferred: vendored fonts, build-sheet, chapter arrangements, sidebar, home/site map, independent layers, history/deep-link/fallback/print/accessibility and optional section labels; application viewers, their exact dependency/version/color conversion and topic-specific grouping remain project-owned |
| Extending reading layers | Transferred: coordinated builder/reader/fallback/styles/check changes and stable saved values; exact shared-engine paths follow the pinned kit |

## Design reference: `docs/topics/vehicle-visuals/index.md`

| Source heading | Disposition and kit home |
|---|---|
| Vehicle visuals | Project-owned subject; transferable page structure demonstrated in starter |
| A cutaway car that shows what the SDK simulates | Genericized: claim-first chapter, full-width numbered interactive figure and labelled spec strip; all vehicle/model/SDK facts excluded |
| One livery per participant | Genericized: complete option gallery, stable semantic colors, appearance-only image captions; palette values/assignment rules excluded |
| Driven by the simulator, invisible to it | Genericized: labelled one-way `bs-flow` and prohibited-feedback row; starter uses source/build/output ownership |
| How exact the motion is | Genericized: measured-value scope and units; no numerical result transferred |
| Simulated or only drawn | Genericized: parallel `bs-part` scope distinction; domain claims excluded |
| Cannot change the physics | Genericized: parallel check tiles with explicit evidence; no physics guarantee transferred |
| Replay real suspension action | Genericized: linked local interactive comparison and loading/fallback rules; recordings and viewer data excluded |
| Grow the car from the recipe | Genericized: understandable construction and optional technical depth; generator/asset details excluded |
| Hand it to the simulator | Genericized: integration scope separate from selected/CPU/native status; application integration excluded |
| Where it stands | Transferred pattern: one current `bs-board` with distinct evidence/status scopes; all hashes/results/open defects excluded |
| What it does not claim | Genericized: concise evidence-adjacent scope and non-duplicated status; vehicle limitations excluded |
| Provenance and regeneration | Genericized: owned generator/input identity and reproducibility; source paths/commands/data excluded |

## Additional user design policy

The later [panel-switcher extraction](../docs/topics/panel-switcher/panel-switcher.md)
shares the generic switching, hash, print and control-style portions of
`docs/site/components/width-lessons.{js,css}`. Track scenarios, figures, data,
legends and specialized figure layouts remain project-owned. The source
project's own documentation records adoption and compatibility status.

The original home page's embedded stylesheet is also extracted into shared
`theme/assets/home.css`: hero, navigation cards, topic gallery, hover states and
responsive layout. The shared version uses the available width. Its project
status, application diagram, dates and subject content remain project-owned.

Transferred into `writing.md`: figures as a completion gate, compartmentalized human pages, tasteful interaction, mechanism names, author-owned robustness, takeaway titles, one fact once, full-width layout, direct answers, explicit unmeasured bounds, complete option exploration and final decision table/verdict. Project copies should point to these rules rather than drift independently.

No source runtime qualification, local recovery grant, archived deployment history, domain requirement or benchmark value is adopted as a shared factual claim. The starter's flows are source-authored diagrams explaining the documentation pipeline; they are illustrations, not measurements.
