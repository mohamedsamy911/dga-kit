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

Current published version: **1.0.3**, released **4 Nov 2025**. The Figma downloads are named
`PC 1.0 …` regardless — that is a file name, not a version.

The migration page carries only one entry of its own, **May 2024 — General Enhancement**, covering
Labels, Textarea and Tabs (clarity, contrast, font size; resize behaviour and padding; layout,
transitions and keyboard navigation). The real record is `/updates/change-log`, captured
2026-08-27:

| Version | Date | What shipped |
|---|---|---|
| **1.0.3** | 4 Nov 2025 | Digital Stamp text updated; Digital Stamp component updated across templates |
| **1.0.2** | 1 Sep 2025 | National Day 95 template added |
| **1.0.1** | 5 May 2025 | Digital Stamp mobile view; Slide-out menu list item; Progress indicator description alignment |
| **1.0.0** | 20 Feb 2025 | 18 new components; Structured List and Pagination **gained RTL variants**; Date Picker label-to-field padding corrected 4px → **8px**; "Digital Signature" renamed **Digital Stamp** |

> 🚩 Two migration traps in 1.0.0. **"Digital Signature" was renamed "Digital Stamp"** — a rename
> is exactly the case that silently fails to swap, per the warning above. And the **Date Picker
> label-to-field padding changed from 4px to 8px**, so any value taken from a Figma file older than
> 20 Feb 2025 is wrong.

> ⚠️ `/updates/roadmap` dates 1.0.0 to Feb **2024** and the templates release to Sep **2024** —
> a year earlier than the change log dates the same versions. Cite the change log. Recorded in
> `https://github.com/mohamedsamy911/dga-kit/blob/master/COVERAGE.md`.

Watch `/updates/change-log` and `/updates/roadmap` for releases.

## Contributing back

DGA accepts design, code and documentation contributions via GitHub. Criteria: relevance, broad
impact over niche cases, minor fixes always welcome, major additions (new components) get
thorough evaluation. Community forums and published contribution guidelines are both marked
**"soon"**. Contact: DS-DGA@dga.gov.sa.

**Worth doing:** the 11 documentation defects in `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/CAPTURE-LOG.md` are exactly the kind of
minor contribution DGA says it wants.
