#!/usr/bin/env python3
"""Generate an RSS feed and writing sitemap from the approved article register.

Only articles whose full text is actually hosted on legesi.xyz are syndicated.
External links remain discoverable in the writing archive, not misrepresented
as locally published articles.
"""
import json
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://legesi.xyz"
articles = json.loads((ROOT / "static/data/articles.json").read_text(encoding="utf-8"))["articles"]
native = sorted((a for a in articles if a.get("native") and a.get("url","").startswith("/")),key=lambda a:a["datePublished"],reverse=True)

def save(element, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    ElementTree(element).write(path, encoding="utf-8", xml_declaration=True)

rss=Element("rss",version="2.0")
channel=SubElement(rss,"channel")
for k,v in (("title","Legesi.xyz — Writing and Research"),("link",BASE+"/writing/"),("description","Independent writing, research and analysis by Kenneth S. Legesi"),("language","en")):
    SubElement(channel,k).text=v
for a in native:
    item=SubElement(channel,"item")
    url=BASE+a["url"]
    for k,v in (("title",a["title"]),("link",url),("guid",url),("description",a.get("summary",""))):
        SubElement(item,k).text=v
    dt=datetime.combine(date.fromisoformat(a["datePublished"]),datetime.min.time(),tzinfo=timezone.utc)
    SubElement(item,"pubDate").text=format_datetime(dt)
save(rss,ROOT/"writing/feed.xml")

namespace="http://www.sitemaps.org/schemas/sitemap/0.9"
urlset=Element("urlset",xmlns=namespace)
for url,modified in [(BASE+"/writing/",None)]+[(BASE+a["url"],a.get("dateModified") or a.get("dateAdded") or a["datePublished"]) for a in native]:
    entry=SubElement(urlset,"url")
    SubElement(entry,"loc").text=url
    if modified:SubElement(entry,"lastmod").text=modified
save(urlset,ROOT/"writing/sitemap.xml")
print(f"Generated feed and sitemap for {len(native)} native articles.")
