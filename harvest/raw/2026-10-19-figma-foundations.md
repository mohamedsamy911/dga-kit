# Raw capture — DGA's Figma "Foundations - Platforms Code" variables, 2026-10-19

**Source.** https://www.figma.com/community/file/1392267405633663431/foundations-platforms-code —
published by **DGA** (`https://www.figma.com/@sdga`, the Figma profile DGA's own `/designing` page
links to). Description: "Platforms Code semantic tokens and visual styles". Licensed **CC BY 4.0**;
support DS-DGA@dga.gov.sa. The page's update notes are dated 16 Jun 2025 and 2 Jul 2025 ("Last
updated 1 year ago"). The design site is Platforms Code 4.0 (October 2026), so the file is older
than the site and may lag it.

**Export.** On 2026-10-19 the owner duplicated the community file into their Figma drafts, and the
variables were read in the browser with Figma's plugin API, read-only calls only
(`figma.variables.getLocalVariableCollectionsAsync`, `getLocalVariablesAsync`). Each alias is kept
and also resolved per mode; colours are written as hex. The export is committed beside this file:
`2026-10-19-figma-foundations-variables.json`, 166,736 bytes, sha256
`579d85266fdd21c75e420fc69253b2bcd5ff56c7bb8f65df3ae34435779ad64e` (compact JSON; the working copy
was later pretty-printed and re-serialises to the same bytes). Attribution: © Digital Government
Authority, CC BY 4.0.

**Contents.** 7 collections, 784 variables: Containers 3 · Primitives 245 · Radius 8
(Desktop/Tablet/Mobile) · Themes 366 (Light/Dark) · Widths 12 · Spacing 104 (Desktop/Tablet/Mobile)
· Typography 46 (Desktop/Tablet/Mobile).

## What it shows, compared with DGA's live CSS (`index-CYyqM6kT.css`)

1. **Radius does not change by screen size.** All 8 radius variables have the same value in all
   three modes: `radius-none` 0, `radius-xs` 2, `radius-sm` 4, `radius-md` 8, `radius-lg` 16,
   `radius-xl` 24, `radius-full` 9999, `card-radius` 16.
   The set is the Platforms Code one; it has no `xxs`, `2xl`, `3xl` or `4xl`.
2. **Spacing and type do.** 39 of 104 spacing variables and 36 of 46 typography variables have
   different values per mode. Desktop typography equals the kit's type scale.
3. **DGA's CSS ships the responsive spacing too.** Three blocks, `@media only screen and
   (min-width: 1025px)`, `(min-width: 768px)` and `(max-width: 767px)`, each set 91 spacing
   variables on `:root`. They match the Figma modes in 206 of 207 comparable values; the exception
   is `button-menu-gap` on mobile (CSS `var(--spacing-2)` = 8px, Figma 4px). Typography is not
   responsive in the CSS.
4. **The CSS order overrides 9 desktop values.** The `min-width: 768px` block comes after the
   `min-width: 1025px` block, so at 1025px and wider the tablet value wins wherever the two differ.
   Read on the rendered Layout and Spacing page at a 1400px viewport: `--card-lg-padding` 24px,
   `--section-padding` 24px, `--section-gap` 24px, `--card-md-gap` 20px,
   `--accordion-md-header-gap` 12px, `--control-title-error-gap` 12px. Figma's Desktop values are
   32, 32, 32, 24, 48 and 16.
5. **Colour primitives: 98 identical, 22 one unit apart, 2 different.** In each of the 22 the CSS
   channel is exactly one lower than Figma's (e.g. `Blue/400` Figma `#53b1fd`, CSS `#53b0fd`;
   10% alpha `1a` vs `19`). That pattern fits a conversion that rounds down; the cause is not
   stated by DGA. `Neutral/500` (`#6c737f`) and `Neutral/950` (`#0d121c`) are among the 22: the CSS
   `--colors-neutral-*` carries `#6c727e` and `#0c111b`. The two real differences are
   `alpha-green-10/20`: Figma `#079455` at 10% and 20%, CSS `#1b8354` at 10% and 20%.
6. **Light theme: 233 identical, 48 one unit apart, 2 different** — `control-disabled` and
   `border-disabled` are `#d2d6db` in Figma and `#9da4ae` in the CSS.
7. **Dark theme: Figma remaps what the CSS does not.** Against the CSS `[data-theme=dark] :root`
   block: 155 identical, 43 one unit apart, 80 different. Examples: `text-primary` Figma `#54c08a`,
   CSS `#1b8354`; `text-error` Figma `#f97066`, CSS `#b42318`; `background-success-50` Figma
   `#06764733`, CSS `#1f2a37`. Figma also defines the five `background-*-light` names the CSS dark
   block omits (in its Icon group), with the same light values and dark tints: brand `#166a451a`,
   success `#0676471a`, info `#175cd31a`, warning `#b547081a`, error `#b423181a`. In the CSS dark
   block, `background-primary-50` is a green alpha (`#1b835419`) and the four status `-50`
   backgrounds are `neutral.800` (`#1f2a37`).
8. **Font family.** `font-family-display` and `font-family-text` are both "IBM Plex Sans Arabic".
   Weights: Regular, Medium, Semibold, Bold, each with an italic.
9. **Three spacing values look out of pattern**, reported as published:
   `control-radio-error-icon-gap` 16 / 16 / **48**; `accordion-md-header-gap` **48** / 12 / 12;
   `progress-indicator-gap` 8 / 8 / **16** (Desktop / Tablet / Mobile).
10. **Smallest mobile text.** `typo-size-text-xs` is 8px and `typo-size-text-2xs` 8px on Mobile;
    `typo-size-text-md` is 12px.

## Tables

Values in px unless the type is a string. Modes in the order Figma lists them.

### Radius

| Variable | Desktop | Tablet | Mobile |
|---|---|---|---|
| `Components/card-radius` | 16 | 16 | 16 |
| `Radius/radius-none` | 0 | 0 | 0 |
| `Radius/radius-xs` | 2 | 2 | 2 |
| `Radius/radius-sm` | 4 | 4 | 4 |
| `Radius/radius-md` | 8 | 8 | 8 |
| `Radius/radius-lg` | 16 | 16 | 16 |
| `Radius/radius-xl` | 24 | 24 | 24 |
| `Radius/radius-full` | 9999 | 9999 | 9999 |

### Containers

| Variable | Value |
|---|---|
| `container-max-width-desktop` | 1280 |
| `container-padding-desktop` | 32 |
| `container-padding-mobile` | 16 |

### Widths

| Variable | Mode 1 |
|---|---|
| `Width/width-xxs` | 320 |
| `Width/width-xs` | 384 |
| `Width/width-sm` | 480 |
| `Width/width-md` | 560 |
| `Width/width-lg` | 640 |
| `Width/width-xl` | 768 |
| `Width/width-2xl` | 1024 |
| `Width/width-3xl` | 1280 |
| `Width/width-4xl` | 1440 |
| `Width/width-5xl` | 1600 |
| `Width/width-6xl` | 1920 |
| `Max Width/paragraph-max-width` | 720 |

### Spacing (all 104)

| Variable | Desktop | Tablet | Mobile |
|---|---|---|---|
| `Global/spacing-none` | 0 | 0 | 0 |
| `Global/spacing-xxs` | 2 | 2 | 2 |
| `Global/spacing-xs` | 4 | 4 | 4 |
| `Global/spacing-sm` | 6 | 6 | 6 |
| `Global/spacing-md` | 8 | 8 | 8 |
| `Global/spacing-lg` | 12 | 12 | 12 |
| `Global/spacing-xl` | 16 | 16 | 16 |
| `Global/spacing-2xl` | 20 | 20 | 20 |
| `Global/spacing-3xl` | 24 | 24 | 24 |
| `Global/spacing-4xl` | 32 | 32 | 32 |
| `Global/spacing-5xl` | 40 | 40 | 40 |
| `Global/spacing-6xl` | 48 | 48 | 48 |
| `Global/spacing-7xl` | 64 | 64 | 64 |
| `Global/spacing-8xl` | 80 | 80 | 80 |
| `Global/spacing-9xl` | 96 | 96 | 96 |
| `Global/spacing-10xl` | 128 | 128 | 128 |
| `Global/spacing-11xl` | 160 | 160 | 160 |
| `Tooltip/tooltip-padding` | 8 | 8 | 8 |
| `Tooltip/tooltip-gap` | 8 | 8 | 8 |
| `Tab/tab-button-gap` | 4 | 4 | 4 |
| `Notification/notification-gap` | 16 | 16 | 8 |
| `Notification/notification-padding` | 16 | 16 | 12 |
| `Notification/notification-h-padding` | 24 | 24 | 16 |
| `Notification/notification-alert-v-padding` | 8 | 8 | 8 |
| `Notification/notification-alert-h-padding` | 24 | 24 | 16 |
| `Notification/notification-toast-v-padding` | 16 | 16 | 12 |
| `Notification/notification-toast-desktop-h-padding` | 24 | 24 | 16 |
| `Notification/notification-toast-mobile-h-padding` | 16 | 16 | 16 |
| `Tab/horizontal-tab-md-button-v-padding` | 12 | 12 | 8 |
| `Tab/horizontal-tab-md-button-h-padding` | 16 | 16 | 12 |
| `Tab/horizontal-tab-sm-button-v-padding` | 8 | 8 | 4 |
| `Tab/horizontal-tab-sm-button-h-padding` | 12 | 12 | 8 |
| `Tab/vertical-tab-md-button-v-padding` | 6 | 6 | 4 |
| `Tab/vertical-tab-md-button-h-padding` | 12 | 12 | 8 |
| `Tab/vertical-tab-sm-button-v-padding` | 2 | 2 | 2 |
| `Tab/vertical-tab-sm-button-h-padding` | 6 | 6 | 4 |
| `Table/table-cell-gap` | 8 | 8 | 4 |
| `Table/table-cell-v-padding` | 8 | 8 | 4 |
| `Table/table-cell-h-padding` | 16 | 16 | 12 |
| `Control/control-vertical-gap` | 4 | 4 | 4 |
| `Control/control-title-error-gap` | 16 | 12 | 8 |
| `Control/control-switch-error-icon-gap` | 8 | 8 | 4 |
| `Control/control-radio-error-icon-gap` | 16 | 16 | 48 |
| `Control/control-switch-description-padding` | 64 | 64 | 64 |
| `Control/control-radio-description-padding` | 48 | 48 | 48 |
| `Form/label-gap` | 4 | 4 | 4 |
| `Form/field-label-gap` | 8 | 8 | 8 |
| `Form/input-padding` | 0 | 0 | 0 |
| `Form/input-gap` | 0 | 0 | 0 |
| `Form/textarea-padding` | 0 | 0 | 0 |
| `Form/textarea-gap` | 0 | 0 | 0 |
| `Form/select-padding` | 0 | 0 | 0 |
| `Form/select-gap` | 0 | 0 | 0 |
| `Form/Iable-container` | 8 | 8 | 8 |
| `Form/Input-container-padding-left` | 8 | 8 | 8 |
| `Form/Input-container-padding-right` | 16 | 16 | 16 |
| `Form/icon-enteredtext` | 8 | 8 | 8 |
| `Form/icon-helpertext` | 8 | 8 | 8 |
| `Form/Prefix-Suffix-padding-left` | 16 | 16 | 16 |
| `Form/Prefix-Suffix-padding-right` | 16 | 16 | 16 |
| `Form/Prefix-Suffix-padding-Top&Bottom` | 2 | 2 | 2 |
| `Form/Prefix-Suffix-lable-icon` | 4 | 4 | 4 |
| `Form/dropdown-container-padding-left&right` | 16 | 16 | 16 |
| `Form/dropdown-icon-content` | 4 | 4 | 4 |
| `Form/textarea-container-padding-left&right` | 16 | 16 | 16 |
| `Form/textarea-container-padding-top&bottom` | 12 | 12 | 12 |
| `Accordion/accordion-lg-header-padding` | 16 | 16 | 16 |
| `Accordion/accordion-lg-header-gap` | 16 | 16 | 16 |
| `Accordion/accordion-md-header-padding` | 12 | 12 | 12 |
| `Accordion/accordion-md-header-gap` | 48 | 12 | 12 |
| `Accordion/accordion-sm-header-padding` | 8 | 8 | 8 |
| `Accordion/accordion-sm-header-gap` | 8 | 8 | 8 |
| `Card/card-lg-padding` | 32 | 24 | 16 |
| `Section/section-padding` | 32 | 24 | 16 |
| `Section/section-gap` | 32 | 24 | 16 |
| `Text/text-content-gap` | 8 | 8 | 4 |
| `Button/buttons-lg-gap` | 4 | 4 | 4 |
| `Icon/icon-text-gap` | 8 | 8 | 4 |
| `Model/modal-padding` | 24 | 24 | 16 |
| `Model/modal-gap` | 8 | 8 | 8 |
| `Button/buttons-lg-padding` | 16 | 16 | 16 |
| `Button/buttons-md-gap` | 4 | 4 | 4 |
| `Button/buttons-md-padding` | 12 | 12 | 12 |
| `Button/buttons-sm-gap` | 4 | 4 | 4 |
| `Button/buttons-sm-padding` | 8 | 8 | 8 |
| `Model/modal-content-bottom-padding` | 16 | 16 | 8 |
| `Button/buttons-group-gap` | 8 | 8 | 4 |
| `Button/button-menu-gap` | 8 | 8 | 4 |
| `Button/button-menu-v-padding` | 8 | 8 | 8 |
| `Button/button-menu-h-padding` | 8 | 8 | 8 |
| `Link/link-md-gap` | 8 | 8 | 4 |
| `Link/link-sm-gap` | 4 | 4 | 4 |
| `Link/links-group-gap` | 12 | 12 | 8 |
| `Progress Indicator/progress-indicator-gap` | 8 | 8 | 16 |
| `Progress Indicator/progress-text-content-side-padding` | 16 | 16 | 12 |
| `Pagination/pagination-Item-sm-padding` | 4 | 4 | 4 |
| `Pagination/pagination-Item-md-padding` | 6 | 6 | 6 |
| `Pagination/pagination-Item-lg-padding` | 8 | 8 | 8 |
| `Pagination/pagination-Items-padding` | 8 | 8 | 4 |
| `Card/card-lg-gap` | 24 | 24 | 16 |
| `Card/card-md-padding` | 32 | 24 | 16 |
| `Card/card-md-gap` | 24 | 20 | 12 |
| `Card/card-sm-padding` | 32 | 24 | 16 |
| `Card/card-sm-gap` | 24 | 20 | 12 |

### Typography (all 46)

| Variable | Desktop | Tablet | Mobile |
|---|---|---|---|
| `Font Family/font-family-display` | IBM Plex Sans Arabic | IBM Plex Sans Arabic | IBM Plex Sans Arabic |
| `Font Wieght/font-weight-bold` | Bold | Bold | Bold |
| `Font Wieght/font-weight-bold-italic` | Bold italic | Bold italic | Bold italic |
| `Font Wieght/font-weight-semibold` | Semibold | Semibold | Semibold |
| `Font Wieght/font-weight-semibold-italic` | Semibold Italic | Semibold Italic | Semibold Italic |
| `Font Wieght/font-weight-medium` | Medium | Medium | Medium |
| `Font Wieght/font-weight-medium-italic` | Medium Italic | Medium Italic | Medium Italic |
| `Font Wieght/font-weight-regular` | Regular | Regular | Regular |
| `Font Wieght/font-weight-italic` | Italic | Italic | Italic |
| `Font Family/font-family-text` | IBM Plex Sans Arabic | IBM Plex Sans Arabic | IBM Plex Sans Arabic |
| `Size/Display/typo-size-display-2xl` | 72 | 56 | 48 |
| `Size/Display/typo-size-display-xl` | 60 | 48 | 40 |
| `Size/Display/typo-size-display-Ig` | 48 | 36 | 32 |
| `Size/Display/typo-size-display-md` | 36 | 30 | 24 |
| `Size/Display/typo-size-display-sm` | 30 | 24 | 20 |
| `Size/Display/typo-size-display-xs` | 24 | 20 | 18 |
| `Size/Text/typo-size-text-xl` | 20 | 18 | 16 |
| `Size/Text/typo-size-text-Ig` | 18 | 16 | 14 |
| `Size/Text/typo-size-text-md` | 16 | 14 | 12 |
| `Size/Text/typo-size-text-sm` | 14 | 12 | 10 |
| `Size/Text/typo-size-text-xs` | 12 | 10 | 8 |
| `Size/Text/typo-size-text-2xs` | 10 | 8 | 8 |
| `Line Height/Display/line-heights-display-2xl` | 90 | 72 | 64 |
| `Line Height/Display/line-heights-display-xl` | 72 | 64 | 56 |
| `Line Height/Display/line-heights-display-Ig` | 60 | 48 | 40 |
| `Line Height/Display/line-heights-display-md` | 44 | 40 | 32 |
| `Line Height/Display/line-heights-display-sm` | 38 | 32 | 28 |
| `Line Height/Display/line-heights-display-xs` | 32 | 28 | 24 |
| `Line Height/Text/line-heights-text-xl` | 30 | 26 | 24 |
| `Line Height/Text/line-heights-text-Ig` | 28 | 24 | 20 |
| `Line Height/Text/line-heights-text-md` | 24 | 20 | 18 |
| `Line Height/Text/line-heights-text-sm` | 20 | 16 | 14 |
| `Line Height/Text/line-heights-text-xs` | 18 | 14 | 12 |
| `Line Height/Text/line-heights-text-2xs` | 14 | 12 | 10 |
| `Paragraph Spacing/Display/paragraph-spacing-display-2xl` | 72 | 46 | 56 |
| `Paragraph Spacing/Display/paragraph-spacing-display-xl` | 60 | 56 | 48 |
| `Paragraph Spacing/Display/paragraph-spacing-display-Ig` | 48 | 40 | 36 |
| `Paragraph Spacing/Display/paragraph-spacing-display-md` | 36 | 32 | 30 |
| `Paragraph Spacing/Display/paragraph-spacing-display-sm` | 30 | 28 | 24 |
| `Paragraph Spacing/Display/paragraph-spacing-display-xs` | 24 | 24 | 20 |
| `Paragraph Spacing/Text/paragraph-spacing-text-xl` | 20 | 18 | 16 |
| `Paragraph Spacing/Text/paragraph-spacing-text-Ig` | 18 | 16 | 14 |
| `Paragraph Spacing/Text/paragraph-spacing-text-md` | 16 | 14 | 12 |
| `Paragraph Spacing/Text/paragraph-spacing-text-sm` | 14 | 12 | 10 |
| `Paragraph Spacing/Text/paragraph-spacing-text-xs` | 12 | 10 | 8 |
| `Paragraph Spacing/Text/paragraph-spacing-text-2xs` | 12 | 10 | 8 |

