---
name: dga-tokens-sync
description: Re-harvest Saudi DGA Platforms Code design tokens from design.dga.gov.sa and diff them against this repo. Use when DGA publishes an update, on the quarterly re-check, or when a token value is disputed.
---

# DGA token sync

Turns a DGA update into a reviewable diff instead of an archaeology project.

## How the tokens were obtained

Not transcribed from swatches — **extracted from the live site's own CSS custom properties**.
design.dga.gov.sa exposes **1,052 variables on `:root`**, which is the authoritative machine-
readable source. Re-run the same extraction:

```js
const rs = getComputedStyle(document.documentElement);
const v = {};
for (const sheet of document.styleSheets) {
  let rules; try { rules = sheet.cssRules } catch(e) { continue }
  for (const r of rules||[]) if (r.style)
    for (const p of r.style) if (p.startsWith('--')) v[p] = rs.getPropertyValue(p).trim();
}
```

Run it on `/guidelines/foundations/color-system` — that page loads the full token set. Group
prefixes: `colors` (479) · `link` · `background` · `button` · `tag` · `form` · `featuredicons` ·
`alpha` · `spacing` · `border` · `icon` · `notification` · `controls` · `stepper` · `table` ·
`radius` · `gradient` · `shadow` · `width` · `tooltip`.

## Procedure

1. Extract as above; write to a scratch file
2. **Diff against `../dga-design-system/assets/tokens.json`**
3. For every change: is it a correction, a rebrand, or a new token? Note which
4. Regenerate `tokens.css` and the Tailwind preset:
   `node ../dga-design-system/assets/generate-tokens.mjs`
5. **Re-run the contrast check** — `node ../dga-design-system/assets/check-contrast.mjs`. A
   changed colour can silently break a pairing that previously passed. Update
   `CONTRAST-AUDIT.md` from its output, and re-run `https://github.com/mohamedsamy911/dga-kit/blob/master/evals/validate-fixtures.py` — an eval
   asserting an old value teaches the skill a false rule.
6. **Update the provenance.** Every section of `tokens.json` carries a `$source` with the page
   it is documented on and the date it was read. Re-stamp `retrieved` on whatever you actually
   re-read — do **not** bulk-update the date across sections you did not visit.
7. **Record what you could not settle as `$verify`, in the data.** A value that looks wrong, is
   disputed by another extraction, or that DGA publishes inconsistently gets an entry next to the
   section it belongs to — not a note in prose that a consumer of `tokens.json` will never see:

   ```json
   { "key": "info.50", "value": "#eff8ff",
     "issue": "what looks wrong, and what the other reading was",
     "status": "disputed",
     "action": "what a consumer should do until it is settled" }
   ```

   `status` must come from the vocabulary in `$meta.$conventions`, and `https://github.com/mohamedsamy911/dga-kit/blob/master/evals/validate-fixtures.py`
   fails the build if it does not. **Anything marked `disputed` must also be written up in
   `harvest/`** — that is checked too.

   This convention is borrowed from `Sara-Saraireh/dga-platforms-code-claude-skill`, and it is
   the reason a suspected typo in DGA's `info.50` was caught rather than propagated.
8. Update `dga-version.md` with the new harvest date and the site's stated version
9. Open a PR with the diff, the contrast delta, and the affected components

## What is NOT in the CSS variables

Do not assume the extraction is complete coverage:

- **Responsive radius and spacing.** DGA's semantic tokens resolve differently on desktop,
  tablet and mobile. Those values live only in the **PC 1.0 Foundations Figma** variable
  collections. `TODO(harvest)`
- ~~**Dark theme values.**~~ **Found 2026-08-27.** All **402** are in the public CSS bundle in a
  single `[data-theme=dark] :root` rule — 390 are `var(--colors-*)` remaps of primitives already
  captured, 12 are literals. Extracted to `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-08-27-dark-theme-roles.json`; the
  spike write-up is `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-08-27-dark-theme-spike.md`.

  > 🚩 **DGA's selector cannot match.** `[data-theme=dark] :root` requires `:root` (`<html>`) to
  > have an ancestor, which it never has. Verified in the live page: 0 elements matched with the
  > attribute on `<html>` or on `<body>`. The correct form is `:root[data-theme="dark"]`. DGA
  > ships a complete dark theme that cannot turn on — report to DS-DGA@dga.gov.sa.

  > ⚠️ Dark is **not** a free win. `text.error` (#b42318) measures **2.68:1** on the dark body and
  > fails AA on every dark surface; `text.primary` drops to **3.71:1**, large-text only. Meanwhile
  > `text.secondary` — this kit's headline light-theme failure — **passes at 7.64:1** in dark.
  > Run `node ../dga-design-system/assets/check-contrast.mjs --theme dark` for the full list —
  > 15 failures, against 5 in light.

  **Wired in 2026-08-27, for audit only.** `tokens.json` carries `role.dark` (20 text + 47
  background roles) and `check-contrast.mjs --theme dark` audits it.

  > 🚩 **`tokens.css` deliberately ships no dark rule, and the Tailwind preset sets no
  > `darkMode` strategy.** Upstream the theme is inert because the selector cannot match, and
  > inert is safe. Emitting a corrected selector would activate 1.05:1 pairings for any consumer
  > already using `data-theme="dark"`. The reasoning is in `generate-tokens.mjs`; the guard is
  > `generated CSS ships no live dark rule` in the eval suite. **Do not "helpfully" turn it on
  > during a re-harvest.**

  The other 340 dark declarations — link, button, tag, form, border, icon, notification,
  controls, stepper, table, tooltip, featuredicons — are uncaptured, as are their light
  counterparts. Same scope decision, recorded in `role.dark.$comment`.

  **On a re-harvest, diff the dark rule too.** If DGA ever corrects the selector, dark goes live
  across every Platforms Code platform on the same day and this kit's guidance changes with it.

## After any re-capture: prove the quotes still hold

A re-harvest rewrites the
[captures in the repo](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw). Any
blockquote in a skill that closely reproduces one of those captured passages is measured against
it, so a page whose wording changed surfaces as **drift** rather than sitting unnoticed in a
reference file.

> That is narrower than "every DGA quote is checked". A quote whose source page was never
> captured has nothing to measure against, and the tool cannot tell it apart from the kit's own
> commentary. Those land in **UNVERIFIABLE**.

Run from a clone of the dga-kit repo — this tool is not installed with the skill:

```bash
python3 evals/check-quote-fidelity.py --ci
```

Three things fail the run:

- **DRIFT** — a reference paragraph reproduces a capture but no longer matches it. Either DGA
  changed the wording (update the reference, and record it in `dga-version.md`) or the reference
  drifted on its own (fix the reference). Never edit the capture to make the check pass.
- **STITCHED** — one blockquote joining passages DGA publishes in different places. Every
  fragment is captured, but no single passage holds them all, so the quote invents the join.
  Split it, and cite each passage where it belongs.
- **MALFORMED FENCES** — a `<!-- dga -->` in a capture without its matching `<!-- /dga -->`.
  The passage inside is lost from the corpus, so fix the fence before trusting any result.

And two that do not:

- **UNVERIFIABLE** — no capture covers that quote's source page. This is the gap list, not a
  defect.
- **Outside the fences** — blockquotes in a capture that are this repo's commentary rather than
  DGA's words. The intended state; only worth a look if one of them is actually DGA's wording.

> ⚠️ The percentage it prints is **blockquote coverage**, not evidence coverage. Its denominator
> is every blockquote in `skills/`, and most of those are the kit's own commentary — so the share
> of genuine *DGA quotes* that are evidenced is higher than the number shown, by an amount nothing
> currently measures. Do not quote it as "the kit is N% evidenced". A true evidence-coverage
> figure needs DGA quotes marked in `skills/` with the same `<!-- dga -->` fence the captures
> use — `TODO`.

> 🚩 The check found two real defects on its first run, both in captures written the same day:
> one truncated a DGA sentence a reference then quoted in full, the other kept one sentence of a
> three-sentence FAQ answer. Both meant a skill was citing DGA text this repo could not evidence.
> Expect it to find more as coverage rises.

## Is a re-harvest even needed? Ask the sentinel first

```bash
python3 harvest/sources.py --check
```

Run from a clone. It diffs the live site against the recorded baseline and writes
[the freshness report](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/FRESHNESS.md). **Exit 0 means nothing shipped** — the Vite build hashes on DGA's CSS and
JS assets are unchanged, so there is no deploy and a re-harvest would produce an identical result.
That check costs about a second and no bandwidth; the 19 MB bundles are only pulled when something
actually changed.

Exit 1 means review pending. What it can tell you without a browser:

- **DGA deployed** — build hash moved
- **A new release** — a new `version-history-*` route appeared. This is the definitive signal
- **Routes added, removed or renamed**, and any count breaking the 50/19/5/6 contract
- **`text.secondary` recoloured** — resolved through its `var()` reference
- 🚩 **The dark selector fixed** — if `[data-theme=dark] :root` becomes `:root[data-theme=dark]`,
  DGA's dark theme activates on every Platforms Code platform at once. `tokens.json role.dark`
  stops being audit-only and `check-contrast.mjs --theme dark` becomes a live finding, not a
  hypothetical one. Treat it as the highest-priority change on this list

> The sentinel **never** updates the baseline. A finding stays reported until you accept it,
> after the guidance has been updated — that ordering is the review gate: nothing rewrites a rule
> because a page moved.

```bash
python3 harvest/sources.py --baseline
```

> It cannot see page **prose** — every route returns the same SPA shell, so a wording change with
> no rebuild is invisible. That is what the quarterly browser harvest below is for.

## Cadence

Quarterly, plus whenever `/updates/change-log` shows a release.

**Current published version: 1.0.3, released 4 Nov 2025.** Releases so far — 1.0.0 (20 Feb 2025) ·
1.0.1 (5 May 2025) · 1.0.2 (1 Sep 2025) · 1.0.3 (4 Nov 2025). Roughly one release every three to
four months, which is what the quarterly cadence above is sized for.

> Do not read the version off the nav badge or the footer — both still say `Version 1.0`. Do not
> read it off the Figma file names either; `PC 1.0 Foundations` is a **file name**. The change log
> is the only authority. Each release has its own route,
> `/updates/change-log/version-history-1-0-3`, so diffing is cheap.

## Known quirks to preserve

- DGA's `.5` spacing variables use **U+2024 ONE DOT LEADER**, not a full stop (`--spacing-0․5`).
  Generated CSS must match or the lookup fails.
- Radius is **not monotonic**: `2xl` (16px) and `3xl` (20px) are smaller than `xl` (24px).
  Don't "fix" it — mirror the source and flag it.
- `primary-sa-flag` has no `600` step; `tertiary-lavendar` has no `500`; `gray` has an extra
  `1000`. All faithful to source.
