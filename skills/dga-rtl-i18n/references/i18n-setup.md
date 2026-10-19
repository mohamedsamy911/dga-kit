# Next.js i18n setup

Stack assumption: Next.js App Router with `next-intl`. If the project has already chosen a
different i18n library, follow the project — this file is the default, not a mandate.

## Locale routing

`app/[locale]/layout.tsx` — the `dir` attribute must be set on `<html>`, server-side. Setting
it client-side causes a visible flip on first paint.

```tsx
export function generateStaticParams() {
  return [{ locale: 'ar' }, { locale: 'en' }]
}

export default async function RootLayout({ children, params }) {
  const { locale } = await params
  const dir = locale === 'ar' ? 'rtl' : 'ltr'
  return (
    <html lang={locale} dir={dir}>
      <body>{children}</body>
    </html>
  )
}
```

- `ar` is the default locale. An unprefixed URL resolves to Arabic.
- Every route must exist in both locales. By kit policy — applying DGA checklist item 39, which asks
  that switching languages update the entire content without loss — a 404 in one language and a
  page in the other is a **blocker**, not a content gap.

## Messages

Use ICU MessageFormat. **Arabic has six plural categories** — `zero`, `one`, `two`, `few`,
`many`, `other` — and code written against English's two produces wrong Arabic for most counts.

```json
{
  "results": "{count, plural, zero {لا توجد نتائج} one {نتيجة واحدة} two {نتيجتان} few {# نتائج} many {# نتيجة} other {# نتيجة}}"
}
```

- One message per sentence, with placeholders. Never assemble a sentence from fragments — word
  order differs and the result is ungrammatical.
- Keys describe meaning, not position: `form.submit`, not `button2`.
- Add a lint step that fails the build on a key present in `en` and missing in `ar`. Silent
  fallback to English is how a bilingual product ships half-translated.

## Fonts

Load Arabic and Latin faces through `next/font` with explicit subsets, and give both a real
fallback:

```ts
// app/fonts.ts — a layout file may not export these, so keep them here and import them
import { IBM_Plex_Sans, IBM_Plex_Sans_Arabic } from 'next/font/google'

// IBM Plex Sans: DGA's typography page. IBM Plex Sans Arabic: DGA's Assessment Checklist, item 3.
// Regular, Medium, Semibold, Bold are DGA's listed weights for IBM Plex Sans; DGA lists none for
// the Arabic face, so the same four are this kit's choice.
// Inline the weight arrays: a shared `const` widens to string[] and fails next/font's types.
export const plex = IBM_Plex_Sans({
  subsets: ['latin'], weight: ['400', '500', '600', '700'], display: 'swap', variable: '--font-plex',
})
export const plexArabic = IBM_Plex_Sans_Arabic({
  subsets: ['arabic'], weight: ['400', '500', '600', '700'], display: 'swap', variable: '--font-plex-arabic',
})
```

Import both into `app/[locale]/layout.tsx`, put their `.variable` classes on `<html>`, and keep
the kit's **Latin-first** order:
`--dga-font-sans: var(--font-plex), var(--font-plex-arabic), system-ui, sans-serif`. `next/font`
renames the families, so the quoted names in `tokens.css` will not match a `next/font` load.
`next/font/google` downloads the files at build time and serves them from your own domain; an
offline build needs `next/font/local` with the same families and weights.

- Subset aggressively. Unsubset Arabic faces are large, and the Arabic subset is the one on the
  critical path for the default locale.
- `display: 'swap'`, and make sure the fallback metrics are close — a swap between faces with
  different metrics reflows Arabic text noticeably.
- Verify the face covers the digits and currency symbol you actually render.

## Checks worth automating

- Grep for physical CSS properties (`margin-left`, `text-align: right`, `left:` …) — should be empty
- Message-key parity between `ar` and `en`
- No hardcoded user-facing strings in components
- Screenshot diff of every route in both locales at each breakpoint
