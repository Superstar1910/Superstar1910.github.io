(async function () {
  const list = document.getElementById('article-list');
  const yearFilter = document.getElementById('article-filter');
  const topicFilter = document.getElementById('article-topic');
  const search = document.getElementById('article-search');
  const count = document.getElementById('article-count');
  if (!list || !yearFilter || !search) return;

  const formatDate = date => date
    ? new Date(date + 'T12:00:00Z').toLocaleDateString('en-GB', {
        day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC'
      })
    : 'Date unverified';

  try {
    const response = await fetch('/static/data/articles.json', {cache: 'no-cache'});
    if (!response.ok) throw new Error('Article register unavailable');
    const {articles} = await response.json();
    const years = [...new Set(articles.map(a => a.datePublished?.slice(0, 4)).filter(Boolean))].sort().reverse();
    const topics = [...new Set(articles.flatMap(a => a.tags || []))].sort();
    for (const year of years) yearFilter.add(new Option(year, year));
    if (topicFilter) for (const topic of topics) topicFilter.add(new Option(topic, topic));

    function render() {
      const query = search.value.trim().toLocaleLowerCase();
      const year = yearFilter.value;
      const topic = topicFilter?.value || '';
      const matches = articles.filter(a =>
        (!year || a.datePublished?.startsWith(year)) &&
        (!topic || (a.tags || []).includes(topic)) &&
        (!query || [a.title, a.summary, a.type, a.platform, ...(a.tags || [])]
          .join(' ').toLocaleLowerCase().includes(query))
      ).sort((a, b) => (b.datePublished || '').localeCompare(a.datePublished || '') ||
        a.title.localeCompare(b.title));

      list.replaceChildren();
      if (count) count.textContent = `Showing ${matches.length} of ${articles.length} publications`;
      if (!matches.length) {
        const p = document.createElement('p');
        p.textContent = 'No matching articles. Try another topic or clear your search.';
        list.append(p);
        return;
      }
      for (const a of matches) {
        const item = document.createElement('article');
        item.className = 'archive-item';
        const meta = document.createElement('p');
        meta.className = 'eyebrow';
        meta.textContent = [formatDate(a.datePublished), a.type,
          a.native ? 'Legesi.xyz' : 'Originally on ' + a.platform].join(' · ');
        const heading = document.createElement('h2');
        const link = document.createElement('a');
        link.href = a.url;
        link.textContent = a.title;
        heading.append(link);
        const description = document.createElement('p');
        description.textContent = a.summary || '';
        const tagRow = document.createElement('div');
        tagRow.className = 'article-tags';
        tagRow.setAttribute('aria-label', 'Article topics');
        for (const tag of a.tags || []) {
          const chip = document.createElement('button');
          chip.type = 'button';
          chip.className = 'article-tag';
          chip.textContent = tag;
          chip.title = 'Filter by ' + tag;
          chip.addEventListener('click', () => {
            if (topicFilter) {topicFilter.value = tag; render(); topicFilter.focus();}
            else {search.value = tag; render(); search.focus();}
          });
          tagRow.append(chip);
        }
        const foot = document.createElement('p');
        const source = document.createElement('a');
        source.href = a.originalUrl;
        source.textContent = 'Original source ↗';
        foot.append(source);
        if (a.research?.repository) {
          const research = document.createElement('a');
          research.href = a.research.repository;
          research.textContent = 'Research repository ↗';
          foot.append(document.createTextNode(' · '), research);
          if (a.research.analysis) {
            const analysis = document.createElement('a');
            analysis.href = a.research.analysis;
            analysis.textContent = 'Underlying analysis ↗';
            foot.append(document.createTextNode(' · '), analysis);
          }
        }
        item.append(meta, heading, description, tagRow, foot);
        list.append(item);
      }
    }
    search.addEventListener('input', render);
    yearFilter.addEventListener('change', render);
    topicFilter?.addEventListener('change', render);
    document.getElementById('article-clear')?.addEventListener('click', () => {
      search.value = ''; yearFilter.value = '';
      if (topicFilter) topicFilter.value = '';
      render(); search.focus();
    });
    render();
  } catch (error) {
    list.textContent = 'The archive is temporarily unavailable. Please use the Substack or research links below.';
    if (count) count.textContent = '';
  }
})();
