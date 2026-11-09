# Writing records

A record is the Markdown document an agent is routed to: a topic record, a guide, a plan, a log or exact evidence. The agent that did the work writes or updates the record first, before any page for people. The [documentation system](documentation.md) owns where a document lives and how it changes; this guide owns what a record says and how it is written. Page design, figures and reading layers belong to the [writing guides](writing.md) and apply only to pages for people.

## One record per topic

Every topic has a record: start it as `docs/topics/<topic>/<topic>.md` and split a growing record into descriptively named files. Do not name subject records `README.md`. The record is authoritative: a page for people explains it and never adds a rule, number or limit the record lacks. [Rendered pages are for people](documentation.md#rendered-pages-are-for-people-records-stay-markdown) covers pages and the `page_only` exception.

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

Keep protocols, outputs, snapshots, failed attempts, changed settings, actual outcomes, reviews actually performed and relevant uncertainty with the work that produced them. For experiments, also retain producing code, inputs, full result tables, source pins and any independent reviews performed in the experiment directory. The page explains what they establish. The worklog records the landing and hashes without duplicating tables. Retained measured content remains subject to the [deletion gate](documentation.md#rules-for-changes-and-chronology).

Historical records preserve their original source pins, inputs, runtime, settings, resource limits, deadlines and verdicts where those fields apply.

## Evidence identity and frozen records

Retain exact original bytes only for a specific citation, source pin or reproduction dependency. Preserve the necessary reference closure, original logical path, source revision, byte count and cryptographic hash in a location manifest. Record a per-document source revision when it differs from the collection default.

Do not rewrite frozen links, add banners to originals or silently replace missing bytes. Current prose links to current knowledge or explicit evidence locations. A manifest indexes identity and location; it is not a second content home.

If a project implements historical link resolution, limit rebasing to explicitly registered origins and records. Current links and missing targets remain strict. A reading view must distinguish exact originals from mutable supporting current files. Do not describe a symlink as a frozen source or write protection.

Restore an original only into an absent destination. Preserve a newer live file separately; do not overwrite unrelated pending work. Source relocation, hash verification and a reading view establish document integrity, not runtime qualification or permission to execute old procedures.

## Shelved investigations

Shelving is a scope decision recorded in the experiment guide and owning topic. Preserve inputs, code, failures and concrete recovery conditions there. Resumption requires a new explicit assignment. A hidden page may remain directly linkable with `hidden = true`; hiding neither deletes evidence nor qualifies a replacement.
