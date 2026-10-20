# Raw capture — component states: page, Assessment Checklist and Figma, 2026-10-20

The kit's state guidance used only the component pages. DGA's Assessment Checklist also names
states for 18 components, and in five it differs from the page. This file records all three
sources side by side.

**Sources.**

1. **Assessment Checklist** — the English sub-rows of items 12–36 in
   `harvest/raw/2026-10-19-assessment-checklist.md` (workbook read 2026-10-19). The workbook
   splits *interactive* states («حالات العنصر التفاعلية») from *contextual* ones («حالات العنصر
   السياقية»). Some rows give only one list.
2. **Component pages** — the kit's record in `components.md` (English pages, retrieved
   2026-08-26). On 2026-10-20 the rendered Arabic pages of Buttons, Radio, Switch, Input, Tabs,
   Checkbox, Breadcrumbs, Dropdown and Date picker were re-read in a browser, «السلوكيات
   (الحالات)» section. Each matched the record: Buttons six; Radio six with «محدد» (Selected);
   Switch, Input and Tabs five with «المضغوط/الضغط» (Pressed) and no Selected; Checkbox, Dropdown
   and Date picker no state section; Breadcrumbs «سبع حالات» naming six (a known AR defect). The
   live build was unchanged (`index-BO_6JOKP.js`, sha256 `4b8aa21d…0340`).
3. **DGA's Figma Components Library** — the `State` and related variant properties in
   `harvest/raw/2026-10-20-figma-components-library.json`. Implementation, not guidance.

## Comparison

| Component (item) | Checklist: interactive | Checklist: contextual | Page | Figma |
|---|---|---|---|---|
| Buttons (12) | Default, Hovered, Pressed, Selected, Focused, Disabled | — | same six | same six |
| Dropdown (13) | Default, Hovered, Pressed, Focused, Read-only, Disabled | — | no state list | same six |
| Link (14) | Default, Hovered, Pressed, Focused, Visited, Disabled | — | same six | same six |
| Accordion (15) | Default, Hovered, Pressed, Focused, Disabled | Expanded / Collapsed | same five | same five; `Expanded` |
| Menu (16) | Default, Hovered, Pressed, Focused, Disabled | Selected | same five | same five plus `Selected` in `State` |
| Content switcher (17) | Normal, Hovered, Focused | Selected | normal, hovered, selected, focused | no state property |
| File uploader (20) | Default, Drag + Hover, Disabled | Uploaded / Not Uploaded | Default, Drag + Hovered, Disabled | Single: Default, Disabled, Uploaded; Multiple: none |
| Checkbox (21) | Default, Hovered, Focused, Read-only, Disabled | Checked / Unchecked / Indeterminate | no state list (Unchecked, Checked, Indeterminate as types) | Default, Hovered, Pressed, Focused, Read-only, Disabled; `Checked`, `Indeterminate` |
| Radio (22) | Default, Hovered, Focused, Read-only, Disabled | Selected / Unselected | Default, Hovered, Pressed, Selected, Focused, Disabled | Default, Hovered, Pressed, Focused, Read-only, Disabled; `Selected` |
| Switch (23) | Default, Hovered, Focused, Disabled | On / Off | Default, Hovered, Pressed, Focused, Disabled | same five as the page; `On` |
| Textarea (24) | Default, Hovered, Pressed, Focused, Read-only, Disabled | — | same six | same six |
| Tabs (25) | Default, Hovered, Focused, Disabled | Selected / Unselected | Default, Hovered, Pressed, Focused, Disabled | Horizontal Tab: the page's five plus Closed, Open; `Selected` |
| Card (28) | Default, Hover, Focused, Disabled | — | Default, Hovered, Focused, Disabled | Default, Hover, Focused, Disabled |
| Nav header (29) | Default, Hovered, Pressed, Focused, Disabled | Selected | Header menu item: the same five, plus Selected / Unselected | Header Menu Item: the same five; `Selected` |
| Breadcrumbs (30) | Default, Hovered, Pressed, Focused, Disabled | — | "seven": enabled, hover, active, focus, visited, disabled, read-only | no state property |
| Rating (32) | Normal, Pressed | Selected, Half | normal, pressed, selected, half | no state property |
| Input (34) | Default, Hovered, Pressed, Focused, Read-only, Disabled | — | Default, Hovered, Pressed, Focused, Disabled; Read-only listed as a type | Text Input: same six as the checklist |
| Date picker (36) | Default, Hovered, Pressed, Focused, Disabled | Selected, Today, Next/Prev | no state list | Date cell: the same five; `Selected`, `Today`, `Nex/Prev` |

Item 29's row reads *"Apply tab and submenu states (…)"*. Item 30 adds *"Note: Current page
should be disabled and non-interactive."* (the workbook prefixes it with an asterisk). Names are as each source spells them: *Hover* (item 28)
and *Drag + Hover* (item 20) are the checklist's words, *Drag + Hovered* the page's.

## Where the page and the checklist differ

1. **Radio** — the page lists Pressed and Selected as states and no Read-only; the checklist has
   no Pressed, adds Read-only, and makes Selected / Unselected contextual.
2. **Switch** — the page lists Pressed; the checklist does not.
3. **Tabs** — the page lists Pressed and no Selected; the checklist has no Pressed and adds
   Selected / Unselected.
4. **Input** — the page lists five states and Read-only as a type; the checklist lists Read-only
   as a state.
5. **Breadcrumbs** — the page names visited and read-only; the checklist does not, and adds the
   current-page note.

Checkbox, Dropdown and Date picker pages give no state list, so the checklist is the only DGA
list for them.

## Figma

DGA's Figma draws the checklist's states for most rows. It has no `Drag + Hover` variant for File
Upload, and the Content Switcher, Breadcrumb and Rating sets carry no state property.

## A trap the checklist exposes

HTML's `readonly` attribute does not apply to checkboxes or radio buttons (HTML Living Standard,
the `readonly` attribute: it applies to text-like `input` types and `textarea`). A read-only
checkbox or radio built with `readonly` still toggles. ARIA 1.2 allows `aria-readonly` on the
`checkbox` and `radiogroup` roles — on the group, not on each `radio`; the change itself has to
be blocked in code.
