# npm package evidence — the official DGA packages

**Retrieved:** 2026-08-28
**Method:** `registry.npmjs.org` metadata for each package, plus extraction of the published
tarball `@platformscode/core@0.0.52` and a count over `dist/types/components.d.ts` and
`dist/collection/components/`.

> ⚠️ **This is NOT a DGA source.** DGA's `/developing` page tells you to install these packages;
> it publishes none of the numbers below. Everything here comes from npm and from the package
> contents. `skills/dga-react/references/official-packages.md` must keep the two apart — an
> earlier version did not, and carried these figures under the DGA citation alone.
>
> The freshness sentinel does **not** watch npm. These numbers can go stale without any DGA
> release, so re-run the commands below rather than trusting the date.

## Registry metadata

| Package | latest | published | versions |
|---|---|---|---|
| `platformscode-new-react` | 0.1.45 | 2026-08-23 | 143 |
| `@platformscode/core` | 0.0.52 | 2026-08-23 | 48 |
| `@platformscode/react` | 0.1.17 | 2025-12-17 | 18 |
| `platformscode-react` | 0.1.0 | 2024-08-14 | 19 |

```bash
curl -sL https://registry.npmjs.org/@platformscode%2fcore |
  python -c "import json,sys;d=json.load(sys.stdin);l=d['dist-tags']['latest'];print(l, d['time'][l][:10], len(d['versions']))"
```

## Component count — 123, not 175

`dist/types/components.d.ts` in `@platformscode/core@0.0.52` declares **123** distinct `dga-*`
tags and **123** `HTMLDga*Element` interfaces. The two counts agree, which is why this is treated
as authoritative. `dist/collection/components/` holds 70 source directories — a different thing,
and not a component count.

```bash
grep -oE '"(dga-[a-z0-9-]+)":' package/dist/types/components.d.ts | sort -u | wc -l   # 123
grep -oE 'interface (HTMLDga[A-Za-z0-9]+Element)' package/dist/types/components.d.ts | sort -u | wc -l   # 123
```

**Correction.** The kit previously published **175 components**. That figure appears in no DGA
capture, nowhere else in the kit, and nowhere in the package. Nothing supported it.

## RTL coverage — 19 of 123, not 48

Components carrying `[dir=rtl]` styling under `dist/collection/components`:

```
dga-accordion · dga-breadcrumbs · dga-datepicker · dga-dropdown · dga-header · dga-icon
dga-inline-alert · dga-link · dga-menu · dga-notification · dga-notification-toast
dga-pagination · dga-progress-indicator · dga-progress-indicator-v3 · dga-quote
dga-structured-list · dga-switch · dga-tabs · dga-textarea
```

```bash
grep -rlE '\[dir\s*=\s*.?rtl' package/dist/collection/components | sed 's|.*/components/||; s|/.*||' | sort -u | wc -l   # 19
```

**Correction, and how the error happened.** The kit previously published **48 components carry
`[dir=rtl]`**. 48 is the number of *published versions* of `@platformscode/core` — the two were
conflated. The distinction matters to anyone planning work: **19 of 123** components shipping
explicit RTL styling means RTL is partially handled and must be tested per component, not assumed.

A whole-`dist` grep returns 148 files, which counts the same components several times across
build outputs. It is not a component count either, and is recorded here only so the next person
does not reach for it.
