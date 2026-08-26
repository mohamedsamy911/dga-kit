---
name: dga-mockup
description: Produce a DGA-compliant screen mockup or wireframe for a Saudi government platform, using real Platforms Code tokens and RTL-first artboards. Use when asked to design, mock up, or wireframe a screen for a Saudi government service.
---

# DGA mockup

Generates screens that are already on-system, so what comes out of the canvas needs correcting
rather than rebuilding.

Composes with the built-in `design` canvas skill rather than replacing it — read that skill for
canvas mechanics; this one supplies the DGA constraints.

## Before drawing

1. **Which template?** DGA publishes 19. Start from the closest — home, service, form, content,
   search, FAQs, contact, help, sitemap, 404, e-Participation, About the Entity. Inventing a
   layout when a DGA template exists is the most common mockup failure. See
   `../dga-design-system/references/patterns.md`.
2. **Arabic first.** Draw `ar` first and derive `en` — not the reverse. An LTR layout with
   Arabic poured in never fully recovers.
3. **Load the tokens** from `../dga-design-system/assets/tokens.json`. Real values, never
   approximations.

## Constraints that apply to every mockup

- **Real Arabic copy**, not lorem and not transliteration
- 12-column desktop grid, 2–4 smaller; breakpoints 600 / 960 / 1280
- Container padding 16 mobile / 32 desktop; max width 1280; paragraphs 720
- Type from the DGA scale; **IBM Plex Sans only** — Saudi Font only on occasion templates,
  headings only
- **Never letter-space Arabic** — drop the −2% display tracking on Arabic text
- Show the states the screen actually needs, not just default
- Icons at 24 unless the context calls for another band

## Every mockup includes, because DGA requires them

- Header with **skip-to-content**
- **Feedback section** — "Was this page useful?" with Yes/No and reason options
- Footer with **Accessibility Tools** and **both** last-modified dates
- The **Digital Stamp**, on any public government page
- Language toggle (direct button for ar/en)

## Definition of done

The mockup passes `dga-design-review` with no blockers. If it doesn't, this skill produced work
the review will reject — fix it here.
