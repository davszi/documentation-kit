// Mobile nav drawer: hamburger toggles the sidebar, backdrop/TOC-click closes it.
(function(){
  var menu = document.getElementById('menu');
  var backdrop = document.getElementById('backdrop');
  function closeNav(){ document.body.classList.remove('nav-open'); }
  if (menu) menu.addEventListener('click', function(){ document.body.classList.toggle('nav-open'); });
  if (backdrop) backdrop.addEventListener('click', closeNav);
  document.querySelectorAll('.toc a').forEach(function(a){ a.addEventListener('click', closeNav); });
})();

// nested_nav: groups the reader opens stay open across pages (per viewer, best
// effort). Groups the server opened (the current page's, or the first on the
// home page) are not stored, so only the reader's own choices persist.
(function(){
  var folds = document.querySelectorAll('.toc details.nav-fold');
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
  // A docked repository section scrolls on its own; otherwise scroll the menu.
  var tree = current.closest('.repo-tree');
  var scroller = tree && tree.scrollHeight > tree.clientHeight + 1 ? tree : bar;
  var box = scroller.getBoundingClientRect(), r = current.getBoundingClientRect();
  if (r.height && (r.bottom > box.bottom - 24 || r.top < box.top)) scroller.scrollTop += r.top - box.top - box.height / 3;
})();

// Group tones: a site may colour its groups in CSS (--g); groups without one get
// the next tone in order, so every group header, page and chapter list matches.
(function(){
  var tones = ['#6ee7c5', '#b69cff', '#ffb35c', '#5cc8ff', '#ff8597', '#9ad46b'];
  var order = [];
  document.querySelectorAll('.toc .nav-group[data-group]').forEach(function(label){
    var group = label.getAttribute('data-group');
    if (order.indexOf(group) < 0) order.push(group);
  });
  order.forEach(function(group, i){
    var members = document.querySelectorAll('.toc [data-group="' + group.replace(/"/g, '\\"') + '"]');
    members.forEach(function(el){
      if (getComputedStyle(el).getPropertyValue('--g').trim()) return;
      el.style.setProperty('--g', tones[i % tones.length]);
    });
  });
})();

