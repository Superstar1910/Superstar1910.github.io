# Legesi.xyz publishing workflow

The Writing page reads `static/data/articles.json`. It lists native pages and clearly identified external historical articles. Original publication dates must come from verified publisher metadata; **never substitute import dates**.

## Add an article
1. Obtain the author's original Markdown/HTML or a lawful export. Preserve images with licence/credit.
2. Publish the rendered article at `writing/<slug>/index.html` (or link to an existing native research page). Use `static/css/brand-tokens.css` and `static/css/editorial.css`.
3. Add an entry to `static/data/articles.json`: `slug`, `title`, `datePublished` (original first-publication date, ISO), `dateAdded` (first hosted on legesi.xyz), `dateModified` (substantive revision date), `type`, `platform`, `originalUrl`, `url`, `summary`, `native`.
4. When importing, keep `native:false` until the full article renders on legesi.xyz. Do not present a link-only entry as a migrated article.
5. On the native article page, display the original date and first-publication platform, and the date added to legesi.xyz. Add JSON-LD BlogPosting with datePublished and dateModified. Use a canonical URL appropriate to the distribution arrangement.
6. Validate links, image accessibility, author ownership, dates, metadata and investment disclosures. Review and merge.

## Sync strategy
- **Substack**: use the publication RSS feed to discover new links and metadata; older content requires author export and reconciliation because feeds are incomplete.
- **Medium**: use account export or authorised feed for discovery; verify historical dates against original posts.
- **LinkedIn**: use the author's export or manually supplied article files; do not scrape authenticated pages or assume a public feed contains full article text.
- A scheduled job may propose new register entries and prepare draft pull requests. Never overwrite native edits, silently republish copyrighted third-party material, or change financial conclusions without review.
- Generate sitemap and RSS from the register once the archive is complete; use CI checks for duplicate slugs, invalid dates and broken internal paths.

## Current migration state
Two research assessments link to full native HTML pages. Two historical Umeme Substack articles are indexed externally, not yet imported. Other articles have not been inventoried. This is a foundation, **not a completed migration**.

## Research-linked article contract
When an article is based on a repository, populate `research.repository`, `research.analysis`, `research.methodology`, `research.cutoff` (only if independently established) and `research.reviewStatus` in the article register. Show research and underlying-analysis links in the public archive. On the full article, include an evidence/methodology panel and link to a versioned commit or release for reproducibility. Do not automatically substitute current model results into historical articles. A materially updated thesis requires a new dated edition or explicit revision note. Keep a changelog and, where practical, a comparison of changed assumptions and valuation outcomes.

The repository URLs currently link to moving `main` branches, **not pinned evidence snapshots**. Before calling an article reproducible, capture the exact commit SHA, source snapshot and model run identifier. Article dates and analysis cut-offs must be verified independently.
