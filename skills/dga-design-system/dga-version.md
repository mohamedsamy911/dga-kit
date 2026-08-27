# DGA version pin

What this kit was built against. A re-harvest updates this file, and the diff is the
changelog.

| | |
|---|---|
| **Source** | https://design.dga.gov.sa/ |
| **Published version** | **1.0.3**, released **4 Nov 2025** — per `/updates/change-log`, read 2026-08-27 |
| **Why other numbers appear** | The nav badge and footer read `Version 1.0`; the Figma downloads are named `PC 1.0 Foundations`, `PC 1.0 Components – Desktop UI Kit` and so on. Those are site chrome and **file names**. They are not the version and must not be cited as one. |
| **Does the harvest predate it?** | No. The 2026-08-26 extraction postdates 1.0.3 by nine months, so token values are current. |
| **Harvested on** | 2026-08-26 |
| **Method** | Live DOM extraction of CSS custom properties — values verbatim, not transcribed |
| **Corroborated by** | An independent extraction dated 2026-06-21 — 48/51 shared colour steps identical. See `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/CROSSREF-SECOND-EXTRACTION.md` in the dga-kit repository (not shipped with the installed skill) |
| **Verified by** | — *(designer sign-off gate — still outstanding)* |

## History

| Date | DGA version | What changed | Actioned by |
|---|---|---|---|
| 2026-08-26 | 1.0.3 | Initial harvest — 1,052 CSS custom properties. *(Recorded at the time as "1.0 / PC 1.0" — the version was not established until 2026-08-27.)* | — |
| 2026-08-26 | 1.0.3 | Cross-checked against an independent extraction. 3 values disputed, carried as `$meta.$disputed` in `tokens.json` |
| 2026-08-27 | 1.0.3 | Harvested `hajj-template` |
| 2026-08-27 | **1.0.3** | Route-table sweep. Harvested `rating-section` (templates genuinely complete at 19 — the previous "19" miscounted two sections as templates), `/designing-for-mobile`, `/contributing`, the three missing Thoughts articles, `/AssessmentCriteria`, `/about-platforms-code`, `/support`, `/updates/*`. **Version pin corrected: the published version is 1.0.3, released 4 Nov 2025**, not a bare 1.0. The 2026-08-26 token harvest postdates it, so token values are current. | — |

## Open at the next harvest

- `neutral.500` and `neutral.950` — one unit apart from the second extraction. No contrast impact.
- `info.50` — they read green (`#ecfdf3`) in June, we read blue (`#eff8ff`) in August. Confirm the
  page was corrected upstream.
