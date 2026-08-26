# Formats

Use the platform `Intl` APIs. Do not hand-roll formatting, and do not use a date library's
own locale data when `Intl` covers it — `Intl` ships the CLDR data the OS and browser agree on.

> **`TODO(harvest)`** — which calendar is primary, which numeral system, and the exact date
> masks are DGA policy decisions, not engineering ones. They come from
> `dga-design-system/references/content.md` once Phase 0 lands. Until then, state the
> assumption you're making rather than silently picking one.

## Dates

```js
// Hijri (Umm al-Qura — the Saudi civil calendar)
new Intl.DateTimeFormat('ar-SA-u-ca-islamic-umalqura', {
  day: 'numeric', month: 'long', year: 'numeric'
}).format(d)

// Gregorian, Arabic locale
new Intl.DateTimeFormat('ar-SA-u-ca-gregory', { dateStyle: 'long' }).format(d)

// Gregorian, Arabic locale, Western digits
new Intl.DateTimeFormat('ar-SA-u-ca-gregory-nu-latn', { dateStyle: 'long' }).format(d)
```

- `islamic-umalqura` is the correct calendar identifier for Saudi civil use. Plain `islamic`
  is a different (astronomical) reckoning and can differ by a day.
- Government services frequently show **both** calendars. If the design shows one, confirm
  that's intentional before building it.
- Store timestamps in UTC, format at the edge. Never store a formatted date.

## Numerals

`ar-SA` defaults to Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩). Force Western digits with `-u-nu-latn`:

```js
new Intl.NumberFormat('ar-SA-u-nu-latn').format(1234.5)  // 1,234.5
new Intl.NumberFormat('ar-SA').format(1234.5)            // ١٬٢٣٤٫٥
```

The choice is a policy decision and it must be consistent product-wide — mixing the two
across screens is the failure mode here, more than either choice being wrong. Note that
Arabic-Indic digits use different group and decimal separators (`٬` and `٫`), which affects
column width in tables.

**Never render digits as Arabic-Indic in anything the user copies into another system** —
reference numbers, IDs, IBANs, tracking codes. Those stay Western and get wrapped in `<bdi>`.

## Currency

```js
new Intl.NumberFormat('ar-SA', { style: 'currency', currency: 'SAR' }).format(1250)
```

⚠️ **Verify the symbol.** Saudi Arabia adopted a new riyal symbol, and runtime `Intl` data may
render `ر.س`, `SAR`, or the new glyph depending on the browser's ICU version. Check what your
target browsers actually produce, check what DGA specifies, and if they disagree, render the
symbol yourself rather than trusting the runtime. Fonts also need to contain the new glyph.

## Phone numbers

Saudi format: `+966 5X XXX XXXX` for mobile. Store E.164 (`+9665XXXXXXXX`), format for display.
Always wrap in `<bdi>` inside Arabic text — the `+` is a neutral character and will jump.

## National ID / Iqama

Ten digits; `1` prefix for citizens, `2` for residents. Two rules:

- **Wrap in `<bdi>`.** It's an LTR run and will otherwise break surrounding punctuation.
- **Mask by default.** Show the last four only, and reveal on explicit user action. Full IDs
  are personal data under PDPL — confirm the exact display and retention requirements against
  the DGA standards harvest before shipping a screen that shows one. `TODO(harvest)`

## Sorting

`Intl.Collator('ar')` for Arabic strings — code-point sort is wrong for Arabic. Where a list
mixes Arabic and Latin entries, decide which group sorts first and make it consistent; the
collator won't decide that for you.

## Relative time

```js
new Intl.RelativeTimeFormat('ar', { numeric: 'auto' }).format(-3, 'day')
```

Prefer this to hand-written "منذ ٣ أيام" strings — Arabic's dual and plural forms make
hand-written relative time wrong for most values.
