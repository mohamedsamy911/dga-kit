# Accessibility

**Sources:** https://design.dga.gov.sa/thoughts/AccessibilityEase · https://design.dga.gov.sa/guidelines/foundations/* · and the Accessibility
section of every component page · **Retrieved:** 2026-08-26

The design site's stated target is **WCAG 2.1 AA**:

> Our aim is to comply with WCAG 2.1 AA accessibility standards.
> — /guidelines/foundations/typography

DGA's separate accessibility guideline (2024) is built on **WCAG 2.2** — see *DGA's accessibility
guideline* below. The kit audits to **WCAG 2.2 AA**, which covers both.

DGA does not publish a separate numbered rule set. Its accessibility requirements are stated
per component, in prose, on each component page. This file consolidates them so `dga-a11y` and
`dga-design-review` can check DGA's actual requirements rather than generic WCAG.

## The five areas DGA names

From `/thoughts/AccessibilityEase`:

1. **Visual design** — sufficient contrast, colourblind-friendly schemes, alternatives to
   visual-only information
2. **Interactive elements** — keyboard-friendly navigation for everything
3. **Screen reader compatibility** — proper tagging and ARIA labels for images, icons and
   non-text elements
4. **Adaptable content** — resizable text, adaptable layouts, presentation changeable without
   losing information or structure
5. **Cognitive considerations** — clear intuitive navigation and consistent layouts to reduce
   cognitive load

## Global thresholds

| Requirement | Value | Source |
|---|---|---|
| Text contrast (small) | **4.5:1** | colour-system, typography, elevation, buttons |
| Text contrast (large) | **3:1** | colour-system |
| Graphical / UI component contrast | **3:1** | colour-system |
| AAA (aspirational) | 7:1 normal, 4.5:1 large | typography |
| **Touch / target size** | **44 × 44 px** | layout-and-spacing, iconography, buttons |
| **Body line height** | **≥ 1.5 × font size** — *"WCAG suggests"* | layout-and-spacing |
| Auto-dismissing notification duration | **≥ 5 seconds** | notification |

⚠️ **DGA contradicts itself on the large-text boundary** — the colour page says 24px, the
typography page says "above 18.5 Bold or 24 Regular". Apply the stricter reading.

⚠️ **`--text-secondary` (#dba102) fails 4.5:1 on every light background in DGA's own palette.**
See `CONTRAST-AUDIT.md`.

## Structural requirements

From `/guidelines/foundations/layout-and-spacing`:

- Reading order must match visual order — critical for screen readers and keyboard users
- Use landmark elements: `<header>`, `<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>`
- Group related items with spacing, borders, `<fieldset>`, and ARIA roles for regions
- Adequate space between clickable elements for motor-impaired and touch users
- Whitespace to reduce cognitive load and separate sections
- Define structure with contrast and alignment, **not colour alone**
- Layout responsive across sizes and orientations

From `/guidelines/components/ui-shell/navigation-header`:

- **A "Skip to Content" link at the start of the header** on every page

## Icons

From `/guidelines/foundations/iconography`:

| Case | Requirement |
|---|---|
| Meaningful icon | Text alternative via `alt`, `aria-label`, or `aria-labelledby` |
| Decorative icon | `aria-hidden="true"` or `alt=""` |
| Inline SVG | `role="img"` **plus** an accessible name |
| `<img>` icon | `alt` describes the icon's *function*, not its appearance |
| CSS background-image icon | Needs adjacent text — screen readers cannot reach it |
| Icon font | ARIA attributes, and character mappings that don't collide with screen readers |
| Interactive icon | ≥ 44×44px target, with surrounding space |

## Elevation

From `/guidelines/foundations/elevation`: depth alone is not a sufficient cue. Pair elevation
with borders or outlines, and make hover/focus changes visible through colour or underline as
well as shadow.

## Per-component ARIA — quick reference

Extracted from each component's Accessibility section. Full detail in `components.md`.

| Component | Required roles / attributes | Keyboard |
|---|---|---|
| **Button** | Native `<button>`; never `<div>`. `aria-label` when no descriptive text | Focusable by default |
| **Input** | `<label for>`/`id`; `aria-describedby` for helper and error; `aria-invalid="true"` on error; correct `type` | Tab / Shift+Tab |
| **Checkbox** | Native `<input type="checkbox">` + `<label>` | Tab to focus, **Space** to toggle |
| **Radio** | Shared `name`; `<fieldset>` + `<legend>` | **One** in tab sequence; **arrows** move within group |
| **Switch** | `<input type="checkbox">` + `role="switch"` + `aria-checked` | Tab, **Space** toggles |
| **File uploader** | Native `<input type="file">`; `aria-label` describing the action | Tab, **Enter or Space** opens dialog |
| **Slider** | `role="slider"`; `aria-valuemin/max/now` per thumb; `aria-label` | Arrows, **Home, End, PageUp, PageDown** |
| **Steps** | `<ol aria-label="Progress">`; `aria-current="step"`; non-nav steps not focusable | Enter/Space if navigational |
| **Date picker** | `role="dialog"` popup; `role="application"` grid; `grid`/`gridcell`/`row`/`columnheader`; `aria-selected`; `aria-live` | Arrows navigate, Enter selects, **Esc closes**; focus starts on selected date |
| **Modal** | `role="dialog"` + `aria-modal="true"` + `aria-labelledby`; background `aria-hidden="true"` | **Focus trapped**; Esc closes; focus returns to opener |
| **Notification** | `role="alert"` (urgent) or `aria-live="polite"`; consider no timeout for critical | Dismissable by keyboard |
| **Breadcrumbs** | `<nav aria-label="Breadcrumb">` + `<ul>`; `aria-current="page"`; separators `aria-hidden="true"` | Tab through links |
| **Navigation header** | `role="banner"`; `role="navigation"`; labels on search and menu toggles | Skip link; Enter/Space activates |
| **Navigation drawer** | `role="navigation"`; `aria-expanded`; skip links | Tab/Enter/arrows; focus into submenu on expand, back to parent on collapse |
| **Tabs** | `role="tablist"/"tab"/"tabpanel"`; `aria-controls`, `aria-selected`, `tabindex` | **Arrows** between tabs, **Home/End** to first/last |
| **Pagination** | `<nav aria-label="Pagination">` + list; `aria-current="page"`; `<a href>` or `<button>` if dynamic | Tab, Enter; arrows optional |
| **Dropdown** | `role="listbox"/"option"`; `aria-haspopup`, `aria-expanded`, `aria-selected` | Arrows open+navigate, Enter/Space selects, **Esc closes** |
| **Accordion** | `role="button"` header; `aria-expanded`, `aria-controls`, `aria-disabled` | Tab, **Enter/Space** toggles |
| **Tooltip** | `role="tooltip"`; `aria-describedby` added only while visible | Shows on **focus**, **Esc** dismisses; no auto-hide |
| **Search box** | `role="search"`; `aria-label`; labelled icons | **Esc clears**, **Enter submits** |
| **Link** | Descriptive text (avoid "click here"); **underlined**; `rel="noopener"` on `target="_blank"`; announce new tab | Tab, Enter |
| **Table** | Native table markup; DGA: ARIA *"only as a last resort"*, and names no roles | Interactive cells keyboard-reachable |
| **Structured list** | `role="list"/"listitem"`, and when tabular `"table"/"row"/"columnheader"/"rowheader"/"cell"/"checkbox"` | Traverse rows, columns, controls |
| **Content switcher** | `role="tablist"/"tab"/"tabpanel"`; `aria-controls`, `aria-selected`; `aria-hidden`+`hidden` on inactive panels | **Arrows** change selection; Tab in/out |
| **Rating** | `role="radiogroup"` + `role="radio"` per star; `aria-checked`; labels "1 star", "2 stars" | **Arrows** select; Tab enters/leaves the group |
| **Slide-out menu** | `role="menu"/"menuitem"`; `aria-label="Close menu"` | **Focus trap**; **Esc** closes |
| **Carousel** | `role="listbox"/"option"`; `aria-roledescription`; `aria-live` when auto-rotating | Tab/Enter/Space/arrows |
| **Chip** | `role="button"` when dismissable; `aria-label="Dismiss [name]"` | Tab, Enter/Space |
| **Floating button** | `aria-label` — DGA shows `"Floating Action Button"` and `"Create new item"`; prefer naming the action | Tab, Enter/Space |
| **Avatar** | `alt` carries the user's name; `role="img"` optional | n/a |
| **Metric** | `aria-live="polite"` on updating values; labelled icons | Tab to CTA |
| **Charts** | `role="img"`; `aria-label` summarising insight; `aria-describedby` for trends | Tab/arrows between data points |
| **Progress bar** | `role="progressbar"`; `aria-valuemin/max/now` | — (DGA states no focus rule) |
| **Radial stepper** | `role="progressbar"`; `aria-valuemin/max/now`; `aria-live="polite"` on step change; current step, total and step names shown visually | Tab; Enter/Space if steps are interactive |
| **Loading** | `role="status"` (or `"alert"`); `aria-live="polite"`; **always include text**; ≤3 flashes/second; respect reduced motion | **Must not be focusable** |
| **Skeleton** | `role="status"`; `aria-label="Content loading, please wait"`; removed from a11y tree when done; a way to pause or disable animation | `tabindex="-1"` |
| **Divider** | `role="separator"` | no focus *"unless they serve an interactive purpose or contain additional information"* |
| **Quote** | `role="blockquote"` + semantic `<blockquote>`; marks `aria-hidden` | n/a |
| **Code snippet** | `aria-live="polite"` on copy; line numbers `aria-hidden` | Tab, Enter/Space |
| **List** | `aria-labelledby` tying the group to its heading; `aria-current="page"` on navigational lists. ⚠️ DGA's intro says "link components" — a copy-paste artefact | keyboard traversal with visible focus |
| **Textarea** | Native `<textarea>` + `<label for>`; `aria-describedby` | Tab; DGA recommends `resize: vertical` |
| **Number input** | `role="spinbutton"`; `aria-valuemin/max/now`; `aria-invalid` | **Up/Down arrows** increment/decrement; Enter confirms *"if required"* |
| **Digital stamp** | `role="status"`; labelled icons | Keyboard-operable expander |
| **Footer** | `role="contentinfo"` | Tab through links |
| **Table of contents** | `role="navigation"` + `aria-label`; DGA: *"you can use"* `aria-current="page"` for the active section | Tab; activation must move focus, not just scroll |
| **Second nav header** | `aria-label="Second Navigation Header"`; `aria-live="polite"` on live values | Tab, Enter/Space |
| **Filtration** | `role="listbox"/"menu"`; `aria-expanded`; `aria-live`; `aria-hidden` on collapsed options | Tab to Apply/Clear; arrows for sliders |
| **Tags** | `<span>` static, **`<button>` interactive**; `aria-live` on add/remove | Arrows across a collection |
| **Card** | ⚠️ **none published** — DGA's section is Accordion's by mistake | — |
| **Menu** | 🚩 **no accessibility section exists** — apply the WAI-ARIA menu pattern | — |

✅ **All 50 component pages extracted.**

## Where DGA is silent — declare the fallback

DGA publishes no guidance on these. A skill must say so rather than implying a DGA rule exists:

- **Motion tokens** — no durations or easings are published. But `prefers-reduced-motion` **is**
  named, in three places: **Filtration** ("allow users to disable them based on system
  settings"), **Loading** (with a CSS example) and **Skeleton**. Loading also carries the
  **no more than three flashes per second** seizure rule. Treat reduced-motion support as a DGA
  expectation, not merely a WCAG fallback.
- **Screen-reader behaviour in Arabic** — no guidance on Arabic pronunciation, `lang`
  switching for mixed-language content, or bidi announcement order
- **Focus order under RTL** — DGA speaks to RTL on a few component pages, among them **Quote**
  (a dedicated RTL accessibility section), **Steps** (direction of progression and the final
  connector line), **Buttons** (icon placement follows "interface directionality"), and
  Pagination in the shipped code. The total is unverified — cite these pages, not a count. Focus
  order under RTL is not among them; it is the consuming team's responsibility.
- **Cognitive accessibility specifics** — named as an area, but with no testable criteria
- **Accessibility statement page** — not covered in the design system, nor in DGA's 2024
  accessibility guideline (read 2026-10-19). `TODO(harvest)`

For each of these, `dga-a11y` falls back to WCAG 2.2 AA and says explicitly that it is doing so.

## DGA's accessibility guideline

*Guideline For Web Accessibility of Digital Channels Content to Serve People with Disabilities and
the Elderly* — DGA-1-2-4-203, issue 2.0, May 2024, on dga.gov.sa (not the design site). Retrieved
2026-10-19. Raw capture:
[the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-a11y-guideline.md).

It walks through all 86 WCAG 2.2 success criteria, one page each, and names its audience as
government entities and the private sector working on government digital services. Its target:

<!-- dga -->
> The framework provides 4 steps on how to use this document to better understand web
> accessibility and align web content with the international industry standard of web
> accessibility (WCAG 2.2 level AA).
<!-- /dga -->

Its levels table — keep these labels when citing it:

| Level | DGA's label |
|---|---|
| A | Essential |
| AA | **Recommended** |
| AAA | Optimal |

> 🚩 **Do not call AA mandatory on this document's authority.** It aligns with 2.2 AA and labels AA
> "Recommended". DGA's Digital Experience Maturity Index 2026 recommends WCAG *"with a compliance
> level of no less than "AA""* — also a recommendation. Say "DGA's guideline targets WCAG 2.2 AA",
> not "DGA requires".

### The six criteria new in WCAG 2.2 at A or AA

| SC | Level | DGA's one-line description (abridged) | Check |
|---|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | the focused element is at least partly visible while navigating by keyboard | Sticky headers, footers, cookie banners never cover the focused element |
| 2.5.7 Dragging Movement | AA | *"a pointer alternative instead of dragging movements"* | Sliders, sortable lists, maps: a tap or click alternative exists |
| 2.5.8 Target Size (Minimum) | AA | at least **24×24 CSS px**, or enough spacing | Below 24×24, a 24px circle around each target does not overlap another |
| 3.2.6 Consistent Help | A | help mechanisms *"in a consistent location"* across pages | Contact, chat and FAQ links sit in the same place on every page |
| 3.3.7 Redundant Entry | A | the user *"doesn't have to enter the same information multiple times"* in a process | Multi-step forms prefill or offer what was already entered |
| 3.3.8 Accessible Authentication (Minimum) | AA | login relying on memory, transcription or problem-solving offers *"at least one alternative"* | Paste and password managers work; a type-the-characters CAPTCHA has an alternative |

> ⚠️ **2.5.8 in DGA's guideline.** Its example says *"buttons must be 24x24 CSS"*, then lists the
> spacing rule, inline links and equivalent controls under *"Nonconforming Content"* — the
> document's heading for cases not assessed. Those are WCAG's exceptions. A 20×20 icon button
> with enough spacing passes 2.5.8. DGA's own recommended minimum, 44×44 (Buttons page), is
> stricter still and is a recommendation.
