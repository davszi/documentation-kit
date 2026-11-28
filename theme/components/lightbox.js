// lightbox.js — click or tap any picture or drawing in a page's content to
// open it full-screen: wheel or pinch zooms, drag pans. A drawing is a vector
// drawing there as on the page, so it stays sharp at any size; a drawing
// therefore fits its column on the page and is enlarged here. Wired by the
// `lightbox` component entry; the build adds it to every page with a picture
// or a drawing. `data-zoom="off"` on a drawing or around it leaves it alone.
(() => {
  const style = document.createElement("style");
  style.textContent = `
    .lb-overlay { position: fixed; inset: 0; z-index: 1000;
      background: rgba(var(--overlay-rgb, 8, 10, 14), 0.92); cursor: zoom-out;
      overflow: hidden; touch-action: none; }
    .lb-close { position: fixed; top: 10px; right: 12px; z-index: 1002; width: 40px; height: 40px;
      border-radius: 999px; border: 1px solid rgba(255,255,255,.22); cursor: pointer;
      background: rgba(var(--overlay-rgb, 8, 10, 14), 0.8); color: var(--text, #e6edf3);
      font: inherit; font-size: 20px; line-height: 1; }
    .lb-close:focus-visible { outline: 2px solid var(--accent, #39d2c0); outline-offset: 2px; }
    /* the transform is the ONLY positioner: absolute top-left origin,
       no flex centering underneath it (that double-offset put the
       image in the bottom-right corner) */
    .lb-overlay img, .lb-overlay svg { position: absolute; left: 0;
      top: 0; max-width: none; max-height: none;
      transform-origin: 0 0; cursor: grab; user-select: none;
      box-shadow: 0 8px 40px rgba(0,0,0,.6); border-radius: 4px;
      background: var(--lightbox-bg, #101319); margin: 0; }
    .lb-overlay img.lb-drag, .lb-overlay svg.lb-drag { cursor: grabbing; }
    /* The bar spans the window less a 4vw margin on each side and wraps
       whole chips; centred with left: 50% it shrank to half the window and
       broke long labels inside their chips. Only the chips take clicks, so
       a click beside them still closes the lightbox. */
    .lb-overlay .fig-chips { position: fixed; top: 12px; left: 4vw;
      right: 4vw; z-index: 1001; margin: 0; pointer-events: none; }
    .lb-overlay .fig-chip { pointer-events: auto; cursor: pointer; }
    .lb-hint { position: fixed; bottom: 14px; left: 50%;
      transform: translateX(-50%); color: var(--caption, #9aa4b2); font-size: 12px;
      font-family: inherit; pointer-events: none; }
    main img, .card img, .ptab-panel img, svg[data-zoomable] { cursor: zoom-in; }
  `;
  document.head.appendChild(style);

  let overlay = null;

  function close() {
    if (overlay) { overlay.remove(); overlay = null; }
    document.removeEventListener("keydown", onKey);
  }
  function onKey(e) { if (e.key === "Escape") close(); }

  function open(target) {
    close();
    overlay = document.createElement("div");
    overlay.className = "lb-overlay";
    let img, natW, natH, chips = null;
    if (typeof target === "string") {
      img = document.createElement("img");
      img.src = target;
    } else {
      // inline SVG: clone it — vector, so the zoom stays crisp forever;
      // drop the page-layout class (max-width/margin would fight the
      // transform positioning)
      img = target.cloneNode(true);
      // A drawing's look can come from rules that name what is around it on
      // the page. The copy stands outside that, so it carries each part's
      // computed look itself.
      const parts = [target, ...target.querySelectorAll("*")], copies = [img, ...img.querySelectorAll("*")];
      parts.forEach((part, i) => {
        const look = getComputedStyle(part), copy = copies[i];
        if (!copy || !copy.style) return;
        LOOK.forEach(name => copy.style.setProperty(name, look.getPropertyValue(name)));
      });
      img.classList.remove("inline-fig");
      img.removeAttribute("data-zoomable");
      const vb = (img.getAttribute("viewBox") || "0 0 1200 600").split(/[\s,]+/);
      natW = parseFloat(vb[2]);
      natH = parseFloat(vb[3]);
      img.style.cssText = "";
      img.style.width = natW + "px";
      img.style.height = natH + "px";
      img.style.display = "block";
      // same line-toggle chips as on the page, mirrored back to the
      // original figure so a toggle done while zoomed persists
      chips = window.figToggles?.buildChips(img, target) || null;
    }
    const hint = document.createElement("div");
    hint.className = "lb-hint";
    hint.textContent = "scroll or pinch to zoom · drag to pan · double-click to reset · Esc to close";
    const shut = document.createElement("button");
    shut.type = "button";
    shut.className = "lb-close";
    shut.setAttribute("aria-label", "Close");
    shut.textContent = "×";
    shut.addEventListener("click", close);
    overlay.append(img, hint, shut);
    if (chips) overlay.appendChild(chips);
    document.body.appendChild(overlay);
    document.addEventListener("keydown", onKey);

    let scale = 1, tx = 0, ty = 0;
    const apply = () => {
      img.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
    };
    const fitInit = () => {
      const w = natW || img.naturalWidth, h = natH || img.naturalHeight;
      // A picture is not enlarged past its own pixels to start with; a drawing has none and fills the window.
      const fit = Math.min(
        (window.innerWidth * 0.94) / w,
        (window.innerHeight * 0.94) / h, natW ? Infinity : 1);
      scale = fit;
      tx = (window.innerWidth - w * scale) / 2;
      ty = (window.innerHeight - h * scale) / 2;
      apply();
    };
    if (natW) fitInit();
    img.addEventListener("load", fitInit);
    overlay.addEventListener("wheel", (e) => {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 1.18 : 1 / 1.18;
      const ns = Math.min(Math.max(scale * factor, 0.05), 40);
      // zoom around the cursor
      tx = e.clientX - (e.clientX - tx) * (ns / scale);
      ty = e.clientY - (e.clientY - ty) * (ns / scale);
      scale = ns;
      apply();
    }, { passive: false });
    // One pointer drags; two pinch, around the point between them.
    let drag = null, pinch = null;
    const down = new Map();
    const between = () => {
      const [a, b] = [...down.values()];
      return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2, far: Math.hypot(a.x - b.x, a.y - b.y) || 1 };
    };
    img.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      down.set(e.pointerId, { x: e.clientX, y: e.clientY });
      // A pointer the browser no longer has, as in a test, cannot be captured; the gesture goes on without.
      try { img.setPointerCapture(e.pointerId); } catch (error) { /* not captured */ }
      if (down.size === 2) { drag = null; pinch = { ...between(), scale, tx, ty }; return; }
      drag = { x: e.clientX - tx, y: e.clientY - ty };
      img.classList.add("lb-drag");
    });
    img.addEventListener("pointermove", (e) => {
      if (!down.has(e.pointerId)) return;
      down.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pinch && down.size === 2) {
        const now = between();
        const ns = Math.min(Math.max(pinch.scale * now.far / pinch.far, 0.05), 40);
        tx = now.x - (pinch.x - pinch.tx) * (ns / pinch.scale);
        ty = now.y - (pinch.y - pinch.ty) * (ns / pinch.scale);
        scale = ns;
        apply();
        return;
      }
      if (!drag) return;
      tx = e.clientX - drag.x;
      ty = e.clientY - drag.y;
      apply();
    });
    const up = (e) => {
      down.delete(e.pointerId);
      pinch = null;
      // The finger that stays goes on dragging from where it is.
      const rest = [...down.values()][0];
      drag = rest ? { x: rest.x - tx, y: rest.y - ty } : null;
      if (!rest) img.classList.remove("lb-drag");
    };
    img.addEventListener("pointerup", up);
    img.addEventListener("pointercancel", up);
    img.addEventListener("dblclick", fitInit);
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) close();
    });
  }

  // What of a drawing's look its copy carries along.
  const LOOK = ["fill", "fill-opacity", "fill-rule", "stroke", "stroke-width", "stroke-opacity", "stroke-dasharray",
    "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "opacity", "color", "font-family", "font-size",
    "font-weight", "font-style", "font-variant-numeric", "letter-spacing", "text-anchor", "dominant-baseline",
    "paint-order", "display", "visibility", "mix-blend-mode"];
  const CONTROLS = "a, button, summary, input, select, textarea, label, [role=button], [tabindex]";
  const OUTSIDE = ".lb-overlay, .diagram-wrap, .fig-chips, .reader-bar, .reader-rail, .reader-island, nav, [data-zoom=off]";

  // The drawing a click or a pointer is on, if it is one a reader would enlarge:
  // in the page's content, large enough to be a figure and not an icon, and
  // not itself a control or inside one.
  function drawingAt(target) {
    if (!(target instanceof Element)) return null;
    let svg = target.closest("svg");
    if (!svg) return null;
    while (svg.parentElement && svg.parentElement.closest("svg")) svg = svg.parentElement.closest("svg");
    if (svg.classList.contains("inline-fig")) return svg.closest(".lb-overlay") ? null : svg;
    if (!svg.hasAttribute("viewBox") || !svg.closest("main, .card, .ptab-panel") || svg.closest(OUTSIDE)) return null;
    const control = target.closest(CONTROLS);
    if ((control && svg.contains(control)) || svg.closest("a, button, summary, label")) return null;
    // A drawing fitted into a phone column is small; an icon or a meter is smaller still.
    const box = svg.getBoundingClientRect();
    return box.width >= 120 && box.height >= 48 ? svg : null;
  }

  // The pointer shows that a drawing opens, once it is over one.
  document.addEventListener("pointerover", (e) => {
    const svg = drawingAt(e.target);
    if (svg && !svg.hasAttribute("data-zoomable")) svg.setAttribute("data-zoomable", "");
  }, { passive: true });

  document.addEventListener("click", (e) => {
    if (e.target.closest(".fig-chips")) return;  // chip clicks are toggles
    // A click the page already used, or the end of a text selection, opens nothing.
    if (e.defaultPrevented || String(window.getSelection?.() || "")) return;
    const svg = drawingAt(e.target);
    if (svg) return open(svg);
    const img = e.target.closest("main img, .card img, .ptab-panel img");
    if (!img || img.closest(".lb-overlay") || img.closest("a")) return;
    open(img.currentSrc || img.src);
  });
})();
