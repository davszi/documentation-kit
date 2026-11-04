// Former page URLs keep their query and deep link when forwarding.
(() => {
  const marker = document.querySelector('[data-page-redirect]');
  if (!marker) return;
  const target = new URL(marker.dataset.pageRedirect, location.href);
  target.search = location.search;
  target.hash = location.hash;
  const link = marker.querySelector('a');
  if (link) link.href = target.href;
  location.replace(target.href);
})();
