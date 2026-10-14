#!/usr/bin/env python3
"""Safely merge an author-controlled Substack migration ZIP into this checkout.

Usage: python scripts/import_substack_archive.py /path/to/legesi_substack_migration.zip
Review git diff, images, dates, provenance, then commit. No automatic publication.
"""
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"static/data/articles.json"

def main(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        incoming=json.loads(z.read("migration-records.json"))["articles"]
        existing=json.loads(REG.read_text(encoding="utf-8"))
        articles=existing["articles"]
        by_url={a["originalUrl"].rstrip("/"):a for a in articles}
        by_slug={a["slug"]:a for a in articles}
        added=updated=0
        for a in incoming:
            url=a["originalUrl"].rstrip("/")
            slug=a["slug"]
            path=f"writing/{slug}/index.html"
            if path not in z.namelist():
                raise ValueError(f"Missing HTML: {path}")
            dest=ROOT/path
            if dest.exists():
                raise ValueError(f"Refusing to overwrite existing native page: {dest}")
            target=by_url.get(url)
            if target is None and slug in by_slug:
                raise ValueError(f"Slug collision requiring manual review: {slug}")
            if target:
                if target.get("native") and target.get("url")!=a["url"]:
                    raise ValueError(f"Existing native publication requires manual reconciliation: {slug}")
                target.update({k:a[k] for k in ("title","datePublished","type","platform","originalUrl","url","summary","native")})
                if a.get("research") and not target.get("research"):
                    target["research"]=a["research"]
                target["dateAdded"]=date.today().isoformat()
                updated+=1
            else:
                a["dateAdded"]=date.today().isoformat()
                articles.append(a)
                by_url[url]=a
                by_slug[slug]=a
                added+=1
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(z.read(path))
        REG.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"Prepared {added} new and {updated} reconciled entries; {len(incoming)} HTML pages. Review before commit.")

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("Usage: import_substack_archive.py ARCHIVE.zip")
    main(sys.argv[1])
