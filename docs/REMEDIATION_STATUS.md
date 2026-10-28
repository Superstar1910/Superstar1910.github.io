# Remediation status — 28 October 2026

## Implemented in the public production release

- Shared About / Work / Writing / Connect navigation, common social/legal footers and parent breadcrumbs across 84 content pages.
- Twenty curated work entries, including all three research programmes, native HTML directories, publication/report labels, related-reading links, 12-item enhanced archive batches and working compatibility aliases.
- Root sitemap/robots, visitor site map, 404 page, canonical/share metadata, responsive local images, normalised imported H1 levels, targeted contrast fixes and a constrained meta CSP.
- All source URLs and original article dates preserved. Current production was used as the baseline; no wholesale V2 replacement.
- Pages uses validated public-only artifacts after passing site-quality checks; migration packages, templates and source scripts are not published.
- HTTPS enforcement enabled; direct HTTP now redirects. Scheduled core-route monitoring and exact action pins added.
- Desktop/mobile and no-JavaScript checks passed; mobile research-table overflow corrected.

## Implemented in vault source, not deployed

Private repository changes pin database and object access to a single provisioned owner; keep release and uploads closed by default; persist SSR refresh cookies; serve guarded attachment downloads; validate signatures; define isolated audit logging; and pin a patched dependency tree and lockfile. A clean build and production dependency scan passed locally. Live provider policy/advisor/MFA/recovery/restore/scanning assurance is not available: the connected account lists no Supabase projects.

## Remaining requirements (do not mark these complete)

1. GitHub blocked saving main protection with a Confirm access / sudo reauthentication. The prepared rule requires pull requests, current site-quality checks and resolved conversations, prohibits force pushes/deletion and applies to administrators. It has NOT been saved. No external reviewer is configured; a single-owner repository must not be locked by requiring self-approval.
2. Registrar DNS access is needed for www, domain verification/renewal and certificate-monitoring ownership. No DNS changes have been made.
3. GitHub Free only enforces branch protections on public repositories. V2/vault privacy must not be weakened to obtain enforcement; paid-plan/private-repository enforcement remains a separate account decision.
4. Strict response CSP, framing/HSTS and other edge headers need a supported host/edge decision. Meta CSP allows existing inline code and is not equivalent to those headers.
5. Informative image/chart alternatives require individual visual/editorial review; an empty alt may be appropriate for decoration. Do not auto-label graphics with invented interpretations.
6. Screen-reader checks, independent financial/research validation and traffic-backed CWV/CrUX/Search Console outcomes remain unverified. Laboratory reports, when generated, do not replace field data.
7. Actual vault provider provisioning, SQL application and direct-access test matrix, MFA enrollment/recovery, backups/restore and malware scanning must pass before approval flags change.

Detailed operations and recovery steps are in OPERATIONS.md and the private vault's docs/RELEASE_AND_RECOVERY.md. This status register reports implementation and assurance separately.
