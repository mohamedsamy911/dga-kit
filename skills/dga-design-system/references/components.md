# Components

**Source:** https://design.dga.gov.sa/guidelines/components/* · **Retrieved:** 2026-08-26
**Status:** ✅ **COMPLETE — 50 of 50 component pages extracted.**
The nav lists 47, not the 45 DGA advertises. Three more exist but are absent from the nav
entirely: `ui-shell/footer`, `forms-and-inputs/textarea`, `forms-and-inputs/number-input`.

Implementation is **not** hand-built — DGA ships an official library. See
`../../dga-react/references/official-packages.md` before writing any component code.

## Page template

Every component page follows the same structure. When extracting one, expect all of:

`Live Demo (Visual | Code)` → `Appearance` → `Types` → `Styles` → `Behaviors (States)` →
`Anatomy` → `Tips (Do / Avoid pairs)` → `Accessibility`

The **Accessibility** section is the highest-value part for `dga-design-review` and `dga-a11y`
— it names the exact ARIA roles and keyboard behaviour DGA requires, per component. The
**Do/Avoid** pairs map directly onto review findings.

Note: every page links a Storybook "complete demo", but Storybook is marked **"soon"** on
/developing and is not yet live.

## Standard state set

DGA defines six interaction states. A design that specifies fewer is incomplete, not compliant:

`Default` · `Hovered` · `Pressed` · `Selected` · `Focused` · `Disabled`

`Focused` is called out explicitly as an accessibility requirement for keyboard navigation.

## Inventory — 45 components in 9 categories

| Category | Components |
|---|---|
| **Actions** (5) | buttons · floating-Button · dropdown · link · chip |
| **Content display** (8) | accordion · card · carousel · list · code-snippet · quote · divider · digital-stamp |
| **Data display** (6) | avatar · metric · table · content-switcher · charts · structured-list |
| **Feedback** (4) | notification · modal · tooltip · rating |
| **Forms & inputs** (8) | checkbox · datepicker · input · file-uploader · radio · slider · steps · switch |
| **Loading & status** (4) | loading · progress-bar · radial-stepper · skeleton |
| **Navigational** (5) | breadcrumbs · menu · pagination · tabs · slide-out |
| **Search & filters** (3) | search-box · tags · filtration |
| **UI shell** (4) | navigation-header · navigation-drawer · table-of-content · second-nav-header |

URL pattern: `/guidelines/components/{category}/{name}`
(`digital-stamp` and `floating-Button` — note DGA's capital B — are DGA-specific and have no
obvious equivalent in other design systems.)

---

## Buttons

`/guidelines/components/actions/buttons` · retrieved 2026-08-26

**Types** — Standard (routine primary actions) · Destructive (irreversible: deletion,
cancelling important processes; DGA requires user confirmation) · Menu (toggles a menu of
options) · Icon (any type rendered icon-only).

⚠️ DGA's own text is inconsistent: the Appearance paragraph lists *five* types including a
close button, then the Types list gives four and drops it. Treat close as a variant of icon
button.

**Emphasis** — three levels: high (critical CTAs and primary actions), medium, low (secondary
or less critical). The page says "four styles" then describes three levels. Another internal
inconsistency.

**Icons** — leading (precedes label, draws attention first, for emphasising a specific action)
or trailing (follows label, complements it when the text carries the meaning). DGA explicitly
ties the choice to "interface directionality" — which in RTL means the leading icon sits on
the right.

**Anatomy** — Container (clickable area) · Button label · Leading or trailing icon.

**Do / Avoid**

| Do | Avoid |
|---|---|
| Group related actions into cohesive clusters | Scattering related actions across the interface |
| Place primary actions prominently — bottom of forms, central positions | Hiding critical buttons inside menus |
| Keep placement consistent across screens | Changing placement haphazardly between screens |
| Use whitespace around buttons | Crowding buttons without visual separation |
| Follow the documented anatomy | Deviating from it |

**Accessibility — DGA requirements**

- Always use the `<button>` element. Non-semantic `<div>` must not be used for actions.
- An `<a>` used as a button must actually navigate and must have a valid `href`.
- Contrast of label text or icon against the button background: **at least 4.5:1**.
- Minimum touch target **44×44px**.
- `aria-label` required on any button whose visible content doesn't describe its function —
  icon buttons especially: `<button aria-label="Close"><img src="icon.svg" alt=""></button>`
- Buttons must be focusable; `<button>` is by default.
- Visible feedback for hover, focus and active states.

⚠️ The button page's accessibility section also carries four paragraphs about **notification**
roles (`role="alert"`, `role="status"`, `aria-live`, `stopAnnouncements`) that appear to be
copy-paste from the notification page. They do not apply to buttons. Ignore them here and take
them from `/guidelines/components/feedback/notification` instead.

---

## Date Picker

`/guidelines/components/forms-and-inputs/datepicker` · retrieved 2026-08-26

**Views** — Single-Month (compact, focused) and Dual-Month (two months side by side, broader
range and more visual context).

**Anatomy** — Month & Year · Date Input (keyboard entry) · Container · Today (circular
indicator) · Selected Date (circular indicator) · Actions (ghost/tertiary buttons) ·
Navigation Buttons.

### 🚩 Gregorian only — no Hijri anywhere

The live demo on DGA's own page renders **"August 2026 · Su Mo Tu We Th Fr Sa"** — Gregorian
months, English day abbreviations, Sunday-start week. The guideline text never mentions Hijri,
Umm al-Qura, or dual-calendar display, and the official npm package contains no Hijri code
(verified by exhaustive search — see `official-packages.md`).

For an Arabic-first Saudi government service this is a gap DGA has not filled. **The
project must supply Hijri support itself.** Decide early whether to wrap `dga-datepicker` or
replace it — it affects every date field in the product. Raise with DS-DGA@dga.gov.sa first,
in case it's on their roadmap.

**Accessibility — DGA requirements**

- `role="dialog"` on the popup; `role="application"` on the date grid inside it
- `grid`, `gridcell`, `row`, `columnheader` roles to structure the grid
- `aria-labelledby` / `aria-describedby` for accessible name and description
- Every interactive element inside labelled with `aria-label` or `aria-labelledby`
- On open, move focus to the selected date — or today if nothing is selected
- Arrow keys navigate dates; Enter selects; Esc closes
- Keyboard-accessible fast navigation between months and years
- `aria-live` announces the focused day and month/year changes
- `aria-selected` kept current on the selected date

⚠️ The intro to the accessibility section says "creating accessible **radio button**
components" — another copy-paste artefact. The requirements listed are genuinely date-picker
ones.

---

## Input

`/guidelines/components/forms-and-inputs/input` · retrieved 2026-08-26

**Types** — Standard · With icon · With prefix/suffix (DGA's own examples: country code before
a phone number, currency symbol after an amount) · Read-only.

**Filled styles** — Default (background + stroke) · Lighter (no stroke, light background) ·
Darker (no stroke, darker background).

**Helper text** — standard (guidance) and error (red, for failed validation).

**States** — Default · Hovered · Pressed · Focused · Disabled. *(No Selected — inputs use five
of the six.)*

**Anatomy** — Container · Input label · Placeholder · Icon · Feedback icon (entry validity) ·
Helper text · Prefix · Suffix.

**Accessibility — DGA requirements**
- Correct HTML element and `type` (`email`, `tel`, `number`…) to get the right mobile keyboard
  and built-in validation
- `<label for>` matched to the input's `id`; where a visible label is undesirable, `aria-label`
  or `aria-labelledby`
- `aria-describedby` linking helper text and error messages
- `aria-invalid="true"` on errored inputs, plus `aria-describedby` to a descriptive message
- Full keyboard access, Tab / Shift+Tab
- Visible focus indicators — borders or shadows
- Adequate touch targets on mobile

> **Note:** the prefix/suffix variant is the DGA-sanctioned pattern for phone country codes.
> Under RTL that prefix is an LTR run — wrap it in `<bdi>`. See `../../dga-rtl-i18n`.

---

## Checkbox

`/guidelines/components/forms-and-inputs/checkbox` · retrieved 2026-08-26

**Variants** — Unchecked · Checked · **Indeterminate** (partial selection within a group).

**Anatomy** — Checkbox input · Label · Helper text · Alert message.

**Accessibility — DGA requirements**
- Native `<input type="checkbox">`
- `<label>` association, either wrapping the input or via `for`/`id`
- ARIA generally unnecessary; use `aria-labelledby`/`aria-label` in complex layouts
- Focusable with Tab, toggled with **Spacebar**
- State changes announce automatically when properly labelled

---

## Radio

`/guidelines/components/forms-and-inputs/radio` · retrieved 2026-08-26

**Variants** — Unselected · Selected. **States** — all six.
**Anatomy** — Radio input (nothing preselected by default) · Label · Helper text · Alert message.

**Accessibility — DGA requirements**
- `<input type="radio">`, grouped by a shared `name`
- `<fieldset>` + `<legend>` to group and label the set
- **Only one radio in the group is in the tab sequence**; arrow keys move within the group
- Left/right *and* up/down arrows cycle the options

> ⚠️ Roving tabindex is required here, and it is the single most commonly missed radio-group
> behaviour. Under RTL, left/right arrow direction is mirrored by the browser for native inputs —
> verify rather than assuming.

---

## Switch

`/guidelines/components/forms-and-inputs/switch` · retrieved 2026-08-26

**Variants** — On · Off, plus helper text and alert message.
**States** — Default · Hovered · Pressed · Focused · Disabled.
**Anatomy** — Switch (off by default) · Label · Helper text · Alert message.

**Accessibility — DGA requirements**
- Implement on `<input type="checkbox">`
- `role="switch"` plus `aria-checked="true|false"`
- `<label>` or `aria-label`; `aria-labelledby` where state text is dynamic
- Spacebar toggles; focusable with Tab
- Visual state and label text must update immediately on change

---

## File uploader

`/guidelines/components/forms-and-inputs/file-uploader` · retrieved 2026-08-26

**Variants** — Single file · Multi file.
**States** — Default · **Drag + Hovered** · Disabled.
**Anatomy** — Drag-and-drop area · Title · Helper text (including accepted file types) ·
Browse files button · Featured icon · Upload status icon · File name · File bar helper text ·
Delete file · Label · Button.

**Accessibility — DGA requirements**
- Built on native `<input type="file">`; both the button and the drop area take keyboard focus
- Tab / Shift+Tab to reach it; **Enter or Space** opens the file dialog
- DGA's own example label: `aria-label="File upload area, press Enter or Space to upload files"`

---

## Slider

`/guidelines/components/forms-and-inputs/slider` · retrieved 2026-08-26

**Variants** — Single-value · Range (two thumbs).
**Anatomy** — Label · Helper text · Track · Thumb · Range selection · Value label · Min/max labels.

**Accessibility — DGA requirements**
- `role="slider"` on the thumb
- `aria-valuemin`, `aria-valuemax`, `aria-valuenow` — and for range sliders, on **each** thumb
- `aria-label="Adjust [function]"`
- Keyboard: Tab, arrows, **Home, End, Page Up, Page Down**
- Each thumb of a range slider needs its own focus state, distinguishable by assistive tech
- Adequate touch hit area; track, thumb and labels must meet contrast requirements

> ⚠️ **RTL:** a slider's value must increase toward the *start* edge — the right, in Arabic.
> DGA does not state this; it is standard bidi behaviour. See `../../dga-rtl-i18n`.

---

## Steps

`/guidelines/components/forms-and-inputs/steps` · retrieved 2026-08-26

**Alignment** — Horizontal (DGA: *"progresses from left to right or right to left for RTL
languages"*) · Vertical.
**Step states** — Completed · Current · Upcoming.
**Interaction states** — Default · Hovered · Focused.
**Anatomy** — Stepper base · Step name · Step description · Next-step line · First / Middle /
Final step. DGA: the final step *"has no line on the right side (or the left side if it is RTL)."*

**Accessibility — DGA requirements**
- Mark up as an ordered list: `<ol aria-label="Progress">` with `<li>` per step
- `aria-current="step"` on the active step
- Non-navigational steps must **not** be focusable and must not use `<button>`/`<a>`
- Navigational steps use `<button>`, focusable, activated with Enter or Space
- Completed / current / upcoming distinguished by more than colour — icons or text too
- Visually-hidden text conveying each step's status for screen readers

> ✅ **One of only two places DGA explicitly addresses RTL.** Cite it when arguing for
> RTL-correct mirroring elsewhere.

---

## Notification

`/guidelines/components/feedback/notification` · retrieved 2026-08-26

**Variants** — Inline (in task flow, top of main content) · Toast (transient, non-modal, top of
screen) · Notification (prominent, top of page).

**Tones** — each variant comes in Info · Success · Warning · Critical/Error · **Neutral**.
Inline additionally comes with and without background colour.

**Anatomy** — Container · Title · Helper text · Actions (actionable only — ghost/tertiary
buttons) · Featured icon / Feedback icon · Link · Close button (optional).

**Accessibility — DGA requirements**
- `role="alert"` for important alerts needing immediate attention (implies `aria-live="assertive"`)
- `aria-live="polite"` for less urgent notifications
- Give users enough time to read; **no timeout at all** for persistent or critical information
- Auto-dismissing notifications stay **at least 5 seconds**
- A clear dismiss mechanism, keyboard accessible
- Modal alerts: move focus in, trap it, and return focus on dismiss

**Do / Avoid** — clear concise language, not vague; timely alerts, not a bombardment.

---

## Modal

`/guidelines/components/feedback/modal` · retrieved 2026-08-26

**Anatomy** — Container · Title · Body message · Actions · Featured icon · Close button (optional).

**Accessibility — DGA requirements**
- `role="dialog"` + `aria-modal="true"`
- `aria-labelledby` pointing at the modal title
- On open, focus moves to the first interactive element (or the container)
- **Focus trapped** inside while open — tabbing must not escape
- Clearly labelled close button, **and Esc closes**
- Background content `aria-hidden="true"` and untabbable
- On close, **focus returns to the element that opened it**
- Sufficient text contrast; usable at all device sizes and orientations

---

## Breadcrumbs

`/guidelines/components/navigational/breadcrumbs` · retrieved 2026-08-26

**States** — seven: enabled, hover, active, focus, **visited**, disabled, read-only.
*(The only component with a visited state — it contains links.)*

**Truncation** — up to **five** items by default; beyond that, first and last with an ellipsis
that expands on click. Wraps to a second line when it exceeds the width.

**Responsive behaviour**

| Breakpoint | Behaviour |
|---|---|
| L–5XL | Full trail until it exceeds space, then truncate |
| Medium | Truncated version by default |
| Small / XS (mobile) | **Only a back arrow and a link to the previous page** |

**Anatomy** — Root ("Home" or the site name) · Separator · Middle · Middle-overflow ·
Current page.

**Accessibility — DGA requirements**
- `<nav aria-label="Breadcrumb">` wrapping a `<ul>` of links
- `aria-current="page"` on the current page item
- All links focusable with discernible text, Tab-navigable
- Visible focus, hover and active feedback
- Custom separator icons need `aria-hidden="true"`

> ⚠️ **RTL:** the separator is a directional glyph and must mirror. So must the mobile back
> arrow. DGA doesn't say so — `../../dga-rtl-i18n/references/rtl-rules.md` does.

---

## Navigation header

`/guidelines/components/ui-shell/navigation-header` · retrieved 2026-08-26

Three sub-components, each with the full six-state set:

**Header menu item** — Selected / Unselected, plus Default, Hovered, Pressed, Focused, Disabled.
**Header action** — layout variants: Inline (icon + text on one line) · Top (icon above text) ·
Text only · Icon only.
**Header sub-menu item** — Simple list · With icon · With helper text · With tag.

**Anatomy** — Brand logo · Navigation links · Action.

**Accessibility — DGA requirements**
- `role="banner"` on the main header; `role="navigation"` on the nav region
- All interactive elements keyboard reachable; Enter or Space activates
- Clear visible `:focus` indicators
- **A "Skip to Content" link at the start of the header** so keyboard and screen-reader users
  can bypass the nav
- WCAG contrast ratios for text on background
- Descriptive labels or `aria-label` on search boxes and menu toggles

> ⚠️ **The brand logo must not mirror in RTL**, while the nav layout must. Skip-link is a DGA
> requirement — `dga-launch-gate` checks for it on every page.

---

## Table

`/guidelines/components/data-display/table` · retrieved 2026-08-26

**Row cell variants** (11) — Default · Link · Entered text (editable) · Tag · Status · Switch ·
Feedback icon · Actions · Avatar · Checkbox · Custom.
**Header cell variants** (6) — Default · Actions · Checkbox (select/deselect all) · Icon
(sortable indicator) · Filter · Custom.
**Anatomy** — Table header · Table row · Table column · Header icon.

**Accessibility — DGA requirements**
- All interactive elements in the table keyboard-reachable
- Avoid complex layouts screen readers struggle to interpret
- **ARIA only as a last resort**, when native HTML is insufficient

> ⚠️ Thinnest accessibility section of any component page — no mention of `<caption>`,
> `scope`, `<th>`, sort announcement, or `aria-sort`. For a government service with data
> tables this is a real gap. Fall back to WCAG 2.1 AA and say so.
> ⚠️ **RTL:** column order mirrors. Numeric columns keep `dir="ltr"` with `tabular-nums`.

---

## Tabs

`/guidelines/components/navigational/tabs` · retrieved 2026-08-26

**Variants** — Horizontal (default) · Vertical.
**Overflow rule:** a horizontal tablist is confined to the container width and **does not
scroll or wrap** — DGA requires an overflow menu button ("More", three dots) instead.
**States** — Default · Hovered · Pressed · Focused · Disabled.
**Anatomy** — Container · Tab title · Icon · Selection indicator · More button · Divider.

**Accessibility — DGA requirements**
- `role="tablist"`, `role="tab"`, `role="tabpanel"`
- `aria-controls`, `aria-selected`, `aria-labelledby`; manage `tabindex`
- **Arrow keys** navigate between tabs; **Home / End** jump to first / last; Tab moves in and
  out of the tablist
- Visible focus indicators; high contrast for the active tab

---

## Pagination

`/guidelines/components/navigational/pagination` · retrieved 2026-08-26

**States** — Default · Hovered · Current page · Focused.
**Anatomy** — Previous navigation · Active page · Page items · Next navigation.

**Accessibility — DGA requirements**
- `<nav aria-label="Pagination">` wrapping `<ul>`/`<ol>` with one `<li>` per link
- `aria-current="page"` on the active page
- `<a href>` for real navigation; `<button>` when paginating dynamically (AJAX)
- Tab moves between links, Enter activates
- Arrow-key support suggested where there are many pages

> ⚠️ **RTL:** prev/next arrows mirror — the official library already does this via
> `[dir=rtl] .pagination__arrow button { transform: … }`.

---

## Tooltip

`/guidelines/components/feedback/tooltip` · retrieved 2026-08-26

**Variants** — Default · **Inverted** (darker background, for dark mode) · plus beak position:
Top · Bottom · Left · Right.
**Anatomy** — Help icon · Title · Body message · Container · Beak (the pointer).

**Accessibility — DGA requirements**
- `role="tooltip"` on the container
- Shows on **focus as well as hover**; hides when both are removed
- `aria-describedby` on the trigger, added when visible and removed when not
- Showing must not steal focus from the trigger
- Slight delay before show/hide, but open long enough to read
- Must not cover other interactive elements
- High contrast, readable text size, not cramped
- **Esc dismisses** without triggering the underlying element
- Interactive tooltips (containing links or buttons) must be treated as modal dialogs
- **Avoid auto-hide** — problematic for slow readers; prefer click-to-dismiss or persist while
  the trigger has focus

> ✅ The "Inverted … for dark mood" variant is independent confirmation that dark theme is a
> real part of the system, not just token scaffolding.
> ⚠️ **RTL:** Left/Right beak positions are physical. Map them to logical start/end.

---

## Dropdown

`/guidelines/components/actions/dropdown` · retrieved 2026-08-26

**Variants** — Default · Filled lighter · Filled darker. Error state integrated.
Helper text and error helper text as with Input.
**Anatomy** — Label · Option · Dropdown list item.

**Accessibility — DGA requirements**
- `role="listbox"` on the list, `role="option"` on each option
- `aria-haspopup="listbox"` and `aria-expanded` on the trigger
- `aria-selected` on the selected option
- `aria-labelledby` or `aria-label` for the accessible name
- Keyboard: Tab in/out · **Arrow keys open and navigate** · Enter/Space selects and closes ·
  **Esc closes without changing selection**
- On open, focus moves to the selected option, or the first if none
- Errors indicated by **both colour and text** ("Invalid selection", "Required field")

---

## Search box

`/guidelines/components/search-and-filters/search-box` · retrieved 2026-08-26

**States** — Default · Hovered · Pressed · Focused · Read-only · Disabled.
**Anatomy** — Input field · Placeholder text · Search icon · Clear button · **Voice search
icon** (microphone).

**Accessibility — DGA requirements**
- `role="search"` on the search region
- `aria-label`/`aria-labelledby` on the box (DGA's example: `aria-label="Search for products"`)
- `aria-placeholder` where the placeholder carries essential context
- Keyboard: Tab to focus · **Esc clears** · **Enter submits**
- Visible focus indicator
- Icons labelled — `aria-label="Clear search"` — or `aria-hidden` when decorative
- Usable on mobile; clear and voice buttons need adequate hit areas

> ⚠️ **RTL:** the magnifying glass is a cosmetic-mirroring case — pick once and record it in
> `brand.md`. See `../../dga-rtl-i18n/references/rtl-rules.md`.

---

## Accordion

`/guidelines/components/content-display/accordion` · retrieved 2026-08-26

**States** — Default · Hovered · Pressed · Focused · Disabled.
**Anatomy** — Accordion title (the control) · Expand/collapse icon · Panel.

**Accessibility — DGA requirements**
- `role="button"` on each header
- `aria-expanded="true|false"` reflecting open state
- `aria-controls` linking header to its panel
- `aria-disabled` on non-interactive headers
- Tab to each header; **Enter or Space** toggles
- On open, move focus into the panel content or keep it on the header — deliberately, not by
  accident
- Clear focus indicators; sufficient contrast on text and icons

---

## Link

`/guidelines/components/actions/link` · retrieved 2026-08-26

**States** — Default · Hovered · Pressed · Focused · **Visited** · Disabled.
**Anatomy** — Link text · Icon (optional).

**Accessibility — DGA requirements**
- Tab focuses; Enter activates (Space too, for links that act as buttons)
- **Descriptive link text — DGA explicitly forbids "click here" and "go to"**
- `title` attribute for extra context on generic text like "read more"
- `aria-label` where the text can't describe the destination
- **Links underlined by default** so they don't rely on colour alone — colour-blind users
- Contrast **≥4.5:1**
- External links: **`rel="noopener noreferrer"`** with `target="_blank"`
- **Indicate new-tab behaviour**, with visually hidden text for screen readers

> ✅ The underline rule and the "no click here" rule are concrete, checkable review items.

---

## Navigation drawer

`/guidelines/components/ui-shell/navigation-drawer` · retrieved 2026-08-26

**Item variants** — Parent (link with dropdown, expands to children) · Link (single level).
**States** — all six including Selected.
**Anatomy** — List items · Expand/collapse chevrons.

**Accessibility — DGA requirements**
- `role="navigation"`; `aria-expanded` on collapsible sections
- Keyboard: Tab, Enter, **Arrow keys**
- **Focus management on expand/collapse** — when a submenu opens, focus moves to its first
  item; when it collapses, focus returns to the parent
- Visible focus indicator
- **"Skip to content" links** so users can bypass a long drawer
- Sufficient contrast

> ⚠️ **RTL:** the drawer opens from the opposite side, and chevron direction mirrors for
> horizontal expansion.

---

## Digital stamp 🇸🇦

`/guidelines/components/content-display/digital-stamp` · retrieved 2026-08-26

**DGA-specific, and directly relevant to every government platform.** A trust component confirming the site is a
verified Saudi government platform. Nothing equivalent exists in other design systems.

**Variants** — Closed (default, compact assurance) · Opened (full verification detail, via a
"How you know?" link).

**What it verifies** — domain classification, HTTPS, and DGA registration. **The registration
number is tied to the entity's License Number.**

| Domain | Entity type |
|---|---|
| `gov.sa` | Ministries, authorities, public institutions, councils, national centres — most entities sit here |
| `edu.sa` | Universities, colleges, government training institutes |
| `org.sa` | Non-profits, conferences, committees affiliated with government |
| `sch.sa` | Public educational institutions, secondary and below |
| `med.sa` | Ministry of Health entities, hospitals, health centres, medical cities |
| `.sa` | Activities, initiatives and programmes of government entities |

**Anatomy** — Government website indicator · "How you know?" link · Domain verification icon +
message · Security confirmation icon + message · DGA registration (linked to License Number).

**Accessibility** — `role="status"`; `aria-label`/`aria-describedby` on icons; fully keyboard
operable including the expandable section; `aria-hidden="true"` on decorative icons; responsive.

> 🚩 **`dga-launch-gate` item.** the entity needs its DGA registration number and License Number before
> this component can be populated. Confirm early — it is a procurement/registration dependency,
> not a build task.

---

## Footer

`/guidelines/components/ui-shell/footer` · retrieved 2026-08-26 · **not listed in the site nav**

**Variants** — >600px (multi-column) · <600px (stacked vertically).

**Anatomy** — Group labels · Footer links · Social media icons · **Accessibility Tools** ·
Link · Legal text · Company logo.

> 🚩 **"Accessibility Tools" is part of DGA's required footer anatomy** — "buttons or links
> designed to improve usability for people with disabilities, which may include font size
> adjustment or contrast settings." This is a *feature* the entity must build, not just styling.
> Most teams miss it because it isn't a WCAG requirement. `dga-launch-gate` checks for it.

**Accessibility** — `role="contentinfo"`; all links keyboard reachable; visible focus;
descriptive link text; skip link; WCAG contrast.

---

## Second nav header

`/guidelines/components/ui-shell/second-nav-header` · retrieved 2026-08-26

A secondary bar **above** the primary navigation carrying contextual information.
**Variants** — Primary (bold dark green) · Gray (neutral).
**Anatomy** — Weather icon + status · Date (with calendar icon) · Time · Location · Quick
action icons.

**Accessibility** — `aria-label="Second Navigation Header"`; descriptive labels per element
(DGA's examples: `aria-label="Current weather in Al-Riyadh: Cloudy"`, `"Current time: 2:30 PM"`);
`aria-live="polite"` for the dynamic values; keyboard operable; decorative icons `aria-hidden`.

> ⚠️ The date in DGA's own demo reads "21 Jan 2024" — **Gregorian**. Same gap as the date
> picker. If you show a Hijri date here, you build it.

---

## Table of contents

`/guidelines/components/ui-shell/table-of-content` · retrieved 2026-08-26

**States** — Selected · Unselected · Default · Hovered · Pressed · Focused.
**Anatomy** — Title · Current page indicator · **Hierarchy indicators** (lines and indentation
showing nesting) · Section titles · Nested section titles.

**Accessibility** — `role="navigation"` + `aria-label="Table of contents"`;
`aria-current="page"` on the active section; keyboard focusable with clear `:focus`; skip links;
**on activation the page must update focus as well as scroll**, and the TOC must update its
active indicator.

> ⚠️ **RTL:** hierarchy indentation flips to the right edge.

---

## Card

`/guidelines/components/content-display/card` · retrieved 2026-08-26

**Variants** — Default · Expandable · Selectable. Expandable and selectable each carry
Default · Hovered · Focused · Disabled.
**Anatomy** — Image · Featured icon · Card title · Description · Custom component (e.g. avatar) ·
Tags · Rating · Actions · Container; plus expand/collapse icon (expandable) and checkbox
(selectable).

> ⚠️ **The card page's entire accessibility section is copy-pasted from Accordion** — it refers
> to "Accordions", "accordion headers" and "accordion panels" throughout. **Cards have no
> accessibility guidance of their own.** For selectable cards (checkbox semantics, group
> labelling) and expandable cards this is a real gap. Fall back to WCAG 2.1 AA and say so.

---

## Carousel

`/guidelines/components/content-display/carousel` · retrieved 2026-08-26

**Variants** — Carousel arrows (left/right, either side) · Carousel controls (pagination dots
below).
**Anatomy** — Navigation arrows · Pagination dots.

**Accessibility** — `role="listbox"` container, `role="option"` per item;
`aria-roledescription`; `aria-live` for auto-rotating carousels; focus must not be lost or
trapped; Tab/Enter/Space/arrows; high contrast against varied backgrounds.

> ⚠️ DGA gives **no pause/stop control requirement** for auto-rotating carousels. WCAG 2.1 AA
> 2.2.2 (Pause, Stop, Hide) requires one. Apply WCAG and flag the gap.
> ⚠️ **RTL:** arrows mirror, and dot order reverses.

---

## Menu

`/guidelines/components/navigational/menu` · retrieved 2026-08-26

**Trailing element types** — Text · Button · Tag · Switch · Icon · None.
**States** — Default · Hovered · Pressed · Focused · Disabled.
**Anatomy** — Group label · Item · Item lead icon · Item trailing element · Divider · Container.

> 🚩 **The menu page has NO accessibility section at all** — the on-page contents run Live Demo,
> Variants, Appearance, Anatomy and stop. For a navigational component that is a significant
> omission. Apply the WAI-ARIA menu pattern (`role="menu"`/`"menuitem"`, arrow-key navigation,
> Esc to close) and state explicitly that DGA provides nothing here.

---

## Tags

`/guidelines/components/search-and-filters/tags` · retrieved 2026-08-26

**Variants** — Standard tag (primary actions) · Status tag (state or condition).
**Styles** (5) — Outline · Neutral · Inverted · Subtle · Ghost.
**Anatomy** — Container · Text · Leading/trailing icon; status tags add a Status indicator.

**Do / Avoid** — group related statuses, don't mix unrelated ones · use words that describe a
state · **avoid labels that truncate** · let tags hug their labels, don't stretch the container.

**Accessibility** — `<span>` for non-interactive, **`<button>` for interactive** (removable);
`aria-label` for icon-only actions like a close icon; arrow-key navigation across a collection;
adequate size and spacing; sufficient contrast; **consider a confirmation or undo for removals**;
announce add/remove via `aria-live="polite" aria-atomic="true"`.

> ⚠️ "Avoid labels that will truncate" is harder in Arabic — the same label often runs longer.
> Check tag labels in both locales.

---

## Filtration

`/guidelines/components/search-and-filters/filtration` · retrieved 2026-08-26

**Variants** — Closed · Opened · Results (applied filters shown as chips at the top).
**Anatomy** — Filter button menu (icon, label, active count) · Applied filter results (tags
with X) · **Search within multi-select** (appears once options exceed a threshold; default
5–10 shown with "Show more") · Checkboxes · Divider · Scroll bar · Single select · Radio ·
Multi-select chips · Range slider · Input range · Date picker · Rating filter · Swap
placeholder · Actions (Apply / Clear).

**Accessibility** — `role="listbox"`/`"menu"` on the container; `aria-expanded` on the filter
button; `aria-live="polite"` on updating results (`assertive` where immediate); descriptive
`aria-label`/`aria-describedby` per filter; **`aria-hidden="true"` on hidden "Show more"
options**; logical tab order through to Apply/Clear; arrows for sliders, Enter/Space for
checkboxes and radios; visible selection states using more than colour; loading indicator with
`role="status"`; larger touch targets on mobile.

> ✅ **The only page in the entire design system that mentions `prefers-reduced-motion`** —
> "ensure they are subtle or allow users to disable them based on system settings." Cite this
> when arguing for reduced-motion support elsewhere; it is DGA's sole statement on motion.

---

## Charts

`/guidelines/components/data-display/charts` · retrieved 2026-08-26

**Variants and hard limits** — Pie: **maximum 6 segments** · Line: **maximum 3 series** ·
Bar: **maximum 3 series**. These are stated caps, not suggestions.
**Anatomy** — Segments/lines/bars · Legend · X-axis · Y-axis · X-axis label · Y-axis label.

**Accessibility** — `role="img"` on static charts; `aria-label`/`aria-labelledby` summarising
purpose and key insights; `aria-describedby` or visually hidden text covering major trends,
highs, lows and comparisons; keyboard navigation between data points (Tab, arrows) with each
focusable; accessible axis and legend labels linked via `aria-labelledby`; visible focus.

> ⚠️ No colour-blind-safe palette guidance, and no requirement to encode series by anything
> other than colour. Apply the WCAG 1.4.1 (Use of Colour) rule and pair colour with pattern,
> marker shape or direct labelling.

---

## Progress bar

`/guidelines/components/loading-and-status/progress-bar` · retrieved 2026-08-26

**Variants** — Linear · Circular. Error state integrated.
**Anatomy** — Container · Progress indicator · Label · Percentage indicator · Helper text ·
Success/error label · Success/error icon.

**Accessibility** — `role="progressbar"` with `aria-valuemin`, `aria-valuemax`, `aria-valuenow`;
`aria-label` or an associated `<label>`; `aria-live` for dynamic updates; distinct visual cues
for success and error **communicated to screen readers too**; sufficient contrast; responsive.

> ⚠️ **RTL:** fill direction must originate at the start edge — the right, in Arabic.

---

## Remaining components — condensed

The nine below follow the standard template; only what is distinctive is recorded.

### Chip · `/actions/chip`
Six states incl. Selected. Anatomy: container (rounded or rectangular) · text · leading icon ·
trailing icon. **A11y:** `role="button"` for dismissable; `aria-label="Dismiss [chip name]"`;
Enter/Space activates; **avoid overuse — DGA cites cognitive load**; avoid very small text.

### Floating button · `/actions/floating-Button`
Circular, floats above the UI, for the single most important action. Anatomy: container · icon ·
optional label. **A11y:** `aria-label` describing the *action* (`"Create new item"`), not
"Floating Action Button"; Tab + Enter/Space; large hit area; **placement must not obstruct
other content**. ⚠️ **RTL:** its corner flips — anchor with `inset-inline-end`.

### Avatar · `/data-display/avatar`
Types: Initial · Image · Icon. Sizes **24/32 (S) · 40/48 (M, standard) · 64/80/120 (L)**.
Shapes: circular · rectangular. Groups: stacked (overlapping) · unstacked.
**A11y:** `alt` carries the user's name; `role="img"` on the container is optional but useful.
⚠️ **RTL:** stacked group overlap direction reverses.

### Metric · `/data-display/metric`
Variants: large chart · small chart. Anatomy: label · main value · trend indicator (arrow +
comparison) · chart · settings icon · CTA button.
**A11y:** `aria-live="polite"` on dynamically updating values; labelled icons; keyboard-reachable
CTA; legible when zoomed. ⚠️ **RTL:** trend arrows are directional and mirror; keep the numeral
run LTR.

### Structured list · `/data-display/structured-list`
Density: compact · spacious. Behaviour: default (static) · selectable. Dividers and container
can each be shown or hidden.
**A11y — unusually thorough:** `role="list"`/`"listitem"`, and where tabular,
`role="table"`/`"row"`/`"columnheader"`/`"rowheader"`/`"cell"`/`"checkbox"`.

> ⚠️ **Inconsistency worth reporting:** the *non-interactive* Structured List gets a full table
> ARIA specification, while the actual **Table** page says use ARIA "only as a last resort" and
> names no roles at all. Apply Structured List's role set to Table too.

### Content switcher · `/data-display/content-switcher`
States: normal · hovered · selected · focused.
🚩 **Hard limit: 2–4 options.** DGA states fewer than two is useless and more than four clutters —
**use Tabs beyond four.** A checkable review rule.
**A11y:** `role="tablist"`/`"tab"`/`"tabpanel"`; `aria-controls`, `aria-selected`;
**arrow keys change selection** (left/right horizontal, up/down vertical) while Tab moves in and
out; `aria-hidden` + `hidden` toggled on inactive panels.

### Rating · `/feedback/rating`
Star states: normal · pressed · selected · **half**. Two types (default, brand), three sizes
(large, medium, small).
**A11y:** `role="radiogroup"` container, `role="radio"` per star; `aria-checked`; explicit labels
("1 star", "2 stars"); **arrow keys select**; Tab enters and leaves the group as a whole.

### Slide-out menu · `/navigational/slide-out`
Variants: white background · gray background. Anatomy: header (title + description) · grouped
content sections · divider · scroll bar · border · actions at the bottom.
**A11y:** `role="menu"`/`"menuitem"`; **focus trap while open**; **Esc closes**;
`aria-label="Close menu"`; decorative icons `aria-hidden`.
⚠️ **RTL:** slides in from the opposite side.

### List · `/content-display/list`
Ordered · unordered · with icons. **A11y:** `aria-labelledby` associating the group with its
heading; `aria-current="page"` for navigational lists; keyboard traversal with visible focus.
⚠️ Its accessibility intro says "accessible **link** components" — another copy-paste artefact.

### Divider · `/content-display/divider`
Horizontal · vertical. **A11y:** `role="separator"`; sufficient contrast — DGA warns against
low-contrast dividers that vanish into the background; must not take focus; consider removing
on mobile to reduce clutter.

### Quote · `/content-display/quote`
White background · transparent. Anatomy: quote title · quote text · author's name · author's
description · quotation marks · author's avatar.
**A11y:** `role="blockquote"` and the semantic `<blockquote>`; `aria-label="Author: [name],
[title]"`; quotation marks `aria-hidden="true"`.

> ✅ **Quote is the ONLY component page with a dedicated RTL section:** *"Support for
> Right-to-Left (RTL) Languages — use the `dir="rtl"` attribute or apply appropriate CSS styling
> to ensure the text and layout adapt to RTL languages seamlessly."* Cite it as DGA's clearest
> statement that RTL support is an accessibility obligation.

### Code snippet · `/content-display/code-snippet`
Multi-line · single-line. Anatomy: code block · programming-language tabs · copy-to-clipboard ·
line numbers · show-more.
**A11y:** `aria-live="polite"` announcing a successful copy; line numbers `aria-hidden="true"`
unless meaningful; language tabs need `role="tab"` + `aria-controls`; screen readers must
correctly interpret line breaks and indentation.
⚠️ **RTL:** code stays LTR inside an RTL page — force `dir="ltr"` on the code block.

### Textarea · `/forms-and-inputs/textarea` *(not in nav)*
Types: standard (scrollbar, resizable) · without scrollbar (resizable) · non-resizable (with
scrollbar). Filled styles: default · lighter · darker. Error feedback for forbidden characters.
States: default · hovered · pressed · focused · **read-only** · disabled.
**A11y:** native `<textarea>` with `<label for>`; `aria-describedby` for format and limits;
**DGA recommends allowing vertical resize** — `textarea { resize: vertical; }`.

### Number input · `/forms-and-inputs/number-input` *(not in nav)*
States: default · hovered · pressed · focused · read-only · disabled. Anatomy: label · input ·
increment (+) · decrement (−) · placeholder · helper text.
**A11y:** `role="spinbutton"`; `aria-valuemin`/`max`/`now`; **Up/Down arrows increment and
decrement**; `aria-invalid="true"` out of range; `aria-describedby` to the error; larger touch
targets for the +/− buttons.
⚠️ **RTL:** +/− button order mirrors; keep the numeral run LTR and consistent with the product's
numeral policy.

---

## Where DGA addresses RTL directly

Only four places in the entire system. These are the citable rules:

1. **Quote** — a dedicated "Support for Right-to-Left (RTL) Languages" accessibility section
2. **Steps** — "progresses from left to right or right to left for RTL languages", and the final
   step's connector line moves to the left side in RTL
3. **Buttons** — icon placement varies with "interface directionality"
4. **Pagination** — the shipped library mirrors the arrows via `[dir=rtl]` (implementation, not guideline)

Everywhere else, RTL behaviour is the consuming team's responsibility. That is the gap
`dga-rtl-i18n` fills.

## Documentation defects found across all 50 pages

| # | Page | Defect |
|---|---|---|
| 1 | Buttons | Prose lists five types, the list gives four |
| 2 | Buttons | Four paragraphs of notification ARIA pasted into the accessibility section |
| 3 | Date picker | Accessibility intro says "radio button components" |
| 4 | Checkbox | Accessibility intro says "radio button components" |
| 5 | **Card** | **Entire accessibility section is Accordion's — cards have no guidance of their own** |
| 6 | **Menu** | **No accessibility section at all** |
| 7 | List | Accessibility intro says "link components" |
| 8 | Notification | Section heading reads "Tips to effectively use tags" |
| 9 | Table | Names no ARIA roles, while Structured List specifies the full set |
| 10 | Carousel | No pause/stop requirement for auto-rotation (WCAG 2.1 AA 2.2.2) |
| 11 | Charts | No colour-blind-safe guidance; series distinguished by colour alone |

Report to DS-DGA@dga.gov.sa alongside the foundations defects.
