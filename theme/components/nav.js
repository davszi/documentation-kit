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
  var current = document.querySelector('.toc a.xpage.current');
  var bar = current && current.closest('.sidebar');
  if (bar) {
    var box = bar.getBoundingClientRect(), r = current.getBoundingClientRect();
    if (r.bottom > box.bottom - 40) bar.scrollTop += r.top - box.top - box.height / 3;
  }
})();
