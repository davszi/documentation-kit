# Code excerpts and diagrams

## Code and diagrams

Use a snippet only when it explains a seam or difficult contract better than prose. Excerpt real repository code, usually a signature and 3–10 decisive lines; link the rest. Use source metadata such as `python source=src/example.py#L42-L49` so drift checks can verify content and real line numbers. Do not present idealized pseudocode as a verified implementation excerpt. Put concise design rationale beside the code. Render excerpts with distinct type/class/function colors, a copy button, source chip, language badge and a line-number gutter showing actual source lines. Reuse shared code chrome and keep every control accessible.

Diagrams come from data or explicit local source and include overflow/collision checks or rendered QA. Shared color/edge semantics apply across pages: boxes denote named components, edges explicitly mean ownership/calls/data flow, dashed lines mean a documented optional path. Include a legend and name the data source in the caption. Numbered sequence steps, common-data mode views and quantitative generated SVGs are useful patterns.

Reuse supported pan/fullscreen/annotation controls where relevant. Do not claim planned edge highlighting, drill-down or semantic zoom as implemented. If added, choose drill-down for independent child diagrams with a breadcrumb, or semantic zoom when surrounding context must remain visible.
