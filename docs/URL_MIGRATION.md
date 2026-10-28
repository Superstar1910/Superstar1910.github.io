# Canonical URL migration — 28 October 2026

Public navigation is **About · Work · Writing · Connect**. Work is now published
at `/work/`; all project/research pages and their tools share
`/work/<lowercase-hyphenated-slug>/<optional-child>/`. Writing and learning URLs
are unchanged. The page register and XML sitemap contain canonical pages only.

`static/data/url-redirects.json` records direct old-to-new routes. The build
regenerates compatibility pages, retaining legacy assets for inbound references.
GitHub Pages cannot configure arbitrary server-side 301/308 redirects. Alias
pages therefore return HTTP 200 with canonical metadata, immediate HTML refresh,
a visible fallback link, and shared JavaScript that preserves incoming query
strings and fragments. Without JavaScript, refresh uses the authored target.
Explicit `index.html` requests on canonical directories resolve to the same
physical file on Pages; canonical tags select the directory form and no internal
links or sitemap entries use `index.html`.

## MTN coverage

The four reader-facing pages now belong to the main site at
`/work/mtn-uganda-stock-coverage/`. The separate MTN repository retains research
sources and generates a `canonical/` export for review, plus redirects at its
legacy Pages paths. `docs/MTN_SOURCE.json` records the imported source revision.
To refresh after reviewing source changes:

```sh
python /path/to/mtn-uganda-stock-coverage/scripts/build_reports.py
python scripts/import_mtn_coverage.py /path/to/mtn-uganda-stock-coverage
python scripts/build_site.py
```

Commit the four imported pages and provenance changes together. Main-site builds
use only the reviewed snapshot; they never fetch changing upstream material.
Article dates, research statements and original publication links are preserved.
Existing RSS item GUIDs for moved research reports are also retained.

## Validation and release order

1. Build and run publication, navigation, coherence and URL audits.
2. Run responsive/browser tests and every legacy URL redirect with query/anchor
   preservation. Sample no-JavaScript redirects and static listings as well.
3. Deploy the main-site migration first. Verify new routes and canonical metadata.
4. Deploy the MTN generator/legacy redirects second, preventing missing targets.
5. Recheck the live sitemap, new routes and old URLs after CDN propagation.

Rollback: revert the main-site migration commit and deploy the previous reviewed
revision. If the MTN redirects have already deployed, revert that repository's
migration first so its old pages are restored before removing new destinations.
Do not delete compatibility pages while inbound links may still be used.

`audit_urls.py` blocks legacy internal links, uppercase/underscore/HTML canonical
paths (except the deliberate 404 document), missing canonical/social URLs,
redirect chains, missing no-JS fallbacks and sitemap drift. It runs in both CI
and the exact-revision publication gate.
