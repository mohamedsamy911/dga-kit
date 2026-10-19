---
name: dga-rtl-i18n
description: Arabic-first RTL layout and bilingual localisation for Saudi government platforms — logical CSS properties, bidirectional text handling, Arabic typography, Hijri dates, numeral and currency formatting, and ar/en parity. Use when building or fixing anything that renders in Arabic, when text or layout looks wrong in RTL, or when setting up i18n in Next.js.
---

# Arabic-first RTL and localisation

This project is Arabic-first: `ar` is the primary locale and `en` is the secondary one.
Build every screen RTL-first and check LTR after, not the other way round — an LTR layout
with Arabic poured into it is the single most common failure and it never fully recovers.

## Read these when the task needs them

- `references/rtl-rules.md` — what mirrors and what doesn't, bidi text handling, the CSS
  properties that are *not* automatically logical, Arabic typography rules
- `references/formats.md` — dates (Hijri and Gregorian), numerals, currency, phone, national ID
- `references/i18n-setup.md` — Next.js locale routing, next-intl, Arabic font loading

## What DGA actually says about RTL

**Very little.** On 2026-10-19 every string in DGA's live site build (`index-BO_6JOKP.js`) was
searched, in English and Arabic, for a fixed set of direction words, and each hit was checked on
the rendered page. The list is complete for those words in that build. Cite the page you rely on,
not a total: the next DGA deploy can change it.

**Explicit guidance** — Quote is the one page with an RTL accessibility item:

<!-- dga -->
> Support for Right-to-Left (RTL) Languages: Use the dir="rtl" attribute or apply appropriate CSS styling to ensure the text and layout adapt to RTL languages seamlessly.
<!-- /dga -->

- **Steps** — *"progresses from left to right or right to left for RTL languages"*, and the
  final step *"has no line on the right side (or the left side if it is RTL)"*
- **Buttons** — leading or trailing icon use varies with *"interface directionality"*
- **Change log 1.0.0** — Structured List and Pagination each *"Added RTL variant"*

**Written right-to-left first** — DGA assumes Arabic without saying so:

- **Search and FAQs pages** — applied filter results list *"from right to left"*
- **Sitemap page** — indentation measured *"on the right side"*, +16px per level

**A physical side, direction unstated** — the English and Arabic text name the same side:

- **Textarea** — *"a scrollbar on the right side"*
- **Second Nav Header** — quick-action icons *"on the right side of the header"*
- **Navigation Header** — *"The image on the left likely represents a company or website logo"*
  (DGA's "likely": a description of the picture, not a placement rule)

⚠️ Do not turn these three into rules in either direction. DGA does not say whether they mirror.
Kit policy: check the placement visually in DGA's template for each language before choosing a
side, and build with logical properties so either answer is a one-line change. Record the choice
in `../dga-brand-overlay/SKILL.md` with the project's other mirroring decisions.

**DGA's own components (code, not guidance)** mirror more than the guidance says: `dga-icon`
flips any icon named `arrow` or `chevron` in RTL by default, and Pagination and Date Picker
rotate their arrow buttons under `[dir=rtl]`.

**Everything else is this project's responsibility**, and that is what this skill exists for.

**Numeral system and calendar: DGA states no policy.** Not Arabic-Indic vs Western, not Hijri vs
Gregorian. DGA's own demos are Gregorian. Say DGA is silent and point at
`../dga-brand-overlay/SKILL.md`, where the project's decision is recorded — never pick one silently.

## The five that catch everyone

**1 · Logical properties only.** `margin-inline-start`, not `margin-left`. `inset-inline-end`,
not `right`. `text-align: start`, not `left`. Physical properties are the reason a layout
"mostly works" in RTL and then breaks in three places nobody checked. A grep for
`margin-left|margin-right|padding-left|padding-right|\bleft:|\bright:|text-align:\s*(left|right)`
in your styles should return nothing.

**2 · Some CSS is never logical.** `transform`, `box-shadow`, `text-shadow`,
`background-position`, and gradient directions do not flip with `dir`. Those need an explicit
`:dir(rtl)` override. This is where "we used logical properties everywhere" quietly stops being
true.

**3 · Isolate every embedded LTR run.** A phone number, URL, ID, filename, or English brand
name inside Arabic text will drag its neighbouring punctuation to the wrong side. Wrap it in
`<bdi>`. This is not cosmetic — it produces genuinely unreadable strings.

**4 · Arabic has six plural forms.** `zero`, `one`, `two`, `few`, `many`, `other`. Code written
against English's two will produce wrong Arabic for most counts. Use ICU MessageFormat and
supply all six; never build a sentence by concatenating fragments.

**5 · Never letter-space Arabic.** Arabic is a connected script — `letter-spacing` breaks the
joins and renders the word as disconnected letters. Scope any tracking rule to Latin text.

## Definition of done

The same screen in `ar` and `en`: no layout regressions, no untranslated strings, no clipped
or overflowing text (Arabic runs longer than English more often than people expect), correct
focus order in both, and every date, number and currency in the locale's format.
