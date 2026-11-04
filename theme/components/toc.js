// Sidebar TOC scrollspy: highlights the entry for the section in view.
(function(){
  var toc = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
  var targets = toc.map(function(a){ return document.getElementById(a.hash.slice(1)); });
  var active = null;
  function spy(){
    var cur = 0;
    for (var i = 0; i < targets.length; i++){
      var t = targets[i];
      if (t && t.getBoundingClientRect().top <= 130) cur = i;
    }
    if (cur === active) return;
    active = cur;
    toc.forEach(function(a, i){ a.classList.toggle('active', i === cur); });
    var link = toc[cur];
    if (link && link.scrollIntoView) link.scrollIntoView({ block: 'nearest' });
  }
  var ticking = false;
  window.addEventListener('scroll', function(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function(){ spy(); ticking = false; });
  }, { passive: true });
  spy();
})();
