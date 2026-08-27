# DGA version pin

What this kit was built against. A re-harvest updates this file, and the diff is the
changelog.

| | |
|---|---|
| **Source** | https://design.dga.gov.sa/ |
| **Version / last-updated as stated by the site** | Site Version 1.0 · design kits PC 1.0 |
| **Harvested on** | 2026-08-26 |
| **Method** | Live DOM extraction of CSS custom properties — values verbatim, not transcribed |
| **Corroborated by** | An independent extraction dated 2026-06-21 — 48/51 shared colour steps identical. See `harvest/CROSSREF-SECOND-EXTRACTION.md` in the dga-kit repository (not shipped with the installed skill) |
| **Verified by** | — *(designer sign-off gate — still outstanding)* |

## History

| Date | DGA version | What changed | Actioned by |
|---|---|---|---|
| 2026-08-26 | 1.0 / PC 1.0 | Initial harvest — 1,052 CSS custom properties | — |
| 2026-08-26 | 1.0 / PC 1.0 | Cross-checked against an independent extraction. 3 values disputed, carried as `$meta.$disputed` in `tokens.json` |
| 2026-08-27 | 1.0 / PC 1.0 | Harvested `hajj-template`, the last outstanding template. Template coverage now complete at 19 | — |

## Open at the next harvest

- `neutral.500` and `neutral.950` — one unit apart from the second extraction. No contrast impact.
- `info.50` — they read green (`#ecfdf3`) in June, we read blue (`#eff8ff`) in August. Confirm the
  page was corrected upstream.
