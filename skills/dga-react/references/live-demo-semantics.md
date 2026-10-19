# What DGA's own components render — observed, not promised

**Installing DGA's package does not guarantee DGA's own accessibility guidance is met.** On
2026-10-19 the live demo on each component page of design.dga.gov.sa was inspected in a browser.
The demo is DGA's own `dga-*` web component, and 44 demos had a single component element to
inspect. In 19 of them, the rendered markup lacks semantics DGA's guidance asks for (the "DGA
asks" column comes from `../../dga-design-system/references/accessibility.md`). If you use the
package, inspect the rendered component and add what is missing. Evidence:
[the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-live-demo-semantics.md).

> ⚠️ **Scope of this evidence.** It shows what DGA's live demos rendered on 2026-10-19: one
> package version (not recorded), one demo state, before interaction. It lists the roles,
> attributes and tags found inside each component, not which element carries which. A later
> version may fix a gap, or a prop the demo does not set may add the attribute. Native HTML
> counts: `<dialog>` is a dialog, `<input type="range">` a slider. This is an observation of DGA's
> implementation, not a DGA rule. Report confirmed gaps to DS-DGA@dga.gov.sa.

## Missing in the rendered demo

| Component | DGA asks | The demo rendered |
|---|---|---|
| Tabs | `role="tablist"/"tab"/"tabpanel"`, `aria-selected`, `aria-controls` | `ul`/`li`/`a`, no tab roles |
| Content switcher | `role="tablist"/"tab"/"tabpanel"`, `aria-selected`, `aria-controls` | `button`s, no tab roles |
| Switch | `role="switch"`, `aria-checked` | `input[type=checkbox]` + `label`: checkbox semantics, not switch |
| Accordion | `role="button"` header, `aria-expanded`, `aria-controls` | `a` elements, no `role="button"`, no `aria-expanded` |
| Dropdown | `role="listbox"/"option"`, `aria-haspopup`, `aria-expanded` | `button`, `ul`/`li`, none of these |
| Steps | `<ol aria-label="Progress">`, `aria-current="step"` | no list, no `aria-current` |
| Pagination | `<nav aria-label="Pagination">`, `aria-current="page"` | `ul`/`li`/`button`, no `nav`, no `aria-current` |
| Slide-out menu | `role="menu"/"menuitem"` | `button`s, `ul`/`li`, no menu roles |
| Search box | `role="search"`, `aria-label` | `input[type=text]` + `button`, neither |
| Table of contents | `role="navigation"` + `aria-label` | `ul`/`li`/`a`, no `nav` |
| Filtration | `aria-expanded`; `role="listbox"`/`"menu"` | `button aria-label="Filter"`, no `aria-expanded` |
| Progress bar | `role="progressbar"`, `aria-valuemin/max/now` | an `svg` with `role="img"`, no `progressbar` role |
| Radial stepper | `role="progressbar"`, `aria-valuemin/max/now` | an `svg`, plus `aria-size` — not an ARIA attribute |
| Loading | `role="status"` (or `"alert"`), `aria-live`, text | no role at all |
| Skeleton | `role="status"`, `aria-label` | no role at all |
| Divider | `role="separator"` | no role, no `<hr>` |
| Quote | `role="blockquote"` + `<blockquote>` | neither |
| Digital stamp | `role="status"` | `svg` and `a` with `role="img"`, no `status` role |
| Charts | `role="img"` + `aria-label` summarising the insight | an `svg`, no role or label |

## Present in the rendered demo

These render the native element DGA's guidance implies. That does not prove labels, values or
keyboard behaviour; test those.

| Component | Rendered |
|---|---|
| Checkbox, file uploader, slider, number input | Native `input` of type `checkbox`, `file`, `range`, `number` |
| Table, structured list | `<table>` with `<th>` |
| Modal | Native `<dialog>`; `aria-labelledby` was not observed |
| Breadcrumbs | A `<nav>`, `aria-label="breadcrumb"` and `aria-current="page"` |
| Link | The new-tab link has `rel="noopener noreferrer"`; DGA asks for `noopener` |

## Not determined

Not determined by this capture:
- **Chip, code snippet, avatar, metric, input, radio, rating, textarea, tags, carousel, list,
  second nav header:** they depend on a state, variant, label value or element association the
  capture does not show.
- **Tooltip, dropdown open state, accordion open state, date picker popup, notification toast:**
  they appear only on interaction, and scripted events did not open them.
- **Buttons, floating button, footer, navigation header:** no single `dga-*` element to inspect.
- **Navigation drawer:** no inline demo.

DGA publishes no accessibility section for Card or Menu, so neither is a gap here.
