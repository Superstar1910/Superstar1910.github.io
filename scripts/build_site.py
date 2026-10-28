#!/usr/bin/env python3
"""Build shared static navigation and progressively enhanced directories in place."""
import html,json,re
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree.ElementTree import Element,SubElement,ElementTree
ROOT=Path(__file__).resolve().parents[1]
BASE='https://legesi.xyz'
ALIASES={'about.html','projects.html','writing.html','archive.html','work/index.html','connect/index.html','research/index.html'}
def esc(s):return html.escape(str(s or ''),quote=True)
def route(p):
 s=p.relative_to(ROOT).as_posix();return '/'+(s[:-10] if s.endswith('index.html') else s)
def files():return sorted(p for p in ROOT.rglob('*.html') if not any(x in p.parts for x in ('.git','_site','node_modules','templates')) and not p.relative_to(ROOT).as_posix().startswith('docs/') and p.relative_to(ROOT).as_posix() not in ALIASES)
def marked(text,name,content):
 pattern=rf'<!-- {name}:start -->.*?<!-- {name}:end -->';block=f'<!-- {name}:start -->{content}<!-- {name}:end -->'
 return re.sub(pattern,lambda m:block,text,flags=re.S) if re.search(pattern,text,re.S) else None
def directory(text,id,content):
 start=re.search(rf'<div\b[^>]*\bid=["\']{id}["\'][^>]*>',text)
 if not start:raise ValueError('Missing directory '+id)
 depth=1
 for m in re.finditer(r'</?div\b[^>]*>',text[start.end():]):
  depth+= -1 if m.group(0).startswith('</') else 1
  if depth==0:
   end=start.end()+m.start();return text[:start.end()]+content+text[end:]
 raise ValueError('Unclosed directory '+id)
def page(title,content):return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — Legesi.xyz</title><link rel="stylesheet" href="/static/css/brand-tokens.css"><link rel="stylesheet" href="/static/css/editorial.css"></head><body><main id="main" class="shell section"><h1>{esc(title)}</h1>{content}</main></body></html>'
projects=json.loads((ROOT/'static/data/public-projects.json').read_text())['projects']
articles=json.loads((ROOT/'static/data/articles.json').read_text())['articles']
titles={urlsplit(p['viewUrl']).path:p.get('title') or p['name'].replace('_',' ').replace('-',' ').title() for p in projects}
def project_markup(p):
 title=p.get('title') or p['name'].replace('_',' ').replace('-',' ').title()
 links=f'<a href="{esc(p["viewUrl"])}">{esc(p.get("viewLabel") or "Explore work →")}</a>'
 if p.get('url'):links+=f' <a href="{esc(p["url"])}" rel="noopener noreferrer" target="_blank">Source &amp; methodology ↗</a>'
 cutoff=f' · Data cutoff: {esc(p["dataCutoff"])}' if p.get('dataCutoff') else ''
 return f'<article class="project-item" data-category="{esc(p["category"])}"><span class="project-category">{esc(p["category"])}</span><h2>{esc(title)}</h2><p>{esc(p.get("description"))}</p><p class="work-status">{esc(p["lifecycleStatus"])} · {esc(p["reviewStatus"])}{cutoff}</p><div class="project-actions">{links}</div></article>'
f=ROOT/'projects/index.html';t=f.read_text();t=re.sub(r'<section class="panel".*?</section>','',t,count=1,flags=re.S)
t=t.replace('Projects &amp; experiments.','Work, research &amp; tools.').replace('Projects &amp; Experiments — Legesi.xyz','Work — Legesi.xyz');t=directory(t,'project-directory',''.join(project_markup(p) for p in projects))
if '<option>Research programmes</option>' not in t:t=t.replace('<option value="all">All projects</option>','<option value="all">All work</option><option>Research programmes</option>')
t=t.replace('PUBLIC PROJECT LIBRARY','PUBLIC WORK LIBRARY').replace('Explore by theme','Filter work by theme')
if 'id="project-count"' not in t:t=t.replace('<div id="project-directory"',f'<p id="project-count" role="status">{len(projects)} public work entries</p><noscript><p>All work is listed below. Enable JavaScript to filter by theme.</p></noscript><div id="project-directory"')
f.write_text(t)
def article_markup(a):
 tags=''.join(f'<button type="button" class="article-tag" data-topic="{esc(x)}">{esc(x)}</button>' for x in a.get('tags',[]));source=f'<a href="{esc(a["originalUrl"])}">Original source ↗</a>';repo=(a.get('research') or {}).get('repository')
 if repo:source+=f' · <a href="{esc(repo)}">Research repository ↗</a>'
 work=next((p for p in projects if p.get('url') and p['url']==repo),None)
 if not work and a['slug'] in ('economic-opportunity-is-not-investability','why-freedom-not-peace-prices-returns'):work=next(p for p in projects if p['name']=='africa-investability-index')
 if work:source+=f' · <a href="{esc(work["viewUrl"])}">Related work →</a>'
 kind='Research report' if a['url'].startswith('/research/') else 'Article';search=' '.join([a['title'],a.get('summary',''),a.get('type',''),a.get('platform',''),*a.get('tags',[])])
 return f'<article class="archive-item" data-search="{esc(search.lower())}" data-year="{esc(a.get("datePublished","")[:4])}" data-topics="{esc(json.dumps(a.get("tags",[])))}"><p class="eyebrow">{esc(a.get("datePublished"))} · {kind}</p><h2><a href="{esc(a["url"])}">{esc(a["title"])}</a></h2><p>{esc(a.get("summary"))}</p><div class="article-tags" aria-label="Article topics">{tags}</div><p>{source}</p></article>'
f=ROOT/'writing/index.html';t=f.read_text();ordered=sorted(articles,key=lambda a:(a.get('datePublished',''),a['title']),reverse=True);t=directory(t,'article-list',''.join(article_markup(a) for a in ordered))
t=t.replace('class="archive-count" aria-live="polite"></p>',f'class="archive-count" aria-live="polite">{len(articles)} publications</p>')
if '<noscript>' not in t:t=t.replace('<div class="archive-controls">','<noscript><p>All publications are listed below. Enable JavaScript to search, filter or show smaller batches.</p></noscript><div class="archive-controls">')
if 'id="article-more"' not in t:t=t.replace('</section><h2>Other publishing platforms','<button type="button" id="article-more" class="archive-clear" hidden>Show more publications</button></section><h2>Other publishing platforms')
f.write_text(t)
for name,target in [('work/index.html','/projects/'),('connect/index.html','/#connect'),('research/index.html','/projects/'),('archive.html','/writing/')]:
 p=ROOT/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Page moved — Legesi.xyz</title><link rel="canonical" href="{BASE+target}"><meta http-equiv="refresh" content="0;url={target}"></head><body><p>This page has moved. <a href="{target}">Continue to Legesi.xyz →</a></p></body></html>')
header=(ROOT/'templates/header.html').read_text().strip();footer=(ROOT/'templates/footer.html').read_text().strip()
def label(path):return titles.get(path) or {'/':'Home','/about/':'About','/projects/':'Work','/writing/':'Writing','/financial-literacy/':'Financial Literacy & Investing','/financial-literacy/emergency-fund/':'Emergency Fund Planner','/privacy/':'Privacy','/terms/':'Terms','/disclaimer/':'Investment Disclaimer','/sitemap/':'Site map'}.get(path)
def breadcrumbs(url,title):
 chain=[('Home','/')]
 if url=='/':return ''
 if url.startswith('/writing/') and url!='/writing/':chain.append(('Writing','/writing/'))
 elif url.startswith('/financial-literacy/'):
  chain.append(('Writing','/writing/'))
  if url!='/financial-literacy/':chain.append(('Financial Literacy','/financial-literacy/'))
 elif url.startswith(('/projects/','/research/')) and url!='/projects/':
  chain.append(('Work','/projects/'));root=next((u for u in titles if url.startswith(u) and url!=u),None)
  if root:chain.append((titles[root],root))
  if '/dashboard/' in url and not url.endswith('/dashboard/'):chain.append(('Dashboard',url.rsplit('/',1)[0]+'/'))
 return '<nav class="site-breadcrumbs shell" aria-label="Breadcrumb"><ol>'+''.join(f'<li><a href="{u}">{esc(n)}</a></li>' for n,u in chain)+f'<li aria-current="page">{esc(title)}</li></ol></nav>'
content='<p>Find the public pages, research programmes and tools.</p><h2>Main pages</h2><ul>'+''.join(f'<li><a href="{u}">{n}</a></li>' for n,u in [('Home','/'),('About','/about/'),('Work','/projects/'),('Writing','/writing/'),('Financial Literacy & Investing','/financial-literacy/'),('Emergency Fund Planner','/financial-literacy/emergency-fund/'),('Connect','/#connect')])+'</ul><h2>Work and research programmes</h2><ul>'+''.join(f'<li><a href="{esc(p["viewUrl"])}">{esc(p.get("title") or p["name"])}</a></li>' for p in projects)+'</ul><h2>Publications</h2><ul>'+''.join(f'<li><a href="{esc(a["url"])}">{esc(a["title"])}</a></li>' for a in ordered)+'</ul>'
(ROOT/'sitemap').mkdir(exist_ok=True);(ROOT/'sitemap/index.html').write_text(page('Site map',content));(ROOT/'404.html').write_text(page('Page not found','<p>The address may have changed. Use the <a href="/sitemap/">site map</a>, <a href="/projects/">work directory</a> or <a href="/writing/">writing archive</a> to find what you need.</p>'))
manifest=[]
for f in files():
 t=f.read_text();url=route(f);title=html.unescape(re.sub('<[^>]*>','',re.search(r'<title>(.*?)</title>',t,re.S).group(1))).split(' — ')[0].split(' | ')[0]
 if not re.search(r'<head\b',t):
  t=re.sub(r'(<html\b[^>]*>)',r'\1<head>',t,count=1);start=re.search(r'<(?:body|main|header)\b',t)
  if start:t=t[:start.start()]+'</head>'+t[start.start():]
 if not re.search(r'<body\b',t):t=t.replace('</head>','</head><body>',1);t=t.replace('</html>','</body></html>')
 if url.startswith('/writing/') and url!='/writing/':
  seen=[False]
  def heading(m):
   if not seen[0]:seen[0]=True;return m.group(0)
   return m.group(0).replace('<h1','<h2',1).replace('</h1>','</h2>')
  t=re.sub(r'<h1\b[^>]*>.*?</h1>',heading,t,flags=re.S)
 main=re.search(r'<main\b[^>]*>',t)
 if main:
  old=re.search(r'\bid=["\']([^"\']+)["\']',main[0])
  if old and old[1]!='main':
   opening=re.sub(r'\bid=["\'][^"\']+["\']','id="main"',main[0]);t=t[:main.start()]+opening+f'<span id="{esc(old[1])}"></span>'+t[main.end():]
  elif not old:t=t[:main.start()]+main[0].replace('<main','<main id="main"',1)+t[main.end():]
 t=re.sub(r'<a\b[^>]*class=["\']skip["\'][^>]*>.*?</a>','',t,flags=re.S)
 h=header;active='/projects/' if url.startswith(('/research/','/projects/')) else '/writing/' if url.startswith(('/writing/','/financial-literacy/')) else '/about/' if url=='/about/' else None
 if active:h=h.replace(f'href="{active}"',f'href="{active}" aria-current="page"')
 h='<a class="skip" href="#main">Skip to content</a>'+h;replaced=marked(t,'site-header',h)
 if replaced is None:
  t=re.sub(r'<header\b[^>]*class=["\'][^"\']*\bsite-header\b[^"\']*["\'][^>]*>.*?</header>','',t,flags=re.S);t=re.sub(r'(<body\b[^>]*>)',lambda m:m.group(1)+'<!-- site-header:start -->'+h+'<!-- site-header:end -->',t,count=1)
 else:t=replaced
 before,after=t.split('<!-- site-header:end -->',1)
 after=after.replace('aria-label="Main navigation"','aria-label="Page navigation"');t=before+'<!-- site-header:end -->'+after
 crumb=breadcrumbs(url,label(url) or title);replaced=marked(t,'site-breadcrumb',crumb)
 if replaced is None:t=t.replace('<!-- site-header:end -->','<!-- site-header:end --><!-- site-breadcrumb:start -->'+crumb+'<!-- site-breadcrumb:end -->',1)
 else:t=replaced
 replaced=marked(t,'site-footer',footer)
 if replaced is None:
  def old_footer(m):
   if 'footer shell' in m[1] or 'article-navigation' in m[1]:return ''
   return '<div class="project-disclosure">'+m[2]+'</div>'
  t=re.sub(r'<footer\b([^>]*)>(.*?)</footer>',old_footer,t,flags=re.S);t=t.replace('</body>','<!-- site-footer:start -->'+footer+'<!-- site-footer:end --></body>')
 else:t=replaced
 t=re.sub(r'(<a\b[^>]*href=["\'](?:/projects/|https://legesi.xyz/projects/)["\'][^>]*>)(← )?Projects(</a>)',lambda m:m[1]+(m[2] or '')+'Work'+m[3],t)
 for css in ['brand-tokens.css','site-shell.css']:
  if '/static/css/'+css not in t:t=t.replace('</head>',f'<link rel="stylesheet" href="/static/css/{css}"></head>')
 canonical=BASE+url
 if re.search(r'<link[^>]*rel=["\']canonical["\']',t):t=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',f'<link rel="canonical" href="{canonical}">',t)
 else:t=t.replace('</head>',f'<link rel="canonical" href="{canonical}"></head>')
 for key,value in [('og:title',title),('og:url',canonical),('og:type','article' if url.startswith('/writing/') and url!='/writing/' else 'website'),('og:image',BASE+'/static/img/legesi-share.png'),('og:image:alt','Kenneth Legesi — Capital, systems and ideas worth building')]:
  if f'property="{key}"' not in t:t=t.replace('</head>',f'<meta property="{key}" content="{esc(value)}"></head>')
 if 'name="twitter:card"' not in t:t=t.replace('</head>','<meta name="twitter:card" content="summary_large_image"></head>')
 if 'name="referrer"' not in t:t=t.replace('</head>','<meta name="referrer" content="strict-origin-when-cross-origin"></head>')
 if 'http-equiv="Content-Security-Policy"' not in t:
  policy="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' https: data:; connect-src 'self'; font-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'self' mailto:"
  t=t.replace('</head>',f'<meta http-equiv="Content-Security-Policy" content="{esc(policy)}"></head>')
 if url=='/' and 'application/ld+json' not in t:
  person={'@context':'https://schema.org','@type':'Person','name':'Kenneth S. Legesi','url':BASE+'/','sameAs':['https://www.linkedin.com/in/kenneth-legesi','https://legesi.substack.com/','https://github.com/Superstar1910','https://x.com/sklegesi']}
  t=t.replace('</head>','<script type="application/ld+json">'+json.dumps(person)+'</script></head>')
 t=re.sub(r'\s+onerror="[^"]*"','',t)
 def image(m):
  s=m[0];src=re.search(r'\bsrc="([^"]+)"',s)
  if src and src[1].startswith('/static/'):
   p=ROOT/src[1].lstrip('/')
   if p.exists():
    try:
     from PIL import Image
     with Image.open(p) as im:w,h=im.size
     if not re.search(r'\bwidth=',s):s=s[:-1]+f' width="{w}" height="{h}">'
    except (ImportError,OSError):pass
  return s
 t=re.sub(r'<img\b[^>]*>',image,t)
 t=re.sub(r'(?<!<!-- table-scroll:start -->)(<table\b.*?</table>)',lambda m:'<div class="site-table-scroll" role="region" aria-label="Scrollable data table" tabindex="0"><!-- table-scroll:start -->'+m[1]+'<!-- table-scroll:end --></div>',t,flags=re.S)
 if url.startswith('/writing/') and url!='/writing/':
  a=next((a for a in articles if a['url']==url),None);repo=((a or {}).get('research') or {}).get('repository');work=next((p for p in projects if p.get('url') and p['url']==repo),None)
  if not work and url in ['/writing/economic-opportunity-is-not-investability/','/writing/why-freedom-not-peace-prices-returns/']:work=next(p for p in projects if p['name']=='africa-investability-index')
  if work and 'related-work:start' not in t:
   block=f'<aside class="related-work shell" aria-label="Related work"><p>Related research: <a href="{esc(work["viewUrl"])}">{esc(work.get("title") or work["name"])}</a>. <a href="/writing/">Back to all writing →</a></p></aside>';t=t.replace('</main>','<!-- related-work:start -->'+block+'<!-- related-work:end --></main>')
 work=next((p for p in projects if urlsplit(p['viewUrl']).path==url),None)
 if work:
  related=[a for a in articles if work.get('url') and (a.get('research') or {}).get('repository')==work['url']]
  if work['name']=='africa-investability-index':related=[a for a in articles if a['slug'] in ('economic-opportunity-is-not-investability','why-freedom-not-peace-prices-returns')]
  if related:
   links=''.join(f'<li><a href="{esc(a["url"])}">{esc(a["title"])}</a></li>' for a in related)
   block='<section class="related-publications"><h2>Related publications</h2><ul>'+links+'</ul><p><a href="/writing/">Browse all writing →</a></p></section>'
   replacement=marked(t,'related-publications',block)
   t=replacement if replacement else t.replace('</main>','<!-- related-publications:start -->'+block+'<!-- related-publications:end --></main>')
 f.write_text(t);manifest.append({'url':url,'title':label(url) or title,'path':f.relative_to(ROOT).as_posix()})
root=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for x in manifest:
 if x['url']=='/404.html':continue
 entry=SubElement(root,'url');SubElement(entry,'loc').text=BASE+x['url'];a=next((a for a in articles if a['url']==x['url']),None)
 if a:SubElement(entry,'lastmod').text=a.get('dateModified') or a['datePublished']
ElementTree(root).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True);(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://legesi.xyz/sitemap.xml\n');(ROOT/'static/data/site-pages.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(f'Built shared navigation for {len(manifest)} pages; {len(projects)} work entries; {len(articles)} publications.')
