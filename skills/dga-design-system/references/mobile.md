# Mobile

**Sources:** https://design.dga.gov.sa/guidelines/templates/* and https://design.dga.gov.sa/guidelines/components/* ·
**Retrieved:** 2026-08-26

> ✅ **`/designing-for-mobile` WAS harvested** — 2026-08-27, recorded in `capture-log.md`. It
> confirms the six Mobile UI Kit component names this file had assembled indirectly from the
> template and component pages. The page is a Figma download landing page and carries **no
> specs**. The specs come from DGA's Figma files instead: the mobile components below (read
> 2026-10-20) and the responsive tokens (read 2026-10-19).
>
> This note has now been wrong in both directions. It first cited the page as a source it had
> never read; the correction then over-swung and said the page was still outstanding, which
> contradicted the capture log for a full day.

DGA ships a **separate Mobile UI Kit** with components that do not exist in the web set. A
mobile screen built only from the web component list is missing DGA's own mobile vocabulary.

## Mobile-only components

DGA's `/designing-for-mobile` page names six: Mobile Navigation Bar, Tap Bar, Top Bar, Splash
Screen, Mobile Modal, Date Picker. There are no guideline pages for them; what follows is from
DGA's Figma file **Mobile Components - Platforms Code** (CC BY 4.0; its page said "last updated 2 years ago"),
read 2026-10-20. Sizes are as drawn on a 375px frame. Evidence: `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-20-figma-mobile-components.md`.

| Site name | In DGA's Figma file | Web equivalent |
|---|---|---|
| **Mobile Navigation Bar**, **Top Bar** | The file's *Navigation Bar* page holds one component set, **Top Bar**, 102px tall: styles Three Actions / Two Actions / Text Actions / Title / Logo; used as the Main or an Internal top bar; optional info text; white, with a bottom border. No component is named Mobile Navigation Bar, so whether the site's two names are one component is not established | closest is Navigation Header |
| **Tap Bar** | **Tab Bar**, 84px tall, normal or on-colour (brand green); selection variants Tab 1 to Tab 5 and No Selected. Each tab item 46×70: icon over label, optional tag; states Normal / Pressed / Selected | — |
| **Splash Screen** | One full-screen frame (375×812); no component | — |
| **Mobile Modal** | 375px wide, **top corners rounded** (`radius-lg`), bottom corners square — a shape that suggests presentation from the bottom edge (an inference; the file draws shape, not placement). Header, body, and actions that can stack | Modal |
| **Date Picker (mobile)** | 375×696, square corners, Range or Select date; date cells 44×44 with a slot for a second date | Datepicker |
| — (not on the site's list) | **Nav Drawer**, 327px wide, green or white, optional overlay; items 44px tall, two levels | Navigation drawer |

"Tap Bar" is spelled "Tab Bar" in the file.

**Also in the file:** buttons are 44 / 40 / 32px tall (Large / Medium / Small); a floating action
button (`Fab_Button`) is 44px tall and fully rounded; 45 of the 57 component sets have an `RTL`
variant, and most sets that carry text have paired English and Arabic text properties.

> ⚠️ **Close buttons come in 20 and 24px sizes.** WCAG 2.2 SC 2.5.8 (AA) needs a 24×24 CSS px
> target unless the target has enough space around it, so the 20px size needs that spacing to
> pass. Kit policy: use the 40px size, or pad the hit area to 44px.

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
