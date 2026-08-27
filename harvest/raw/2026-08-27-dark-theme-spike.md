# Dark theme spike — 2026-08-27

**Question.** This kit records DGA's dark theme as *"documented as existing, not exposed in CSS"*
and lists the values as obtainable only from the PC 1.0 Figma variable collections. A grep of the
shipped CSS bundle contradicted that. Does a dark theme exist in the published CSS, and does it
change the shape of the token harvester?

**Answer. Yes, and yes.** DGA ships a complete 402-declaration dark theme in the public CSS —
**and it can never activate**, because of a one-character defect in its selector.

Extracted values: `2026-08-27-dark-theme-roles.json` (all 402, declared and resolved to hex).

---

## Method — no browser needed for the values

```bash
curl -s https://design.dga.gov.sa/            # 4,417-byte SPA shell
# -> href="/assets/index-PDaQ7SHU.css"
curl -s https://design.dga.gov.sa/assets/index-PDaQ7SHU.css   # 3.9 MB
```

The bundle carries the whole token surface. The dark block is a single rule; find it with
`[data-theme=dark] :root{` and read to the closing brace.

> The filename hash is Vite's build hash. It changes on every DGA deploy, which makes it a free
> and exact "DGA redeployed" tripwire — cheaper and more reliable than hashing any rendered page.

---

## Finding 1 — the dark theme exists, in full

**402 declarations** in one rule, covering every semantic family:

| Family | Roles | Family | Roles |
|---|---|---|---|
| link | 48 | notification | 23 |
| button | 45 | text | 20 |
| background | 43 | controls | 17 |
| tag | 33 | stepper | 15 |
| form | 33 | table | 8 |
| alpha | 32 | tooltip | 6 |
| featuredicons | 30 | control | 1 |
| border | 25 | | |
| icon | 23 | | |

**390 of 402 are `var(--colors-*)` references** to primitives already captured in `tokens.json`.
Only **12 are literals**, and 10 of those are alpha-composite values.

That settles the architecture question: **dark is a role→primitive remap layer, not a second
palette.** No new primitive colours exist. `tokens.json` needs a `roles.dark` remap section, not a
parallel colour table.

Every one of the 402 resolves to a concrete hex against the light-theme `:root` primitives —
zero unresolved.

---

## Finding 2 🚩 — the selector is broken, so the theme cannot turn on

DGA ships:

```css
[data-theme=dark] :root { --background-body: var(--colors-neutral-900); /* …402… */ }
```

`:root` is `<html>`. The descendant combinator requires `:root` to have an ancestor carrying
`[data-theme=dark]`. **`<html>` has no ancestor.** The rule matches nothing, in any document, ever.

The correct selector is `:root[data-theme="dark"]` — the same characters without the space.

### Proven in the live page, not reasoned about

`document.querySelectorAll('[data-theme="dark"] :root').length`:

| State | Elements matched | `--background-body` |
|---|---|---|
| default | **0** | `#f9fafb` (light) |
| `data-theme="dark"` on `<html>` | **0** | `#f9fafb` (light) |
| `data-theme="dark"` on `<body>` | **0** | `#f9fafb` (light) |
| same 402 declarations re-injected as `:root[data-theme="dark"]` | — | **`#111927` (dark)** |

The values are correct and complete. Only the selector is wrong.

### No alternative activation path exists

| Searched for | Occurrences in the bundle |
|---|---|
| `prefers-color-scheme` | **0** |
| `:root[data-theme` (the correct form) | **0** |
| `.dark` class | **0** |
| `[data-theme=dark] :root` (the shipped form) | 1 |

> `dark-mode` appears 12 times and is a **red herring** — every hit is a Hugeicons glyph class
> (`.hgi-dark-mode`), the moon icon. Not theming.

The only working `[data-theme="dark"]` selectors in the bundle are **component-scoped tooltip
rules** (`.tooltip[data-theme="dark"] .tooltip-main…`). Those match correctly and do work — the
Tooltip has a real dark variant. That is the only dark styling a DGA platform gets today.

**Report to DS-DGA@dga.gov.sa.** This is a shipped feature that is one space away from working.

---

## Finding 3 🚩 — dark mode would introduce new AA failures

Contrast of the dark theme's own text roles on its own surfaces, computed with this kit's
`check-contrast.mjs`:

| Role | Hex | on `bg.body` #111927 | on `bg.white` #0c111b | on `bg.card` #1f2a37 |
|---|---|---|---|---|
| text.default | #ffffff | 17.61 PASS | 18.89 PASS | 14.54 PASS |
| text.display | #f9fafb | 16.86 PASS | 18.08 PASS | 13.91 PASS |
| text.primary-paragraph | #f3f4f6 | 16.01 PASS | 17.17 PASS | 13.21 PASS |
| text.secondary-paragraph | #e5e7eb | 14.23 PASS | 15.26 PASS | 11.74 PASS |
| **text.primary** | #1b8354 | **3.71 large-only** | **3.98 large-only** | **3.06 large-only** |
| text.secondary | #dba102 | **7.64 PASS** | 8.20 PASS | 6.31 PASS |
| **text.tertiary** | #80519f | 3.02 large-only | 3.23 large-only | **2.49 FAIL** |
| text.success | #069454 | 4.51 PASS | 4.83 PASS | 3.72 large-only |
| text.info | #156fee | 3.81 large-only | 4.08 large-only | 3.14 large-only |
| text.warning | #dc6803 | 5.05 PASS | 5.42 PASS | 4.17 large-only |
| **text.error** | #b42318 | **2.68 FAIL** | **2.87 FAIL** | **2.21 FAIL** |
| text.primary-light | #88d8ad | 10.46 PASS | 11.22 PASS | 8.63 PASS |
| text.secondary-light | #fae996 | 14.39 PASS | 15.44 PASS | 11.88 PASS |
| text.tertiary-light | #ccadd9 | 8.85 PASS | 9.49 PASS | 7.30 PASS |
| text.default-disabled | #9da4ae | 7.01 PASS | 7.52 PASS | 5.78 PASS |

Three consequences:

**The gold problem is a light-theme problem.** `text.secondary` (#dba102) fails at **2.30:1** on
every light surface — this kit's headline finding — and **passes at 7.64:1** on dark. The role is
not broken; it was placed in the wrong theme.

**`text.error` is unreadable in dark.** #b42318 measures **2.68:1** on the dark body and fails on
every dark surface. An error colour nobody can read is the most consequential defect here.

**`text.primary` — the brand green — degrades.** 4.75:1 in light (a marginal pass) becomes
**3.71:1** in dark: large text only. The primary brand text colour stops being usable for body copy.

> Dark mode is not a free win. Enabling it as shipped trades one failing text role for two.
> `text.error` and `text.primary` both need darker-theme substitutes DGA has not published.
> `secondary-gold.800` solves light; nothing published solves dark error text.

---

## Finding 4 ⚠️ — one dark value looks wrong, unverified

`--form-datecell-background-disabled: #ffffff` — a **white** background declared inside the dark
block, where every neighbouring surface resolves to `#0c111b`–`#1f2a37`. Looks like an oversight,
but DGA may intend a white date cell. Recorded as `TODO(verify)`, not asserted as a defect.

The alpha primitives are **deliberately inverted** in the dark block — `--alpha-white-80` goes
from `#ffffffcc` (light) to `#161616cc` (dark), and `--alpha-black-40` from `#16161666` to
`#ffffff66`. That reads as intentional: a "light scrim" and a "dark scrim" swap roles relative to
the surface. It does mean `--text-oncolor-*` resolves to near-black on brand-coloured surfaces in
dark mode, which is worth checking against a real component. Also `TODO(verify)`.

---

## What this changes for the harvester

1. **Token extraction must read the CSS bundle, not just `getComputedStyle(:root)`.** The dark
   block never applies, so computed style can never see it. Parse the rule out of the CSSOM or the
   fetched stylesheet.
2. **`tokens.json` gains a dark role-remap section** — 402 role→primitive mappings, no new
   primitives. `$source` and `$verify` conventions apply as normal.
3. **`generate-tokens.mjs` gains a dark output**, and must emit `:root[data-theme="dark"]` — the
   corrected selector — with a comment recording that DGA's own is unmatchable.
4. **`check-contrast.mjs` gains a dark pass.** Its current 5 FAILs are light-theme only. Dark has a
   different and partly worse set.
5. **The sentinel should watch this rule specifically** as a critical fact: if DGA fixes the space,
   dark mode goes live for every platform on Platforms Code, and the kit's guidance changes the
   same day.
