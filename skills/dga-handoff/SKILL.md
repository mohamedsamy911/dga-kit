---
name: dga-handoff
description: Turn an approved design into a DGA developer handoff specification for a Saudi government platform — component inventory, token map, state matrix, accessibility annotations and bilingual copy table. Use when a design is signed off and ready to build.
---

# DGA design → development handoff

The seam where compliance is lost: the designer knew the rule, the developer never heard it.
This skill makes the handover a structured artefact instead of a Figma link and a conversation.

**Prerequisite:** the design has passed `dga-design-review` with zero blockers. If it hasn't,
run that first — handing off a non-compliant design just moves the problem downstream.

## Produce these seven sections

### 1 · Component inventory
Every element mapped **three ways**: the DGA guideline name → the `platformscode-new-react`
component (`dga-*`) → the repo's wrapper, if any. Flag anything with no DGA equivalent as a
custom component needing justification.

### 2 · Token map
Every colour, space, radius, type style and shadow as its **semantic** token name, never a hex.
Where the design used something off-token, name the substitution made and why.
Flag **responsive tokens** — DGA's radius and spacing resolve differently per breakpoint.

### 3 · State matrix
A row per interactive element, a column per DGA state — **Default · Hovered · Pressed ·
Selected · Focused · Disabled** — plus loading, empty and error where applicable. Blank cells
are open questions, not omissions; list them in §7.

### 4 · Accessibility annotations
Per component, the ARIA and keyboard contract from
`../dga-design-system/references/accessibility.md`: roles, required attributes, keyboard model,
focus behaviour. Include the two DGA requirements teams miss — **skip-to-content** and
**Accessibility Tools first in tab order**.

### 5 · Bilingual copy table
`ar` and `en` side by side for every string, including button labels, helper text, error
messages, empty states and the required strings from
`../dga-design-system/references/content.md`. Mark any string still awaiting Arabic.

### 6 · RTL notes
What mirrors and what doesn't on this screen specifically — see `../dga-rtl-i18n`. Call out
embedded LTR runs (phone numbers, IDs, reference numbers, code) needing `<bdi>`.

### 7 · Open questions
Everything undecided, with who must decide it. An honest list here is worth more than a
complete-looking spec that guesses.

## Definition of done

A developer can build the screen from the spec alone without asking a clarifying question about
a DGA rule.
