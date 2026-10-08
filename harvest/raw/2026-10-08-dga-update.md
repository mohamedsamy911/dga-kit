# Raw capture — DGA update, 2026-10-08

Evidence for the re-harvest triggered by the sentinel run of 2026-10-08 (`harvest/sources.py
--check`, exit 1: DGA deployed, stylesheet `PDaQ7SHU` → `CYyqM6kT`, bundle `cnrvMddo` →
`BO_6JOKP`). Captured from https://design.dga.gov.sa/ in **English**, through the rendered SPA,
with the global nav, drawer and footer chrome removed.

## Method — reproducible, and checked against DGA's own bytes

Pages were rendered in a browser after switching the locale to English, navigating in-page
(`history.pushState` + `popstate`, the same router path a nav click takes), and reading the
page's `innerText`.

Every fenced passage below was then **machine-checked against DGA's own strings**: the live
bundle `assets/index-BO_6JOKP.js` and all 167 lazy chunks it imports were downloaded, and each
fenced sentence was confirmed present verbatim (whitespace and typographic apostrophes
normalised). A transcription slip in this file therefore fails that check rather than becoming a
quote. The page text is DGA's i18n strings, which is why the bundle is an exact witness.

What was found **unchanged** since 2026-08-27, by the same byte check:

- **Tokens.** `harvest/reconcile-tokens.py --write` against the live stylesheet reproduces
  `harvest/RECONCILIATION.md` exactly apart from the build label (1,126 names, 2,528
  declarations, 412 unreconciled, same split), and all 121 distinct hex values in `tokens.json`
  are still declared.
- **Quoted prose.** Of the 114 sentences fenced as DGA text in the 2026-08-27 and 2026-08-28
  captures, 93 are still verbatim in the live bundle. The 21 that are not: 18 line items of the
  old change log, which DGA replaced (below), and 3 `/support` FAQ lines that are still live but
  were captured with elisions.
- **Typography** and **Iconography** foundation pages: the rules the kit carries are unchanged.

What this capture does **not** cover: the prose of the 50 component pages and the 19 templates
already harvested was not re-read page by page. Only the fenced August quotes above were
re-verified.

---

## `/updates/change-log`

DGA **renumbered its release history**. On 2026-08-27 this page listed four releases, 1.0.0
(20 Feb 2025) to 1.0.3 (4 Nov 2025), with per-item notes. It now lists eighteen, with titles only
and **no dates**, and `/updates/change-log/version-history-1-0-3` renders this same list. Nothing
on the site maps the old 1.0.3 to a new number. The list ships as a ~1 KB chunk,
`assets/releases-<hash>.js` (`{version:"4.0.0",type:"major",highlights:4}, …`). The nav badge,
which read `Version 1.0` on 2026-08-27, now reads `Version 4.0`.

<!-- dga -->
> A change log is a record of all significant changes made to the system, including updates,
> additions, deletions, and corrections.
<!-- /dga -->

Releases listed: 4.0.0 · 3.6.0 · 3.5.0 · 3.4.0 · 3.3.0 · 3.2.0 · 3.1.0 · 3.0.0 · 2.6.0 · 2.5.0 ·
2.4.0 · 2.3.0 · 2.2.0 · 2.1.0 · 2.0.0 · 1.2.0 · 1.1.0 · 1.0.0. Titles of the ones the kit uses:

<!-- dga -->
> Version 4.0.0
>
> Hajj Template, AI Section, Saudi Font & Icon Migration
>
> Hajj template added to the template library
>
> New AI section introduced in the documentation
>
> Migration to the Saudi font across the system
>
> Full icon set migration
<!-- /dga -->

3.6.0 is titled "Foundation Day Template", 3.4.0 "National Day 95 Template". **No entry mentions
National Day 96 or Life Journeys**, both of which are live.

**"New AI section introduced in the documentation"** — no page on the site carries one on
2026-10-08: `/`, `/designing`, `/developing`, `/design-installation`, `/designing-for-mobile`,
`/migration-guide`, `/about-platforms-code`, `/support` and `/contributing` were read, and the
route table has no AI route. Announced, not found.

**"Migration to the Saudi font across the system"** — read against the typography page below,
which still restricts Saudi Font to occasions and main headings, and the live site's computed
body font, which is still `IBMPlexSansArabic`. The changelog line does not change that rule.

---

## `/guidelines/foundations/typography` — the Saudi Font rule, unchanged

<!-- dga -->
> Saudi Font is reserved exclusively for national and seasonal occasions, such as National Day
> and Founding Day. It should be limited to main headings only. Using the font in paragraph text
> or long-form content is not recommended, in order to maintain readability and ease of browsing.
<!-- /dga -->

---

## Templates — the route table

The children of `/guidelines/templates` in the SPA route table (relative `path:"…"` entries):
hajj-template, founding-day, **national-day**, **national-day-96**, **life-journeys**, home-page,
contact-us-page, form-page, help-page, feedback-section, service-page, faqs-page, sitemap-page,
page-not-found, cookies-banner, search-page, about-page, e-participation-page, content-page,
chatbot, rating-section — **21 routed**.

DGA's navigation lists **20**: `national-day` (National Day 95) is no longer in it, but
`/guidelines/templates/national-day` still renders the National Day 95 template unchanged. The
sentinel reported it as removed because it matched full-path link strings rather than the route
table — a sentinel defect, fixed in the same change as this capture.

## `/guidelines/templates/national-day-96`

<!-- dga -->
> National Day 96 Template
>
> This template is designed as part of the Saudi National Day 96 theme, featuring culturally
> inspired illustrations that reinforce national identity and highlight the significance of the
> occasion.
>
> Option 1: The template uses decorative traditional patterns as dividers inspired by the Saudi
> National Day 96 identity to separate the sections.
>
> Option 2: The template highlights the Saudi National Day 96 identity through the main section,
> decorative elements, and visual patterns distributed across the page, creating a cohesive
> national look and a consistent visual identity.
>
> Community Contribution: Hero Sections designed by Fahad BinDakhil | Saudi Icons designed by
> Norah Alotaibi, winners of the DGA National Day 96 Contribution Competition.
>
> As part of the Saudi National Day 96 theme, multiple Hero Section designs have been created to
> offer flexibility in layout, tone, and visual identity. These variations aim to reflect
> national pride while maintaining a cohesive user experience.
>
> Illustration Hero Sections: Featuring culturally inspired illustrations in green and national
> motifs to enhance Saudi identity.
>
> Photos Hero Sections: Photographic visuals combined with culturally inspired backdrops and
> national messages that reflect Saudi values, heritage, and pride. Designed to create an
> emotional connection and strengthen national identity.
>
> Hero Section with Animation: Changes between different images and colors with each transition,
> giving the page a more interactive and dynamic look.
<!-- /dga -->

The page's hero tabs are Illustration, Photos and Animation — **three**. Its footer section shows
**Dark Green Footer** only. National Day 95 had four heroes (with Leaders Portrait) and a Dark
Green or Default footer.

## `/guidelines/templates/national-day` — National Day 95, still served

<!-- dga -->
> option 2: The template highlights each title with traditional illustrations from the Saudi
> National Day 95, giving the sections a more distinctive character and stronger visual
> identity.
>
> Leaders Portrait Hero Sections: Highlighting the leadership with a bold background and official
> tone, suitable for formal presentations.
>
> Hero Section with Animation: Simplified white or green backgrounds featuring subtle motion
> elements, designed for interactive or landing pages.
<!-- /dga -->

## `/guidelines/templates/life-journeys`

<!-- dga -->
> Life Journeys
>
> The journey details page template is designed to provide users with comprehensive information
> about a specific government journey. It typically includes an overview of the journey,
> detailed steps and requirements, related journeys, and supporting information to help users
> understand and complete the process.
<!-- /dga -->

The rest of the page is the shared template guidance every template page repeats — search
behaviour, nav header, optional second nav header, the 125 × 42 px logo placeholder, the feedback
section, the footer, the two last-modified dates and the digital stamp — and it matches what
`patterns.md` already carries under *Rules that apply to EVERY template*. The live preview
(journey cards, onboarding steps, a journey-details page with stages) is demo content, not
guidance.

---

## `/contributing` — rewritten

The 2026-08-27 page (four tests, four steps with two marked "soon", submission via GitHub) has
been replaced.

<!-- dga -->
> The Platforms Code grows through collaboration. Whether you are a designer, developer, content
> creator, accessibility specialist, or digital practitioner, your contribution can help shape
> better and more consistent digital experiences across government platforms.
>
> Consistent
>
> Aligned with the Platforms Code design principles, components, and visual language.
>
> Reusable
>
> Built with scalability and reuse in mind, rather than solving for a single use case.
>
> Accessible
>
> Designed to support inclusive experiences and accessibility best practices.
>
> User-Centered
>
> Focused on real user needs and meaningful improvements to the digital experience.
>
> Well Documented
>
> Supported by clear guidance, usage recommendations, and relevant examples.
>
> Explore
>
> Review the Platforms Code and identify an opportunity where your contribution can add value.
>
> Create
>
> Design, develop, or improve a component, pattern, template, or resource following the
> Platforms Code principles and guidelines.
>
> Submit
>
> Share your contribution with the Platforms Code team for review.
>
> Review
>
> Our team will evaluate the contribution based on quality, usability, consistency,
> accessibility, and alignment with the Platforms Code.
>
> Share
>
> Approved contributions can become part of the Platforms Code and be shared with the wider
> community.
<!-- /dga -->

Contribution types listed: Icons & Illustrations · Components · Patterns · Templates & Sections ·
Documentation & Guidance · Accessibility Improvements.

The **Submit** button is a `<button>` with no `href`; clicking it opens
`https://hawi.gov.sa/club/club-details/<id>` in a new window. Two such `hawi.gov.sa` club URLs are
in the bundle. The page no longer mentions GitHub. A *Champions — DGA National Day 96* section
links two new narrative pages, `/contributing/hero-section-case-study` and
`/contributing/icons-case-study`, which describe the winning entries and state no rules.
