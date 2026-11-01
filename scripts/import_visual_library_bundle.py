#!/usr/bin/env python3
"""Import the verified Legesi Visual Library ZIP into a local site checkout.

Run from repository root: python scripts/import_visual_library_bundle.py path/to/bundle.zip
This command does NOT push, merge or deploy.
"""
import argparse
import json
import os
import tempfile
import zipfile
from pathlib import Path
from shutil import copyfileobj

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "static/data/visual-library.json"
REQUIRED = {"id", "title", "file", "thumbnail", "alt", "category", "caption",
            "project", "source_type", "source_reference", "tags", "version",
            "approval_status", "rights_status", "related_url", "description"}

def checked_path(s):
    if not isinstance(s, str) or not s.startswith("/static/img/visuals/"):
        raise ValueError(f"Unsafe gallery path: {s!r}")
    p = Path(s.lstrip("/"))
    if ".." in p.parts or p.suffix.lower() not in {".webp", ".png", ".jpg", ".jpeg", ".svg"}:
        raise ValueError(f"Unsafe path/extension: {s!r}")
    target = (ROOT / p).resolve()
    if not target.is_relative_to(ROOT.resolve()):
        raise ValueError("Path escapes repository")
    return p, target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    with zipfile.ZipFile(args.zip_path) as z:
        if z.testzip() is not None:
            raise ValueError("Invalid ZIP CRC")
        members = z.infolist()
        names = [i.filename for i in members]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP member names")
        if any(i.file_size > 30 * 1024 * 1024 for i in members) or sum(i.file_size for i in members) > 200 * 1024 * 1024:
            raise ValueError("ZIP extraction size cap exceeded")
        if any(i.filename.startswith("/") or ".." in Path(i.filename).parts or chr(92) in i.filename for i in members):
            raise ValueError("Unsafe ZIP member path")
        proposed = json.loads(z.read("candidate_catalogue_entries.json"))
        base = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        if not isinstance(proposed, list):
            raise ValueError("Expected a list of candidate entries")
        existing_ids = {v["id"]: v for v in base["assets"]}
        existing_paths = {v["file"]: v for v in base["assets"]}
        seen_ids, seen_paths, to_add = set(), set(), []
        for a in proposed:
            if REQUIRED - a.keys():
                raise ValueError(f"Missing required metadata in {a.get('id')}: {REQUIRED - a.keys()}")
            if a["approval_status"] != "approved":
                raise ValueError(f"Not approved: {a['id']}")
            if not isinstance(a["rights_status"], str) or not a["rights_status"].strip() or any(word in a["rights_status"].lower() for word in ("pending", "verify", "uncleared", "restricted")):
                raise ValueError(f"Rights not cleared: {a['id']}")
            if a["id"] in seen_ids or a["file"] in seen_paths:
                raise ValueError(f"Duplicate in bundle: {a['id']}")
            seen_ids.add(a["id"]); seen_paths.add(a["file"])
            if a["id"] in existing_ids:
                if existing_ids[a["id"]]["file"] != a["file"]:
                    raise ValueError(f"Existing ID collides: {a['id']}")
                continue
            if a["file"] in existing_paths:
                raise ValueError(f"Existing file collides: {a['file']}")
            for key in ("file", "thumbnail"):
                path, dest = checked_path(a[key])
                if path.as_posix() not in names:
                    raise FileNotFoundError(f"Bundle omits {path}")
                if dest.exists():
                    raise FileExistsError(f"Refusing to overwrite existing image: {dest}")
            to_add.append(a)
        if args.dry_run:
            print(f"Dry run OK: {len(to_add)} new assets, {len(proposed)-len(to_add)} already catalogued")
            return
        for a in to_add:
            for key in ("file", "thumbnail"):
                p, dest = checked_path(a[key])
                dest.parent.mkdir(parents=True, exist_ok=True)
                with z.open(p.as_posix()) as src, open(dest, "xb") as dst:
                    copyfileobj(src, dst)
            base["assets"].append(a)
        if to_add:
            with tempfile.NamedTemporaryFile("w", dir=CATALOGUE.parent, delete=False, encoding="utf-8") as tmp:
                json.dump(base, tmp, ensure_ascii=False, indent=2)
                tmp.write("\n")
                name = tmp.name
            os.replace(name, CATALOGUE)
        print(f"Imported {len(to_add)} assets. Run the site validator before committing.")

if __name__ == "__main__":
    main()
