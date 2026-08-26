---
name: dga-ui-adapter
description: Apply Saudi DGA "Platforms Code" rules to a project built on ANY UI library — Tailwind, MUI, Chakra, shadcn/Radix, Ant Design, Bootstrap, Vue/Angular kits, or plain CSS. Use when a .gov.sa or Saudi government platform must be DGA-compliant but does not use DGA's own React package. Covers wiring the DGA tokens into your theme, mapping all 50 DGA component specs onto whatever your library calls them, the rules that fail an audit while passing a build, and the components no library ships.
tags:
  - dga
  - platforms-code
  - saudi
  - ksa
  - design-system
  - compliance
  - accessibility
  - rtl
---

# DGA compliance on any UI library

A Saudi government platform must satisfy **Platforms Code** — the National Design System of
Saudi Arabia, published by the Digital Government Authority at design.dga.gov.sa. Compliance is
**scored**, not stylistic: the entity is assessed against the Digital Transformation and Digital
Experience Maturity indicators.

DGA ships its own React library (`platformscode-new-react`). Most projects don't use it. This
skill is the bridge: **DGA's rules, expressed against whatever library you already have.**

| Question | Skill |
|---|---|
| What does DGA actually *say*? | `dga-design-system` |
| The project uses DGA's own `platformscode-new-react` | `dga-react` |
| **The project uses any other UI library** | **this skill** |
| Arabic typography, bidi, Hijri dates, numerals | `dga-rtl-i18n` |
| Is this design compliant? | `dga-design-review` |
| Is this running app accessible? | `dga-a11y` |
| Is the platform ready to launch? | `dga-launch-gate` |

## What adapting costs, stated honestly

When you don't use DGA's library you lose DGA's own implementation as a reference. Every
component spec has to be re-expressed in your library, and *"does this match DGA"* becomes a
judgement instead of a diff. This skill exists to make that judgement repeatable — and to stop
the specific mistakes that pass a build, a type check and a casual review.

## Step 1 — wire the tokens once, at the theme layer

All 1,052 DGA values are already extracted and machine-readable:

| File (in `../dga-design-system/assets/`) | Use it when |
|---|---|
| `tokens.json` | Your library takes a JS/TS theme object — MUI, Chakra, Ant, styled-components, vanilla-extract, Style Dictionary |
| `tokens.css` | Your library is CSS-variable-driven — shadcn/Radix, Tailwind v4, Bootstrap 5.3+, Web Components, plain CSS |
| `tailwind-preset.js` | Tailwind v3 |

Per-library wiring snippets: `references/token-wiring.md`.

**Tokens are owned by exactly one place** — your theme provider, root stylesheet or Tailwind
config. Nothing downstream re-declares them. A component that reaches past the theme for a hex
is the failure this whole layer exists to prevent.

## Step 2 — the rules

Eight rules. Each is library-independent, and each one has burned somebody.

1. **Never hardcode a colour.** Reference the semantic role (`text-default`, `background-card`),
   never a primitive (`neutral-900`), never a literal. DGA is explicit that primitives "lack
   contextual meaning"; the semantic layer is what lets a dark theme land later without touching
   components.

2. **🚩 `text.secondary` is not a text colour.** DGA designates gold `#dba102` as a *text* role
   and it measures **2.30:1 on white** — under the 4.5:1 small-text threshold *and* under the
   3:1 large-text one. There is no size at which it is compliant on a light surface. Same for
   `text.primary-light`, `text.secondary-light` and `text.tertiary-light`, which are dark-surface
   tokens. The name invites the mistake and reviewers defer to it, because it *is* a real DGA
   token. Need gold text on white? `secondary-gold.800` (#945c01) is the first step that clears
   AA.

   ⚠️ **Only `text.secondary` actually fails.** The three `-light` roles are **dark-surface
   tokens**, not defects — on DGA's own `background.black` they measure 10.75:1, 14.79:1 and
   9.09:1. Do not delete them from your theme; they are the only text roles DGA publishes *for*
   dark surfaces. Scope them, don't remove them.

   `node ../dga-design-system/assets/check-contrast.mjs` lists every pairing — but read what it
   does and does not cover before you gate a build on it.

3. **Never letter-space Arabic.** DGA's display scale carries **-2% tracking**. Arabic is a
   connected script — tracking breaks the joins. Scope `letter-spacing` to Latin, or zero it
   under `[dir="rtl"]`.

4. **Six states, always.** DGA specifies Default, Hovered, Pressed, Selected, Focused and
   Disabled for every interactive component. A component with no visible focus state is not
   compliant — focus is an accessibility requirement, not polish. Most libraries give you five
   and let focus fall back to the browser default; check rather than assume.

5. **44 x 44 px minimum touch target**, on every interactive element. Most libraries' small-size
   controls are under it. This is DGA-stated, and stricter than WCAG 2.1 AA (2.5.5 is AAA).

6. **A skip-to-content link on every page**, first in the DOM inside the header.

7. **Logical CSS properties only** — `margin-inline-start`, not `margin-left`; `inset-inline`,
   not `left`. `transform`, `box-shadow` and gradients are *not* logical and need an explicit
   `[dir="rtl"]` override. See `dga-rtl-i18n`.

8. **Cite or omit.** Where DGA is silent — numerals, Hijri, Arabic body typeface, motion
   durations — name the gap and the fallback you are applying, usually WCAG 2.1 AA. **Never
   invent a DGA rule to fill one.** A compliance claim that cannot be cited is worse than none.

## Step 3 — map the components

`references/component-mapping.md` maps all 50 DGA components onto the generic component role,
gives the name in MUI, Chakra v3, shadcn/Radix and Ant Design, and — the part that matters —
states the **DGA-specific constraint your library will not give you for free**. A sample:

- Links are **underlined by default**; "click here" and "go to" are forbidden as link text
- Content Switcher is capped at **2-4 options** — beyond four it must become Tabs
- A horizontal tablist **never scrolls or wraps**; overflow goes to a "More" button
- Pie charts **max 6 segments**; line and bar **max 3 series**
- Breadcrumbs truncate past **5** items, and on mobile show back-arrow plus previous page only
- Pagination appears after **10** items
- Critical notifications **never auto-dismiss**; anything that does waits 5s or longer
- Sliders in RTL increase toward the **start** edge
- Steps in RTL progress right-to-left, and swap to a Radial Stepper on mobile

## Step 4 — build the things no library ships

This is the compliance gap. Four of these are government-mandated rather than stylistic, so no
component library and no automated accessibility tool will tell you they are missing.

| Must build | Why it matters |
|---|---|
| **Digital Stamp** 🚩 | Verifies the site is a registered `.gov.sa` platform. Needs the entity's DGA registration number and License Number — a **procurement dependency, start early**. |
| **Footer with Accessibility Tools** 🚩 | DGA lists font-size and contrast controls as required footer anatomy, and they come **first in tab order**. A feature to build, not styling. Not a WCAG requirement, so nothing automated catches its absence. |
| **Feedback section** 🚩 | "Was this page useful?" plus Yes/No and reason options, on **every page**. Its results feed the mandated performance-statistics page. |
| **Navigation Header / Second Nav Header** | DGA-specific anatomy and layouts. `role="banner"` plus `role="navigation"`. |
| **Table of Contents** | Required on content-heavy pages. Activation must move **focus**, not just scroll. |
| **Two last-modified dates** | Page *and* platform. Both, on every page. |

Plus, if you display dates: **a Hijri wrapper**. Nothing in DGA and nothing in any UI library
provides one — DGA's own datepicker demo is Gregorian and its official package contains no Hijri
code. A tested `Intl`-based implementation ships at
`../dga-react/assets/reference-impl/dga-date.ts`; it has no framework dependency, so it drops
into any project.

Full specs for all of the above: `../dga-design-system/references/patterns.md` and
`components.md`.

## Where to look

| File | Covers |
|---|---|
| `references/token-wiring.md` | Wiring the DGA tokens into Tailwind v3/v4, MUI, Chakra v3, shadcn/Radix, Ant Design, styled-components, or plain CSS |
| `references/component-mapping.md` | All 50 DGA components, your library's name for each, and the DGA constraint to add |
| `../dga-design-system/assets/check-contrast.mjs` | WCAG audit of **DGA's own** role x background table. It never reads your source — see the CI note below |

## What the contrast checker does and does not do

Worth being precise, because it is easy to wire it up and believe you are covered.

**What it does.** Reads `tokens.json` and scores every DGA text role against every DGA light
surface. It is an audit of **what DGA publishes**, and it is the evidence behind rule 2.

**What it does not do.** It never opens your source. Nothing you write can change its exit code.
It also does not score pairings *your theme composes* — a `colorPalette` `fg` on `muted`, a hover
state, text over a brand fill. Those are where AA actually breaks in a real build, and they are
invisible to this script.

**So `--ci` cannot be a green gate.** On stock DGA tokens it exits **1**, permanently, because
`text.secondary` fails. A pipeline that reports it green has the flag missing. Wire it as:

1. **Run it once as a documented artefact** — `--json`, committed. It is your evidence of which
   upstream tokens are unusable, and it re-runs correctly after a harvest.
2. **Gate the build on your own source instead** — a grep for hex literals outside the theme
   layer, and for the role names you have ruled out. ⚠️ A grep for a token you *deleted* can
   never fail; see the silent-failure note in `references/token-wiring.md`.
3. **Add a check over the pairings your theme actually composes**, which this script does not
   generate for you.

## Honest limits

- **No dark theme values.** DGA documents a dark variant for every semantic colour but publishes
  the values only in the PC 1.0 Figma variable collections. Omitted rather than invented — but
  build components theme-aware from day one, with the dark slot ready and empty. Retrofitting
  costs far more.
- **No responsive radius or spacing.** DGA's *semantic* radius and spacing resolve differently on
  Desktop, Tablet and Mobile. The public CSS exposes one value each, so treating them as
  constants is wrong on two of three breakpoints. Figma-only.
- **No component recipes.** Yours to author against the specs. Recipes for six different
  libraries would rot faster than they helped.
- **Two DGA component pages are defective.** Card's accessibility section is Accordion's, pasted
  in; Menu has none at all. Apply WCAG and the WAI-ARIA menu pattern, and say DGA is silent.
