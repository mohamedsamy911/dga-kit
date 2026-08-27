# Contrast audit — DGA text roles on DGA backgrounds

**Derived from:** `../assets/tokens.json` (values harvested from https://design.dga.gov.sa/guidelines/foundations/color-system, 2026-08-26). Not a harvested page —
every ratio here is computed. Reproduce with `node ../assets/check-contrast.mjs`.

Computed from the verbatim token values extracted from design.dga.gov.sa on 2026-08-26.
Ratios are WCAG 2.x relative luminance, calculated — not estimated.

**DGA's own stated thresholds** (from `/guidelines/foundations/color-system`):

> Small Text: text below 24 px must have a contrast ratio of at least 4.5:1.
> Large Text: text of 24 px and larger should have a ratio of no less than 3:1.
> Graphical Elements and User Interface Components: minimum 3:1.
> — design.dga.gov.sa/guidelines/foundations/color-system · retrieved 2026-08-26

Note DGA sets the large-text boundary at **24px**, which is stricter than WCAG's own
definition (18.66px bold / 24px regular). Use DGA's number.

## `--text-*` on `--background-white` (#ffffff) and `--background-body` (#f9fafb)

| Token | on white | on body | Small text |
|---|---:|---:|---|
| `text-default` #161616 | 18.10 | 17.32 | PASS |
| `text-display` #1f2a37 | 14.54 | 13.91 | PASS |
| `text-primary-paragraph` #384250 | 10.18 | 9.74 | PASS |
| `text-primary-sa-flag` #14573a | 8.56 | 8.19 | PASS |
| `text-error` #b42318 | 6.57 | 6.29 | PASS |
| `text-info` #175cd3 | 5.99 | 5.73 | PASS |
| `text-tertiary` #80519f | 5.84 | 5.59 | PASS |
| `text-success` #067647 | 5.69 | 5.45 | PASS |
| `text-warning` #b54707 | 5.43 | 5.19 | PASS |
| `text-secondary-paragraph` #6c727e | 4.83 | 4.62 | PASS |
| `text-primary` #1b8354 | 4.75 | **4.55** | PASS — thin margin |
| **`text-secondary` #dba102** | **2.30** | **2.21** | **FAIL** |
| `text-primary-light` #88d8ad | 1.68 | 1.61 | FAIL — dark surfaces only |
| `text-secondary-light` #fae996 | 1.22 | 1.17 | FAIL — dark surfaces only |
| `text-tertiary-light` #ccadd9 | 1.99 | 1.91 | FAIL — dark surfaces only |
| `text-default-disabled` #9da4ae | 2.51 | 2.41 | Exempt (disabled) |

## Findings

### 1 · `--text-secondary` (gold, #dba102) fails on every light background — **Blocker**

At 2.30:1 on white it misses the 4.5:1 small-text threshold and also misses the 3:1
large-text threshold. There is no size at which this token is compliant as text on a light
surface.

The name is the hazard. `text-secondary` reads as a general-purpose secondary text colour —
the obvious choice for a subheading or a caption — and the token set gives no signal that it
is restricted. It is safe only on dark surfaces (7.85:1 on `background-black`).

**Rule for `dga-react` and `dga-design-review`:** `text-secondary` is never applied to text on
a light background. Where gold text is genuinely wanted on white, `secondary-gold-800`
(#945c01) is the first step that clears AA, at 5.54:1. Confirm this substitution with DGA
before it goes into a shipped screen.

### 2 · `--text-primary` clears AA by 0.05 on `background-body` — **Major**

4.55:1 against the 4.5:1 requirement. It passes, but any darkening of the background or
lightening of the green breaks it, and a designer applying an opacity to green text on the
body background will fail without realising. Treat green text on `background-body` as
requiring an explicit contrast check rather than assuming the token is safe.

### 3 · The `-light` text variants are dark-surface tokens

`primary-light`, `secondary-light` and `tertiary-light` all fail badly on light backgrounds
and all pass comfortably on dark ones (10.75, 14.79 and 9.09 on `background-black`). Not a
defect — but the naming does not say so, and nothing stops their misuse. Document the pairing.

## Dark theme — 15 failures, and worse ones

`node ../assets/check-contrast.mjs --theme dark` · values captured 2026-08-27

DGA publishes a complete dark theme (402 declarations) in its CSS bundle. **It cannot currently
activate** — the selector `[data-theme=dark] :root` never matches, because `:root` is `<html>`
and has no ancestor. So nothing below ships today. It ships the moment DGA adds one space.

| Role | Dark value | Worst dark surface | Ratio | |
|---|---|---|---|---|
| text.default | #ffffff | background.brand-light **#f3fcf6** | **1.05:1** | 🚩 |
| text.display | #f9fafb | background.brand-light | **1.00:1** | 🚩 |
| text.primary-paragraph | #f3f4f6 | background.brand-light | **1.05:1** | 🚩 |
| text.error | #b42318 | background.card #1f2a37 | **2.21:1** | 🚩 |
| text.error | #b42318 | background.body #111927 | **2.68:1** | 🚩 |
| text.tertiary | #80519f | background.card | **2.49:1** | 🚩 |
| text.primary | #1b8354 | background.card | 3.06:1 | large only |

**The `*-light` surfaces are the worst finding in either theme.** DGA's dark block does not remap
`background.brand-light`, `error-light`, `info-light`, `success-light` or `warning-light`, so they
keep their near-white light values while `text.default` flips to `#ffffff`. White on `#f3fcf6` is
**1.05:1** — effectively invisible. Nine of the fifteen dark failures are on those five surfaces.

**`text.error` is the most consequential single role.** An error message is exactly the text a
user must be able to read, and it fails on every dark surface with no published substitute.
`notification.text-error` uses `red.300` in dark — that is the nearest thing DGA offers.

### The light finding is not absolute

`text.secondary` (#dba102) fails at 2.30:1 on every **light** surface and **passes at 7.64:1** on
the dark body. The role is not inherently broken; it is in the wrong theme. State the 2.30:1
failure as a light-theme finding.

### If you enable dark mode

You are shipping something DGA has not — and something this kit deliberately does not generate.
`tokens.css` emits no dark rule, because correcting DGA's selector would activate these pairings
for anyone already using `data-theme="dark"`. You own:

| What | Substitute | Sourced from |
|---|---|---|
| `text.error` | **red.300 `#fca19b`** | DGA's own dark `notification.text-error` and `controls.control-text-error` |
| `text.primary` in body copy | **sa-flag.300 `#88d8ad`** (10.46:1) | DGA's own dark `text.primary-light` |
| the five `*-light` status surfaces | **nothing published** | every dark variant DGA ships for them — `notification-`, `tag-`, `featuredicons-` — still resolves to the same near-white value |

The first two are citable. **The third is not**, which is why this kit will not generate a dark
stylesheet: making it safe would mean inventing a DGA value.

Record each substitution in `dga-brand-overlay`. Full evidence:
`https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-08-27-dark-theme-spike.md` in the dga-kit repo.

---

## Recommendation

These three findings are exactly what an automated check should catch. Encode this table as a
token-pairing allowlist in `dga-react` so that a disallowed text/background combination fails
at build time rather than at design review.
