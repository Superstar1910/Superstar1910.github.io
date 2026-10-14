# Legesi.xyz — Brand & Design System v1.0

**Brand proposition:** Ideas worth exploring. Things worth building.  
**Mantra:** *Semper Facere Meliorem* — Always strive to make things better.

## Positioning
An independent editorial home for Kenneth S. Legesi's work at the intersection of capital, infrastructure, technology and ideas. The experience should convey quiet authority, intellectual curiosity and disciplined execution—not a corporate brochure or a repository dump.

## Identity and voice
- Precise, intellectually independent, grounded and constructive.
- Explain the problem, evidence, method, uncertainty and next step.
- Avoid inflated claims, unexplained acronyms, exaggerated outcomes and stock-business imagery.
- Clearly distinguish published research, working prototypes and verified live applications.
- Do not imply regulatory approval, investment suitability or independent verification.

## Design tokens
Canonical reusable tokens: [static/css/brand-tokens.css](static/css/brand-tokens.css).

| Role | Token | Value |
|---|---|---|
| Ink | `--brand-ink` | `#15253A` |
| Editorial blue | `--brand-blue` | `#29496D` |
| Muted slate | `--brand-muted` | `#596A7D` |
| Hairline | `--brand-line` | `#E3E8ED` |
| Paper | `--brand-paper` | `#FFFFFF` |
| Section wash | `--brand-wash` | `#F8FAFC` |

**Typography:** Georgia / Times New Roman for editorial display and section headings; Arial / Helvetica for body, navigation, controls and data labels. Wordmark: uppercase sans-serif, bold, generous tracking. Use system font stacks; do not distribute font files.

**Layout:** Maximum content width 1240px; generous whitespace; narrow text columns for long-form research; thin rules and restrained borders. Cards use subtle borders and minimal rounding. Maintain responsive mobile layouts.

**Interaction:** Clear text links, visible keyboard focus, accessible labels, no autoplay or gratuitous animation. Respect reduced-motion preferences. Avoid decorative badges and oversized coloured callouts.

## Imagery
Prefer authentic personal, project, infrastructure and architectural photographs. Use imagery only when it helps explain the work. Avoid generic trading floors, handshake stock photos and unsubstantiated visual claims. Record image ownership, licence, alt text and attribution where applicable.

## Public project presentation
Each project card must answer: what it does, who it is for, what is available now and where to explore it. Prefer a verified live demo or rendered HTML page for nontechnical readers. If none exists, link to a readable research note or repository; never label a raw GitHub HTML blob as a deployed application.

Suggested page pattern: eyebrow → strong editorial heading → one-paragraph purpose → evidence/method → interactive or published output → source/methodology → limitations → next step.

## Research publishing
Show research date and cut-off, author, source register, assumptions, limitations and material conflicts where applicable. Link to the site investment disclaimer. Separate factual observations from estimates and scenarios. Preserve repository-specific open-source licences.

## Architecture and governance
- **Public site:** legesi.xyz; source of shared design tokens and reference layout.
- **Public research/apps:** adopt tokens and editorial conventions progressively; retain project-specific functional UI where warranted.
- **Private vault:** distinct authenticated application and security controls; may share visual identity but never public assets containing confidential data.
- Review at each material design change; update this guide and tokens together. No implication that linked repositories are already migrated.

## Implementation checklist
1. Load `brand-tokens.css` before site/project CSS.
2. Use tokens rather than new arbitrary palette values.
3. Provide accessible heading hierarchy, navigation, mobile layouts and visible focus.
4. Distinguish live demos from research notes and source repositories.
5. Check privacy, intellectual property and investment-disclaimer links.
