#!/usr/bin/env python3
"""Validate historical dates, provenance and publication metadata."""
import json
import pathlib
from datetime import date

ROOT=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"static/data/articles.json").read_text(encoding="utf-8"))
seen=set()
for a in data["articles"]:
    for key in ("slug","title","datePublished","originalUrl","url","platform","native"):
        assert key in a and a[key] not in (None,""), f"Missing {key}: {a.get('slug')}"
    assert a["slug"] not in seen, f"Duplicate slug: {a['slug']}"
    seen.add(a["slug"])
    published=date.fromisoformat(a["datePublished"])
    if a.get("dateAdded"):
        assert published <= date.fromisoformat(a["dateAdded"]), f"Import predates publication: {a['slug']}"
    if a.get("dateModified"):
        date.fromisoformat(a["dateModified"])
    if a.get("research"):
        assert a["research"].get("repository","").startswith("https://"), f"Invalid repository: {a['slug']}"
    if a["native"] and a["url"].startswith("/"):
        path=ROOT/a["url"].strip("/")/"index.html"
        assert path.is_file(), f"Missing native article: {path}"
print(f"Validated {len(seen)} article records.")
