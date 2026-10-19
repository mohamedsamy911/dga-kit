# Brand and identity

**Sources:** https://design.dga.gov.sa/guidelines/templates/* (seasonal and occasion pages, header/footer rules) ·
https://design.dga.gov.sa/guidelines/foundations/typography · https://design.dga.gov.sa/guidelines/foundations/iconography ·
**Retrieved:** 2026-08-26
**Also:** https://design.dga.gov.sa/thoughts/consistency-and-unified-identity — **Retrieved:** 2026-08-27
(the only page where DGA explains *why* the palette and the typeface are what they are)

> Brand rules are **cross-cutting**: DGA publishes no single brand page, so these are gathered
> from the page set above. Individual rules cite their specific page inline where one exists.

## Entity logo

**Placeholder: W 125px × H 42px.** Build the logo as a component and swap it into the
placeholder. If it compresses, adjust dimensions to match rather than distorting it.

## Nav header and footer — do not restyle

> When detaching the nav-header, **adhere strictly to the original structure and style. Do not
> alter the colors or fonts** to maintain consistency with the overall design.

The same instruction is repeated for the footer on every template page. Recolouring either is a
compliance failure, not a brand choice — this is the main constraint on how far an entity's own
identity may go.

## Year of AI logo

- Approved versions only: **coloured** on light or neutral backgrounds, **white** on dark
  backgrounds or images
- No modifications; maintain clarity and adequate clear space; use consistently across the platform
- Where two logos already exist it becomes the **third**, laid out **horizontally on desktop,
  stacked vertically on mobile**, with proper alignment, spacing and visual balance

## Colour identity

`/thoughts/consistency-and-unified-identity` · retrieved 2026-08-27

DGA's own subtitle for the palette: **"The green flag, the Saudi besht, and the fragrant lavender
fields."** Every colour in the system is a heritage reference, not an aesthetic choice.

| Colour | Derived from | DGA's stated meaning |
|---|---|---|
| **Green** (primary) | the **Saudi Arabian flag**, *"which dates back three centuries of pride"* | growth, prosperity, unity, solidarity, national cohesion |
| **Black and gold** (secondary) | the **Saudi besht** | *"classic elegance and beauty"* — prestige and dignity |
| **Purple / lavender** (secondary) | **lavender fields** that adorn the Kingdom's deserts in spring | — |

Token family for the primary is `primary-sa-flag`, with `background-sa-flag` (#074c30) as its
surface.

> 🚩 **This is why `text.secondary` (#dba102) fails contrast.** Gold entered the system as a
> **besht heritage colour**, and a text role name was attached to it afterwards. It measures
> 2.30:1 on white and fails AA at every size — see `CONTRAST-AUDIT.md`. Treat it as a brand
> accent that was mis-named, never as a text colour. `secondary-gold.800` (#945c01) is the first
> gold step that clears AA on white.

> An earlier version of this section called gold *"richness and prestige"* and lavender *"a calm
> accent"* without a source. That was paraphrase, not citation. Corrected 2026-08-27 to DGA's
> published wording.

## Typeface identity — why IBM Plex Sans

`/thoughts/consistency-and-unified-identity` · retrieved 2026-08-27

<!-- dga -->
> The IBM Plex Sans font has been chosen as the unified font for **all platforms in the Kingdom of
> Saudi Arabia**.
<!-- /dga -->

DGA's four stated reasons:

- Supports **100 global languages**
- Supports **eight** font weights
- Compatible with Android, Microsoft and Apple operating systems
- *"Extensive studies and tests have been conducted to ensure it provides a smooth and easy
  reading experience"*

> ⚠️ **This page names no Arabic body face** — it says IBM Plex Sans is the unified font and stops
> there. Do not read *"supports 100 global languages"* as naming one. **DGA's Assessment Checklist
> does** (item 3, retrieved 2026-10-19): *"Use the approved font: IBM Plex Sans Arabic, as
> specified in the Platforms Code."* Cite the checklist for the Arabic face, not this page; see
> `../../dga-launch-gate/references/assessment-checklist.md`. Saudi Font stays restricted to
> national occasions, headings only.

> The **Latin-first stack order** is this kit's policy, not DGA's:
> `"IBM Plex Sans", "IBM Plex Sans Arabic", system-ui, sans-serif`, so Latin renders in IBM Plex
> Sans, the face the typography page names. DGA's Figma Foundations file does the opposite: it
> sets IBM Plex Sans Arabic for all text (read 2026-10-19). Both are defensible; match design and
> build. See `../../dga-ui-adapter/references/token-wiring.md`.

## Why unification is mandated

`/thoughts/consistency-and-unified-identity` · retrieved 2026-08-27

Useful when an entity pushes to extend its own brand further than the header/footer rule allows.
DGA's three stated reasons are about the citizen, not about tidiness:

- **Enhancing trust** — *"citizens feel that the government is integrated, organized, and working
  diligently to meet their needs"*
- **Ease of recognition** — *"Users can identify a particular service as government-affiliated
  just by looking at its design, making it easier for them to access reliable sources"*
- **Effective communication** — unified designs make messages clearer and more effective

> The recognition argument is the one that answers *"can we restyle the header?"* — a restyled
> header removes the signal that tells a citizen the site is genuinely governmental. That is the
> rationale behind the do-not-restyle rule above.

## Seasonal identities

**Saudi Font is permitted only for national and seasonal occasions, main headings only** —
National Day, Founding Day. DGA: *"available under a license agreement from the Ministry of
Culture"*. Never in paragraph or long-form text (Hajj template: *"must not be used"*;
typography: *"not recommended"*).

Occasion templates carry their own visual identity — National Day 96 illustrations (95 left
DGA's nav on 2026-10-08 but is still served), Founding Day Najdi architecture motifs — applied
through DGA's supplied templates rather than invented.

> DGA's change log lists *"Migration to the Saudi font across the system"* under 4.0.0. The
> typography page, re-read 2026-10-08, still restricts Saudi Font to national and seasonal
> occasions and main headings only, and the live site's body font is still IBM Plex Sans Arabic.
> The rule above stands; do not read the change-log line as permission to set body text in it.

## Entity overlay — decisions to record here

`TODO(entity)` — this section is where the project records its own answers, once confirmed:

- the entity's own brand colours, and exactly where they may override DGA tokens (given that header and
  footer are fixed)
- The entity logo asset (DGA's reference is 125×42) and its clear-space rules
- the entity's DGA **registration number** and **License Number** for the Digital Stamp component
- The contested icon-mirroring decisions from `../../dga-rtl-i18n/references/rtl-rules.md`:
  media playback controls, magnifying glass, charts with a time axis. Decide once, record here.
