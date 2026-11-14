# The kit's browser-test dependency is not declared

Found on 2026-11-14 while writing the [dependencies rule](../../rules/engineering/code.md#dependencies).
Delete this record and its line in [KIT_OPEN.md](KIT_OPEN.md) when the kit
follows the rule or deivid decides the exception.

## What is wrong

The rule asks that every dependency the code needs stands in the project's
dependency file and is installed into the environment. The kit's four browser
suites need Playwright and Chromium. Neither is declared:

- `requirements.txt` holds the Python dependencies only, and the kit has no
  `package.json`.
- `tests/run_checks.sh` takes Playwright from the path in `DOCS_PLAYWRIGHT`
  and skips the browser suites when it is unset.
- The version, `playwright@1.62.1`, is written only in the Pages workflow,
  `.github/workflows/`, which installs it into a temporary folder.

So a fresh clone that follows the [README](../../README.md) gets no browser
suites, and a local run can use a different Playwright version than the
workflow.

## Question

How does the kit declare Playwright and Chromium for its browser suites?

## Options

- declare Playwright in a `package.json` with a lock file, install it in the
  README's setup steps and let the workflow install from the same file;
- or keep the path variables and state the exception in the rule's terms, with
  the pinned version in one tracked place that both the README and the
  workflow read.

## Recommendation

The first option. It is what the rule asks, and it puts the version in one
place.

## What waits on the answer

Nothing in the next release: the gap is in the kit's development checks.
Consumers are not affected, because building a site needs no Node.js.
