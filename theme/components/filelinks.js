// Source links retain a repository identity independent of generated-site depth.
// Hosted URLs are emitted by the builder; local review opens the same checkout.
(function(){
  var GH_REPO = '{{GH_REPO}}';
  var GH_REF = '{{GH_REF}}';
  var HOSTED = location.protocol !== 'file:';
  var match = decodeURIComponent(location.pathname).match(/^(.*)\/\.build\/docs\/html\/[^\/]*$/);
  var REPO_ROOT = match ? match[1] : '';
  // No remote means HTTP source links keep the builder/exporter's local paths.
  if (HOSTED && !GH_REPO) return;
  document.querySelectorAll('a[href]').forEach(function(a){
    // The publication exporter already pointed this link at its published copy.
    if (a.getAttribute('data-repo-exported') !== null) return;
    var href = a.getAttribute('href');
    var relative = a.getAttribute('data-repo-path');
    var fragment = a.getAttribute('data-repo-fragment') || '';
    if (!relative) {
      if (!href || href.charAt(0) === '#' || /^(?:[a-z]+:|\/\/)/i.test(href)) return;
      var split = href.split('#');
      fragment = split[1] || '';
      if (!/\.(?:py|md)$/.test(split[0]) && !split[0].endsWith('/')) return;
      var out = [];
      ('docs/html/' + split[0]).split('/').forEach(function(p){
        if (p === '..') out.pop();
        else if (p !== '.' && p !== '') out.push(p);
      });
      relative = out.join('/').replace(/^docs\/src\/pages\//,'docs/topics/').replace(/^docs\/src\//,'docs/site/');
      relative = relative.replace(/^docs\/topics\/([^/]+)\.md$/,'docs/topics/$1/index.md');
    }
    var line = (fragment.match(/^L(\d+)/) || a.textContent.match(/:(\d+)\s*$/) || [])[1];
    var directory = relative.endsWith('/');
    if (HOSTED) {
      if (!a.getAttribute('data-repo-path')) a.setAttribute('href', GH_REPO + (directory ? '/tree/' : '/blob/') + encodeURIComponent(GH_REF) + '/' + relative + (fragment ? '#' + fragment : line ? '#L' + line : ''));
      a.title = 'Open source on GitHub';
    } else if (REPO_ROOT) {
      if (/\.(?:py|md)$/.test(relative) && (!fragment || line)) {
        a.setAttribute('href', 'vscode://file' + REPO_ROOT + '/' + relative + (line ? ':' + line : ''));
        a.title = 'Open source in VS Code';
      } else {
        a.setAttribute('href', encodeURI('file://' + REPO_ROOT + '/' + relative) + (fragment ? '#' + fragment : ''));
        a.title = 'Open local source';
      }
    }
  });
  if (!HOSTED && REPO_ROOT) document.querySelectorAll('[data-local-src], [data-local-poster]').forEach(function(media){
    ['src','poster'].forEach(function(attr){
      var path = media.getAttribute('data-local-' + attr);
      if (path) media.setAttribute(attr, encodeURI('file://' + REPO_ROOT + '/' + path));
    });
  });
})();

// A record page may offer its Markdown source to the clipboard (`copy_raw` on
// its [[source_pages]] table). The text is in the page, so nothing is fetched.
(function(){
  var button = document.querySelector('[data-copy-raw]');
  var held = document.querySelector('script[data-raw-source]');
  if (!button || !held) return;
  var label = button.textContent, timer = 0;
  function say(text){
    button.textContent = text;
    clearTimeout(timer);
    timer = setTimeout(function(){ button.textContent = label; }, 1800);
  }
  function byHand(text){
    // For a page opened from disk, where the clipboard interface is not offered.
    var area = document.createElement('textarea');
    area.value = text; area.setAttribute('readonly', ''); area.style.position = 'fixed'; area.style.opacity = '0';
    document.body.appendChild(area); area.select();
    var done = false;
    try { done = document.execCommand('copy'); } catch (e) {}
    area.remove(); button.focus();
    say(done ? 'Copied' : 'Copy failed');
  }
  button.addEventListener('click', function(){
    var text = '';
    try { text = JSON.parse(held.textContent); } catch (e) { say('Copy failed'); return; }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function(){ say('Copied'); }, function(){ byHand(text); });
    } else byHand(text);
  });
})();
