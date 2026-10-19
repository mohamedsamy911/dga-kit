# Raw capture — DGA web accessibility guideline (DGA-1-2-4-203, issue 2.0)

**Source:** *Guideline For Web Accessibility of Digital Channels Content to Serve People with
Disabilities and the Elderly*, Digital Government Authority —
https://dga.gov.sa/sites/default/files/2024-05/Guideline%20For%20Web%20Accessibility%20of%20Digital%20Channels%20Content%20to%20Serve%20People%20with%20Disabilities%20and%20the%20Elderly-V2.0_0.pdf

**Retrieved:** 2026-10-19, downloaded by the owner in a browser (dga.gov.sa challenges automated
clients, so the kit does not fetch it). 173 pages, 4,297,152 bytes, sha256
`09757e3a0731f807f40cfede02ac2669d613875d6483d29b37103fe73cc15578`.

**Cover page:** Document Classification: Guideline · Document Type: Public · Issue No: 2.0 ·
Document No: DGA-1-2-4-203 · May 2024.

**Method:** text extracted with PyMuPDF; the PDF's line breaks are joined with single spaces and
page headers and numbers dropped. Nothing else is changed: the document's own typos ("are is",
"they are no adjacent") are kept. This is a DGA document, separate from design.dga.gov.sa; the
Platforms Code site states its own aim on `/guidelines/foundations/typography` (*"Our aim is to
comply with WCAG 2.1 AA accessibility standards."*), captured earlier.

## Introduction (p. 4)

<!-- dga -->
> DGA has released the second version of the 'Guidelines for Web Accessibility to Digital Content
> Channels for People with Disabilities and the Elderly' to comply with the accessibility and
> usability standards established by the World Wide Web Consortium (W3C) and the Web Content
> Accessibility Guidelines (WCAG). These guidelines are intended to be implemented on digital
> channels to enhance the overall understanding and approach towards meeting the internationally
> acceptable level of web accessibility.
<!-- /dga -->

## Scope and audience (p. 6)

<!-- dga -->
> This document covers Web Content Accessibility Guidelines (WCAG 2.2), and the success criteria
> for their application in addition to support government entities by providing digital content
> that is more accessible to all target audiences.
<!-- /dga -->

<!-- dga -->
> This guide targets all government entities and the private sector that develop or operate
> digital government-related activities, including user interface designers, website and
> application developers, digital content administrators, and product owners, to enable them to
> make web content accessible for a variety of beneficiaries, including people with disabilities
> and the elderly.
<!-- /dga -->

## Framework (p. 8)

<!-- dga -->
> To inform the target audience on assessing and enhancing web accessibility across digital
> channels, the framework below has been developed. The framework provides 4 steps on how to use
> this document to better understand web accessibility and align web content with the
> international industry standard of web accessibility (WCAG 2.2 level AA).
<!-- /dga -->

The framework graphic on the same page labels step 2 *"Learn Web Content Accessibility
Guidelines 2.3"*. WCAG 2.3 does not exist; the rest of the document says 2.2.

## WCAG 2.2 structure and levels (pp. 9–10)

<!-- dga -->
> The Web Content Accessibility Guidelines (WCAG 2.2) framework is based on 4 principles
> (perceivable, operable, understandable, and robust), which encompass a total of 13 guidelines
> and 86 success criteria, spanning 3 levels of compliance (Level A, Level AA, and Level AAA).
<!-- /dga -->

The levels table, read row by row (requirement, then the level's label):

<!-- dga -->
> Level A compliance requires that basic accessibility features are implemented to ensure that
> web content can be accessed by most people with disabilities. Level A: Essential
>
> Level AA compliance requires that more advanced accessibility features are implemented to
> ensure that web content can be accessed by a wider range of people with disabilities. Level AA:
> Recommended
>
> Level AAA compliance requires that the highest level of accessibility standards and features
> are implemented to ensure that web content can be accessed by the widest range of people with
> disabilities, including those with very specific accessibility requirements. Level AAA: Optimal
<!-- /dga -->

The per-principle tables (pp. 16, 59, 113, 153) list 86 criteria. They omit 4.1.1 Parsing,
which WCAG 2.2 made obsolete, and assign the same levels WCAG 2.2 does — including the criteria
new in 2.2 below.

## The criteria new in WCAG 2.2 at Level A or AA

Each page opens with a one-sentence description. Levels are from the per-principle tables.

<!-- dga -->
> 2.4.11 Success criterion: Focus Not Obscured (Minimum) This success criterion requires that a
> partial part of the UI/UX element is focused and visible when the beneficiary is using a
> keyboard to navigate through the content of the webpage.
<!-- /dga -->

<!-- dga -->
> 2.5.7 Success Criterion: Dragging Movement This success criterion requires providing a
> beneficiary with a pointer alternative instead of dragging movements for actions that require
> dragging items across a webpage.
<!-- /dga -->

<!-- dga -->
> 2.5.8 Success criterion: Target Size (Minimum) This success criterion requires that interactive
> elements (such as buttons or links) have a sufficient size and/or spacing size, to ensure that
> they are no adjacent interactive element is selected instead of the intended element. Examples
> • Target size of pointer inputs is at least 24x24 CSS pixels (i. e UI elements such as buttons
> must be 24x24 CSS). o E.g., Three buttons are next to each other, each having a dimension of
> 24x24 CSS pixels. Here no additional space is required.
<!-- /dga -->

<!-- dga -->
> Nonconforming Content • Links within a paragraph • If the targets size of the pointer inputs is
> less than 24x24 CSS pixels, a sufficient spacing of at least 24 CSS diameter circle should be
> between each interactive element. • If more than one target, which performs the same function,
> is available, then only one of the pointer inputs needs to have a minimum size of 24x24 CSS and
> enough space around it. • If the target size is by default and cannot be altered by the product
> owner. • If a target is important and should legally be mandated for conveying the information.
<!-- /dga -->

The 2.5.8 page files WCAG's exceptions (spacing, inline links, an equivalent control, user-agent
default, essential) under the heading *"Nonconforming Content"*, which the document defines on
p. 15 as content that *"will not be assessed against the success criterion"*. Read them as the
exceptions they are; the example sentence *"buttons must be 24x24 CSS"* does not override the
spacing exception listed below it.

<!-- dga -->
> 3.2.6 Success criterion: Consistent Help This success criterion requires that any help
> mechanism such as (phone number, email or social media etc.) are is in a consistent location
> across multiple webpages within a website or application.
<!-- /dga -->

<!-- dga -->
> 3.3.7 Success criterion: Redundant Entry This success criterion requires that website content
> enables access to previously entered information and/or data by the beneficiary , this is to
> ensure that the beneficiary doesn’t have to enter the same information multiple times when
> completing a process (e.g. filling a form or survey or completing a payment task.)
<!-- /dga -->

<!-- dga -->
> 3.3.8 Success criterion: Accessible Authentication (Minimum) This success criterion requires
> that any login authentication method relying on memory, transcription or problem-solving should
> include at least one alternative non-cognitive function test used for authentication purposes.
<!-- /dga -->

Levels in the tables: 2.4.11, 2.5.7, 2.5.8 and 3.3.8 are AA; 3.2.6 and 3.3.7 are A.

## What this capture does not settle

- The levels table labels AA **"Recommended"**, while p. 8 aligns the framework with *"WCAG 2.2
  level AA"*. The document does not say AA is mandatory. A later DGA report (the Digital
  Experience Maturity Index 2026, captured separately) recommends WCAG *"with a compliance level of
  no less than "AA""*. Neither is a statement that AA conformance is a launch condition.
- The Platforms Code site still says WCAG **2.1** AA. Which version DGA's design assessment uses is
  not stated in either source.
