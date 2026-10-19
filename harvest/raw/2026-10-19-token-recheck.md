# Raw capture — re-checking the open token values, 2026-10-19

Settles the `TODO(verify)` entries left in `tokens.json`: `neutral.500`, `neutral.950` (disputed
with an independent extraction), `info.50`, the radius documenting page, and the radius scale's
order.

**Method.** The live stylesheet `https://design.dga.gov.sa/assets/index-CYyqM6kT.css` (the deploy
recorded in `source-inventory.json`; sha256 prefix `8e6eceb43957f5b5`) was searched for every
declaration of each name. The same names were then read with `getComputedStyle` on the rendered
Color System page, which is what a browser actually applies.

## Neutral 500 and 950 — two different DGA names

DGA's stylesheet declares both values, under different names:

| Name | Value | Rendered value |
|---|---|---|
| `--colors-neutral-500` | `#6c727e` | `#6c727e` |
| `--colors-gray-neutral-500` | `#6c737f` | `#6c737f` |
| `--colors-neutral-950` | `#0c111b` | `#0c111b` |
| `--colors-gray-neutral-950` | `#0d121c` | `#0d121c` |

`--text-secondary-paragraph` is declared as `var(--colors-neutral-500)` and renders `#6c727e`.

The kit carries `neutral.*`. `gray-neutral` is one of the generic grey ramps the kit excludes by
name (`harvest/reconcile-tokens.py`). The independent extraction's values (`#6c737f`, `#0d121c`,
labelled `gray.500` / `gray.950` there) match `gray-neutral` exactly, so that is the likely source
of the difference. Both hex values exist in the live stylesheet, under different names.

> **Corrected the same day.** DGA's Figma Foundations file, read later on 2026-10-19, gives
> `Neutral/500` as `#6c737f` and `Neutral/950` as `#0d121c` — an exact match for the independent
> read under the *same* name. So the difference is between DGA's CSS and DGA's Figma, one unit
> apart, not two names. See `2026-10-19-figma-foundations.md`.

The Color System page shows its swatches as images and prints no hex codes, so the page itself
cannot say which name a swatch uses.

## Info 50

`--colors-info-50` is `#eff8ff` (blue) in the stylesheet and on the rendered page;
`--colors-success-50` is `#ecfdf3`. The June read of `#ecfdf3` for `info.50` is not present in the
current build. When it changed cannot be established from the live site.

## Radius — three `:root` blocks

The stylesheet declares radius in three `:root` blocks. In source order:

1. and 2. (identical): `none 0`, `xxs 2px`, `xs 4px`, `sm 6px`, `md 8px`, `lg 10px`, `xl 12px`,
   `2xl 16px`, `3xl 20px`, `4xl 24px`, `full 9999px`.
3. A primitive set and its aliases: `--radius-0`…`--radius-9999`, then `none`, `xs` (2px), `sm`
   (4px), `md` (8px), `lg` (16px), `xl` (24px), `full`.

The later block wins where names overlap. Rendered on the page: `none 0`, `xxs 2px`, `xs 2px`,
`sm 4px`, `md 8px`, `lg 16px`, `xl 24px`, `2xl 16px`, `3xl 20px`, `4xl 24px`, `full 9999px` —
exactly the values in `tokens.json`. `xxs`, `2xl`, `3xl` and `4xl` exist only in the first set, so
the merged scale is not in size order (`2xl` 16px is smaller than `xl` 24px). Within each set on
its own, the order is consistent.

Documenting page: no DGA page lists radius values. `/thoughts/designToken` (displayed) describes a
"Radius collection" that *"includes all the radius values for each component"*, with Desktop,
Tablet and Mobile sub-collections, and gives no values.
