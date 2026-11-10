# Lint does not check HTML links to repository files

Open work. Evidence is verified; the fix is not decided.

## What is missing

Lint checks Markdown links in records and pages: the target must exist and its
anchor must resolve. It does not check a link written as HTML, `<a href="…">`,
that points at a repository file. Topic pages use such links often, because
their bodies are largely HTML.

## Evidence

- 2026-11-09: the 2.0.0 starter home page linked `../project/PROJECT_CONTEXT.md`,
  a file that does not exist. Strict lint never reported it.
- 2026-11-10: an independent reviewer upgraded a simulated consumer to the
  3.0.0 state. It put `<a href="../../.docs-kit/rules/writing.md#numbers-and-staleness">`
  in a page body after that anchor had been removed. `lint --strict` printed
  `lint clean (0 warning(s))`.

## Why it is not simply fixed

Checking these links adds lint errors to projects that pass today. Under
[what a version number promises](../topics/releases/releases.md#what-a-version-number-promises)
that is a major change, and its size in the consuming projects is not measured.

## Next step

Measure how many HTML links to repository files the consuming projects have and
how many would fail. Then decide between an error, a warning and a note.
