// fold-controls.js — the "Also show" bar for spine+fold pages without the
// chapter reader. Folds are typed <details> blocks emitted by build.py (fold:
// math / experiment / code / dead-end; "(open)" makes one start open). The bar
// offers only the kinds the page has: a kind switched on opens every fold of
// that kind page-wide, All switches every kind; with nothing on the reader is
// in the story. A reader's own click on one fold is saved and wins on the next
// visit. Deep links auto-open their fold. Storage matches the chapter reader.
(() => {
  const style = document.createElement("style");
  // Colours read the theme's properties with the kit's value as fallback, as the
  // other scripts do. A fold's hue reads --fold-color, which the chapter reader's
  // stylesheet sets per kind; without the reader the kit hue applies.
  style.textContent = `
    details.fold { border-left: 2px solid var(--fold-color, #666); border-radius: 0;
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
    details.fold-math { border-left-color: var(--fold-color, #a99df0); }
    details.fold-math > summary { color: var(--fold-color, #a99df0); }
    details.fold-experiment { border-left-color: var(--fold-color, #5dcaa5); }
    details.fold-experiment > summary { color: var(--fold-color, #5dcaa5); }
    details.fold-code { border-left-color: var(--fold-color, #85b7eb); }
    details.fold-code > summary { color: var(--fold-color, #85b7eb); }
    details.fold-dead-end { border-left-color: var(--fold-color, #f0997b); }
    details.fold-dead-end > summary { color: var(--fold-color, #f0997b); }
    details.fold > summary + * { margin-top: .6em; }
    .fold-bar { display: flex; flex-wrap: wrap; align-items: center;
      gap: 7px; margin: 1em 0 1.4em; position: sticky; top: 8px;
      z-index: 20; background: rgba(var(--bg-rgb, 13, 17, 23), 0.88);
      backdrop-filter: blur(4px); padding: 7px 10px; border-radius: 999px;
      border: 1px solid rgba(255,255,255,.1); width: fit-content; }
    .fold-bar .fb-label { font-size: 12px; opacity: .75; margin-right: 2px; }
    .fold-bar button { font: inherit; font-size: 12.5px; color: var(--chip-text, #cdd6e0);
      background: transparent; border: 1px solid rgba(255,255,255,.14);
      border-radius: 999px; padding: 3px 12px; cursor: pointer;
      transition: background .15s; }
    .fold-bar button:hover { background: rgba(var(--control-hover-rgb, 60, 70, 90), .5); }
    .fold-bar button[aria-pressed="true"] { background: rgba(var(--control-hover-rgb, 60, 70, 90), .75);
      border-color: rgba(255,255,255,.3); }
    .fold-bar .fb-all { display: inline-flex; align-items: center; gap: 7px; border: 0; }
    .fold-bar .fb-all::after { content: ""; width: 26px; height: 14px; border-radius: 999px;
      background: radial-gradient(circle at 7px 50%, var(--caption, #9aa4b2) 5px, transparent 5.5px), rgba(255,255,255,.16); }
    .fold-bar .fb-all[aria-checked="true"]::after {
      background: radial-gradient(circle at 19px 50%, var(--accent, #39d2c0) 5px, transparent 5.5px), rgba(var(--accent-rgb, 57, 210, 192), .35); }
  `;
  document.head.appendChild(style);

  // The chapter reader owns its own "Also show" options and routing. Keep this
  // component's fold styling; all other pages get this bar.
  if (document.querySelector('[data-fold-controls="columns"]')) return;

  const folds = [...document.querySelectorAll("details.fold")];
  if (!folds.length) return;

  const KINDS = [
    ["math", "Math"],
    ["experiment", "Experiments"],
    ["code", "Code"],
    ["dead-end", "Alternatives"],
  ];
  const present = KINDS.filter(([kind]) => folds.some((f) => f.dataset.fold === kind));
  const valid = (kind) => KINDS.some(([known]) => known === kind);
  const layersKey = "foldlayers:" + location.pathname;
  const statesKey = "foldstates:" + location.pathname;
  const LIMIT = 200;
  const read = (key) => { try { return JSON.parse(localStorage.getItem(key)); } catch (e) { return null; } };
  const write = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {} };

  // One set of switched-on kinds; the single mode of the earlier bar counts.
  let saved = read(layersKey);
  if (!Array.isArray(saved)) {
    let legacy = null;
    try { legacy = localStorage.getItem("foldmode:" + location.pathname); } catch (e) {}
    saved = legacy === "all" ? KINDS.map(([kind]) => kind) : valid(legacy) ? [legacy] : [];
  }
  const layers = new Set(saved.filter(valid));
  const stored = read(statesKey);
  const states = new Map(Array.isArray(stored) ? stored.filter((entry) => Array.isArray(entry)
    && typeof entry[0] === "string" && typeof entry[1] === "boolean").slice(-LIMIT) : []);
  const saveStates = () => {
    while (states.size > LIMIT) states.delete(states.keys().next().value);
    write(statesKey, [...states]);
  };

  // A fold is known by its section, kind and title; its author's open
  // attribute is its starting state when no option or click decides.
  const info = new Map(), seen = new Map();
  for (const fold of folds) {
    const summary = fold.querySelector("summary"), tag = summary?.querySelector(".fold-tag");
    const text = summary?.textContent || "";
    const title = (tag ? text.slice(tag.textContent.length) : text).trim();
    const base = (fold.closest("section[id]")?.id || "") + "|" + fold.dataset.fold + "|" + title;
    const count = (seen.get(base) || 0) + 1;
    seen.set(base, count);
    info.set(fold, {key: count > 1 ? base + "#" + count : base, authored: fold.open === true});
    summary?.addEventListener("click", (event) => {
      if (event.defaultPrevented) return;
      const key = info.get(fold).key;
      states.delete(key);
      states.set(key, !fold.open);
      saveStates();
    });
  }
  folds.forEach((fold) => {
    const known = info.get(fold), state = states.get(known.key);
    fold.open = state !== undefined ? state : layers.has(fold.dataset.fold) || known.authored;
  });

  let bar = document.querySelector(".fold-bar");
  if (!bar) {
    bar = document.createElement("div");
    const anchor = folds[0].closest("section") || folds[0];
    anchor.parentNode.insertBefore(bar, anchor);
  }
  bar.className = "fold-bar";
  bar.setAttribute("role", "group");
  bar.setAttribute("aria-label", "Also show, on this page");
  const label = document.createElement("span");
  label.className = "fb-label";
  label.setAttribute("aria-hidden", "true");
  label.textContent = "Also show";
  bar.appendChild(label);

  const buttons = [];
  const all = document.createElement("button");
  function sync() {
    for (const b of buttons) b.setAttribute("aria-pressed", String(layers.has(b.dataset.fold)));
    all.setAttribute("aria-checked", String(present.every(([kind]) => layers.has(kind))));
  }
  // An option sets every fold of its kinds and replaces their saved states.
  function setKinds(kinds, on) {
    for (const kind of kinds) { if (on) layers.add(kind); else layers.delete(kind); }
    folds.forEach((fold) => {
      if (!kinds.includes(fold.dataset.fold)) return;
      const known = info.get(fold);
      fold.open = on;
      states.delete(known.key);
      if (!on && known.authored) states.set(known.key, false);
    });
    write(layersKey, [...layers]);
    saveStates();
    sync();
  }
  for (const [kind, text] of present) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = text;
    b.dataset.fold = kind;
    b.addEventListener("click", () => setKinds([kind], !layers.has(kind)));
    buttons.push(b);
    bar.appendChild(b);
  }
  all.type = "button";
  all.className = "fb-all";
  all.setAttribute("role", "switch");
  all.textContent = "All";
  all.addEventListener("click", () => setKinds(present.map(([kind]) => kind), all.getAttribute("aria-checked") !== "true"));
  bar.appendChild(all);
  sync();
  // Folds of no known kind have nothing to offer here: no bar, only the deep links below.
  if (!present.length) bar.parentNode?.removeChild(bar);

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
