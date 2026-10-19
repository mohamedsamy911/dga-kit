---
name: dga-launch-gate
description: Pre-launch DGA compliance gate for a Saudi government digital service — the transparency, content, registration and platform-integration requirements beyond design. Use before go-live, for a compliance audit, or when asked what a Saudi government site must publish.
---

# DGA launch gate

Wider than design. This is the go-live checklist: what a Saudi government platform must
**publish and integrate**, not how it must look. Design compliance is `dga-design-review`'s job;
accessibility is `dga-a11y`'s. This skill owns everything else.

Sourced from DGA's template guidelines, chiefly **About the Entity** and **e-Participation** —
the two pages carrying the transparency mandate. Full detail in
`../dga-design-system/references/patterns.md`. Also from DGA documents outside the design site,
each labelled where it is used: the **Assessment Checklist** (`references/assessment-checklist.md`),
the **registration controls** DGA-1-2-2-106 (`references/registration-controls.md`), and the two
**measurement reports** (`references/measurement-indicators.md`).

## Run in this order — registration first

### 1 · Registration and identity (start early — these have lead times)
DGA regulatory controls, DGA-1-2-2-106 v2.0 — `references/registration-controls.md`. Report these
as their own list, citing the control number.
- [ ] **DGA approval before launching a new platform** (circular 5589), and a **registration
      certificate** through Raqmi's "تسجيل منصة جديدة" service (2-106-09). DGA defines the
      certificate as granted before development begins; registering data alone is **not** approval
- [ ] On a platform registered with DGA, **new services and changes to registered services** have
      DGA's approval before launch (2-106-41)
- [ ] **Digital Stamp** issued (2-106-30) and displayed — the stamp page's registration number,
      tied to the entity's **License Number**; DGA's checklist (item 11) puts it **at the top of
      the page**, its certificate number linked, at most two secondary elements beside it
- [ ] Domain correct for entity type — authorities and ministries are **`gov.sa`**; seasonal
      platforms launch on a **subdomain** (2-106-25); internal platforms are registered on a
      subdomain of the entity's main government domain (2-106-37)
- [ ] **IPv6** and **DNSSEC** on the domain (2-106-72); the **servers hosting the entity's
      domains** inside Saudi Arabia (2-106-73) — domain hosting, not every server
- [ ] HTTPS, verifiable through the Digital Stamp

> 🚩 The certificate and registration number are a procurement dependency, not a build task. Chase
> them in week one. **2-106-12** is why any of this applies: the entity applies the Platforms
> Code on all its platforms, apps and websites, new or already registered.

### 2 · Required on every page
- [ ] **Skip-to-content link** at the start of the header
- [ ] **Accessibility Tools** in the footer — DGA: *"may include features like font size
  adjustment or contrast settings"*
- [ ] Header and footer, if detached: original structure and style kept — colours and fonts unchanged
- [ ] Arabic is the primary language, and switching languages updates **the entire content**
  without loss (DGA checklist item 39: *"without any loss or omission of information"*); the
  toggle reloads **every** element including interactive content. That every route exists in
  both locales is *kit policy*, the way the kit applies item 39

### 2b · DGA template guidance on every page — advisory
DGA repeats these on every template page but words them as benefits, not obligations. Check for
them; report a miss as **"does not follow DGA's template guidance"** — never as non-compliant, a
Blocker, or a reason a launch fails.
- [ ] **Feedback section** — "Was this page useful?" with Yes/No (DGA: *"the most important
  element"*); reason options, which DGA says *"helps"*. Its results feed the e-Participation
  statistics page
- [ ] **Last modified date for the page** and **for the platform** — DGA explains why each helps
- [ ] **Accessibility Tools first in tab order** (advisory) — DGA's Chatbot template: *"the correct approach
  is to ensure that accessibility tools and options are placed at the beginning of the tab order"*

### 3 · Required pages
- [ ] Home · Contact us · Help & Support · FAQs · Sitemap · **404** · Search · Content
- [ ] **About the Entity** (see §4) · **e-Participation** (see §5)
- [ ] **Cookies banner**, if one is shown — message, Privacy Policy link, Accept All; Reject All and Manage
      Preferences *"if required by regulations"*. If a Manage Cookies view is offered (DGA: *"Is
      optional"*), Strictly Necessary is always on and uneditable
- [ ] Prescribed navigation paths, reflected in the sitemap:
      `Homepage > About the Entity > e-Participation` and `… > Contact us`
- [ ] From DGA's checklist (`references/assessment-checklist.md`): the footer carries official
      links, the entity's logos, contact information and privacy policies (item 27); privacy and
      security notices are linked at login, registration and wherever user data is collected
      (item 41); the sitemap is comprehensive and up to date (item 37)

### 3b · Saudi law — Personal Data Protection Law (not DGA guidance)
Law, not design guidance and not legal advice: `references/pdpl.md` (Bureau of Experts, Arabic
text as amended, read 2026-10-19). **Report these as a separate "Saudi-law observations" list.
They do not change the DGA verdict below.**
- [ ] **Art. 12** — a privacy policy is available before data is collected, and addresses purpose,
      data, collection method, storage, processing, destruction, rights, and how to exercise them
- [ ] **Art. 13** — where data is collected directly, notice comes **before collection begins**,
      including whether collecting all or part of it is mandatory or optional
- [ ] **Art. 5 / 7** — except where the law provides otherwise, consent can be withdrawn; no
      unrelated consent is required to use the service
- [ ] **Art. 11** — only the data the stated purpose needs, collected without misleading wording

The PDPL does not mention cookies. Do not cite it for the cookie banner.

### 4 · About the Entity — the transparency mandate
- [ ] Senior management: photos, official information, biography links, contact details, unified format
- [ ] All departments, each expanding in place to a one-or-two sentence description
- [ ] **Organisational diagram built as a real diagram, NOT an image** (readability and accessibility)
- [ ] Sister entities
- [ ] Links to the national platforms: `my.gov.sa` · `data.gov.sa` · `istitlaa.ncc.gov.sa` ·
      Tafaul · `boe.gov.sa` · `etimad.gov.sa` · Jadaara
- [ ] Strategies listed and linked, archived ones marked `[Archived]`
- [ ] Policies published: core functional · **Service Level Agreement** · **Privacy Policy** ·
      **Freedom of Information** · **Data Sharing** · **Open Data** · **E-Participation** ·
      **Sustainable Development**; plus regulations and bylaws
- [ ] **Budgets: current plus the last five**, each linked to the MoF National Budget page *and*
      its open dataset
- [ ] Tenders via **Etimad** — planned, open and completed, each with step-by-step access instructions
- [ ] Partnerships across five categories (international, government, private, civil society,
      academic), each with objectives, target groups, benefits, timeline, projects, outcomes
- [ ] UN SDGs: overview, all 17 listed, **up to 5** the entity contributes to, tied to Vision 2030
- [ ] Careers: planned recruitment, open vacancies, **Jadarat** links, volunteering if applicable
- [ ] News newest-first and filterable; events filterable by category, date or alphabetically

### 5 · e-Participation and Open Data
- [ ] e-Participation page, visible on the homepage and in the top nav
- [ ] Open Data section referencing the **National Open Data Platform**, linking the entity's
      section on **open.data.gov.sa**
- [ ] **Open Data Policy** aligned with National Data Management Office legislation
- [ ] **Open Data Library** — datasets, publication frequency, national platform link
- [ ] **Open Data Use Cases**
- [ ] **Open Data Request** form — process, mechanism, response time, **automatic acknowledgement**
- [ ] **Performance statistics page**, reachable from the footer, previous year from 1 January,
      from Google Analytics; "Was this page useful?" as a pie chart with percentages visible
      without hover; totals and per-reason counts; support tables **≤10 rows × 10 columns**

### 6 · Measurement regimes
The entity is scored against these; adopting Platforms Code feeds both. Both are now described in
`references/measurement-indicators.md` (DGA's public reports, read 2026-10-19):
- [ ] **Digital Transformation Measurement** (Qiyas) — measures the **entity**: 95 criteria answered
      in DGA's measurement system. The criteria are not public. Record: *not assessed by this kit*;
      ask the entity for its latest results
- [ ] **Digital Experience Maturity Index** — an annual expert assessment of **selected**
      platforms (59 in 2026); detailed criteria go only to the owning entities. Record: *not
      assessed by this kit*; ask for the platform's detailed report if it was assessed. Its four
      interface recommendations (overlays, login, search, WCAG AA) are advisory; see the
      reference
- [ ] DGA's own **Assessment Criteria** — `/AssessmentCriteria`, and the **checklist** DGA asks
      teams to submit: `references/assessment-checklist.md`, all 56 items

> ## The verdict is FAIL or INCOMPLETE — never PASS
>
> | Verdict | When |
> |---|---|
> | **FAIL** | a checked, cited launch requirement fails. A failure found against a partial rubric is still a real failure. Advisory template guidance, DXMI recommendations, checklist statuses and Saudi-law observations are reported in their own lists and never decide FAIL. |
> | **INCOMPLETE** | no cited applicable failure was found in the items checked. Write it out in full: *"INCOMPLETE — no cited applicable failure found in the checked items; DGA's assessment and approval, and the entity's measurement results, were not verified. This is not a DGA go-live approval."* |
>
> **PASS is unavailable, and stays unavailable.** Go-live approval is DGA's to give, through its
> own assessment — the next step after an INCOMPLETE is to submit to it (two weeks ahead; see
> below). The two measurement regimes cannot be scored from outside the entity. A PASS from this
> kit would be an approval it has no standing to issue, and a green artefact gets forwarded to
> people who will not read this paragraph.

**The Assessment Criteria are published.** Full rubric in `references/assessment-criteria.md` —
read it before any go-live call. In short:

- **Four scored categories:** Accessibility · Consistency · Design · Usability
- **Four Mandatory criteria** — DGA's page groups them under the heading *Essential*: Design
  System Compliance · Typography and Color Standards · Layout and Spacing (mobile-first, spacing
  grid) · Mobile Usability. DGA's stated consequence, verbatim:
  a project failing these **"*typically* cannot proceed to deployment"**. Report it with the hedge — DGA describes the
  normal outcome and names no exception process, so this gate must not upgrade it to a guarantee
- **Four Recommended criteria**, including *"Ensure an **Arabic-first content strategy**"* — DGA's
  own words, so cite `/AssessmentCriteria` rather than presenting Arabic-first as this kit's
  inference
- **Optional** is named but has no published criteria. Do not invent them
- Submit **two weeks ahead**; the review runs **~20 days** with a revision cycle built in. Budget
  five weeks from "done" to approval
- A **1–10** compliance score with named levels. **No passing threshold is published** — do not quote a target

> **The checklist file is captured** (2026-10-19): `references/assessment-checklist.md`. Its 56
> items sit in two groups, المعايير الأساسية (1–43) and المعايير الثانوية (44–56). DGA does not map
> them onto the page's Mandatory / Recommended / Optional; keep them apart.

## Output

Pass/fail per item, with evidence links and a named owner for every open item. This is the
artefact attached to the go-live approval.
