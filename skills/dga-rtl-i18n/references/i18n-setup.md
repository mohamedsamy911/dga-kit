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
- Every route must exist in both locales. A 404 in one language and a page in the other is a
  bilingual-parity **blocker**, not a content gap.

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
import localFont from 'next/font/local'
// Family and weights come from the DGA type scale — TODO(harvest)
```

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
