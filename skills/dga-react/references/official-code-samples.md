# DGA's own code samples, per component

Every DGA component page has a **Code** tab beside the live demo. This table records what each
one shows: the element names and the package it imports. Read 2026-10-19 from all 50 component
pages; every sample, byte-exact: [the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-code-samples.md).

> ⚠️ **Illustrative, not a requirement.** These are DGA's demo snippets. A prop value in one
> (`size="lg"`, `style="primary-brand"`) shows only that the sample *uses* it. It is not a DGA
> rule, a default, or a complete API. For the API, check the package's own types
> (`official-packages.md`). Two samples are not samples at all, and one names an element
> `DgaRadialSteppe`. Validate before copying.

Under every sample DGA displays the same note:

<!-- dga -->
> While the use of the bundled React library is recommended for optimal compatibility and
> performance, it's not mandatory.You have the flexibility to leverage your preferred framework
> if you choose to do so. However, it's crucial to ensure that the component is styled according
> to the provided examples, maintaining consistency in the user interface regardless of the
> library used.
<!-- /dga -->

**Which package?** DGA's samples disagree. 9 import from `platformscode-react` (no release since
0.1.0 on 2024-09-18) and 5 from `platformscode-new-react`. The NavHeader sample imports from
both, plus `@platformscode/icons`. 35 show only the element with no import, and the 2
placeholders import Mongoose from `'untitled'`. This kit's
`dga-react` skill targets `platformscode-new-react`, the package with current releases. If you
copy a sample, import its element from the package you actually installed, and check that the
export exists.

| Component | Element(s) the sample shows | Import shown | Note |
|---|---|---|---|
| Buttons | `Btn`, `Tick02Icon` | `platformscode-react` |  |
| Chip | `DgaChip` | none shown |  |
| Dropdown | `Dropdown` | none shown |  |
| Floating Button | `FloatingButton` | `platformscode-new-react` |  |
| Link | `Link` | none shown |  |
| Accordion | `DgaAccordion` | none shown |  |
| Card | `DgaCard` | none shown |  |
| Carousel | `DgaCarousel`, `DgaCarouselItem` | none shown |  |
| Code Snippet | `DgaCodesnippet` | none shown |  |
| Digital Stamp | `DgaDigitalSignature` | `platformscode-new-react` |  |
| Divider | `DgaDivider` | none shown |  |
| List | `DgaListItem`, `DgaListV2` | none shown |  |
| Quote | `DgaQuote` | none shown |  |
| Avatar | `DgaAvatar` | none shown |  |
| Charts | `DgaChart` | `platformscode-react` |  |
| Content Switcher | `DgaContentSwitcher` | none shown |  |
| Metric | `DgaMetric` | none shown |  |
| Structured List | `DgaStructuredList` | none shown |  |
| Table | `DgaDataTable` | none shown |  |
| Modal | `DgaModal` | none shown |  |
| Notification | `DgaNotificationToast` | none shown |  |
| Rating | `DgaRating` | none shown |  |
| Tooltip | `DgaTooltip` | none shown |  |
| Checkbox | `DgaCheckbox` | none shown |  |
| Datepicker | `DgaDatepicker` | none shown |  |
| File Uploader | `DgaFileUpload` | none shown |  |
| Input | `DgaTextInput` | none shown |  |
| Number Input | `DgaNumberInput` | `platformscode-react` |  |
| Radio | `DgaRadioButton` | none shown |  |
| Slider | `DgaSlider` | `platformscode-new-react` |  |
| Steps | `DgaProgressIndicator`, `DgaProgressIndicatorStep` | none shown |  |
| Switch | `Switch` | `platformscode-react` |  |
| Textarea | `Textarea` | `platformscode-react` |  |
| Loading | `Spinner` | `platformscode-react` |  |
| Progress Bar | `Tag` | `platformscode-react` | Shows only a `Tag` with an icon; no progress bar |
| Radial Stepper | `DgaRadialSteppe` | none shown | Element spelled `DgaRadialSteppe` (sic) |
| Skeleton | `DgaLineSkeleton`, `DgaSquareSkeleton` | none shown | Plain `<div>` wrapper around the skeleton elements |
| Breadcrumbs | `DgaBreadcrumbs` | none shown |  |
| Menu | — | `untitled` | Shows an unrelated Mongoose schema, not a Menu sample |
| Pagination | `DgaPagination` | none shown |  |
| Slide Out | `DgaButton`, `DgaDivider`, `DgaMenuGroup`, `DgaMenuItem`, `DgaSlideoutMenu`, `DgaSlideoutMenuActions`, `DgaSlideoutMenuHeader`, `DgaSlideoutMenuItems` | none shown |  |
| Tabs | `TabsComponent` | `platformscode-new-react` |  |
| Filtration | `DgaFiltration` | none shown |  |
| Search Box | `DgaSearchBox` | none shown |  |
| Tags | `DgaTag` | none shown |  |
| Footer | — | `untitled` | Shows an unrelated Mongoose schema, not a Footer sample |
| Navigation Drawer | `CircleIcon`, `SidePanel` | `platformscode-react` |  |
| Navigation Header | `DgaIcon`, `NavHeader`, `NavHeaderActionBtn`, `NavHeaderActions`, `NavHeaderLink`, `NavHeaderLogos`, `NavHeaderMain`, `NavHeaderMenu` | `@platformscode/icons`, `platformscode-new-react`, `platformscode-react` |  |
| Second Nav Header | `DgaButton`, `DgaIcon`, `DgaSecondNavHeader`, `DgaSecondNavHeaderActions`, `DgaSecondNavHeaderContent`, `DgaSecondNavHeaderItem` | none shown |  |
| Table Of Content | `DgaTableOfContent` | none shown |  |
