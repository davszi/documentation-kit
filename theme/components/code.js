// Code-block chrome: wraps bare <pre> blocks in a .codeblock, then gives
// every block its hover chips — language badge, source link (rewritten to
// VS Code / GitHub by filelinks.js, which runs after this), copy button.
(function(){
  document.querySelectorAll('pre').forEach(function(pre){
    if (pre.closest('.codeblock')) return;
    var wrap = document.createElement('div');
    wrap.className = 'codeblock';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
  });

  document.querySelectorAll('.codeblock').forEach(function(cb){
    var pre = cb.querySelector('pre');
    if (!pre || cb.querySelector('.cb-chips')) return;
    var chips = document.createElement('div');
    chips.className = 'cb-chips';

    var lang = cb.getAttribute('data-lang');
    if (lang){
      var badge = document.createElement('span');
      badge.className = 'cb cb-lang';
      badge.textContent = lang;
      chips.appendChild(badge);
    }

    var src = cb.getAttribute('data-source');
    if (src){
      var path = src.split('#')[0];
      var line = (src.split('#')[1] || '').match(/^L(\d+)/);
      var a = document.createElement('a');
      a.className = 'cb cb-src';
      a.textContent = path.split('/').pop() + (line ? ':' + line[1] : '');
      a.setAttribute('href', '../../' + path);  // repo-relative from docs/html/
      chips.appendChild(a);
    }

    var copy = document.createElement('button');
    copy.className = 'cb cb-copy';
    copy.type = 'button';
    copy.textContent = 'copy';
    copy.title = 'Copy code';
    copy.addEventListener('click', function(){
      if (!navigator.clipboard) return;
      var code = pre.querySelector('code') || pre;
      navigator.clipboard.writeText(code.textContent).then(function(){
        copy.textContent = '✓ copied';
        copy.classList.add('ok');
        setTimeout(function(){
          copy.textContent = 'copy';
          copy.classList.remove('ok');
        }, 1200);
      });
    });
    chips.appendChild(copy);
    cb.appendChild(chips);
  });
})();
