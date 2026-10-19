# Design decisions and evidence

Built 2026-08-31 using dga-kit **0.7.2**, installed through the Codex CLI. Updated 2026-10-19 to dga-kit **0.13.0** (see *Kit 0.13.0 update* below). The `dga-frontend-dev` Codex agent authored the UI. The parent agent handled setup, documentation, verification, and delivery.

## Source boundary

The source material below was read from the installed kit's references. This build did **not** re-harvest DGA or verify the entire live system. Foundation/component references carry retrieval date **2026-08-26**; the completed template harvest is dated **2026-08-27**. Interpretations have not received independent DGA designer sign-off.

| Decision | Source or explicitly stated fallback |
| --- | --- |
| DGA color roles and sizes | [Color system](https://design.dga.gov.sa/guidelines/foundations/color-system), kit `foundations.md`, retrieved 2026-08-26 |
| Container up to 1280px, 16/32px outer padding, 600/960/1280 breakpoints, 44px targets, 1.5 body line-height | [Layout and spacing](https://design.dga.gov.sa/guidelines/foundations/layout-and-spacing), kit `foundations.md`, retrieved 2026-08-26 |
| IBM Plex Sans Latin, display/body distinction | [Typography](https://design.dga.gov.sa/guidelines/foundations/typography), retrieved 2026-08-26 |
| IBM Plex Sans Arabic | DGA's [Assessment Checklist](https://design.dga.gov.sa/assets/updated-checkList.xlsx) item 3, retrieved 2026-10-19 (the typography page names only IBM Plex Sans). Body text uses the kit's Latin-first `--dga-font-sans` in both directions. No Saudi Font is used. |
| Arabic default, Gregorian dates and Latin digits in both locales | **Project choice.** The kit documents no DGA numeral/calendar policy. `Intl` provides locale formatting with explicit calendar and numeral options. |
| Arabic letter-spacing zero, logical properties, mixed-script bidi isolation | Kit `dga-rtl-i18n`; implementation guidance where the DGA harvest has limited RTL detail, not a fabricated DGA rule |
| Skip link and semantic navigation | [Navigation header](https://design.dga.gov.sa/guidelines/components/ui-shell/navigation-header), kit `accessibility.md`, retrieved 2026-08-26 |
| Footer text-size and contrast controls | Kit `components.md`, Footer anatomy, retrieved 2026-08-26; controls come before footer links in tab order |
| Feedback and page/platform modification dates | Kit `patterns.md` and `components.md`, retrieved 2026-08-26/27 |
| Focus and native form semantics | Kit `accessibility.md`, plus [WCAG 2.2](https://www.w3.org/TR/WCAG22/) AA as the audit target. The design site states WCAG 2.1 AA; DGA's accessibility guideline DGA-1-2-4-203 aligns with WCAG 2.2 AA and labels AA "Recommended" — neither is treated as a certification |
| No official registration stamp | **Demo boundary.** No entity registration/license was supplied. Fabricating one would misrepresent official verification. |
| High-contrast mode | **Project choice.** Uses tested semantic pairings; never activates DGA's upstream dark theme. |
| Dark mode | **Project choice.** A complete showcase-specific semantic palette built from harvested primitives; it never activates DGA's published dark roles. |
| Abstract geometric Wasl brand/hero | **Fictional project identity.** No DGA or government emblem and no official affiliation. |

## Kit 0.13.0 update (2026-10-19)

The kit added DGA's Assessment Checklist, registration controls, accessibility guideline and two
measurement reports. Applied here, each with its source:

| Change | Source |
| --- | --- |
| Generated tokens re-vendored byte-for-byte (adds `color.alpha`, the Arabic face in `--dga-font-sans`) | Kit `generate-tokens.mjs`; hash pinned in `scripts/check-theme.mjs` |
| Services section directly below the hero; the trust strip moved after it | Checklist item 7 (service platforms) |
| Service page headings Requirements · Required Documents · Steps · Service Details Card (الشروط · المستندات المطلوبة · الخطوات · بطاقة تفاصيل الخدمة); card adds target audience and channels | Checklist item 8; kit `patterns.md` service card |
| External links carry an external-link icon; internal links no longer use an outward arrow. Lucide `SquareArrowOutUpRight` stands in for DGA's "Link Square" icon — a **documented deviation** from items 14 and 29, which name DGA's icon | Checklist items 14 and 29 |
| Privacy page linked at the form, before data entry | Checklist item 41 |
| "Report a showcase issue" (GitHub) in the footer on every page — a contact for the showcase itself, not task help and not a service or government channel | Project choice, toward checklist item 27's contact information (see below) |
| 404 heading and CTA use DGA's suggested Arabic copy | Kit `content.md`, *Copy DGA gives* |
| Language switching updates the whole page | Checklist item 39 (already implemented; now cited) |
| Search result counts announced with `role="status"`; footer tools built in, no overlay | DXMI 2026 recommendations 5 and 4 (advisory) |
| axe scans include `wcag22aa` | WCAG 2.2 AA audit target |

**Demo boundaries, not exemptions.** A fictional site cannot truthfully show these, so they are
absent and nothing here counts as meeting them: the Digital Stamp (checklist item 11, control
2-106-30), registration and approval under DGA-1-2-2-106, and entity logos and official contact
details in the footer (item 27).

**Not implemented — gaps, not boundaries.** A fictional site could provide these; it does not
yet: a sitemap page (item 37) and the star rating section (item 8, `rating-section` template; the
per-page feedback section is present).

## Tokens and contrast

`src/styles/dga-tokens.css` is copied unchanged from the installed plugin. `docs/dga-tokens.source.json` preserves its source data; the upstream MIT license is included. Project aliases belong in `src/styles/theme.css`; components consume semantic roles, not raw hex values.

DGA's published `text.secondary` is gold `#dba102` and measures approximately **2.30:1 on white**. The showcase does not use it as text on a light surface. The raw data still retains that value so it remains an honest harvest.

`dga-upstream-contrast.json` is an audit of **DGA's token table**, not of the application. Its failures are upstream evidence, not a green build gate. The app instead checks its own theme choices and rendered pages. DGA's published dark values remain audit-only; high contrast is independently authored here.

## Project dark mode

DGA publishes dark declarations, but the installed kit records that their selector is unreachable and that five light status surfaces have no dark equivalent. The showcase therefore does not enable or repair those upstream roles. Its `data-theme="dark"` block is a clearly labeled project palette mapped through the same semantic aliases as light mode. Components never select primitive colors directly.

The footer toggle is bilingual, keyboard operable, and exposes its state with `aria-pressed`. The selection lives only in React memory: routes and language changes preserve it, while a reload returns to light mode in line with the demo's no-persistence boundary. Native controls receive the matching CSS `color-scheme`.

Dark mode and high contrast are independent settings. High contrast follows the dark block in the cascade and temporarily takes visual precedence, while `data-theme="dark"` remains selected. Turning high contrast off restores the selected dark palette. This behavior and the full dark route set are browser-tested in Arabic and English at mobile and desktop widths.

## Footer button states

The footer uses separate project aliases for button borders, hover, pressed, selected, and disabled states. Disabled text-size controls keep the dark footer surface and an opaque muted icon, with a dashed border to distinguish the unavailable action. They do not inherit the light disabled background used by buttons on white surfaces. Disabled primary/secondary buttons also retain their disabled appearance on hover.

The browser regression checks require at least 4.5:1 for enabled button foregrounds and 3:1 for focus outlines and our outlined control boundaries. Keeping disabled icons at least 3:1 is an additional **project usability choice**: inactive controls are exempt under WCAG. See [WCAG 2.1 non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html) and [minimum text contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html), reviewed 2026-08-31. WCAG does not require every button to have a contrasting border if its text/icon already identifies the control.

## Product scope

The app is a front-end demonstration: a catalog, details, simulated application/review/confirmation, request tracking, and kit explanation. All service titles, fees, processing times, and request status content are fictional. No back-end connection is present. Form values and page feedback remain in memory. The local request reference is illustrative and is not an acknowledgement from an agency.

The app uses lightweight hash routing, React state, and native controls. This deliberately avoids authentication, network APIs, a global-state library, a component-framework adapter, or a server. All fonts ship with the app.

## Not a launch-readiness verdict

This showcase does not demonstrate or validate Digital Transformation / Digital Experience Maturity indicator coverage, DGA registration, legal policy completeness, actual integration availability, Figma-only responsive variables, or Arabic screen-reader pronunciation. Those require separate evidence and review before any real launch.
