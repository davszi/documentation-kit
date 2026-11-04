// plot-toggles.js — per-line toggles for inlined SVG figures. Any artist
// the generator tagged with gid "tg-<group>--<n>" becomes toggleable: one
// chip per <group>, clicking hides/shows every element of that group
// (path panel, inset and curvature panel together). Each SVG is wrapped
// in a .fig-unit so downstream components (carousel) treat figure+chips
// as one slide. Runs before carousel.js (emission order in build.py).
// Exposes window.figToggles.buildChips(svg, mirror) so the lightbox can
// offer the same chips on its zoomed clone and mirror state back to the
// page figure.
(() => {
  const style = document.createElement("style");
  style.textContent = `
    .fig-unit { display: block; margin: 1em 0; }
    .fig-chips { display: flex; flex-wrap: wrap; gap: 7px;
      justify-content: center; margin-top: 6px; }
    .fig-chip { display: inline-flex; align-items: center; gap: 6px;
      font-size: 12.5px; color: #cdd6e0; background: rgba(30, 36, 48, .6);
      border: 1px solid rgba(255,255,255,.12); border-radius: 999px;
      padding: 3px 11px; cursor: pointer; user-select: none;
      transition: opacity .15s, background .15s; }
    .fig-chip:hover { background: rgba(55, 65, 85, .8); }
    .fig-chip.off { opacity: .38; }
    .fig-chip.off .fig-dot { background: transparent !important;
      border: 1px solid currentColor; }
    .fig-dot { width: 10px; height: 10px; border-radius: 3px;
      flex: none; }
  `;
  document.head.appendChild(style);

  const LABELS = {
    pinned: "κ=0 joints",
    menger: "Menger joints (default)",
    stacked: "optimized joints",
    heuristic: "Menger heuristic",
    free_psi: "free_psi",
    free_kappa: "free_kappa",
    free_both: "free_both",
    corridor: "road corridor",
    waypoints: "waypoints",
  };

  function collect(svg) {
    const groups = {};
    svg.querySelectorAll('[id^="tg-"]').forEach((el) => {
      const key = el.id.slice(3).split("--")[0];
      (groups[key] ||= []).push(el);
    });
    return groups;
  }

  function strokeOf(group) {
    for (const el of group) {
      const p = el.matches("path") ? el : el.querySelector("path");
      if (!p) continue;
      const s = getComputedStyle(p);
      for (const c of [s.stroke, s.fill]) {
        if (c && c !== "none" && c !== "rgba(0, 0, 0, 0)") return c;
      }
    }
    return "#9aa4b2";
  }

  // Chips controlling `svg`'s groups; toggles are mirrored onto `mirror`
  // (the page original, when called from the lightbox) so a hide done
  // while zoomed persists after closing.
  function buildChips(svg, mirror = null) {
    const groups = collect(svg);
    const keys = Object.keys(groups);
    if (!keys.length) return null;
    const mirrorGroups = mirror ? collect(mirror) : null;
    const chips = document.createElement("div");
    chips.className = "fig-chips";
    for (const key of keys) {
      const els = groups[key];
      const chip = document.createElement("button");
      chip.className = "fig-chip";
      if (els[0].style.display === "none") chip.classList.add("off");
      const dot = document.createElement("span");
      dot.className = "fig-dot";
      dot.style.background = strokeOf(els);
      chip.append(dot, document.createTextNode(LABELS[key] || key));
      chip.addEventListener("click", (e) => {
        e.stopPropagation();
        const off = chip.classList.toggle("off");
        els.forEach((el) => { el.style.display = off ? "none" : ""; });
        mirrorGroups?.[key]?.forEach((el) => {
          el.style.display = off ? "none" : "";
        });
      });
      chips.appendChild(chip);
    }
    return chips;
  }

  window.figToggles = { buildChips };

  document.querySelectorAll("svg.inline-fig").forEach((svg) => {
    const unit = document.createElement("span");
    unit.className = "fig-unit";
    svg.parentNode.insertBefore(unit, svg);
    unit.appendChild(svg);
    const chips = buildChips(svg);
    if (chips) unit.appendChild(chips);
  });
})();
