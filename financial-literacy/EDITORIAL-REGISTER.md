# Financial literacy and investing — editorial reconciliation register

Status: working editorial inventory, not a publication log. Historical article titles below are drawn from the All Things Content development programme. Publication dates and full-text source provenance must be checked before importing anything into `static/data/articles.json`.

## Published records verified in website register
- Why Your Brain Is Your Worst Investment Enemy — `/writing/why-your-brain-is-your-worst-investment/`
- Risk is Personal, but Also a Privilege — `/writing/risk-is-personal-but-also-a-privilege/`
- Bond Yield Rate Vs Bond Coupon Rate — `/writing/bond-yield-rate-vs-bond-coupon-rate/`
- How I Turned Macro Outlooks into ETF Portfolios and How They Performed by Year-End 2025 — `/writing/how-i-turned-macro-outlooks-into/`
- Tail Risk: The Losses That Don’t Show Up in Your Models — `/writing/tail-risk-the-losses-that-dont-show/`

These are related published pieces, **not** evidence that all historical course drafts have been published.

## Draft series to reconcile (unverified publication)
### Personal finance
- 10 Common Financial Mistakes (And How to Avoid Them)
- Investing for Life: Tailoring Your Portfolio for Your Goals
- Retirement Planning
- Family Financial Planning 101
- Building the Perfect Rainy-Day Fund (historical LinkedIn source to check)
- When are Life Insurance Products Suitable? The Case of an Endowment With Profits Policy (historical LinkedIn source to check)

### Investing
- Understanding Investment Risks
- How to Measure Investment Performance: Beyond Just Returns
- Technology Meets Investing
- Investing with a Conscience: The Rise of ESG
- Investing in Emerging Markets
- Beyond the Basics: Advanced Strategies for Growing Wealth
- Regional and global equities, government securities, unit trusts vs ETFs, and portfolio allocation lessons

### Behavioural investing — Seek > Target > Story series
- Series introduction
- Confirmation bias
- Herd mentality
- Overconfidence
- Anchoring
- Fear and greed
- Practical bias mitigation
- COVID-19 market case study
- Tools for smarter investing
- Loss aversion (confirm whether a complete draft exists)

## Editorial gate for every candidate
1. Recover original full text and its canonical source; do not reconstruct missing text from titles.
2. Check against existing `articles.json` slugs, original URLs and article content to avoid duplication.
3. Fact-check investment examples, laws, taxes, market prices, returns and dated statements; label historical figures and verify calculations.
4. Check attribution, rights, audience, narrative structure, disclosures and all external links.
5. Publish the reviewed article at a stable native URL; only then add a verified record to `articles.json` with correct dates and original URL.
6. Regenerate feeds first with `python scripts/build_article_feeds.py`, then run `python scripts/validate_articles.py` and `python scripts/audit_publishing.py` against the updated register and generated `writing/feed.xml` and `writing/sitemap.xml`; inspect generated feeds and website rendering.
7. Update the financial literacy hub with a direct link, category and status. Verify live Pages deployment.

## Interactive tool QA register
- Emergency Fund Planner: merged; browser smoke test and accessibility audit outstanding. Test zero contribution, already-funded reserves, negative values, non-integer months, overflow and mobile viewport.
- Financial health checklist: planned, not implemented.
- Risk profiler: planned, not implemented; avoid portraying scores as personalised suitability assessments.
- Portfolio allocation explorer: planned, not implemented; scenario illustrations must not imply recommendations.
- Performance evaluator: planned, not implemented; define cash-flow timing, benchmarks, currency and fee treatment before coding.

## Publication governance
Never invent original publication dates or mark drafts as live. Avoid importing private project data, personal investment records or unverified valuation estimates. Separate education from regulated advice and maintain an explicit source register.
