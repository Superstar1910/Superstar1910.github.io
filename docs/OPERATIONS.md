# Public website operations

Production is `Superstar1910/Superstar1910.github.io`. Development starts from its current main branch. The separate historical V2 copy is not a deployment source and must not replace production wholesale.

## Publication

1. Open a branch from current production. Edit content and the approved JSON registers.
2. Run `python scripts/build_site.py`, `python scripts/build_article_feeds.py`, `python scripts/validate_articles.py`, `python scripts/audit_publishing.py`, `python scripts/audit_navigation.py`, and `python scripts/audit_coherence.py`.
3. Review article dates, sources, research associations, figure descriptions and role statements. Null review dates mean no verified review is claimed.
4. Open a PR; `Site quality / site-quality` runs for every change, including primary pages and policies. It checks mobile/desktop samples, filters and no-JavaScript listings.
5. With Pages configured for **GitHub Actions**, `Publish reviewed site` runs after successful main-branch quality checks, checks out that exact SHA and uploads only `_site/`. No imports, templates or source scripts are published.
6. Confirm the deployment succeeds and the public pages contain the expected changes. Daily `Monitor public site` detects core route failures.

Use `templates/header.html` and `templates/footer.html` for global navigation. Keep canonical URLs stable; `/work/`, `/research/` and `/connect/` are compatibility aliases. Native writing belongs under `/writing/`; project-specific navigation stays below the common header. Keep vault credentials, models and records outside this public repository.

## Rollback and restore

Revert the offending merge through a PR and rerun quality checks. Preserve `CNAME`, `.nojekyll`, existing article routes and original dates. The previous known-good source revision is recoverable through Git history. If deployment fails, retain the last successful artifact rather than repointing DNS. Record the reverted SHA and verify Home, Work, Writing, a report and a calculator.

Git is source history, not a backup of private records, account recovery material or provider settings. The owner must separately maintain registrar recovery, renewal, MFA and administrator access. Establish a private encrypted backup and restoration procedure for any future vault before real data enters it.

## Remaining access and assurance requirements

- The connected Supabase account listed no projects on 28 October 2026. Vault SQL, recovery, direct API denial and restore tests therefore cannot be claimed as deployed/passed.
- Registrar access is required to configure `www`, verify domain ownership, confirm renewal and inspect DNS/certificate monitoring. Do not publish the vault hostname before its release gates pass.
- GitHub Pages response-header support is limited. The meta CSP is a constrained baseline allowing existing inline code; it is not equivalent to strict response CSP or frame-ancestors/HSTS. A host/edge decision and regression checks are required for those headers.
- Real-user CWV needs sufficient traffic and Search Console/CrUX access. Browser checks do not replace a screen-reader audit, informative-chart review or independent research validation.
- Do not turn current research metadata into a false validation claim. Figures with empty alt need individual editorial review; decorative figures may correctly remain empty.

## V2 reconciliation rule

The 28 October coherence release uses current production and preserves the newer housing, financial-literacy, PAYGo, AI-policy, Enduring Enterprises and Investability content. Bring any future V2 design or verified career narrative into this source through a reviewed diff. Retain the old V2 branch for reference; do not overwrite it or its history without reconciliation.
