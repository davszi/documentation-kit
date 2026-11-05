// Slide faces: overflow flag and the bridge into the full chapter. Layout,
// including the narrow stacked mode, is pure CSS; this script only adds the
// bridge and an authoring flag. It runs after the chapter reader (component
// emission order), so faces already sit inside their .chapter-body.
document.addEventListener('DOMContentLoaded', () => {
  const faces = [...document.querySelectorAll('[data-slide-face]')];
  if (!faces.length) return;
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Authoring aid: ?slide-check outlines faces whose content does not fit.
  if (new URLSearchParams(location.search).has('slide-check')) document.documentElement.setAttribute('data-slide-check', '');

  // Overflow = canvas content taller than its 16:9 box, or the flexible middle squeezed.
  // A stacked (narrow) canvas has no fixed height and cannot overflow.
  const measure = face => {
    const canvas = face.querySelector(':scope > .slide-canvas') || face;
    const stacked = getComputedStyle(canvas).aspectRatio === 'auto';
    const main = canvas.querySelector('.slide-main');
    const over = !stacked && (canvas.scrollHeight > canvas.clientHeight + 1 || (!!main && main.scrollHeight > main.clientHeight + 1));
    face.toggleAttribute('data-slide-overflow', over);
  };
  const measureAll = () => faces.forEach(measure);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(entries => entries.forEach(entry => measure(entry.target)));
    faces.forEach(face => observer.observe(face));
  }
  document.fonts?.ready.then(measureAll);
  faces.forEach(face => face.querySelectorAll('img').forEach(image => image.addEventListener('load', () => measure(face), {once: true})));
  addEventListener('load', measureAll);

  // The element that currently scrolls this chapter: the card body in the
  // single/paired reader views, otherwise the window (All chapters, plain pages).
  const scrollerOf = face => {
    for (let node = face.parentElement; node && node !== document.body; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (/(auto|scroll)/.test(style.overflowY) && node.scrollHeight > node.clientHeight + 1) return node;
    }
    return null;
  };
  // A heading counts only when it is visible in normal reading: not inside a
  // closed fold, a hidden tab panel or another hidden container.
  const visibleHeading = node => {
    const candidates = node.matches('h2, h3') ? [node] : [...node.querySelectorAll('h2, h3')];
    return candidates.find(heading => {
      for (let up = heading; up && up !== node.parentElement; up = up.parentElement) {
        if (up.hidden || up.matches('details:not([open]) > :not(summary), [role="tabpanel"]')) return false;
      }
      return true;
    }) || null;
  };

  faces.forEach(face => {
    const chapter = face.closest('.chapter-body') || face.closest('[data-reader-chapter], section') || face.parentElement;
    chapter.classList.add('has-slide-face');
    if (!face.closest('.chapter-body')) chapter.classList.add('slide-chapter');

    // The first visible heading after the slide opens the full chapter. An eyebrow
    // directly before it repeats the slide's context and stays only for assistive technology.
    let heading = null;
    for (let node = face.nextElementSibling; node && !heading; node = node.nextElementSibling) heading = visibleHeading(node);
    let anchor = heading;
    if (heading) {
      heading.classList.add('slide-bridge-title');
      const before = heading.previousElementSibling;
      if (before && before.matches('.eyebrow, [data-slide-eyebrow]')) { before.classList.add('slide-bridged-eyebrow'); anchor = before; }
    }

    const faceWords = face.textContent.trim().split(/\s+/).filter(Boolean).length;
    const words = Math.max(0, chapter.textContent.trim().split(/\s+/).filter(Boolean).length - faceWords);
    const figures = [...chapter.querySelectorAll('figure, img, svg')]
      .filter(node => !node.closest('[data-slide-face], button, summary, a') && !node.parentElement.closest('figure, svg')).length;
    const bridge = document.createElement('div');
    bridge.className = 'slide-bridge';
    bridge.innerHTML = '<span class="slide-bridge-pill">Full chapter</span>' +
      `<span class="slide-bridge-meta">≈ ${Math.max(1, Math.round(words / 220))} min read · ${figures} ${figures === 1 ? 'figure' : 'figures'}</span>`;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'slide-bridge-button';
    bridge.appendChild(button);
    if (anchor) anchor.insertAdjacentElement('beforebegin', bridge);
    else face.insertAdjacentElement('afterend', bridge);

    const topIn = (element, scroller) => scroller
      ? element.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop
      : element.getBoundingClientRect().top + window.scrollY;
    let arrived = null;
    const sync = () => {
      const scroller = scrollerOf(face);
      const position = scroller ? scroller.scrollTop : window.scrollY;
      const furthest = scroller ? scroller.scrollHeight - scroller.clientHeight
        : document.documentElement.scrollHeight - window.innerHeight;
      // "Arrived" once the bridge reaches the top of the visible area, or the
      // chapter is too short for that and is scrolled as far as it goes.
      const now = position >= Math.min(topIn(bridge, scroller), furthest) - 48 && position > 8;
      if (now === arrived) return;
      arrived = now;
      button.innerHTML = now ? 'Back to slide <span aria-hidden="true">↑</span>' : 'Continue reading <span aria-hidden="true">↓</span>';
      button.classList.toggle('is-back', now);
    };
    // Scroll events do not bubble; capture catches the card body as well as the window.
    document.addEventListener('scroll', sync, {passive: true, capture: true});
    addEventListener('resize', sync);
    sync();
    button.addEventListener('click', () => {
      const scroller = scrollerOf(face);
      const target = arrived ? topIn(face, scroller) - 8 : topIn(bridge, scroller) - 4;
      (scroller || window).scrollTo({top: Math.max(0, target), behavior: reduce() ? 'auto' : 'smooth'});
    });
  });
});
