# DGA Assessment Checklist — the 56 items

**Source:** https://design.dga.gov.sa/assets/updated-checkList.xlsx — the **Download Checklist**
file on `/AssessmentCriteria` (and on the Designing and Developing pages) · **Retrieved:**
2026-10-19 · HTTP Last-Modified 2026-09-20 · sha256 `117d10c5…8075`
**Raw capture (every row, Arabic and English):**
[the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-assessment-checklist.md)

This is the file DGA asks a team to complete and submit with its assessment
(`assessment-criteria.md` covers the page around it). It holds **56 numbered criteria**, many with
unnumbered sub-rows that say what DGA looks for. Each row has a status dropdown: **تطبيق كلي**
(fully applied) · **تطبيق جزئي** (partly applied) · **غير مطبق** (not applied) · **N/A لاينطبق**.

> ⚠️ **Two groupings, not one.** The workbook puts items 1–43 under **المعايير الأساسية** and
> 44–56 under **المعايير الثانوية**. The `/AssessmentCriteria` page grades **Mandatory /
> Recommended / Optional**, with four Mandatory criteria. Neither source maps one onto the other,
> so do not call a الأساسية item "Mandatory", and do not tell a team a missed item
> *"typically cannot proceed to deployment"* — that sentence is about the page's Mandatory
> criteria. Report a miss as the status DGA's own dropdown would give it.

> The table quotes **DGA's English cell**. The Arabic cell is the same criterion and occasionally
> says more — item 4's second sub-row adds *«مع الالتزام بعدم استخدام المسافات المخصصة للعناصر»*,
> which the English omits. When they differ, quote both.

## The items

### المعايير الأساسية (primary — the workbook's own group; not "Mandatory")

| # | DGA's criterion (the workbook's English, verbatim) | DGA reference | Kit coverage |
|---|---|---|---|
| 1 | Ensure the Unified Design System (Platforms Code) version 1.0 is correctly implemented | `/` | `dga-design-review` |
| 2 | Ensure the use of approved colors as defined in the Unified Design System (Platforms Code) | `/guidelines/foundations/color-system` | `dga-design-review`, `dga-ui-adapter` |
| 3 | Adhere to Typography guidelines by using approved fonts, appropriate font weights for headings, and responsive typography measures | `/guidelines/foundations/typography` | `dga-design-review`, `dga-ui-adapter` |
| 4 | Ensure spacing values are applied according to the Unified Design System (Platforms Code) | `/guidelines/foundations/layout-and-spacing` | `dga-design-review`, `dga-ui-adapter` |
| 5 | Ensure responsive design that adapts effectively to different screen sizes and orientations to provide a seamless experience across devices | `/guidelines/foundations/layout-and-spacing` | `dga-design-review`, `dga-mockup` |
| 6 | Ensure usage of approved icons as per the Unified Design System (Code of Platforms) | `/guidelines/foundations/iconography` | `dga-design-review` |
| 7 | Ensure the homepage template is applied according to the platform | `/guidelines/templates/home-page` | `dga-design-review` (templates) |
| 8 | Ensure the service page template is applied | `/guidelines/templates/service-page` | `dga-design-review` (templates) |
| 9 | Ensure the e-Participation template is applied | `/guidelines/templates/e-participation-page` | `dga-design-review` (templates) |
| 10 | Ensure the search template is applied | `/guidelines/templates/search-page` | `dga-design-review` (templates) |
| 11 | Ensure digital stamp follows the Platforms Code Design System | `/guidelines/components/content-display/digital-stamp` | `dga-launch-gate` §1 |
| 12 | Ensure Buttons follow the Platforms Code Design System | `/guidelines/components/actions/buttons` | `dga-design-review`, `dga-a11y` |
| 13 | Ensure Dropdown Input follows the Platforms Code Design System | `/guidelines/components/actions/dropdown` | `dga-design-review`, `dga-a11y` |
| 14 | Ensure Link follows the Platforms Code Design System | `/guidelines/components/actions/link` | `dga-design-review`, `dga-a11y` |
| 15 | Ensure Accordions follow the Platforms Code Design System | `/guidelines/components/content-display/accordion` | `dga-design-review`, `dga-a11y` |
| 16 | Ensure Menu follows the Platforms Code Design System | `/guidelines/components/navigational/menu` | `dga-design-review`, `dga-a11y` |
| 17 | Ensure Content Switcher follows the Platforms Code Design System | `/guidelines/components/data-display/content-switcher` | `dga-design-review`, `dga-a11y` |
| 18 | Ensure Notifications follow the Platforms Code Design System | `/guidelines/components/feedback/notification` | `dga-design-review`, `dga-a11y` |
| 19 | Ensure Modals follow the Platforms Code Design System | `/guidelines/components/feedback/modal` | `dga-design-review`, `dga-a11y` |
| 20 | Ensure File Upload follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/file-uploader` | `dga-design-review`, `dga-a11y` |
| 21 | Ensure Checkbox follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/checkbox` | `dga-design-review`, `dga-a11y` |
| 22 | Ensure Radio follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/radio` | `dga-design-review`, `dga-a11y` |
| 23 | Ensure Switch follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/switch` | `dga-design-review`, `dga-a11y` |
| 24 | Ensure Textarea follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/textarea` | `dga-design-review`, `dga-a11y` |
| 25 | Ensure Tabs follow the Platforms Code Design System | `/guidelines/components/navigational/tabs` | `dga-design-review`, `dga-a11y` |
| 26 | Ensure Tags follow the Platforms Code Design System | `/guidelines/components/search-and-filters/tags` | `dga-design-review`, `dga-a11y` |
| 27 | Ensure Footer follows the Platforms Code Design System | `/guidelines/components/ui-shell/footer` | `dga-design-review`, `dga-a11y` |
| 28 | Ensure Cards follow the Platforms Code Design System | `/guidelines/components/content-display/card` | `dga-design-review`, `dga-a11y` |
| 29 | Ensure Nav Header follows the Platforms Code Design System | `/guidelines/components/ui-shell/navigation-header` | `dga-design-review`, `dga-a11y` |
| 30 | Ensure Breadcrumb follows the Platforms Code Design System | `/guidelines/components/navigational/breadcrumbs` | `dga-design-review`, `dga-a11y` |
| 31 | Ensure Avatar follows the Platforms Code Design System | `/guidelines/components/data-display/avatar` | `dga-design-review`, `dga-a11y` |
| 32 | Ensure Rating follows the Platforms Code Design System | `/guidelines/components/feedback/rating` | `dga-design-review`, `dga-a11y` |
| 33 | Ensure Tooltip follows the Platforms Code Design System | `/guidelines/components/feedback/tooltip` | `dga-design-review`, `dga-a11y` |
| 34 | Ensure Text Input follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/input` | `dga-design-review`, `dga-a11y` |
| 35 | Ensure Tables follow the Platforms Code Design System | `/guidelines/components/data-display/table` | `dga-design-review`, `dga-a11y` |
| 36 | Ensure Date Picker follows the Platforms Code Design System | `/guidelines/components/forms-and-inputs/datepicker` | `dga-design-review`, `dga-a11y` |
| 37 | Ensure that a Sitemap is created to support user navigation and facilitate content discoverability. | — | `dga-launch-gate` §3 |
| 38 | Ensure that interaction design effectively facilitates user tasks, including button responses, gesture recognition, and feedback. | — | `dga-design-review` |
| 39 | Ensure that content prioritizes the Arabic-first approach, while supporting the use of other languages in accordance with the DGA standards. | — | `dga-rtl-i18n`, `dga-launch-gate` §2 |
| 40 | Ensure that mechanisms are in place for users to provide feedback about the application/website, and that this feedback is acknowledged and utilized by the organization. | — | `dga-launch-gate` §2b |
| 41 | Ensure that the visibility and clarity of privacy and security notices are evaluated, and that they are understandable and accessible to all users. | — | `dga-launch-gate` §3, §3b |
| 42 | Ensure consistency in the terminology used across the system to prevent confusion and support user understanding. | — | `dga-content-writer` agent |
| 43 | Ensure a consistent approach to how errors are handled and displayed across the application/website to ensure a smooth user experience. | — | `dga-content-writer` agent |

### المعايير الثانوية (secondary — the workbook's own group; not "Mandatory")

| # | DGA's criterion (the workbook's English, verbatim) | DGA reference | Kit coverage |
|---|---|---|---|
| 44 | Follow the Unified Design System (Platforms Code) for the Nav Drawer component | `/guidelines/components/ui-shell/navigation-drawer` | `dga-design-review` |
| 45 | Follow the Unified Design System (Platforms Code) for the Pagination component | `/guidelines/components/navigational/pagination` | `dga-design-review` |
| 46 | Ensure the Loading component is implemented per the Unified Design System (Platforms Code) guidelines | `/guidelines/components/loading-and-status/loading` | `dga-design-review` |
| 47 | Ensure the Steps component is in line with the Unified Design System (Platforms Code) specifications | `/guidelines/components/forms-and-inputs/steps` | `dga-design-review` |
| 48 | Ensure the design establishes a clear visual hierarchy, directing the user's attention to important elements first | — | **partly uncovered** — usability is measured, not read |
| 49 | Ensure the navigation is intuitive, including logical grouping and labeling of sections and links | — | **partly uncovered** — usability is measured, not read |
| 50 | Ensure common tasks can be completed efficiently with minimal steps and intuitive interactions | — | **partly uncovered** — usability is measured, not read |
| 51 | Ensure available help resources and documentation are easily accessible, clear, and useful in assisting users to effectively use the application/website | — | **partly uncovered** — usability is measured, not read |
| 52 | Ensure the language used in the interface is clear, concise, and appropriate for the intended audience, and assess localization efforts for multilingual support | — | **partly uncovered** — usability is measured, not read |
| 53 | Evaluate whether the user interface behaves in a predictable manner, reducing user confusion and errors | — | **partly uncovered** — usability is measured, not read |
| 54 | Ensure the interaction patterns (eg, gestures, clicks, navigation) are consistent, making the system intuitive and learnable | — | **partly uncovered** — usability is measured, not read |
| 55 | Ensure the content (text, images, videos) is presented in a uniform style and tone appropriate for the target audience | — | **partly uncovered** — usability is measured, not read |
| 56 | Ensure that feedback provided to users for their actions is consistent in style and timing across the application/website to avoid confusion | — | **partly uncovered** — usability is measured, not read |


## Sub-rows that add to this kit's guidance

Quoted from the workbook's English. Each was absent from, or weaker in, the design.dga.gov.sa
pages the kit had read.

**Item 3 — the Arabic typeface.** The first time a DGA source names it:

<!-- dga -->
> Use the approved font: IBM Plex Sans Arabic, as specified in the Platforms Code.
<!-- /dga -->

**Item 6 — icons** (item 26 says the same of tags):

<!-- dga -->
> Status colors must not be used for non-status purposes.
<!-- /dga -->

<!-- dga -->
> For icons larger than 24px, use the "Featured icon" variant without modifying its colors or sizes.
<!-- /dga -->

<!-- dga -->
> If no suitable icon is available in the icon library to meet the need, a custom icon must be designed in accordance with the icon design guidelines. A request for approval should then be submitted using the link provided in the reference.
<!-- /dga -->

The link in the reference column is `https://survey.dga.gov.sa/survey/start/91ed577e-38dd-4181-9d12-1b91b4456c94`.

**Item 7 — the home page's first section after the hero:**

<!-- dga -->
> For informational platforms, include a news or info section directly below the hero section.
<!-- /dga -->

<!-- dga -->
> For service platforms, include a services section directly below the hero section.
<!-- /dga -->

**Item 8 — the service page's wording:**

<!-- dga -->
> Full adherence to the approved service page template is required, including the use of the same terms and headings, such as: Steps, Requirements, Required Documents, Service Details Card, and others, without any modification or changes.
<!-- /dga -->

**Item 11 — the Digital Stamp's placement:**

<!-- dga -->
> The stamp must be placed at the top of the page.
<!-- /dga -->

<!-- dga -->
> Verify that the certificate number is correctly linked to its corresponding certificate page.
<!-- /dga -->

<!-- dga -->
> Secondary elements (such as buttons or links) for options like sharing or accessibility tools may be added to the left side of the stamp, with a maximum of two secondary elements allowed.
<!-- /dga -->

"Left" is the workbook's word, written for the Arabic layout. It does not say where these go in
an LTR layout; report the placement you found rather than inventing a rule.

**Items 12–36 — component states.** Eighteen items name the states to apply, often split into
interactive and contextual ones (*"Apply contextual states (Selected / Unselected)"*). Five differ
from the component page: Radio, Switch, Tabs, Input and Breadcrumbs. All 18 are tabulated beside
the page's list in *Standard state set*, `../../dga-design-system/references/components.md`.
Report a state only the checklist names here, not as a page violation; mark it N/A, with the
reason, where it does not apply.

**Items 14 and 29 — external links:**

<!-- dga -->
> If the link leads to an external page, an external link icon (Link Square) must be included with it.
<!-- /dga -->

**Item 18 — which notification to use:**

<!-- dga -->
> If the notification is temporary, use Notification Toasts.
<!-- /dga -->

<!-- dga -->
> If the notification is permanent, use Inline Alerts.
<!-- /dga -->

<!-- dga -->
> For high-priority permanent alerts at the top of the page, use Notification.
<!-- /dga -->

**Item 19 — modals:**

<!-- dga -->
> Avoid using pop-ups for detailed data entry — for extensive data input, please use the form template.
<!-- /dga -->

**Item 27 — footer:**

<!-- dga -->
> Ensure the footer includes mandatory elements like official links, organization logos, contact information, and privacy policies, as specified in the Design System (Code of Platforms).
<!-- /dga -->

**Item 28 — cards:**

<!-- dga -->
> Only two adjustments are allowed: alignment of internal elements or adjusting inner spacing to create visual contrast when displaying multiple cards.
<!-- /dga -->

<!-- dga -->
> Actionable cards (clickable cards) must include clear Call-To-Action (CTA) buttons. For informational cards, CTA buttons are optional.
<!-- /dga -->

**Item 30 — breadcrumbs:**

<!-- dga -->
> Maintain consistency between the breadcrumb and the hierarchical structure of the sitemap to ensure accurate navigation and user guidance.
<!-- /dga -->

**Item 38 — motion:**

<!-- dga -->
> Avoid hiding important elements (such as buttons or content) behind animations or effects; these elements must always be visible without requiring scrolling or additional interaction.
<!-- /dga -->

**Item 39 — Arabic first, and complete switching.** Until this file, the kit said DGA states no
parity rule. The checklist does:

<!-- dga -->
> Use Arabic as the primary language across all pages and components, ensuring high-quality wording and language accuracy.
<!-- /dga -->

<!-- dga -->
> When switching between Arabic and English, the entire content must be accurately updated without any loss or omission of information.
<!-- /dga -->

**Item 40 — feedback receipt:**

<!-- dga -->
> Display a confirmation message after feedback submission to indicate successful receipt.
<!-- /dga -->

Item 40 asks for *"a clear method for users to submit feedback"*. It does not make the
per-page "Was this page useful?" section mandatory; that stays DGA template guidance.

**Item 41 — privacy and security notices:**

<!-- dga -->
> Provide clear links or messages at key interaction points—such as login, registration pages, or when collecting user data—to inform users about privacy and security notices.
<!-- /dga -->

## Observed in the workbook

- Item 8's two sub-rows on the rating and feedback components have the **same English text**
  (*"Apply the feedback component …"*); the Arabic names two components, عنصر التقييم and عنصر
  التغذية الراجعة, and their reference cells point to `rating-section` and `feedback-section`.
- Item 1 names *"version 1.0"* of the Platforms Code. The workbook was last saved 2025-07-15; the
  site's change log now lists releases up to 4.0.0 (`../../dga-design-system/dga-version.md`).
  Which release an assessment checks is not stated — ask DGA rather than assume.
- The English alternates *Platforms Code*, *Code of Platforms* and *Platform Design Code*. They
  are one product.
