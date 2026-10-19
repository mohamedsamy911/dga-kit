---
name: dga-react
description: Build or fix React/Next.js UI on DGA's official Platforms Code library (platformscode-new-react) for a Saudi government project. Use ONLY when the project installs DGA's own React package — for a project on any other UI library (Tailwind, MUI, Chakra, shadcn, Ant, plain CSS), use dga-ui-adapter instead.
---

# DGA in React

> ## ⚠️ Which React skill?
>
> This skill assumes the project uses **DGA's own React library**, `platformscode-new-react`.
>
> **If the project uses any other UI library — Tailwind, MUI, Chakra, shadcn/Radix, Ant Design,
> Bootstrap, a Vue or Angular kit, or plain CSS — stop and use `dga-ui-adapter`.** None of DGA's
> own components are available there, so the guidance below does not apply. `dga-ui-adapter` maps
> the same DGA rules onto whatever library you do have.

## Start here: you are not writing a component library

DGA ships an official one. Read `references/official-packages.md` before writing any component.

```
npm install platformscode-new-react@latest
```

**123** Stencil-based components including the UI shell (`dga-header`, `dga-nav-header`,
`dga-footer`, `dga-drawer`, `dga-table-of-content`), the full form set, `dga-data-table`,
`dga-file-upload`, `dga-digital-signature`. **Icons are bundled** — DGA states no separate
install is needed.

⚠️ **RTL is handled only partially.** **19 of the 123** components carry `[dir=rtl]` styling —
not the whole set. Test RTL per component rather than assuming the library covers it; the list is
in `references/official-packages.md`. These counts come from the published package, **not** from
any DGA page — method and evidence in
[the npm package capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-08-28-npm-packages.md).

**This skill's job is the gap layer**: what the official package doesn't give you, plus
enforcing DGA's rules in the code you write around it.

## The gaps you must fill

| Gap | What to do |
|---|---|
| **Hijri calendar** — absent from the package entirely | Wrap or replace `dga-datepicker`. `../dga-rtl-i18n/references/formats.md` has the `Intl` recipe. Decide early — it touches every date field. |
| **i18n** — one component references `locale` | `../dga-rtl-i18n/references/i18n-setup.md` |
| **Responsive tokens** | DGA's radius and spacing semantic tokens resolve differently per breakpoint. Values live in the PC 1.0 Figma collections, not in CSS. `TODO(harvest)` |
| **Arabic typeface** | IBM Plex Sans Arabic — named by DGA's Assessment Checklist (item 3), not by the typography page. `--dga-font-sans` carries both faces, Latin first. |

## Non-negotiables

**Never hardcode a colour.** Every value comes from `../dga-design-system/assets/tokens.json`.
A literal hex in a component is a review failure — kit policy. DGA's own Charts sample passes
literal hexes, so do not copy that part.

**DGA's own code samples** — what each component page's Code tab shows, element names and imports:
`references/official-code-samples.md`. They are illustrative, not an API contract.

**The package does not guarantee DGA's accessibility guidance.** On 2026-10-19, 19 of DGA's own live component demos
rendered without semantics DGA's guidance asks for. For example, `dga-tabs` has no
`tablist`/`tab` roles and `dga-switch` renders a plain checkbox. Inspect the rendered component
and add what is missing: `references/live-demo-semantics.md`.

**Reference semantic tokens, not primitives.** DGA separates them deliberately: primitives
(`brand-600`) are raw; semantic (`text-primary`, `background-card`) carry intent and resolve
per theme. Components use semantic tokens only.

**Build theme-aware from day one.** DGA defines light *and* dark values for every semantic
colour — e.g. `control-primary-hovered` is `Primary-SA-Flag/800` light, `/300` dark.
Retrofitting a dark theme costs far more than building for it.

**`--text-secondary` is not a general text colour.** #dba102 measures 2.30:1 on white and fails
AA at every size. Encode the pairing table from `CONTRAST-AUDIT.md` as an allowlist so a
disallowed text/background pair fails at build time, not at design review.

**Logical CSS properties only.** `margin-inline-start`, never `margin-left`. See
`../dga-rtl-i18n`. `transform`, `box-shadow` and gradients are not logical and need `:dir(rtl)`.

**Never letter-space Arabic.** DGA's Display 2xl–md carry −2% tracking. Scope it to Latin.

**Ship the states the component's page lists.** DGA's vocabulary is Default, Hovered, Pressed,
Selected, Focused, Disabled, but each component specifies its own subset (inputs and tabs list
five, no Selected) — check its spec in `../dga-design-system/references/components.md`. Focused
is an accessibility requirement, not a nicety.

**Semantic HTML, per DGA.** `<button>` for actions — never `<div>`. `<fieldset>`/`<legend>` for
radio groups. `<ol>` for steps. `<nav aria-label="Breadcrumb">`. Per-component requirements in
`../dga-design-system/references/accessibility.md`.

**Skip-to-content link** at the start of every page's header — a DGA requirement.

## Version discipline

`@platformscode/core` is at `0.0.53` and the React wrappers at `0.1.45` (npm, 2026-10-19).
Pre-1.0 gives no breaking-change guarantee. **Pin exact versions** and read the changelog before
every bump.

## Definition of done

A screen built with this skill passes `dga-design-review` with zero blockers, renders correctly
in `ar` and `en`, and contains no hardcoded colour values.
