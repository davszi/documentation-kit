// fold-controls.js — the reader-mode bar for spine+fold pages. Folds are
// typed <details> blocks emitted by build.py (fold: math / experiment /
// code / dead-end). The bar opens every fold of a kind page-wide: the
// math reader clicks "+ math" once and reads linearly; the skimmer keeps
// everything closed and still gets a complete story. Individual folds
// stay clickable regardless of mode. Deep links auto-open their fold.
(() => {
  const style = document.createElement("style");
  style.textContent = `
    details.fold { border-left: 2px solid #666; border-radius: 0;
      margin: 0.9em 0; padding: 2px 0 2px 14px; }
    details.fold > summary { cursor: pointer; list-style: none;
      font-size: 0.92em; user-select: none; opacity: .92; }
    details.fold > summary::-webkit-details-marker { display: none; }
    details.fold > summary::before { content: "▸"; display: inline-block;
      margin-right: 7px; transition: transform .15s; }
    details.fold[open] > summary::before { transform: rotate(90deg); }
    .fold-tag { font-size: 11px; letter-spacing: .04em;
      padding: 1px 8px; border-radius: 999px; margin-right: 7px;
      border: 1px solid currentColor; opacity: .9; }
    details.fold-math { border-left-color: #a99df0; }
    details.fold-math > summary { color: #a99df0; }
    details.fold-experiment { border-left-color: #5dcaa5; }
    details.fold-experiment > summary { color: #5dcaa5; }
    details.fold-code { border-left-color: #85b7eb; }
    details.fold-code > summary { color: #85b7eb; }
    details.fold-dead-end { border-left-color: #f0997b; }
    details.fold-dead-end > summary { color: #f0997b; }
    details.fold > summary + * { margin-top: .6em; }
    .fold-bar { display: flex; flex-wrap: wrap; align-items: center;
      gap: 7px; margin: 1em 0 1.4em; position: sticky; top: 8px;
      z-index: 20; background: rgba(14, 17, 23, 0.88);
      backdrop-filter: blur(4px); padding: 7px 10px; border-radius: 999px;
      border: 1px solid rgba(255,255,255,.1); width: fit-content; }
    .fold-bar .fb-label { font-size: 12px; opacity: .6; margin-right: 2px; }
    .fold-bar button { font: inherit; font-size: 12.5px; color: #cdd6e0;
      background: transparent; border: 1px solid rgba(255,255,255,.14);
      border-radius: 999px; padding: 3px 12px; cursor: pointer;
      transition: background .15s; }
    .fold-bar button:hover { background: rgba(60, 70, 90, .5); }
    .fold-bar button.on { background: rgba(90, 105, 135, .45);
      border-color: rgba(255,255,255,.3); }
  `;
  document.head.appendChild(style);

  // The chapter-reader prototype owns its column-scoped controls and routing.
  // Keep this component's fold styling; all other pages retain the global bar.
  if (document.querySelector('[data-fold-controls="columns"]')) return;

  const folds = [...document.querySelectorAll("details.fold")];
  if (!folds.length) return;

  const KINDS = [
    ["none", "story"],
    ["math", "+ math"],
    ["experiment", "+ experiments"],
    ["code", "+ code"],
    ["dead-end", "+ dead ends"],
    ["all", "everything"],
  ];
  const key = "foldmode:" + location.pathname;

  let bar = document.querySelector(".fold-bar");
  if (!bar) {
    bar = document.createElement("div");
    const anchor = folds[0].closest("section") || folds[0];
    anchor.parentNode.insertBefore(bar, anchor);
  }
  bar.className = "fold-bar";
  const label = document.createElement("span");
  label.className = "fb-label";
  label.textContent = "read:";
  bar.appendChild(label);

  const btns = new Map();
  function setMode(mode, persist = true) {
    folds.forEach((f) => {
      f.open = mode === "all" || f.dataset.fold === mode;
    });
    btns.forEach((b, k) => b.classList.toggle("on", k === mode));
    if (persist) try { localStorage.setItem(key, mode); } catch (e) {}
  }
  for (const [kind, text] of KINDS) {
    const b = document.createElement("button");
    b.textContent = text;
    b.addEventListener("click", () => setMode(kind));
    btns.set(kind, b);
    bar.appendChild(b);
  }

  let saved = null;
  try { saved = localStorage.getItem(key); } catch (e) {}
  setMode(saved || "none", false);
  btns.forEach((b, k) => b.classList.toggle("on", k === (saved || "none")));

  // deep links: opening a hash inside a closed fold expands the chain
  function openHash() {
    if (!location.hash) return;
    const el = document.getElementById(location.hash.slice(1));
    if (!el) return;
    let d = el.closest("details.fold");
    while (d) { d.open = true; d = d.parentElement?.closest("details.fold"); }
    el.scrollIntoView();
  }
  window.addEventListener("hashchange", openHash);
  openHash();
})();
