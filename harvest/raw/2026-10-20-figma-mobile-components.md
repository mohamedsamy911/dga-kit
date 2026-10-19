# Raw capture — DGA's Figma "Mobile Components - Platforms Code", 2026-10-20

**Source.** https://www.figma.com/community/file/1392271796654597578/mobile-components-platforms-code —
published by **DGA** (`https://www.figma.com/@sdga`). Description: "Platforms Code mobile components
library". Licensed **CC BY 4.0**. The page said "Last updated 2 years ago" on 2026-10-20, so it is
older than the design site's Platforms Code 4.0. © Digital Government Authority, CC BY 4.0.

**Export.** With the owner's approval the community file was opened into the owner's Figma drafts
and read with the plugin API, read-only calls only (`loadAllPagesAsync`, `findAllWithCriteria`,
`componentPropertyDefinitions`, `boundVariables`, `getVariableByIdAsync`). For each component set:
its variant properties, the default variant's size, auto-layout padding and gap, corner radius and
the names of the variables bound to it, plus one sample per `Size` option. Pages with no
component sets list their top frames. Committed beside this file:
`2026-10-20-figma-mobile-components.json`, 54,830 bytes, sha256
`9b63f4aafad66a299c233b82053a1bdd9930e8886ca7f5912536e91f51effa92`. All 74 bound variable IDs
resolved to names.

This is structure, not a full spec: it records what the components are made of, not their
behaviour. Sizes are as drawn on a 375px-wide frame.

## The mobile-only components

DGA's `/designing-for-mobile` page lists six: Mobile Navigation Bar · Tap Bar · Top Bar · Splash
Screen · Mobile Modal · Date Picker (captured 2026-08-27). In the Figma file:

| Site name | Figma page → component set | What the file shows |
|---|---|---|
| Mobile Navigation Bar, Top Bar | `UI Shell - Navigation Bar` → **Top Bar** | 375×102. `Style`: Three Actions / Two Actions / Text Actions / Title / Logo. `Usage`: Main Top Bar / Internal Top Bar. Optional info text. White background (`background-white`), bottom border `border-neutral-secondary`. No component is named Mobile Navigation Bar; whether the site's two names are one component is not established. |
| Tap Bar | `UI Shell - Tab Bar` → **Tab Bar**, **Tab Item** | Tab Bar 375×84, `Type` No Selected / Tab 1 … Tab 5 (selection variants), `OnColor` True/False; on-colour fill `background-primary`. Tab Item 46×70: icon over label, padding 12/8 (`spacing-lg`/`spacing-md`), gap 4, optional tag; states Normal / Pressed / Selected. |
| Splash Screen | `UI Shell - Splash Screen` | One frame, `Splashscreen`, 375×812. No component set. |
| Mobile Modal | `Modals` → **Modal** (+ Header, Body, Actions) | 375 wide. Top corners `radius-lg`, bottom corners `radius-none`; the shape suggests presentation from the bottom edge, which the file does not state. Padding `modal-padding` / `modal-content-bottom-padding`, gap `modal-gap`. Actions can stack. |
| Date Picker | `Date Picker` → **Date Picker**, **Date cell**, **_Date field** | 375×696, square corners, `Type` Range / Select date. Date cells 44×44 with a secondary-date slot (`Secondary Date`, `2ndry Date`). |
| — | `UI Shell - Nav Drawer` → **Nav Drawer**, **Nav Drawer Item**, **User section** | Not in the site's list. Drawer 327×840, `Background` Green / White, optional overlay. Items 44 tall, two levels, link / parent / divider, optional external-link mark and tag. |

## Other facts worth knowing

- **Buttons** come in three heights: Large 44, Medium 40, Small 32 (radius `radius-sm`). A
  floating action button, `Fab_Button`, is fully rounded (`radius-full`), 44 tall.
- **Close button** sizes are 20, 24, 32 and 40px square. The 20px and 24px sizes are smaller
  than a 44px touch target.
- **45 of the 57 named component sets have an `RTL` property** (True/False), and those with text
  pair `Text EN` / `Text AR` properties. The 12 without `RTL` are Avatar, Avatar Group,
  Button-Close, Checkbox, Date cell, Toggle, Pagination, Radio, Rating, Spinner, Help Icon and
  Positioned.
- **Banner** (a mobile alert bar) has `Style` Neutral / Critical / Warning / Success / Info and
  binds `notification-*` spacing tokens.

## All component sets

Component sets whose names start with `_` (building blocks) are left out. `RTL` is left out of the
property list.

| Page | Component set | Variants | Variant properties | Default size |
|---|---|---|---|---|
| Accordions | Accordion | 192 | Size: Large/Medium/Small; Icon alignment: Leading/Trailing; State: Default/Pressed/Focused/Disabled; Expanded: False/True; Flush: False/True | 366×56 |
| Accordions | Accordion list | 2 | — | 378×280 |
| Avatar | Avatar | 42 | Type: Image/Initials/Icon; Square: False/True; Size: 24px/32px/40px/48px/64px/80px/120px | 24×24 |
| Avatar | Avatar Group | 2 | Stacked: True/False | 172×32 |
| Tags | Tag | 288 | Size: Medium/Small/x Small; Color: Gray/Brand/Success/Destructive/Warning/On-color/Info; Outline: False/True; Rounded: False/True; Icon only: False/True | 64×32 |
| Tags | Status Badge | 90 | Size: Medium/Small/x Small; Status: Neutral/Green/Blue/Yellow/Red; Style: Inverted/Subtle/Ghost | 98×32 |
| Banner | Banner | 10 | Style: Neutral/Critical/Warning/Success/Info | 343×128 |
| Buttons | Button | 960 | Size: Large/Medium/Small; State: Default/Pressed/Selected/Focused/Disabled; Style: Primary-Neutral/Primary-Brand/Secondary-Solid/Secondary-Outline/Subtle/Transparent; Icon only: False/True; On-color: False/True; Destructive: NO/YES | 110×44 |
| Buttons | Fab_Button | 120 | State: Default/Pressed/Selected/Focused/Disabled; Style: Primary-Neutral/Primary-Brand/Secondary-Solid; Icon only: False/True; On-color: False/True | 102×44 |
| Buttons | Button-menu | 360 | Size: Large/Medium/Small; State: Default/Pressed/Selected/Focused/Disabled; Style: Primary-Neutral/Primary-Brand/Secondary-Solid/Secondary-Outline/Subtle/Transparent; Icon only: False/True | 106×40 |
| Buttons | Button-Close | 24 | Size: Small/Medium/Large/x Small; State: Default/Pressed/Focused; On-color: False/True | 20×20 |
| Checkbox | Checkbox | 90 | Checked: True/False; Indeterminate: False/True; State: Default/Pressed/Focused/Read-only/Disabled; Size: Medium/Small/x Small; Style: Brand/Neutral | 24×24 |
| Checkbox | Checkbox Label | 2 | — | 382×96 |
| Card | Card | 102 | Type: Default/Expanded/Selectable; State: Default/Hover/Focused/Disabled/Default (Expanded)/Hover (Expanded)/Focused (Expanded)/Disabled (Expanded)/Default (Selected)/Hover (Selected)/Focused (Selected)/Disabled (Selected); Effect: With Sahdow/No Shadow/Stroke | 343×232 |
| Content switcher | Content Switcher | 4 | OnColor: False/True | 304×32 |
| Date Picker | Date cell | 26 | Selected: False/True; Today: False/True; Nex/Prev: False/True/End/Start; State: Default/Pressed/Disabled; Null: False/True | 44×44 |
| Date Picker | Date Picker | 4 | Type: Range/Select date | 375×696 |
| Dropdown Input | Dropdown List Item | 18 | State: Default/Pressed/Focused/Disabled; Type: Single Select/Multi Select/Group label | 320×28 |
| Dropdown Input | Dropdown Input | 120 | Filled: False/True; State: Default/Pressed/Focused/Read-only/Disabled; Error: False/True; Style: Default/Filled lighter/Filled darker | 320×72 |
| File upload | File Upload / Multiple | 2 | — | 328×376 |
| File upload | File Upload / Single | 6 | State: Default/Disabled/Uploaded | 326×116 |
| Inline Alert | Inline Alert | 20 | Type: Neutral/Info/Destructive/Warning/Success; Background: White/Color | 343×140 |
| Link | Link | 120 | Size: Medium (16px)/Small (14px); Style: Neutral/Brand/On-color; Inline: False/True; State: Default/Pressed/Focused/Visited/Disabled | 58×24 |
| List | List_item | 10 | State: Default/Pressed/Focus/Disabled/Selected | 327×44 |
| Menu | Menu list item | 48 | Trail element: None/Text/Button/Tag/Switch/Icon; State: Default/Pressed/Focused/Disabled | 225×40 |
| Menu | Menu | 2 | — | 241×596 |
| Menu | Toggle | 4 | State: Off/On; Mode: Dark/Light | 51×31 |
| Modals | Modal | 2 | Mobile: False | 375×430 |
| Modals | Modal Header | 4 | Actions: False/True | 480×52 |
| Modals | Modal Actions | 4 | Stack: False/True | 480×64 |
| Modals | Modal Body | 6 | Center Align: False/True; Content: Text/Placeholder | 480×36 |
| Notification Toast | Notification Toast | 10 | Type: Neutral/Info/Critical/Error/Warning/Success | 343×148 |
| Pagination | Pagination | 3 | Size: Small/Large/Meduim | 216×24 |
| Radio | Radio label | 2 | — | 382×112 |
| Radio | Radio | 20 | Selected: False/True; Style: Neutral/Brand; State: Default/Pressed/Focused/Read-only/Disabled | 32×32 |
| Rating | Rating | 6 | Size: Large/Meduim/Small; Brand: No/Yes | 256×48 |
| Progress indicator | Stepper | 20 | Alignment: Horizontal/Vertical; State: Current/Completed/Upcomming; Focused: no/yes | 158×88 |
| Spinner | Spinner | 84 | Size: tiny/x-small/small/medium/large/x-large/huge; Style: Neutral/On-color/Brand; Indicator: 1/2/3/4 | 20×20 |
| Switch | Switch | 12 | State: Default/Pressed/Disabled; On: False/True | 52×32 |
| Switch | Switch Label | 4 | Trail switch: False/True | 382×104 |
| Tabs | Horizontal Tab | 48 | Size: Small/Medium/Large; Selected: False/True; State: Default/Pressed/Focused/Disabled | 72×52 |
| Tabs | Vertical Tab | 48 | Size: Small/Medium/Large; Selected: False/True; State: Default/Pressed/Focused/Disabled | 72×40 |
| Tabs | Horizontal Tab List | 10 | Size: Medium/Small/Large; Tab Icons: False/True; Flush: False/True | 562×52 |
| Tabs | Vertical Tab List | 12 | Size: Medium/Small/Large; Tab icons: False/True | 150×200 |
| Text input | Text Input | 40 | State: Default/Pressed/Focused/Read-only/Disabled; Filled: False/True; Error: False/True | 320×112 |
| Text input | Label | 16 | Type: Regular (Default)/Semibold; Size: Medium/Large; Disabled: False/True | 46×20 |
| Text input | Input Prefix-Suffix | 56 | Type: Dropdown/Text; State: Default/Pressed/Selected/Focused/Disabled; Style: Solid/Subtle; Size: Large/Medium | 115×40 |
| Textarea | Textarea | 120 | State: Default/Pressed/Focused/Read-only/Disabled; Filled: False/True; Error: False/True; Style: Default/Filled lighter/Filled darker | 320×124 |
| Tooltip | Tooltip | 52 | Inverted: True/False; Beak placement: None/Top/Bottom/Left/Right; Beak Alignment: Start/Center/End | 240×74 |
| Tooltip | Help Icon | 24 | Open: False/True; Placement: Top/Bottom/Left/Right; Alignment: Start/Center/End | 20×20 |
| UI Shell - Nav Drawer | Nav Drawer Item | 74 | On Color: False/True; Type: Link/Parent (Sub-menu)/Divider; Level: Level 2/Level 1; State: Default/Pressed/Focused/Selected/Disabled; Expanded: False/True | 224×44 |
| UI Shell - Nav Drawer | Nav Drawer | 8 | Background: Green/White; Overlay: False/True | 327×840 |
| UI Shell - Nav Drawer | User section | 4 | OnColor: False/True | 362×92 |
| UI Shell - Tab Bar | Tab Item | 12 | State: Normal/Pressed/Selected; Type: Tab Bar Item; OnColor: False/True | 46×70 |
| UI Shell - Tab Bar | Tab Bar | 24 | Type: No Selected/Tab 1/Tab 2/Tab 3/Tab 4/Tab 5; OnColor: True/False | 375×84 |
| UI Shell - Tab Bar | Positioned | 3 | Type: Small/Large/Large with max digits | 12×12 |
| UI Shell - Navigation Bar | Top Bar | 10 | Style: Three Actions/Two Actions/Text Actions/Title/Logo; Usage: Internal Top Bar/Main Top Bar | 375×102 |
| UI Shell - Splash Screen | frame `Splashscreen` | — | — | 375×812 |
| Thumbnail | frame `Thumbnail (Detatch this > Right click > Set as thumbnail)` | — | — | 1600×960 |
