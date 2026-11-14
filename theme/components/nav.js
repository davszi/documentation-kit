// Mobile nav drawer: hamburger toggles the sidebar, backdrop/TOC-click closes it.
(function(){
  var menu = document.getElementById('menu');
  var backdrop = document.getElementById('backdrop');
  function closeNav(){ document.body.classList.remove('nav-open'); }
  if (menu) menu.addEventListener('click', function(){ document.body.classList.toggle('nav-open'); });
  if (backdrop) backdrop.addEventListener('click', closeNav);
  document.querySelectorAll('.toc a').forEach(function(a){ a.addEventListener('click', closeNav); });
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
(function(){
  var box = document.querySelector('.toc .repo-tree[data-repo-tree-src]');
  var all = box && box.querySelector('details.repo-tree-all');
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
    script.src = box.getAttribute('data-repo-tree-src');
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
  var tones = ['#6ee7c5', '#b69cff', '#ffb35c', '#5cc8ff', '#ff8597', '#9ad46b'];
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

