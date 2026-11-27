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
  // The bar keeps the menu button and the page name. The reading controls move
  // to the navigation (a row of icons under the site name) and the stepper to
  // the stage (an island at the bottom centre); both are moved, not cloned.
  const tools = nav.querySelector('.reader-tools');
  const viewNames = {single: 'One ' + unit, pair: 'Two ' + plural, full: 'All ' + plural, present: 'Presentation'};
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
  const island = nav.querySelector('[data-reader-pagination]');
  const place = island.querySelector('.reader-place');
  island.setAttribute('aria-label', unitTitle + ' stepper');
  const viewButtons = [...nav.querySelectorAll('[data-reader-view]')];
  viewButtons.forEach(node => { const name = viewNames[node.dataset.readerView]; node.setAttribute('aria-label', name); node.title = name; });
  // The icons are drawn at run time, so the built page holds no extra SVG figure.
  const toolIcon = paths => `<svg viewBox="0 0 20 20" width="19" height="19" aria-hidden="true" focusable="false">${paths}</svg>`;
  const toolDrawings = {
    single:'<rect x="5" y="3.5" width="10" height="13" rx="1.6"/>',
    pair:'<rect x="2.5" y="3.5" width="6.5" height="13" rx="1.4"/><rect x="11" y="3.5" width="6.5" height="13" rx="1.4"/>',
    full:'<rect x="4" y="2.5" width="12" height="4" rx="1.2"/><rect x="4" y="8" width="12" height="4" rx="1.2"/><rect x="4" y="13.5" width="12" height="4" rx="1.2"/>',
    present:'<path class="reader-tool-fill" d="M7 4.5v11l9-5.5z"/>',
    about:'<circle cx="10" cy="10" r="7.5"/><path d="M10 9v5M10 6.3v.2"/>',
    help:'<circle cx="10" cy="10" r="7.5"/><path d="M7.9 7.9a2.2 2.2 0 1 1 3 2c-.6.3-.9.8-.9 1.4v.3M10 14.1v.2"/>',
  };
  viewButtons.forEach(node => { node.innerHTML = toolIcon(toolDrawings[node.dataset.readerView]); });
  tools.querySelector('[data-reader-about]').innerHTML = toolIcon(toolDrawings.about);
  tools.querySelector('[data-reader-help]').innerHTML = toolIcon(toolDrawings.help);
  // Presentation and the Slides switch exist only on pages with a slide face.
  const presentable = !!document.querySelector('[data-slide-face]');
  const slidesButton = nav.querySelector('[data-reader-slides]');
  const presentButton = nav.querySelector('[data-reader-view="present"]');
  if (presentButton) presentButton.hidden = !presentable;
  const overview = document.querySelector('.topic-overview');
  const stage = make('div', 'topic-stage');
  stage.setAttribute('role', 'region');
  stage.setAttribute('aria-label', pageTitle + ' ' + plural);
  const strip = make('div', 'topic-strip');
  stage.appendChild(strip);
  topics[0].section.parentNode.insertBefore(stage, topics[0].section);
  let active = 0, activeColumn = 0, full = false, paired = false, pair = [0, Math.min(1, topics.length - 1)], pinned = null, routedHash = null;
  // Presentation is a fourth view; presentReturn is the view it leaves to.
  let presenting = false, presentReturn = null;
  let drawerTab = 'chapters', drawerTrigger = null, drawerPinned = false;
  // One choice for the whole site: hiding the menu on one page hides it on the next.
  const drawerPreferenceKey = 'reader-nav-pin:' + (document.body.dataset.siteHomeLabel || '');
  // Wide screens open docked navigation until the reader closes it; phones start closed.
  drawerPinned = true;
  try { const saved = localStorage.getItem(drawerPreferenceKey); if (saved !== null) drawerPinned = saved === 'true'; } catch (_) {}
  const browserScrollMode = history.scrollRestoration;
  const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)');
  const kinds = [['math', 'Math'], ['experiment', 'Experiments'], ['code', 'Code'], ['dead-end', 'Alternatives']];
  const validKinds = new Set(kinds.map(([kind]) => kind));
  // One set of reading layers for the whole page, in every chapter and column.
  // A returning reader keeps what the first column had (foldcolumns) or the
  // single mode of the plain fold bar (foldmode).
  const layersKey = 'foldlayers:' + location.pathname;
  const readStored = key => { try { return JSON.parse(localStorage.getItem(key)); } catch (_) { return null; } };
  let layers = new Set();
  try {
    const saved = readStored(layersKey), columns = readStored('foldcolumns:' + location.pathname);
    if (Array.isArray(saved)) layers = new Set(saved.filter(kind => validKinds.has(kind)));
    else if (Array.isArray(columns) && Array.isArray(columns[0])) layers = new Set(columns[0].filter(kind => validKinds.has(kind)));
    else {
      const legacy = localStorage.getItem('foldmode:' + location.pathname);
      layers = new Set(legacy === 'all' ? [...validKinds] : validKinds.has(legacy) ? [legacy] : []);
    }
  } catch (_) {}
  // A reader's own click on a fold is saved for that fold and wins on the next
  // visit. Saved states are [key, open] pairs, the most recent last, bounded.
  const statesKey = 'foldstates:' + location.pathname, foldStateLimit = 200;
  let foldStates = new Map();
  try {
    const saved = readStored(statesKey);
    if (Array.isArray(saved)) foldStates = new Map(saved.filter(entry => Array.isArray(entry) && typeof entry[0] === 'string' && typeof entry[1] === 'boolean').slice(-foldStateLimit));
  } catch (_) {}
  const foldInfo = new Map(), foldKeyCount = new Map();
  let layerChanges = 0;
  // All chapters hides slide faces unless the reader turns them on for this page.
  const slidesKey = 'readerslides:' + location.pathname;
  let slidesShown = false;
  try { slidesShown = localStorage.getItem(slidesKey) === 'shown'; } catch (_) {}
  const positions = new Map();
  topics.forEach((topic, index) => {
    const section = topic.section;
    // A slide face's title is not a heading; skip any heading inside one regardless.
    // The chapter's own headline: a heading of the chapter itself, not one inside a slide
    // face, a fold, a figure, a tab panel or a card nested further in. A card that opens the
    // chapter (an adapted page keeps the author's card inside its chapter) is the chapter.
    const heading = [...section.querySelectorAll('h2, h3')].find(node => {
      for (let up = node.parentElement; up && up !== section; up = up.parentElement) {
        if (up.matches('[data-slide-face], details, aside, figure, [role="tabpanel"]')) return false;
        if (up.matches('section, article, .card') && !(up.parentElement === section && section.children[0] === up)) return false;
      }
      return true;
    });
    // Without a headline of its own the chapter keeps its strip, which names it, in One chapter.
    section.classList.toggle('topic-headless', !heading);
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
    const body = make('div', 'chapter-body');
    [...section.childNodes].forEach(node => body.appendChild(node));
    section.appendChild(header); section.appendChild(body);
    section.classList.add('topic-card'); section.setAttribute('tabindex', '-1');
    if (heading?.id) section.setAttribute('aria-labelledby', heading.id);
    else section.setAttribute('aria-label', topic.label);
    strip.appendChild(section);
    Object.assign(topic, {header, body, heading, pin, folds: [...body.querySelectorAll('details.fold')]});
    topic.folds.forEach(fold => {
      const summary = fold.querySelector('summary'), tag = summary?.querySelector('.fold-tag');
      const text = summary?.textContent || '', title = (tag ? text.slice(tag.textContent.length) : text).trim();
      // A fold is known by its chapter, kind and title; the author's open
      // attribute is its starting state when no option or click decides.
      const base = section.id + '|' + fold.dataset.fold + '|' + title, seen = (foldKeyCount.get(base) || 0) + 1;
      foldKeyCount.set(base, seen);
      foldInfo.set(fold, {key: seen > 1 ? base + '#' + seen : base, authored: fold.open === true});
      summary?.addEventListener('click', event => { if (!event.defaultPrevented) rememberFold(fold, !fold.open); });
      if (!summary || !tag) return;
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
  stage.appendChild(island);
  // A mostly sideways swipe of 70 px or more turns the chapter. A drag that
  // starts inside something that scrolls sideways itself is left to it.
  let swipeStart = null;
  const scrollsSideways = node => {
    for (let current = node; current && current !== stage; current = current.parentElement) {
      if (current.scrollWidth > current.clientWidth + 4 && /auto|scroll/.test(window.getComputedStyle(current).overflowX)) return true;
    }
    return false;
  };
  stage.addEventListener('touchstart', event => {
    const touch = event.touches[0];
    // Controls that own their keys (inputs, sliders, drawings, canvases) own their drags too,
    // and a pinch-zoomed page pans instead of turning.
    const owned = event.target?.closest?.(keyOwners) || scrollsSideways(event.target) || window.visualViewport?.scale > 1;
    swipeStart = event.touches.length === 1 && !full && !presenting && !owned ? {x:touch.clientX, y:touch.clientY} : null;
  }, {passive:true});
  stage.addEventListener('touchcancel', () => { swipeStart = null; }, {passive:true});
  stage.addEventListener('touchend', event => {
    if (!swipeStart) return;
    const touch = event.changedTouches[0], dx = touch.clientX - swipeStart.x, dy = touch.clientY - swipeStart.y;
    swipeStart = null;
    if (Math.abs(dx) >= 70 && Math.abs(dx) >= 1.5 * Math.abs(dy)) move(dx < 0 ? 1 : -1);
  }, {passive:true});
  const layout = content.parentElement;
  // One navigation tree: site groups and pages, with this page's chapters
  // nested under its own entry. The top-bar menu button is the only toggle.
  const railButtons = [];
  const drawerHead = make('div', 'reader-drawer-head');
  const home = make('a', 'reader-home'); home.href = 'index.html';
  // The drawer header repeats the sidebar brand: the project's mark and name.
  const brand = sidebar.querySelector('.brand');
  const brandMark = brand?.querySelector('.brand-mark');
  if (brandMark) home.appendChild(brandMark.cloneNode(true));
  home.appendChild(make('span', 'reader-home-name', brand?.querySelector('.brand-name')?.textContent || document.body.dataset.siteHomeLabel || 'Documentation'));
  drawerHead.appendChild(home);
  const drawerTools = make('div', 'reader-drawer-tools'); drawerHead.appendChild(drawerTools);
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
  const currentPage = toc.querySelector('a.xpage.current') || toc.querySelector('.repo-tree a[aria-current="page"]');
  if (currentPage) { currentPage.after(chapterList); if (currentPage.dataset.group) chapterList.dataset.group = currentPage.dataset.group; }
  else { const openWork = toc.querySelector(':scope > a.open-work'); if (openWork) openWork.after(chapterList); else toc.prepend(chapterList); }
  sidebar.insertBefore(drawerHead, toc);
  sidebar.insertBefore(tools, toc);
  sidebar.setAttribute('aria-label', 'Documentation drawer'); sidebar.inert = true;
  // "Also show": one set of options for the page, at the bottom of the
  // navigation. Only the kinds of fold the page has are offered; with nothing
  // switched on the reader is in the story. All is a switch over every kind.
  const presentKinds = kinds.filter(([kind]) => topics.some(topic => topic.folds.some(fold => fold.dataset.fold === kind)));
  const layerPanel = nav.querySelector('[data-reader-layers]');
  const allSwitch = layerPanel.querySelector('[data-reader-layer-all]');
  layerPanel.setAttribute('aria-label', 'Also show, in every ' + unit);
  const layerButtons = presentKinds.map(([kind, label]) => {
    const node = button('reader-layer', label); node.dataset.readerLayer = kind; node.setAttribute('aria-pressed', 'false');
    node.addEventListener('click', () => setLayers([kind], !layers.has(kind)));
    layerPanel.querySelector('.reader-layers-row').insertBefore(node, slidesButton); return node;
  });
  allSwitch.addEventListener('click', () => setLayers(presentKinds.map(([kind]) => kind), allSwitch.getAttribute('aria-checked') !== 'true'));
  allSwitch.hidden = !presentKinds.length;
  sidebar.appendChild(layerPanel);
  const kitLine = sidebar.querySelector('.kit-line'); if (kitLine) sidebar.appendChild(kitLine);
  topics.forEach(topic => topic.folds.forEach(resolveFold));
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
    // Presentation hides the navigation without changing its remembered state.
    sidebar.inert = !open || presenting; content.inert = open && !docked && !presenting;
    sidebar.setAttribute('role', open && !docked ? 'dialog' : 'navigation');
    if (open && !docked) sidebar.setAttribute('aria-modal', 'true'); else sidebar.removeAttribute('aria-modal');
    [...railButtons, ...nav.querySelectorAll('[data-reader-drawer]')].forEach(node => node.setAttribute('aria-expanded', String(open)));
  }
  function closeDrawer(returnFocus = true, clearPin = true) {
    document.body.classList.remove('reader-nav-open');
    if (clearPin) { drawerPinned = false; persistDrawerPin(); }
    syncDrawer(); window.dispatchEvent(new Event('resize'));
    if (returnFocus) (drawerTrigger || menuButton)?.focus({preventScroll:true});
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
    ['Move through chapters', 'Use the arrows on the stepper at the bottom of the page, click a neighbouring chapter at its edge, swipe sideways on a touch screen, or press the left and right arrow keys. Each chapter resumes where you left it. Controls inside figures keep their own keys.'],
    ['Choose the arrangement', 'The row of icons under the site name shows One chapter, Two chapters or All chapters' + (presentable ? ', starts the Presentation' : '') + ' and opens About this page and this help. On narrow screens the row is in the navigation menu.'],
    ['Compare two chapters', 'Two chapters shows two equal columns. The stepper and the arrow keys move both until you pin one. Select an unpinned column before choosing its chapter from the navigation.'],
    ['Choose how much to read', 'With nothing switched on you read the story. Also show, at the bottom of the navigation, opens Math, Experiments, Code or Alternatives in every chapter and both columns at once; All switches every kind on or off. A fold you open or close yourself keeps that state on your next visit, until you choose its kind again.'],
    ['Hold a reference', 'Pin the button on a column header to hold that chapter while the other moves. Purple marks the pinned column; its own scrolling still works.'],
    ['Keep navigation handy', 'On wide screens the navigation docks beside the page. Hide it with « and bring it back with ☰ at the top of the page; the choice holds across the site. Reading stays interactive and chapter links keep the navigation open. On narrow screens, navigation opens over the page and closes after choosing a chapter or an arrangement.']
  ];
  if (presentable) helpItems.push(['Present the slides', 'Presentation shows each chapter\'s slide across the window, starting at the current chapter. Left and right arrows or Page Up and Page Down change chapter, Home and End go to the first and last. Scroll, or use the up and down arrows and Space, to read the full chapter below its slide. F switches fullscreen; Escape leaves. All chapters hides the slides until you switch on Slides under Also show.']);
  const readerWords = text => text.replace(/chapters/g, plural).replace(/chapter/g, unit);
  helpItems.forEach(([title, text]) => { const card = make('div', 'reader-help-card'); card.appendChild(make('h4', '', readerWords(title))); card.appendChild(make('p', '', readerWords(text))); help.appendChild(card); });
  const aboutHelp = button('reader-text-button', 'Reader help and shortcuts'); aboutHelp.addEventListener('click', () => { dismissDialog(about, false); showDialog(help, tools.querySelector('[data-reader-about]')); }); about.appendChild(aboutHelp);
  let dialogTrigger = null;
  function showDialog(dialog, trigger) {
    if (!drawerDocked()) closeDrawer(false, false); dialogTrigger = trigger; dialog.showModal();
  }
  // A trigger inside the closed overlay navigation cannot take focus back; the
  // menu button that opens the navigation does.
  function dismissDialog(dialog, returnFocus = true) {
    dialog.close();
    if (returnFocus && dialogTrigger?.isConnected) (sidebar.contains(dialogTrigger) && sidebar.inert ? menuButton : dialogTrigger).focus({preventScroll:true});
  }
  tools.querySelector('[data-reader-about]').addEventListener('click', event => showDialog(about, event.currentTarget));
  tools.querySelector('[data-reader-help]').addEventListener('click', event => showDialog(help, event.currentTarget));
  function columnFor(index) { return !full && paired ? Math.max(0, pair.indexOf(index)) : activeColumn; }
  function shownIndices() { return full ? topics.map((_, index) => index) : paired ? pair : [active]; }
  // At load each fold takes the reader's saved state for it; otherwise it is open
  // when its kind is switched on or its author opened it. After that a fold keeps
  // its state while the page is open, however it was opened (a click, a deep or
  // jump link, find in page); only an option click changes it.
  function resolveFold(fold) {
    const info = foldInfo.get(fold), saved = foldStates.get(info.key);
    fold.open = saved !== undefined ? saved : layers.has(fold.dataset.fold) || info.authored;
  }
  function saveFoldStates() {
    while (foldStates.size > foldStateLimit) foldStates.delete(foldStates.keys().next().value);
    try { localStorage.setItem(statesKey, JSON.stringify([...foldStates])); } catch (_) {}
  }
  function rememberFold(fold, open) {
    const key = foldInfo.get(fold).key;
    foldStates.delete(key); foldStates.set(key, open); saveFoldStates();
  }
  function remember() {
    // Presentation always opens a chapter on its slide; it keeps no reading positions.
    if (!full && !presenting) shownIndices().forEach(index => { const topic = topics[index]; positions.set(topic.section.id, topic.body.scrollTop); });
  }
  function restore() {
    topics.forEach((topic, index) => {
      topic.body.scrollTop = presenting && index === active ? 0 : positions.get(topic.section.id) || 0;
      topic.section.classList.toggle('topic-scrolled', topic.body.scrollTop > 24);
    });
  }
  function captureAnchor(topic, opensAfter) {
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
      if (!opensAfter(fold)) { node = fold.querySelector('summary') || node; offset = Math.max(0, offset); }
      fold = fold.parentElement?.closest('details.fold');
    }
    return {node, offset, top};
  }
  // An option sets every fold of its kinds, in every chapter, and replaces the
  // saved states of those folds: only an author-open fold that the option
  // closes keeps a saved state, so the next visit shows it closed as well.
  function setLayers(changed, on) {
    const index = active, opensAfter = fold => changed.includes(fold.dataset.fold) ? on : fold.open;
    const anchor = captureAnchor(topics[index], opensAfter);
    remember();
    changed.forEach(kind => { if (on) layers.add(kind); else layers.delete(kind); });
    layerChanges += 1;
    topics.forEach(topic => topic.folds.forEach(fold => {
      if (!changed.includes(fold.dataset.fold)) return;
      const info = foldInfo.get(fold);
      fold.open = on; foldStates.delete(info.key);
      if (!on && info.authored) foldStates.set(info.key, false);
    }));
    function restoreAnchor() {
      if (!anchor?.node.isConnected) return;
      const delta = anchor.node.getBoundingClientRect().top - anchor.top - anchor.offset;
      if (full) window.scrollBy({top:delta, behavior:'instant'}); else topics[index].body.scrollTop += delta;
    }
    restoreAnchor();
    const change = layerChanges, wasFull = full, scroll = full ? window.scrollY : topics[index].body.scrollTop;
    // Responsive figures may finish their reflow on the next frame. Do not
    // overwrite a newer layer change, navigation or deliberate reader scroll.
    requestAnimationFrame(() => {
      if (layerChanges !== change || full !== wasFull || !shownIndices().includes(index)) return;
      if ((full ? window.scrollY : topics[index].body.scrollTop) !== scroll) return;
      restoreAnchor(); remember();
    });
    try { localStorage.setItem(layersKey, JSON.stringify([...layers])); } catch (_) {}
    saveFoldStates();
    syncLayerControls();
    remember();
  }
  function syncLayerControls() {
    const allOn = presentKinds.length > 0 && presentKinds.every(([kind]) => layers.has(kind));
    layerButtons.forEach(node => {
      const kind = node.dataset.readerLayer, on = layers.has(kind), label = kinds.find(([key]) => key === kind)[1];
      node.setAttribute('aria-pressed', String(on));
      node.title = `${on ? 'Hide' : 'Show'} ${label.toLowerCase()} in every ${unit}`;
    });
    allSwitch.setAttribute('aria-checked', String(allOn));
    allSwitch.title = `${allOn ? 'Close' : 'Open'} every fold in every ${unit}`;
  }
  function targetFromHash(hash) { try {
    const id = decodeURIComponent(hash.slice(1));
    return id === 'top' ? topics[0]?.section : document.getElementById(id);
  } catch (_) { return null; } }
  function topicOf(target) { return topics.findIndex(topic => topic.section === target || topic.section.contains(target)); }
  // Presentation is named in the address (?view=present), so a reload or a
  // shared link opens the same slide in the same view. Other views leave the
  // address as it was.
  function viewInAddress() { return new URL(location.href).searchParams.get('view') === 'present'; }
  function address(hash) {
    if (presenting === viewInAddress()) return hash || location.href;
    const url = new URL(location.href);
    if (presenting) url.searchParams.set('view', 'present'); else url.searchParams.delete('view');
    if (hash) url.hash = hash;
    return url.href;
  }
  function saveHistory(push, hash = location.hash) {
    const state = {...history.state, chapterReader: {active, activeColumn, full, paired, pair:[...pair], pinned, present:presenting, presentReturn}};
    if (push && hash !== location.hash) history.pushState(state, '', address(hash)); else history.replaceState(state, '', address(hash));
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
    presenting = presentable && state.present === true;
    if (presenting) { full = false; paired = false; pinned = null; activeColumn = 0; presentReturn = validReturn(state.presentReturn); }
    return true;
  }
  function validReturn(value) {
    if (!value || !['single', 'pair', 'full'].includes(value.view)) return {view:'single', pair:[...pair], pinned:null, activeColumn:0};
    const pairOk = Array.isArray(value.pair) && value.pair.length === 2 && value.pair.every(i => Number.isInteger(i) && i >= 0 && i < topics.length) && value.pair[0] !== value.pair[1];
    return {view:value.view, pair:pairOk ? [...value.pair] : [...pair], pinned:pairOk && [0, 1].includes(value.pinned) ? value.pinned : null, activeColumn:value.activeColumn === 1 ? 1 : 0};
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
  // A chapter that opens with a slide face shows the face alone in its first
  // view. `faceRoom` splits the height the face leaves in the chapter's window:
  // `lift` above the face and `drop` below it, so the face stands in the middle
  // of what the bottom controls leave free and the next line starts below the
  // fold. A face taller than the window gets no space; it scrolls.
  function faceRoom(view, top, height, dock) {
    const free = Math.ceil(view - top - height);
    if (!(free > 0)) return {lift: 0, drop: 0};
    const lift = Math.max(0, Math.floor((free - dock) / 2));
    return {lift, drop: free - lift};
  }
  const leadingFace = '.chapter-body > .slide-face:first-child, .chapter-body > :first-child > .slide-face:first-child';
  const fittedFaces = new Map();
  const faceWatch = typeof ResizeObserver === 'function' ? new ResizeObserver(() => fitFaces()) : null;
  function fitFaces() {
    topics.forEach(topic => {
      const face = topic.body.querySelector('[data-slide-face]');
      if (!face) return;
      if (faceWatch && !fittedFaces.has(face)) { faceWatch.observe(face); faceWatch.observe(topic.body); }
      const was = fittedFaces.get(face) || {lift: 0, drop: 0};
      let room = {lift: 0, drop: 0};
      // Only a face that opens the chapter, in the one-chapter view, is fitted:
      // the same faces the margin rule in slide-face.css names.
      if (!full && !paired && !presenting && topic.body.clientHeight > 0 && topic.section.offsetWidth > 0 && face.matches(leadingFace)) {
        // Neighbouring chapters are drawn smaller; measure in the chapter's own pixels.
        const scale = topic.section.getBoundingClientRect().width / topic.section.offsetWidth || 1;
        const top = (face.getBoundingClientRect().top - topic.body.getBoundingClientRect().top) / scale + topic.body.scrollTop - was.lift;
        const dock = parseFloat(window.getComputedStyle(topic.body).getPropertyValue('--reader-dock')) || 0;
        room = faceRoom(topic.body.clientHeight, top, face.offsetHeight, dock);
      }
      fittedFaces.set(face, room);
      if (room.lift === was.lift && room.drop === was.drop) return;
      face.style.setProperty('--reader-face-lift', room.lift + 'px');
      face.style.setProperty('--reader-face-drop', room.drop + 'px');
      face.toggleAttribute('data-reader-face-lifted', room.lift > 0);
      // A reader who is past the face keeps their line when the room changes.
      if (topic.body.scrollTop > 24) topic.body.scrollTop += room.lift + room.drop - was.lift - was.drop;
    });
  }
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
      // The previous/next targets cover exactly the visible sliver of each
      // neighbouring card, so their hover outline matches what the reader sees.
      const gap = parseFloat(window.getComputedStyle(stage).getPropertyValue('--topic-gap')) || 20;
      const sliver = Math.max(0, (stage.clientWidth - section.offsetWidth) / 2 - gap);
      peekButtons.forEach(node => { node.style.width = `${sliver}px`; node.style.display = sliver < 4 ? 'none' : ''; });
    }
  }
  function render(animate = true) {
    content.dataset.topicLayout = full ? 'full' : 'deck'; content.dataset.topicView = presenting ? 'present' : paired ? 'pair' : 'single';
    document.body.classList.toggle('topic-deck', !full);
    if (presentable) content.dataset.readerFaces = slidesShown ? 'shown' : 'hidden';
    if ('scrollRestoration' in history) history.scrollRestoration = full ? browserScrollMode : 'manual';
    topics.forEach((topic, i) => {
      topic.section.classList.remove('topic-preview-hover');
      const shown = full || (paired ? pair.includes(i) : i === active);
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
    prev.disabled = navigation(-1) === null; next.disabled = navigation(1) === null;
    prev.setAttribute('aria-label', prev.disabled ? 'Start of ' + plural : paired && !full ? 'Previous ' + unit + ' in the unpinned columns' : `Previous ${unit}: ${topics[active - 1].label}`);
    next.setAttribute('aria-label', next.disabled ? 'End of ' + plural : paired && !full ? 'Next ' + unit + ' in the unpinned columns' : `Next ${unit}: ${topics[active + 1].label}`);
    peekButtons.forEach((node, i) => { const peer = i ? next : prev; node.hidden = peer.disabled || full || paired || presenting; node.setAttribute('aria-label', peer.getAttribute('aria-label')); node.title = peer.getAttribute('aria-label'); });
    count.textContent = !full && paired ? `${pluralTitle} ${pair[0] + 1} and ${pair[1] + 1} of ${topics.length}${pinned === null ? '' : '; ' + (pinned ? 'right' : 'left') + ' pinned'}` : `${unitTitle} ${active + 1} of ${topics.length}`;
    place.replaceChildren(make('b', '', !full && paired ? `${pair[0] + 1}–${pair[1] + 1}` : String(active + 1)), make('span', '', ` of ${topics.length}`));
    // The fade under the stepper takes the chapter's own background colour.
    const paint = window.getComputedStyle(topics[active].section).backgroundColor;
    if (paint && paint !== 'transparent' && !/^rgba\(.*,\s*0\)$/.test(paint)) stage.style.setProperty('--reader-card-bg', paint);
    const view = currentView();
    viewButtons.forEach(node => { node.setAttribute('aria-pressed', String(node.dataset.readerView === view)); node.disabled = node.dataset.readerView === 'pair' && topics.length < 2; });
    if (slidesButton) slidesButton.hidden = !presentable || !full;
    layerPanel.hidden = !presentKinds.length && (!slidesButton || slidesButton.hidden);
    syncLayerControls(); setOffset(); align(animate); fitFaces();
    syncPresentation();
  }
  function currentView() { return presenting ? 'present' : full ? 'full' : paired ? 'pair' : 'single'; }
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
    if (target === topic.section) topic.body.scrollTop = presenting ? 0 : positions.get(topic.section.id) || 0;
    else topic.body.scrollTop += target.getBoundingClientRect().top - topic.body.getBoundingClientRect().top - 12;
    if (!presenting) positions.set(topic.section.id, topic.body.scrollTop);
    topic.section.classList.toggle('topic-scrolled', topic.body.scrollTop > 24);
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
    if (view === 'present') { startPresentation(active, document.activeElement); return; }
    // A choice made in the overlay navigation closes it, so the chapter takes focus.
    if (document.body.classList.contains('reader-nav-open') && !drawerDocked()) closeDrawer(false, false);
    if (topics.length < 2 && view === 'pair') view = 'single';
    const wasFull = full; remember(); presenting = false;
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
  // ---- Presentation: the active chapter fills the window with its slide on
  // top; the full chapter follows below and scrolls within the chapter only.
  // Chapters without a slide face get a run-time title card. It is not a slide
  // face (no data-slide-face) and never appears in the built HTML.
  // Focused controls own their keys in every view.
  const keyOwners = 'input, select, textarea, button, a, summary, svg, canvas, video, audio, iframe, [data-reader-horizontal], [contenteditable]:not([contenteditable="false"]), [role="tab"], [role="tablist"], [role="slider"], [role="spinbutton"], [role="textbox"]';
  let presentBar = null, presentStatus = null, presentControls = null, presentShown = false, presentTrigger = null, idleTimer = 0, fullscreenLeftAt = -1e9;
  const icon = path => `<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path d="${path}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const icons = {
    restart:'M6 5v14M18 6l-8 6 8 6z', previous:'M15 5l-7 7 7 7', next:'M9 5l7 7-7 7',
    enter:'M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5', leave:'M9 4v5H4M20 9h-5V4M15 20v-5h5M4 15h5v5', close:'M6 6l12 12M18 6L6 18',
  };
  if (presentable) {
    presentBar = make('div', 'present-bar'); presentBar.hidden = true;
    presentBar.setAttribute('role', 'toolbar'); presentBar.setAttribute('aria-label', 'Presentation controls');
    const control = (name, label, action) => { const node = button('present-button present-' + name, '', label); node.innerHTML = icon(icons[name]); node.addEventListener('click', action); return node; };
    presentControls = {
      restart: control('restart', 'Start again from the first ' + unit, () => presentGo(0)),
      previous: control('previous', 'Previous ' + unit, () => presentGo(active - 1)),
      next: control('next', 'Next ' + unit, () => presentGo(active + 1)),
      fullscreen: control('enter', 'Enter fullscreen', () => toggleFullscreen()),
      close: control('close', 'Leave presentation', () => exitPresentation()),
    };
    presentStatus = make('span', 'present-status'); presentStatus.setAttribute('role', 'status'); presentStatus.setAttribute('aria-live', 'polite'); presentStatus.setAttribute('aria-atomic', 'true');
    presentControls.fullscreen.setAttribute('aria-pressed', 'false');
    presentControls.fullscreen.hidden = !document.fullscreenEnabled;
    [presentControls.restart, presentControls.previous, presentStatus, presentControls.next, presentControls.fullscreen, presentControls.close].forEach(node => presentBar.appendChild(node));
    // First in the document, so Shift+Tab from the slide reaches the controls.
    document.body.insertBefore(presentBar, document.body.firstChild);
    ['pointermove', 'pointerdown'].forEach(type => document.addEventListener(type, wake, {passive:true}));
    presentBar.addEventListener('focusin', wake);
    document.addEventListener('fullscreenchange', () => {
      if (!document.fullscreenElement) fullscreenLeftAt = performance.now();
      syncFullscreen();
    });
  }
  function syncFullscreen() {
    if (!presentControls) return;
    const on = !!document.fullscreenElement, node = presentControls.fullscreen, label = on ? 'Leave fullscreen' : 'Enter fullscreen';
    node.innerHTML = icon(icons[on ? 'leave' : 'enter']); node.setAttribute('aria-label', label); node.title = label + ' (F)';
    node.setAttribute('aria-pressed', String(on));
  }
  function toggleFullscreen() {
    const request = document.fullscreenElement ? document.exitFullscreen?.() : document.documentElement.requestFullscreen?.();
    request?.catch?.(() => {});
  }
  // The controls fade when idle and return on pointer movement or a key press.
  function wake() {
    if (!presenting) return;
    document.body.classList.remove('present-idle'); clearTimeout(idleTimer);
    // Keyboard focus on a control keeps them visible; a mouse click does not.
    idleTimer = setTimeout(() => { if (presenting && !presentBar.querySelector(':focus-visible')) document.body.classList.add('present-idle'); }, 2600);
  }
  function titleCard(topic) {
    if (topic.slide !== undefined) return;
    const face = topic.body.querySelector('[data-slide-face]');
    if (face) { face.classList.add('present-slide'); topic.slide = face; return; }
    const card = make('div', 'present-title-card present-slide');
    card.dataset.readerGenerated = ''; card.setAttribute('aria-hidden', 'true');
    const canvas = make('div', 'present-title-canvas');
    canvas.appendChild(make('p', 'present-title-eyebrow', pageTitle));
    canvas.appendChild(make('p', 'present-title-heading', topic.heading?.textContent.trim() || topic.label));
    const lead = [...topic.body.querySelectorAll('.bs-lead')].find(node => !node.closest('[data-slide-face], details.fold'));
    if (lead) {
      const copy = lead.cloneNode(true); copy.className = 'present-title-lead';
      copy.removeAttribute('id'); copy.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
      canvas.appendChild(copy);
    }
    card.appendChild(canvas); topic.body.insertBefore(card, topic.body.firstChild); topic.slide = card;
  }
  function syncPresentation() {
    if (!presentBar) return;
    presentBar.hidden = !presenting;
    document.body.classList.toggle('reader-presenting', presenting);
    if (presenting) {
      topics.forEach(titleCard);
      const topic = topics[active];
      presentStatus.replaceChildren(make('span', 'present-count', `${active + 1} / ${topics.length}`), make('span', 'present-sr', `${unitTitle} ${active + 1} of ${topics.length}: `), make('span', 'present-label', topic.label));
      presentStatus.querySelector('.present-count').setAttribute('aria-hidden', 'true');
      presentControls.previous.disabled = active === 0; presentControls.next.disabled = active === topics.length - 1;
      presentControls.previous.setAttribute('aria-label', active === 0 ? 'Start of ' + plural : `Previous ${unit}: ${topics[active - 1].label}`);
      presentControls.next.setAttribute('aria-label', active === topics.length - 1 ? 'End of ' + plural : `Next ${unit}: ${topics[active + 1].label}`);
      [presentControls.previous, presentControls.next].forEach(node => { node.title = node.getAttribute('aria-label'); });
    }
    if (presenting === presentShown) return;
    presentShown = presenting; syncDrawer(); syncFullscreen();
    if (presenting) wake();
    else {
      clearTimeout(idleTimer); document.body.classList.remove('present-idle');
      if (document.fullscreenElement) document.exitFullscreen?.()?.catch?.(() => {});
    }
  }
  function startPresentation(index, trigger) {
    if (!presentable) return;
    if (!presenting) {
      presentReturn = {view:currentView(), pair:[...pair], pinned, activeColumn};
      presentTrigger = trigger && tools.contains(trigger) ? trigger : null;
      if (!drawerDocked()) closeDrawer(false, false);
    }
    remember(); presenting = true; full = false; paired = false; pinned = null; activeColumn = 0; active = index;
    render(false); restore(); window.scrollTo({top:0, behavior:'instant'});
    saveHistory(false, '#' + topics[active].section.id); window.dispatchEvent(new Event('resize'));
    focusChapter();
  }
  // Every chapter change lands at the top of that chapter, on its slide.
  function presentGo(index) {
    if (!presenting || index < 0 || index >= topics.length) return;
    const keepFocus = presentBar.contains(document.activeElement);
    if (index === active) { topics[active].body.scrollTo({top:0, behavior:'instant'}); return; }
    visit(topics[index].section, true, !keepFocus);
  }
  function exitPresentation() {
    if (!presenting) return;
    const back = presentReturn || validReturn(null);
    presenting = false; activeColumn = back.activeColumn;
    if (back.view === 'pair' && back.pair.includes(active)) {
      pair = [...back.pair]; pinned = back.pinned; paired = true;
      activeColumn = pair.indexOf(active); if (pinned === activeColumn && pinned !== null) pinned = null;
    }
    selectView(back.view);
    if (presentTrigger?.isConnected && presentTrigger.getClientRects().length) presentTrigger.focus({preventScroll:true});
    presentTrigger = null;
  }
  function presentKey(event) {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || document.querySelector('.lb-overlay')) return;
    const key = event.key, inBar = presentBar.contains(event.target);
    if (key === 'Escape') {
      // The first Escape leaves fullscreen (the browser's own); only a later one leaves the view.
      if (document.fullscreenElement || performance.now() - fullscreenLeftAt < 500) return;
      if (event.target?.closest('input, select, textarea, [contenteditable]:not([contenteditable="false"])')) return;
      event.preventDefault(); exitPresentation(); return;
    }
    if (inBar ? [' ', 'Enter'].includes(key) : event.target?.closest(keyOwners)) return;
    const body = topics[active].body, smooth = reducedMotion?.matches ? 'instant' : 'smooth';
    const moves = {ArrowRight:active + 1, PageDown:active + 1, ArrowLeft:active - 1, PageUp:active - 1, Home:0, End:topics.length - 1};
    if (key in moves && !event.shiftKey) { event.preventDefault(); if (!event.repeat) presentGo(moves[key]); return; }
    // Scrolling stays inside the chapter: it never changes the chapter.
    if (key === 'ArrowDown' || key === 'ArrowUp') { event.preventDefault(); body.scrollBy({top:key === 'ArrowDown' ? 64 : -64, behavior:smooth}); return; }
    if (key === ' ') { event.preventDefault(); body.scrollBy({top:(event.shiftKey ? -1 : 1) * body.clientHeight * 0.85, behavior:smooth}); return; }
    if ((key === 'f' || key === 'F') && !event.shiftKey && !event.repeat) { event.preventDefault(); toggleFullscreen(); }
  }
  // All chapters: the Slides switch shows or hides slide faces and their bridges.
  slidesButton?.addEventListener('click', () => {
    const topic = topics[active], line = Math.max(0, nav.getBoundingClientRect().bottom) + 12;
    const anchor = [...topic.body.querySelectorAll('p, h2, h3, h4, li, figure, table, summary')]
      .filter(node => !node.closest('[data-slide-face], .slide-bridge, .present-title-card'))
      .find(node => { const box = node.getBoundingClientRect(); return box.height > 0 && box.bottom > line; }) || topic.section;
    const before = anchor.getBoundingClientRect().top;
    slidesShown = !slidesShown;
    try { localStorage.setItem(slidesKey, slidesShown ? 'shown' : 'hidden'); } catch (_) {}
    syncSlidesButton(); render(false);
    if (full) window.scrollBy({top:anchor.getBoundingClientRect().top - before, behavior:'instant'});
  });
  function syncSlidesButton() {
    if (!slidesButton) return;
    const label = (slidesShown ? 'Hide' : 'Show') + ' slide faces in All ' + plural;
    slidesButton.setAttribute('aria-pressed', String(slidesShown)); slidesButton.setAttribute('aria-label', label); slidesButton.title = label;
  }
  syncSlidesButton();
  prev.addEventListener('click', () => move(-1)); next.addEventListener('click', () => move(1));
  viewButtons.forEach(node => node.addEventListener('click', () => selectView(node.dataset.readerView)));
  document.addEventListener('keydown', event => {
    if (about.open || help.open) return;
    if (presenting) { wake(); presentKey(event); return; }
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
    if (event.target?.closest(keyOwners)) return;
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
  let islandRest = 0;
  document.addEventListener('scroll', event => {
    const topic = topics.find(candidate => candidate.body === event.target);
    if (topic) topic.section.classList.toggle('topic-scrolled', topic.body.scrollTop > 24);
    if (topic ? !topic.section.classList.contains('topic-visible') : !full || event.target !== document) return;
    island.classList.add('reader-island-away'); clearTimeout(islandRest);
    islandRest = setTimeout(() => island.classList.remove('reader-island-away'), 900);
  }, {capture:true, passive:true});
  window.addEventListener('hashchange', () => route()); window.addEventListener('popstate', () => route(true));
  window.addEventListener('resize', () => { syncDrawer(); setOffset(); align(false); fitFaces(); });
  window.addEventListener('load', fitFaces);
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
  // A reload or shared link of a presentation opens the same slide in the same view.
  if (presentable && viewInAddress()) { presenting = true; presentReturn = validReturn(history.state?.chapterReader?.presentReturn); }
  const initial = targetFromHash(location.hash);
  if (!initial || !visit(initial, false, false, false)) render(false);
  routedHash = location.hash; saveHistory(false); window.scrollTo({top:0, behavior:'instant'}); window.dispatchEvent(new Event('resize'));
  if (initial && topicOf(initial) >= 0 && initial !== topics[active].section) requestAnimationFrame(() => { if (topicOf(initial) === active) { reveal(initial); scrollToTarget(initial); } });
});
