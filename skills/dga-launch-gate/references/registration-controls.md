# DGA regulatory controls — registering platforms and domains (DGA-1-2-2-106)

> ⚠️ **DGA regulatory controls, not design guidance.** This file comes from DGA's *ضوابط تسجيل
> وإدارة النطاقات والمنصات والخدمات الحكومية الرقمية* (version 2.0, September 2026), not from
> design.dga.gov.sa. The document defines a control (ضابط) as a requirement government entities
> must comply with. Most of its 92 numbered controls are administrative — forms, approvals, fees,
> domain classes — and invisible in a platform's UI. Only the ones a launch review can act on are
> listed. Report them **separately** from the design findings.

**Source:**
https://dga.gov.sa/sites/default/files/2026-10/V2.0-%D8%B6%D9%88%D8%A7%D8%A8%D8%B7%20%D8%AA%D8%B3%D8%AC%D9%8A%D9%84%20%D9%88%D8%A7%D9%95%D8%AF%D8%A7%D8%B1%D8%A9%20%D8%A7%D9%84%D9%86%D8%B7%D8%A7%D9%82%D8%A7%D8%AA%20%D9%88%D8%A7%D9%84%D9%85%D9%86%D8%B5%D8%A7%D8%AA%20%D9%88%D8%A7%D9%84%D8%AE%D8%AF%D9%85%D8%A7%D8%AA%20%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A%D8%A9%20%D8%A7%D9%84%D8%B1%D9%82%D9%85%D9%8A%D8%A9.pdf
· Arabic only ·
**Retrieved:** 2026-10-19 · sha256 `44b5e003…4251`. The Arabic text is the authority; the English
here is the kit's summary. Verbatim capture:
[the raw capture](https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-19-registration-controls.md).

## The control that makes the Platforms Code apply

<!-- dga -->
> 2-106-12 تلتزم الجهة الحكومية بتطبيق نظام التصميم الموحد (كود المنصات) في جميع المنصات والتطبيقات والمواقع الإلكترونية التابعة للجهة، سواءً الجديدة أو المسجلة مسبقًا لدى الهيئة.
<!-- /dga -->

The government entity applies the Unified Design System (the Platforms Code) on **all** its
platforms, applications and websites, new or already registered with DGA. This is the citation for
*why* a government platform follows the Platforms Code; design.dga.gov.sa itself says how.

## What a launch review can check

| Control | Kit's summary of the Arabic | What to look for |
|---|---|---|
| **Circular 5589** (preface) | DGA's approval is needed **before launching any new digital platform** | Approval exists before go-live |
| **2-106-09** | Platform data and documents go to DGA through the **"تسجيل منصة جديدة"** service on the **"رقمي"** platform, and the entity obtains a **registration certificate** | Certificate number on file |
| Definition, **شهادة تسجيل** | Granted **before development of a new platform begins**; it counts as approval to launch, provided the platform keeps to what was declared and to DGA's standards and controls | Certificate predates the build, or the team knows it does not |
| Definition, **تسجيل المنصة الرقمية** | Registering a platform **does not mean DGA approves it**; it means the data was submitted | Do not report "registered" as "approved" |
| **2-106-30** | The entity is registered with DGA and the **Digital Stamp** is issued | Stamp issued, and shown — see below |
| Definition, **الختم الرقمي** | An electronic certificate that **must be displayed** on digital channels, per DGA's data and template | Stamp present on the platform |
| **2-106-41** | DGA approval **before launching new services**, or modifying registered ones, on a registered platform | Each new or modified service in this release has its own approval |
| **2-106-38** | Platform and service data registered with DGA is reviewed and updated **quarterly** | Owner named for the quarterly update |
| **2-106-25 / 2-106-37** | Seasonal platforms **launch** on a subdomain, never a separate main domain (2-106-25); internal platforms are **registered** on a subdomain branching from the entity's main government domain, never a separate main domain (2-106-37) | Domain matches the platform type |
| **2-106-22** | A seasonal platform closes within **90 days** after its event; DGA may exempt some | Closure date planned |
| **2-106-79** | The registration certificate comes **before reserving the domain** when the domain is for a platform or website | Order of steps |
| **2-106-72** | **IPv6** adopted and **DNSSEC** enabled, to protect government domains | Check DNS and network config |
| **2-106-73** | The **servers hosting the entity's domains** are inside Saudi Arabia | Hosting location of the domain's servers |
| **2-106-87.05 / .06** | DGA **may suspend** a platform's domain if it does not comply with DGA's standards, requirements or policies — and may suspend the **main** domain even when the offending platform is a subdomain | The consequence, quoted with its "may" |

> 🚩 **2-106-73 is about the servers that host the entity's *domains*.** It does not say every
> application server, CDN or third-party service must sit in the Kingdom. Do not widen it; data
> residency for other systems is a question for the entity's own policies and other regulators.

> 🚩 **Keep "may".** 2-106-87 opens *«يحق للهيئة»* — DGA has the right to suspend. It is a
> power, not an automatic outcome. Report a gap as *"DGA's controls allow suspension"*, never as
> *"the domain will be suspended"*.

## Domain classes

The document's domain classification (2-106-55, 2-106-58) matches the table on DGA's Digital
Stamp page, already in `../../dga-design-system/references/components.md`: `gov.sa`
(ministries, authorities, public institutions, councils, national centres; second-level
branches for their sub-entities), `edu.sa`, `org.sa`, `sch.sa`, `med.sa`, and `.sa` for
revenue-sharing platforms, activities, initiatives and programmes after DGA approves the name.

## What this file does not cover

The application forms, fee approvals (2-106-16 to 2-106-19), national-platform feasibility
studies, domain naming rules, deletion, suspension procedure and ownership transfer. They are in
the source document; none is checkable on a platform.
