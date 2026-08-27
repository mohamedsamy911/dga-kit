# Coverage map

Every area of design.dga.gov.sa, and which skill owns it. One owner per area — no skill
duplicates another's rules, because rules live once in `dga-design-system/references/`.

## DGA source → owning skill

| DGA area | Pages | Extracted into | Owned by |
|---|---|---|---|
| Foundations — colour | 1 | `foundations.md`, `tokens.json`, `CONTRAST-AUDIT.md` | `dga-design-system` |
| Foundations — typography | 1 | `foundations.md` | `dga-design-system` |
| Foundations — layout & spacing | 1 | `foundations.md`, `tokens.json` | `dga-design-system` |
| Foundations — elevation | 1 | `foundations.md`, `tokens.json` | `dga-design-system` |
| Foundations — iconography | 1 | `foundations.md` | `dga-design-system` |
| Components | **50** | `components.md` | `dga-design-system` |
| Templates | **19** | `patterns.md` | `dga-design-system` |
| Accessibility (per-component + Accessibility Ease) | 51 | `accessibility.md` | `dga-a11y` |
| Design tokens (`/thoughts/designToken`) | 1 | `foundations.md` §Token architecture | `dga-tokens-sync` |
| Local & global standards | 1 | `foundations.md` §Compliance context | `dga-launch-gate` |
| Transparency mandate (About the Entity, e-Participation) | 2 | `patterns.md` | `dga-launch-gate` |
| Brand & identity (logos, seasonal, Saudi Font) | across templates | `brand.md` | `dga-brand-overlay` |
| Content & language | across templates | `content.md` | `dga-design-system` |
| RTL — DGA's own explicit statements | **`TODO(verify)`** | `rtl-rules.md` + citations | `dga-rtl-i18n` |
| Developer setup (`/developing`, install) | 2 | `official-packages.md` | `dga-react` |
| DGA rules expressed in a non-DGA UI library | — | `token-wiring.md`, `component-mapping.md` | `dga-ui-adapter` |
| Designer setup (`/designing`, Figma install) | 2 | `patterns.md`, `brand.md` | `dga-mockup` |
| Designing for mobile (`/designing-for-mobile`) | 1 | `mobile.md` | `dga-mockup` |
| Library migration (`/migration-guide`) | 1 | `library-migration.md` | `dga-tokens-sync` |
| **Assessment Criteria** (`/AssessmentCriteria`) | 1 | `assessment-criteria.md` | `dga-launch-gate` |
| Atomic design (`/thoughts/atomic-design`) | 1 | `foundations.md` §Atomic design | `dga-frontend-architect`, `dga-handoff` |
| Responsive design (`/thoughts/responsive-design`) | 1 | `foundations.md` §Responsive design | `dga-design-system` |
| Consistency & unified identity (`/thoughts/consistency-and-unified-identity`) | 1 | `brand.md` §Colour identity, §Typeface identity | `dga-brand-overlay` |
| Contributing (`/contributing`) | 1 | `foundations.md` §Contributing back to DGA | `dga-design-system` |
| Change log + roadmap (`/updates/*`) | 6 | `harvest/raw/2026-08-27-section-sweep.md` | `dga-tokens-sync` |

## Skill lanes — what each one alone does

| Skill | Owns | Explicitly does NOT |
|---|---|---|
| **dga-design-system** | The rules. Foundations, 50 components, 19 templates, content, tokens. Read by everything else. | Judge a design, write code, or run anything |
| **dga-design-review** | Auditing a *design* against DGA. Seven fixed passes, severity rubric, verdict. | Audit code, or produce designs |
| **dga-mockup** | *Producing* compliant screens from DGA templates, Arabic-first | Review its own output — that's design-review's job |
| **dga-handoff** | The design→dev seam. Component inventory, token map, state matrix, bilingual copy | Design or build |
| **dga-react** | Code, **when the project uses DGA's own `platformscode-new-react`** — the gap layer over it | Apply to a project on any other UI library; that is `dga-ui-adapter` |
| **dga-ui-adapter** | Code, **on every other UI library** — wiring DGA tokens into your theme, 50 component mappings, the build list | Teach you your own UI library |
| **dga-rtl-i18n** | Arabic-first mechanics. Mirroring, bidi, Arabic typography, Intl formats, next-intl | Component specs |
| **dga-a11y** | Auditing *running code* against DGA's per-component ARIA + WCAG 2.1 AA | Review static designs |
| **dga-launch-gate** | Everything beyond design: registration, transparency mandate, required pages, Open Data, measurement indicators | Design or accessibility detail |
| **dga-tokens-sync** | Re-harvesting tokens and diffing them | Anything at build time |
| **dga-brand-overlay** | One entity's overlay, and the project's open decisions (numerals, calendar, mirroring) | Override anything DGA fixes |

## Two code skills, one active at a time

`dga-react` and `dga-ui-adapter` never both apply. Which one depends on the project's UI library:

| Project uses | Use | Because |
|---|---|---|
| `platformscode-new-react` | `dga-react` | DGA's own 175 components are available as the reference implementation. The skill is the gap layer over them. |
| **Anything else** — Tailwind, MUI, Chakra, shadcn/Radix, Ant, Bootstrap, Vue/Angular kits, plain CSS | `dga-ui-adapter` | None of DGA's components are available, so every spec must be re-expressed and *"does this match DGA"* becomes a judgement rather than a diff. |

## Agents

| Agent | Lane | Writes files? |
|---|---|---|
| `dga-designer` | Problem framing → state matrix → copy → handoff | Yes |
| `dga-frontend-architect` | Structural decisions before code exists | **No** |
| `dga-frontend-dev` | Implementation from a spec | Yes |
| `dga-code-reviewer` | Correctness, security, DGA, WCAG AA | **No** |
| `dga-compliance-auditor` | Pre-launch go/no-go with evidence | **No** |
| `dga-content-writer` | Arabic-first bilingual interface copy | Yes |

## Eval suites

| Suite | Cases | Tests |
|---|---|---|
| `evals/dga-design-review/` | 11 | Detection vs restraint on design review |
| `evals/dga-ui-adapter/` | 12 | Detection, restraint, and **library confusion** — advice for the wrong library, or a component it does not have |

## Guarding against our own drift

The monitoring in `dga-tokens-sync` watches **DGA** for changes. `evals/check-quote-fidelity.py`
watches **us** — it compares every DGA quote in `skills/` against the captured page text in
`harvest/raw/`, and fails on a paragraph that reproduces a capture without matching it.

That is the direction this repo has actually gone wrong: `-2%` shipped as invalid CSS, the
template count asserted as 19 when the harvest held 17, and a launch-gate quote that dropped
DGA's word *"typically"*. None of those would be caught by re-checking design.dga.gov.sa.

```bash
python3 evals/check-quote-fidelity.py --ci
```

It reports **blockquote coverage**: how many blockquote paragraphs in `skills/` could be matched
to a captured DGA passage. The figure is deliberately not repeated here — it moves whenever a
blockquote is added anywhere in `skills/`, and a copy of it in this file went stale within an hour
of being written. Run the command for the current number.

Read it for what it is. The denominator counts *every* blockquote, and most of those are the
kit's own commentary rather than DGA quotes, so the true share of *DGA quotes* that are evidenced
is higher — by an amount nothing currently measures. A real evidence-coverage figure needs DGA
quotes marked in `skills/` with the same `<!-- dga -->` fence the captures use — `TODO`.

Raising the numerator means capturing more pages, never editing a reference to match.

`evals/validate-fixtures.py` checks every value the cases assert against `tokens.json`. Run it
after any re-harvest: an eval asserting a stale value teaches the skill a false rule, which is
worse than having no eval.

**Any fabrication fails a suite outright**, regardless of detection score.

## Where a design is checked twice — on purpose

`dga-design-review` pass 6 checks accessibility *in the design*; `dga-a11y` checks it *in the
running code*; `dga-code-reviewer` checks what is visible *statically in the source*. Different
artefacts, different failure modes, same rules. That is the only intentional overlap.

## Known gaps — what this kit does NOT cover

Stated plainly so no skill implies coverage it lacks.

| Gap | Impact | Fix |
|---|---|---|
| **Digital Transformation Measurement Indicator** | `dga-launch-gate` §6 incomplete | Harvest — published outside design.dga.gov.sa |
| **Digital Experience Maturity Indicator** | same | same |
| **Assessment Criteria *checklist file*** | The scoring page is captured (`harvest/raw/2026-08-27-section-sweep.md`); the downloadable checklist is a separate file | `Download Checklist` on `/AssessmentCriteria` |
| **Responsive radius & spacing values** | Per-breakpoint tokens can't be resolved; treating them as constants is wrong on two of three breakpoints | PC 1.0 Foundations Figma variable collections |
| ~~**Dark theme values**~~ | **Closed 2026-08-27** — all **402** are in the public CSS bundle; the 67 text/background roles are in `tokens.json` as `role.dark` and audited by `check-contrast.mjs --theme dark`. 🚩 DGA's selector `[data-theme=dark] :root` can never match, so its dark theme is inert. **We do not ship it either** — see the row below | Remaining 340 non-role declarations are uncaptured in **both** themes — see `role.dark.$comment` |
| **Dark theme, shippable** | `tokens.css` deliberately emits **no** dark rule. Correcting DGA's selector would activate 1.05:1 pairings for anyone already using `data-theme="dark"`, and the five `*-light` status surfaces have no dark tint anywhere in DGA's output — so it cannot be made safe without inventing values | An entity that wants dark mode owns the remediation and records it in `dga-brand-overlay` |
| **Mobile UI Kit** (6 components) | Names confirmed from `/designing-for-mobile` 2026-08-27; **no specs** — that page is a Figma download landing page | Figma-only |
| **Arabic-language version of the site** | Arabic terminology for `content.md`. The toggle is reachable and renders; only the terminology harvest is outstanding | The `العربية` toggle |
| **Storybook** | Component demos | Marked "soon" by DGA — not available yet |
| **Designer sign-off** | Values are exact; the *interpretation* is unverified | A DGA-literate designer reads the references |

## Disputed and unverified claims

Recorded rather than quietly resolved, per the kit's own cite-or-omit rule.

| Claim | Status |
|---|---|
| **How many places DGA itself states an RTL rule.** This file previously said "6 references across the whole system". Nothing in the kit enumerates them, so the number cannot be checked from its own files, and a review of the derived skills named four (Quote, Steps, Buttons, Pagination). The 16 ⚠️ **RTL** callouts in `components.md` are the kit's *derived* guidance, which is a different count and must not be conflated with DGA's own statements. | **`TODO(verify)`** — settle by re-reading the live site and listing the pages. Until then no skill may cite a number. |
| Three colour values disputed against an independent extraction | Carried as `$meta.$disputed` in `tokens.json`; see `harvest/CROSSREF-SECOND-EXTRACTION.md` |
| **How many components DGA ships.** `/about-platforms-code` publishes a **33+** counter. `/guidelines/components/` enumerates **50** routes. | Recorded, not reconciled. This kit cites **50** — the enumerable count. The counter is stale marketing copy. |
| **When 1.0.0 and 1.0.2 shipped.** `/updates/roadmap` dates them Feb 2024 and Sep 2024; `/updates/change-log` dates the same versions 20 Feb **2025** and 1 Sep **2025**. | Cite the change log — the more specific record. |

## Where DGA itself is silent

No skill invents a rule here. Each says DGA is silent and names its fallback.

Numeral policy · Hijri calendar · Arabic body typeface · motion tokens (durations and easings —
though `prefers-reduced-motion` **is** required in three places) · terminology glossary ·
Arabic tone of voice · **Card accessibility** (DGA's section is Accordion's, pasted in) ·
**Menu accessibility** (no section exists at all) · Table ARIA roles · carousel pause control
(WCAG 2.1 AA 2.2.2 requires one — apply WCAG) · colour-blind-safe chart palettes · dark-mode
usage guidance · accessibility-statement page.

## Where DGA's own tokens fail WCAG

Not a gap in this kit — a fact about the source, and the reason `check-contrast.mjs` exists.
`text.secondary` (#dba102) is a DGA token **designated for text** that measures 2.30:1 on white
and fails AA at every size. Three `text.*-light` tokens are dark-surface only despite the naming.
Run `node skills/dga-design-system/assets/check-contrast.mjs` for the current list.
