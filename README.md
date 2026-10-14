# Legesi.xyz

Public professional website and native writing archive for Kenneth S. Legesi. Hosted as a **static website** at https://legesi.xyz using GitHub Pages, with the custom domain configured in `CNAME`.

## Architecture

- `index.html`, `about/`, `projects/`, `research/`, `writing/`: public pages and research.
- `static/css/`, `static/js/`, `static/data/articles.json`: shared presentation, archive browser, and publication metadata.
- `writing/<article-slug>/index.html`: native articles, retaining original publication dates and attribution.
- `writing/feed.xml` and `writing/sitemap.xml`: generated syndication and discovery files.
- `scripts/validate_articles.py`: article-register checks.
- `scripts/audit_publishing.py`: static page, canonical URL, RSS and sitemap consistency checks.
- `scripts/build_article_feeds.py`: regenerates syndication files from the approved register.
- `.nojekyll`: publish static files without Jekyll transformations.

The public repository must not contain personal-vault data, private investment records, credentials, or subscriber exports. The private vault is a **separate** owner-only system.

## Local preview and checks

From the repository root:

```sh
python3 scripts/validate_articles.py
python3 scripts/audit_publishing.py
python3 -m http.server 8000
```

Open http://localhost:8000 and check mobile navigation, article rendering, images, and writing archive search. JavaScript is used for the searchable writing directory; native article pages remain readable without JavaScript.

When the approved article register changes, run:

```sh
python3 scripts/build_article_feeds.py
python3 scripts/audit_publishing.py
```

## Publication

Use reviewed pull requests for content changes. GitHub Pages deploys from `main`; check the **pages-build-deployment** workflow and the actual live URL before announcing a release. A green repository validation does not prove that the custom domain is serving the latest deployment.

Historical Substack posts were imported as native pages through PR #12. Original dates and source URLs are preserved; editorial verification of external images and research associations remains ongoing. The ZIP in `imports/` is a temporary author-prepared migration package, **not** the original Substack subscriber/account export.

## Rollback

Revert the relevant merge commit via a reviewed PR if a release causes regressions. Preserve `CNAME` and `.nojekyll` unless intentionally changing hosting architecture.
