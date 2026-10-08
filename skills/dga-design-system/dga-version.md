# DGA version pin

What this kit was built against. A re-harvest updates this file, and the diff is the
changelog.

| | |
|---|---|
| **Source** | https://design.dga.gov.sa/ |
| **Published version** | **4.0.0** — per `/updates/change-log`, read 2026-10-08. DGA publishes **no release date** for it. |
| **Why other numbers appear** | DGA **renumbered its release history** in 2026: on 2026-08-27 the change log listed 1.0.0–1.0.3 with dates, on 2026-10-08 it lists eighteen undated releases, 1.0.0–4.0.0, and nothing maps one numbering to the other. The nav badge now reads `Version 4.0` (it read `Version 1.0` against 1.0.3, so it is chrome, not a source). The Figma downloads are still named `PC 1.0 …` — **file names**. Cite only the change log. |
| **Are the token values current?** | Re-checked rather than inferred from dates: on 2026-10-08 every colour value in `tokens.json` was still declared in the live stylesheet (build `CYyqM6kT`), and the full reconciliation of DGA's 1,126 custom properties reproduced unchanged. |
| **Harvested on** | 2026-08-26 · re-harvested 2026-10-08 (DGA update) |
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
| 2026-10-08 | **4.0.0** | **DGA update.** Change log renumbered (18 releases, no dates; the 1.0.x rows above are the old numbering). Harvested **National Day 96** and **Life Journeys**; National Day 95 left DGA's nav but is still served, so **21 templates** are routed. `/contributing` rewritten. Tokens, typography and iconography unchanged. The changelog's *"AI section"* was not found on any page. Evidence: `https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/raw/2026-10-08-dga-update.md` in the dga-kit repository (not shipped with the installed skill). | — |

## Open at the next harvest

- `neutral.500` and `neutral.950` — one unit apart from the second extraction. No contrast impact.
- `info.50` — they read green (`#ecfdf3`) in June, we read blue (`#eff8ff`) in August. Confirm the
  page was corrected upstream.
