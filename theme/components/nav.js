// Mobile nav drawer on pages without the reader, which drives its own drawer:
// the menu button opens the sidebar and moves focus into it; the button, the
// backdrop, Escape or a link closes it. Below 900 px a closed sidebar is inert,
// so its off-screen links take no keyboard focus, and an open one makes the
// page behind it inert, except the top bar: its menu button stays reachable by
// keyboard and screen reader to close the drawer, which covers it for a
// pointer. The state follows the body's nav-open class, whichever script sets
// it. Without JavaScript nothing is inert and the links stay reachable.
(function(){
  var menu = document.getElementById('menu');
  var backdrop = document.getElementById('backdrop');
  var sidebar = document.getElementById('sidebar');
  var content = document.querySelector('main.content');
  var narrow = window.matchMedia('(max-width:900px)');
  function isOpen(){ return document.body.classList.contains('nav-open'); }
  function sync(){
    if (document.body.classList.contains('reader-enabled')) return;
    var open = isOpen();
    if (menu) menu.setAttribute('aria-expanded', String(open));
    if (sidebar) sidebar.inert = narrow.matches && !open;
    var behind = narrow.matches && open;
    if (content) Array.prototype.forEach.call(content.children, function(node){
      if (!node.classList.contains('topbar')) node.inert = behind;
    });
  }
  function closeNav(refocus){
    var was = isOpen();
    document.body.classList.remove('nav-open');
    sync();
    if (was && refocus && menu) menu.focus({preventScroll:true});
  }
  function openNav(){
    document.body.classList.add('nav-open');
    sync();
    var first = sidebar && sidebar.querySelector('a[href], button, summary');
    if (first) first.focus({preventScroll:true});
  }
  if (menu) menu.addEventListener('click', function(){ if (isOpen()) closeNav(true); else openNav(); });
  if (backdrop) backdrop.addEventListener('click', function(){ closeNav(true); });
  document.addEventListener('keydown', function(event){
    if (event.key !== 'Escape' || !isOpen() || document.body.classList.contains('reader-enabled')) return;
    event.preventDefault();
    closeNav(true);
  });
  document.querySelectorAll('.toc a').forEach(function(a){ a.addEventListener('click', function(){ closeNav(false); }); });
  new MutationObserver(sync).observe(document.body, {attributes: true, attributeFilter: ['class']});
  if (narrow.addEventListener) narrow.addEventListener('change', sync); else if (narrow.addListener) narrow.addListener(sync);
  sync();
})();

// nested_nav and folded_groups: groups the reader opens stay open across pages
// (per viewer, best effort). Groups the server opened (the current page's, or
// with nested_nav the first on the home page) are not stored, so only the
// reader's own choices persist.
(function(){
  var folds = document.querySelectorAll('.toc details.nav-fold, .toc details.nav-section-fold');
  if (!folds.length) return;
  var key = 'docsite-nav-open:' + (document.body.getAttribute('data-site-home-label') || '');
  var opened = [];
  try { opened = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
  if (!Array.isArray(opened)) opened = [];
  folds.forEach(function(fold){
    var group = fold.dataset.group;
    if (opened.indexOf(group) >= 0) fold.open = true;
    if (fold.hasAttribute('data-nav-default')) return;
    // Record on click, which runs before the queued toggle event and before navigation.
    fold.querySelector('summary').addEventListener('click', function(){
      var willOpen = !fold.open;
      opened = opened.filter(function(g){ return g !== group; });
      if (willOpen) opened.push(group);
      try { localStorage.setItem(key, JSON.stringify(opened)); } catch (e) {}
    });
  });
})();

// Keep the current page's sidebar entry in view: its nested_nav group entry, or
// its repository-tree file when the page has no navigation entry.
(function(){
  var current = document.querySelector('.toc a.xpage.current') || document.querySelector('.toc .repo-tree a[aria-current="page"]');
  var bar = current && current.closest('.sidebar');
  if (!bar || !(document.querySelector('.toc details.nav-fold') || current.closest('.repo-tree'))) return;
  var scroller = bar;
  var box = scroller.getBoundingClientRect(), r = current.getBoundingClientRect();
  if (r.height && (r.bottom > box.bottom - 24 || r.top < box.top)) scroller.scrollTop += r.top - box.top - box.height / 3;
})();

// A Reference tree too large to repeat in every page is written once as
// reference.tree.js. A <script src> hands its markup over, since fetch() of a
// neighbouring file fails on a page opened from disk. It loads when "Browse by
// folder" opens, or at once on a page the tree lists, which then unfolds to its
// file as the inline tree does. Without JavaScript the disclosure keeps the
// folders leading to the page and a link to the Reference index page.
// The tree box is taken only from the shell's sidebar, which comes before the
// page content, and the script only from the build's own reference.tree.js,
// so nothing the page content holds can choose what loads.
(function(){
  var sidebar = document.getElementById('sidebar');
  var box = sidebar && sidebar.matches('nav.sidebar') && !sidebar.closest('main')
    ? sidebar.querySelector(':scope > .toc > .repo-tree[data-repo-tree-src]') : null;
  var source = box && box.getAttribute('data-repo-tree-src');
  var all = source && /^reference\.tree\.js(?:\?v=[0-9a-f]+)?$/.test(source) && box.querySelector(':scope > details.repo-tree-all');
  if (!all) return;
  var current = box.getAttribute('data-repo-tree-current');
  var state = 'idle';
  function place(){
    var markup = window.docsReferenceTree;
    if (typeof markup !== 'string') { state = 'failed'; return; }
    var holder = document.createElement('div');
    holder.innerHTML = markup;
    var list = holder.querySelector('ul.repo-tree-list');
    if (!list) { state = 'failed'; return; }
    var here = null;
    if (current) {
      list.querySelectorAll('a.repo-tree-file').forEach(function(a){
        if (a.getAttribute('href') === current) here = a;
      });
    }
    if (here) {
      here.classList.add('current');
      if (box.hasAttribute('data-repo-tree-mark')) here.setAttribute('aria-current', 'page');
      for (var node = here.parentElement; node && node !== list; node = node.parentElement) {
        if (node.matches('li.repo-tree-folder')) {
          node.classList.add('has-current');
          node.querySelector(':scope > details').open = true;
        }
      }
    }
    var old = all.querySelector(':scope > ul.repo-tree-list');
    if (old) old.replaceWith(list); else all.insertBefore(list, all.querySelector(':scope > .repo-tree-index'));
    list.addEventListener('click', function(event){
      if (event.target.closest('a')) document.body.classList.remove('nav-open');
    });
    box.setAttribute('data-repo-tree-ready', '');
    state = 'ready';
    var bar = here && here.closest('.sidebar');
    if (bar && all.open) {
      var frame = bar.getBoundingClientRect(), r = here.getBoundingClientRect();
      if (r.height && (r.bottom > frame.bottom - 24 || r.top < frame.top)) bar.scrollTop += r.top - frame.top - frame.height / 3;
    }
  }
  function load(){
    if (state !== 'idle') return;
    if (typeof window.docsReferenceTree === 'string') { place(); return; }
    state = 'loading';
    var script = document.createElement('script');
    script.src = source;
    script.onload = place;
    script.onerror = function(){ state = 'failed'; };
    document.head.appendChild(script);
  }
  if (current) load();
  else all.addEventListener('toggle', function(){ if (all.open) load(); });
})();

// Group tones: a site may colour its groups in CSS (--g); groups without one get
// the next tone in order, so every group header, page, chapter list and home-page
// map group matches.
(function(){
  // The tones are theme colours (base.css), so a project's [theme_colors] can move them.
  var tones = [1, 2, 3, 4, 5, 6].map(function(n){ return 'var(--group-tone-' + n + ')'; });
  var order = [];
  document.querySelectorAll('.toc .nav-group[data-group]').forEach(function(label){
    var group = label.getAttribute('data-group');
    if (order.indexOf(group) < 0) order.push(group);
  });
  order.forEach(function(group, i){
    var name = window.CSS && CSS.escape ? CSS.escape(group) : group.replace(/["\\]/g, '\\$&');
    var members = document.querySelectorAll('.toc [data-group="' + name + '"], .map-group[data-group="' + name + '"]');
    members.forEach(function(el){
      if (getComputedStyle(el).getPropertyValue('--g').trim()) return;
      el.style.setProperty('--g', tones[i % tones.length]);
    });
  });
})();

// The sidebar's last line names the kit; here it gains the day and hour of the
// last build, in the reader's own time zone. The time comes from build-info.js,
// which the build writes beside the pages. It is asked for afresh on each
// load, so a cached page cannot show an older site as newly built.
(function(){
  var slot = document.querySelector('[data-kit-built]');
  if (!slot) return;
  var info = document.createElement('script');
  info.src = 'build-info.js?' + Date.now();
  info.onload = function(){
    var built = new Date(window.docsSiteBuilt || '');
    if (isNaN(built)) return;
    slot.textContent = 'Site built ' + built.toLocaleString(undefined, {day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit'});
    slot.title = window.docsSiteBuilt + ' (UTC)';
    slot.hidden = false;
  };
  document.head.appendChild(info);
})();
