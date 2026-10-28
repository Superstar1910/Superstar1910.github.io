#!/usr/bin/env python3
"""Check actual generated page navigation, metadata, JSON links and discovery."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree
R=Path(__file__).resolve().parents[1];errors=[]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
pages=json.loads((R/'static/data/site-pages.json').read_text())
projects=json.loads((R/'static/data/public-projects.json').read_text())['projects']
articles=json.loads((R/'static/data/articles.json').read_text())['articles']
allowed=set() # All public work pages are now published in this repository.
def check_url(value,source):
 u=urlsplit(value)
 if u.netloc and u.netloc!='legesi.xyz':return
 if u.scheme and u.scheme not in ('https','http'):return
 if not u.path.startswith('/'):return
 if any(u.path.startswith(x) for x in allowed):return
 p=R/unquote(u.path).lstrip('/')
 if u.path.endswith('/'):p=p/'index.html'
 if not p.is_file():errors.append(f'{source}: missing same-origin target {value}')
for page in pages:
 s=(R/page['path']).read_text();p=Page();p.feed(s)
 for ident in ('site-header','site-footer','main'):
  if sum(a.get('id')==ident for t,a in p.tags)!=1:errors.append(f'{page["path"]}: requires exactly one {ident}')
 if s.count('aria-label="Main navigation"')!=1:errors.append(f'{page["path"]}: primary navigation missing/duplicated')
 header=s.split('<!-- site-header:start -->')[1].split('<!-- site-header:end -->')[0]
 labels=re.findall(r'<a\b[^>]*>([^<]+)</a>',header)
 if labels!=['Skip to content','LEGESI.XYZ','About','Work','Writing','Connect']:errors.append(f'{page["path"]}: inconsistent primary labels {labels}')
 for url in ['/privacy/','/terms/','/disclaimer/','https://x.com/sklegesi','/sitemap/']:
  footer=s.split('<!-- site-footer:start -->')[1].split('<!-- site-footer:end -->')[0]
  if f'href="{url}"' not in footer:errors.append(f'{page["path"]}: missing footer {url}')
 if page['url']!='/' and 'aria-label="Breadcrumb"' not in s:errors.append(f'{page["path"]}: no breadcrumb')
 if sum(t=='h1' for t,a in p.tags)!=1:errors.append(f'{page["path"]}: must have one H1')
 if f'href="https://legesi.xyz{page["url"]}"' not in s:errors.append(f'{page["path"]}: canonical missing')
 if 'property="og:image"' not in s:errors.append(f'{page["path"]}: no share image')
 for t,a in p.tags:
  if t in ('a','link','img','script'):
   for k in ('href','src'):
    if a.get(k):check_url(a[k],page['path'])
for p in projects:
 for key in ('title','category','lifecycleStatus','reviewStatus','researchLead','nextReviewTrigger'):
  if not p.get(key):errors.append(f'{p["name"]}: no {key}')
 check_url(p['viewUrl'],p['name'])
 for u in p.get('methodologyUrls',[]):check_url(u,p['name'])
for a in articles:check_url(a['url'],a['slug'])
for path,expected in [('work/index.html',len(projects)),('writing/index.html',len(articles))]:
 s=(R/path).read_text();n=s.count('data-category=') if path.startswith('work') else s.count('data-search=')
 if n!=expected:errors.append(f'{path}: static entries {n} != register {expected}')
urls={x.text for x in ElementTree.parse(R/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
for p in pages:
 if p['url']!='/404.html' and 'https://legesi.xyz'+p['url'] not in urls:errors.append('Root sitemap missing '+p['url'])
for e in errors:print('ERROR:',e)
print(f'Coherence: {len(pages)} pages, {len(projects)} work entries, {len(articles)} publications; {len(errors)} problems.')
if errors:raise SystemExit(1)
