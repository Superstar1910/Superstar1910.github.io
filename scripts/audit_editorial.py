#!/usr/bin/env python3
"""Validate editorial/contact contracts beyond basic link availability."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
import json,re
R=Path(__file__).resolve().parents[1]
pages=json.loads((R/'static/data/site-pages.json').read_text());articles=json.loads((R/'static/data/articles.json').read_text())['articles'];projects=json.loads((R/'static/data/public-projects.json').read_text())['projects']
for p in pages:
    text=(R/p['path']).read_text()
    assert 'klegesi@oakstonecapital.co' not in text.lower(),p['url']+' exposed contact address'
    assert all(u.lower().startswith('mailto:sklegesi@gmail.com') for u in re.findall(r'href="(mailto:[^"]+)"',text,re.I)),p['url']+' unexpected email recipient'
    header=text.split('<!-- site-header:start -->')[1].split('<!-- site-header:end -->')[0]
    assert 'href="/#connect"' in header,p['url']+' contact navigation'
writing=(R/'writing/index.html').read_text()
assert 'LEARNING COLLECTION' not in writing and 'ORIGINAL SERIES' not in writing
assert writing.index('id="article-search"')<writing.index('Other publishing platforms')
assert 'id="article-platform"' in writing
for p in projects:
    u=urlsplit(p['viewUrl']);assert u.netloc in ('','legesi.xyz') and u.path.startswith('/work/'),p['name']+' must lead to its own landing page'
    text=(R/u.path.strip('/')/'index.html').read_text();assert '<h1' in text and 'http-equiv="refresh"' not in text,p['name']+' missing landing page'
financial=(R/'work/financial-literacy/index.html').read_text()
crumb=financial.split('<!-- site-breadcrumb:start -->')[1].split('<!-- site-breadcrumb:end -->')[0]
assert 'href="/work/"' in crumb and 'href="/writing/"' not in crumb
feed=ET.parse(R/'writing/feed.xml').getroot();items=feed.findall('./channel/item')
assert len(items)==sum(a.get('native',False) for a in articles)
for i in items:
    body=i.findtext('{http://purl.org/rss/1.0/modules/content/}encoded') or ''
    assert len(body)>100,'RSS item missing full text: '+i.findtext('title')
    assert not re.search(r'(?:href|src)="/(?!/)',body),'RSS contains relative URL'
assert any(a['datePublished']<'2025-01-01' for a in articles),'Historical archive missing'
assert any(a.get('native') and a['platform']=='Medium' for a in articles)
assert all(not a.get('native') for a in articles if a['platform']=='LinkedIn'),'Unverified LinkedIn full-text claim'
css=(R/'static/css/site-shell.css').read_text();assert '#site-header{position:sticky;top:0;' in css
print(f'Editorial: {len(pages)} pages use email contact; {len(projects)} internal Work landing pages; {len(items)} full-text RSS items.')
