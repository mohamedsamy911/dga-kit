# Foundations

**Source:** https://design.dga.gov.sa/guidelines/foundations/* · **Retrieved:** 2026-08-26
**System:** "Platforms Code" — National Design System of Saudi Arabia, published by DGA
**Verified by:** — *(designer sign-off outstanding)*

Machine-readable values live in `../assets/tokens.json`, extracted verbatim from the site's
own CSS custom properties (1,052 of them). Prefer those over anything transcribed here.

---

## Colour

Primary green references the flag of the Kingdom of Saudi Arabia — DGA states it was chosen
to symbolise "growth, prosperity, unity, cooperation, and national solidarity."

Three palette groups: **neutral**, **primary**, **semantic**. Secondary is split into **gold**
(richness, prestige, emphasis) and **lavender** (calm, accent, contrast). Semantic: red=error,
yellow=warning, blue=info, green=success. Twelve grades per hue, plus black and white.

DGA's stated contrast requirements:

> Small Text: below 24 px must have a contrast ratio of at least 4.5:1.
> Large Text: 24 px and larger, no less than 3:1.
> Graphical Elements and UI Components: minimum 3:1.
> — /guidelines/foundations/color-system · retrieved 2026-08-26

⚠️ **DGA contradicts itself on the large-text boundary.** The typography page states the
standard WCAG definition instead:

> Level (AA) for large text (above 18.5 Bold or 24 Regular): 3:1
> — /guidelines/foundations/typography · retrieved 2026-08-26

**Take the stricter reading:** treat 24px regular as the boundary and require 4.5:1 below it.
Raise with DGA.

Pairing rule DGA gives for neutrals:

> use text colors like (Gray 500, Gray 600, Gray 700, and Gray 950) for lighter backgrounds
> with a number 400 and below. For backgrounds numbered 500 and above, use white text.
> — /guidelines/foundations/typography · retrieved 2026-08-26

**See `CONTRAST-AUDIT.md`** — one DGA text token fails AA on every light background in DGA's
own palette.

---

## Typography

**Two families:**

| Family | Role | Weights |
|---|---|---|
| **IBM Plex Sans** | Everything | Regular, Medium, Semibold, Bold |
| **Saudi Font** (Ministry of Culture) | National and seasonal occasions **only** — National Day, Founding Day. **Main headings only.** | Regular, Bold |

DGA is explicit that Saudi Font must not be used for paragraph or long-form text. It requires
a licence from the Ministry of Culture.

⚠️ **Open question — no Arabic typeface is specified for body text.** The page names "IBM Plex
Sans… developed by IBM in collaboration with Bold Monday, released 2017," which is the Latin
family. IBM Plex Sans Arabic exists and is the obvious intent, but the guideline does not say
so, and for an Arabic-first government system that is a material gap. **Confirm with DGA
(DS-DGA@dga.gov.sa) before locking the font stack.** `TODO(verify)`

**Two style groups.** *Display* for headings at large sizes; *Text* for body, labels and UI.
DGA is explicit that display styles are reserved for headings, never body copy.

### Display

| Style | Size | Line height | Tracking |
|---|---|---|---|
| Display 2xl | 72px / 4.5rem | 90px / 5.625rem | −2% (CSS: `-0.02em`) |
| Display xl | 60px / 3.75rem | 72px / 4.5rem | −2% (CSS: `-0.02em`) |
| Display lg | 48px / 3rem | 60px / 3.75rem | −2% (CSS: `-0.02em`) |
| Display md | 36px / 2.25rem | 44px / 2.75rem | −2% (CSS: `-0.02em`) |
| Display sm | 30px / 1.875rem | 38px / 2.375rem | — |
| Display xs | 24px / 1.5rem | 32px / 2rem | — |

### Text

| Style | Size | Line height |
|---|---|---|
| Text xl | 20px / 1.25rem | 30px / 1.875rem |
| Text lg | 18px / 1.125rem | 28px / 1.75rem |
| Text md | 16px / 1rem | 24px / 1.5rem |
| Text sm | 14px / 0.875rem | 20px / 1.25rem |
| Text xs | 12px / 0.75rem | 18px / 1.125rem |
| Text 2xs | 10px / 0.625rem | 14px / 0.875rem |

⚠️ **Negative tracking (−2%) on the display sizes must not be applied to Arabic.** Arabic is a
connected script and letter-spacing breaks the joins. Scope tracking to Latin runs only —
see `../../dga-rtl-i18n/references/rtl-rules.md`.

⚠️ **CSS `letter-spacing` does not accept percentages.** Percentages were proposed in
css-text-4 and never shipped, so `letter-spacing: -2%` is silently dropped by every browser.
`tokens.json` keeps DGA's published `-2%` — it is the harvested value, and a re-harvest must
diff clean against it. `generate-tokens.mjs` converts it to `-0.02em` at the boundary, so all
generated CSS and Tailwind output is valid. **Never hand-write `-2%` into a stylesheet**, and
never "correct" the value in `tokens.json`.

⚠️ **Text 2xs is 10px.** Below any reasonable minimum for body copy. Use for non-essential
metadata only, never for content a user must read.

DGA's own typography guidance: set generous line height, keep line length moderate, prioritise
readable body sizes, and keep spacing consistent.

---

## Layout and spacing

**Grid:** 12 columns on desktop, reducing to 2–4 on smaller aspect ratios. Columns, margins
(outer edge to content) and gutters (between columns).

**Breakpoints:**

| Name | Range | Breakpoint |
|---|---|---|
| Small — Mobile | 0–599 | 600 |
| Medium — Tablet | 600–959 | 960 |
| Large — Desktop | 960–1279 | 1280 |
| X Large — Desktop | 1280+ | 1280+ |

**Spacing scale** (documented names — note these differ from the CSS variables actually
shipped on the site, which expose only `none` through `xl` under these names plus a parallel
numeric scale):

`none` 0 · `xxs` 2 · `xs` 4 · `sm` 6 · `md` 8 · `lg` 12 · `xl` 16 · `2xl` 20 · `3xl` 24 ·
`4xl` 32 · `5xl` 40 · `6xl` 48 · `7xl` 64 · `8xl` 80 · `9xl` 96 · `10xl` 128 · `11xl` 160 (px)

**Containers:** mobile padding 16px · desktop padding 32px · desktop max-width 1280px ·
paragraph max-width 720px.

### ⚠️ Errors in DGA's own tables

The rem and px columns disagree in several rows. The **px values are the ones that match the
shipped CSS variables** — use px, ignore the rem column:

| Row | DGA says | Actual |
|---|---|---|
| `spacing-7xl` | 5rem = 64px | 5rem is 80px; 64px is 4rem |
| `spacing-8xl` | 6rem = 80px | 6rem is 96px |
| `spacing-9xl` | 7rem = 96px | 7rem is 112px |
| `spacing-11xl` | 11rem = 160px | 11rem is 176px |
| `width-xs` | 34rem = 384px | 34rem is 544px; 384px is 24rem |
| `paragraph-max-width` | 20rem = 720px | 20rem is 320px; 720px is 45rem |
| `Shadows-shadow-2xl` Y-axis | 240 | CSS ships 24px — the doc has a stray digit |

Report these to DS-DGA@dga.gov.sa.

### Accessibility rules DGA states here

- Reading order must match visual order; use landmark elements (`header`/`nav`/`main`/`footer`)
- Group related items with spacing, borders, fieldsets, ARIA roles
- **Minimum target size 44×44px** for interactive elements
- Text contrast at least 4.5:1
- **Line height at least 1.5× font size** for body text
- Layout must be responsive across sizes and orientations

---

## Responsive design

**Source:** /thoughts/responsive-design · retrieved 2026-08-27

DGA's framing, which is worth quoting when responsiveness is treated as a nice-to-have:

<!-- dga -->
> Responsive design is particularly crucial for **government websites**, which must serve diverse
> audiences with different devices and accessibility needs.
<!-- /dga -->

**Stated for developers**

- **Mobile-first.** *"Start by designing for the smallest screens and progressively enhance the
  design for larger screens."* It is also part of a **Mandatory** assessment criterion (Layout and
  Spacing) — see `../../dga-launch-gate/references/assessment-criteria.md`
- **CSS Flexbox and Grid** for adaptive layouts
- **Media-query breakpoints** — *"Use common breakpoints but also tailor them to the design's
  needs"*. The concrete values are in the breakpoint table above, from the Layout and spacing page
- **Container queries** — DGA says *"when they become widely supported"*. That hedge is now stale;
  container queries are baseline in current browsers. Treat DGA's caution as dated, not as a ban

**Stated for designers**

- **Relative units for type** — *"like 16px (1em, 1rem)"*, adjusting sizes and line heights for
  legibility on small and large screens
- **Fluid grids** that adjust to screen size
- **Touchscreen navigation** — interactive elements *"appropriately sized and spaced for touch
  inputs"*. No pixel figure **on this page** — but DGA states **44×44px** on
  `/guidelines/foundations/layout-and-spacing` (see *Accessibility rules DGA states here*, above),
  so cite **DGA** for the number.
  ⚠️ Do **not** attribute it to WCAG 2.1 AA. WCAG 2.1's target-size criterion, **2.5.5, is Level
  AAA** — not AA. (The AA criterion, 2.5.8 Target Size (Minimum), at 24×24px, arrived in WCAG
  **2.2**.) An earlier version of this line called 2.5.5 "AA", which contradicted
  `../../dga-ui-adapter/SKILL.md`, where the kit already had it right. DGA's own 44px rule is
  stricter than either, so citing it loses nothing.
- **Content hierarchy** — essential information prominent and reachable on small screens

### ⚠️ DGA contradicts itself on the tablet grid

| Page | Tablet columns |
|---|---|
| `/guidelines/foundations/layout-and-spacing` | *"reducing to **2–4** on smaller aspect ratios"* |
| `/thoughts/responsive-design` | *"e.g., 12-column grid for desktop, **8-column grid for tablet**"* |

Both are DGA's. **Cite the Layout and spacing page** — it is the foundation page, it is specific,
and the Thoughts page marks its own figures as an example (`e.g.`) rather than a rule. Do not
present 8 columns as a DGA requirement. Recorded in `https://github.com/mohamedsamy911/dga-kit/blob/master/COVERAGE.md`.

DGA names **no mobile column count** on either page.

## Elevation

Seven shadow steps (`xs` → `3xl`), several of which are two-layer for a smoother falloff.
All use `#101828` at varying opacity. Exact values in `tokens.json`.

Four backdrop-blur steps: 8, 16, 24, 40. DGA warns blur can harm text readability — use
sparingly.

**Accessibility:** depth cues alone are not sufficient. Pair elevation with borders or
outlines, and make hover/focus state changes visible by something other than shadow — colour
change or underline — for users who don't perceive depth.

---

## Iconography

**Platforms Code Icons** is the mandated set. For designers it ships as a Figma icon library
and SVG assets; for developers it is **included by default in all DGA packages — no separate
install**.

**Icon categories:** Main (system icons), Item (containers), Featured (styled containers for
alerts and page content), Feedback response (success/error), Rating star, Social media logos,
National flags (for nationality and phone fields), Integration tools, Payment methods, Help.

**Sizes:**

| Band | Sizes | Use |
|---|---|---|
| Extra small | 10, 14, 16px | Very narrow spaces — small buttons, badges |
| Small | 18, 20px | Small and XS badges |
| **Medium** | **24px** | **Standard for most components** |
| Large | 28, 32px | Sparingly, to highlight content in spacious areas |

**Accessibility requirements DGA states:**

- Meaningful icons need a text alternative — `alt`, `aria-label`, or `aria-labelledby`
- Decorative icons must be hidden: `aria-hidden="true"` or `alt=""`
- Inline SVG icons need `role="img"` plus an accessible name
- CSS background-image icons need adjacent text — screen readers can't reach them
- Interactive icons: **at least 44×44px** target, with adequate surrounding spacing

---

## Not covered by DGA

Looked for, not found on the site:

- **Motion / animation** — no durations, easings or motion guidance page exists in the sitemap.
  Fall back to a stated house default and label it as such.
- **Arabic body typeface** — see the typography warning above.
- **A dark-mode *page*** — but dark theme itself IS defined; see "Token architecture" below.
  What's missing is prose guidance on when to use it.


---

## Token architecture

**Source:** /thoughts/designToken · retrieved 2026-08-26

Two collection types, and the distinction matters for how `dga-react` consumes them:

**Primitive (foundational)** — raw values with no contextual meaning: the colour ramps, the
spacing and radius scales. Never reference these directly in component code.

**Semantic (context-specific)** — primitives abstracted into named intent. Three collections:

| Collection | Structure |
|---|---|
| **Theme** | Per-component colour choices, each with **Light and Dark variants** |
| **Radius** | Per-component, with **Desktop / Tablet / Mobile** variants |
| **Spacing & width** | Per-component, with **Desktop / Tablet / Mobile** variants |

Two consequences worth planning around:

1. **Dark theme is a first-class part of the system — and it is broken.** DGA's own example:
   `control-primary-hovered` resolves to `Primary-SA-Flag/800` in light and `/300` in dark.
   Build components theme-aware from the start; retrofitting is far more expensive.

   **The values are public.** All **402** dark role declarations ship in the site's CSS bundle
   and are captured in `../assets/tokens.json` under `role.dark` — 390 of them remaps of
   primitives already in the light palette, so dark is a *role remap layer*, not a second palette.

   > 🚩 **DGA's dark theme cannot activate.** It is published under `[data-theme=dark] :root`,
   > a selector that can never match: `:root` is `<html>`, and a descendant combinator requires
   > an ancestor it does not have. Verified in the live page — 0 elements matched, no computed
   > value changed, and the bundle contains no `prefers-color-scheme` rule and no `.dark` class.
   > The corrected form is `:root[data-theme="dark"]`. Report the defect to DS-DGA@dga.gov.sa.

   > 🚩 **This kit does not ship a dark stylesheet either, and that is deliberate.** Upstream the
   > theme is inert, and inert is safe. Emitting the corrected selector would activate it for any
   > consumer already using `data-theme="dark"` — Chakra v3 does, out of the box — turning a
   > harmless upstream bug into a live accessibility regression in someone else's product. It
   > also cannot be made safe from DGA's own values: `text.error` and `text.primary` have cited
   > substitutes, but the five `*-light` status surfaces have **none** — every dark variant DGA
   > publishes for them, under `notification-`, `tag-` and `featuredicons-`, still resolves to the
   > same near-white value. Inventing a dark tint would break cite-or-omit.

   > ⚠️ **Enabling dark is not a free win.** Five `*-light` status surfaces are not remapped, so
   > white text lands on a near-white background at **1.05:1**; `text.error` (#b42318) is
   > **2.68:1** on the dark body, failing at every size; `text.primary` drops to **3.71:1**,
   > large text only. Meanwhile `text.secondary` — the light theme's failure — *passes* at
   > **7.64:1**. Run `node ../assets/check-contrast.mjs --theme dark` and read
   > `tokens.json role.dark.$verify` before shipping dark mode.
2. **Radius and spacing are responsive tokens, not fixed values.** The same semantic token
   resolves differently on desktop, tablet and mobile. A React implementation that treats
   `radius-md` as a constant will be wrong on two of three breakpoints. `TODO(harvest)` — the
   per-breakpoint values are in the Figma variable collections, not exposed as CSS variables on
   the site. Get them from the "PC 1.0 Foundations" Figma file.

---

## Compliance context

**Source:** /thoughts/localAndGlobal · retrieved 2026-08-26

Adopting Platforms Code is not only a design decision — it feeds two measurement regimes the entity
will be scored against, both tied to Saudi Vision 2030:

- **Digital Transformation Measurement Indicator** — diagnoses an entity's current state and
  tracks progress against digital-transformation standards.
- **Digital Experience Maturity Indicator** — measures maturity of platforms and services,
  beneficiary satisfaction, and community participation.

DGA states the system aligns with United Nations requirements, feeding the Kingdom's standing
in international digital-government indices.

This is what `dga-launch-gate` checks against. Both indicators need their own harvest — they
are published outside design.dga.gov.sa. `TODO(harvest)`

DGA's own **Assessment Criteria** — the rubric a project is actually scored against before
go-live — *is* published on the site and is captured in
`../../dga-launch-gate/references/assessment-criteria.md`.

---

## Atomic design — DGA's IA vocabulary

**Source:** /thoughts/atomic-design · retrieved 2026-08-27

<!-- dga -->
> We adopt an atomic design methodology to ensure organization and sustainability in the
> development of user interfaces.
<!-- /dga -->

This matters because it is **DGA's own vocabulary**, not a generic methodology reference. When an
architect or a handoff names a layer, use these five words — they are the terms a DGA reviewer
will use back.

| Level | DGA's definition | DGA's example |
|---|---|---|
| **Atoms** | *"basic building blocks […] that cannot be broken down any further without losing their functionality"* | buttons, input fields, labels |
| **Molecules** | *"relatively simple groups of UI elements functioning together as a unit"* | a form label + input + button = a search form |
| **Organisms** | *"relatively complex components made up of groups of molecules and/or atoms"* | a navigation bar with logo, search form and menu items |
| **Templates** | *"groups of organisms combined to form page layouts"*, focused on content structure | — |
| **Pages** | *"specific instances of templates […] with real content and data"* | — |

Stated benefits: Consistency · Scalability · Collaboration · Maintainability · Flexibility.

**Use it to organise your own project, not to relabel DGA's.** DGA publishes the methodology and
publishes a flat set of 50 components; it never says which component sits at which level. So:

- ✅ *"In our inventory we are treating the search bar as a molecule composed of Input and Button."*
  — your classification, your project's structure.
- ❌ *"DGA classifies Card as an organism."* — DGA says no such thing.

The useful test is decomposition, not labelling: if a screen will not break down into the DGA
components you already have, that is the signal to check whether a genuinely custom component is
being invented — and to price it. See `dga-frontend-architect` decision 8.

> ⚠️ DGA's own `/guidelines/components/` groups the 50 components by **function** — Actions,
> Content Display, Data Display, Feedback, Forms and Inputs, Loading and Status, Navigational,
> Search and Filters, UI Shell. Those nine categories, not the five atomic levels, are DGA's
> published classification. Cite the categories; use the levels as a method.

---

## Contributing back to DGA

**Source:** /contributing · retrieved 2026-08-27 · also /support

Where to send a defect found in DGA's published documentation — this kit has a list of seven in
`capture-log.md`.

**Is it worth contributing?** DGA's four tests: **Relevance** (fixes an issue or meaningfully
enhances the platform) · **Broad impact** (benefits the majority, not niche cases) · **Minor
enhancements** (bug fixes, new icons — *"always valuable"*) · **Major additions** (new components
need thorough evaluation).

**The four steps, and their real status:**

| # | Step | Status on 2026-08-27 |
|---|---|---|
| 1 | Familiarize yourself with core principles and components | live |
| 2 | Join the community — forums, community meetings | **"soon"** |
| 3 | Follow contribution guidelines on the GitHub page | **"soon"** |
| 4 | Submit contributions via GitHub with a clear description | Submit |

Types accepted: **design**, **code**, **documentation**.

> 🚩 **There is no published GitHub URL and no published contribution guideline.** Steps 2 and 3
> are both marked *"soon"*, and the page names no repository. Until that changes, the only working
> route is **DS-DGA@dga.gov.sa**. Do not tell anyone to open a pull request against a repository
> this kit cannot name.

> `/support` describes a **"beem community"** as a support channel and a **Storybook** for
> developers. Neither is live — Storybook is marked "soon" on every component page. Several
> `/support` answers are also written for an internal DGA audience (*"our organization"*,
> *"internal communication platforms"*). Treat that page as intent, not as a citeable rule.
