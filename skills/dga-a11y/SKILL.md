---
name: dga-a11y
description: Accessibility audit against WCAG 2.1 AA and Saudi DGA "Platforms Code" accessibility requirements. Use when auditing a running app, a build, or a component library for accessibility compliance.
---

# DGA accessibility audit

DGA's stated target is **WCAG 2.1 AA**. DGA publishes no numbered rule set of its own — its
requirements are stated per component, in prose. `../dga-design-system/references/accessibility.md`
consolidates them; read it before auditing.

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
| Notification timing — ≥5s, none for critical | Timing, not markup |
| Screen reader in Arabic | Pronunciation, `lang` switching on mixed content, bidi order |
| Skip-to-content link works | Presence is checkable; that it lands correctly is not |
| Target size ≥44×44px | Computed size, often only wrong at one breakpoint |

**4 · Report** split into Automated / Manual / Passed, each item citing DGA *and* WCAG.

## DGA thresholds to assert against

- Text contrast **4.5:1** small, **3:1** large, **3:1** UI components and graphics
- Target size **44×44px**
- Body line height **≥1.5×** font size
- Auto-dismissing notifications **≥5s**; no timeout on critical
- Skip-to-content link at the start of every header
- Reading order matches visual order; landmark elements present
- Nothing conveyed by colour alone; elevation paired with borders or outlines

⚠️ **Where DGA contradicts itself, apply the stricter reading and flag it.** Known: large-text
boundary is 24px on the colour page, "18.5 Bold or 24 Regular" on typography.

⚠️ **Known DGA token defect:** `--text-secondary` (#dba102) is designated a text role but
measures 2.30:1 on white. Flag every use on a light surface as a Blocker even though it is a
DGA token — see `../dga-design-system/references/CONTRAST-AUDIT.md`.

## Where DGA is silent — name the fallback

**Motion durations and easings** (none published — but `prefers-reduced-motion` support **is**
required, on the Filtration, Loading and Skeleton pages, so cite it as a DGA rule rather than a
WCAG fallback) · Arabic screen-reader behaviour ·
focus order under RTL · testable cognitive criteria · the accessibility-statement page. For
each, fall back to WCAG 2.1 AA and **say so in the report** rather than implying a DGA rule.

## Definition of done

Runs unattended in CI, in both locales, and its output is trusted enough to block a merge.
