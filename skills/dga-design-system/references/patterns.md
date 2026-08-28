# Patterns and page templates

**Source:** https://design.dga.gov.sa/guidelines/templates/* · **Retrieved:** 2026-08-26
**19 templates**, not the 13 the nav suggests. Six are reachable only from the templates index:
e-Participation, About the Entity, Content Page, Cookies Banner, Chatbot, Rating Section.

Each template page offers a live preview, the code, and a Figma file.

---

## Rules that apply to EVERY template

These repeat verbatim across all templates. Treat them as global requirements — a page missing
any of them fails review regardless of which template it follows.

### Feedback section — required
> The most important element in the feedback section is the **"Was this page useful?"** question
> with **"Yes" and "No"** buttons. Including options for specific reasons why the page was or
> wasn't useful helps in pinpointing exact issues or strengths.

Not optional, and not just the yes/no — the follow-up reason options are part of the requirement.
Their results feed the performance-statistics page (below).

### Two last-modified dates — required
- **Last modified date for the page** — so users can judge whether the content is current
- **Last modified date for the platform** — signalling the platform is actively maintained

Both. Most teams ship only the first.

### Nav header and footer — do not restyle
> When detaching the nav-header **adhere strictly to the original structure and style. Do not
> alter the colors or fonts.** Same instruction for the footer.

A recoloured header or footer is a Blocker.

### Logo placeholder
**W: 125px × H: 42px.** If the logo is compressed, adjust dimensions to match rather than
distorting it.

### Search behaviour
- **Autocomplete** — real-time suggestions, updating dynamically as the user types
- **Clear button** — appears once typing starts, disappears when empty, **must be keyboard
  accessible**
- On the search page specifically: the typed portion is **highlighted within the suggestions**,
  and the query **remains in the field after searching** so it can be edited

### Second nav header
Optional. When used, build it from library components and take its background from the design
tokens. Hovering a button shows a tooltip naming the action.

### Language switching
- **Two languages (Arabic/English): a direct toggle button.** On press the page updates or
  reloads immediately with *all* elements in the new language — text, menus, instructions, and
  interactive content including buttons.
- **More than two: a dropdown.**

### Clickable vs unclickable cards
A card meant to drive an action **needs a CTA button**. A display-only card may omit it if the
card already carries enough information.

### Mobile
Long titles with limited horizontal space: **put the button below the content**, stack
vertically — and apply the same structure consistently across all sections.

---

## Home page

Hero section: when using an image background, prioritise image quality, text readability and
responsiveness.

**"View All" button** — place it prominently, close to the element indicating more content
exists. Label it plainly: "View All" or "Show All".

**Year of AI logo** — approved versions only (coloured for light/neutral backgrounds, white for
dark backgrounds or images), no modifications, adequate clear space, used consistently. If two
logos are already present it becomes the **third**, laid out **horizontally on desktop and
stacked vertically on mobile**.

---

## Service page

- **Service description** — concise, covering the essentials of the service process
- **Steps to obtain the service** — clearly **numbered**, each easy to follow
- **Service card** must carry: target audience · service duration · channels · cost · contact
  details · a link to the FAQs

---

## Form page

Built for **multi-step** forms.

- Steps **numbered (1, 2, 3…)**, each with a **clear title** stating what is required and a
  **short description** giving specific instructions
- **Large screens: Progress Indicator. Mobile and small screens: Radial Stepper** — a specific
  responsive component swap, not a styling choice
- Required fields use the text input's built-in required-information feature

---

## Page not found (404)

- Avoid overly technical language. "404 – Page Not Found" and "Something Went Wrong" are both
  acceptable, but **add a friendly message**: *"Sorry! We can't find the page you're looking for."*
- **A CTA is required** — "Back to the homepage" / "Back To Home". A second ("Go Back") is optional.

---

## Search page

- **Pagination** after **10 items**, at the bottom of the list. Current page clearly highlighted;
  Next/Previous arrows included.
- **"Clear Filter" button** near the filter options, labelled plainly ("Clear Filter" / "Reset
  Filter")
- **Mobile filtering uses a dropdown** to avoid clutter
- Applied filter results list **from right to left** *(DGA writes its own guidance assuming RTL)*,
  each with a delete icon
- Multi-checkbox search with no match shows **"No Data Found"**
- **"Sort By"** toggles its icon between ascending and descending
- Page description **truncates after two lines**
- Tags optional — clear, concise, colour-coded
- **External links get an icon** marking them as off-platform
- **File links get an icon** chosen by file type, or the file extension in the label

---

## Content page

Two shapes: standard (light/medium content, linear flow) and heavy content **with a Table of
Contents**, which DGA notes improves accessibility and SEO.

Media: images and videos at full width or smaller, always responsive. Links inside the text body
pull the reader in contextually; links at the end act as independent references when there are
many.

---

## Contact us

- **Emergency contacts** — optional
- **State management** — use the design system's neutral / critical / warning / success /
  informational notifications to communicate outcomes
- Text input error states must show helper text guiding the correction

---

## Cookies banner 🚩

- **Message** — concise explanation of why cookies are used
- **A "Privacy Policy" link** to the full policy
- **Actions:** Accept All · **Reject All** (where regulations require) · **Manage Preferences**
  (where regulations require)
- **Manage cookies modal:** Strictly Necessary cookies are **always enabled and uneditable**;
  every optional category individually toggleable. Actions: Confirm Choices · Reject All ·
  Close (without saving).
- Optional: confirmation message with **Undo**, and an error state when preferences fail to save

---

## Chatbot

- Brief friendly introduction naming its purpose and capabilities
- Key areas: general enquiries · guidance on forms · **checking service statuses** · directing
  users to departments
- **End-of-session feedback** — "Was this helpful? [Yes/No]"
- **Escalation to a human**, with response times stated when no one is available
- Multiple languages; **text-to-speech and speech-to-text**

**🚩 Accessibility Tools must come FIRST in the tab order.**
> Users relying on assistive technologies need quick access to essential tools without tabbing
> through the entire page… Use the `tabindex` attribute strategically.

This pairs with the footer's Accessibility Tools requirement: the controls live in the footer but
must be **reachable first by keyboard**.

**Floating button placement:** must not cover important content, including on mobile; must
contrast against its background (add a shadow or white border if the colour can't change); two
buttons stack vertically; more than two go into an expandable menu.

---

## e-Participation page 🚩

Citizen engagement in decision-making — opinions on upcoming laws, economic projects and
developmental initiatives.

**Breadcrumb path is prescribed:** `Homepage > About The Entity > e-Participation`, and it must be
reflected in the sitemap, visible on the homepage, and reachable from the top nav.

### Open Data — required section
- Objectives of open data, **referencing adoption of the National Open Data Platform**, with a
  link to the entity's section on **open.data.gov.sa**
- **Open Data Policy** link, aligned with legislation from the National Data Management Office
- **Open Data Library** — datasets, publication frequency, link to the national platform
- **Open Data Use Cases** — initiatives reusing the data for the community
- **Open Data Request** form — process, mechanism, expected response time, and an **automatic
  acknowledgement** of receipt

### Website and services performance statistics — required
- Reached from the footer: `E-Participation > Portal and Services Performance Statistics >
  Portal Performance Statistics`
- Previous year's data from **1 January**, sourced from **Google Analytics**; filter by year if
  segmented
- **"Was this page useful?" results as a pie chart** — percentage on hover *and* shown below the
  chart without interaction; totals and counts for both answers and for each reason category
- Optional: downloadable data file (stating that clicking downloads directly), and supporting
  tables **capped at 10 rows × 10 columns**

---

## About the Entity page 🚩 — the transparency mandate

The largest compliance surface in the design system. Required sections:

**Organisational structure** — senior management with photos, official information, biography
links and contact details in a unified format · all departments, each expanding to a one-or-two
sentence description on the same page · **an organisational diagram that must NOT be an image** —
build it as a hierarchical diagram or flowchart so it stays readable and accessible when scaled ·
sister entities.

**Specialized national platforms** the entity must link to:
`my.gov.sa` (National Platform) · `data.gov.sa` (Open Data) · `istitlaa.ncc.gov.sa` (Legal
Consultations) · Tafaul (e-Participation) · `boe.gov.sa` (Laws and Legislation) ·
`etimad.gov.sa` (Tenders and Procurements) · Jadaara (Unified Recruitment)

**Strategies and policies** — all strategies and policies listed and linked, archived ones marked
`[Archived]`. Named policies: core functional policies · Service Level Agreement · **Privacy
Policy** · **Freedom of Information Policy** · **Data Sharing Policy** · **Open Data Policy** ·
**E-Participation Policy** · **Sustainable Development Policy**. Plus regulations and bylaws.

**Budget and expenditures** — **current plus the last five budgets**, each linked to the Ministry
of Finance National Budget page *and* to the corresponding open dataset. Archived marked
`[Archived]`.

**Tenders and procurements** — via **Etimad**, covering planned, open and completed, each with
step-by-step instructions and images for reaching them.

**Partnerships** — international organisations · government entities · private sector · civil
society · academic institutions. Each with objectives, target groups, benefits, timeline,
projects and expected outcomes.

**Sustainable Development Goals** — overview of the UN SDGs, the Kingdom's position, all 17
listed, and **up to 5** the entity contributes to, tied to Vision 2030.

**Careers** — planned recruitment for the current year · current openings with qualifications and
skills · links to **Jadarat** · volunteering, if applicable. Each expands in place on click.

**News and events** — newest first, filterable alphabetically or by date; events optionally on
their own page, filterable by category, date or alphabetically.

**Navigation paths prescribed:** `Homepage > About the Ministry/Authority/Platform > e-Participation`
and `… > Contact us`, both reflected in the sitemap.

---

## FAQs page

- **Search inside FAQs** — recommended once there are **more than 20 questions**. Real-time
  results as the user types, with **matches highlighted**. With categories, results show under
  "All".
- **Categories** — optional, but preferred above 20 questions across different fields.
  **The "All" category is mandatory.** On mobile, **no more than five** categories before
  switching to a dropdown.
- **Pagination** after 10 items
- **Answer evaluation** (optional) below the answer, with a confirmation message once rated

---

## Help & support page

Multiple contact methods (Contact Us, FAQs), service availability, and response times.

**Card sizing:** all cards match the largest card in height *and* width, for a unified layout.

---

## Sitemap page

- **Clear heading labels for SEO**; breadcrumbs using the same structure as the rest of the site
- **Filled points = main pages · Empty points = subpages**
- **Link sizes:** main page → Medium · subpage → Small
- **Indentation:** main links start at **0px on the right side**; subpages start at **16px and
  increase by 16px per level** (16 / 32 / 48…)
- External links carry an off-platform icon

> ✅ *"spacing on the right side"* — DGA specifies indentation from the **right**. Another place
> the guidelines are written RTL-first.

---

## Feedback section (standalone page)

Rating, comments and suggestions, with clear prompts. The "Was this page useful?" question and
its reason options are the core; **additional questions are guidance and may be adapted.**

- **Submission confirmation page** after submitting
- **Mobile:** buttons go **below** the text

---

## Rating section
`/guidelines/templates/rating-section` retrieved 2026-08-27

A **separate template** from the feedback section above, and easy to conflate with it. The two ask
different questions of different things:

| | Feedback section | Rating section |
|---|---|---|
| Question | *"Was this page useful?"* | *"How would you rate this service?"* |
| Subject | the **page** | the **service** |
| Control | Yes/No plus reason options | the **star Rating component** |

DGA's own wording:

<!-- dga -->
> The most important element in the evaluation section is the question, "How would you rate this
> service?" accompanied by a star rating component.
<!-- /dga -->

- The star control is the **Rating** component (`/guidelines/components/feedback/rating`) - do not
  substitute a numeric or thumbs control
- Show **specific numbers** alongside the stars. DGA's stated reason: it makes it easier to
  identify issues or strengths accurately rather than reading a bare average
- **Submission confirmation page** after submitting, same as the feedback section
- **Mobile:** buttons go **below** the text, same as the feedback section

> Both patterns can appear on one platform. A service page carrying only *"Was this page useful?"*
> has not satisfied the rating template, and vice versa.

---

## Seasonal and occasion templates

The only place **Saudi Font** is permitted — and headings only.

### National Day 95
Culturally inspired illustrations reinforcing national identity. Two section treatments:
traditional patterns as dividers, or traditional illustrations marking each title.
**Four hero variants:** Leaders Portrait (formal) · Illustration (green, national motifs) ·
Photos (heritage backdrops) · **Animated** (white or green, subtle motion).
Footer: Dark Green or Default.

### Founding Day 2026
Dark themes inspired by **Najdi architecture**, traditional ornaments as dividers. Three section
options; heroes: Historic Architecture · Expressive Imagery (horsemen, warm heritage gradients) ·
Animated.
**Ehsan element** — an optional floating button linking to the Ehsan platform, included because
Founding Day 2026 coincides with Ramadan.

### Hajj 2026 template
`/guidelines/templates/hajj-template` · retrieved 2026-08-27

Visual identity drawn from Hajj and the **"Hayyakum Allah"** (حياكم الله) slogan — welcoming the
Guests of Allah, and DGA's stated framing of the Kingdom's role in serving pilgrims.

**Two section treatments** (DGA calls them Option 1 / Option 2):
- **Option 1** — decorative dividers between sections, keeping the overall design simple
- **Option 2** — visual patterns inside certain sections (services, backgrounds), for a richer
  feel and a stronger identity through the page

**Three hero variants:**
- **Background – Object** — dark background with an arch-framed image; DGA describes the object
  treatment as adding depth and a spiritual atmosphere
- **Background – Color** — neutral background taken from the photo's dominant tone, keeping the
  text area calm and readable
- **Background – Image** — image-led, the photo blending softly into the text side

**Ehsan element** — an optional floating button linking to the **Adahi (sacrifice) service** on
the Ehsan platform during the Hajj season. Same component as the Founding Day one above; the
floating-button rules below apply unchanged.

> The page repeats the **Saudi Font** rules verbatim: download from the Ministry of Culture,
> national and seasonal occasions only, **main headings only**, never paragraph or long-form
> text. See `brand.md` — this page is a second source for the same rule, not a new one.

**Floating-button rules (shared with Chatbot):** must not cover important content, including on
mobile; must contrast with its background (add shadow or white outline if the colour is fixed);
two buttons stack vertically; more than two go into an expandable menu.

---

## Where the templates address RTL

Adding to the component-level list, the templates assume RTL as the default reading direction:

- **Search page / FAQs page** — applied filter results list *"from right to left"*
- **Sitemap page** — indentation measured *"on the right side"*, increasing by 16px per level
- **Language switching** — a direct ar/en toggle that reloads *every* element including
  interactive content

Together with Quote, Steps and Buttons these are the places DGA speaks to RTL that this harvest
found. ⚠️ **Do not cite a total** — the count was never enumerated at capture time and is
`TODO(verify)`; cite the specific page you rely on. See https://github.com/mohamedsamy911/dga-kit/blob/master/COVERAGE.md, *Disputed and unverified
claims*.
