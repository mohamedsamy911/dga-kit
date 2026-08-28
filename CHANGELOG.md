# Changelog

Notable changes to dga-kit. Dates are when the work landed, not when DGA published.

The kit's rule is **cite or omit**: every rule carries a source URL and a retrieval date. So this
file records not only what was added, but what turned out to be **wrong** — a correction to a
claim is the more important entry, because someone may have shipped against it.

This project does not follow semantic versioning strictly. A minor bump means new coverage; a
patch means corrections. Nothing here is a DGA release — see
`skills/dga-design-system/dga-version.md` for the Platforms Code version this kit is pinned to
(currently **PC 1.0.3**, released 4 Nov 2025).

## 0.7.0 — 2026-08-28

The first release since 0.6.0, covering 14 commits. It is a **minor** bump under the policy above:
new coverage (the Assessment Criteria, freshness monitoring, a verified Codex install path) landed
alongside corrections. Several corrections retract claims 0.6.0 shipped — read *Corrected* first
if you installed that version.

### Corrected — read these first

- **Dark theme is published, not Figma-only.** The kit said DGA published dark values only in the
  PC 1.0 Figma collections. False: DGA ships **402 dark declarations** in its public CSS, under
  `[data-theme=dark] :root` — a selector that can never match, because `:root` is `<html>` and a
  descendant combinator needs an ancestor it does not have. Verified live: zero elements matched.
  The values are carried in `tokens.json` under `role.dark` for **audit only** and deliberately
  never generated into `tokens.css`; five `*-light` status surfaces have no dark tint at all, so
  white text on them measures **1.05:1**.
- **WCAG 2.5.5 is Level AAA, not AA.** `foundations.md` cited the 44×44px target as "WCAG 2.1 AA
  2.5.5". The AA target-size criterion (2.5.8, 24×24px) is WCAG **2.2**. DGA states 44×44px
  itself on `/guidelines/foundations/layout-and-spacing`, so cite DGA, which is stricter than
  either.
- **`/designing-for-mobile` was harvested** (2026-08-27). `mobile.md` claimed it was outstanding,
  contradicting the capture log. That note has now been wrong in both directions.
- **The launch gate can no longer issue a PASS.** With the two Measurement Indicators uncaptured,
  the permitted verdicts are FAIL or **INCOMPLETE**. A PASS would be an unearned go-live approval
  carrying this kit's name.
- **A Hijri date wrapper is not a DGA requirement.** DGA states no calendar policy and its own
  demos are Gregorian. It sat on a compliance-ordered build list.
- **A language toggle is conditional, not universal.** DGA's rule is: *given* two languages, use a
  direct toggle. It does not require every platform to be bilingual.
- **The RTL count is unverified.** "Exactly six places" contradicted the kit's own reference,
  which says not to cite a total. The enumeration stays; the number is gone.
- **`--ci` on the contrast checker cannot go green** on stock DGA tokens, and README and
  INSTALL.md both recommended it as a build gate. It reports **20** failures by default (5 light,
  15 dark), not five. Commit `--json` as an artefact; gate on a grep over your own source.
- **SECURITY.md claimed no network calls and no dependencies.** Both false once the freshness
  tooling landed: it fetches DGA, and `--playwright` pulls Chromium.
- **`.claude-plugin/plugin.json` said "compliance"** with no unofficial/non-certification caveat,
  while the other two manifests carried one. It is the description shown in the install prompt.

### Added

- **A verified Codex install path.** `.agents/plugins/marketplace.json` — the catalogue
  `codex plugin add` installs from; a plugin manifest alone is not installable. Established from
  Codex's own `plugin-creator` system skill (`~/.codex/skills/.system/plugin-creator/`), whose
  `validate_plugin.py` this repo's `.codex-plugin/plugin.json` **passes**. The docs previously
  said "no verified Codex install path" — honest when written, since the specification had not
  been located, and wrong once it was. `"skills": "./skills/"` is confirmed correct against four
  independent sources.

- **Assessment Criteria** (`/AssessmentCriteria`, captured 2026-08-27) — the rubric a platform is
  actually scored against, closing the kit's longest-standing documented gap. DGA's hedge is
  preserved verbatim: a project failing the mandatory criteria *"typically* cannot proceed to
  deployment".
- **Freshness monitoring**, review-gated throughout. `harvest/sources.py --check` diffs the live
  site against a recorded baseline — build hashes, the route table and release list read out of
  DGA's own JS bundle, `text.secondary`, the dark selector, sitemap and robots. `harvest/deep.py`
  adds browser-captured page text. Nothing accepts its own findings: `compare()` writes nothing,
  the deep harvest needs an explicit `--accept`, and the weekly Action has `contents: read`.
- **`evals/test-automation.py`** — scenario tests for the monitoring itself, because a monitor
  that has silently stopped working looks exactly like a quiet week.
- **`evals/check-quote-fidelity.py`** — compares the DGA quotes a capture covers against that
  captured page text. Found two real defects on its first run. Now also reports **DGA-marked coverage**:
  blockquotes fenced as DGA's words, and which of them no capture backs.
- **Cross-platform CI** — the installers now run on macOS, Linux and Windows. `install-skills.ps1`
  had never been executed by CI at all.
- **A Tailwind smoke test** — the generated preset is compiled by the real Tailwind and asserted
  to emit DGA values.

### Security

- **Path traversal in the deep harvest.** `slug_for()` replaced only `/`, a POSIX assumption; on
  Windows a capture key like `/x\..\..\evil` escaped `harvest/snapshots/`. Capture files are
  untrusted input. Now sanitised, with a containment check at the write site.
- **Poisoned baselines.** `--baseline` accepted any HTTP 200 as the site. A maintenance page, or a
  valid cached shell in front of a proxy answering the asset requests with a login page, wrote a
  baseline with real-looking build hashes beside zero tokens and zero routes — after which every
  check compared that emptiness against itself and reported a quiet week forever. Both the shell
  and the two assets are now validated for status and content.
- **`--baseline` erased accepted Tier-B hashes**, discarding review state a human had signed off.
- **GitHub Actions pinned to commit SHAs** rather than mutable tags.
- **`xargs -r` removed** from `install-skills.sh` — a GNU extension that BSD xargs rejects, so both
  cross-reference checks would have failed on macOS, the platform the script advertises.

### Known gaps

- The two **Measurement Indicators** are published outside `design.dga.gov.sa` and are uncaptured.
- **Designer sign-off** outstanding: token values are exact, their interpretation is unverified.
- **Figma-only**: responsive radius/spacing, and the six mobile component specs.
- **Codex installs the 11 skills; the 6 agents are Claude Code only.** Codex's plugin contract
  has no `agents` field. Converting them to Codex's TOML agent format is unstarted.
- **`interface.capabilities` is `["Skills"]`, unattested.** Schema-valid, but no local
  enumeration says what Codex does with a given capability label.
- **Quote coverage**: only 2 DGA pages are captured, so 78 of 92 blockquotes cannot be checked
  against a source. Raising this needs a capture run, never an edit to a reference.

## 0.6.0

Released with the PC 1.0.3 documentation updates. See the git history for detail — this changelog
begins here.
