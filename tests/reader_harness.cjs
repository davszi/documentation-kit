// Small DOM stand-in for the Node logic checks of the shared reader scripts.
// It runs the kit's real theme/components/chapter-reader.js inside node:vm on
// a synthetic page whose toolbar is parsed from the real chapter-reader.html.
// Geometry (widths, rectangles, card offsets) is fixture input that drives the
// script's code paths; these checks prove state and routing, never layout.
// READER_LOGIC_COMPONENTS points the checks at another copy of
// theme/components, which is how mutation checks run without touching the kit.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const KIT_ROOT = path.resolve(__dirname, '..');
const COMPONENTS = process.env.READER_LOGIC_COMPONENTS
  ? path.resolve(process.env.READER_LOGIC_COMPONENTS)
  : path.join(KIT_ROOT, 'theme/components');
const readComponent = name => fs.readFileSync(path.join(COMPONENTS, name), 'utf8');

// ---- Fixture: a synthetic page, so no kit page text is load-bearing. -------

const FOLD_KINDS = ['math', 'experiment', 'code', 'dead-end'];
const CHAPTERS = [
  {id: 'overview', label: 'Overview'},
  {id: 'notation', label: 'Notation'},
  {id: 'model', label: 'Model'},
  {id: 'solver', label: 'Solver'},
  {id: 'validation', label: 'Validation'},
  {id: 'results', label: 'Results'},
  {id: 'limits', label: 'Limits'},
  {id: 'outlook', label: 'Outlook'},
];
// Other pages of the fixture site, as the build lists them in the sidebar.
const SITE_PAGES = [
  {href: 'index.html', label: 'Home', group: 'Start'},
  {href: 'reader-check.html', label: 'Reader check', group: 'Guides'},
  {href: 'second-guide.html', label: 'Second guide', group: 'Guides'},
  {href: 'appendix.html', label: 'Appendix', group: 'Reference'},
];
const FIXTURE = {
  siteHomeLabel: 'Fixture docs',
  brandMark: '◆',
  brandName: 'Fixture project',
  // A paragraph inside the Math fold of chapter deepChapter, for deep links.
  deepTarget: 'validation-detail',
  deepChapter: 4,
  bodyTop: 112, // top edge of every chapter body in the viewport
  layerOffset: 750, // fold paragraphs sit this far down their chapter body
  navHeight: 56,
  drawerWidth: 280, // stage width lost while navigation is docked
  cardFraction: 0.8, // single-view card width as a share of the stage
};

// ---- Fake DOM ---------------------------------------------------------------

function rect(top, left, width, height) {
  return {top, left, width, height, bottom: top + height, right: left + width};
}

const camel = name => name.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());

class FakeElement {
  constructor(tag, doc = null) {
    Object.assign(this, {
      tag, doc, id: '', parentElement: null, children: [], classes: new Set(),
      attrs: {}, dataset: {}, events: {}, hidden: false, inert: false,
      disabled: false, open: false, tabIndex: 0, _text: '', _scroll: 0, _clientWidth: 800,
    });
    const properties = new Map();
    this.style = {
      setProperty: (key, value) => properties.set(key, value),
      getPropertyValue: key => properties.get(key) || '',
    };
    this.classList = {
      add: (...keys) => keys.forEach(key => this.classes.add(key)),
      remove: (...keys) => keys.forEach(key => this.classes.delete(key)),
      contains: key => this.classes.has(key),
      toggle: (key, on) => {
        const wanted = on === undefined ? !this.classes.has(key) : Boolean(on);
        if (wanted) this.classes.add(key); else this.classes.delete(key);
        return wanted;
      },
    };
  }

  get className() { return [...this.classes].join(' '); }
  set className(value) { this.classes = new Set(String(value).split(/\s+/).filter(Boolean)); }
  get childNodes() { return this.children; }
  get parentNode() { return this.parentElement; }
  get isConnected() {
    for (let node = this; node; node = node.parentElement) if (node.tag === 'document') return true;
    return false;
  }
  get textContent() { return this._text + this.children.map(node => node.textContent).join(''); }
  set textContent(value) {
    this._text = String(value);
    this.children.forEach(node => { node.parentElement = null; });
    this.children = [];
  }
  // A docked navigation drawer takes its width from the reading stage.
  get clientWidth() {
    const docked = this.classes.has('topic-stage') && this.doc?.body.classes.has('reader-nav-docked');
    return this._clientWidth - (docked ? FIXTURE.drawerWidth : 0);
  }
  set clientWidth(value) { this._clientWidth = value; }
  get scrollTop() { return this._scroll; }
  set scrollTop(value) { this._scroll = Math.max(0, value); }

  appendChild(node) {
    node.parentElement?.removeChild(node);
    node.parentElement = this;
    this.children.push(node);
    return node;
  }
  insertBefore(node, sibling) {
    node.parentElement?.removeChild(node);
    const index = sibling ? this.children.indexOf(sibling) : this.children.length;
    assert.ok(index >= 0, 'insertBefore needs a reference node that is a child');
    node.parentElement = this;
    this.children.splice(index, 0, node);
    return node;
  }
  removeChild(node) {
    this.children.splice(this.children.indexOf(node), 1);
    node.parentElement = null;
    return node;
  }
  prepend(...nodes) {
    const first = this.children.find(node => !nodes.includes(node)) || null;
    nodes.forEach(node => this.insertBefore(node, first));
  }
  after(...nodes) {
    const parent = this.parentElement;
    if (!parent) return;
    const later = parent.children.slice(parent.children.indexOf(this) + 1);
    const next = later.find(node => !nodes.includes(node)) || null;
    nodes.forEach(node => parent.insertBefore(node, next));
  }
  replaceChildren(...nodes) {
    this.children.slice().forEach(node => this.removeChild(node));
    this._text = '';
    nodes.forEach(node => this.appendChild(node));
  }
  cloneNode(deep) {
    const copy = new FakeElement(this.tag, this.doc);
    copy.className = this.className;
    copy._text = this._text;
    if (deep) this.children.forEach(child => copy.appendChild(child.cloneNode(true)));
    return copy;
  }

  setAttribute(key, value) {
    if (key === 'id') this.id = String(value);
    else if (key === 'class') this.className = value;
    else if (key === 'hidden') this.hidden = true;
    else if (key.startsWith('data-')) this.dataset[camel(key.slice(5))] = String(value);
    else {
      this.attrs[key] = String(value);
      if (key === 'tabindex') this.tabIndex = Number(value);
    }
  }
  getAttribute(key) {
    if (key === 'id') return this.id || null;
    if (key === 'class') return this.className;
    if (key === 'hidden') return this.hidden ? '' : null;
    if (key.startsWith('data-')) return this.dataset[camel(key.slice(5))] ?? null;
    if (key === 'href') return this.attrs.href ?? this.href ?? null;
    return this.attrs[key] ?? null;
  }
  hasAttribute(key) { return this.getAttribute(key) !== null; }
  removeAttribute(key) { delete this.attrs[key]; }

  // Enough CSS selector support for the selectors the reader scripts use:
  // tag, .class, #id, [attr], [attr="v"], [attr^="v"], :not(...), descendant.
  matches(selector) {
    return selector.split(',').some(alternative => {
      let part = alternative.trim();
      const negation = part.match(/:not\(([^)]+)\)/);
      if (negation && this.matches(negation[1])) return false;
      part = part.replace(/:not\([^)]+\)/g, '');
      const space = part.lastIndexOf(' ');
      if (space >= 0) {
        return this.matches(part.slice(space + 1)) && Boolean(this.parentElement?.closest(part.slice(0, space)));
      }
      const tag = part.match(/^[\w-]+/);
      if (tag && this.tag !== tag[0]) return false;
      for (const [, name] of part.matchAll(/\.([\w-]+)/g)) if (!this.classes.has(name)) return false;
      for (const [, id] of part.matchAll(/#([\w-]+)/g)) if (this.id !== id) return false;
      for (const [, key, op, wanted] of part.matchAll(/\[([\w-]+)(?:(\^?=)"([^"]*)")?\]/g)) {
        const value = this.getAttribute(key);
        if (value === null) return false;
        if (op === '=' && value !== wanted) return false;
        if (op === '^=' && !String(value).startsWith(wanted)) return false;
      }
      return true;
    });
  }
  closest(selector) {
    for (let node = this; node; node = node.parentElement) if (node.matches(selector)) return node;
    return null;
  }
  contains(target) {
    for (let node = target; node; node = node.parentElement) if (node === this) return true;
    return false;
  }
  querySelectorAll(selector) {
    const found = [];
    const walk = node => node.children.forEach(child => {
      if (child.matches(selector)) found.push(child);
      walk(child);
    });
    walk(this);
    return found;
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }

  addEventListener(type, listener) { (this.events[type] ||= []).push(listener); }
  listenerCount(type) { return (this.events[type] || []).length; }
  emit(type, fields = {}) {
    const event = {
      type, target: this, currentTarget: this,
      preventDefault() { this.defaultPrevented = true; },
      ...fields,
    };
    (this.events[type] || []).forEach(listener => listener(event));
    return event;
  }

  // Hidden nodes and content of closed <details> have no box, as in a browser.
  getBoundingClientRect() {
    if (this.hidden || this.closest('[hidden]')) return rect(0, 0, 0, 0);
    for (let node = this.parentElement; node; node = node.parentElement) {
      const inSummary = this.matches('summary') || node.querySelector('summary')?.contains(this);
      if (node.tag === 'details' && !node.open && !inSummary) return rect(0, 0, 0, 0);
    }
    return this.rectFn ? this.rectFn() : rect(1000, 0, 100, 44);
  }
  getClientRects() {
    // Reader styles hide the sidebar brand; the drawer header repeats it.
    if (this.classes.has('brand')) return [];
    const box = this.getBoundingClientRect();
    return box.height === 0 ? [] : [box];
  }
  scrollIntoView() { this.scrolled = (this.scrolled || 0) + 1; }
  focus(options) {
    if (options) assert.equal(options.preventScroll, true, 'The reader moves focus without scrolling the page');
    this.doc.activeElement = this;
    for (let node = this; node; node = node.parentElement) node.emit('focusin', {target: this});
  }
  showModal() { this.open = true; this.querySelector('button')?.focus({preventScroll: true}); }
  close() { this.open = false; this.emit('close'); }
}

// Parse the reader toolbar template into fake elements. The template is a
// single well-formed fragment without comments in attributes, so a tag
// tokenizer suffices; a mismatched close tag fails loudly.
function parseFragment(html, doc) {
  const root = new FakeElement('fragment', doc);
  let current = root;
  const tokens = /<!--[\s\S]*?-->|<\/([\w-]+)\s*>|<([\w-]+)([^>]*)>|([^<]+)/g;
  for (const [token, closing, opening, attributes, text] of html.matchAll(tokens)) {
    if (token.startsWith('<!--')) continue;
    if (closing) {
      assert.equal(current.tag, closing, `chapter-reader.html closes <${closing}> out of order`);
      current = current.parentElement;
    } else if (opening) {
      const node = new FakeElement(opening, doc);
      for (const [, key, value] of attributes.matchAll(/([\w-]+)(?:="([^"]*)")?/g)) node.setAttribute(key, value ?? '');
      current.appendChild(node);
      if (!/\/\s*$/.test(attributes) && !['input', 'br', 'img', 'meta', 'link'].includes(opening)) current = node;
    } else if (text.trim()) {
      current._text += text.trim();
    }
  }
  assert.equal(current, root, 'chapter-reader.html leaves an element unclosed');
  return root.children;
}

// Toolbar elements chapter-reader.js looks up without a null check.
const TOOLBAR_HOOKS = [
  '.reader-title strong', '[data-reader-drawer]', '[data-reader-pagination]', '[data-topic-prev]',
  '[data-topic-next]', '[data-topic-count]', '[data-reader-view="single"]', '[data-reader-view="pair"]',
  '[data-reader-view="full"]', '[data-reader-about]', '[data-reader-help]', '.reader-tools', '.reader-place',
  '[data-reader-layers]',
];

// ---- Page builder -------------------------------------------------------------

function bootReader(hash = '', options = {}) {
  const {
    width = 800, gap = 16, reducedMotion = false, stored = {}, chapters = CHAPTERS,
    pageName = 'reader-check', title = 'Reader check', unit = 'chapter', groups = {},
    redirects = {}, adapted = false, headingTag = 'h3', foldKinds = null,
    subsections = [], sitePages = SITE_PAGES, runReader = true, authorOpen = [],
    headless = [], storageThrows = false,
  } = options;
  const location = new URL(`file:///fixture-site/${pageName}.html${hash}`);
  const document = new FakeElement('document');
  document.doc = document;
  const make = (tag, {id = '', cls = '', parent = null, text = ''} = {}) => {
    const node = new FakeElement(tag, document);
    node.id = id;
    node.className = cls;
    node._text = text;
    parent?.appendChild(node);
    return node;
  };
  const linkTo = (href, node) => {
    node.attrs.href = href;
    node.href = new URL(href, location).href;
    if (href.startsWith('#')) node.hash = href;
    return node;
  };
  document.body = make('body', {parent: document});
  document.head = make('head', {parent: document});
  document.body.dataset.siteHomeLabel = FIXTURE.siteHomeLabel;
  document.getElementById = id => document.querySelectorAll('[id]').find(node => node.id === id) || null;
  document.createElement = tag => { const node = make(tag); node.clientWidth = width; return node; };

  const layout = make('div', {cls: 'layout', parent: document.body});
  const sidebar = make('aside', {id: 'sidebar', cls: 'sidebar', parent: layout});
  const brand = make('a', {cls: 'brand', parent: sidebar});
  make('span', {cls: 'brand-mark', parent: brand, text: FIXTURE.brandMark});
  make('span', {cls: 'brand-name', parent: brand, text: FIXTURE.brandName});
  const toc = make('div', {id: 'toc', cls: 'toc', parent: sidebar});
  const content = make('main', {id: 'top', cls: 'content', parent: layout});
  const overview = make('details', {cls: 'topic-overview', parent: content});
  make('summary', {parent: overview, text: 'About this page'});
  make('p', {parent: overview, text: 'Introduction and links'});
  const config = make('div', {parent: content});
  Object.assign(config.dataset, {readerTitle: title, readerUnit: unit});
  config.hidden = true;
  if (adapted) config.dataset.readerAdapted = '';

  const [nav] = parseFragment(readComponent('chapter-reader.html'), document);
  for (const hook of TOOLBAR_HOOKS) assert.ok(nav.querySelector(hook), `chapter-reader.html provides ${hook}`);
  content.appendChild(nav);
  nav.rectFn = () => rect(0, 0, width, FIXTURE.navHeight);

  // Card geometry stands in for the stylesheet: pair view shows two equal
  // columns, single view a card narrower than the stage, laid out in a row.
  const stageWidth = () => width - (document.body.classes.has('reader-nav-docked') ? FIXTURE.drawerWidth : 0);
  const pairView = () => content.dataset.topicView === 'pair' && content.dataset.topicLayout === 'deck';
  const sections = chapters.map((chapter, index) => {
    const section = make('section', {id: chapter.id, cls: 'card', parent: content});
    if (groups[chapter.id]) section.dataset.readerGroup = groups[chapter.id];
    if (adapted) section.dataset.readerChapter = '';
    section.top = 1000 + 200 * index;
    // A headless chapter has no heading of its own, only one inside a card after its opening text.
    if (headless.includes(index)) {
      make('p', {parent: section, text: 'Opening text'});
      make('h3', {id: 'heading-' + index, parent: make('div', {cls: 'card', parent: section}), text: 'Nested'});
    }
    else make(headingTag, {id: 'heading-' + index, parent: section, text: chapter.label});
    make('p', {id: 'story-' + index, parent: section, text: 'Story content'});
    for (const kind of foldKinds?.[index] ?? FOLD_KINDS) {
      const fold = make('details', {id: `fold-${index}-${kind}`, cls: 'fold fold-' + kind, parent: section});
      fold.dataset.fold = kind;
      // An author-open fold: `<!-- fold: math (open) ... -->` or raw HTML with `open`.
      fold.open = authorOpen.some(([chapter, open]) => chapter === index && open === kind);
      const summary = make('summary', {parent: fold});
      make('span', {cls: 'fold-tag', parent: summary, text: kind});
      make('span', {parent: summary, text: 'Details'});
      const deep = index === FIXTURE.deepChapter && kind === 'math';
      const id = deep ? FIXTURE.deepTarget : `depth-${index}-${kind}`;
      const paragraph = make('p', {id, parent: fold, text: 'Layer content'});
      paragraph.rectFn = () => {
        const scrolled = section.querySelector('.chapter-body')?.scrollTop || 0;
        return rect(FIXTURE.bodyTop + FIXTURE.layerOffset - scrolled, 0, 200, 100);
      };
      if (index === 0 && kind === 'math') {
        make('p', {id: 'display-equation', parent: fold, text: '$$x^2 + y^2 = r^2$$'});
        const table = make('table', {id: 'depth-table', parent: fold});
        make('td', {parent: table, text: '123 preserved'});
      }
    }
    Object.defineProperties(section, {
      offsetWidth: {get: () => pairView() ? (stageWidth() - gap) / 2 : stageWidth() * FIXTURE.cardFraction},
      offsetLeft: {get: () => pairView() ? 0 : index * (stageWidth() * FIXTURE.cardFraction + gap)},
    });
    section.rectFn = () => rect(content.dataset.topicLayout === 'deck' ? 68 : section.top, 0, section.offsetWidth, 400);
    return section;
  });
  const links = chapters.map(chapter => linkTo('#' + chapter.id, make('a', {parent: toc, text: chapter.label})));
  // Subsections: a heading (or nested card) inside a chapter, optionally
  // inside that chapter's fold number `fold`, with its own sidebar link.
  subsections.forEach(({id, label, chapter, card = false, fold}) => {
    const parent = Number.isInteger(fold) ? sections[chapter].querySelectorAll('details.fold')[fold] : sections[chapter];
    make(card ? 'section' : 'h4', {id, cls: card ? 'card' : '', parent, text: label});
    linkTo('#' + id, make('a', {cls: 'sub-link', parent: toc, text: label}));
  });
  const redirected = [];
  location.replace = href => redirected.push(href);
  Object.entries(redirects).forEach(([id, href]) => {
    const marker = linkTo(href, make('a', {id, parent: content}));
    marker.dataset.readerRedirect = 'moved';
  });
  sitePages.forEach(({href, label, group}) => {
    const current = href === pageName + '.html';
    const link = linkTo(href, make('a', {cls: 'xpage' + (current ? ' current' : ''), parent: toc, text: label}));
    link.dataset.group = group;
    if (current) link.setAttribute('aria-current', 'page');
  });
  const backdrop = make('div', {id: 'backdrop', cls: 'backdrop', parent: document.body});

  const window = new FakeElement('window');
  Object.assign(window, {innerWidth: width + 24, innerHeight: 800, scrollY: 0});
  window.matchMedia = () => ({matches: reducedMotion});
  window.getComputedStyle = () => ({getPropertyValue: key => key === '--topic-gap' ? gap + 'px' : ''});
  window.scrollTo = ({top}) => { window.scrollY = top; };
  window.scrollBy = ({top}) => { window.scrollY += top; };
  window.dispatchEvent = event => window.emit(event.type, event);
  const storage = new Map(Object.entries(stored));
  // Storage that throws stands for a browser that refuses site data.
  const refuse = () => { throw new Error('SecurityError: storage is disabled'); };
  const localStorage = storageThrows ? {getItem: refuse, setItem: refuse} : {
    getItem: key => storage.get(key) ?? null,
    setItem: (key, value) => storage.set(key, String(value)),
  };
  // Session history as a stack of {url, state}; states are stored as copies.
  const entries = [{url: location.href, state: null}];
  let cursor = 0;
  const copy = value => JSON.parse(JSON.stringify(value));
  const history = {
    scrollRestoration: 'auto',
    get state() { return entries[cursor].state; },
    pushState(state, unused, url) {
      location.href = new URL(url, location).href;
      entries.splice(++cursor, entries.length, {url: location.href, state: copy(state)});
    },
    replaceState(state, unused, url) {
      location.href = new URL(url, location).href;
      entries[cursor] = {url: location.href, state: copy(state)};
    },
  };
  const frames = [];
  // Timers run when the test flushes, after the animation frames.
  const timers = new Map();
  let timerId = 0;
  const flush = () => {
    while (frames.length || timers.size) {
      while (frames.length) frames.shift()();
      const [id, callback] = timers.entries().next().value || [];
      if (id !== undefined) { timers.delete(id); callback(); }
    }
  };

  const page = {document, window, location, history, storage, content, sidebar, toc, nav, overview,
    backdrop, sections, links, redirected, flush};
  if (!runReader) return page;
  vm.runInNewContext(readComponent('chapter-reader.js'), {
    document, window, location, history, localStorage, URL,
    requestAnimationFrame: callback => frames.push(callback),
    setTimeout: callback => { timers.set(++timerId, callback); return timerId; },
    clearTimeout: id => timers.delete(id),
    Event: class { constructor(type) { this.type = type; } },
  });
  document.emit('DOMContentLoaded');
  flush();
  const stage = content.querySelector('.topic-stage');
  if (!stage) return page;
  return Object.assign(page, readerControls(page, {stage, chapters, width, gap, back: () => {
    assert.ok(cursor > 0, 'Back needs an earlier history entry');
    location.href = entries[--cursor].url;
    window.emit('popstate');
    // The browser jumps to the fragment; the reader must restore its own position.
    const section = sections.find(node => '#' + node.id === location.hash);
    if (section) section.querySelector('.chapter-body').scrollTop = 0;
    window.emit('hashchange');
    flush();
  }}));
}

// Interaction helpers and state probes for a page the reader has taken over.
function readerControls(page, {stage, chapters, width, gap, back}) {
  const {document, content, nav, sections} = page;
  const strip = stage.querySelector('.topic-strip');
  const bodies = sections.map(section => section.querySelector('.chapter-body'));
  bodies.forEach(body => { body.rectFn = () => rect(FIXTURE.bodyTop, 0, width, 620); });
  const controlSelectors = {
    prev: '[data-topic-prev]', next: '[data-topic-next]', count: '[data-topic-count]',
    single: '[data-reader-view="single"]', pair: '[data-reader-view="pair"]', full: '[data-reader-view="full"]',
    about: '[data-reader-about]', help: '[data-reader-help]', drawer: '[data-reader-drawer]',
    present: '[data-reader-view="present"]', island: '[data-reader-pagination]', place: '.reader-place',
    tools: '.reader-tools', slides: '[data-reader-slides]',
  };
  const control = name => {
    const node = document.querySelector(controlSelectors[name]);
    assert.ok(node, `chapter-reader.html provides the ${name} control`);
    return node;
  };
  // A primary click: pointerdown bubbles, the button's own handler runs, then
  // the document-level click handler sees it.
  const click = (node, fields = {}) => {
    const event = {
      button: 0, target: node, currentTarget: node,
      preventDefault() { this.defaultPrevented = true; }, ...fields,
    };
    for (let current = node; current; current = current.parentElement) current.emit('pointerdown', event);
    if (node.tag === 'button') node.emit('click', event);
    return document.emit('click', event);
  };
  const key = (value, fields = {}) =>
    document.emit('keydown', {key: value, target: document.activeElement || content, ...fields});
  const chapterKey = (value, fields = {}) => key(value, {target: content, ...fields});
  const visible = () => sections.filter(section => !section.inert).map(section => section.id);
  // The page-wide "Also show" options at the bottom of the navigation.
  const panel = () => document.querySelector('.reader-layers');
  const option = kind => kind === 'all' ? panel().querySelector('[data-reader-layer-all]')
    : panel().querySelector(`[data-reader-layer="${kind}"]`);
  // Press options until exactly `kinds` are on.
  const layers = kinds => {
    panel().querySelectorAll('[data-reader-layer]').forEach(node => {
      if ((node.getAttribute('aria-pressed') === 'true') !== kinds.includes(node.dataset.readerLayer)) click(node);
    });
  };
  const swipe = (x0, y0, x1, y1, target = sections.find(section => section.classes.has('topic-active'))) => {
    stage.emit('touchstart', {target, touches: [{clientX: x0, clientY: y0}]});
    stage.emit('touchend', {target, touches: [], changedTouches: [{clientX: x1, clientY: y1}]});
  };
  const folds = index => sections[index].querySelectorAll('details.fold');
  const states = index => folds(index).map(fold => fold.open);
  // A reader's own click on a fold summary: the summary's click handlers run,
  // then the browser toggles the fold unless a handler prevented it.
  const toggleFold = (index, n) => {
    const fold = folds(index)[n], summary = fold.querySelector('summary');
    const event = summary.emit('click', {button: 0, preventDefault() { this.defaultPrevented = true; }});
    if (!event.defaultPrevented) fold.open = !fold.open;
    return event;
  };
  const pin = index => click(sections[index].querySelector('.chapter-pin'));
  const translateX = node => Number(node.style.transform.match(/translate3d\(([-\d.]+)px/)[1]);

  // Single view: every chapter stays in the strip, none is hidden, only the
  // active one is interactive, and the strip centres it in the stage.
  const assertCentred = (index, what = 'Single view') => {
    assert.equal(strip.children.length, chapters.length, `${what}: every chapter stays in the strip`);
    assert.ok(sections.every(section => !section.hidden), `${what}: no chapter is hidden`);
    assert.deepEqual(visible(), [sections[index].id], `${what}: only ${sections[index].id} is shown`);
    const card = sections[index];
    const centreOffset = card.offsetLeft + translateX(strip) - (stage.clientWidth - card.offsetWidth) / 2;
    assert.ok(Math.abs(centreOffset) < 1e-8, `${what}: the strip centres ${card.id} in the current stage width`);
  };
  // Pair view: left column at 0, right column one card and gap further, all
  // other chapters placed outside the stage.
  const assertPair = (left, right, what = 'Pair view') => {
    assert.equal(content.dataset.topicView, 'pair', `${what}: the page is in pair view`);
    assert.equal(strip.children.length, chapters.length, `${what}: every chapter stays in the strip`);
    const cardWidth = sections[left].offsetWidth;
    assert.equal(translateX(sections[left]), 0, `${what}: ${sections[left].id} is the left column`);
    assert.equal(translateX(sections[right]), cardWidth + gap, `${what}: ${sections[right].id} is the right column`);
    assert.deepEqual(visible(), [sections[left].id, sections[right].id].sort((a, b) =>
      sections.findIndex(s => s.id === a) - sections.findIndex(s => s.id === b)), `${what}: only the two columns are shown`);
    sections.forEach((section, i) => {
      if (i === left || i === right) return;
      const x = translateX(section);
      assert.ok(x + section.offsetWidth <= 0 || x >= stage.clientWidth, `${what}: ${section.id} is placed off stage`);
    });
  };
  return {stage, strip, bodies, control, click, key, chapterKey, visible, panel, option, layers, folds, states,
    toggleFold, swipe, pin, back, assertCentred, assertPair};
}

// Run fold-controls.js on a booted page, with its own storage.
function runFoldControls(page, localStorage) {
  vm.runInNewContext(readComponent('fold-controls.js'), {
    document: page.document, window: page.window, location: page.location, localStorage,
  });
}

module.exports = {CHAPTERS, SITE_PAGES, FIXTURE, FakeElement, rect,
  readComponent, bootReader, runFoldControls};
