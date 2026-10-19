---
name: dga-a11y
description: Accessibility audit against WCAG 2.2 AA and Saudi DGA "Platforms Code" accessibility requirements. Use when auditing a running app, a build, or a component library for accessibility compliance.
---

# DGA accessibility audit

**Audit target: WCAG 2.2 AA.** Two DGA sources name a target, and they differ:

- The Platforms Code's typography page: *"Our aim is to comply with WCAG 2.1 AA accessibility
  standards."*
- DGA's accessibility guideline (DGA-1-2-4-203, issue 2.0, May 2024) is built on **WCAG 2.2** and
  aligns with *"the international industry standard of web accessibility (WCAG 2.2 level AA)"*. Its
  levels table labels AA **"Recommended"** (A is "Essential", AAA "Optimal").

WCAG 2.2 AA contains every 2.1 AA criterion except 4.1.1 Parsing, which 2.2 removed as obsolete,
so auditing to 2.2 AA covers both. Report the **six criteria new in 2.2** under the guideline's
name and level, never as a design-site rule — and do not call AA mandatory: DGA's guideline says
"Recommended". DGA's per-component requirements are in prose on each component page;
`../dga-design-system/references/accessibility.md` consolidates them, and the guideline's own
text is in its section *DGA's accessibility guideline*. Read it before auditing.

## Procedure

**1 · Automated sweep.** Run axe-core, pa11y and Lighthouse against the built app or Storybook.
Run in **both locales** — `ar` and `en`. A pass in English proves nothing about the Arabic
build.

**2 · Map every machine finding to a DGA rule.** A raw axe violation is not actionable to a
government team; "fails DGA's stated 4.5:1 requirement, colour-system page" is. Where DGA has
no matching rule, cite WCAG and **say explicitly that DGA is silent**.

**3 · Manual checks — the ones no scanner reaches.**

| Check | Why a scanner misses it |
|---|---|
| Focus order under RTL | Scanners read DOM order, not visual order in a mirrored layout |
| Focus visibility against the *actual* background | Scanners check the token, not the composite |
| Modal focus trap, Esc, focus return to opener | Requires interaction |
| Radio-group roving tabindex + arrow keys | Requires keyboard interaction |
| Date picker grid keyboard model | Arrows/Enter/Esc, focus starting on the selected date |
| Notification timing — typically ≥5s; consider none for critical | Timing, not markup |
| Screen reader in Arabic | Pronunciation, `lang` switching on mixed content, bidi order |
| Skip-to-content link works | Presence is checkable; that it lands correctly is not |
| Target size ≥44×44px | Computed size, often only wrong at one breakpoint |
| Focus not hidden behind sticky headers, footers or banners (2.4.11) | Depends on scroll position |
| Every drag has a single-pointer alternative (2.5.7) | Requires interaction |
| Help is in the same place on every page (3.2.6) | Compares pages |
| A process never asks twice for what the user already entered (3.3.7) | Spans steps of a flow |
| Login has an option that needs no memory test or transcription (3.3.8) | Login flows sit behind auth |

**4 · Report** split into Automated / Manual / Passed, each item citing DGA *and* WCAG.

## DGA thresholds to assert against

- Text contrast **4.5:1** small, **3:1** large, **3:1** UI components and graphics
- Target size **44×44px** — DGA's *"recommended minimum"*. The WCAG 2.2 AA floor is **24×24 CSS
  px** (2.5.8), with exceptions for spacing, inline links and equivalent controls
- Body line height **≥1.5×** font size
- Auto-dismissing notifications *"typically at least 5 seconds"*; for critical ones, *"consider not
  having a timeout"*
- Skip-to-content link at the start of every header
- Reading order matches visual order; landmark elements present
- Nothing conveyed by colour alone; elevation paired with borders or outlines

⚠️ **Where DGA contradicts itself, apply the stricter reading and flag it.** Known: large-text
boundary is 24px on the colour page, "18.5 Bold or 24 Regular" on typography.

⚠️ **Known DGA token defect:** `--text-secondary` (#dba102) is designated a text role but
measures 2.30:1 on white. Flag every use on a light surface as a Blocker even though it is a
DGA token — see `../dga-design-system/references/CONTRAST-AUDIT.md`.

## DGA's own components are not a pass

A screen built on DGA's package still needs this audit. On 2026-10-19, 19 of DGA's live component
demos rendered without semantics DGA's guidance asks for: tabs without tab roles, a switch that is
a plain checkbox, a progress bar with no `progressbar` role. See
`../dga-react/references/live-demo-semantics.md`. Audit the rendered output, never the component
name.

## Where DGA is silent — name the fallback

**Motion durations and easings** (none published — but DGA asks for `prefers-reduced-motion`
support on the Filtration, Loading and Skeleton pages, so cite DGA there rather than a WCAG
fallback) · Arabic screen-reader behaviour ·
focus order under RTL · testable cognitive criteria · the accessibility-statement page. For
each, fall back to WCAG 2.2 AA and **say so in the report** rather than implying a DGA rule.

**Overlays.** DGA's Digital Experience Maturity Index 2026 recommends *"dispensing with unstable
floating external accessibility add-ons (Accessibility Overlays)"* (advisory, recommendation 4).
Build the footer's Accessibility Tools into the platform; flag a third-party overlay.

## Definition of done

Runs unattended in CI, in both locales, and its output is trusted enough to block a merge.
