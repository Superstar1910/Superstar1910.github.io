# Repository contract
Production repository: `Superstar1910/Superstar1910.github.io`
Public gallery: https://legesi.xyz/visuals/
Asset directory: `static/img/visuals/<project-slug>/`
Catalogue: `static/data/visual-library.json`
Gallery: `visuals/index.html`
Validator: `scripts/validate_visual_library.py`
CI gate: `.github/workflows/site-quality.yml`
Candidate inventory: `docs/VISUAL_ASSET_INVENTORY.md`

Inspect current repository before editing. Preserve existing published paths and use only eligible approved originals. Catalogue schema presently includes: id, title, file, thumbnail, alt, category, caption, project, source_type, source_reference, tags, version, approval_status, rights_status, related_url, description. Respect current category vocabulary; if changed, update validator and gallery together. Ensure unique IDs and paths; check assets and thumbnails exist. Do not place restricted images or confidential metadata in public repository or catalogue. Verify browser rendering after deployment. All stages need evidence.
