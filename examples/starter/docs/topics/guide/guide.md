# Authoring example: source, evidence and reader

## Scope

This topic owns the starter's illustrative documentation architecture and acceptance checklist. It makes no claim about application behavior, benchmark results or completed browser checks. The human-facing explanation is `index.md`.

## Ownership

| Item | Canonical owner |
|---|---|
| Project orientation and commands | `docs/PROJECT_CONTEXT.md` |
| Site title, source repository/ref and navigation | `docs/site/site.toml` |
| Shared rules, reader and theme | Pinned `.docs-kit` submodule |
| Subject facts and future accepted requirements | The relevant named topic record |
| Human explanation | Topic `index.md`, drawn from its record |
| Raw experiment evidence | Producing experiment directory |
| Unfinished work routing | `docs/open/OPEN.md` |
| Chronology | `docs/worklog.md` |

## Diagram sources

The numbered figures on the guide are authored by hand in the page source. Figures 2 and 3 are HTML flows written directly in `index.md`. Figures 1 and 4 are SVG drawings in `docs/site/fragments/ownership.html` and `docs/site/fragments/slide-anatomy.html`; `index.md` includes each fragment twice, in the numbered figure and in its chapter's slide face, so the slide cannot drift from the figure. The fragments carry no ids, so they can appear twice on one page. All four depict ownership, information direction or page structure; they contain no measured quantities. Their source files are their generators. Changes require wide/narrow rendered inspection and reference/anchor checks. No remote media or fonts are required.

## Slide faces

The guide demonstrates slide faces on two chapters, following `.docs-kit/rules/writing/pages.md` (Slide faces):

- Faces come after the chapters. Build the chapters first, then ask the person whether the page should get faces; add none without a yes.
- A face shows one finding with a real visual: the chapter's own figure, drawn large enough to fill most of the canvas between the title and the scope line, with its parts numbered 01, 02 and so on.
- The shape of the content sets the layout. The guide's face is one example: beside the figure, numbered points (`slide-points`) each give a short claim in bold and a sentence or two that explain it, separated by thin rules. Only the points the title names are emphasised (`is-key`); a warning point carries a cross (`is-alert`). A closing row (`slide-facts`) gives facts the chapter states, each as a small label over a value, and the scope line ends the face. Another face may be one figure across the canvas with labels on its parts, a row of steps or a matrix.
- Boxes of text are not a visual. A face whose main area only repeats the title and lead in boxes is removed, and a chapter with nothing to show gets no face.
- When a chapter needs a figure and has none, make the figure for the chapter first, from what exists; never draw invented data.
- No fact exists only on a slide: every statement on a face is also in its chapter.
- Text in a slide figure stays at least 11 px at a 390 px wide viewport; the drawings use 25 user units in a 600-unit-wide view box for their smallest labels.

## Acceptance checklist

- Initialize a version-pinned shared-kit submodule and configure the real source repository/ref.
- Register every published page; keep links and public anchors stable.
- Build, check freshness and lint from the project root.
- Inspect wide, narrow and two-column reading, keyboard/focus, reduced motion, print and no-JavaScript fallback.
- Keep each measured claim linked to source revision, inputs, runtime, command, units and results.
- Rerun before applying a result to changed measured inputs or behavior.
- State checks as passed only after they have actually run.

## Example verdict

The starter demonstrates the shared-kit architecture selected for this package. Alternatives in the human page compare ownership and maintenance costs rather than measured timing. A project adopting the starter still owns its integration and review checks.
