# DGA components on any UI library

All 50 DGA component specs, the name your library probably uses, and — the column that matters —
**the DGA-specific constraint your library will not give you for free.**

Full DGA specs (anatomy, six states, ARIA, do/don't) live in
`../../dga-design-system/references/components.md`. This file is the translation layer only.

**How to read it.** Find the DGA component. If your library has an equivalent, use it and add the
constraint. If the cell says **build**, no mainstream library ships one — see
`../SKILL.md` Step 4. Library names verified against MUI v6, Chakra UI v3, shadcn/ui (Radix
primitives) and Ant Design v5; a library not listed almost certainly has the same component under
a name from one of these four.

Everything below applies on top of the eight rules in `../SKILL.md` — semantic tokens, six
states, 44px targets, no Arabic letter-spacing, logical properties.

---

## Actions

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Buttons | `Button` | `Button` | `Button` | `Button` | 4 types (standard, destructive, menu, icon) x 3 emphasis levels. Map emphasis to variant, type to colour. Icon-only needs an accessible name. |
| Floating Button | `Fab` | `IconButton`+`Float` | build | `FloatButton` | Must not cover content; must contrast with whatever is behind it; two may stack vertically; **3 or more go in an expandable menu**. |
| Link | `Link` | `Link` | `<a>` + class | `Typography.Link` | 🚩 **Underlined by default** — most libraries are not. "Click here" and "go to" are **forbidden** as link text. |
| Chip | `Chip` | `Tag` | `Badge` | `Tag` | Six states including Selected. Dismissable chips need `role="button"` and `aria-label="Dismiss …"`. |
| Dropdown (action) | `Menu` | `Menu` | `DropdownMenu` | `Dropdown` | See Menu under Navigational — DGA publishes **no** accessibility section for it. |

## Content display

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Accordion | `Accordion` | `Accordion` | `Accordion` | `Collapse` | Standard WAI-ARIA disclosure. |
| Card | `Card` | `Card` | `Card` | `Card` | Variants: default / expandable / selectable. ⚠️ DGA publishes **no** card accessibility guidance — its section is Accordion's, pasted in. Fall back to WCAG and say so. |
| Carousel | build (or embla) | `Carousel` | `Carousel` (embla) | `Carousel` | ⚠️ DGA specifies **no pause/stop control** for auto-rotation. WCAG 2.1 AA 2.2.2 requires one. **Apply WCAG** and note the divergence. |
| List | `List` | `List` | `<ul>` | `List` | |
| Code Snippet | build | `CodeBlock` | build | `Typography.Text code` | Force `dir="ltr"` on the block inside an RTL page, or the code renders unreadable. |
| Quote | `<blockquote>` | `Blockquote` | build | `<blockquote>` | ✅ The one DGA component page with a dedicated RTL section — follow it. |
| Divider | `Divider` | **`Separator`** | `Separator` | `Divider` | `role="separator"`. Chakra v3 renamed it; `Divider` does not exist there. |
| **Digital Stamp** | **build** | **build** | **build** | **build** | 🚩 Government-mandated trust component. Needs the entity's DGA registration number + License Number. **Procurement lead time — start early.** |

## Data display

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Avatar | `Avatar` | `Avatar` | `Avatar` | `Avatar` | Sizes 24/32 (S), 40/48 (M), 64/80/120 (L). `alt` carries the person's name. |
| Metric | build | `Stat` | build | `Statistic` | Adds a trend indicator and sparkline. **Trend arrows are directional — they mirror in RTL.** |
| Table | `Table`/`DataGrid` | `Table` | `Table` | `Table` | ⚠️ DGA names **no ARIA roles for Table** while specifying the full set for Structured List. Apply Structured List's roles here too. |
| Content Switcher | `ToggleButtonGroup` | `SegmentGroup` | `ToggleGroup` | `Segmented` | 🚩 Capped at **2-4 options**. Beyond four it must be Tabs — this is a hard DGA limit, not a suggestion. |
| Charts | recharts / MUI X | `@chakra-ui/charts` | recharts | `@ant-design/charts` | 🚩 Hard caps: pie **max 6 segments**; line and bar **max 3 series**. DGA gives no colour-blind-safe palette — pair colour with pattern or direct labels. |
| Structured List | `List`+`ListItemText` | `DataList` | `<dl>` | `Descriptions` | DGA specifies `list`/`listitem` plus the full table role set. |

## Feedback

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Notification | `Alert` / `Snackbar` | `Alert` / toaster | `Alert` / `Sonner` | `Alert` / `notification` | 3 variants x 5 tones **including Neutral** (most libraries lack a neutral tone — add it). 🚩 **No timeout on critical.** Anything auto-dismissing waits 5s or longer. |
| Modal | `Dialog` | `Dialog` | `Dialog` | `Modal` | Focus trap, Esc closes, focus returns to the opener, background `aria-hidden`. |
| Tooltip | `Tooltip` | `Tooltip` | `Tooltip` | `Tooltip` | Shows on **focus** as well as hover; Esc dismisses; **avoid auto-hide**. Left/Right beak positions are physical — map them to logical start/end. |
| Rating | `Rating` | `RatingGroup` | build | `Rate` | DGA adds a **half-star** state. |

## Forms and inputs

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Input | `TextField` | `Input`+`Field` | `Input`+`Label` | `Input` | The prefix/suffix variant is DGA's sanctioned pattern for phone country codes — wrap the prefix in `<bdi>` under RTL or the +966 lands on the wrong side. |
| Textarea | `TextField multiline` | `Textarea` | `Textarea` | `Input.TextArea` | DGA recommends allowing vertical resize. |
| Number Input | `TextField type=number` | `NumberInput` | build | `InputNumber` | `role="spinbutton"`, Up/Down arrows. +/- order mirrors in RTL; **keep the numeral run LTR**. |
| Checkbox | `Checkbox` | `Checkbox` | `Checkbox` | `Checkbox` | DGA includes an **Indeterminate** state. |
| Radio | `RadioGroup` | `RadioGroup` | `RadioGroup` | `Radio.Group` | `fieldset` + `legend`, roving tabindex, arrows move within the group. |
| Switch | `Switch` | `Switch` | `Switch` | `Switch` | `role="switch"` + `aria-checked`. |
| Select / Dropdown | `Select` | `Select` | `Select` | `Select` | Needs an error state and helper text — wrap in the library's field/form-item. |
| Slider | `Slider` | `Slider` | `Slider` | `Slider` | ⚠️ **RTL: the value must increase toward the start edge.** Several libraries get this wrong — test it. |
| File Uploader | `<input type=file>` | `FileUpload` | build | `Upload` | Enter **or Space** opens the dialog from the drop area. |
| Steps | `Stepper` | `Steps` | build | `Steps` | ✅ DGA states RTL explicitly: progresses right-to-left, and the final step's connector moves to the **left**. 🚩 **Radial Stepper on mobile**, Progress Indicator on large screens — a required responsive swap, not a nicety. |
| **Date Picker** | `DatePicker` (X) | `DatePicker` | `Calendar`+`Popover` | `DatePicker` | 🚩 **Gregorian only, everywhere.** No library and no DGA package supplies Hijri. Use `../../dga-react/assets/reference-impl/dga-date.ts` (Umm al-Qura, tested, framework-free) and wrap. **Decide wrap-or-replace before the first date field ships.** |

## Loading and status

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Loading | `CircularProgress` | `Spinner` | `Loader` icon | `Spin` | `role="status"`, **always include text**, must **not** be focusable, 3 flashes/second maximum, honour `prefers-reduced-motion`. |
| Progress Bar | `LinearProgress` | `Progress` | `Progress` | `Progress` | RTL: the fill originates at the start edge. |
| Radial Stepper | `CircularProgress` | `ProgressCircle` | build | `Progress type=circle` | The mobile form of Steps — see Steps. |
| Skeleton | `Skeleton` | `Skeleton` | `Skeleton` | `Skeleton` | `tabindex="-1"`, removed from the accessibility tree once loading completes, honour `prefers-reduced-motion`. |

## Navigational

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Breadcrumbs | `Breadcrumbs` | `Breadcrumb` | `Breadcrumb` | `Breadcrumb` | Truncate past **5** items. 🚩 **Mobile shows back-arrow + previous page only.** Separators mirror in RTL and need `aria-hidden`. |
| Menu | `Menu` | `Menu` | `DropdownMenu` | `Menu` | 🚩 DGA publishes **no accessibility section at all** for Menu. Apply the WAI-ARIA menu pattern and state that DGA is silent. |
| Pagination | `Pagination` | `Pagination` | `Pagination` | `Pagination` | Appears after **10** items. Prev/next arrows mirror in RTL. |
| Tabs | `Tabs` | `Tabs` | `Tabs` | `Tabs` | 🚩 A horizontal tablist **never scrolls and never wraps** — overflow goes to a More button. Most libraries default to scrolling; turn it off. |
| Slide-out Menu | `Drawer` | `Drawer` | `Sheet` | `Drawer` | Focus trap, Esc closes. **Opens from the opposite side in RTL.** |

## Search and filters

| DGA | MUI | Chakra v3 | shadcn/Radix | Ant | DGA constraint to add |
|---|---|---|---|---|---|
| Search Box | `Autocomplete` | `Combobox` | `Command` | `AutoComplete` | 🚩 Requires **autocomplete with real-time suggestions**, a keyboard-accessible clear button, and the query **retained after search**. A bare text input does not satisfy this. |
| Tags | `Chip` | `Tag`/`TagsInput` | `Badge` | `Tag` | Interactive tags must be `<button>`, never `<span>`. |
| Filtration | composite | composite | composite | composite | Build from Popover + Checkbox + RadioGroup + Slider + Tag + DatePicker. ✅ The only DGA page that mentions `prefers-reduced-motion`. |

## UI shell — mostly gaps

No component library ships a compliant government shell. This is the bulk of the build.

| DGA | Any library | DGA constraint |
|---|---|---|
| **Navigation Header** | **build** | DGA-specific anatomy: brand logo, nav links, header actions in 4 layouts, sub-menu items in 4 variants. `role="banner"` + `role="navigation"`. |
| Navigation Drawer | `Drawer`/`Sheet` | Focus moves to the submenu's first item on expand and returns to the parent on collapse. |
| **Table of Contents** | **build** | Required on content-heavy pages. Activation must move **focus**, not just scroll. |
| **Second Nav Header** | **build** | Contextual bar above the primary nav. `aria-live="polite"` on live values. |
| **Footer** | **build** | 🚩 Must contain **Accessibility Tools** (font-size + contrast controls), **first in tab order**. `role="contentinfo"`. |
| Skip link | usually **build** | Required on **every** page, first in the DOM inside the header. A handful of libraries ship one (Chakra's `SkipNavLink`); most do not. |
| **Feedback section** | **build** | 🚩 "Was this page useful?" + Yes/No + reason options, on every page. Feeds the mandated performance-statistics page. |

## Mobile

DGA ships a separate Mobile UI Kit with six components that have **no public spec pages and no
equivalent in any web library**: Mobile Navigation Bar, Tap Bar, Top Bar, Splash Screen, Mobile
Modal, mobile Date Picker. Specs are Figma-only.
See `../../dga-design-system/references/mobile.md`.

## The build list

Ordered by compliance risk, not effort. This is the same list whatever your library is.

1. **Digital Stamp** — blocked on the entity's DGA registration + License Number (procurement)
2. **Footer with Accessibility Tools** — a feature; no automated tool catches its absence
3. **Feedback section** — every page; feeds the mandated statistics page
4. **Navigation Header** + **Second Nav Header**
5. **Skip link**, if your library has none
6. **Table of Contents**
7. **Hijri date wrapper** around the date picker — ⚠️ **not a DGA requirement.** DGA states no
   calendar policy at all, and its own demos are Gregorian (see `../../dga-rtl-i18n/SKILL.md`).
   This sits on a compliance-ordered list, so read it as: *if your project decided on Hijri*,
   nothing ships it for you. Do not report its absence as a DGA finding.
8. **Filtration** composite
9. Mobile shell components, once the Figma kit is in hand
