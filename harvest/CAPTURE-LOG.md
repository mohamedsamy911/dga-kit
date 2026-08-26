# Capture log

Evidence trail for every DGA rule this kit asserts.

**Source:** https://design.dga.gov.sa/ — "Platforms Code", National Design System of Saudi Arabia
**Site footer version:** © 2025 · **Design kit version:** PC 1.0
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
| Templates | **18 of 19** | `/guidelines/templates/*` — home, service, form, contact-us, help, faqs, search, sitemap, page-not-found, feedback-section, cookies, chatbot, e-participation, open-data, performance-statistics, about-the-entity, founding-day, national-day | 2026-08-26 |

**Tokens:** 1,052 CSS custom properties extracted from `:root`, covering 41 colour families,
spacing, radius, shadow, width, container, and per-component role tokens.

## Outstanding

| Section | Count | Note |
|---|---|---|

| Templates | **1** | `hajj` only. The other 18 are captured — see the table above. Corrected 2026-08-27: this row previously listed 13 and was stale. |
| Designer | `/designing-for-mobile` | |
| Developer | `/migration-guide`, `/contributing` | |
| Principles | `/thoughts/atomic-design`, `/responsive-design`, `/consistency-and-unified-identity` | |
| Other | `/support`, `/updates/roadmap`, `/updates/change-log`, FAQ, Assessment Criteria | |
| **Off-site** | Digital Transformation Measurement + Digital Experience Maturity indicators | Needed for `dga-launch-gate`; published outside this site |
| **Off-site** | PC 1.0 Figma files | Responsive radius/spacing values live only in the Figma variable collections |

## Counted but not enumerated — `TODO(verify)`

- **DGA's own explicit RTL statements.** The harvest recorded a count of six but never listed
  which pages they are, so the number is unciteable and a later review named four. On the next
  visit, enumerate the pages where DGA *itself* states an RTL rule and record the list, not a
  total. Do not conflate it with the kit's derived per-component RTL guidance in `components.md`,
  which is a larger and different set.

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
