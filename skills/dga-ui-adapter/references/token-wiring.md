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

Use `colorPalette="brand"` rather than per-instance colours, and put the display-scale
`letterSpacing` behind a Latin-only scope.

### 🚩 `createSystem(defaultConfig, ...)` merges — it does not replace

This is the trap in the snippet above, and it has two consequences that both pass a build.
Both are Chakra's documented defaults — see Chakra UI v3 docs, *Theming → Customization*
(`defaultConfig` is merged into `createSystem`) and *Color Mode* (the provider follows system
preference by default). Neither is a quirk of this kit's reading.

**1 · You inherit Chakra's dark theme even with no toggle.** Chakra's `defaultConfig` ships
`_dark` values on its own semantic tokens (`bg`, `fg`, `border`, the gray ramp its recipes use).
Chakra's `ColorModeProvider` wraps `next-themes`, which enables system preference by default — so
a visitor whose OS is in dark mode gets the `.dark` class applied **whether or not you expose a
toggle**. Chakra's built-ins flip dark underneath DGA roles that stay light, and you ship the
half-dark theme you were trying to avoid, triggered by an OS setting nobody chose in your app.

Since DGA publishes no dark values (Figma-only), pin it until they are in hand:

```tsx
<ColorModeProvider forcedTheme="light" />   // or defaultTheme="light" enableSystem={false}
```

and grep for `_dark` in CI so it cannot reappear by accident.

**2 · Omitting a key does not delete it.** Chakra keeps `xl: 1280px` and `2xl: 1536px` from
`defaultConfig`, so `lg` and `xl` both sit at 1280px and `2xl` is a phantom band DGA never
defines. Unknown breakpoint keys are not errors, so a `{ base, xl: ... }` copied from a Chakra
example silently no-ops. The same goes for Chakra's default palette: `color="blue.500"` keeps
compiling. Build the config without `defaultConfig`, or remove the keys explicitly — and assert
the result in a test rather than assuming.

**DGA defines four bands, `xl` included** — mobile 0–599, tablet 600–959, desktop 960–1279,
xl 1280+. Three Chakra thresholds (600/960/1280) cover all four. Delete Chakra's extra keys
because your thresholds already cover DGA's bands, **not** because DGA lacks an `xl`. And note
that DGA "desktop" is Chakra `md` — that off-by-one name will confuse anyone reading a DGA spec
against your code.

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

**Order the stack Latin-first.** Font fallback resolves *per character*, not per string, so both
faces get used regardless of order — but the order decides which one renders **Latin**:

```css
/* right: Latin from the face DGA names, Arabic from the Arabic face */
font-family: "IBM Plex Sans", "IBM Plex Sans Arabic", system-ui, sans-serif;

/* wrong: IBM Plex Sans Arabic contains Latin glyphs, so it wins for Latin
   and DGA's named face never renders anything */
font-family: "IBM Plex Sans Arabic", "IBM Plex Sans", system-ui, sans-serif;
```

Arabic-first *looks* like the Arabic-first principle applied to the font stack. It is not — it
silently replaces the one typeface DGA actually specifies.

⚠️ **`letterSpacings` carry `-0.02em` on `display-2xl` … `display-md`** (design spec says −2%;
CSS `letter-spacing` does not accept percentages). Never let that reach Arabic.

## Contrast — one real failure, three misreadings

**Exactly one DGA text token fails AA outright:**

| Token | on `background.white` | Verdict |
|---|---|---|
| `text.secondary` #dba102 | **2.30:1** | Fails at every size, large included. No light surface is safe. |

The three `-light` roles are **not failures** — they are dark-surface tokens, and the naming
invites the wrong conclusion in both directions:

| Token | on white | on `background.black` #161616 | on `background.neutral-800` |
|---|---|---|---|
| `text.primary-light` #88d8ad | 1.68:1 ✗ | **10.75:1** ✓ | 8.63:1 ✓ |
| `text.secondary-light` #fae996 | 1.22:1 ✗ | **14.79:1** ✓ | 11.88:1 ✓ |
| `text.tertiary-light` #ccadd9 | 1.99:1 ✗ | **9.09:1** ✓ | 7.30:1 ✓ |

`-light` means *"for use on dark"*, not *"the light-theme variant"*. **Do not delete these from
your theme** — they are the only text roles DGA publishes for dark surfaces, and removing them
while keeping a dark slot leaves you with nothing legitimate to put in it. Scope them to dark
surfaces; do not remove them.

`check-contrast.mjs` already encodes this: it marks `-light`, `oncolor-*` and `*disabled*` roles
as expected-on-dark and excludes them from its verdict. Its FAIL list is `text.secondary` alone.

Also worth knowing: `text.primary` (#1b8354) clears AA by **0.05** on `background.body`
(4.55:1). It passes, but any opacity applied to green text there breaks it.

Full table: `../../dga-design-system/references/CONTRAST-AUDIT.md`. Read
`../SKILL.md` -> *What the contrast checker does and does not do* before gating a build on it.

## 🚩 Deleting a token fails silently

A tempting way to stop `text.secondary` being used is to leave it out of the theme. **It does not
work, and it makes the failure quieter.**

In Chakra v3 — and in most token systems that resolve by string — an unrecognised token is passed
through as a raw CSS value:

```tsx
<Text color="text.secondary">   // token deleted from the theme
// emits:  color: text.secondary
// browser: invalid declaration, dropped
// result:  text renders in the inherited colour. No build error. No type error.
```

You have converted a loud wrong colour into a silent one, and a visual review will not catch it.
The same applies to a Tailwind class that no longer maps, and to a CSS variable that is never
declared — `var(--gone)` with no fallback resolves to nothing.

Two consequences:

1. **Repoint, do not delete.** Keep `text.secondary` defined and resolve it to
   `secondary-gold.800` (#945c01, 5.54:1 on white), or to your own accent. A defined token that
   is safe beats an undefined one that fails open.
2. **A grep for a deleted token can never fail.** If your CI greps `src/` for
   `text.secondary` *and* you removed the token, the check passes by construction — it is
   guarding nothing. Grep for what a developer will actually write: the hex literal `#dba102`,
   `background.secondary` (the same gold under another role), and `colorPalette="secondary"`.

## Quirks preserved from source

Faithful to DGA, and deliberately not "fixed":

- **Radius is not monotonic** — `2xl` (16px) and `3xl` (20px) are smaller than `xl` (24px)
- `primary-sa-flag` has no `600` step; `brand.600` (#1b8354) fills that role
- `tertiary-lavendar` has no `500`, and that is DGA's spelling
- `gray` carries an extra `1000` step that no other ramp has
- DGA's own `.5` spacing variables use **U+2024 ONE DOT LEADER**, not a full stop
