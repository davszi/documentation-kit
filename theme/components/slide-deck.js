// Extracted deck: overflow flags, present mode (P, arrows, space, Esc, F) and print.
(() => {
  const frames = [...document.querySelectorAll('.deck-frame')];
  // Authoring flag only: narrow layout is pure CSS and a stacked canvas cannot overflow.
  const flag = () => frames.forEach(frame => {
    const face = frame.querySelector('.slide-face'), canvas = face && (face.querySelector(':scope > .slide-canvas') || face);
    if (!canvas) return;
    const main = canvas.querySelector('.slide-main'), stacked = getComputedStyle(canvas).aspectRatio === 'auto';
    face.toggleAttribute('data-slide-overflow', !stacked && (canvas.scrollHeight > canvas.clientHeight + 1 || (!!main && main.scrollHeight > main.clientHeight + 1)));
  });
  let index = 0;
  const show = i => {
    index = Math.max(0, Math.min(frames.length - 1, i));
    frames.forEach((frame, n) => frame.classList.toggle('is-current', n === index));
    history.replaceState(null, '', '#' + frames[index].id);
  };
  const present = on => {
    document.body.classList.toggle('deck-presenting', on);
    if (on) {
      const hashed = frames.findIndex(frame => '#' + frame.id === location.hash);
      show(hashed >= 0 ? hashed : index);
    }
    requestAnimationFrame(flag);
  };
  document.querySelector('[data-deck-present]')?.addEventListener('click', () => present(true));
  document.querySelector('[data-deck-print]')?.addEventListener('click', () => window.print());
  document.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.target.closest('input, textarea, select')) return;
    const presenting = document.body.classList.contains('deck-presenting');
    if (event.key === 'p' || event.key === 'P') { present(!presenting); event.preventDefault(); return; }
    if (!presenting) return;
    if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { show(index + 1); event.preventDefault(); }
    else if (['ArrowLeft', 'PageUp'].includes(event.key)) { show(index - 1); event.preventDefault(); }
    else if (event.key === 'Home') show(0);
    else if (event.key === 'End') show(frames.length - 1);
    else if (event.key === 'Escape') present(false);
    else if (event.key === 'f' || event.key === 'F') {
      document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.();
    }
  });
  document.addEventListener('click', event => {
    if (!document.body.classList.contains('deck-presenting') || event.target.closest('a, button')) return;
    show(index + (event.clientX < innerWidth / 3 ? -1 : 1));
  });
  addEventListener('resize', flag);
  addEventListener('load', flag);
  document.fonts?.ready.then(flag);
  flag();
})();
