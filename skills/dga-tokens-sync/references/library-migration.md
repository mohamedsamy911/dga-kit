# Library migration (Figma)

**Source:** /migration-guide · **Retrieved:** 2026-08-26

The designer-side counterpart to token sync. When DGA publishes a new library version:

## Files to re-download

- PC 1.0 Foundations
- PC 1.0 icon pack
- PC 1.0 Components – Desktop UI Kit
- PC 1.0 Components – Mobile UI Kit

## Procedure

1. Import the new library file into the project folder (a team file **and** a project folder
   inside it must exist)
2. Open it in Figma
3. Publish it to the team holding the design files
4. Click the library icon → select the library to replace → choose the new one. Components in
   use are swapped automatically.

## ⚠️ The failure mode

> When swapping, Figma updates styles and components with **matching names**, including sets and
> variants. Ensure component names haven't changed in the previous library.

A renamed component **silently fails to swap** and keeps the old definition. After any migration,
diff the component inventory before and after, and check anything that didn't update.

## Version history DGA publishes

Current: **PC 1.0** (site Version 1.0). The only changelog entry on the migration page is
**May 2024 — General Enhancement**, covering Labels, Textarea and Tabs (clarity, contrast, font
size; resize behaviour and padding; layout, transitions and keyboard navigation).

Watch `/updates/change-log` and `/updates/roadmap` for releases.

## Contributing back

DGA accepts design, code and documentation contributions via GitHub. Criteria: relevance, broad
impact over niche cases, minor fixes always welcome, major additions (new components) get
thorough evaluation. Community forums and published contribution guidelines are both marked
**"soon"**. Contact: DS-DGA@dga.gov.sa.

**Worth doing:** the 11 documentation defects in `harvest/CAPTURE-LOG.md` are exactly the kind of
minor contribution DGA says it wants.
