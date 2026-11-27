# Writing records

A record is the Markdown document an agent is routed to: a topic record, a guide, a plan or a log. The agent that did the work writes or updates the record first, before any page for people. A plan, decision record, review or coordination note is deleted once its work has landed; see [finished working documents](#finished-working-documents). The [documentation system](documentation.md) owns where a document lives and how it changes; this guide owns what a record says and how it is written. Page design and reading layers belong to the [page guides](writing.md) and apply only to pages for people.

## One record per topic

Every topic has a record: start it as `docs/topics/<topic>/<topic>.md`. When it grows, split it into descriptively named files; together they are the topic's record. Do not name a record `README.md`; only the repository root has one ([README is the bounded exception](documentation.md#readme-is-the-bounded-exception)). A page for people follows the record: [rendered pages are for people](documentation.md#rendered-pages-are-for-people-records-stay-markdown) says what a page may add, how pages stay in step when a record changes, and the `page_only` exception.

## Format

Records use plain Markdown headings, tables, lists, exact file references and evidence links. Keep layout HTML out of agent records. Store a needed diagram in a separate file and link it. Preserve anchors referenced by other documents.

## Naming and honest claims

Use one term per object across prose, controls, legends, tables, figures and output. Name a mechanism the reader sees; use formulation internals only when explaining that formulation. A rename sweeps all surfaces. State what a function receives, returns and optimizes/interpolates, and which inputs vary or stay fixed.

A project that has renamed terms, or whose pages use a simpler term than its records, keeps one list of those terms in its [development conventions](documentation.md#canonical-homes): the term, a link to the record that defines it, and the words it replaces. The list defines nothing itself. Where a record keeps the older or more technical term on purpose, the list says so. A rename changes the list first, then sweeps all surfaces.

Decision rationale belongs beside the decision, including why an instrument/default was chosen and why alternatives lost. A decision the person made is kept with its date, who decided, the person's words and its known weakness. A baseline cited for current shipped behavior measures what ships; label retired baselines historical. An experimental verdict and deployment measurements are distinct content kinds.

Separate claims requiring different evidence: visual fidelity, smoothness, input preservation, correspondence with a source and physical accuracy. A local check or smoother drawing proves only its tested property. Label accepted future behavior, implemented behavior, CPU checks and native/runtime observations separately. Say "not measured" plainly and provide a supported bound where available. Never manufacture an estimate to fill an empty metric.

## Numbers and staleness

A current measured claim requires a source commit, exact reproduction command, runtime/environment, workload, units, baseline, method and scope. Link its raw result and limitations. Config values, derivations and design arithmetic are not measurements; cite their source and label them accordingly.

When code, input data, method, workload or runtime conditions affecting a claim change, rerun before quoting it as current evidence. Keep the old record's date, runtime, inputs and scope; a historical label does not qualify changed inputs. Presentation-only edits may reuse captured results only after checking identities, numbers and treatments remain intact.

A new reading of saved results is a result too: a breakdown the record does not give, a count across settings, a pattern found while drawing a figure. Before a page shows it, the record that owns the results gets a dated addition with the reading, how it is computed from the tracked data, and its scope. The addition says so when it reruns nothing and changes no earlier conclusion.

When a redesign restates numbers in new prose, figures or slides, record each number's source in a ledger and lock the evidence blocks kept verbatim. The project owns the ledger format and the checks for both. A slide face may show only numbers that its chapter also shows; every distinct number a redesigned chapter shows, figure labels included, has a ledger source. The kit's lint checks the part about slide faces: it warns when a face shows a number that its chapter does not show outside the face, as [slide faces and decks](site/authoring.md#slide-faces-and-decks) describes. The ledger of sources, and the checks of the ledger and of the locked blocks, stay the project's.

Keep protocols, snapshots, failed attempts, changed settings, actual outcomes, the results of reviews actually performed and relevant uncertainty with the work that produced them. For experiments, also retain producing code, inputs, run output, full result tables, source pins and any independent reviews performed in the experiment directory. A page, where one exists, explains what they establish. The worklog records the landing and hashes without duplicating tables. Retained measured content remains subject to the [deletion gate](documentation.md#rules-for-changes-and-chronology).

Run output is the raw result a claim links and what a person needs to check that claim again: the measured data, the result summaries, the run's own records and its logs. It is tracked in the experiment directory before the experiment is reported as complete. Output that exists only in an untracked build or temporary folder is not retained, and a claim that rests on it is [not measured](#naming-and-honest-claims). Every attempt keeps its entry in the record; its output is run output when a number or verdict the record states rests on it. Caches, environment copies and compiled bytecode are not run output. Name output that no stated number or verdict rests on in the [completion report](engineering/handoffs.md#reporting-completion) and propose its deletion.

Keeping run output outside Git is the person's decision. Ask, and give the size and the options. Until the person answers, the experiment is not complete: record the [unanswered question](engineering/delivery.md#decisions-and-blockers), and state in the experiment directory where the files are. When the person chooses a place outside Git, the experiment directory records where the files are and how to check they are the same files, for example by hash.

A source pin stands for producing code that lives in the repository when the run started from a clean tree, so that the pinned commit is the complete producing state, submodule pointers included; when that commit stays reachable on a branch or tag that is never rewritten; and when the experiment directory records the pin, the command and the identities of the inputs. The experiment directory then need not hold a copy of that code. The pin still stands for the code after the code is deleted from the current tree. The same holds for a plan, protocol or review document that a run recorded by hash: when a record in the repository gives its commit, path and hash, and that commit stays reachable on a branch or tag that is never rewritten, they stand for the document. Code that was not committed when the run started is kept in the experiment directory as a diff against the commit the run started from, with new files and changes inside submodules included; that commit is recorded and stays reachable as above. The project's own producing code that lives outside the repository is kept as a copy; a declared dependency is identified by its version. A run does not copy the working tree to record its source. Where a copy of the tree cannot be avoided, it holds only files that Git tracks or would track, never ignored files. An ignored file the run reads is an input and is recorded by its identity.

Historical records preserve their original source pins, inputs, runtime, settings, resource limits, deadlines and verdicts where those fields apply.

## Excerpts, formulas and figures

A record may carry a code excerpt, a formula or a figure. The rules about what such content may claim apply in a record as on a page; the layout and presentation rules do not.

- Code excerpts: the verified-excerpt and source-metadata rules in [code and diagrams](writing/code.md#code-and-diagrams).
- Formulas: the derivation and numerical-verification rules in [mathematical explanation](writing/math.md#mathematical-explanation).
- Screenshots and experiment visuals: the provenance rules in [run visuals and experiment lifecycle](writing/figures.md#run-visuals-and-experiment-lifecycle).

## Finished working documents

A plan, a decision record, a review or a coordination note exists to get a piece of work done. Delete it once that work has landed and its lasting content is in the owning record. [From open work to subject knowledge](documentation.md#from-open-work-to-subject-knowledge) gives the steps and the approval a deletion needs.

Git keeps the deleted document. Where something still needs it, cite the commit and path. A hash recorded for it stays valid, because Git returns the same bytes.

Do not keep a finished working document in the tree as an unedited file, and do not move it into an evidence folder. A rule that is in force lives in a current record.

Topic records and guides are edited in place, and the worklog is append-only, so neither leaves an old file behind. [Numbers and staleness](#numbers-and-staleness) lists what an experiment retains.

## Shelved investigations

Shelving is a scope decision recorded in the experiment's own guide and in the owning topic. Preserve inputs, code, failures and concrete recovery conditions there. Resumption requires a new explicit assignment. A hidden page may remain directly linkable with `hidden = true`; hiding neither deletes evidence nor qualifies a replacement.

## Changes, worklog and open work

The documentation system owns how a record changes. [Rules for changes and chronology](documentation.md#rules-for-changes-and-chronology) cover deletion, the worklog and probes. [From open work to subject knowledge](documentation.md#from-open-work-to-subject-knowledge) covers `OPEN.md` and work that matures into a topic.
