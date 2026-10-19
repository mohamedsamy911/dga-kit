# DGA go-live checklist

Tickable form of `SKILL.md`. Attach the completed copy to the go-live approval.

**Service:** ______________________  **Date:** __________  **Signed off by:** ______________

## 0 · Registration — start in week one, these have lead times

DGA regulatory controls, DGA-1-2-2-106 v2.0 (`registration-controls.md`):

- [ ] DGA approval before launching a new platform (circular 5589)
- [ ] Registration certificate through Raqmi, "تسجيل منصة جديدة" (2-106-09) — registration alone is not approval
- [ ] New services, and changes to registered services, approved by DGA before launch (2-106-41)
- [ ] DGA registration number obtained
- [ ] Entity License Number obtained
- [ ] Digital Stamp issued (2-106-30), populated with both, **at the top of the page** (DGA checklist item 11)
- [ ] Domain correct for entity type (an authority is `gov.sa`; seasonal platforms on a subdomain, 2-106-25; internal platforms on a subdomain of the main government domain, 2-106-37)
- [ ] IPv6 and DNSSEC (2-106-72); servers hosting the entity's domains in Saudi Arabia (2-106-73)
- [ ] HTTPS live and verifiable through the Digital Stamp

## 1 · On every page

- [ ] *Advisory — DGA template guidance:* Feedback "Was this page useful?" + Yes/No; reason options
- [ ] *Advisory — DGA template guidance:* Last modified date — page, and platform
- [ ] Skip-to-content link at the start of the header
- [ ] Accessibility Tools in the footer (DGA's examples: font size, contrast)
- [ ] *Advisory — DGA template guidance:* Accessibility Tools reachable **first in tab order** (DGA's Chatbot template)
- [ ] Header and footer, if detached: original structure and style kept — colours and fonts unchanged
- [ ] Switching languages updates the entire content without loss (DGA checklist item 39); every
      route in **both** `ar` and `en` is the *kit policy* that applies it
- [ ] Language toggle reloads every element, interactive content included

## 2 · Required pages

- [ ] Home · [ ] Contact us · [ ] Help & Support · [ ] FAQs · [ ] Sitemap
- [ ] 404 with friendly message + "Back to homepage" CTA
- [ ] Search · [ ] Content
- [ ] About the Entity (§3) · [ ] e-Participation (§4)
- [ ] Cookies banner, if shown — message, Privacy Policy link, Accept All; Reject All and Manage Preferences
  *"if required by regulations"*
- [ ] Cookies: if a Manage Cookies view is offered (DGA: optional), Strictly Necessary always on and uneditable
- [ ] Nav path `Homepage > About the Entity > e-Participation` reflected in the sitemap
- [ ] Nav path `Homepage > About the Ministry/Authority/Platform > Contact us` reflected in the sitemap

## 2b · Saudi law — PDPL (not DGA guidance, not legal advice; `pdpl.md`; reported separately)

- [ ] Art. 12: privacy policy available before collection; addresses purpose, data, collection method, storage, processing, destruction, rights, how to exercise them
- [ ] Art. 13: where data is collected directly, notice before collection begins, incl. whether all or part is mandatory or optional
- [ ] Art. 5 / 7: except where the law provides otherwise, consent can be withdrawn; no unrelated consent required for the service
- [ ] Art. 11: only the data the stated purpose needs; no misleading wording

## 3 · About the Entity — transparency mandate

- [ ] Senior management: photos, official info, bio links, contacts, unified format
- [ ] All departments, each expanding in place
- [ ] Organisational diagram — **built as a diagram, NOT an image**
- [ ] Sister entities
- [ ] National platform links: my.gov.sa · data.gov.sa · istitlaa.ncc.gov.sa · Tafaul ·
      boe.gov.sa · etimad.gov.sa · Jadaara
- [ ] Strategies listed + linked, archived marked `[Archived]`
- [ ] Policies: core · SLA · **Privacy** · **Freedom of Information** · **Data Sharing** ·
      **Open Data** · **E-Participation** · **Sustainable Development**
- [ ] Regulations and bylaws page
- [ ] Budgets — current **plus last five**, each linked to MoF National Budget + open dataset
- [ ] Tenders via Etimad — planned, open, completed, with access instructions
- [ ] Partnerships × 5 categories, each with objectives/groups/benefits/timeline/outcomes
- [ ] UN SDGs — overview, all 17, up to 5 the entity contributes to, tied to Vision 2030
- [ ] Careers — planned, open, Jadarat links, volunteering if applicable
- [ ] News newest-first + filterable; events filterable

## 4 · e-Participation and Open Data

- [ ] e-Participation page, on homepage and in top nav
- [ ] Open Data section referencing the National Open Data Platform
- [ ] Entity section linked on **open.data.gov.sa**
- [ ] Open Data Policy, aligned with NDMO legislation
- [ ] Open Data Library — datasets, publication frequency, platform link
- [ ] Open Data Use Cases
- [ ] Open Data Request form — process, mechanism, response time
- [ ] Request form sends an **automatic acknowledgement**
- [ ] Performance statistics page, reachable from the footer
- [ ] Stats: previous year from 1 January, from Google Analytics
- [ ] "Was this page useful?" as a pie chart, percentages visible **without hover**
- [ ] Totals and per-reason counts shown
- [ ] Support tables ≤ 10 rows × 10 columns

## 5 · Design and accessibility

- [ ] `dga-design-review` run on every template — zero Blockers
- [ ] `dga-a11y` run against the built app in **both** locales — zero Blockers
- [ ] Contrast pairings checked against `CONTRAST-AUDIT.md`
- [ ] `prefers-reduced-motion` respected; no animation above 3 flashes/second

## 6 · Measurement

- [ ] DGA Assessment Checklist completed — all 56 items, each with DGA's own status (تطبيق كلي /
      تطبيق جزئي / غير مطبق / N/A); see `assessment-checklist.md`
- [ ] Digital Transformation Measurement (Qiyas): entity's latest results requested — *not
      assessed by this kit*
- [ ] Digital Experience Maturity Index: platform's detailed report requested, if it was assessed —
      *not assessed by this kit*

> ⚠️ §6 is **not scorable by this kit** — the two measurement regimes' criteria are not public
> (`measurement-indicators.md`). The overall verdict is FAIL or INCOMPLETE, never PASS.

## 7 · DGA Assessment Criteria — the four Mandatory criteria

DGA: failing these *"typically cannot proceed to deployment"*. Keep the hedge when reporting.

Full rubric and the Recommended set: `assessment-criteria.md`.

- [ ] **Design System Compliance** — Platforms Code correctly implemented
- [ ] **Typography and Color Standards** — approved text and functional colours
      (⚠️ `text.secondary` #dba102 is 2.30:1 — use `secondary-gold.800` or darker for gold text)
- [ ] **Layout and Spacing** — wireframe dimensions, **mobile-first**, spacing grid
- [ ] **Mobile Usability** — touch interactions, viewport sizing, navigation on small screens

Timing, not a tickbox:

- [ ] Assessment submitted **at least two weeks** before the desired review date
- [ ] Evidence pack prepared per criterion — references, screenshots, code snippets
- [ ] Checklist reviewed by **someone other than its author** before submission
