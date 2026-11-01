# Luck, Risk & Wealth — Editorial release review

Review date: 2026-11-01
Branch: `editorial/luck-risk-wealth-series`
Pull request: #45
Scope: Twelve standalone HTML essays and a series landing page.

## Editorial assessment
- All twelve essays expanded to approximately 700–820 words including page navigation and boilerplate; substantive essay body may be slightly shorter. Review before release.
- Narrative flow: opening proposition, tension/obstacle, practical response and reflective conclusion.
- Voice: grounded, reflective, non-promissory; avoids invented autobiographical anecdotes.
- Terminology: distinguishes financial income from wealth, nominal from real returns, control from influence, and valuation from liquidity.
- Financial guidance: educational only, with no individualised asset-allocation prescriptions or guaranteed outcomes.

## Numerical verification
- Essay 07: UGX 1,000,000 monthly contributions at month-end; 10% *effective annual* return; equivalent monthly rate `(1.10)^(1/12)-1`; 420 months gives UGX 3.39879 billion; 300 months gives UGX 1.23332 billion. Rounded prose UGX 3.40bn and UGX 1.23bn. Pre-fee, pre-tax, nominal hypothetical.
- Essay 11: UGX 120m / 0.03 = UGX 4.0bn; / 0.04 = UGX 3.0bn; / 0.05 = UGX 2.4bn. Rates are illustrative, not guaranteed sustainable.
- Essay 06: 50% drawdown requires 100% gain; 75% drawdown requires 300% gain.

## Publication blockers
1. Approved visual image binaries have not been confirmed archived in `static/img/visuals/luck-risk-wealth/`; do not substitute regenerated images.
2. Add the collection to the existing `/writing/` archive and publication feed using the repository's established generator or data source; do not manually patch generated outputs without checking their source of truth.
3. Ensure site shell, accessibility, metadata, canonical URLs, structured data and responsive rendering match existing writing pages.
4. Run the repository's validators and CI, then check all 13 routes on the deployed site.
5. Editorial sign-off on full article bodies and visual-to-article correspondence.

## Release decision
**Editorial drafts substantially expanded; not yet cleared for production merge.** This document is an audit trail, not a claim of live publication.
