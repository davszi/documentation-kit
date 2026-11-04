// Mobile nav drawer: hamburger toggles the sidebar, backdrop/TOC-click closes it.
(function(){
  var menu = document.getElementById('menu');
  var backdrop = document.getElementById('backdrop');
  function closeNav(){ document.body.classList.remove('nav-open'); }
  if (menu) menu.addEventListener('click', function(){ document.body.classList.toggle('nav-open'); });
  if (backdrop) backdrop.addEventListener('click', closeNav);
  document.querySelectorAll('.toc a').forEach(function(a){ a.addEventListener('click', closeNav); });
})();
