# Responsive tokens — what changes by screen size

Source: DGA's Figma file **Foundations - Platforms Code**
(`https://www.figma.com/community/file/1392267405633663431/foundations-platforms-code`, published
by DGA, CC BY 4.0, last updated 2 Jul 2025), its variables read 2026-10-19, and DGA's live
stylesheet read the same day. Evidence:
`https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-figma-foundations.md`.

## The short version

- **Radius is the same at every size.** All eight radius variables are identical on Desktop, Tablet
  and Mobile in DGA's Figma. Use the values in `tokens.json` as constants.
- **Spacing and type change.** 39 component spacing values and 36 typography values have separate
  Desktop, Tablet and Mobile values, listed below. Desktop typography is the scale in
  `foundations.md`.
- **DGA's CSS already ships the spacing ones**, as custom properties inside three media queries.
  It does not ship responsive typography.

## Which widths DGA uses for the three modes

DGA's stylesheet sets the responsive spacing in three blocks:

```css
@media only screen and (min-width: 1025px) { :root { /* Desktop */ } }
@media only screen and (min-width: 768px)  { :root { /* Tablet  */ } }
@media only screen and (max-width: 767px)  { :root { /* Mobile  */ } }
```

These cut-offs (767/768/1025px) are not the layout breakpoints in `foundations.md`
(600/960/1280px). DGA publishes both; this kit does not reconcile them. Use the media-query
widths for these tokens, because that is where DGA's own CSS switches them.

> ⚠️ **Do not copy DGA's block order.** `min-width: 768px` also matches every desktop screen, and
> DGA's file puts it *after* the desktop block, so on a 1025px+ screen the tablet value wins
> wherever the two differ. Measured on DGA's own site at 1400px: `--card-lg-padding` 24px and
> `--section-padding` 24px, where the Desktop value is 32px. Nine values are affected. Bound the
> tablet query instead — `(min-width: 768px) and (max-width: 1024px)` — or order the blocks
> mobile → tablet → desktop.

One CSS value differs from Figma: `button-menu-gap` on Mobile is 8px in the CSS and 4px in Figma.

## Things to know before using the tables

- **Three values look out of pattern** and are reported as DGA published them:
  `control-radio-error-icon-gap` jumps to 48px on Mobile; `accordion-md-header-gap` is 48px on
  Desktop and 12px elsewhere; `progress-indicator-gap` doubles on Mobile. Check the component's
  Figma frame before relying on them.
- **8px text on Mobile.** `typo-size-text-xs` and `typo-size-text-2xs` are 8px on Mobile, and
  `typo-size-text-md` is 12px. WCAG sets no minimum font size, so this is not a WCAG failure.
  Kit policy: do not set content a user must read below 12px, and test Arabic at the Mobile sizes,
  where dots and marks are hardest to read.
- **The Figma file is older than the site** (July 2025 against Platforms Code 4.0). Where the live
  CSS and Figma differ, both are recorded; neither silently replaces the other.

### Spacing — values that change

| Figma variable | Desktop | Tablet | Mobile |
|---|---|---|---|
| `notification-gap` | 16 | 16 | 8 |
| `notification-padding` | 16 | 16 | 12 |
| `notification-h-padding` | 24 | 24 | 16 |
| `notification-alert-h-padding` | 24 | 24 | 16 |
| `notification-toast-v-padding` | 16 | 16 | 12 |
| `notification-toast-desktop-h-padding` | 24 | 24 | 16 |
| `horizontal-tab-md-button-v-padding` | 12 | 12 | 8 |
| `horizontal-tab-md-button-h-padding` | 16 | 16 | 12 |
| `horizontal-tab-sm-button-v-padding` | 8 | 8 | 4 |
| `horizontal-tab-sm-button-h-padding` | 12 | 12 | 8 |
| `vertical-tab-md-button-v-padding` | 6 | 6 | 4 |
| `vertical-tab-md-button-h-padding` | 12 | 12 | 8 |
| `vertical-tab-sm-button-h-padding` | 6 | 6 | 4 |
| `table-cell-gap` | 8 | 8 | 4 |
| `table-cell-v-padding` | 8 | 8 | 4 |
| `table-cell-h-padding` | 16 | 16 | 12 |
| `control-title-error-gap` | 16 | 12 | 8 |
| `control-switch-error-icon-gap` | 8 | 8 | 4 |
| `control-radio-error-icon-gap` | 16 | 16 | 48 |
| `accordion-md-header-gap` | 48 | 12 | 12 |
| `card-lg-padding` | 32 | 24 | 16 |
| `section-padding` | 32 | 24 | 16 |
| `section-gap` | 32 | 24 | 16 |
| `text-content-gap` | 8 | 8 | 4 |
| `icon-text-gap` | 8 | 8 | 4 |
| `modal-padding` | 24 | 24 | 16 |
| `modal-content-bottom-padding` | 16 | 16 | 8 |
| `buttons-group-gap` | 8 | 8 | 4 |
| `button-menu-gap` | 8 | 8 | 4 |
| `link-md-gap` | 8 | 8 | 4 |
| `links-group-gap` | 12 | 12 | 8 |
| `progress-indicator-gap` | 8 | 8 | 16 |
| `progress-text-content-side-padding` | 16 | 16 | 12 |
| `pagination-Items-padding` | 8 | 8 | 4 |
| `card-lg-gap` | 24 | 24 | 16 |
| `card-md-padding` | 32 | 24 | 16 |
| `card-md-gap` | 24 | 20 | 12 |
| `card-sm-padding` | 32 | 24 | 16 |
| `card-sm-gap` | 24 | 20 | 12 |

### Typography — values that change

| Figma variable | Desktop | Tablet | Mobile |
|---|---|---|---|
| `typo-size-display-2xl` | 72 | 56 | 48 |
| `typo-size-display-xl` | 60 | 48 | 40 |
| `typo-size-display-Ig` | 48 | 36 | 32 |
| `typo-size-display-md` | 36 | 30 | 24 |
| `typo-size-display-sm` | 30 | 24 | 20 |
| `typo-size-display-xs` | 24 | 20 | 18 |
| `typo-size-text-xl` | 20 | 18 | 16 |
| `typo-size-text-Ig` | 18 | 16 | 14 |
| `typo-size-text-md` | 16 | 14 | 12 |
| `typo-size-text-sm` | 14 | 12 | 10 |
| `typo-size-text-xs` | 12 | 10 | 8 |
| `typo-size-text-2xs` | 10 | 8 | 8 |
| `line-heights-display-2xl` | 90 | 72 | 64 |
| `line-heights-display-xl` | 72 | 64 | 56 |
| `line-heights-display-Ig` | 60 | 48 | 40 |
| `line-heights-display-md` | 44 | 40 | 32 |
| `line-heights-display-sm` | 38 | 32 | 28 |
| `line-heights-display-xs` | 32 | 28 | 24 |
| `line-heights-text-xl` | 30 | 26 | 24 |
| `line-heights-text-Ig` | 28 | 24 | 20 |
| `line-heights-text-md` | 24 | 20 | 18 |
| `line-heights-text-sm` | 20 | 16 | 14 |
| `line-heights-text-xs` | 18 | 14 | 12 |
| `line-heights-text-2xs` | 14 | 12 | 10 |
| `paragraph-spacing-display-2xl` | 72 | 46 | 56 |
| `paragraph-spacing-display-xl` | 60 | 56 | 48 |
| `paragraph-spacing-display-Ig` | 48 | 40 | 36 |
| `paragraph-spacing-display-md` | 36 | 32 | 30 |
| `paragraph-spacing-display-sm` | 30 | 28 | 24 |
| `paragraph-spacing-display-xs` | 24 | 24 | 20 |
| `paragraph-spacing-text-xl` | 20 | 18 | 16 |
| `paragraph-spacing-text-Ig` | 18 | 16 | 14 |
| `paragraph-spacing-text-md` | 16 | 14 | 12 |
| `paragraph-spacing-text-sm` | 14 | 12 | 10 |
| `paragraph-spacing-text-xs` | 12 | 10 | 8 |
| `paragraph-spacing-text-2xs` | 12 | 10 | 8 |

