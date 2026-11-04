// Independent local comparisons: buttons select panels, hashes reveal their
// target, and print temporarily exposes every option. No script: all readable.
(() => {
  document.querySelectorAll('[data-panel-switcher]').forEach(root => {
    const buttons = [...root.querySelectorAll('[data-panel-choice]')];
    const panels = [...root.querySelectorAll('[data-panel]')];
    if (!buttons.length || buttons.length !== panels.length) return;
    const select = value => {
      if (!panels.some(panel => panel.dataset.panel === value)) return;
      panels.forEach(panel => {panel.hidden = panel.dataset.panel !== value;});
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.panelChoice === value)));
    };
    const followHash = () => {
      let target;
      try {target = document.getElementById(decodeURIComponent(location.hash.slice(1)));} catch {return false;}
      const panel = target && panels.find(panel => panel === target || panel.contains(target));
      if (panel) select(panel.dataset.panel);
      return Boolean(panel);
    };
    root.dataset.panelReady = 'true';
    buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.panelChoice)));
    select(root.dataset.panelDefault || panels[0].dataset.panel);
    followHash();
    window.addEventListener('hashchange', followHash);
    let beforePrint;
    window.addEventListener('beforeprint', () => {
      beforePrint = panels.map(panel => panel.hidden);
      panels.forEach(panel => {panel.hidden = false;});
    });
    window.addEventListener('afterprint', () => {
      if (beforePrint) panels.forEach((panel, index) => {panel.hidden = beforePrint[index];});
    });
  });
})();
