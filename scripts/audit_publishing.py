#!/usr/bin/env python3
"""Validate the deployed static site's native writing inventory and syndication.

Run from any directory: python scripts/audit_publishing.py
This is a deterministic repository audit, not a live HTTP availability check.
"""
import json
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://legesi.xyz"
REGISTER = ROOT / "static/data/articles.json"
REQUIRED = [ROOT / "index.html", ROOT / "CNAME", ROOT / ".nojekyll",
            ROOT / "writing/index.html", ROOT / "writing/feed.xml",
            ROOT / "writing/sitemap.xml"]
errors = []
for path in REQUIRED:
    if not path.is_file():
        errors.append(f"Missing site file: {path.relative_to(ROOT)}")
if (ROOT / "CNAME").is_file() and (ROOT / "CNAME").read_text().strip() != "legesi.xyz":
    errors.append("CNAME does not match legesi.xyz")

articles = json.loads(REGISTER.read_text(encoding="utf-8"))["articles"]
native = [a for a in articles if a.get("native") and a.get("url", "").startswith("/")]
expected_urls = {BASE + a["url"] for a in native}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonical = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href", ""))
        for key in ("href", "src"):
            if tag in ("a", "link", "script", "img") and attrs.get(key):
                self.links.append((tag, key, attrs[key]))

def local_path(url):
    u = urlsplit(url)
    if u.scheme or u.netloc or not u.path.startswith("/"):
        return None
    if u.path == "/":
        return ROOT / "index.html"
    path = ROOT / u.path.lstrip("/")
    if u.path.endswith("/"):
        return path / "index.html"
    return path

for a in native:
    url = a["url"]
    file = local_path(url)
    if file is None or not file.is_file():
        errors.append(f"Native article missing: {url}")
        continue
    parser = Links()
    parser.feed(file.read_text(encoding="utf-8"))
    if parser.canonical != [BASE + url]:
        errors.append(f"Canonical URL mismatch: {url}")
    for tag, key, link in parser.links:
        path = local_path(link)
        # Check only static assets; other internal navigation is audited separately.
        if path is not None and (link.startswith("/static/") or link.startswith("/writing/")):
            if not path.is_file():
                errors.append(f"Broken local {tag} {key} in {url}: {link}")
    try:
        date.fromisoformat(a["datePublished"])
    except (KeyError, ValueError):
        errors.append(f"Invalid publication date: {url}")

if (ROOT / "writing/feed.xml").is_file():
    rss = ET.parse(ROOT / "writing/feed.xml").getroot()
    feed_urls = {x.text for x in rss.findall("./channel/item/link")}
    if feed_urls != expected_urls:
        errors.append(f"RSS inventory mismatch: missing={len(expected_urls-feed_urls)}, extra={len(feed_urls-expected_urls)}")
if (ROOT / "writing/sitemap.xml").is_file():
    sitemap = ET.parse(ROOT / "writing/sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {x.text for x in sitemap.findall("./s:url/s:loc", ns)}
    if not expected_urls.issubset(sitemap_urls):
        errors.append(f"Sitemap missing {len(expected_urls-sitemap_urls)} native article URLs")

if errors:
    for err in errors:
        print("ERROR:", err)
    raise SystemExit(f"Publishing audit failed with {len(errors)} issue(s).")
print(f"Publishing audit passed: {len(native)} native pages, RSS and sitemap inventories match.")
