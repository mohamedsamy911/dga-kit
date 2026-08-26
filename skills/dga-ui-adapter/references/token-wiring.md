# Wiring DGA tokens into your library

The DGA values are already extracted. Do **not** re-transcribe them — point your theme at the
generated files in `../../dga-design-system/assets/`:

| File | Shape |
|---|---|
| `tokens.json` | `{ color, role, space, radius, width, container, shadow, typography, breakpoint, grid }` |
| `tokens.css` | `--dga-color-*`, `--dga-text-*`, `--dga-background-*`, `--dga-space-*`, `--dga-radius-*` on `:root` |
| `tailwind-preset.js` | A Tailwind v3 preset — `screens` plus `extend.{colors,spacing,borderRadius,...}` |

Regenerate all three after a re-harvest: `node ../../dga-design-system/assets/generate-tokens.mjs`.
Never hand-edit the outputs.

**Getting them into your project.** dga-kit is a Claude Code plugin, not an npm package, so the
files are not in `node_modules`. Copy the one you need into your repo and commit it — it is a
generated artefact with its source and retrieval date in the header, so it reviews cleanly and
diffs cleanly on the next harvest. The snippets below assume `src/styles/dga/`.

## The one structural rule

DGA splits **primitives** (`color.brand.600`) from **semantic roles** (`role.text.default`).
Your components consume the semantic layer only. Wire both — primitives so the semantic layer
has something to resolve to, semantics so a dark theme can repoint later without touching a
single component.

---

## Tailwind v3

```js
// tailwind.config.js
import dga from './src/styles/dga/tailwind-preset.js'
export default { presets: [dga], content: ['./src/**/*.{ts,tsx}'] }
```

Then `bg-brand-600`, `text-text-default`, `p-6`, `rounded-lg`. Use **logical** utilities only:
`ms-`/`me-`/`ps-`/`pe-`/`start-`/`end-`, never `ml-`/`mr-`/`left-`/`right-`.

## Tailwind v4

v4 reads CSS, so skip the preset:

```css
@import "tailwindcss";
@import "./dga/tokens.css";

@theme inline {
  --color-brand-600: var(--dga-color-brand-600);
  --color-text-default: var(--dga-text-default);
  --color-background-card: var(--dga-background-card);
  /* ...repeat for the roles you use; primitives come through tokens.css */
}
```

## shadcn/ui + Radix (CSS variables)

shadcn's theme is a fixed set of role variables. **The wiring differs between Tailwind v4 and
v3 because of how shadcn consumes those variables.** Using the wrong format silently breaks
every mapping — no error, just unstyled defaults.

### shadcn + Tailwind v4

v4 shadcn consumes variables as raw values via `@theme inline`. DGA's hex tokens work directly:

```css
@import "./dga/tokens.css";

:root {
  --background:      var(--dga-background-body);
  --foreground:      var(--dga-text-default);
  --card:            var(--dga-background-card);
  --primary:         var(--dga-background-primary);
  --primary-foreground: var(--dga-text-oncolor-primary);
  --destructive:     var(--dga-background-error);
  --muted-foreground:var(--dga-text-secondary-paragraph);
  --border:          var(--dga-color-neutral-200);
  --ring:            var(--dga-background-primary);
  --radius:          var(--dga-radius-md);
}
```

### shadcn + Tailwind v3 (pre-v4)

⚠️ **Pre-v4 shadcn components consume variables as `hsl(var(--background))`** — they expect
**bare HSL channel triplets** (e.g. `210 20% 98%`), not hex values. Feeding hex produces
`hsl(#f9fafb)` which is invalid CSS, silently dropped by every browser. You must convert
DGA's hex values to HSL channels:

```css
@import "./dga/tokens.css";

:root {
  /* DGA hex → HSL channels for pre-v4 shadcn hsl(var(--x)) consumption */
  --background:        210 20% 98%;     /* --dga-background-body     #f9fafb */
  --foreground:        0 0% 8.6%;       /* --dga-text-default         #161616 */
  --card:              0 0% 100%;       /* --dga-background-card      #ffffff */
  --primary:           153 65.8% 31%;   /* --dga-background-primary   #1b8354 */
  --primary-foreground:0 0% 100%;       /* --dga-text-oncolor-primary #ffffff */
  --destructive:       4 74.3% 48.8%;   /* --dga-background-error     #d92c20 */
  --muted-foreground:  220 7.7% 45.9%;  /* --dga-text-secondary-paragraph #6c727e */
  --border:            220 13% 91%;     /* --dga-color-neutral-200    #e5e7eb */
  --ring:              153 65.8% 31%;   /* --dga-background-primary   #1b8354 */
  --radius:            0.5rem;          /* --dga-radius-md = 8px      */
}
```

If you add more DGA tokens to the shadcn theme, convert each hex to HSL channels with the
same pattern. The source hex is in the comment so the mapping stays auditable.

### Common to both versions

⚠️ Do **not** map `--muted-foreground` to `--dga-text-secondary`. That is the gold token that
fails AA at every size — see rule 2 in `../SKILL.md`. `--dga-text-secondary-paragraph` (#6c727e)
is the one you want.

## MUI

```ts
import { createTheme } from '@mui/material/styles'
import t from './styles/dga/tokens.json'

export const dgaTheme = createTheme({
  direction: 'rtl',                                    // plus stylis-plugin-rtl in the cache
  palette: {
    primary:   { main: t.color.brand['600'], dark: t.color.brand['800'], light: t.color.brand['400'] },
    error:     { main: t.role.background.error },
    warning:   { main: t.role.background.warning },
    info:      { main: t.role.background.info },
    success:   { main: t.role.background.success },
    text:      { primary: t.role.text.default, secondary: t.role.text['secondary-paragraph'] },
    background:{ default: t.role.background.body, paper: t.role.background.card },
  },
  shape: { borderRadius: parseInt(t.radius.md) },
  typography: { fontFamily: '"IBM Plex Sans", system-ui, sans-serif' },
  breakpoints: { values: { xs: 0, sm: 600, md: 960, lg: 1280, xl: 1920 } },
  components: {
    MuiButton:     { styleOverrides: { root: { minHeight: 44, minWidth: 44 } } },
    MuiIconButton: { styleOverrides: { root: { minHeight: 44, minWidth: 44 } } },
    MuiLink:       { defaultProps: { underline: 'always' } },   // DGA requires underlined links
  },
})
```

MUI's `palette.text.secondary` is a *name collision trap*: DGA's `text.secondary` is gold and
non-compliant, MUI's is a muted grey. Map MUI's to DGA's `secondary-paragraph`, as above.

## Chakra v3

```ts
import { createSystem, defaultConfig, defineConfig } from '@chakra-ui/react'
import t from './styles/dga/tokens.json'

// tokens.json carries $comment/$note annotation keys — strip them, then wrap for Chakra v3.
const clean = (o) => Object.entries(o).filter(([k]) => !k.startsWith('$'))
const wrap  = (o) => Object.fromEntries(clean(o).map(([k, v]) => [k, { value: v }]))

export const system = createSystem(defaultConfig, defineConfig({
  theme: {
    breakpoints: { sm: '600px', md: '960px', lg: '1280px' },
    tokens: {
      colors: Object.fromEntries(
        clean(t.color).filter(([k]) => k !== 'base')
          .map(([fam, ramp]) => [fam, wrap(ramp)])),
      radii: wrap(t.radius),
      spacing: wrap({ ...t.space.numeric, ...t.space.named }),
      fonts: {
        heading: { value: '"IBM Plex Sans", system-ui, sans-serif' },
        body:    { value: '"IBM Plex Sans", system-ui, sans-serif' },
        // National/seasonal occasions, MAIN HEADINGS ONLY. Ministry of Culture licence.
        occasion:{ value: '"Saudi Font", "IBM Plex Sans", system-ui, sans-serif' },
      },
    },
    semanticTokens: {
      colors: Object.fromEntries(clean(t.role).map(([g, roles]) => [g, wrap(roles)])),
    },
  },
}))
```

Use `colorPalette="brand"` rather than per-instance colours, and put the `-0.02em`
`letterSpacing` (design spec says −2%; CSS `letter-spacing` does not accept percentages)
on the display scale behind a Latin-only scope.

## Ant Design

```ts
import t from './styles/dga/tokens.json'

<ConfigProvider direction="rtl" theme={{ token: {
  colorPrimary:   t.color.brand['600'],
  colorError:     t.role.background.error,
  colorWarning:   t.role.background.warning,
  colorSuccess:   t.role.background.success,
  colorInfo:      t.role.background.info,
  colorText:      t.role.text.default,
  colorTextSecondary: t.role.text['secondary-paragraph'],
  colorBgBase:    t.role.background.body,
  colorBgContainer: t.role.background.card,
  borderRadius:   parseInt(t.radius.md),
  fontFamily:     '"IBM Plex Sans", system-ui, sans-serif',
  controlHeight:  44,                                   // DGA minimum target
}}} />
```

## styled-components / vanilla-extract / Emotion

`tokens.json` is a plain object — pass it straight in as the theme, and read
`theme.role.text.default` in components. Nothing to convert.

## Plain CSS / Web Components / Vue / Angular

Import `tokens.css` once at the root and reference `var(--dga-text-default)` everywhere. It is
framework-free and works in a shadow root if you attach it to `:host` as well as `:root`.

---

## Typography, whatever the library

**IBM Plex Sans** for everything. **Saudi Font** only on national and seasonal occasion pages,
**main headings only** — DGA states paragraph use is not recommended, and it requires a Ministry
of Culture licence. `tokens.css` ships `--dga-font-sans` only; if you need Saudi Font, declare it
yourself under a name that cannot be reached by accident (`fonts.occasion`,
`--dga-font-occasion`) and never as a body fallback.

⚠️ **DGA names only the Latin IBM Plex Sans and specifies no Arabic body face.** IBM Plex Sans
Arabic is the obvious intent, but DGA does not say so. Confirm with DS-DGA@dga.gov.sa before
locking the stack — a bilingual product with a mismatched Arabic fallback changes texture
mid-sentence.

⚠️ **`letterSpacings` carry `-0.02em` on `display-2xl` … `display-md`** (design spec says −2%;
CSS `letter-spacing` does not accept percentages). Never let that reach Arabic.

## Contrast — enforce, do not review

Four DGA text tokens fail WCAG AA on every light background in DGA's own palette:

| Token | on `background.white` | Verdict |
|---|---|---|
| `text.secondary` #dba102 | **2.30:1** | Fails AA at every size, large included |
| `text.primary-light` #88d8ad | 1.68:1 | Dark surfaces only |
| `text.secondary-light` #fae996 | 1.22:1 | Dark surfaces only |
| `text.tertiary-light` #ccadd9 | 1.99:1 | Dark surfaces only |

Also worth knowing: `text.primary` (#1b8354) clears AA by **0.05** on `background.body`
(4.55:1). It passes, but any opacity applied to green text on the body background breaks it.

Run `node ../../dga-design-system/assets/check-contrast.mjs` in CI rather than trusting a reviewer to spot these.
Full table: `../../dga-design-system/references/CONTRAST-AUDIT.md`.

## Quirks preserved from source

Faithful to DGA, and deliberately not "fixed":

- **Radius is not monotonic** — `2xl` (16px) and `3xl` (20px) are smaller than `xl` (24px)
- `primary-sa-flag` has no `600` step; `brand.600` (#1b8354) fills that role
- `tertiary-lavendar` has no `500`, and that is DGA's spelling
- `gray` carries an extra `1000` step that no other ramp has
- DGA's own `.5` spacing variables use **U+2024 ONE DOT LEADER**, not a full stop
