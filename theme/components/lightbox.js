// lightbox.js — click any content figure to open it full-screen with
// wheel zoom + drag pan. Wired by the `lightbox` component entry.
(() => {
  const style = document.createElement("style");
  style.textContent = `
    .lb-overlay { position: fixed; inset: 0; z-index: 1000;
      background: rgba(8, 10, 14, 0.92); cursor: zoom-out;
      overflow: hidden; }
    /* the transform is the ONLY positioner: absolute top-left origin,
       no flex centering underneath it (that double-offset put the
       image in the bottom-right corner) */
    .lb-overlay img, .lb-overlay svg { position: absolute; left: 0;
      top: 0; max-width: none; max-height: none;
      transform-origin: 0 0; cursor: grab; user-select: none;
      box-shadow: 0 8px 40px rgba(0,0,0,.6); border-radius: 4px;
      background: #101319; margin: 0; }
    .lb-overlay img.lb-drag, .lb-overlay svg.lb-drag { cursor: grabbing; }
    .lb-overlay .fig-chips { position: fixed; top: 12px; left: 50%;
      transform: translateX(-50%); z-index: 1001; margin: 0;
      max-width: 92vw; cursor: default; }
    .lb-hint { position: fixed; bottom: 14px; left: 50%;
      transform: translateX(-50%); color: #9aa4b2; font-size: 12px;
      font-family: inherit; pointer-events: none; }
    main img, .card img, .ptab-panel img { cursor: zoom-in; }
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
      img.classList.remove("inline-fig");
      const vb = (img.getAttribute("viewBox") || "0 0 1200 600").split(/\s+/);
      natW = parseFloat(vb[2]);
      natH = parseFloat(vb[3]);
      img.style.width = natW + "px";
      img.style.height = natH + "px";
      // same line-toggle chips as on the page, mirrored back to the
      // original figure so a toggle done while zoomed persists
      chips = window.figToggles?.buildChips(img, target) || null;
    }
    const hint = document.createElement("div");
    hint.className = "lb-hint";
    hint.textContent = "scroll to zoom · drag to pan · double-click to reset · Esc to close";
    overlay.append(img, hint);
    if (chips) overlay.appendChild(chips);
    document.body.appendChild(overlay);
    document.addEventListener("keydown", onKey);

    let scale = 1, tx = 0, ty = 0;
    const apply = () => {
      img.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
    };
    const fitInit = () => {
      const w = natW || img.naturalWidth, h = natH || img.naturalHeight;
      const fit = Math.min(
        (window.innerWidth * 0.94) / w,
        (window.innerHeight * 0.94) / h, 1);
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
    let drag = null;
    img.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      drag = { x: e.clientX - tx, y: e.clientY - ty };
      img.classList.add("lb-drag");
      img.setPointerCapture(e.pointerId);
    });
    img.addEventListener("pointermove", (e) => {
      if (!drag) return;
      tx = e.clientX - drag.x;
      ty = e.clientY - drag.y;
      apply();
    });
    img.addEventListener("pointerup", () => {
      drag = null;
      img.classList.remove("lb-drag");
    });
    img.addEventListener("dblclick", fitInit);
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) close();
    });
  }

  document.addEventListener("click", (e) => {
    if (e.target.closest(".fig-chips")) return;  // chip clicks are toggles
    const svg = e.target.closest("svg.inline-fig");
    if (svg && !svg.closest(".lb-overlay")) return open(svg);
    const img = e.target.closest("main img, .card img, .ptab-panel img");
    if (!img || img.closest(".lb-overlay") || img.closest("a")) return;
    open(img.currentSrc || img.src);
  });
})();
