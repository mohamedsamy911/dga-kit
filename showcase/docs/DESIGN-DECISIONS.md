# Design decisions and evidence

Built 2026-08-31 using dga-kit **0.7.2**, installed through the Codex CLI. The `dga-frontend-dev` Codex agent authored the UI. The parent agent handled setup, documentation, verification, and delivery.

## Source boundary

The source material below was read from the installed kit's references. This build did **not** re-harvest DGA or verify the entire live system. Foundation/component references carry retrieval date **2026-08-26**; the completed template harvest is dated **2026-08-27**. Interpretations have not received independent DGA designer sign-off.

| Decision | Source or explicitly stated fallback |
| --- | --- |
| DGA color roles and sizes | [Color system](https://design.dga.gov.sa/guidelines/foundations/color-system), kit `foundations.md`, retrieved 2026-08-26 |
| Container up to 1280px, 16/32px outer padding, 600/960/1280 breakpoints, 44px targets, 1.5 body line-height | [Layout and spacing](https://design.dga.gov.sa/guidelines/foundations/layout-and-spacing), kit `foundations.md`, retrieved 2026-08-26 |
| IBM Plex Sans Latin, display/body distinction | [Typography](https://design.dga.gov.sa/guidelines/foundations/typography), retrieved 2026-08-26 |
| IBM Plex Sans Arabic companion font | **Project choice.** DGA's harvested page does not explicitly name an Arabic body typeface. No Saudi Font is used. |
| Arabic default, Gregorian dates and Latin digits in both locales | **Project choice.** The kit documents no DGA numeral/calendar policy. `Intl` provides locale formatting with explicit calendar and numeral options. |
| Arabic letter-spacing zero, logical properties, mixed-script bidi isolation | Kit `dga-rtl-i18n`; implementation guidance where the DGA harvest has limited RTL detail, not a fabricated DGA rule |
| Skip link and semantic navigation | [Navigation header](https://design.dga.gov.sa/guidelines/components/ui-shell/navigation-header), kit `accessibility.md`, retrieved 2026-08-26 |
| Footer text-size and contrast controls | Kit `components.md`, Footer anatomy, retrieved 2026-08-26; controls come before footer links in tab order |
| Feedback and page/platform modification dates | Kit `patterns.md` and `components.md`, retrieved 2026-08-26/27 |
| Focus and native form semantics | Kit `accessibility.md`, plus [WCAG 2.1](https://www.w3.org/TR/WCAG21/) fallback where DGA is silent |
| No official registration stamp | **Demo boundary.** No entity registration/license was supplied. Fabricating one would misrepresent official verification. |
| High-contrast mode | **Project choice.** Uses tested semantic pairings; never activates DGA's upstream dark theme. |
| Abstract geometric Wasl brand/hero | **Fictional project identity.** No DGA or government emblem and no official affiliation. |

## Tokens and contrast

`src/styles/dga-tokens.css` is copied unchanged from the installed plugin. `docs/dga-tokens.source.json` preserves its source data; the upstream MIT license is included. Project aliases belong in `src/styles/theme.css`; components consume semantic roles, not raw hex values.

DGA's published `text.secondary` is gold `#dba102` and measures approximately **2.30:1 on white**. The showcase does not use it as text on a light surface. The raw data still retains that value so it remains an honest harvest.

`dga-upstream-contrast.json` is an audit of **DGA's token table**, not of the application. Its failures are upstream evidence, not a green build gate. The app instead checks its own theme choices and rendered pages. DGA's published dark values remain audit-only; high contrast is independently authored here.

## Footer button states

The footer uses separate project aliases for button borders, hover, pressed, selected, and disabled states. Disabled text-size controls keep the dark footer surface and an opaque muted icon, with a dashed border to distinguish the unavailable action. They do not inherit the light disabled background used by buttons on white surfaces. Disabled primary/secondary buttons also retain their disabled appearance on hover.

The browser regression checks require at least 4.5:1 for enabled button foregrounds and 3:1 for focus outlines and our outlined control boundaries. Keeping disabled icons at least 3:1 is an additional **project usability choice**: inactive controls are exempt under WCAG. See [WCAG 2.1 non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html) and [minimum text contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html), reviewed 2026-08-31. WCAG does not require every button to have a contrasting border if its text/icon already identifies the control.

## Product scope

The app is a front-end demonstration: a catalog, details, simulated application/review/confirmation, request tracking, and kit explanation. All service titles, fees, processing times, and request status content are fictional. No back-end connection is present. Form values and page feedback remain in memory. The local request reference is illustrative and is not an acknowledgement from an agency.

The app uses lightweight hash routing, React state, and native controls. This deliberately avoids authentication, network APIs, a global-state library, a component-framework adapter, or a server. All fonts ship with the app.

## Not a launch-readiness verdict

This showcase does not demonstrate or validate Digital Transformation / Digital Experience Maturity indicator coverage, DGA registration, legal policy completeness, actual integration availability, Figma-only responsive variables, or Arabic screen-reader pronunciation. Those require separate evidence and review before any real launch.
