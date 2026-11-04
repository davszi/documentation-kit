// carousel.js — turns each <div class="fig-carousel"> (a plain list of
// <img> tags in the page source) into a one-at-a-time slideshow with
// prev/next arrows, dot navigation, and gentle autoplay that pauses on
// hover and after any manual interaction. Images stay ordinary <img>
// elements, so the lightbox keeps working on the visible slide.
(() => {
  const style = document.createElement("style");
  style.textContent = `
    .fig-carousel { position: relative; margin: 1em 0; }
    .fig-carousel > img, .fig-carousel > .fig-unit { display: none;
      width: 100%; margin: 0 auto; }
    .fig-carousel > img.fc-active, .fig-carousel > .fig-unit.fc-active {
      display: block; }
    .fc-btn { position: absolute; top: 50%; transform: translateY(-50%);
      z-index: 5; background: rgba(20, 24, 32, 0.75); color: #dfe6ef;
      border: 1px solid rgba(255,255,255,.15); border-radius: 999px;
      width: 38px; height: 38px; font-size: 19px; line-height: 1;
      cursor: pointer; transition: background .15s; }
    .fc-btn:hover { background: rgba(60, 70, 90, 0.9); }
    .fc-prev { left: 8px; } .fc-next { right: 8px; }
    .fc-dots { display: flex; justify-content: center; gap: 7px;
      margin-top: 8px; flex-wrap: wrap; }
    .fc-dot { width: 9px; height: 9px; border-radius: 50%; border: 0;
      padding: 0; background: rgba(140, 150, 165, 0.4); cursor: pointer;
      transition: transform .15s, background .15s; }
    .fc-dot.fc-active { background: var(--bright, #7fd4ff);
      transform: scale(1.3); }
    .fc-label { text-align: center; color: #9aa4b2; font-size: 12.5px;
      margin-top: 4px; min-height: 1.2em; }
  `;
  document.head.appendChild(style);

  document.querySelectorAll(".fig-carousel").forEach((box) => {
    // slides: plain <img> or the .fig-unit wrappers plot-toggles built
    // around inlined SVGs (that script runs first — build emission order)
    const imgs = [...box.querySelectorAll(":scope > img, :scope > .fig-unit")];
    if (imgs.length < 2) return;
    const interval = parseInt(box.dataset.interval || "4500", 10);
    let idx = 0, timer = null, paused = false;

    const dots = document.createElement("div");
    dots.className = "fc-dots";
    const label = document.createElement("div");
    label.className = "fc-label";
    imgs.forEach((_, i) => {
      const d = document.createElement("button");
      d.className = "fc-dot";
      d.setAttribute("aria-label", `slide ${i + 1}`);
      d.addEventListener("click", () => { manual(); show(i); });
      dots.appendChild(d);
    });

    const mkBtn = (cls, txt, step) => {
      const b = document.createElement("button");
      b.className = `fc-btn ${cls}`;
      b.textContent = txt;
      b.addEventListener("click", () => { manual(); show(idx + step); });
      return b;
    };
    box.append(mkBtn("fc-prev", "‹", -1), mkBtn("fc-next", "›", +1), dots, label);

    function show(i) {
      idx = (i + imgs.length) % imgs.length;
      imgs.forEach((im, k) => im.classList.toggle("fc-active", k === idx));
      [...dots.children].forEach((d, k) =>
        d.classList.toggle("fc-active", k === idx));
      const el = imgs[idx];
      const inner = el.querySelector?.("svg.inline-fig");
      const name = (el.alt || inner?.getAttribute("aria-label")
        || el.src?.split("/").pop() || "").replace(/\.(png|svg)$/, "");
      label.textContent = `${name}  (${idx + 1}/${imgs.length})`;
    }
    function tick() {
      // never rotate under an open lightbox — the zoomed figure's slide
      // would change beneath the user
      if (!paused && !document.querySelector(".lb-overlay")) show(idx + 1);
    }
    function manual() {
      // a manual action stops autoplay for this carousel — predictable
      // reading beats surprise rotation once the user engages
      if (timer) { clearInterval(timer); timer = null; }
    }
    box.addEventListener("mouseenter", () => { paused = true; });
    box.addEventListener("mouseleave", () => { paused = false; });
    // opening a slide in the lightbox is engagement — stop autoplay so
    // the user returns to the slide they zoomed
    box.addEventListener("click", (e) => {
      if (e.target.closest("img, svg.inline-fig")) manual();
    });
    show(0);
    timer = setInterval(tick, interval);
  });
})();
