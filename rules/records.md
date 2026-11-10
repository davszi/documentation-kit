# Writing records

A record is the Markdown document an agent is routed to: a topic record, a guide, a plan or a log. The agent that did the work writes or updates the record first, before any page for people. Exact evidence is kept as records too, but it is preserved, not rewritten; see [evidence identity and frozen records](#evidence-identity-and-frozen-records). The [documentation system](documentation.md) owns where a document lives and how it changes; this guide owns what a record says and how it is written. Page design and reading layers belong to the [page guides](writing.md) and apply only to pages for people.

## One record per topic

Every topic has a record: start it as `docs/topics/<topic>/<topic>.md`. When it grows, split it into descriptively named files; together they are the topic's record. Do not name subject records `README.md`. A page for people follows the record: [rendered pages are for people](documentation.md#rendered-pages-are-for-people-records-stay-markdown) says what a page may add, how pages stay in step when a record changes, and the `page_only` exception.

## Format

Records use plain Markdown headings, tables, lists, exact file references and evidence links. Keep layout HTML out of agent records. Store a needed diagram in a separate file and link it. Preserve anchors referenced by other documents.

## Naming and honest claims

Use one term per object across prose, controls, legends, tables, figures and output. Name a mechanism the reader sees; use formulation internals only when explaining that formulation. A rename sweeps all surfaces. State what a function receives, returns and optimizes/interpolates, and which inputs vary or stay fixed.

Decision rationale belongs beside the decision, including why an instrument/default was chosen and why alternatives lost. A baseline cited for current shipped behavior measures what ships; label retired baselines historical. An experimental verdict and deployment measurements are distinct content kinds.

Separate claims requiring different evidence: visual fidelity, smoothness, input preservation, correspondence with a source and physical accuracy. A local check or smoother drawing proves only its tested property. Label accepted future behavior, implemented behavior, CPU checks and native/runtime observations separately. Say "not measured" plainly and provide a supported bound where available. Never manufacture an estimate to fill an empty metric.

## Numbers and staleness

A current measured claim requires a source commit, exact reproduction command, runtime/environment, workload, units, baseline, method and scope. Link its raw result and limitations. Config values, derivations and design arithmetic are not measurements; cite their source and label them accordingly.

When code, input data, method, workload or runtime conditions affecting a claim change, rerun before quoting it as current evidence. Keep the old record's date, runtime, inputs and scope; a historical label does not qualify changed inputs. Presentation-only edits may reuse captured results only after checking identities, numbers and treatments remain intact.

When a redesign restates numbers in new prose, figures or slides, record each number's source in a ledger and lock the evidence blocks kept verbatim. The project owns the ledger format and the checks for both. A slide face may show only numbers that its chapter also shows; every distinct number a redesigned chapter shows, figure labels included, has a ledger source.

Keep protocols, outputs, snapshots, failed attempts, changed settings, actual outcomes, reviews actually performed and relevant uncertainty with the work that produced them. For experiments, also retain producing code, inputs, full result tables, source pins and any independent reviews performed in the experiment directory. Repository size decides where this material is stored, not whether it is kept. A project may hold bulky files outside Git; the experiment directory then records where they are and how to check they are the same files, for example by hash. A page, where one exists, explains what they establish. The worklog records the landing and hashes without duplicating tables. Retained measured content remains subject to the [deletion gate](documentation.md#rules-for-changes-and-chronology).

Historical records preserve their original source pins, inputs, runtime, settings, resource limits, deadlines and verdicts where those fields apply.

## Excerpts, formulas and figures

A record may carry a code excerpt, a formula or a figure. The rules about what such content may claim apply in a record as on a page; the layout and presentation rules do not.

- Code excerpts: the verified-excerpt and source-metadata rules in [code and diagrams](writing/code.md#code-and-diagrams).
- Formulas: the derivation and numerical-verification rules in [mathematical explanation](writing/math.md#mathematical-explanation).
- Screenshots and experiment visuals: the provenance rules in [run visuals and experiment lifecycle](writing/figures.md#run-visuals-and-experiment-lifecycle).

## Evidence identity and frozen records

Retain exact original bytes only for a specific citation, source pin or reproduction dependency. Preserve the necessary reference closure, original logical path, source revision, byte count and cryptographic hash in a location manifest. Record a per-document source revision when it differs from the collection default.

Do not rewrite frozen links, add banners to originals or silently replace missing bytes. Current prose links to current knowledge or explicit evidence locations. A manifest indexes identity and location; it is not a second content home.

If a project implements historical link resolution, limit rebasing to explicitly registered origins and records. Current links and missing targets remain strict. A reading view must distinguish exact originals from mutable supporting current files. Do not describe a symlink as a frozen source or write protection.

Restore an original only into an absent destination. Preserve a newer live file separately; do not overwrite unrelated pending work. Source relocation, hash verification and a reading view establish document integrity, not runtime qualification or permission to execute old procedures.

The [resources guide](site/resources.md#resource-closure-and-evidence) describes the location manifest and the adapters a project may register for these records.

## Shelved investigations

Shelving is a scope decision recorded in the experiment's own guide and in the owning topic. Preserve inputs, code, failures and concrete recovery conditions there. Resumption requires a new explicit assignment. A hidden page may remain directly linkable with `hidden = true`; hiding neither deletes evidence nor qualifies a replacement.

## Changes, worklog and open work

The documentation system owns how a record changes. [Rules for changes and chronology](documentation.md#rules-for-changes-and-chronology) cover deletion, the worklog and probes. [From open work to subject knowledge](documentation.md#from-open-work-to-subject-knowledge) covers `OPEN.md` and work that matures into a topic.
