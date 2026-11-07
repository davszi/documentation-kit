// Source content is the fallback: no chapters are hidden or cloned.
document.addEventListener('DOMContentLoaded', () => {
  const nav = document.getElementById('chapter-reader');
  const config = document.querySelector('[data-reader-title]');
  const content = document.querySelector('.content');
  const sidebar = document.getElementById('sidebar');
  const toc = document.getElementById('toc');
  const links = [...document.querySelectorAll('.toc a[href^="#"]')];
  const adapted = config?.dataset.readerAdapted !== undefined;
  const topics = links.map(link => ({link, label: link.textContent.trim(), section: document.getElementById(link.hash.slice(1))})).filter(topic => topic.section?.matches('section.card') && (!adapted || topic.section.dataset.readerChapter !== undefined));
  if (!nav || !config || !content || !sidebar || !toc || !topics.length) return;
  const pageTitle = config.dataset.readerTitle;
  const unit = config.dataset.readerUnit === 'section' ? 'section' : 'chapter';
  const plural = unit + 's';
  const unitTitle = unit[0].toUpperCase() + unit.slice(1);
  const pluralTitle = unitTitle + 's';
  nav.querySelector('.reader-title strong').textContent = pageTitle;
  nav.setAttribute('aria-label', pageTitle + ' ' + unit + ' reader');
  const menuButton = nav.querySelector('[data-reader-drawer]');
  menuButton?.setAttribute('aria-label', 'Open ' + plural);
  nav.querySelector('.reader-views')?.setAttribute('aria-label', unitTitle + ' layout');
  nav.querySelector('[data-reader-view-select]')?.setAttribute('aria-label', unitTitle + ' layout');
  function redirectMoved(target) {
    if (!target?.dataset.readerRedirect) return false;
    location.replace(target.href); return true;
  }
  if (redirectMoved(targetFromHash(location.hash))) return;
  const make = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const button = (cls, text, label) => {
    const node = make('button', cls, text);
    node.type = 'button';
    if (label) { node.setAttribute('aria-label', label); node.title = label; }
    return node;
  };
  const prev = nav.querySelector('[data-topic-prev]');
  const next = nav.querySelector('[data-topic-next]');
  const count = nav.querySelector('[data-topic-count]');
  const pagination = nav.querySelector('[data-reader-pagination]');
  const viewButtons = [...nav.querySelectorAll('[data-reader-view]')];
  const viewSelect = nav.querySelector('[data-reader-view-select]');
  const overview = document.querySelector('.topic-overview');
  const stage = make('div', 'topic-stage');
  stage.setAttribute('role', 'region');
  stage.setAttribute('aria-label', pageTitle + ' ' + plural);
  const strip = make('div', 'topic-strip');
  stage.appendChild(strip);
  topics[0].section.parentNode.insertBefore(stage, topics[0].section);
  let active = 0, activeColumn = 0, full = false, paired = false, pair = [0, Math.min(1, topics.length - 1)], pinned = null, routedHash = null;
  let drawerTab = 'chapters', drawerTrigger = null, drawerPinned = false;
  const drawerPreferenceKey = 'reader-nav-pin:' + location.pathname;
  // Wide screens open docked navigation until the reader closes it; phones start closed.
  drawerPinned = true;
  try { const saved = localStorage.getItem(drawerPreferenceKey); if (saved !== null) drawerPinned = saved === 'true'; } catch (_) {}
  const browserScrollMode = history.scrollRestoration;
  const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)');
  const kinds = [['math', 'Math'], ['experiment', 'Experiments'], ['code', 'Code'], ['dead-end', 'Alternatives']];
  const validKinds = new Set(kinds.map(([kind]) => kind));
  const preferenceKey = 'foldcolumns:' + location.pathname;
  let profiles = [new Set(), new Set()];
  try {
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(preferenceKey)); } catch (_) {}
    if (Array.isArray(saved) && saved.length === 2 && saved.every(Array.isArray)) profiles = saved.map(values => new Set(values.filter(kind => validKinds.has(kind))));
    else {
      const legacy = localStorage.getItem('foldmode:' + location.pathname);
      const initial = legacy === 'all' ? [...validKinds] : validKinds.has(legacy) ? [legacy] : [];
      profiles = [new Set(initial), new Set(initial)];
    }
  } catch (_) {}
  const generations = [0, 0], foldCache = [new Map(), new Map()], positions = new Map();
  topics.forEach((topic, index) => {
    const section = topic.section;
    // A slide face's title is not a heading; skip any heading inside one regardless.
    const heading = [...section.querySelectorAll('h2, h3')].find(node => !node.closest('[data-slide-face]'));
    const header = make('header', 'chapter-header');
    const identity = make('div', 'chapter-identity');
    const number = make('span', 'chapter-number', String(index + 1).padStart(2, '0'));
    identity.appendChild(number);
    // The toolbar carries a short label; the chapter keeps its full headline.
    identity.appendChild(make('span', 'chapter-label', topic.label));
    heading?.classList.add('chapter-headline');
    const tools = make('div', 'chapter-tools');
    const pin = button('chapter-pin', '', `Pin ${topic.label}`);
    const pinIcon = make('span', 'chapter-pin-icon', '⌖'); pinIcon.setAttribute('aria-hidden', 'true'); pin.appendChild(pinIcon);
    pin.appendChild(make('span', 'chapter-pin-label', 'Pinned'));
    pin.setAttribute('aria-pressed', 'false');
    tools.appendChild(pin);
    header.appendChild(identity); header.appendChild(tools);
    const layerRow = make('div', 'chapter-layers'); layerRow.setAttribute('role', 'group'); layerRow.setAttribute('aria-label', 'Reading layers');
    const story = button('chapter-layer chapter-layer-preset', 'Story', 'Story only'); story.dataset.readerPreset = 'story';
    story.addEventListener('click', () => setLayers(columnFor(index), new Set(), index)); layerRow.appendChild(story);
    const layerButtons = kinds.map(([kind, label]) => {
      const node = button('chapter-layer', label); node.dataset.readerLayer = kind;
      node.addEventListener('click', () => {
        const owner = columnFor(index), layers = new Set(profiles[owner]);
        if (layers.has(kind)) layers.delete(kind); else layers.add(kind);
        setLayers(owner, layers, index);
      });
      layerRow.appendChild(node); return node;
    });
    const all = button('chapter-layer chapter-layer-preset', 'All', 'Show all'); all.dataset.readerPreset = 'all';
    all.addEventListener('click', () => setLayers(columnFor(index), new Set(validKinds), index)); layerRow.appendChild(all);
    header.appendChild(layerRow);
    const body = make('div', 'chapter-body');
    [...section.childNodes].forEach(node => body.appendChild(node));
    section.appendChild(header); section.appendChild(body);
    section.classList.add('topic-card'); section.setAttribute('tabindex', '-1');
    if (heading?.id) section.setAttribute('aria-labelledby', heading.id);
    else section.setAttribute('aria-label', topic.label);
    strip.appendChild(section);
    Object.assign(topic, {header, body, layerRow, layerButtons, story, all, pin, folds: [...body.querySelectorAll('details.fold')], owner: null, generation: -1});
    // Legacy chapters without typed folds expose their complete story. Empty
    // layer switches would suggest controls that do not affect their content.
    layerRow.hidden = !topic.folds.length;
    topic.folds.forEach(fold => {
      const summary = fold.querySelector('summary'), tag = summary?.querySelector('.fold-tag');
      if (!summary || !tag) return;
      const title = summary.textContent.slice(tag.textContent.length).trim();
      tag.textContent = kinds.find(([kind]) => kind === fold.dataset.fold)?.[1] || fold.dataset.fold;
      const titleNode = make('span', 'fold-title', title);
      summary.replaceChildren(tag, titleNode);
      const panel = make('div', 'fold-content');
      [...fold.childNodes].filter(node => node !== summary).forEach(node => panel.appendChild(node));
      fold.appendChild(panel);
      panel.querySelectorAll('table').forEach(table => {
        let scroll = table.closest('.scroll');
        if (!scroll) { scroll = make('div', 'scroll fold-table'); table.parentNode.insertBefore(scroll, table); scroll.appendChild(table); }
        scroll.dataset.readerHorizontal = ''; scroll.setAttribute('tabindex', '0');
        scroll.setAttribute('role', 'region'); scroll.setAttribute('aria-label', title + ' data table');
      });
      panel.querySelectorAll('p').forEach(paragraph => {
        if (!/^\s*\$\$[\s\S]*\$\$\s*$/.test(paragraph.textContent) && !paragraph.querySelector('.katex-display')) return;
        paragraph.classList.add('fold-equation'); paragraph.dataset.readerHorizontal = '';
        paragraph.setAttribute('tabindex', '0'); paragraph.setAttribute('role', 'region'); paragraph.setAttribute('aria-label', 'Display equation');
      });
      panel.querySelectorAll('#width-sampling-comparison .case h3').forEach(heading => heading.setAttribute('aria-level', '5'));
    });
    body.querySelectorAll('p').forEach(paragraph => {
      if (!/^\s*\$\$[\s\S]*\$\$\s*$/.test(paragraph.textContent) && !paragraph.querySelector('.katex-display')) return;
      paragraph.classList.add('fold-equation'); paragraph.dataset.readerHorizontal = '';
      paragraph.setAttribute('tabindex', '0'); paragraph.setAttribute('role', 'region'); paragraph.setAttribute('aria-label', 'Display equation');
    });
    body.querySelectorAll('table').forEach(table => {
      let scroll = table.closest('.scroll');
      if (!scroll) { scroll = make('div', 'scroll'); table.parentNode.insertBefore(scroll, table); scroll.appendChild(table); }
      scroll.dataset.readerHorizontal = ''; scroll.setAttribute('tabindex', '0');
      scroll.setAttribute('role', 'region'); if (!scroll.getAttribute('aria-label')) scroll.setAttribute('aria-label', topic.label + ' data table');
    });
    positions.set(section.id, 0);
    function selectColumn() {
      if (!full && paired && pinned === null && pair.includes(index) && active !== index) {
        remember(); active = index; activeColumn = pair.indexOf(index); render(false); saveHistory(false);
      }
    }
    section.addEventListener('pointerdown', selectColumn);
    section.addEventListener('focusin', selectColumn);
    pin.addEventListener('click', () => {
      if (!paired || full) return;
      remember(); const side = pair.indexOf(index);
      if (side < 0) return;
      pinned = pinned === side ? null : side;
      activeColumn = pinned === null ? side : 1 - pinned;
      active = pair[activeColumn]; render(false); saveHistory(false); focusChapter();
    });
  });
  const peekButtons = [-1, 1].map(step => {
    const node = button(`topic-peek topic-peek-${step < 0 ? 'prev' : 'next'}`, '');
    node.addEventListener('pointerenter', () => { if (!full && !paired) topics[active + step]?.section.classList.add('topic-preview-hover'); });
    node.addEventListener('pointerleave', () => topics.forEach(topic => topic.section.classList.remove('topic-preview-hover')));
    node.addEventListener('focus', () => { if (!full && !paired) topics[active + step]?.section.classList.add('topic-preview-hover'); });
    node.addEventListener('blur', () => topics.forEach(topic => topic.section.classList.remove('topic-preview-hover')));
    node.addEventListener('click', () => move(step)); stage.appendChild(node); return node;
  });
  const layout = content.parentElement;
  // One navigation tree: site groups and pages, with this page's chapters
  // nested under its own entry. The top-bar menu button is the only toggle.
  const railButtons = [];
  const drawerHead = make('div', 'reader-drawer-head');
  const home = make('a', 'reader-home'); home.href = 'index.html';
  home.appendChild(make('span', 'reader-home-mark', '∿')); home.appendChild(make('span', '', document.body.dataset.siteHomeLabel || 'Documentation'));
  drawerHead.appendChild(home);
  const drawerTools = make('div', 'reader-drawer-tools'); drawerHead.appendChild(drawerTools);
  const pinDrawerButton = button('reader-drawer-pin', '⌖ Pin', 'Pin navigation');
  pinDrawerButton.addEventListener('click', () => {
    drawerPinned = !drawerPinned; persistDrawerPin(); syncDrawer();
    window.dispatchEvent(new Event('resize'));
  });
  // One control: hiding the sidebar is remembered; the menu button brings it back.
  const closeDrawerButton = button('reader-icon reader-drawer-close', '«', 'Hide navigation');
  closeDrawerButton.addEventListener('click', () => closeDrawer()); drawerTools.appendChild(closeDrawerButton);
  const chapterList = make('div', 'reader-chapter-list'); chapterList.id = 'reader-chapter-list';
  chapterList.setAttribute('aria-label', pluralTitle + ' of this page');
  const jumpUnit = config.dataset.readerUnit === 'section' ? 'section' : 'chapter';
  // Chapters take their page's group colour; only pages with their own chapter
  // groups give each group a track colour (data-part cycles a palette).
  const chapterGroups = topics.some(topic => topic.section.dataset.readerGroup);
  let part = -1;
  topics.forEach((topic, index) => {
    const group = topic.section.dataset.readerGroup;
    if (group) { part += 1; const label = make('span', 'reader-nav-group', group); label.dataset.part = String(part % 5); chapterList.appendChild(label); }
    if (chapterGroups) topic.link.dataset.part = String(Math.max(part, 0) % 5);
    topic.link.dataset.chapterNumber = String(index + 1).padStart(2, '0'); chapterList.appendChild(topic.link);
    const shortcuts = links.filter(link => !topics.some(candidate => candidate.link === link)
      && topic.section.contains(document.getElementById(link.hash.slice(1))));
    if (!shortcuts.length) return;
    const jumpGroup = make('details', 'reader-chapter-jumps');
    jumpGroup.dataset.readerShortcutsFor = topic.section.id;
    jumpGroup.setAttribute('aria-label', 'Jump within ' + topic.label);
    jumpGroup.appendChild(make('summary', '', 'Jump within this ' + jumpUnit));
    const destinations = make('div', 'reader-jump-links'); jumpGroup.appendChild(destinations);
    shortcuts.forEach(link => {
      const label = link.textContent.trim();
      const target = document.getElementById(link.hash.slice(1));
      const foldKind = target.closest('details.fold')?.dataset.fold;
      const kind = kinds.find(([key]) => key === foldKind)?.[1];
      link.classList.add('reader-chapter-sub'); link.textContent = '';
      link.appendChild(make('span', 'reader-jump-title', label));
      if (kind) { link.dataset.readerJumpKind = foldKind; link.appendChild(make('span', 'reader-jump-kind', kind)); }
      const purpose = `Jump to ${label} in ${topic.label}` + (kind ? `; opens ${kind} details` : '');
      link.setAttribute('aria-label', purpose); link.title = purpose;
      destinations.appendChild(link);
    });
    topic.jumps = {group:jumpGroup, links:shortcuts}; chapterList.appendChild(jumpGroup);
  });
  const currentPage = toc.querySelector('a.xpage.current');
  if (currentPage) { currentPage.after(chapterList); if (currentPage.dataset.group) chapterList.dataset.group = currentPage.dataset.group; }
  else toc.prepend(chapterList);
  const progressRow = make('div', 'reader-progress-row'); progressRow.setAttribute('aria-hidden', 'true');
  const progress = make('div', 'reader-progress'); const progressBar = make('i'); progress.appendChild(progressBar);
  const progressCount = make('span', 'reader-progress-count');
  progressRow.appendChild(progress); progressRow.appendChild(progressCount);
  sidebar.insertBefore(drawerHead, toc); sidebar.insertBefore(progressRow, toc);
  sidebar.setAttribute('aria-label', 'Documentation drawer'); sidebar.inert = true;
  const backdrop = document.getElementById('backdrop');
  backdrop?.addEventListener('click', () => closeDrawer());
  nav.querySelector('[data-reader-drawer]')?.addEventListener('click', event => toggleDrawer('chapters', event.currentTarget));
  function setDrawerTab(tab) { drawerTab = tab; }
  function toggleDrawer(tab, trigger) {
    if (document.body.classList.contains('reader-nav-open')) { closeDrawer(); return; }
    setDrawerTab(tab); drawerTrigger = trigger;
    if (window.innerWidth > 900 && !drawerPinned) { drawerPinned = true; persistDrawerPin(); }
    document.body.classList.add('reader-nav-open'); syncDrawer(); followActiveLink();
    window.dispatchEvent(new Event('resize'));
    closeDrawerButton.focus({preventScroll:true});
  }
  function drawerDocked() { return drawerPinned && document.body.classList.contains('reader-nav-open') && window.innerWidth > 900; }
  function persistDrawerPin() { try { localStorage.setItem(drawerPreferenceKey, String(drawerPinned)); } catch (_) {} }
  function syncDrawer() {
    const open = document.body.classList.contains('reader-nav-open'), docked = drawerDocked();
    document.body.classList.toggle('reader-nav-docked', docked);
    sidebar.inert = !open; content.inert = open && !docked;
    sidebar.setAttribute('role', open && !docked ? 'dialog' : 'navigation');
    if (open && !docked) sidebar.setAttribute('aria-modal', 'true'); else sidebar.removeAttribute('aria-modal');
    pinDrawerButton.setAttribute('aria-pressed', String(drawerPinned));
    pinDrawerButton.textContent = drawerPinned ? '⌖ Pinned' : '⌖ Pin';
    pinDrawerButton.title = drawerPinned ? 'Unpin navigation' : 'Pin navigation · docks on wide screens';
    pinDrawerButton.setAttribute('aria-label', pinDrawerButton.title);
    [...railButtons, ...nav.querySelectorAll('[data-reader-drawer]')].forEach(node => node.setAttribute('aria-expanded', String(open)));
  }
  function closeDrawer(returnFocus = true, clearPin = true) {
    document.body.classList.remove('reader-nav-open');
    if (clearPin) { drawerPinned = false; persistDrawerPin(); }
    syncDrawer(); window.dispatchEvent(new Event('resize'));
    if (returnFocus && drawerTrigger) drawerTrigger.focus({preventScroll:true});
  }
  setDrawerTab('chapters');
  function createDialog(cls, title) {
    const dialog = make('dialog', 'reader-dialog ' + cls); dialog.setAttribute('aria-label', title);
    const head = make('div', 'reader-dialog-head'); head.appendChild(make('strong', '', title));
    const close = button('reader-icon', '×', 'Close ' + title.toLowerCase()); close.addEventListener('click', () => dismissDialog(dialog));
    head.appendChild(close); dialog.appendChild(head); document.body.appendChild(dialog);
    dialog.addEventListener('cancel', event => { event.preventDefault(); dismissDialog(dialog); });
    dialog.addEventListener('click', event => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dismissDialog(dialog);
    });
    return dialog;
  }
  const about = createDialog('reader-about', 'About this page');
  if (overview) { overview.open = true; about.appendChild(overview); }
  const help = createDialog('reader-help', 'Using the reader');
  const helpItems = [
    ['Move through chapters', 'Use the arrows or the left and right arrow keys. Each chapter resumes where you left it. Controls inside figures keep their own keys.'],
    ['Compare two chapters', 'Two chapters shows two equal columns. Arrows move both until you pin one. Select an unpinned column before choosing its chapter from the navigation drawer.'],
    ['Choose how much to read', 'Story is always visible. The layer buttons under each chapter heading combine Math, Experiments, Code and Alternatives independently for each column. On narrow columns, scroll the row sideways. You can still open individual folds.'],
    ['Hold a reference', 'Pin the button on a column header to hold that chapter while the other moves. Purple marks the pinned column; its own scrolling and layer buttons still work.'],
    ['Keep navigation handy', 'On wide screens the navigation docks beside the page. Hide it with « and bring it back with ☰; each page remembers the choice. Reading stays interactive and chapter links keep the sidebar open. On narrow screens, navigation opens over the page and closes after choosing a chapter.']
  ];
  const readerWords = text => text.replace(/chapters/g, plural).replace(/chapter/g, unit);
  helpItems.forEach(([title, text]) => { const card = make('div', 'reader-help-card'); card.appendChild(make('h4', '', readerWords(title))); card.appendChild(make('p', '', readerWords(text))); help.appendChild(card); });
  const aboutHelp = button('reader-text-button', 'Reader help and shortcuts'); aboutHelp.addEventListener('click', () => { dismissDialog(about, false); showDialog(help, nav.querySelector('[data-reader-about]')); }); about.appendChild(aboutHelp);
  let dialogTrigger = null;
  function showDialog(dialog, trigger) {
    if (!drawerDocked()) closeDrawer(false, false); dialogTrigger = trigger; dialog.showModal();
  }
  function dismissDialog(dialog, returnFocus = true) {
    dialog.close(); if (returnFocus && dialogTrigger?.isConnected) dialogTrigger.focus({preventScroll:true});
  }
  nav.querySelector('[data-reader-about]').addEventListener('click', event => showDialog(about, event.currentTarget));
  nav.querySelector('[data-reader-help]').addEventListener('click', event => showDialog(help, event.currentTarget));
  function columnFor(index) { return !full && paired ? Math.max(0, pair.indexOf(index)) : activeColumn; }
  function shownIndices() { return full ? topics.map((_, index) => index) : paired ? pair : [active]; }
  function cacheFolds(topic) {
    if (topic.owner === null) return;
    foldCache[topic.owner].set(topic.section.id, {generation: topic.generation, states: topic.folds.map(fold => fold.open)});
  }
  function assignFolds(topic, owner) {
    if (topic.owner === owner && topic.generation === generations[owner]) return;
    cacheFolds(topic);
    const saved = foldCache[owner].get(topic.section.id);
    topic.folds.forEach((fold, index) => { fold.open = saved?.generation === generations[owner] ? saved.states[index] : profiles[owner].has(fold.dataset.fold); });
    topic.owner = owner; topic.generation = generations[owner];
  }
  function remember() {
    shownIndices().forEach(index => { const topic = topics[index]; if (!full) positions.set(topic.section.id, topic.body.scrollTop); cacheFolds(topic); });
  }
  function restore() { topics.forEach(topic => { topic.body.scrollTop = positions.get(topic.section.id) || 0; }); }
  function captureAnchor(topic, layers) {
    const rect = topic.body.getBoundingClientRect();
    const top = full ? nav.getBoundingClientRect().bottom + topic.header.getBoundingClientRect().height + 12 : rect.top + 12;
    // Keep the visible paragraph anchored as the selected folds change.
    let node = [...topic.body.querySelectorAll('p, h4, h3, summary, .math, .owns, table, svg.inline-fig')].find(candidate => {
      const box = candidate.getBoundingClientRect();
      return box.height > 0 && box.bottom > top && box.top < Math.min(rect.bottom, window.innerHeight);
    });
    if (!node) return null;
    let offset = node.getBoundingClientRect().top - top;
    let fold = node.closest('details.fold');
    while (fold && topic.body.contains(fold)) {
      if (!layers.has(fold.dataset.fold)) { node = fold.querySelector('summary') || node; offset = Math.max(0, offset); }
      fold = fold.parentElement?.closest('details.fold');
    }
    return {node, offset, top};
  }
  function setLayers(owner, layers, index) {
    const anchor = captureAnchor(topics[index], layers);
    remember(); profiles[owner] = layers; generations[owner]++;
    shownIndices().filter(i => columnFor(i) === owner).forEach(i => assignFolds(topics[i], owner));
    function restoreAnchor() {
      if (!anchor?.node.isConnected) return;
      const delta = anchor.node.getBoundingClientRect().top - anchor.top - anchor.offset;
      if (full) window.scrollBy({top:delta, behavior:'instant'}); else topics[index].body.scrollTop += delta;
    }
    restoreAnchor();
    const generation = generations[owner], wasFull = full, scroll = full ? window.scrollY : topics[index].body.scrollTop;
    // Responsive figures may finish their reflow on the next frame. Do not
    // overwrite a newer layer change, navigation or deliberate reader scroll.
    requestAnimationFrame(() => {
      if (generations[owner] !== generation || full !== wasFull || !shownIndices().includes(index) || columnFor(index) !== owner) return;
      if ((full ? window.scrollY : topics[index].body.scrollTop) !== scroll) return;
      restoreAnchor(); remember();
    });
    try { localStorage.setItem(preferenceKey, JSON.stringify(profiles.map(profile => [...profile]))); } catch (_) {}
    updateReadingButtons();
    remember();
  }
  function updateReadingButtons() {
    topics.forEach((topic, index) => {
      const owner = columnFor(index), profile = profiles[owner];
      const side = paired && !full ? owner ? 'Right' : 'Left' : 'Active';
      topic.layerRow.setAttribute('aria-label', `${side} column reading layers; Story always stays visible`);
      topic.layerButtons.forEach(node => {
        const on = profile.has(node.dataset.readerLayer), label = kinds.find(([kind]) => kind === node.dataset.readerLayer)[1];
        node.setAttribute('aria-pressed', String(on));
        node.setAttribute('aria-label', `${on ? 'Hide' : 'Show'} ${label.toLowerCase()} in the ${side.toLowerCase()} column`);
        node.title = node.getAttribute('aria-label');
      });
      topic.story.setAttribute('aria-pressed', String(profile.size === 0));
      topic.all.setAttribute('aria-pressed', String(profile.size === validKinds.size));
    });
  }
  function targetFromHash(hash) { try {
    const id = decodeURIComponent(hash.slice(1));
    return id === 'top' ? topics[0]?.section : document.getElementById(id);
  } catch (_) { return null; } }
  function topicOf(target) { return topics.findIndex(topic => topic.section === target || topic.section.contains(target)); }
  function saveHistory(push, hash = location.hash) {
    const state = {...history.state, chapterReader: {active, activeColumn, full, paired, pair:[...pair], pinned}};
    if (push && hash !== location.hash) history.pushState(state, '', hash); else history.replaceState(state, '', hash || location.href);
    routedHash = location.hash;
    syncJumpSelection();
  }
  function syncJumpSelection() {
    const target = targetFromHash(location.hash);
    topics.forEach(topic => topic.jumps?.links.forEach(link => {
      const selected = target?.id === link.hash.slice(1);
      link.classList.toggle('reader-jump-current', selected);
      if (selected) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    }));
  }
  function historyView() {
    const state = (history.state?.chapterReader || history.state?.roadReview);
    if (!state || !Number.isInteger(state.active) || state.active < 0 || state.active >= topics.length) return;
    if (!Array.isArray(state.pair) || state.pair.length !== 2 || new Set(state.pair).size !== Math.min(2, topics.length) || !state.pair.every(i => Number.isInteger(i) && i >= 0 && i < topics.length)) return;
    if (![null, 0, 1].includes(state.pinned)) return;
    remember(); active = state.active; full = state.full === true; paired = state.paired === true; pair = [...state.pair]; pinned = state.pinned;
    activeColumn = [0, 1].includes(state.activeColumn) ? state.activeColumn : paired ? Math.max(0, pair.indexOf(active)) : 0;
    return true;
  }
  function navigation(step) {
    if (!full && paired) {
      const updated = [...pair];
      for (const side of pinned === null ? [0, 1] : [1 - pinned]) { updated[side] += step; if (pinned !== null && updated[side] === pair[pinned]) updated[side] += step; }
      return updated.every(i => i >= 0 && i < topics.length) ? updated : null;
    }
    const index = active + step; return index >= 0 && index < topics.length ? index : null;
  }
  function setOffset() { content.style.setProperty('--topic-scroll-offset', (nav.getBoundingClientRect().height + 12) + 'px'); }
  function align(animate = true) {
    if (full) return;
    strip.classList.toggle('topic-animate', animate && !reducedMotion?.matches);
    if (paired) {
      strip.style.transform = 'translate3d(0px,0,0)';
      const width = topics[pair[0]].section.offsetWidth;
      const gap = parseFloat(window.getComputedStyle(stage).getPropertyValue('--topic-gap')) || 20;
      const anchor = pair[pinned === 0 ? 1 : 0];
      topics.forEach((topic, i) => { const side = pair.indexOf(i); const x = side >= 0 ? side * (width + gap) : i < anchor ? -(anchor - i) * (width + gap) : stage.clientWidth + (i - anchor - 1) * (width + gap); topic.section.style.transform = `translate3d(${x}px,0,0)`; });
    } else {
      topics.forEach(topic => { topic.section.style.transform = ''; });
      const section = topics[active].section;
      strip.style.transform = `translate3d(${(stage.clientWidth - section.offsetWidth) / 2 - section.offsetLeft}px,0,0)`;
    }
  }
  function render(animate = true) {
    content.dataset.topicLayout = full ? 'full' : 'deck'; content.dataset.topicView = paired ? 'pair' : 'single';
    document.body.classList.toggle('topic-deck', !full);
    if ('scrollRestoration' in history) history.scrollRestoration = full ? browserScrollMode : 'manual';
    topics.forEach((topic, i) => {
      topic.section.classList.remove('topic-preview-hover');
      const shown = full || (paired ? pair.includes(i) : i === active);
      if (shown) assignFolds(topic, columnFor(i));
      topic.section.inert = !shown;
      topic.section.classList.toggle('topic-active', i === active);
      topic.section.classList.toggle('topic-visible', shown);
      const held = !full && paired && pinned !== null && pair[pinned] === i;
      topic.section.classList.toggle('topic-pinned', held);
      topic.link.classList.toggle('active', !full && paired ? shown : i === active);
      if (topic.jumps) topic.jumps.group.open = shown;
      if (i === active) { topic.link.setAttribute('aria-current', full ? 'location' : 'step'); topic.link.classList.add('visited'); } else topic.link.removeAttribute('aria-current');
      topic.pin.hidden = !paired || full;
      topic.link.classList.toggle('reader-link-pinned', held);
      topic.pin.title = `${held ? 'Unpin' : 'Pin'} ${columnFor(i) ? 'right' : 'left'}: ${topic.label}`;
      topic.pin.setAttribute('aria-label', topic.pin.title); topic.pin.setAttribute('aria-pressed', String(held));
    });
    syncJumpSelection(); followActiveLink();
    progressBar.style.transform = `scaleX(${(active + 1) / topics.length})`;
    progressCount.textContent = `${String(active + 1).padStart(2, '0')} / ${String(topics.length).padStart(2, '0')}`;
    prev.disabled = navigation(-1) === null; next.disabled = navigation(1) === null;
    prev.setAttribute('aria-label', prev.disabled ? 'Start of ' + plural : paired && !full ? 'Previous ' + unit + ' in the unpinned columns' : `Previous ${unit}: ${topics[active - 1].label}`);
    next.setAttribute('aria-label', next.disabled ? 'End of ' + plural : paired && !full ? 'Next ' + unit + ' in the unpinned columns' : `Next ${unit}: ${topics[active + 1].label}`);
    pagination.hidden = !paired && !full;
    peekButtons.forEach((node, i) => { const peer = i ? next : prev; node.hidden = peer.disabled || full || paired; node.setAttribute('aria-label', peer.getAttribute('aria-label')); node.title = peer.getAttribute('aria-label'); });
    count.textContent = !full && paired ? `${pluralTitle} ${pair[0] + 1} and ${pair[1] + 1} of ${topics.length}${pinned === null ? '' : '; ' + (pinned ? 'right' : 'left') + ' pinned'}` : `${unitTitle} ${active + 1} of ${topics.length}`;
    const view = full ? 'full' : paired ? 'pair' : 'single';
    viewButtons.forEach(node => { node.setAttribute('aria-pressed', String(node.dataset.readerView === view)); node.disabled = node.dataset.readerView === 'pair' && topics.length < 2; }); viewSelect.value = view;
    const pairOption = viewSelect.querySelector('option[value="pair"]'); if (pairOption) pairOption.disabled = topics.length < 2;
    updateReadingButtons(); setOffset(); align(animate);
  }
  // Keyboard, button and scroll navigation move the active chapter; keep its
  // drawer link (with its group heading when it opens a group) in view.
  function followActiveLink() {
    const link = topics[active]?.link; if (!link || chapterList.hidden || !link.getClientRects().length) return;
    let box = link.parentElement; while (box && !(box.scrollHeight > box.clientHeight && /auto|scroll/.test(getComputedStyle(box).overflowY))) box = box.parentElement;
    if (!box) return;
    const heading = link.previousElementSibling?.classList.contains('reader-nav-group') ? link.previousElementSibling : link;
    const view = box.getBoundingClientRect(), margin = 48;
    const top = heading.getBoundingClientRect().top - view.top, bottom = link.getBoundingClientRect().bottom - view.top;
    if (top < margin) box.scrollTop += top - margin;
    else if (bottom > box.clientHeight - margin) box.scrollTop += bottom - box.clientHeight + margin;
  }
  function reveal(target) { let fold = target.closest('details.fold'); while (fold) { fold.open = true; fold = fold.parentElement?.closest('details.fold'); } }
  function scrollToTarget(target) {
    if (full || target === content) {
      const index = topicOf(target), headerHeight = index >= 0 && target !== topics[index].section ? topics[index].header.getBoundingClientRect().height : 0;
      target.style.scrollMarginTop = (nav.getBoundingClientRect().height + headerHeight + 12) + 'px';
      target.scrollIntoView({block:'start', behavior:'instant'}); return;
    }
    const topic = topics[topicOf(target)];
    if (target === topic.section) topic.body.scrollTop = positions.get(topic.section.id) || 0;
    else topic.body.scrollTop += target.getBoundingClientRect().top - topic.body.getBoundingClientRect().top - 12;
    positions.set(topic.section.id, topic.body.scrollTop);
  }
  function focusChapter(index = active) { topics[index].section.focus({preventScroll:true}); }
  function visit(target, writeHash = false, focus = false, animate = true) {
    const index = topicOf(target); if (index < 0 && target !== content) return false;
    remember(); const chosen = index < 0 ? 0 : index;
    if (!full && paired) {
      if (pair.includes(chosen)) { activeColumn = pinned !== null ? 1 - pinned : pair.indexOf(chosen); active = pair[activeColumn]; }
      else { activeColumn = pinned !== null ? 1 - pinned : activeColumn; pair[activeColumn] = chosen; active = chosen; }
    } else active = chosen;
    render(animate); reveal(target);
    if (writeHash) saveHistory(true, '#' + encodeURIComponent(target.id));
    if (focus) focusChapter(chosen);
    scrollToTarget(target); return true;
  }
  function move(step) {
    const target = navigation(step); if (target === null) return;
    if (Array.isArray(target)) { remember(); pair = target; if (pinned !== null) activeColumn = 1 - pinned; active = pair[activeColumn]; render(); restore(); saveHistory(true, '#' + topics[active].section.id); focusChapter(); }
    else visit(topics[target].section, true, true);
  }
  function selectView(view) {
    if (topics.length < 2 && view === 'pair') view = 'single';
    const wasFull = full; remember();
    if (view === 'full') full = true;
    else {
      full = false;
      if (view === 'pair' && !paired) {
        if (activeColumn === 1) { const right = Math.max(1, active); pair = [right - 1, right]; }
        else { const left = Math.min(active, topics.length - 2); pair = [left, left + 1]; }
        active = pair[activeColumn]; pinned = null;
      } else if (view === 'single') pinned = null;
      paired = view === 'pair';
      if (paired && wasFull) {
        if (pinned !== null && active === pair[pinned]) activeColumn = pinned;
        else {
          activeColumn = pinned === null ? activeColumn : 1 - pinned;
          if (active === pair[1 - activeColumn]) pair[1 - activeColumn] = active > 0 ? active - 1 : active + 1;
          pair[activeColumn] = active;
        }
      }
      if (paired && !pair.includes(active)) active = pair[pinned === null ? activeColumn : 1 - pinned];
    }
    render(false); if (!full) { restore(); window.scrollTo({top:0, behavior:'instant'}); }
    else if (!wasFull) scrollToTarget(topics[active].section);
    saveHistory(false); window.dispatchEvent(new Event('resize'));
    focusChapter();
  }
  prev.addEventListener('click', () => move(-1)); next.addEventListener('click', () => move(1));
  viewButtons.forEach(node => node.addEventListener('click', () => selectView(node.dataset.readerView)));
  viewSelect.addEventListener('change', () => selectView(viewSelect.value));
  document.addEventListener('keydown', event => {
    if (about.open || help.open) return;
    if (event.key === 'Escape' && document.body.classList.contains('reader-nav-open')) { event.preventDefault(); closeDrawer(); return; }
    if (document.body.classList.contains('reader-nav-open') && !drawerDocked() && event.key === 'Tab') {
      const nodes = [...sidebar.querySelectorAll('button, a[href], summary')].filter(node => !node.closest('[hidden]') && node.tabIndex !== -1 && node.getClientRects().length > 0);
      const first = nodes[0], last = nodes[nodes.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus({preventScroll:true}); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus({preventScroll:true}); }
      return;
    }
    if (full || event.defaultPrevented || event.repeat || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    if (about.open || help.open || document.querySelector('.lb-overlay') || document.body.classList.contains('reader-nav-open') && !drawerDocked()) return;
    if (event.target?.closest('input, select, textarea, button, a, summary, svg, canvas, video, audio, iframe, [data-reader-horizontal], [contenteditable]:not([contenteditable="false"]), [role="tab"], [role="tablist"], [role="slider"], [role="spinbutton"], [role="textbox"]')) return;
    event.preventDefault(); move(event.key === 'ArrowRight' ? 1 : -1);
  });
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const link = event.target?.closest('a[href]'); if (!link || link.target || link.hasAttribute('download')) return;
    const url = new URL(link.href, location.href);
    if (sidebar.contains(link) && !drawerDocked()) closeDrawer(false, false);
    if (url.origin !== location.origin || url.pathname !== location.pathname || url.search !== location.search || !url.hash) return;
    const target = targetFromHash(url.hash); if (!target || (topicOf(target) < 0 && target !== content)) return;
    event.preventDefault(); visit(target, true, true);
  });
  function route(fromHistory = false) {
    if (!fromHistory && routedHash === location.hash) return;
    const restored = fromHistory && historyView();
    const target = targetFromHash(location.hash) || (!location.hash ? content : null);
    if (redirectMoved(target)) return;
    if (restored) {
      render(false); restore();
      // Clicking a column changes the active side without changing the URL.
      // Its history snapshot takes precedence over that older fragment.
      const destination = full && topicOf(target) !== active ? topics[active].section : target;
      const shown = destination && (destination === content || shownIndices().includes(topicOf(destination)));
      if (shown) reveal(destination);
      const hash = location.hash; routedHash = hash;
      requestAnimationFrame(() => { if (location.hash === hash) { restore(); if (shown) scrollToTarget(destination); } });
      return;
    }
    if (target && visit(target)) { const hash = location.hash; routedHash = hash; requestAnimationFrame(() => { if (location.hash === hash) scrollToTarget(target); }); }
  }
  window.addEventListener('hashchange', () => route()); window.addEventListener('popstate', () => route(true));
  window.addEventListener('resize', () => { syncDrawer(); setOffset(); align(false); });
  window.addEventListener('scroll', () => {
    if (!full) return;
    const line = nav.getBoundingClientRect().height + 80; let index = 0;
    topics.forEach((topic, i) => { if (topic.section.getBoundingClientRect().top <= line) index = i; });
    if (index !== active) { active = index; render(false); }
  }, {passive:true});
  let printFoldStates = null;
  window.addEventListener('beforeprint', () => {
    remember(); printFoldStates = topics.map(topic => topic.folds.map(fold => fold.open));
    topics.forEach(topic => topic.folds.forEach(fold => { fold.open = true; }));
    if (overview) { overview.open = true; content.insertBefore(overview, nav); }
  });
  window.addEventListener('afterprint', () => {
    if (printFoldStates) topics.forEach((topic, index) => topic.folds.forEach((fold, i) => { fold.open = printFoldStates[index][i]; }));
    printFoldStates = null;
    if (overview) about.insertBefore(overview, aboutHelp);
    requestAnimationFrame(() => { if (!full) restore(); align(false); });
  });
  document.body.classList.add('reader-enabled'); nav.hidden = false;
  if (drawerPinned && window.innerWidth > 900) document.body.classList.add('reader-nav-open');
  syncDrawer();
  const initial = targetFromHash(location.hash);
  if (!initial || !visit(initial, false, false, false)) render(false);
  routedHash = location.hash; saveHistory(false); window.scrollTo({top:0, behavior:'instant'}); window.dispatchEvent(new Event('resize'));
  if (initial && topicOf(initial) >= 0 && initial !== topics[active].section) requestAnimationFrame(() => { if (topicOf(initial) === active) { reveal(initial); scrollToTarget(initial); } });
});
