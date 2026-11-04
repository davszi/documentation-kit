// Page tabs (.ptab / .ptab-panel — distinct from the mode-views tabs):
// click switching, hash deep-links that activate the owning tab, and a
// TOC filtered to the active tab (unannotated links always show).
(function(){
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.ptab'));
  if (!tabs.length) return;
  var panels = Array.prototype.slice.call(document.querySelectorAll('.ptab-panel'));
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a[data-ptab]'));

  function activate(i, scrollId){
    tabs.forEach(function(t){ t.classList.toggle('on', +t.getAttribute('data-ptab') === i); });
    panels.forEach(function(p){ p.hidden = +p.getAttribute('data-ptab') !== i; });
    tocLinks.forEach(function(a){
      a.style.display = +a.getAttribute('data-ptab') === i ? '' : 'none';
    });
    if (scrollId){
      var el = document.getElementById(scrollId);
      if (el) el.scrollIntoView();
    }
  }

  tabs.forEach(function(t){
    t.addEventListener('click', function(){ activate(+t.getAttribute('data-ptab')); });
  });

  function route(){
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    var panel = el && el.closest('.ptab-panel');
    if (panel) activate(+panel.getAttribute('data-ptab'), id);
  }

  window.addEventListener('hashchange', route);
  activate(0);
  route();
})();
