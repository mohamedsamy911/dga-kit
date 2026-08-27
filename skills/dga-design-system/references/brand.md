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

> The IBM Plex Sans font has been chosen as the unified font for **all platforms in the Kingdom of
> Saudi Arabia**.

DGA's four stated reasons:

- Supports **100 global languages**
- Supports **eight** font weights
- Compatible with Android, Microsoft and Apple operating systems
- *"Extensive studies and tests have been conducted to ensure it provides a smooth and easy
  reading experience"*

> ⚠️ **This page still names no Arabic body face.** It says IBM Plex Sans is the unified font and
> stops there. The gap recorded in `capture-log.md` stands: DGA is silent on the Arabic typeface
> for body text, and Saudi Font is restricted to national occasions, headings only. Do not read
> *"supports 100 global languages"* as a statement that IBM Plex Sans Arabic is mandated — DGA
> does not name it.

> The **Latin-first stack order** matters and is this kit's guidance, not DGA's:
> `"IBM Plex Sans", "IBM Plex Sans Arabic", system-ui, sans-serif`. Reversing it makes the Arabic
> face render Latin from its own Latin glyphs, so the face DGA actually names never renders.
> See `../../dga-ui-adapter/references/token-wiring.md`.

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
National Day, Founding Day. It is licensed separately from the Ministry of Culture. Never in
paragraph or long-form text.

Occasion templates carry their own visual identity — National Day 95 illustrations, Founding Day
Najdi architecture motifs — applied through DGA's supplied templates rather than invented.

## Entity overlay — decisions to record here

`TODO(entity)` — this section is where the project records its own answers, once confirmed:

- the entity's own brand colours, and exactly where they may override DGA tokens (given that header and
  footer are fixed)
- The entity logo asset (DGA's reference is 125×42) and its clear-space rules
- the entity's DGA **registration number** and **License Number** for the Digital Stamp component
- The contested icon-mirroring decisions from `../../dga-rtl-i18n/references/rtl-rules.md`:
  media playback controls, magnifying glass, charts with a time axis. Decide once, record here.
