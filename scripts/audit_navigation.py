#!/usr/bin/env python3
"""Audit internal site navigation, including path and anchor targets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):self.ids.add(a["id"])
        if tag=="a" and a.get("name"):self.ids.add(a["name"])
        if tag in ("a","link","script","img") and (a.get("href") or a.get("src")):
            self.links.append((tag,a.get("href") or a.get("src")))
pages={}
for file in ROOT.rglob("*.html"):
    if any(part.startswith(".") or part in ("node_modules","_site") for part in file.relative_to(ROOT).parts):continue
    p=Page();p.feed(file.read_text(encoding="utf-8"));pages[file.resolve()]=p
errors=[];checked=0
for file,page in pages.items():
    for tag,href in page.links:
        u=urlsplit(href)
        if u.scheme or u.netloc or href.startswith("//") or u.path.startswith(("mailto:","tel:","data:")):continue
        if not u.path and not u.fragment:continue
        if u.path.startswith("/"):target=ROOT/unquote(u.path).lstrip("/")
        else:target=file.parent/unquote(u.path)
        if u.path.endswith("/") or target.is_dir():target=target/"index.html"
        target=target.resolve()
        if not target.is_file():
            errors.append(f"{file.relative_to(ROOT)}: missing {href}")
            continue
        checked+=1
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f"{file.relative_to(ROOT)}: missing anchor {href}")
for e in errors:print("ERROR:",e)
print(f"Checked {len(pages)} HTML pages and {checked} local links; {len(errors)} problems.")
if errors:raise SystemExit(1)
