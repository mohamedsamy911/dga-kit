# Content and language

**Sources:** https://design.dga.gov.sa/guidelines/templates/* · https://design.dga.gov.sa/guidelines/components/* ·
https://design.dga.gov.sa/guidelines/foundations/* · **Retrieved:** 2026-08-26

> DGA publishes **no standalone content style guide**. Every rule below is gathered from the
> page set above and cites its specific page inline. Where DGA is silent that is stated, not
> filled in.

## Bilingual operation

**Language switching** — with two languages (Arabic and English), a **direct toggle button**,
which DGA calls *"the simplest and most effective way"*.
On press the page updates or reloads immediately with **all** elements in the new language:
text, menus, instructions, and interactive content including buttons. With more than two
languages, a **dropdown**.

The site itself ships in Arabic and English (`العربية` toggle).

**Parity — kit policy:** every route must exist in both locales. DGA states no parity rule; it
only says the toggle updates *all* elements of the page. The kit treats a page present in one
language and missing in the other as a defect, not a content backlog item.

## Copy DGA gives

Mostly as examples (*"such as"*, *"like"*) — the wording is DGA's suggestion unless noted. The
Arabic column is **DGA's own Arabic**, from the same guidance on its Arabic pages (confirmed
displayed 2026-10-18; https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-18-arabic-copy.md). Use it rather than
translating the English back.

| Where | English (DGA) | Arabic (DGA) |
|---|---|---|
| Feedback section — *DGA template guidance, advisory* | **"Was this page useful?"** with **"Yes"** / **"No"**, plus reason options | «هل كانت هذه الصفحة مفيدة؟» مع «نعم» / «لا» |
| 404 page — acceptable titles | "404 - Page Not Found" or "Something Went Wrong" | «404 - الصفحة غير موجودة» أو «حدث خطأ ما» |
| 404 page — friendlier message | *"Sorry! We can't find the page you're looking for."* | «عذرًا! لم نستطع إيجاد الصفحة التي تبحث عنها.» |
| 404 page — CTA | "Back to the homepage" / "Back To Home"; optional "Go Back" | «العودة إلى الصفحة الرئيسية» / «الرجوع للرئيسية»؛ اختياري «الرجوع للصفحة السابقة» |
| Chatbot opening | *"Hello! How can I help you today?"* | «مرحبًا! كيف يمكنني مساعدتك اليوم؟» |
| Chatbot close | *"Was this helpful? [Yes/No]"* | «هل كان هذا مفيدًا؟ [نعم/لا].» |
| Search, no results | **"No Data Found"** | *DGA's Arabic page describes the message without quoting one* |
| Filter reset | **"Clear Filter"** or **"Reset Filter"** | «إزالة التصفية» أو «إعادة تعيين التصفية» |
| Show more content | **"View All"** or **"Show All"** | «عرض الكل» أو «إظهار الكل» |
| Error text (with colour) | "Invalid selection", "Required field" | «اختيار غير صحيح»، «الحقل المطلوب» |
| FAQ categories (optional) | When used: *"The 'All' category must be added."* | «يجب إضافة تصنيف الكل.» |

## Tone

- **404s:** avoid overly technical language; be friendly and concise
- **Links:** descriptive text. DGA: *"Avoid vague phrases such as "click here" or "go to.""*
- **Tags:** words that describe a state or status; **avoid labels that will truncate**
- **Errors:** indicate by colour **and** text — e.g. "Invalid selection", "Required field"
- **Form steps:** each has a clear title stating what is required, then a short direct
  description of what to do

## Dates and freshness

DGA's template guidance shows **two** last-modified dates on every page — one for the page, one
for the platform — and explains why each helps; it does not call them mandatory.

⚠️ **Calendar:** DGA's own demos are **Gregorian** ("August 2026", "21 Jan 2024") and no
guideline anywhere mentions Hijri, Umm al-Qura, or dual-calendar display. For a Saudi government
service this is a gap the project must close itself, and the decision belongs here once made.
See `../../dga-rtl-i18n/references/formats.md`.

## Numerals

⚠️ **`TODO(verify)` — DGA states no numeral policy.** Nothing on the site specifies Arabic-Indic
(٠١٢٣) versus Western (0123) digits. The site's own Arabic pages are the best available evidence;
confirm with DS-DGA@dga.gov.sa. The choice must then be consistent product-wide — inconsistency
across screens is worse than either option.

## Link conventions

- **External links** carry an icon marking them off-platform
- **File links** carry an icon chosen by file type, or show the extension in the label
- New-tab links must announce that behaviour, with visually hidden text for screen readers, and
  carry `rel="noopener"` (DGA; `noreferrer` too is the kit's suggestion)

## Content limits DGA states

| Limit | Value |
|---|---|
| Search / FAQ pagination *(optional)* | after **10** items |
| Statistics support tables | max **10 rows × 10 columns** |
| Content switcher options | **2–4** (use Tabs beyond) |
| Pie chart segments | max **6** |
| Line / bar chart series | max **3** |
| Breadcrumb items before truncation | **5** |
| FAQ categories on mobile | max **5**, then a dropdown |
| FAQ search threshold | recommended above **20** questions |
| Search result description | truncates after **2 lines** |
| Paragraph width | **720px** |

## Not covered by DGA

- **Terminology glossary** — none published
- **Numeral policy** — see above
- **Hijri dates** — absent everywhere
- **Arabic tone of voice** — no guidance beyond the per-component notes above
- **Arabic body typeface** — see `foundations.md`

For each, `dga-design-review` states that DGA is silent and names the fallback rather than
inventing a rule.
