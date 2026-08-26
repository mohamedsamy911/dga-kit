---
name: dga-brand-overlay
description: Record and apply one entity's brand layer on top of the DGA Platforms Code baseline — where the entity's identity may override DGA and where DGA always wins. Also the single place a project records the decisions DGA leaves open (numerals, calendar, RTL mirroring, Arabic typeface). Use when entity-specific branding, logos or colours are involved, or when a project needs to settle a question DGA does not answer.
tags:
  - dga
  - platforms-code
  - saudi
  - branding
  - project-decisions
---

# Entity brand overlay

DGA Platforms Code is the baseline for every Saudi government platform. Your entity's own
identity sits **on top of it**, and only in the places DGA leaves open.

This skill is deliberately separate from `dga-design-system` so the DGA core stays reusable
across entities. **Fork this file per project** — it is a template with blanks, not a reference.
Everything here is either a DGA constraint (fixed) or a `TODO(entity)` your project fills in once
and every other skill then reads.

## What DGA fixes, and no entity can change

These are compliance requirements, not style preferences. An entity brand guideline that
contradicts one of these loses.

- **Header and footer structure, colours and fonts.** DGA repeats on every template page:
  *"adhere strictly to the original structure and style. Do not alter the colors or fonts."*
- **The Digital Stamp** and its verification content
- **Typography** — IBM Plex Sans. Saudi Font only on occasion templates, headings only, with a
  Ministry of Culture licence
- **The required page furniture** — feedback section, both last-modified dates, skip link,
  Accessibility Tools in the footer
- **Component anatomy and the six states**
- **The colour roles themselves.** An entity may supply brand colours; it may not repoint
  `text.default` at one that fails contrast. Run
  `../dga-design-system/assets/check-contrast.mjs` against any override before adopting it.

## What the entity supplies

| Item | Status |
|---|---|
| Logo asset and its size in the header (DGA's reference is 125 x 42px), built as a component | `TODO(entity)` |
| Entity brand colours, and exactly where they may sit alongside DGA tokens | `TODO(entity)` |
| **DGA registration number** + **License Number** for the Digital Stamp | `TODO(entity)` — **chase early, this is procurement, not code** |
| Domain — `gov.sa` for ministries, authorities, public institutions, councils and national centres; `edu.sa`, `med.sa`, `sch.sa` and others per DGA's table | `TODO(entity)` |
| Entity-specific content for About the Entity (see `dga-launch-gate`) | `TODO(entity)` |
| Arabic and English entity name, exactly as registered | `TODO(entity)` |

## Project-level decisions DGA leaves open

DGA publishes no policy on any of these. Decide once, record the answer **here**, and every other
skill reads it rather than guessing. An inconsistent answer across a product is worse than either
choice.

| Decision | Options | Recorded answer |
|---|---|---|
| **Numeral system** | Arabic-Indic (٠١٢٣) or Western (0123) | `TODO(entity)` |
| **Calendar** | Hijri, Gregorian, or both side by side | `TODO(entity)` |
| **Arabic body typeface** | DGA names only the Latin IBM Plex Sans. IBM Plex Sans Arabic is the obvious intent but is not stated — confirm with DS-DGA@dga.gov.sa | `TODO(entity)` |
| **Locales shipped** | `ar` only, `ar` + `en`, others | `TODO(entity)` |
| **Motion durations and easings** | DGA publishes none. `prefers-reduced-motion` **is** required in three places | `TODO(entity)` |
| **Dark theme** | DGA documents dark values but publishes them only in Figma | `TODO(entity)` |

Once filled in, these are binding on `dga-rtl-i18n`, `dga-ui-adapter`, `dga-react` and
`dga-mockup`. Until filled in, those skills must say "the project has not decided" rather than
picking silently.

## Where an override is legitimate

Narrow, and worth stating precisely so it is not used as a loophole:

- **Accent and illustration colour** in content areas, provided every text pairing still clears
  WCAG AA
- **Photography, iconography style and illustration** within DGA's iconography rules
- **Tone of voice** in Arabic copy — DGA gives content rules but no house voice
- **Product-specific components** DGA does not specify at all

Everything else inherits. When you are unsure whether something is an override or a violation,
it is a violation — ask DGA at DS-DGA@dga.gov.sa rather than shipping and finding out at
assessment time.
