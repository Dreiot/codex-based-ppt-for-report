# Design system and quality assurance

## Adaptive design baseline

Use a 16:9 canvas with a clean white background, dark-gray primary text, and restrained deep-blue accents. Maintain strong hierarchy, generous margins, and academic restraint. Build an original clean master; do not retain `Made with GAMMA` or other third-party template branding.

Treat this as a design language, not a fixed template. Vary layout according to content:

- use process diagrams for workflows and dependencies;
- use before-after structures for method or formula changes;
- use plots and experimental figures for quantitative evidence;
- use annotated formulas for mathematical changes;
- use tables only for genuine repeated-field comparison;
- use cards sparingly for short categories or decision summaries.

Avoid decks where most slides reuse the same table, card grid, or text-heavy layout. Preserve consistent typography, spacing, color, and chapter navigation while allowing page-specific composition.

## Design tendencies

- `严谨学术型`: prioritize definitions, formulas, controlled comparisons, and precise annotations.
- `视觉讲解型`: prioritize mechanisms, process diagrams, experimental figures, and progressive explanation.
- `决策讨论型`: prioritize questions, evidence, options, risks, and next decisions.
- `自定义`: follow user-specified palette, density, reference slides, or composition while preserving readability and evidence integrity.

Recommend one tendency after the report type is chosen, but require confirmation or adjustment before production.

## Visual rules

- Keep titles concise, natural, and topic-led by default. Do not use prompt-like, slogan-like, or presentation-strategy sentences as titles; move those statements into the body or speaker notes.
- Make the main takeaway visible without reading speaker notes.
- Use Chinese labels in diagrams and charts unless an official name must remain unchanged.
- Do not fabricate decorative data, plots, citations, or icons that imply evidence.
- Preserve figure aspect ratios and legibility.
- Avoid tiny body text, excessive borders, dense full-slide tables, and uncontrolled color proliferation.
- Include section dividers for multi-project reports.
- Insert a visible chapter transition before each project rather than switching directly between technical slides.
- Keep projects visually consistent but structurally separate.

## Required QA

Render every slide and inspect at full size. Check:

1. the approved presentation artifact opens successfully and remains editable: `.pptx` by default, or offline `.html` when explicitly requested;
2. slide count and order match the approved outline;
3. every substantive claim maps to the evidence ledger;
4. research-facing wording preserves the evidence boundary between established observations, preliminary results, planned work, unperformed experiments, and unresolved uncertainty without requiring developer-facing status codes on slides;
5. every material workflow or formula change has before, after, rationale, core difference, and impact;
6. Chinese terminology and first-use bilingual expansion follow the content rules;
7. formulas use native Office Math or clean LaTeX/MathJax vector output for non-trivial display equations; every vector equation has `Equation: <source-id>` alt text; formulas remain legible and notation-consistent and correctly render subscripts, superscripts, fractions, norms, traces, transposes, and Greek symbols without raw programmer-style underscores or ordinary text-box approximations;
8. every formula preserves its natural aspect ratio: SVG formulas use `preserveAspectRatio="xMidYMid meet"`, are fitted with one uniform scale derived from the `viewBox`, and have no more than 1% relative difference between the natural and displayed aspect ratios;
9. formula-heavy slides have been visually checked at full size for stretching, clipping, blur, font substitution, and misplaced subscripts or superscripts;
10. speaker notes exist on every substantive slide when the approved format supports them and form a natural Chinese talk track with takeaway, explanation, caveat, and transition rather than production instructions or metadata; otherwise the pre-approved limitation and agreed substitute are recorded;
11. speaker notes contain no `[Sources]` blocks or source lists unless the user explicitly requested source-bearing notes; provenance remains traceable in the temporary evidence packet;
12. no text, shape, image, or chart overflows the canvas;
13. no empty placeholders, clipped text, accidental overlaps, or unreadable labels remain;
14. no third-party template branding remains;
15. layouts show appropriate variation without losing visual consistency;
16. slide titles are concise topic labels or natural scientific titles, and presenter-oriented framing has been moved to body text or speaker notes;
17. every project in a multi-project deck begins with a clear chapter transition or divider;
18. the final presentation uses the local production date as `<YYYY-MM-DD>.pptx` or `.html` unless the user requested another name, and existing decks remain untouched unless overwrite permission was explicit;
19. the default final output location contains only the requested presentation artifact; evidence packets, QA reports, renderings, source projects, and inspection data remain in the temporary run directory until user acceptance and are then removed unless explicitly requested.

## Internal QA record

Record each check internally as `PASS`, `FAIL`, or `NOT RUN`. For `FAIL`, state the defect and whether it was fixed. For `NOT RUN`, state why and name any substitute inspection. Do not convert substitute evidence into a false pass. Keep this record transient by default and persist it only when the user explicitly requests a QA report.
