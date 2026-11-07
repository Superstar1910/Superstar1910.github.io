#!/usr/bin/env python3
"""Import an approved local image into the Legesi.xyz visual catalogue.

Run from a checked-out site repository in Codex or a local Git workspace:
 python scripts/import_visual.py --source /path/to/approved.png --slug coffee-bean-economics --title "Who Captures the Economics of a Coffee Bean?" --project coffee-pricing-engine --caption "Illustrative economics; gross café sales are not profit." --related-url /writing/who-captures-the-economics-of-a-coffee-bean/

The script writes real image bytes, catalogue metadata, and optionally an article image.
Commit and open a PR using the authenticated git/gh workflow; do not write directly to main.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "static/data/visual-library.json"
ALLOWED = {".png": bytes.fromhex("89504e470d0a1a0a"), ".jpg": bytes.fromhex("ffd8ff"), ".jpeg": bytes.fromhex("ffd8ff"), ".webp": b"RIFF"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--caption", required=True)
    p.add_argument("--related-url", default="/visuals/")
    p.add_argument("--alt", default=None)
    args = p.parse_args()
    for field in (args.slug, args.project):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", field):
            p.error("slug and project must be lowercase kebab-case")
    src = args.source.resolve(strict=True)
    if not src.is_file() or src.is_symlink():
        p.error("source must be a regular file, not a symlink")
    suffix = src.suffix.lower()
    if suffix not in ALLOWED:
        p.error("Only PNG, JPEG and WebP images are accepted")
    raw = src.read_bytes()
    if len(raw) > 12 * 1024 * 1024 or len(raw) < 100:
        p.error("Image must be between 100 bytes and 12 MiB")
    if not raw.startswith(ALLOWED[suffix]) or (suffix == ".webp" and raw[8:12] != b"WEBP"):
        p.error("Invalid image signature")
    digest = hashlib.sha256(raw).hexdigest()
    dest = ROOT / "static/img/visuals" / args.project / (args.slug + suffix)
    if dest.exists():
        p.error(f"Destination already exists: {dest}")
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0.0":
        p.error("Unsupported catalogue schema")
    webpath = "/" + dest.relative_to(ROOT).as_posix()
    if any(a.get("file") == webpath or a.get("source_sha256") == digest for a in data["assets"]):
        p.error("Asset or content already catalogued")
    asset_id = "LVC-" + digest[:12].upper()
    if any(a.get("id") == asset_id for a in data["assets"]):
        p.error("Asset ID collision")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    data["assets"].append({
        "id": asset_id, "title": args.title, "file": webpath,
        "thumbnail": webpath, "alt": args.alt or args.title,
        "category": "research", "caption": args.caption,
        "project": args.project, "source_type": "chatgpt-approved-original",
        "source_reference": src.name,
        "tags": ["coffee", "research", "value-chain"] if args.project == "coffee-pricing-engine" else ["research"],
        "version": "user-approved-final", "approval_status": "approved",
        "rights_status": "user-approved-for-publication",
        "related_url": args.related_url,
        "description": args.caption, "source_sha256": digest
    })
    CATALOGUE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Imported {webpath}; catalogue ID {asset_id}")
    print("Next: inspect image and text, run python scripts/validate_visual_library.py, site checks, then commit and open PR.")
if __name__ == "__main__":
    main()
