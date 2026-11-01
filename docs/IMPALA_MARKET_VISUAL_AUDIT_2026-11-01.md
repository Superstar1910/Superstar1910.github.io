# Impala Market — Visual Library intake audit (2026-11-01)

**State:** discovery and recovery performed; **no new Impala Market asset qualified for publication**. This is an intake/audit record, **not** a gallery catalogue entry or approval to publish.

## Scope and provenance
- Project: Impala Market, fixed-income data and investment intelligence system. Related source: `Superstar1910/impala_market`, deployed research at `https://blog.impala.market/`.
- Visual Library contract: `.agents/skills/legesi-visual-library/SKILL.md`; target repository `Superstar1910/Superstar1910.github.io`.
- Accessible prior Project conversation summaries, searchable conversation/Library files, source-image previews and the GitHub catalogue were examined. **Complete access to every historical chat and original generated image was not available.**
- Catalogue review found **45 existing records and zero with an Impala Market project/title match** at review time. This is a catalogue count, not an exhaustive repository file count.

## Recovered source images (not authorised for public archiving)
| Candidate | Recovery status | Final/version assessment | Publication block |
|---|---|---|---|
| `Uganda FX Pressure Watch Dashboard.png` | Original image visually inspected through connected Library | Separate earlier or alternative version; no explicit Impala Market final approval evidenced | Oakstone branding; typography overlap; financial data verification; cross-project scope |
| `Uganda FX Pressure Watch Dashboard(1).png` | Original image visually inspected through connected Library | Distinct revised version; final approval not evidenced | Oakstone branding; typography/source labels overlap; data verification; rights and project attribution |

**Important:** These source images are **not copied to public GitHub**. Both contain information about Ugandan government bond yields, but are not Impala Market-branded approved assets. The fact of a later numeric filename does not establish approval.

## Other identified candidate families
| Family | Accessible historical evidence | State |
|---|---|---|
| Treasury bill auction graphics | 2025–2026 research discussion and attached screenshot references | pending-original-recovery and final-version-proof |
| Uganda sovereign yield curves | Bond auction and investment-intelligence research | pending-original-recovery and numerical/source reconciliation |
| Auction-day / secondary-market liquidity | Article analyses, data windows, dashboard narratives | pending-original-recovery and numerical/source reconciliation |
| Impala fixed-income dashboard | Streamlit screenshot references and application discussions | pending-original-recovery; avoid treating UI screenshot as standalone approved research |
| IPS and portfolio allocation visuals | IPS engine discussions, global asset-universe design | pending-original-recovery and suitability/publication rights |
| Uganda FX Pressure Watch dashboards | Two original PNGs inspected, from cross-project personal Library | excluded from immediate publication, pending approval and accuracy checks |

## Gate results
- **Discovery:** partial; six visual families identified, two original images visually inspected.
- **Source provenance:** two cross-project originals recovered for visual inspection; original bytes not ingested into the repository.
- **Final approval:** zero demonstrably approved in-scope originals.
- **New archived images:** zero.
- **New gallery records:** zero.
- **New merged/published assets:** zero.
- **Validation/CI:** not run for new image intake because no asset package was eligible; do not infer pass.
- **Live website:** publication of any new Impala images not asserted; gallery accessibility could not be independently confirmed during this audit.

## Next admission criteria
For each distinct visual, recover original bytes; identify the approved final versus superseded revisions; check numbers against dated BoU or other source datasets; confirm rights and confidentiality; classify correctly as Impala versus Oakstone cross-project content; optimise and hash images; upload on a dedicated intake branch; validate catalogue and images with `scripts/validate_visual_library.py` and site CI; review/merge; verify live rendering.

No placeholders, inferred images, re-creations, unverified investment numbers or new gallery catalogue entries are authorised by this report.

## Recovery pass 2 — exact Project folder and repository starter (2026-11-01)

The accessible personal Library has a named folder `/Impala Market`, but its direct folder listing returned **zero files**. This confirms that this folder cannot supply the historical originals in the current access context; it does not prove no visual assets ever existed in prior chats.

The separately stored original `impala-market-repository-starter.zip` was successfully materialised and its ZIP inventory inspected: 17 files, all source text/configuration/Markdown/CSV and **zero raster/vector image files**. It includes `charts/README.md` but no chart exports. No publication authorisation is implied by having the starter package.

Live GitHub `Superstar1910/impala_market` README was read: modules include Dashboard, Auctions, Secondary Market, Yield Curve, Instruments and Alerts. The README describes chart-producing software and download-as-CSV functionality, **not** a curated set of approved image originals. GitHub code search for `chart` and `png` returned no indexed matches; that is inconclusive for assets in an unindexed repository.

### Provenance-based recovery queue (next available source)
1. **First priority: auction and secondary market illustrations.** Recover attached images and final revisions from the March 2026 Project conversations; reconcile auction dates, observation units, tenor, coupons and turnover time windows before release.
2. **Yield curves.** Export source-backed dated figures from a reproducible Impala Market data snapshot; do not substitute an illustration for an approved historical original. Mark new exports as new work requiring explicit editorial approval.
3. **Streamlit market dashboard.** Re-obtain version-specific screenshots, record app commit and data freshness; treat as product screenshots, not verified chart data.
4. **IPS engine visuals.** Verify the implementation matches published product behaviour and asset-class assumptions, and avoid showing personalised financial information.
5. **Cross-project FX Pressure Watch.** Keep both original Oakstone PNGs out of the Impala Market publication batch absent explicit cross-project approval and numerical QA.

### Required import evidence per candidate
- Exact original file path, source conversation or attached asset identifier
- Distinct final-version evidence and evidence of superseded variants
- Original SHA-256, size and image dimensions
- Quantitative claims and source document dates where applicable
- Rights/publication and confidentiality clearance
- Appropriate Impala Market project tag and descriptive alt/caption
- Reviewer approval; web-optimised derivative hash and thumbnail
- PR, validator and GitHub Actions status; merged commit and HTTP/rendering verification

**Pass 2 disposition:** no eligible Impala Market original recoverable from the named Library folder or recovered starter ZIP; no new gallery entries, binary uploads, merges or live publications performed.
