# Phase 0 — capture design.dga.gov.sa

I can't reach the site from my session (fetch proxy blocked, search 403, no Chrome
extension connected). This is the one step that needs you. Budget ~30–45 minutes.

## Fastest path first

Before capturing page by page, check whether DGA publishes a **downloadable design kit** —
a Figma library, a UI kit, an icon pack, or a token/CSS file. It's usually linked from the
homepage or a "Resources" / "Downloads" / "Get started" section. If one exists, drop it in
`INBOX/` and it shortcuts most of what's below, with exact values instead of transcribed ones.

## Capture method

For each page: **Ctrl+P → Destination "Save as PDF" → Save** into `dga-kit/harvest/INBOX/`.

PDF, not screenshot, and not "Save page as". PDF keeps the text selectable *and* keeps the
spec diagrams — component pages routinely put a measurement in the diagram that never appears
in the prose, and that's exactly the value that gets lost.

Before printing a page, expand anything collapsed on it — accordions, tabs, "show code"
toggles, state pickers. Collapsed content doesn't print.

Name files `NN-section-page.pdf` in the order you capture them, e.g. `03-foundations-color.pdf`.

## What to capture

Tick as you go. If a section doesn't exist on the site, write "not present" next to it —
knowing a rule is absent is as useful as knowing what it says.

### Foundations — capture every page
- [ ] Colour — roles, hex values, and any stated contrast pairings
- [ ] Typography — Arabic and Latin scales: size, line-height, weight, tracking. Note the font families and where to get them.
- [ ] Spacing / layout scale
- [ ] Grid and breakpoints
- [ ] Corner radii, elevation / shadow
- [ ] Iconography — style rules, sizes, the icon set itself
- [ ] Motion — durations, easings

### Components — capture every component page
Every one, even the ones you think you won't use. Cheaper now than mid-sprint.
For each, make sure the print includes: anatomy, variants, sizes, **all states**
(default / hover / focus / active / disabled / loading / error), RTL notes, and the
do/don't examples.

### Patterns & templates
- [ ] Page templates / layouts
- [ ] Forms — validation, error handling, required-field marking
- [ ] Data tables, search, filtering
- [ ] Authentication (Nafath) if covered
- [ ] Error pages, empty states, notifications
- [ ] Multi-step / wizard flows

### Accessibility
- [ ] Every accessibility page — DGA's requirements and any stated WCAG level

### Content & language
- [ ] Arabic-first / bilingual rules, ar↔en parity expectations
- [ ] Tone of voice, terminology glossary
- [ ] Numerals (Arabic-Indic vs Western), dates (Hijri / Gregorian), currency, phone, address, national ID

### Brand & identity
- [ ] Government entity logo lockups, co-branding, clear space
- [ ] Favicon / app icon requirements

## While you capture — fill in CAPTURE-LOG.md

One line per page: URL, date, and the page's stated version or "last updated" date if it
shows one. That log is the audit trail behind every rule the skills later assert, and it's
what makes a re-harvest a readable diff instead of an archaeology project.

## When you're done

Tell me, and I'll read `INBOX/` and build the reference files and design tokens.
Then a designer — ideally a native Arabic speaker — reviews the extract before anything
gets built on top of it. That review is the gate on Phase 1.
