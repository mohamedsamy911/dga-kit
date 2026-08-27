# Raw capture — section sweep, 2026-08-27

Evidence for the pages found missing by the coverage validation of 2026-08-27. Captured from
https://design.dga.gov.sa/ in **English**, via in-page SPA navigation (see *Method* below).
Text is verbatim page content with the global nav, drawer and footer chrome removed.

**Why this sweep happened.** The kit had been validated area-by-area but never against the
site's own route table. Extracting every `href` from the DOM produced the authoritative page
list and showed 13 pages the capture log did not account for — including one template, three
Thoughts articles, and the **Assessment Criteria**, which the kit had recorded as an off-site
download it could not reach.

## Method — reproducible

The site is a client-rendered SPA. Two things that do **not** work:

- `fetch('/thoughts/atomic-design')` returns the 3,983-byte app shell for every route.
- Deep-linking with the browser's address bar bounces to `/`.

What works:

```js
document.querySelector('a[href="/thoughts/atomic-design"]').click()   // real click drives the router
await new Promise(r => setTimeout(r, 3000))
```

Then extract the **content** `<main>`, not the first one — there are two, and
`document.querySelector('main')` returns the navigation drawer:

```js
let m = document.querySelector('h1'); while (m && m.tagName !== 'MAIN') m = m.parentElement
m.innerText
```

Switch to English before capturing: the default locale is Arabic. Click the element whose text
is exactly `English`.

The full route table comes from:

```js
[...new Set([...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')))].sort()
```

---

## `/guidelines/templates/rating-section`

<!-- dga -->
> Rating Section
>
> The Rating Section Component is a crucial interface element that allows users to provide
> feedback, typically through a stars. It plays an essential role in evaluating user satisfaction
> and identifying areas for improvement.
>
> **Guidelines**
>
> Rating Section: The most important element in the evaluation section is the question, "How would
> you rate this service?" accompanied by a star rating component. By including specific numbers
> indicating whether the service was helpful or not, it becomes easier to accurately identify
> issues or strengths to enhance the experience.
>
> **Submission Confirmation** — Success Message: After the user submits their rating, a
> confirmation page will appear indicating that their response has been successfully submitted.
>
> **Mobile Version** — Rating Section - Mobile Version: In the mobile version, the buttons will be
> placed below the text to ensure a better user experience and a smoother layout for smaller
> screens.
<!-- /dga -->

---

## `/AssessmentCriteria`

The page the kit recorded as an unreachable off-site download. It is a full published page.

<!-- dga -->
> The assessment criteria of Platforms Code is designed to ensure that all users, from designers
> and developers to project managers overseeing government digital projects, have a clear
> understanding of the expectations and standards set forth by this comprehensive design system.
<!-- /dga -->

**Purpose:** Ensure Compliance · Maintain Quality · Facilitate Improvement
**Importance:** Consistency · Scalability · Accountability
**Who should use it:** Designers · Developers · Stakeholders · Project Managers · Quality
Assurance Specialists

### Assessment categories

<!-- dga -->
> **Accessibility** — Ensuring digital products are accessible by evaluating adherence to the Web
> Content Accessibility Guidelines (WCAG) for users with disabilities, ensuring compatibility with
> assistive technologies.
>
> **Consistency** — Ensures consistency in design elements across a project, checking for uniform
> use of design tokens like colors, typography, spacing, and adherence to guidelines to maintain a
> cohesive identity.
>
> **Design** — Focuses on maintaining high UI design standards by ensuring visual consistency with
> design tokens and the UI Kit, and ensuring responsive designs for a seamless experience across
> all devices.
>
> **Usability** — Focuses on optimizing user interfaces for ease and efficiency by assessing
> clarity, intuitiveness, logical flow, load times, and task completion.
<!-- /dga -->

### Compliance levels

**Essential — Mandatory Compliance**

<!-- dga -->
> **Design System Compliance** — Ensure the Unified Design System (Platforms Code) version 1.0 is
> correctly implemented.
>
> **Typography and Color Standards** — Implement approved primary text colors and functional
> colors in line with the Unified Design System (Platforms Code).
>
> **Layout and Spacing** — Follow the specified layout and spacing guidelines, including wireframe
> dimensions, a mobile-first approach, and a spacing grid.
>
> **Mobile Usability** — Ensure the application/website is fully usable on mobile devices,
> considering factors such as touch interactions, viewport sizing, and navigational access on
> smaller screens.
<!-- /dga -->

**Recommended**

<!-- dga -->
> **Design Consistency and Standards Compliance** — Ensure the use of approved icons, adherence to
> custom icon guidelines, and consistent visual design elements. Implement components according to
> the Unified Design System
>
> **User Experience and Interaction Design** — Evaluate interaction design effectiveness, intuitive
> navigation, and efficient task completion. Ensure errors are clearly explained, feedback is
> immediate, and interface behavior is predictable.
>
> **Content Strategy and Localization** — Create a sitemap supporting user navigation and content
> discoverability. Ensure an **Arabic-first content strategy** and clear, concise language for the
> intended audience.
>
> **Usability and Accessibility** — Ensure effective search functionality and accessible help
> resources. Evaluate user feedback mechanisms, privacy notice visibility, and consistent error
> handling across the platform.
<!-- /dga -->

A third level, **Optional**, is named in the page's FAQ but has no criteria listed. The FAQ
question is *"How are mandatory, recommended, and optional criteria distinguished?"* and this is
the whole answer:

<!-- dga -->
> Mandatory criteria are non-negotiable and must be met for the project to proceed. These often
> relate to legal, security, and core functionality requirements.
>
> Recommended criteria are not essential for project approval but are advised to enhance quality,
> user experience, or future scalability. Meeting these can differentiate the project positively.
>
> Optional criteria are additional enhancements that could provide a competitive advantage or
> long-term benefits but are not critical for the current phase of the project.
<!-- /dga -->

> ⚠️ **Extended 2026-08-27.** This capture originally kept only the Optional sentence, while
> `assessment-criteria.md` quoted all three levels — so two thirds of that quote had no evidence
> here. Second finding from `evals/check-quote-fidelity.py`.

### Submission

<!-- dga -->
> Complete the Assessment Checklist including project details, expected compliance levels, and any
> particular comments. […] Assessment should be submitted **at least two weeks before** the desired
> review date to allow sufficient time for thorough assessment.
<!-- /dga -->

### Review timeline

| Days | Stage | Contents |
|---|---|---|
| 1–2 | Initial Screening | Confirmation of Submission; Preliminary Check for all mandatory documents |
| 3–10 | Detailed Assessment | Design Review; Accessibility Review; Usability Testing; Compliance Check |
| 11–12 | Compilation of Feedback | Reviewers compile reports; meeting to consolidate findings |
| 13–15 | Feedback and Revisions | Detailed feedback provided; revision period |
| 16–20 | Final Review and Approval | Revised project submitted; **approval or rejection** |
| Post-20 | Documentation and Closure | Final documentation archived; deployment or re-assessment |

### Compliance score bands

Scored 1–100, reported as a 1–10 grade:

| Grade | Band |
|---|---|
| 1 – 1.9 | Non-Compliant |
| 2 – 2.9 | Very Poor Compliance |
| 3 – 3.9 | Poor Compliance |
| 4 – 4.9 | Below Average Compliance |
| 5 – 5.9 | Fair Compliance |
| 6 – 6.9 | Moderate Compliance |
| 7 – 7.9 | Good Compliance |
| 8 – 8.9 | Very Good Compliance |
| 9 – 9.9 | Excellent Compliance |
| 10 | Outstanding Compliance |

### Consequence of failure

DGA states this only in the page's FAQ, answering *"What happens if a project fails to meet
mandatory criteria?"* — there is no section of the page with this heading. The heading here is
this capture's, not DGA's.

<!-- dga -->
> If a project fails to meet mandatory criteria, it typically **cannot proceed to deployment**. The
> project team must address the deficiencies identified during the review process and resubmit the
> project for another review. Critical failures might require significant rethinking of project
> scope, design, or even objectives.
<!-- /dga -->

> ⚠️ **Corrected 2026-08-27.** This capture originally stopped after "another review", dropping
> the third sentence — while `assessment-criteria.md` quoted all three. A reference file was
> therefore citing DGA text that this repo could not evidence. Found by
> `evals/check-quote-fidelity.py` on its first run.

The checklist itself is a download (`Download Checklist`) and is **still not obtained** — the page
describes it; the file is separate.

---

## `/thoughts/consistency-and-unified-identity`

The palette rationale. This is the source that explains *why* gold is in the system.

<!-- dga -->
> **Colors** — The green flag, the Saudi besht, and the fragrant lavender fields.
>
> […] The primary color in the Platforms code is the green color derived from the Saudi Arabian
> flag, which dates back three centuries of pride. This color was chosen to symbolize the values of
> growth, prosperity, unity, solidarity, and national cohesion carried by the Saudi flag.
>
> The **secondary colors are black and gold**, reflecting classic elegance and beauty, derived from
> the **Saudi Besht**, which represents prestige and dignity. Another secondary color is **purple**,
> reflecting the colors of lavender fields that adorn the Kingdom's deserts in the spring season.
<!-- /dga -->

<!-- dga -->
> **Fonts** — The IBM Plex Sans font has been chosen as the unified font for all platforms in the
> Kingdom of Saudi Arabia. […]
> - Supports 100 global languages.
> - Supports eight different font weights.
> - Compatible with Android, Microsoft, and Apple operating systems.
> - Extensive studies and tests have been conducted to ensure it provides a smooth and easy reading
>   experience.
<!-- /dga -->

On the goal:

<!-- dga -->
> Consistency in design also ensures that users feel comfortable and familiar when navigating
> between different digital government platforms and services […]
>
> **Enhancing Trust** · **Ease of Recognition** — Users can identify a particular service as
> government-affiliated just by looking at its design · **Effective Communication**
<!-- /dga -->

---

## `/thoughts/atomic-design`

<!-- dga -->
> We adopt an atomic design methodology to ensure organization and sustainability in the
> development of user interfaces.
<!-- /dga -->

The five levels, verbatim:

<!-- dga -->
> **Atoms** — the basic building blocks of matter, such as buttons, input fields, labels, and other
> elements that cannot be broken down any further without losing their functionality.
>
> **Molecules** — relatively simple groups of UI elements functioning together as a unit. For
> instance, a form label, input field, and button can combine to create a search form molecule.
>
> **Organisms** — relatively complex components made up of groups of molecules and/or atoms. An
> example would be a navigation bar that includes a logo, search form, and menu items.
>
> **Templates** — groups of organisms combined to form page layouts. Templates focus on the
> underlying content structure and define how different components fit together.
>
> **Pages** — specific instances of templates. They include real content and data, providing a
> tangible example of the final user interface.
<!-- /dga -->

Benefits named: Consistency · Scalability · Collaboration · Maintainability · Flexibility.

---

## `/thoughts/responsive-design`

<!-- dga -->
> Responsive design is particularly crucial for government websites, which must serve diverse
> audiences with different devices and accessibility needs.
<!-- /dga -->

**For designers**

<!-- dga -->
> **Scalable Typograph[y]** — Use relative units, like 16px (1em, 1rem) for font sizes to maintain
> readability across different devices.
>
> **Fluid Grids** — Use fluid grid layouts that adjust based on the screen size.
>
> **Responsive Breakpoints** — Set up grid systems for different breakpoints (e.g., **12-column
> grid for desktop, 8-column grid for tablet**) to guide the layout adjustments for each screen
> size.
>
> **Touchscreen Navigation** — Consider the use of touch gestures and ensure that interactive
> elements are appropriately sized and spaced for touch inputs on mobile devices.
<!-- /dga -->

**For developers**

<!-- dga -->
> **Mobile-First Approach** — Start by designing for the smallest screens and progressively enhance
> the design for larger screens.
>
> **CSS Flexbox and Grid** — Utilize CSS Flexbox and Grid layouts to create flexible and adaptive
> designs.
>
> **Container Queries** — Consider using container queries (when they become widely supported) to
> style elements based on the size of their parent container, rather than the viewport size.
<!-- /dga -->

> ⚠️ The 12/8-column figures are given as an example (`e.g.`), not as a fixed DGA grid. Cite them
> as DGA's stated example, not as a mandated column count. DGA names **no mobile column count** on
> this page.

---

## `/designing-for-mobile`

Confirms the Mobile UI Kit component list that `mobile.md` had assembled indirectly.

<!-- dga -->
> Begin your journey with our extensive Mobile UI Kit in Platforms Code, meticulously crafted for
> mobile interfaces. Similar to its web counterpart, this kit comes packed with additional
> components optimized for mobile views.
<!-- /dga -->

<!-- dga -->
> **Tailored Experience** — Mobile Navigation Bar · Tap Bar · Top Bar · Splash Screen · Mobile
> Modal · Date Picker
<!-- /dga -->

That is the whole page. There are **no specs** for these six — the page is a Figma download
landing page, so the Figma-only gap stands.

---

## `/contributing`

<!-- dga -->
> Platforms Code flourishes with contributions from designers and developers like you.
<!-- /dga -->

**Should I contribute?** Relevance · Broad Impact · Minor Enhancements (bug resolutions, new icons)
· Major Additions (new components need thorough evaluation).

**How to contribute** — four steps, two of which are not live:

| # | Step | Status |
|---|---|---|
| 1 | Familiarize Yourself | live |
| 2 | Join the Community (forums, community meetings) | **soon** |
| 3 | Follow Contribution Guidelines (on the GitHub page) | **soon** |
| 4 | Submit Your Contributions via GitHub | Submit |

Types: Design Contributions · Code Contributions · Documentation.

> ⚠️ No GitHub URL is published on this page. Steps 2 and 3 are marked "soon", so there is no
> public contribution guideline document to cite yet.

---

## `/support`

Support routes: Documentation · Community (**soon**) · Contributions. Plus 15 FAQs. The ones that
carry facts not stated elsewhere:

<!-- dga -->
> **What are the main components of the Platforms Code design system?** — a Designer UI Kit,
> Developer Component Library, Documentation Website, and now, a Mobile Design Library.
>
> **What tools are included […] for developers?** — resources such as a **Storybook** for showcasing
> UI components, code snippets, documentation, and integration guidelines.
>
> **Is the Platforms Code design system customizable to fit our organization's branding and style?**
> — Yes […] It provides guidelines and resources for customization while maintaining consistency
> with the overall design system.
>
> **Where can I find additional support?** — through our support channels, such as **beem
> community**, or designated contacts within the organization.
<!-- /dga -->

> ⚠️ Several answers are written for an internal audience ("our organization", "internal
> communication platforms") and describe things that are not live (Storybook, community). Treat
> this page as intent, not as a citeable rule.

---

## `/about-platforms-code`

<!-- dga -->
> Platforms Code, an **open-source** design system **funded by DGA**, streamlines digital projects
> by combining code, design tools, and guidelines in a community-driven approach.
<!-- /dga -->

Published counters — **these contradict the rest of the site** and must not be cited as component
counts:

| Figure | Label |
|---|---|
| 33+ | Component — "for Streamlined Design Solutions" |
| 4,650 | Variants — "for Tailored User Experiences" |
| 12 | Adoption — "Aligned with Official Guidelines" |

> ⚠️ **33+ components** conflicts with the 50 component pages published under
> `/guidelines/components/`. The counter is stale marketing copy. This kit cites **50**, which is
> the enumerable route count. Do not reconcile the two — record the conflict.

---

## `/updates/roadmap`

<!-- dga -->
> A core principle of the design system is 'continuous improvement', thus constant development is
> expected to enhance the system.
<!-- /dga -->

| Date | Item | Status |
|---|---|---|
| Feb 2024 | Version 1.0.0 — "18 newly added components and 19 updated and fixed components" | Done |
| Sep 2024 | Templates | Done |

The Sep 2024 template release lists 16 templates: Home Page · Services Page · Search Results Page ·
E-Participation Page · Sitemap · Contact Us Page · About the Entity Page · Form Page · Help &
Support Page · 404 – Page Not Found · FAQ Page · General Content Page · Feedback Section · Cookies
Consent Banner · Chatbot Interface · **Rating Section**.

> ⚠️ The roadmap dates (Feb 2024, Sep 2024) disagree with the change log's dates for the same
> versions (20 Feb **2025**, 1 Sep **2025**). Cite the change log; it is the more specific record.
> The roadmap lists **nothing future-dated** despite describing itself as outlining future plans.

---

## `/updates/change-log`

**The current published version is 1.0.3, released 4 Nov 2025.** This kit's harvest of 2026-08-26
therefore captured 1.0.3, not a bare "1.0".

Each entry is its own route: `/updates/change-log/version-history-1-0-3` etc.

### Version 1.0.3 — 4 Nov 2025
<!-- dga -->
> Fixes & Updates:
> - **Digital Stamp:** Update digital stamp text.
> - **Templates:** Update digital stamp component.
<!-- /dga -->

### Version 1.0.2 — 1 Sep 2025
<!-- dga -->
> New Templates:
> - **National Day 95 Template**
<!-- /dga -->

### Version 1.0.1 — 5 May 2025
<!-- dga -->
> Fixes & Updates:
> - **Digital Stamp:** Added Mobile view.
> - **Slide-out menu:** Update the Menu list item.
> - **Progress indicator:** Fixed description text alignment.
<!-- /dga -->

### Version 1.0.0 — 20 Feb 2025
<!-- dga -->
> New Components: Charts · Carousel · Chips · Code Snippet · Digital Stamp · Divider · Floating
> Button · Filtration · Metric · Number Input · Progress Bar · Quote · Radial Stepper · Skeleton ·
> Slider · Search Box · Slide-out Menu · Second Level Nav Header
>
> Fixes & Updates:
> - **Card:** Fixed states variant. Added expanded and selected variants.
> - **Checkbox:** Fixed prototype issue.
> - **Date Picker:** Added a nested instance of the Year Dropdown. Adjusted padding between the
>   label and field to 8px (previously 4px). Added darker and lighter styles.
> - **File Uploader:** Added Helper Text AR variant.
> - **Modal:** Fixed Featured Icon.
> - **Menu:** Added selected state.
> - **Notifications:** Added Helper Text AR variant.
> - **Nav Header:** Fixed prototype issues. Removed entity logo. Fixed placeholder logo.
> - **Nav Drawer:** Fixed placeholder logo.
> - **Radio Button:** Added prototype.
> - **Rating:** Fixed prototype issue.
> - **Structured List:** **Added RTL variant.**
> - **Tabs:** Fixed divider alignment.
> - **Tags:** Adjusted icon color.
> - **Footer:** Added links. Fixed prototype issues.
> - **Digital Signature:** Updated Name to be **Digital Stamp**.
> - **Pagination:** **Added RTL variant.**
> - **Search Box:** Fixed the tooltip on focused state.
<!-- /dga -->

> Two entries bear on the open `TODO(verify)` for DGA's own RTL statements: **Structured List** and
> **Pagination** each shipped an explicit "RTL variant". That is DGA's own record of an RTL
> decision, and neither is a page-level statement — so it is evidence for the enumeration, not the
> enumeration itself.

> The Date Picker entry says the label-to-field padding was corrected from 4px to **8px**. Any
> value harvested from a Figma file older than 20 Feb 2025 would be wrong.
