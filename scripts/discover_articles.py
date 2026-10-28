#!/usr/bin/env python3
"""Discover author-feed candidates for review; never auto-publish imported work."""
import json,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
SOURCES=[('Substack','https://legesi.substack.com/feed'),('Medium','https://medium.com/feed/@kennethlegesi')]
def main():
    articles=json.loads((R/'static/data/articles.json').read_text())['articles']
    known={a['originalUrl'].split('?')[0].rstrip('/') for a in articles}
    known.update(e['url'].split('?')[0].rstrip('/') for a in articles for e in a.get('syndications',[]))
    candidates=[];statuses=[]
    for platform,url in SOURCES:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'LegesiResearchArchive/1.0 (+https://legesi.xyz)'})
            with urllib.request.urlopen(req,timeout=25) as response:raw=response.read(3_000_000)
            root=ET.fromstring(raw)
            if root.tag!='rss' or root.find('channel') is None:raise ValueError('Response is not an RSS feed')
            items=root.findall('./channel/item')
            for item in items:
                link=(item.findtext('link') or '').split('?')[0].rstrip('/')
                if not link.startswith('https://') or link in known:continue
                candidates.append({'title':item.findtext('title'),'originalUrl':link,'datePublishedRaw':item.findtext('pubDate'),'platform':platform,'status':'candidate-needs-review'})
            statuses.append({'platform':platform,'feed':url,'status':'checked','feedItems':len(items),'completeArchive':False})
        except Exception as exc:statuses.append({'platform':platform,'feed':url,'status':'unavailable','error':str(exc),'completeArchive':False})
    output=R/'data/article-import-candidates.json';output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({'generatedAt':datetime.now(timezone.utc).isoformat(),'sources':statuses,'candidates':candidates,'note':'Feeds may expose only recent entries. LinkedIn requires a reviewed article list/export; no automatic native-content claim.'},indent=2)+'\n')
    print(f'{len(candidates)} review candidates; {sum(s["status"]=="unavailable" for s in statuses)} unavailable source(s). Published register unchanged.')
if __name__=='__main__':main()
