# Changelog

Notable changes to dga-kit. Dates are when the work landed, not when DGA published.

The kit's rule is **cite or omit**: every rule carries a source URL and a retrieval date. So this
file records not only what was added, but what turned out to be **wrong** — a correction to a
claim is the more important entry, because someone may have shipped against it.

This project does not follow semantic versioning strictly. A minor bump means new coverage; a
patch means corrections. Nothing here is a DGA release — see
`skills/dga-design-system/dga-version.md` for the Platforms Code version this kit is pinned to
(currently **PC 1.0.3**, released 4 Nov 2025).

## 0.7.1 — 2026-08-30

Corrections and guards, no new DGA coverage. Every fix here closes a gap between what the kit
*said* and what it *shipped* — the failure direction this repo has actually had.

### Corrected — read these first

- **The token-count claim was an overclaim, by roughly 3.5×.** DGA declares **1,052** CSS
  custom properties on `:root`; `tokens.json` carries **303** values, plus **67** dark values
  held for audit only. The prose converted one number into the other — the `dga-ui-adapter`
  theme-wiring step told a developer every one of the 1,052 was already extracted and
  machine-readable, immediately above the table pointing at a file holding under a third of
  that. Corrected in README, both `plugin.json` manifests, `dga-ui-adapter`,
  `dga-design-system`, `dga-tokens-sync` and `foundations.md`. **Quote 1,052 as what was read
  and 303 as what is shipped.** The gap is aliases and per-component role vars resolving to
  values already carried, and it has **not** been reconciled var-by-var — that is now stated
  rather than implied.
- **COVERAGE.md's no-duplication claim was false.** It said rules live once, in
  `dga-design-system/references/`. The breakpoint bands, spacing scale and paragraph width are
  restated in `dga-design-review`, `dga-mockup` and `dga-ui-adapter` prose — deliberately, because
  a skill that sends you to another file for four numbers is a worse skill. They were consistent,
  but nothing checked them. The claim now names the exception and the guard.
- **The agents silently overrode your model choice.** Five of six pinned `model: opus`,
  documented nowhere, so a user who had chosen a cheaper model for their session was billed Opus
  rates on six agents without being told. **All pins removed** — the agents inherit the session
  model. The recommendation to run the two verdict-producing agents on the strongest available
  model is now stated in COVERAGE.md as advice, which is what it always should have been.

### Added — guards for the above

- `evals/validate-fixtures.py` gained a **token count contract**: `$meta.carriedValues` and
  `$meta.carriedDarkValues` are asserted to be the real leaf counts of `tokens.json`, every doc
  that sizes the token set must quote them, and no file may describe the 1,052 read as a count of
  tokens shipped.
- ...and a **restated-value guard**: breakpoint bands, spacing steps and the paragraph max-width
  are re-derived from `tokens.json` and compared against every markdown copy. Both scans skip
  fenced code blocks so documentation can quote the defect it describes.
- Every new guard is **mutation-tested** — change the value, confirm the run turns red, revert.
  The first breakpoint check listed the expected bands as literal regex alternatives, so a
  drifted `600-899` failed to match and the check went green on a real regression. It was
  decoration for one commit; the mutation test is why that did not ship.

### Added — the evals actually run now

- `evals/build-evals-json.py` generates `skills/<skill>/evals/evals.json` from the markdown cases,
  so all **23 cases** run under `claude plugin eval` instead of being scored by hand. The markdown
  stays the source a human reviews; the JSON is a build artefact, never hand-edited.
- Case files gained an optional `## grader` section, used in place of `## traps` where the traps
  section also carries maintainer history the grader should not read. Used once, on
  `dga-ui-adapter` case 12.
- Every generated case carries the kit's own bar as a final expectation: **a rule attributed to
  DGA that DGA does not publish fails the case**, whatever else the answer gets right.
- CI gate added: `python evals/build-evals-json.py --check`. A case added in markdown and not
  regenerated is now caught, rather than silently never run.

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
