# Content and language

**Source:** design.dga.gov.sa templates, components and foundations · **Retrieved:** 2026-08-26

DGA publishes no standalone content style guide. The rules below are gathered from where they
actually appear — template guidance and component pages. Where DGA is silent, that is recorded
rather than filled in.

## Bilingual operation

**Language switching** — with two languages (Arabic and English), a **direct toggle button**.
On press the page updates or reloads immediately with **all** elements in the new language:
text, menus, instructions, and interactive content including buttons. With more than two
languages, a **dropdown**.

The site itself ships in Arabic and English (`العربية` toggle).

**Parity:** every route must exist in both locales. A page present in one language and missing
in the other is a compliance failure, not a content backlog item.

## Required copy

Some strings are effectively prescribed by DGA:

| Where | Required content |
|---|---|
| Feedback section, **every page** | **"Was this page useful?"** with **Yes / No**, plus reason options |
| 404 page | A friendly message — DGA's example: *"Sorry! We can't find the page you're looking for."* Plus a CTA: "Back to the homepage" / "Back To Home" |
| Chatbot opening | Brief friendly introduction — DGA's example: *"Hello! How can I help you today?"* |
| Chatbot close | *"Was this helpful? [Yes/No]"* |
| Search, no results | **"No Data Found"** |
| Filter reset | **"Clear Filter"** or **"Reset Filter"** |
| Show more content | **"View All"** or **"Show All"** |
| FAQ categories | An **"All"** category is mandatory |

## Tone

- **404s:** avoid overly technical language; be friendly and concise
- **Links:** descriptive text. **"Click here" and "go to" are explicitly forbidden.**
- **Tags:** words that describe a state or status; **avoid labels that will truncate**
- **Errors:** indicate by colour **and** text — e.g. "Invalid selection", "Required field"
- **Form steps:** each has a clear title stating what is required, then a short direct
  description of what to do

## Dates and freshness

Every page carries **two** last-modified dates — one for the page, one for the platform.

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
  carry `rel="noopener noreferrer"`

## Content limits DGA states

| Limit | Value |
|---|---|
| Search / FAQ pagination | after **10** items |
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
