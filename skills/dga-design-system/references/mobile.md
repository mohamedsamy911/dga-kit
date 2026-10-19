# Mobile

**Sources:** https://design.dga.gov.sa/guidelines/templates/* and https://design.dga.gov.sa/guidelines/components/* ·
**Retrieved:** 2026-08-26

> ✅ **`/designing-for-mobile` WAS harvested** — 2026-08-27, recorded in `capture-log.md`. It
> confirms the six Mobile UI Kit component names this file had assembled indirectly from the
> template and component pages. The page is a Figma download landing page and carries **no
> specs**. The six mobile component specs remain Figma-only; the responsive token values are now
captured (see *Responsive tokens* below).
>
> This note has now been wrong in both directions. It first cited the page as a source it had
> never read; the correction then over-swung and said the page was still outstanding, which
> contradicted the capture log for a full day.

DGA ships a **separate Mobile UI Kit** with components that do not exist in the web set. A
mobile screen built only from the web component list is missing DGA's own mobile vocabulary.

## Mobile-only components

| Component | Web equivalent |
|---|---|
| **Mobile Navigation Bar** | — |
| **Tap Bar** | — (bottom tab bar) |
| **Top Bar** | closest is Navigation Header, but distinct |
| **Splash Screen** | — |
| **Mobile Modal** | Modal, but a distinct mobile treatment |
| **Date Picker (mobile)** | Datepicker, distinct mobile variant |

`TODO(harvest)` — these have no public guideline pages; specs live in the **PC 1.0 Components –
Mobile UI Kit** Figma file. Get it before designing mobile screens.

## Responsive rules DGA states elsewhere

Gathered from the templates and components, since there is no consolidated mobile guideline:

| Context | Mobile behaviour |
|---|---|
| **Form steps** | **Radial Stepper** on mobile; Progress Indicator on large screens |
| **Breadcrumbs** | Back arrow + previous page link only |
| **Footer** | Stacks vertically below 600px |
| **Filtering** | Dropdown menu, not inline filters |
| **FAQ categories** | Max 5, then a dropdown |
| **Long titles** | Button below the content, stacked vertically — applied consistently |
| **Feedback section** | Buttons below the text |
| **Year of AI logo** | Stacked vertically (horizontal on desktop) |
| **Floating buttons** | Must not cover content; two stack vertically; 3+ go in an expandable menu |
| **Container padding** | 16px (32px desktop) |

## Responsive tokens

On Mobile, 39 component spacing values and 36 typography values change from Desktop — most shrink,
for example `card-lg-padding` 16px (32px on Desktop) and body `text-md` 12px (16px). Radius does
not change. DGA's CSS switches the spacing at `max-width: 767px`. Values and the known CSS defect:
`responsive-tokens.md`.
