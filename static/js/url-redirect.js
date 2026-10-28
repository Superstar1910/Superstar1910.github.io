/* Static-host compatibility redirects; destinations are authored in the route map. */
(() => {
  const link = document.getElementById('redirect-target');
  if (!link) return;
  const target = new URL(link.getAttribute('href'), location.origin);
  if (target.origin !== location.origin) return;
  if (location.search) target.search = location.search;
  if (location.hash) target.hash = location.hash;
  link.href = target.href;
  location.replace(target.href);
})();
