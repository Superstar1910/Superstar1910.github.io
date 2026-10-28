#!/usr/bin/env python3
"""Enforce canonical URL contracts and direct compatibility redirects."""
import json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,urljoin
from xml.etree import ElementTree as ET
from url_routes import redirects,file_for
R=Path(__file__).resolve().parents[1];BASE='https://legesi.xyz';errors=[]
class Page(HTMLParser):
    def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
pages=json.loads((R/'static/data/site-pages.json').read_text());aliases=redirects(R);canonical={p['url'] for p in pages}
for p in pages:
    u=p['url'];tags=Page((R/p['path']).read_text()).tags
    if u!='/404.html' and not re.fullmatch(r'/(?:[a-z0-9]+(?:-[a-z0-9]+)*/)*',u):errors.append(f'Non-uniform canonical URL: {u}')
    if u.startswith(('/projects/','/research/','/mtn-uganda-stock-coverage/')):errors.append(f'Legacy content route: {u}')
    for kind,attr,expected in [('link','rel','canonical'),('meta','property','og:url')]:
        values=[a.get('href' if kind=='link' else 'content') for t,a in tags if t==kind and a.get(attr)==expected]
        if values!=[BASE+u]:errors.append(f'{u}: {expected} mismatch {values}')
    for tag,a in tags:
        if tag!='a' or not a.get('href'):continue
        if '&amp;' in a['href']:errors.append(f'{u}: double-escaped URL {a["href"]}')
        if a['href'].startswith('https://github.com/Superstar1910/work/'):errors.append(f'{u}: invalid source repository URL')
        target=urlsplit(urljoin(BASE+u,a['href']))
        if target.netloc!='legesi.xyz':continue
        if target.path in aliases:errors.append(f'{u}: links through alias {a["href"]}')
        if target.path.endswith('/index.html'):errors.append(f'{u}: explicit index link {a["href"]}')
for old,new in aliases.items():
    target=urlsplit(new).path
    if target not in canonical:errors.append(f'{old}: destination not canonical: {new}')
    if new in aliases:errors.append(f'{old}: redirect chain to {new}')
    p=file_for(R,old)
    if not p.exists():errors.append(f'{old}: redirect missing');continue
    tags=Page(p.read_text()).tags
    if not any(t=='link' and a.get('rel')=='canonical' and a.get('href')==BASE+new for t,a in tags):errors.append(f'{old}: redirect canonical mismatch')
    if not any(t=='meta' and a.get('http-equiv')=='refresh' and a.get('content')=='0;url='+new for t,a in tags):errors.append(f'{old}: no no-JS redirect')
    if not any(t=='script' and a.get('src')=='/static/js/url-redirect.js' for t,a in tags):errors.append(f'{old}: state-preserving redirect missing')
sitemap={e.text for e in ET.parse(R/'sitemap.xml').iter() if e.tag.endswith('loc')}
if sitemap!={BASE+u for u in canonical if u!='/404.html'}:errors.append('Sitemap does not exactly match canonical inventory')
for e in errors:print('ERROR:',e)
print(f'URL contracts: {len(canonical)} canonical pages, {len(aliases)} legacy URL forms; {len(errors)} problems.')
if errors:raise SystemExit(1)
