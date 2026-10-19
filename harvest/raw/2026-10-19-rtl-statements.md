# Raw capture — every place DGA's guidance names a reading direction or a side, 2026-10-19

Closes the `TODO(verify)` on DGA's own RTL statements by enumerating them, instead of counting
from memory.

**Method.**

1. Downloaded the live site build from Saudi Arabia: `https://design.dga.gov.sa/assets/index-BO_6JOKP.js`,
   14,860,610 bytes, sha256 `4b8aa21d37ab66d281ec1a1ff2dacfe3e911b2d7296a9c5ea89e668c18af0340`.
   The shell linked `index-CYyqM6kT.css`, the stylesheet already recorded in
   `source-inventory.json`, so this is the same deploy as the 2026-10-18 re-read.
2. Searched every string literal in it, English and Arabic, for: `RTL`, `LTR`, `right-to-left`,
   `left to right`, `mirror`, `directionality`, `right side`, `left side`, `left hand`,
   `the right`, `the left`, `to the right`, `to the left`, `من اليمين إلى اليسار`,
   `من اليسار إلى اليمين`, `الجانب الأيمن`, `الجانب الأيسر`, `على اليسار`, `اتجاه`.
3. Opened each matching English page in a browser and checked the sentence is **displayed**.
   DGA's text table holds strings its pages never show, and two hits were of that kind.

The list below is complete for those terms against this build, and no further. Repeat this when
either asset name in the shell changes (`index-BO_6JOKP.js` or `index-CYyqM6kT.css`): the page
text lives in the script, so a text-only deploy may change the script and not the stylesheet.

## 1 · Explicit RTL guidance — displayed

Quote, `/guidelines/components/content-display/quote`, accessibility section:

<!-- dga -->
> Support for Right-to-Left (RTL) Languages: Use the dir="rtl" attribute or apply appropriate CSS styling to ensure the text and layout adapt to RTL languages seamlessly.
<!-- /dga -->

Arabic text table, same item:

<!-- dga -->
> دعم اللغات من اليمين إلى اليسار (RTL): استخدم السمة dir="rtl" أو قم بتطبيق تنسيقات CSS المناسبة لضمان تكيف النص والتخطيط مع اللغات من اليمين إلى اليسار بسلاسة.
<!-- /dga -->

Steps, `/guidelines/components/forms-and-inputs/steps`, Alignment and Anatomy:

<!-- dga -->
> A step-by-step navigation element that progresses from left to right or right to left for RTL languages, commonly used in forms or processes.
<!-- /dga -->

<!-- dga -->
> Final step: Represents the last step in the sequence; it can be in any of the three states. It has no line on the right side (or the left side if it is RTL), indicating the absence of a following step.
<!-- /dga -->

Buttons, `/guidelines/components/actions/buttons`, Icon Placement in Buttons:

<!-- dga -->
> Icons in Platforms Code the icon can be a leading icon or trailing icon. A trailing icon follows the button label, while a leading icon precedes it. Both types serve similar purposes, offering visual cues and enhancing the user interface. However, their use varies based on content flow, level of emphasis or interface directionality.
<!-- /dga -->

## 2 · Templates written right-to-left first — displayed

Search page and FAQs page (`/guidelines/templates/search-page`, `/guidelines/templates/faqs-page`),
the same sentence on both:

<!-- dga -->
> How to Display the Selected Filter Results: After the user selects and confirms the filter options, the results are displayed in a list at the bottom of the search section, from right to left.
<!-- /dga -->

Sitemap page, `/guidelines/templates/sitemap-page`:

<!-- dga -->
> Spacing: For main page links, the spacing on the right side starts at 0px. For subpage links, the spacing starts at 16px and increases by 16px with each sublevel (16px, 32px, 48px, and so on).
<!-- /dga -->

## 3 · A physical side, with no direction stated — displayed

These name one side in the English text and the same side in the Arabic text table. None says
whether the side changes with the reading direction.

Textarea, `/guidelines/components/forms-and-inputs/textarea`, Types (Standard, and Non-Resizable):

<!-- dga -->
> This textarea includes a scrollbar on the right side, allowing users to scroll through the content if it exceeds the visible area.
<!-- /dga -->

Second Nav Header, `/guidelines/components/ui-shell/second-nav-header`, Anatomy, Quick Action Icons:

<!-- dga -->
> A set of icons located on the right side of the header, representing quick-access actions.
<!-- /dga -->

Navigation Header, `/guidelines/components/ui-shell/navigation-header`, Anatomy, Brand Logo:

<!-- dga -->
> The image on the left likely represents a company or website logo that helps to establish brand identity.
<!-- /dga -->

Note DGA's "likely": this describes the illustration, not a placement rule.

## 4 · In DGA's change log

`/updates/change-log`, version 1.0.0 (20 Feb 2025): Structured List and Pagination each
"Added RTL variant". Already captured verbatim in `2026-08-27-section-sweep.md`.

## 5 · In DGA's own components, not in guidance

The `dga-*` web components served in the same build (the package recorded as `@platformscode/core`
in `2026-10-19-live-demo-semantics.md`). This is what DGA's code does, not a rule DGA states.

- `dga-icon` mirrors an icon in RTL when its name contains `arrow` or `chevron`, unless
  `flip-rtl` is set to false; any other icon mirrors only when `flip-rtl` is set:
  `g=t?(t.includes("arrow")||t.includes("chevron"))&&e!==!1:!1,h=e||g` and
  `:host(.flip-rtl):host-context([dir='rtl']) .icon-inner{transform:scaleX(-1)}`.
- Pagination: `[dir=rtl] .pagination__arrow button{transform:rotate(180deg)}`.
- Date Picker: `[dir=rtl] .date-picker__navigator-buttons dga-button-v2{transform:rotate(180deg)}`,
  and the range highlight's rounded ends swap sides under `[dir=rtl]`.
- Carousel: an `isRTL()` check reverses which arrow moves to the next slide.

## Found in the text table but not displayed — not cited

- Layout and Spacing, Alignment → Object: *"…aligning text to the left for optimal visual
  balance."* The Alignment section does not render on the page.
- Home page and the seasonal templates, Hero / About / Services sections: *"…an image or an
  illustration on the left hand side."* The Home page template does not display it.

Also excluded: Figma instructions on `/designing` ("Assets tab on the left side of the screen"),
which describe Figma, not a product; Tooltip's Left and Right beak variants, which are variant
names; and the Arabic word `اتجاه` where it means "trend" or "orientation".
