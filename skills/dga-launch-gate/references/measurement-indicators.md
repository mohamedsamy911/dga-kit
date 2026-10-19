# DGA's two measurement regimes — what they are, and why this kit cannot score them

**Sources:** DGA's public reports, downloaded 2026-10-19 —
*Digital Experience Maturity Index for Government Services – General Report 2026* (August 2026)
and *قياس التحول الرقمي 2025* (executive report, 6 November 2025). Raw capture with URLs and
hashes:
[the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-measurement-indicators.md).

Both are **periodic measurements**, not a launch check. Neither public report lists its
item-level criteria, so this kit names them and stops there.

## Digital Experience Maturity Index (DXMI) — مؤشر نضج التجربة الرقمية

<!-- dga -->
> The Digital Experience Maturity Index (DXMI) is an annual index designed to measure the maturity
> of digital government platforms and services based on several key perspectives and themes.
<!-- /dga -->

- **Who is assessed:** a selected set — *"(59) high-priority digital platforms"* in 2026. A new
  platform is not automatically in it.
- **Structure:** four perspectives, 20 themes. Beneficiary Satisfaction **25%** (CSAT survey) ·
  User Experience **50%** (expert assessment, field visits) · Complaints-Handling **15%** ·
  Technologies & Tools **10%**. User Experience's themes include Usability, Availability and
  Compatibility, and **Accessibility (For People with Disabilities and the Elderly)**.
- **Levels:** Emergent · Developed · Competent · Advanced · Exceptional. No percentage bands are
  published.
- **The criteria are not public:** *"the detailed reports for the platforms included in this cycle
  were completed and shared with the owning entities of the platforms."*

### DXMI recommendations — DGA advisory, not scored controls

The report's 14 recommendations are addressed to entities that own platforms. They are DGA's
advice for the next cycle, not launch conditions. Four bear on the interface; report a miss as
*"does not follow DXMI 2026 recommendation N"*:

| # | Recommendation, in short | Kit check |
|---|---|---|
| 3 | Login point clear and independent in the main navigation; fewer redirects and pop-ups; Nafath a primary option *"whenever applicable"* | `dga-design-review` |
| 4 | Accessibility built into the platform, *"dispensing with unstable floating external accessibility add-ons (Accessibility Overlays)"* | `dga-a11y` |
| 5 | Search: tolerant matching, advanced filtering, highlighted matches not shown by colour alone, **result count announced via `aria-live`** | `dga-a11y`, `dga-design-review` |
| 7 | WCAG *"with a compliance level of no less than "AA""*, accessible CAPTCHA alternatives including audio, testing with persons with disabilities and seniors | `dga-a11y` |

> 🚩 **Overlays versus Accessibility Tools.** DGA's footer anatomy includes **Accessibility
> Tools** (font size, contrast). DXMI recommendation 4 is about **external, floating overlay
> add-ons**. They are compatible: build the tools into the platform; do not bolt on a third-party
> overlay to provide them.

## Digital Transformation Measurement (Qiyas) — قياس التحول الرقمي

- **Who is assessed:** the **government entity**, not a platform — 240 entities in 2025.
- **Structure:** 10 perspectives, 23 axes, **95 criteria**, answered with evidence in DGA's
  measurement system and verified by DGA. One perspective is beneficiary centricity (participation
  and beneficiary experience); another is channels and digital services.
- **Per criterion:** full compliance (all requirements met), partial (one missed), none (two or
  more missed).
- **The 95 criteria are not in the report.** Entities answer them inside DGA's measurement system.

The report's Arabic text extracts in reversed order, so the kit does not quote it; the figures
above are the kit's reading of pages 4, 7 and 8.

## What this means for a launch verdict

A platform team cannot score either regime from the outside, and both run on DGA's measurement
cycles rather than at a platform's launch. The launch gate therefore records them as **not
assessed by this kit** and asks the entity for its latest detailed DXMI report (if the platform
is one of those assessed) and its Qiyas results. It does not convert an unknown into a pass.
