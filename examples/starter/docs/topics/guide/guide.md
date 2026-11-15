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

The numbered figures on the guide are authored by hand in the page source. Figures 2 and 3 are HTML flows written directly in `index.md`. Figures 1 and 4 are SVG drawings in `docs/site/fragments/ownership.html` and `docs/site/fragments/slide-anatomy.html`, which `index.md` includes in the numbered figures. The fragments carry no ids, so a page may include one more than once. The two slide faces are written in `index.md` itself and redraw their chapter's figure for the slide: the first as an HTML matrix, the second as inline SVG with an upright drawing that replaces the wide one below 720 px. All four depict ownership, information direction or page structure; they contain no measured quantities. Their source files are their generators. Changes require wide/narrow rendered inspection and reference/anchor checks. No remote media or fonts are required.

## Slide faces

The guide demonstrates slide faces on two chapters, following `.docs-kit/rules/writing/pages.md` (Slide faces):

- Faces come after the chapters. Build the chapters first, then ask the person whether the page should get faces; add none without a yes.
- A face shows one finding with a real visual that fills the canvas between the title and the scope line. The chapter's figures and numbers are its material: a face may crop, combine, annotate or redraw them, and it shows nothing its chapter does not state. Repeating the chapter's figure unchanged is the fallback.
- The shape of the finding sets the layout, and two faces share a layout only when their content has the same shape. The frame stays the same on every face: the label row and title at the top, the scope line at the bottom, the type roles and the tones. The guide's two faces show two shapes:
  - The first chapter's finding is who owns which folder. Its face is a matrix: the three folders of Figure 1 against what each holds, who writes it and when it changes. The two cells where the project is in control carry the accent, and the output's "never edited" is marked as a warning.
  - The slide-face chapter's finding is that a face is a view of its chapter. Its face draws Figure 4's face large beside the chapter card it opens, with a line from the chapter's figure to the face's visual; a chapter with nothing to show, and so no face, is the smaller limit.
  - Other findings take other shapes: a timeline, a row of steps above two conclusions, a figure beside a decisive number. The shared slide components, such as ruled points (`slide-points`) and a closing facts row (`slide-facts`), are parts to choose from; neither guide face needs them.
- Local slide classes stay with their face. Each guide face has a `<style>` element inside the face, so its classes travel into an extracted deck. The classes carry a prefix for that face, use container units and are marked `!important`, like the shared canvas; below 720 px a container query stacks the matrix into one card per folder or swaps the wide drawing for an upright one.
- Boxes of text are not a visual. A face whose main area only repeats the title and lead in boxes is removed, and a chapter with nothing to show gets no face.
- When a chapter needs a figure and has none, make the figure for the chapter first, from what exists; never draw invented data.
- No fact exists only on a slide: every statement on a face is also in its chapter. `docsite.py lint` checks the numbers and fails on a chapter with more than one face; the shared browser check `assertSlideFaces` measures each face in its chapter, a phone width of 390 px included.
- Text in a slide figure stays at least 11 px at a 390 px wide viewport. The figure fragments use 25 user units in a 600-unit-wide view box for their smallest labels; the faces' upright drawings use at least 14 units in a 340-unit-wide view box.

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
