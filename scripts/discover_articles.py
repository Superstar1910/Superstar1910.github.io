#!/usr/bin/env python3
"""Discover candidate Substack posts without changing published content."""
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
REGISTER=ROOT/"static/data/articles.json"
OUTPUT=ROOT/"data/article-import-candidates.json"
FEED="https://legesi.substack.com/feed"

def value(node, tag):
    item=node.find(tag)
    return (item.text or "").strip() if item is not None else ""

def main():
    existing=json.loads(REGISTER.read_text(encoding="utf-8"))["articles"]
    known={a.get("originalUrl","").rstrip("/") for a in existing}
    request=urllib.request.Request(FEED,headers={"User-Agent":"LegesiResearchArchive/1.0 (+https://legesi.xyz)"})
    with urllib.request.urlopen(request,timeout=25) as response:
        data=response.read(3_000_000)
    root=ET.fromstring(data)
    candidates=[]
    for item in root.findall(".//channel/item"):
        link=value(item,"link").split("?")[0].rstrip("/")
        if not link.startswith("https://legesi.substack.com/p/") or link in known:
            continue
        candidates.append({"title":value(item,"title"),"originalUrl":link,"datePublishedRaw":value(item,"pubDate"),"platform":"Substack","status":"candidate-needs-review","researchRepository":None})
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps({"generatedAt":datetime.now(timezone.utc).isoformat(),"source":FEED,"candidates":candidates},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Found {len(candidates)} new candidate(s); published article register unchanged.")

if __name__=="__main__":
    main()
