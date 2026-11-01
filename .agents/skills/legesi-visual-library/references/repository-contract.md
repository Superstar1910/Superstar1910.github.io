# Repository contract

**Canonical public repository:** `Superstar1910/Superstar1910.github.io`
**Live gallery:** https://legesi.xyz/visuals/
**Public assets:** `static/img/visuals/<project-slug>/`
**Public catalogue:** `static/data/visual-library.json`
**Gallery:** `visuals/index.html`
**Validator:** `scripts/validate_visual_library.py`
**Site CI:** `.github/workflows/site-quality.yml`
**Intake workflow:** `.github/workflows/import-visual-library-bundle.yml`
**Importer:** `scripts/import_visual_library_bundle.py`
**Candidate summaries:** `docs/VISUAL_ASSET_INVENTORY.md`

**Private archival destination:** use only an existing confirmed private repository and a non-deployable directory, with no public GitHub Pages deployment or public image URL. Confirm privacy and access each run; do not assume a private branch inside the public repository is private.

Inspect current schema before editing. Public entries need ID, title, file, thumbnail, alt, category, caption, project, tags, source reference, version, rights and approval status. Preserve legacy paths/IDs, respect category vocabulary and update validator/gallery together if it changes.

No private source names, unreleased valuation figures or confidential transaction details in public metadata. Build the site only from approved public assets. Git history can preserve publicly deleted bytes; document residual exposure.
