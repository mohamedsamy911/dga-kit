---
name: dga-design-review
description: Audit a UI design against Saudi DGA "Platforms Code" standards. Use when reviewing a screen, flow, mockup, Figma export, or live page for DGA compliance, or when asked whether a design is ready for development.
---

# DGA design review

Auditing a design against **Platforms Code**, the National Design System of Saudi Arabia.
Output is a findings report a designer can act on line by line.

## Before you start

1. **Load the rules.** Read `dga-design-system` — its quick reference first, then only the
   `references/` files the passes below need. Never review from memory.
2. **Get the artefact.** Screenshot, PDF, Figma export, or a URL. If it's a URL you can reach,
   read computed styles too — measured values let you cite exact numbers.
3. **Establish context** and state it: locale (ar / en / both), breakpoint, and whether this is
   a public service page or an internal console.

## Run the passes in this order

Fixed order, every run. A free-form review returns different findings each time and makes
"we fixed everything from last review" unanswerable.

### 1 · Layout & grid
- 12-column grid on desktop, reducing to 2–4 columns on smaller aspect ratios
- Breakpoints: **Mobile 0–599 · Tablet 600–959 · Desktop 960–1279 · XL 1280+**
- Container padding **16px mobile / 32px desktop**; max width **1280px**
- Running text within **720px** paragraph max-width
- Every gap on the DGA spacing scale (`none` 0 · `xxs` 2 · `xs` 4 · `sm` 6 · `md` 8 · `lg` 12 ·
  `xl` 16 · `2xl` 20 · `3xl` 24 · `4xl` 32 · `5xl` 40 · `6xl` 48 · `7xl` 64 · `8xl` 80 ·
  `9xl` 96 · `10xl` 128 · `11xl` 160). Off-scale spacing is the most common finding — measure.
- Reading order matches visual order; landmark structure present
- **Skip-to-content link** at the start of the header

### 2 · RTL correctness
Before the cosmetic passes — RTL errors are structural and invalidate what follows.
- Genuinely mirrored layout, not an LTR layout with Arabic poured in
- Reading order, alignment, icon mirroring — `dga-rtl-i18n/references/rtl-rules.md`
- **Steps** progress right-to-left, and the final step's connector line is on the *left*
  (DGA states both explicitly)
- **Breadcrumb separators** and the mobile back arrow mirror
- **Brand logo does not mirror**
- Latin runs and numerals inside Arabic text are isolated

### 3 · Colour & contrast
- Every colour maps to a DGA token — name the nearest one for anything that doesn't
- Small text (<24px) **≥ 4.5:1** · large text **≥ 3:1** · UI components and graphics **≥ 3:1**
- **`--text-secondary` (#dba102) on any light background is an automatic Blocker** — 2.30:1.
  See `CONTRAST-AUDIT.md`.
- `-light` text tokens (`primary-light`, `secondary-light`, `tertiary-light`) on a light
  background — Blocker. They are dark-surface tokens.
- Green text on `background-body` clears AA by 0.05 — flag for explicit verification
- DGA's neutral pairing rule: text from Gray 500/600/700/950 on backgrounds ≤400; white text
  on backgrounds ≥500
- Nothing conveyed by colour alone
- State the measured ratio and the required one. Never assert a failure without the number.

### 4 · Typography
- **IBM Plex Sans** only. **Saudi Font** is restricted to national and seasonal occasions
  (National Day, Founding Day), **main headings only** — never body or long-form. Saudi Font
  in paragraph text is a Blocker.
- Sizes on the DGA scale — Display 2xl/xl/lg/md/sm/xs (72/60/48/36/30/24) and Text
  xl/lg/md/sm/xs/2xs (20/18/16/14/12/10), with DGA's paired line heights
- Display styles for headings only, never body copy
- Line height **≥1.5×** font size for body text
- **Tracking −2% on Display 2xl–md must not apply to Arabic** — letter-spacing breaks the
  connected script. Blocker on Arabic text.
- Text 2xs (10px) used for anything a user must read — Major
- Heading hierarchy sequential

### 5 · Components & states
- Is each component a DGA component, a modified one, or invented? Flag the latter two and name
  the DGA component it should be.
- **DGA's six states: Default · Hovered · Pressed · Selected · Focused · Disabled.** A design
  that omits states the screen needs is incomplete — a form with only default-state inputs is
  not compliant.
- Anatomy matches the documented parts for that component (`components.md`)
- Icon sizes from the DGA bands: 10/14/16 XS · 18/20 S · **24 standard** · 28/32 L
- Breadcrumbs truncate past **five** items; mobile shows back arrow + previous page only
- Notifications: no timeout on critical; **≥5s** if auto-dismissing
- **Content switcher with more than 4 options — Major.** DGA caps it at 2–4; use Tabs instead.
- **Charts over the caps — Major.** Pie max 6 segments; line and bar max 3 series.
- **Tabs that scroll or wrap — Major.** DGA requires a More/overflow button.
- Avatar sizes from the DGA bands: 24/32 S · 40/48 M · 64/80/120 L
- **Footer without Accessibility Tools — Blocker.** DGA lists font-size and contrast controls as
  required footer anatomy. It is a feature to build, not styling.
- **Government site without the Digital Stamp — Blocker.** Needs the entity's DGA registration number
  and License Number; confirm early, it's a registration dependency.

### 6 · Interaction & accessibility
- Target size **≥44×44px**
- Focus indicator present *and* visible against the actual background behind it
- Focus order correct under RTL
- Per-component ARIA per `accessibility.md` — modal focus trap and Esc, radio-group roving
  tabindex and arrow keys, `aria-current="page"` on breadcrumbs, `role="banner"`/`"navigation"`
- Error states associated to their fields (`aria-describedby`, `aria-invalid`)
- Loading, empty and error states shown
- **Links underlined** and never labelled "click here" or "go to" — both are stated DGA rules
- **Reduced motion respected.** DGA requires `prefers-reduced-motion` support in three places
  (Filtration, Loading, Skeleton) and caps flashing at three per second.
- Loading indicators carry text, use `role="status"`, and are **not focusable**
- Card and Menu: DGA publishes no accessibility guidance for either (Card's section is
  Accordion's by mistake; Menu has none). Apply WCAG 2.1 AA and **say DGA is silent**.
- Cite the DGA rule **and** the WCAG 2.1 AA criterion

### 7 · Content & bilingual parity
- Terminology, tone, sentence case
- Numeral system consistent product-wide; date, currency, phone and ID formats correct
- **Hijri**: if the screen shows a date, does it need Hijri? DGA's own date picker is
  Gregorian-only and provides nothing here — flag any date field that lacks a decision.
- Both locales: same content, same features, Arabic that reads as Arabic

## Rules for findings

- **Cite or drop it.** Name the DGA rule and its source. If DGA doesn't cover something, you may
  still raise it — label it `House` and say plainly it is not a DGA requirement.
- **Where DGA contradicts itself, say so and apply the stricter reading.** Known: the large-text
  contrast boundary (24px on the colour page vs 18.5 Bold / 24 Regular on typography).
- **Give the fix with the token.** "20px isn't on the scale — use 24px (`3xl`)" beats "spacing
  is inconsistent."
- **One finding per issue, not per instance** — eleven wrong greys is one finding with a count.
- **Don't invent measurements.** Can't measure it from the artefact? `Note — needs measurement`.

## Output

`references/report-template.md`, severity from `references/severity-rubric.md`.

Close with an explicit verdict: **Ready for development** or **Not ready — N blockers**.
