---
name: dga-design-system
description: Canonical Saudi DGA (Digital Government Authority) design system reference — foundations, components, patterns, accessibility, Arabic content rules and design tokens. Use when answering any question about DGA design rules, looking up a token value or component spec, or when another DGA skill needs the source of truth.
---

# DGA design system

The single source of truth for design.dga.gov.sa in this project. Every other `dga-*` skill
reads from here rather than carrying its own copy of the rules.

> ## Harvest complete — interpretation unverified
>
> **Populated and citable:** all 8 reference files. 5 foundations, **50 component pages**,
> **19 templates**, and **1,052 design tokens** taken verbatim from the live site's CSS custom
> properties. Every rule carries a source URL and retrieval date.
>
> **Known gaps, stated so no answer implies coverage it lacks:** the Digital Transformation and
> Digital Experience Maturity indicators (published outside design.dga.gov.sa); the responsive
> radius/spacing and dark-theme values (PC 1.0 Figma variable collections only); the six
> mobile-only component specs; the Hajj template.
>
> ⚠️ **No designer sign-off yet.** Values are exact; interpretation is not verified.

## The one rule

**Cite or omit.** Every rule in `references/` carries its source URL and retrieval date. Where
DGA is silent on something, say so plainly and name the fallback you're applying. Never present
a general best practice as a DGA requirement, and never invent a token value — a compliance
reference that is confidently wrong is worse than no reference.

When you state a rule, give the citation with it. When you can't, say which file you'd expect
it in and that it isn't there.

## Where things are

| Question about… | Read |
|---|---|
| Colour, type scale, spacing, grid, radii, elevation, icons, motion | `references/foundations.md` |
| A specific component — anatomy, variants, states, RTL notes, ARIA | `references/components.md` |
| Page templates, forms, tables, search, auth, errors, empty states | `references/patterns.md` |
| Accessibility requirements and their WCAG mapping | `references/accessibility.md` |
| Arabic-first rules, tone, glossary, numerals, date and currency formats | `references/content.md` |
| Entity logo lockups, co-branding, clear space, favicons | `references/brand.md` |
| Mobile — mobile-only components and responsive rules | `references/mobile.md` |
| Contrast pairings that pass and fail | `references/CONTRAST-AUDIT.md` |
| Machine-readable values | `assets/tokens.json` · `assets/tokens.css` · `assets/tailwind-preset.js` |
| What was captured, from where, and when | `references/capture-log.md` · `dga-version.md` |

Read only the file the question needs. These are large; loading all six for a question about
button radius wastes the context the answer needs.

## Quick reference — the 20 rules

Verbatim DGA requirements, inline so a partial load of this skill is still useful.
Everything here is cited in `references/`.

**Colour**
1. Small text (<24px) **≥4.5:1** · large text **≥3:1** · UI components and graphics **≥3:1**
2. **`--text-secondary` (#dba102) fails AA on every light background — 2.30:1.** Never use it as
   text on a light surface. `secondary-gold-800` (#945c01) is the first compliant step.
3. `-light` text tokens are **dark-surface only**
4. Text from Gray 500/600/700/950 on backgrounds ≤400; white text on backgrounds ≥500

**Typography**
5. **IBM Plex Sans** for everything. **Saudi Font is national/seasonal occasions only, main
   headings only** — never body or long-form
6. Display styles for headings only, never body copy
7. Body line height **≥1.5×** font size
8. Display 2xl–md carry **−2% tracking — never apply it to Arabic** (breaks the connected script)

**Layout**
9. 12 columns desktop, 2–4 smaller. Breakpoints **600 / 960 / 1280**
10. Container padding **16px mobile / 32px desktop**, max width **1280px**, paragraph **720px**
11. Spacing on the scale: 0·2·4·6·8·12·16·20·24·32·40·48·64·80·96·128·160
12. **Target size ≥44×44px**

**Components**
13. Six states: **Default · Hovered · Pressed · Selected · Focused · Disabled**
14. Icons: 10/14/16 XS · 18/20 S · **24 standard** · 28/32 L. Avatars: 24/32 S · **40/48 M** ·
    64/80/120 L
15. **Content switcher takes 2–4 options only** — use Tabs beyond four
16. **Charts: pie max 6 segments, line and bar max 3 series**
17. Breadcrumbs truncate past **five** items; mobile shows back arrow + previous page only
18. Tabs never scroll or wrap — **overflow goes to a More button**
19. Notifications: **no timeout on critical**, **≥5s** if auto-dismissing
20. **Links are underlined**, and "click here" / "go to" are forbidden as link text

**Two things DGA requires that teams routinely miss**
- The **footer must contain Accessibility Tools** — font size and contrast controls. A feature,
  not styling.
- A **skip-to-content link** at the start of every page.

**And one it doesn't provide**
- **No Hijri calendar** — not in the guidelines, not in the demos, not in the npm package.
  you build it.

## Related skills

- `dga-design-review` — audits a design against these rules
- `dga-react` — builds React components that implement them
- `dga-rtl-i18n` — Arabic-first layout and localisation mechanics
- `dga-a11y` — runs the accessibility checks against real code
- `dga-brand-overlay` — where the entity's own identity overrides this baseline, and where it doesn't
