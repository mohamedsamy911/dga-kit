# Contrast audit — DGA text roles on DGA backgrounds

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

## Recommendation

These three findings are exactly what an automated check should catch. Encode this table as a
token-pairing allowlist in `dga-react` so that a disallowed text/background combination fails
at build time rather than at design review.
