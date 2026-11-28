// fold-controls.js — the "Also show" bar for spine+fold pages without the
// chapter reader. Folds are typed <details> blocks emitted by build.py (fold:
// math / experiment / code / dead-end; "(open)" makes one start open). The bar
// offers only the kinds the page has: a kind switched on opens every fold of
// that kind page-wide, All switches every fold, the folds of no kind (fold:
// detail) among them, which have no option of their own; with nothing on the
// reader is in the story. A reader's own click on one fold is saved and wins on the next
// visit. Deep links auto-open their fold. Storage matches the chapter reader.
(() => {
  // The folds' and the bar's styles are in fold-controls.css. The chapter reader
  // owns its own "Also show" options and routing: the build leaves this script
  // off its pages, and a page that carries the reader's bar anyway gets no bar.
  if (document.querySelector('[data-fold-controls="columns"]')) return;

  const folds = [...document.querySelectorAll("details.fold")];
  if (!folds.length) return;

  const KINDS = [
    ["math", "Math"],
    ["experiment", "Experiments"],
    ["code", "Code"],
    ["dead-end", "Not chosen"],
  ];
  // A fold of no kind has no option; All opens it, and it is stored like a kind.
  const DETAIL = "detail";
  const present = KINDS.filter(([kind]) => folds.some((f) => f.dataset.fold === kind));
  const presentLayers = [...present.map(([kind]) => kind), ...(folds.some((f) => f.dataset.fold === DETAIL) ? [DETAIL] : [])];
  const valid = (kind) => kind === DETAIL || KINDS.some(([known]) => known === kind);
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
    saved = legacy === "all" ? [...KINDS.map(([kind]) => kind), DETAIL] : valid(legacy) ? [legacy] : [];
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
    all.setAttribute("aria-checked", String(presentLayers.every((kind) => layers.has(kind))));
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
  all.addEventListener("click", () => setKinds(presentLayers, all.getAttribute("aria-checked") !== "true"));
  bar.appendChild(all);
  sync();
  // Folds of an unknown kind have nothing to offer here: no bar, only the deep links below.
  if (!presentLayers.length) bar.parentNode?.removeChild(bar);

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
