# Raw capture — DGA's Figma "Components Library - Platforms Code", 2026-10-20

**Source.** https://www.figma.com/community/file/1392264328585493958/components-library-platforms-code —
published by **DGA** (`https://www.figma.com/@sdga`). Description: "Introducing (Platforms Code) the
National Design System of Saudi Arabia". Licensed **CC BY 4.0**. Its update notes run to 3 Nov 2025
(Digital Stamp text). © Digital Government Authority, CC BY 4.0.

**Export.** Opened into the owner's Figma drafts with the owner's approval and read with the plugin
API, read-only, the same way as `2026-10-20-figma-mobile-components.md`: per component set, the
variant properties, the default variant's size, auto-layout padding and gap, corner radius and
bound variable names, and one sample per `Size` option. Committed beside this file:
`2026-10-20-figma-components-library.json`, 130,022 bytes, sha256
`3ee9580243699700cfe39c7f372f09ddaade5fc06978df13a05b6d18519fdd2c`. 141 component sets on 59
pages; 105 named sets after dropping `_` building blocks.

Sizes are as drawn in the library, in Figma px. A drawn size is the visible element, not
necessarily its hit area.

## Findings

1. **Buttons are drawn 40 / 32 / 24px tall** (Large / Medium / Small), padding 16 / 12 / 8px,
   radius 4. The mobile kit draws them 44 / 40 / 32px. DGA's Buttons page gives 44×44px as
   *"a recommended minimum"* touch target; only the mobile Large size meets it as drawn.
2. **Other small interactive parts:** Checkbox 24 / 20 / 16px; Close button 20 / 24 / 32 / 40px;
   Help icon 20px; table sort and filter icons 20px.
3. **Skeleton** circle and square sizes are 24, 48, 64, 80, 120, 170 and 240px. That matches the
   English page (*"between 24px to 240px"*), not the Arabic one («بين 24px إلى 48px»).
4. **Floating Button** 56 or 64px, fully rounded. **Avatar** 24 to 120px. **Date cell** 56px on
   web, 44px in the mobile kit.

## All named component sets

| Page | Component set | Variants | Default size | Sizes (w×h) |
|---|---|---|---|---|
| Accordions | Accordion | 240 | 366×56 | Large 366×56, Medium 366×48, Small 366×40 |
| Accordions | Accordion list | 2 | 378×280 | — |
| Avatar | Avatar | 42 | 24×24 | 32px 32×32, 40px 40×40, 48px 48×48, 64px 64×64, 80px 80×80, 120px 120×120, 24px 24×24 |
| Avatar | Avatar Group | 2 | 172×32 | — |
| Breadcrumb | Breadcrumb | 10 | 80×20 | — |
| Buttons | Button | 1344 | 110×40 | Large 110×40, Medium 92×32, Small 74×24 |
| Buttons | Button-menu | 432 | 106×40 | Large 106×40, Medium 88×32, Small 70×24 |
| Buttons | Button-Close | 32 | 20×20 | x Small 20×20, Small 24×24, Medium 32×32, Large 40×40 |
| Card | Card | 102 | 360×228 | — |
| Charts | Pie Chart | 48 | 500×284 | — |
| Charts | Line Chart | 2 | 512×277 | — |
| Charts | Bar Chart | 2 | 515×239 | — |
| Checkbox | Checkbox | 108 | 24×24 | Medium 24×24, Small 20×20, x Small 16×16 |
| Checkbox | Checkbox Label | 2 | 382×100 | — |
| Carousel | Carousel | 3 | 1296×210 | — |
| Carousel | Carousel Controls | 6 | 16×16 | Large 16×16, Mideum 12×12, Small 8×8 |
| Carousel | Carousel Arrows | 60 | 48×48 | Medium 40×40, Large 48×48, Small 32×32 |
| Content Switcher | Content Switcher | 12 | 304×32 | Small 304×32, Medium 304×40, Large 304×48 |
| Chip | Chip | 288 | 60×32 | Small 47×20, Medium 51×24, Large 60×32 |
| Code Snippet | Code Snippet | 2 | 743×587 | — |
| Date Picker | Date cell | 41 | 56×56 | — |
| Date Picker | Date Picker | 6 | 424×456 | — |
| Digital Stamp | Digital Stamp | 8 | 1728×32 | — |
| Digital Stamp | Extension | 24 | 1664×88 | — |
| Dropdown Input | Dropdown List Item | 22 | 320×28 | — |
| Dropdown Input | Dropdown Input | 288 | 320×68 | Large 320×388, Medium 320×380 |
| Divider | Divider | 8 | 192×1 | — |
| File upload | File Upload / Multiple | 2 | 334×272 | — |
| File upload | File Upload / Single | 6 | 326×116 | — |
| Floating Button | Floating Button | 288 | 56×56 | Small 56×56, Large 64×64 |
| Filtration | Filtration | 20 | 123×40 | — |
| Inline Alert | Inline Alert | 40 | 1024×132 | — |
| Link | Link | 144 | 30×24 | Small 26×20, Medium 30×24 |
| List | List | 18 | 110×96 | — |
| List | List item | 36 | 86×24 | — |
| Loading | Loading | 84 | 20×20 | xx Small 20×20, x Small 24×24, Small 28×28, Medium 32×32, Large 36×36, x Large 40×40, xx Large 44×44 |
| Modals | Modal | 4 | 600×208 | — |
| Menu | Menu list item | 72 | 225×40 | — |
| Menu | Menu | 2 | 241×632 | — |
| Metric | Metric | 4 | 360×293 | — |
| Notification | Notification | 10 | 1280×56 | — |
| Notification Toast | Notification Toast | 20 | 484×148 | — |
| Number Input | Input Prefix-Suffix | 48 | 56×40 | Large 56×40, Medium 44×32 |
| Number Input | Number Input | 288 | 183×68 | Large 183×68, Medium 183×60 |
| Pagination | Pagination | 6 | 226×24 | Large 291×40, Small 226×24, Meduim 272×32 |
| Progress Bar | Circular Progress Bar | 40 | 200×200 | 64px 64×64, 80px 80×80, 120px 120×120, 160px 160×160, 200px 200×200 |
| Progress Bar | Progress Bar | 48 | 320×50 | Small 320×50, Medium 320×56, Large 320×68 |
| Progress indicator | Progress Indicator | 40 | 158×88 | — |
| Quote | Quote | 8 | 640×270 | Large 846×270, Small 640×270 |
| Radio | Radio | 24 | 32×32 | — |
| Radio | Radio Label | 2 | 382×108 | — |
| Rating | Rating | 6 | 256×48 | Large 256×48, Meduim 176×32, Small 136×24 |
| Radial Stepper | Radial Stepper | 30 | 165×54 | 64px 210×64, 48px 194×64, 40px 165×54, 80px 246×80, 120px 286×120 |
| Radial Stepper | Circular Stepper | 120 | 40×40 | 40px 40×40, 48px 48×48, 64px 64×64, 80px 80×80, 120px 120×120 |
| Skeleton | Skeleton Component | 5 | 280×354 | — |
| Skeleton | Skeleton Square | 7 | 240×240 | 240px 240×240, 170px 170×170, 120px 120×120, 80px 80×80, 64px 64×64, 48px 48×48, 24px 24×24 |
| Skeleton | Skeleton Rectangle | 6 | 320×40 | Large 320×40, Medium 75×32, Small 59×24 |
| Skeleton | Skeleton Circle | 7 | 240×240 | 240px 240×240, 170px 170×170, 120px 120×120, 80px 80×80, 64px 64×64, 48px 48×48, 24px 24×24 |
| Skeleton | Skeleton Line | 2 | 277×22 | Large 277×22, Small 277×14 |
| Switch | Switch | 20 | 48×24 | — |
| Switch | Switch Label | 4 | 382×96 | — |
| Structured List | Structured List Header Cell | 2 | 228×48 | — |
| Structured List | Structured List Row Cell | 36 | 228×64 | — |
| Structured List | Structured List Header | 2 | 684×48 | — |
| Structured List | Structured List Row | 4 | 684×64 | — |
| Structured List | Structured List | 64 | 684×304 | — |
| Slider | Slider | 24 | 334×64 | Small 341×64, Medium 341×70 |
| Search Box | Search Box | 144 | 320×104 | Medium 320×104, Large 320×112 |
| Search Box | Trailing Icon | 2 | 20×20 | — |
| Slideout Menu | Slideout Menu | 8 | 346×912 | — |
| Slideout Menu | Slideout Menu Header | 2 | 260×78 | — |
| Table | Table Row Cell | 44 | 228×64 | — |
| Table | Table Header Cell | 12 | 228×48 | — |
| Table | Table Header Cell - Sort | 15 | 20×20 | — |
| Table | Table Header Cell - Filter | 10 | 20×20 | — |
| Table | Table Row | 4 | 1000×64 | — |
| Table | Table | 16 | 1330×1008 | — |
| Table | Table Header | 2 | 1000×48 | — |
| Tabs | Vertical Tab | 60 | 72×40 | Medium 72×32, Large 72×40, Small 60×24 |
| Tabs | Vertical Tab List | 12 | 150×200 | Medium 150×160, Large 150×200, Small 150×120 |
| Tabs | Horizontal Tab | 64 | 81×52 | Medium 81×44, Large 81×52, Small 73×36 |
| Tabs | Horizontal Tab List | 10 | 650×52 | Medium 634×44, Large 650×52, Small 634×44 |
| Tags | Tag | 288 | 86×32 | x Small 56×20, Small 64×24, Medium 86×32 |
| Tags | Status Tag | 90 | 98×32 | Medium 98×32, Small 76×24, x Small 64×20 |
| Text input | Text Input | 288 | 320×68 | Large 320×68, Medium 320×60 |
| Text input | Label | 16 | 46×20 | Medium 46×20, Large 51×24 |
| Textarea | Textarea | 144 | 320×124 | — |
| Tooltip | Tooltip | 52 | 240×78 | — |
| Tooltip | Help Icon | 48 | 20×20 | — |
| UI Shell - Nav Header | Header Sub-menu Item | 16 | 320×64 | — |
| UI Shell - Nav Header | Header Menu Item | 20 | 116×72 | — |
| UI Shell - Nav Header | Header Action | 60 | 108×72 | — |
| UI Shell - Nav Header | Item Icon | 4 | 48×48 | — |
| UI Shell - Nav Header | Nav Header | 8 | 1728×72 | — |
| UI Shell - Nav Header | Header Menu | 8 | 40×72 | — |
| UI Shell - Nav Header | Nav Header Sub-Menu | 24 | 1440×276 | — |
| UI Shell - Nav Header | Logo Placeholder | 12 | 183×74 | Large 157×74, Small 106×42, Medium 132×58 |
| UI Shell - Nav Drawer | Nav Drawer Item | 90 | 224×36 | — |
| UI Shell - Nav Drawer | Nav Drawer | 12 | 256×903 | — |
| UI Shell - Nav Drawer | Nav Drawer Header | 4 | 256×72 | — |
| UI Shell - Second Level Nav Header | Second Nav Header | 4 | 1440×40 | — |
| UI Shell - Second Level Nav Header | sub-header-Item | 4 | 78×24 | — |
| UI Shell - Table of Content | TOC Item | 48 | 200×32 | — |
| UI Shell - Table of Content | TOC | 2 | 222×706 | — |
| UI Shell - Footer | Footer | 8 | 1327×484 | — |
