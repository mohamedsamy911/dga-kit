# Capture log

Evidence trail for every DGA rule this kit asserts.

**Source:** https://design.dga.gov.sa/ — "Platforms Code", National Design System of Saudi Arabia
**Site footer version:** © 2025 · **Design kit version:** **PC 1.0.3**, released 4 Nov 2025
(per `/updates/change-log`, captured 2026-08-27 — earlier notes in this kit said bare "PC 1.0")
**Captured by:** Claude, via Claude-in-Chrome on `mohamed-samy`
**Method:** live page text + CSS custom-property extraction from the DOM. Token values are
verbatim from the running site, not transcribed from screenshots.
**Verified by:** — ⚠️ designer sign-off still outstanding

## Captured

| Section | Page | URL | Date |
|---|---|---|---|
| Site | Home / sitemap | `/` | 2026-08-26 |
| Foundations | Color system | `/guidelines/foundations/color-system` | 2026-08-26 |
| Foundations | Typography | `/guidelines/foundations/typography` | 2026-08-26 |
| Foundations | Layout and spacing | `/guidelines/foundations/layout-and-spacing` | 2026-08-26 |
| Foundations | Elevation | `/guidelines/foundations/elevation` | 2026-08-26 |
| Foundations | Iconography | `/guidelines/foundations/iconography` | 2026-08-26 |
| Designer | Start designing | `/designing` | 2026-08-26 |
| Designer | Design installation (Figma) | `/design-installation` | 2026-08-26 |
| Developer | Start developing | `/developing` | 2026-08-26 |
| Principles | Accessibility Ease | `/thoughts/AccessibilityEase` | 2026-08-26 |
| Principles | Design tokens | `/thoughts/designToken` | 2026-08-26 |
| Principles | Local & global standards | `/thoughts/localAndGlobal` | 2026-08-26 |
| Components | **All 50 pages** | `/guidelines/components/{category}/{name}` | 2026-08-26 |
| Templates | **17** | `/guidelines/templates/*` — home-page, service-page, form-page, contact-us-page, help-page, faqs-page, search-page, sitemap-page, page-not-found, content-page, feedback-section, cookies-banner, chatbot, e-participation-page, about-page, founding-day, national-day | 2026-08-26 |
| Templates | **hajj-template** | `/guidelines/templates/hajj-template` | 2026-08-27 |
| Templates | **rating-section** | `/guidelines/templates/rating-section` — completes the set at **19** | 2026-08-27 |
| Designer | Designing for mobile | `/designing-for-mobile` | 2026-08-27 |
| Developer | Contributing | `/contributing` | 2026-08-27 |
| Principles | Atomic design | `/thoughts/atomic-design` | 2026-08-27 |
| Principles | Responsive design | `/thoughts/responsive-design` | 2026-08-27 |
| Principles | Consistency and unified identity | `/thoughts/consistency-and-unified-identity` | 2026-08-27 |
| Compliance | **Assessment Criteria** | `/AssessmentCriteria` — categories, compliance levels, 20-day review, score bands | 2026-08-27 |
| Other | About Platforms Code | `/about-platforms-code` | 2026-08-27 |
| Other | Support + 15 FAQs | `/support` | 2026-08-27 |
| Other | Roadmap | `/updates/roadmap` | 2026-08-27 |
| Other | Change log + 4 version pages | `/updates/change-log`, `/updates/change-log/version-history-1-0-{0,1,2,3}` | 2026-08-27 |

**Tokens:** 1,052 CSS custom properties extracted from `:root`, covering 41 colour families,
spacing, radius, shadow, width, container, and per-component role tokens.

## Outstanding

| Section | Count | Note |
|---|---|---|

| ~~Templates~~ | — | **Closed 2026-08-27** — `hajj-template` and `rating-section` harvested; all 19 templates captured. |
| ~~Designer~~ | — | **Closed 2026-08-27** — `/designing-for-mobile` captured. `/migration-guide` was never outstanding; it was captured 2026-08-26 into `dga-tokens-sync/references/library-migration.md` and this row was wrong. |
| ~~Developer~~ | — | **Closed 2026-08-27** — `/contributing` captured. |
| ~~Principles~~ | — | **Closed 2026-08-27** — all three captured; Thoughts is now 6 of 6. |
| ~~Other~~ | — | **Closed 2026-08-27** — `/support` (with its 15 FAQs), `/updates/roadmap`, `/updates/change-log` and its four version pages, `/about-platforms-code`, and `/AssessmentCriteria` captured. |
| Site | `/sitemap` | The site's own sitemap page. Navigation only — no rule on it. Not planned. |
| **Off-site** | Digital Transformation Measurement + Digital Experience Maturity indicators | Needed for `dga-launch-gate`; published outside this site |
| **Off-site** | **Assessment Criteria checklist file** | The *page* is now captured; the downloadable checklist itself is a separate file and is still not obtained |
| **Off-site** | PC 1.0 Figma files | Responsive radius/spacing values live only in the Figma variable collections |

> **Correction, 2026-08-27.** This row previously read *"All 19"* and listed `open-data` and
> `performance-statistics` as templates. Neither is a template route — both are **required
> sections inside** the e-Participation and About the Entity templates, and they are documented as
> such in `patterns.md`. The list also omitted `content-page` (which was captured) and
> `rating-section` (which was not). Actual coverage on 2026-08-26 was **17 of 19**, not 19. Found
> by extracting the site's own route table; raw evidence in `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-08-27-section-sweep.md`.


## Gaps — looked for, not found on the site

Recorded so a skill can distinguish "DGA is silent" from "we didn't check."

- **Motion tokens** — no durations or easings anywhere. But `prefers-reduced-motion` IS required,
  in three component pages (Filtration, Loading, Skeleton).
- **Arabic body typeface** — typography names IBM Plex Sans (the Latin family) and gives no
  Arabic face for body text. Saudi Font is restricted to national occasions, headings only.
- **Hijri calendar** — absent from the datepicker guideline, the live demo, and the official
  npm package.
- **Dark-mode guidance** — dark theme values exist in the token collections, but there is no
  page explaining when or how to use it.
- **Storybook** — linked from every component page, marked "soon", not yet live.
- **Card accessibility** — the page's section is Accordion's, pasted. No card guidance exists.
- **Menu accessibility** — no section at all.
- **Carousel pause control** — not required by DGA despite WCAG 2.1 AA 2.2.2.

## Downloads not yet obtained

- PC 1.0 Foundations · PC 1.0 icon pack · PC 1.0 Components Desktop UI Kit ·
  PC 1.0 Components Mobile UI Kit (Figma) — needed for responsive token values
- Saudi Font — licensed separately from the Ministry of Culture
- Assessment Criteria checklist (download link on `/designing` and `/developing`)

## Errors found in DGA's published documentation

Report to DS-DGA@dga.gov.sa. Detail in `skills/dga-design-system/references/foundations.md`.

1. Six rem↔px mismatches in the spacing, width and paragraph-max-width tables
2. `Shadows-shadow-2xl` Y-axis printed as `240`; shipped CSS is `24px`
3. Large-text contrast boundary stated differently on the colour page (24px) and the
   typography page (18.5 Bold / 24 Regular)
4. Button page lists five types in prose, four in the list
5. Button page's accessibility section contains four paragraphs about notification ARIA roles
6. Date picker's accessibility intro refers to "radio button components"
7. `--text-secondary` (#dba102) is designated a text role but fails WCAG AA on every light
   background in DGA's own palette — see `CONTRAST-AUDIT.md`
