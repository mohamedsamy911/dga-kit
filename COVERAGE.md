# Coverage map

Every area of design.dga.gov.sa, and which skill owns it. One owner per area — no skill
duplicates another's rules, because rules live once in `dga-design-system/references/`.

## DGA source → owning skill

| DGA area | Pages | Extracted into | Owned by |
|---|---|---|---|
| Foundations — colour | 1 | `foundations.md`, `tokens.json`, `CONTRAST-AUDIT.md` | `dga-design-system` |
| Foundations — typography | 1 | `foundations.md` | `dga-design-system` |
| Foundations — layout & spacing | 1 | `foundations.md`, `tokens.json` | `dga-design-system` |
| Foundations — elevation | 1 | `foundations.md`, `tokens.json` | `dga-design-system` |
| Foundations — iconography | 1 | `foundations.md` | `dga-design-system` |
| Components | **50** | `components.md` | `dga-design-system` |
| Templates | **19** | `patterns.md` | `dga-design-system` |
| Accessibility (per-component + Accessibility Ease) | 51 | `accessibility.md` | `dga-a11y` |
| Design tokens (`/thoughts/designToken`) | 1 | `foundations.md` §Token architecture | `dga-tokens-sync` |
| Local & global standards | 1 | `foundations.md` §Compliance context | `dga-launch-gate` |
| Transparency mandate (About the Entity, e-Participation) | 2 | `patterns.md` | `dga-launch-gate` |
| Brand & identity (logos, seasonal, Saudi Font) | across templates | `brand.md` | `dga-brand-overlay` |
| Content & language | across templates | `content.md` | `dga-design-system` |
| RTL — DGA's own explicit statements | **`TODO(verify)`** | `rtl-rules.md` + citations | `dga-rtl-i18n` |
| Developer setup (`/developing`, install) | 2 | `official-packages.md` | `dga-react` |
| DGA rules expressed in a non-DGA UI library | — | `token-wiring.md`, `component-mapping.md` | `dga-ui-adapter` |
| Designer setup (`/designing`, Figma install) | 2 | `patterns.md`, `brand.md` | `dga-mockup` |
| Designing for mobile (`/designing-for-mobile`) | 1 | `mobile.md` | `dga-mockup` |
| Library migration (`/migration-guide`) | 1 | `library-migration.md` | `dga-tokens-sync` |
| **Assessment Criteria** (`/AssessmentCriteria`) | 1 | `assessment-criteria.md` | `dga-launch-gate` |
| Atomic design (`/thoughts/atomic-design`) | 1 | `foundations.md` §Atomic design | `dga-frontend-architect`, `dga-handoff` |
| Responsive design (`/thoughts/responsive-design`) | 1 | `foundations.md` §Responsive design | `dga-design-system` |
| Consistency & unified identity (`/thoughts/consistency-and-unified-identity`) | 1 | `brand.md` §Colour identity, §Typeface identity | `dga-brand-overlay` |
| Contributing (`/contributing`) | 1 | `foundations.md` §Contributing back to DGA | `dga-design-system` |
| Change log + roadmap (`/updates/*`) | 6 | `harvest/raw/2026-08-27-section-sweep.md` | `dga-tokens-sync` |

## Skill lanes — what each one alone does

| Skill | Owns | Explicitly does NOT |
|---|---|---|
| **dga-design-system** | The rules. Foundations, 50 components, 19 templates, content, tokens. Read by everything else. | Judge a design, write code, or run anything |
| **dga-design-review** | Auditing a *design* against DGA. Seven fixed passes, severity rubric, verdict. | Audit code, or produce designs |
| **dga-mockup** | *Producing* compliant screens from DGA templates, Arabic-first | Review its own output — that's design-review's job |
| **dga-handoff** | The design→dev seam. Component inventory, token map, state matrix, bilingual copy | Design or build |
| **dga-react** | Code, **when the project uses DGA's own `platformscode-new-react`** — the gap layer over it | Apply to a project on any other UI library; that is `dga-ui-adapter` |
| **dga-ui-adapter** | Code, **on every other UI library** — wiring DGA tokens into your theme, 50 component mappings, the build list | Teach you your own UI library |
| **dga-rtl-i18n** | Arabic-first mechanics. Mirroring, bidi, Arabic typography, Intl formats, next-intl | Component specs |
| **dga-a11y** | Auditing *running code* against DGA's per-component ARIA + WCAG 2.1 AA | Review static designs |
| **dga-launch-gate** | Everything beyond design: registration, transparency mandate, required pages, Open Data, measurement indicators | Design or accessibility detail |
| **dga-tokens-sync** | Re-harvesting tokens and diffing them | Anything at build time |
| **dga-brand-overlay** | One entity's overlay, and the project's open decisions (numerals, calendar, mirroring) | Override anything DGA fixes |

## Two code skills, one active at a time

`dga-react` and `dga-ui-adapter` never both apply. Which one depends on the project's UI library:

| Project uses | Use | Because |
|---|---|---|
| `platformscode-new-react` | `dga-react` | DGA's own 175 components are available as the reference implementation. The skill is the gap layer over them. |
| **Anything else** — Tailwind, MUI, Chakra, shadcn/Radix, Ant, Bootstrap, Vue/Angular kits, plain CSS | `dga-ui-adapter` | None of DGA's components are available, so every spec must be re-expressed and *"does this match DGA"* becomes a judgement rather than a diff. |

## Agents

| Agent | Lane | Writes files? |
|---|---|---|
| `dga-designer` | Problem framing → state matrix → copy → handoff | Yes |
| `dga-frontend-architect` | Structural decisions before code exists | **No** |
| `dga-frontend-dev` | Implementation from a spec | Yes |
| `dga-code-reviewer` | Correctness, security, DGA, WCAG AA | **No** |
| `dga-compliance-auditor` | Pre-launch go/no-go with evidence | **No** |
| `dga-content-writer` | Arabic-first bilingual interface copy | Yes |

## Eval suites

| Suite | Cases | Tests |
|---|---|---|
| `evals/dga-design-review/` | 11 | Detection vs restraint on design review |
| `evals/dga-ui-adapter/` | 12 | Detection, restraint, and **library confusion** — advice for the wrong library, or a component it does not have |

## The source contract

`harvest/source-inventory.json` is the map the freshness monitoring is built on: every
design.dga.gov.sa page this kit depends on, the reference file that owns it, and what a change
would invalidate. Rebuild it with:

```bash
python3 harvest/sources.py --baseline
```

Three measured facts about the site shape everything downstream, and each is recorded in the
file so nobody rebuilds a monitor on a false premise:

| Measured | Consequence |
|---|---|
| Every route returns the same 4,417-byte SPA shell with **HTTP 200 — including routes that do not exist** | HTTP status can never detect a removed or renamed page, and a per-route content hash is identical for every route. A monitor built on either is permanently green and proves nothing. |
| The shell links `/assets/index-<vite-hash>.css` | The filename carries the build hash, so it changes on every DGA deploy. Cheapest exact "DGA shipped something" signal, and the file holds the whole token surface. |
| `sitemap.xml` is fetchable but **stale** — 34 components and 16 templates against the real 50 and 19 | A lower-bound signal only. Never a count. Its template set is exactly the Sep 2024 release. |

So monitoring is two tiers, and every source carries which applies:

- **Tier A** — reachable by `curl`: stylesheet, sitemap, robots, shell. Cheap, run often.
- **Tier B** — needs a headless browser driving client-side navigation. Page text, nav route
  enumeration, the counts. Expensive, run on a Tier A signal or quarterly.

Tier B sources carry `contentHash: null` until a deep harvest fills it — honest missing data.
When that harvest lands it **may** write hashes, but only with provenance saying a browser
rendered the page:

```json
{ "contentHash": "…", "hashMethod": "browser-innertext" }
```

`evals/validate-fixtures.py` accepts `browser-innertext` and `browser-dom`, and fails a Tier B
hash carrying any other method or none — because the only thing `curl` can hash is the shell,
which is byte-identical for every route including ones that do not exist. A hash like that would
go green forever and prove nothing. The rule is provenance, not abstinence.

The suite also fails if a reference declares a DGA page the inventory does not track, so citing a
new page without adding it to the contract is caught rather than silently unmonitored. A route can
be exempted, but only as `route -> rationale` — a bare list would let a future exemption be added
with no justification, which is exactly how a dependency stops being monitored. An empty rationale
fails. The exemption map is currently empty.

The file also pins the **counts as a contract** (50 components, 19 templates, 5 foundations,
6 Thoughts) and a **critical-facts watch list** — the published version, the four Mandatory
assessment criteria, the unmatchable dark-theme selector, and `text.secondary`. Every one of
those is asserted against the file it protects, so a stale watch-list entry fails rather than
quietly pointing the sentinel at a value nothing depends on any more. One assertion fails if the
sitemap ever stops being stale.

`owns[]` is **machine-derived and machine-checked**, not curated. The eval suite scans every
provenance declaration in `skills/` — including the per-section `**Source:**` lines partway down
a file, which is where the hand-built map kept losing entries — and fails if a declared route's
inventory entry does not list the declaring file as an owner. Append-only records are excluded
and say so: `capture-log.md` logs what was captured and when, so a DGA change does not make it
wrong; `dga-version.md` *is* an owner, because a release means the pin itself must change.

The map covers more than the obvious owner per route —
a page can stale several references at once. `/guidelines/templates/*` alone owns `patterns.md`,
`brand.md`, `content.md` and `mobile.md`, and the six Thoughts articles are listed individually
because their dependants genuinely differ. Files derived from those references — the ui-adapter
mappings, the RTL rules — are deliberately **not** listed: rules live once in
`dga-design-system/references/`, so the chain runs through the owning reference, not around it.

## Freshness — the Tier A sentinel

```bash
python3 harvest/sources.py --check
```

Diffs the live site against the baselines in `source-inventory.json` and writes
[harvest/FRESHNESS.md](harvest/FRESHNESS.md). **It never updates the baseline** — a detected
change stays reported until a human accepts it with `--baseline`. The automation reports; it does
not decide.

### It is cheaper and sees more than the plan assumed

The SPA bundle is a static asset, and it **contains the route table** — all 50 component slugs,
19 templates, 5 foundations, 6 Thoughts, plus one route per published release. So the counts
contract and *"has DGA released?"* are answerable by `curl` after all. Only page **prose** needs
a browser.

The bundles are ~19 MB, too heavy to pull for nothing, so `--check` fetches the 4 KB shell first
and reads the Vite build hashes out of it. Unchanged hashes mean DGA has not deployed and there is
nothing a deep read could find, so it stops there — **about a second**. A deploy triggers the full
read, about five.

| What it detects | How |
|---|---|
| DGA deployed | Vite build hash on the CSS or JS asset |
| A new release | a new `version-history-*` route in the bundle |
| A route added, removed or renamed | route-set diff against the baseline |
| A count breaking the contract | live count vs `contracts` |
| `text.secondary` recoloured | resolved through its `var()` reference, both levels recorded |
| **The dark selector being fixed** | the highest-impact single change DGA could make |
| sitemap or robots edited | content hash, checked even on the cheap path |

### What it cannot see

Page prose. Every route returns the same shell, so a wording change with no rebuild is invisible
to Tier A — that is what the quarterly browser harvest is for. Route removal is read from the
bundle, so it also needs a deploy to surface. Both limits are printed in `FRESHNESS.md` rather
than left for someone to discover.

### Running on a schedule

| Workflow | Trigger | Does |
|---|---|---|
| `.github/workflows/dga-freshness.yml` | Mondays 06:00 UTC, or manual | Runs the sentinel, uploads `FRESHNESS.md`, opens **one rolling issue** when review is pending |
| `.github/workflows/ci.yml` | push + PR | The offline checks: fixtures, quote fidelity, contrast self-test, generated-file drift, installer, manifests |

Two properties of the sentinel workflow are load-bearing and asserted by the eval suite:

- **`permissions: contents: read`.** It cannot commit. A workflow able to write the repo could
  accept its own findings, which would silently close the review gate everything else defers to.
  `--baseline` is a human step, run locally, after the guidance has been updated.
- **Exit 1 is a result, not a failure.** The job stays green and the issue carries the signal;
  only exit >1 — a sentinel that could not complete — fails the build. Conflating the two either
  turns every real DGA change into a red build people learn to ignore, or hides a broken check
  behind an expected red.

The issue has a full lifecycle, not just an open:

| Sentinel | Workflow does |
|---|---|
| exit 1, no open issue | opens one, labelled `dga-freshness` |
| exit 1, issue already open | **comments** on it — a fresh issue every Monday for the same unread finding is how a queue stops being read |
| exit 0, issue open | **comments and closes** it: the baseline now matches, so the finding was accepted or reverted upstream |
| exit 0, no issue | nothing |

The close arm matters as much as the open one. Without it the issue stays open after a maintainer
accepts the baseline, and the next unrelated change is appended to an issue whose body describes
something already resolved — history that reads as still open.

## Tier B — the deep harvest

```bash
python3 harvest/deep.py --routes            # the 91 pages to visit
python3 harvest/deep.py --emit-js           # the extraction snippet
python3 harvest/deep.py --capture out.json  # process {route: innerText} from any driver
python3 harvest/deep.py --playwright        # drive it locally
```

Tier B is narrower than the plan assumed, because the bundle gave Tier A the route table and the
release list. What is left for a browser is page **prose** — a wording change that ships without
a rebuild is invisible to Tier A, and prose is what every reference file quotes.

**Extraction is separate from processing on purpose.** `deep.py` owns the contract — the JS, the
normalisation, the hashing, the diff — and not the browser. The driver is the least portable part
and the most likely to rot; the contract is what has to stay identical across drivers. A capture
taken by hand in devtools is processed by exactly the same code as an automated one.

> `--playwright` needs `pip install playwright && playwright install chromium`. It is **not**
> exercised by CI and was not run when it was written. `--capture` is the tested path — the
> snapshots in `harvest/snapshots/` were produced through it from a real browser session.

Three traps are encoded in the snippet, each hit for real during the harvests:

| Trap | What happens if you miss it |
|---|---|
| Deep links bounce to `/` | every page returns the home page |
| `querySelector('main')` is the **nav drawer** | every hash is the navigation, identical everywhere |
| Default locale is Arabic | half the corpus is the wrong language and every hash churns |

Snapshots live in `harvest/snapshots/` — machine-owned, overwritten each run, used only for
hashing and diffing. Deliberately **not** `harvest/raw/`: those are human-curated evidence with
`<!-- dga -->` fences marking DGA's own words, and auto-dumping page text into them would fill
the quote-fidelity corpus with unvetted noise. Promote a snapshot by hand, with fences, when you
need to cite it.

### The review gate applies here too

`--capture` **writes nothing** — no snapshot, no hash, no change in `skills/`. `--accept` is the
only thing that writes, and it is the Tier B equivalent of `sources.py --baseline`.

That ordering is load-bearing, not tidiness. A run that stored the new snapshot while reporting
the change would compare live against its own output next time, report *"unchanged"*, and the
diff nobody had read yet would be gone — the automation quietly accepting its own finding.

A **NEW** page is pending too, not merely unchanged: a page with no baseline has never been
reviewed, so a first harvest fails until someone accepts it rather than passing at exit 0.

| Status | Meaning | Exit |
|---|---|---|
| `unchanged` | matches the accepted snapshot | 0 |
| `NEW` | no baseline — never reviewed | 1 |
| `CHANGED` | differs; unified diff printed | 1 |
| `EMPTY` | the driver returned no text | **2** |
| `MISSING` | the driver never reported this route at all | **2** |

**A harvest with holes is a failed harvest, not a clean one.** `EMPTY` and `MISSING` refuse
`--accept` outright — not "accept the pages that came back". Recording a partial run as the
baseline would make the missing pages look unchanged forever, and a browser that died on forty
of ninety-one routes would report *"fifty-one unchanged"* and pass.

Every route the driver was asked for comes back in the result set, so a failure surfaces instead
of disappearing. `--capture` treats the file as the intended set (a deliberate subset is fine);
add `--all` to assert it covers every Tier B route.

Verified by behaviour in the eval suite, including the specific property the first version broke:
report twice, and the diff is identical both times.

## Testing the monitoring itself

```bash
python3 evals/test-automation.py
```

The rest of the suite checks the kit's **content** against DGA. This one checks the
**automation**: given a known change, does the sentinel report it, in the right words, without
quietly fixing anything? A monitor that has silently stopped working looks exactly like a monitor
with nothing to report, which is why this is not optional.

| # | Scenario | Asserted |
|---|---|---|
| 1 | a quiet week | reports nothing at all |
| 2 | a new DGA version | named in the finding, and ordered numerically past the ninth patch |
| 3 | a changed token | both old and new value; includes DGA fixing the dark selector |
| 4 | a template added, removed, **or renamed** | a rename must not net out to silence |
| 5 | a blocked source page | Tier A claims nothing it could not read; Tier B is `EMPTY`/`MISSING`, never clean |
| 6 | a contradiction | reported, and the **contract is not rewritten to match** |

Scenario 6 is the one with teeth. A live count disagreeing with the contract must stay a finding
for a human — a monitor that adopts the live value has stopped being a contract. The same
scenario also pins that the contradictions DGA publishes *about itself* stay recorded with both
sides: **33+ components** against 50 enumerable routes, and the roadmap dating releases a year
before the change log does. Neither is silently settled in favour of the number the kit prefers.

Making this testable required splitting `compare()` — pure, offline, no clock — out of
`sources.py --check`, which fetches. Every scenario had been an ad-hoc test during development,
run once by mutating the real baseline against the live site. Now they run every time.

Each detector was verified by **breaking it**: disabling the release check, the fact diff, the
route-set diff, or making `compare()` adopt the live count each fails exactly the scenarios that
name it, and nothing else.

## Guarding against our own drift

The monitoring in `dga-tokens-sync` watches **DGA** for changes. `evals/check-quote-fidelity.py`
watches **us** — it compares every DGA quote in `skills/` against the captured page text in
`harvest/raw/`, and fails on a paragraph that reproduces a capture without matching it.

That is the direction this repo has actually gone wrong: `-2%` shipped as invalid CSS, the
template count asserted as 19 when the harvest held 17, and a launch-gate quote that dropped
DGA's word *"typically"*. None of those would be caught by re-checking design.dga.gov.sa.

```bash
python3 evals/check-quote-fidelity.py --ci
```

It reports **blockquote coverage**: how many blockquote paragraphs in `skills/` could be matched
to a captured DGA passage. The figure is deliberately not repeated here — it moves whenever a
blockquote is added anywhere in `skills/`, and a copy of it in this file went stale within an hour
of being written. Run the command for the current number.

Read it for what it is. The denominator counts *every* blockquote, and most of those are the
kit's own commentary rather than DGA quotes, so the true share of *DGA quotes* that are evidenced
is higher — by an amount nothing currently measures. A real evidence-coverage figure needs DGA
quotes marked in `skills/` with the same `<!-- dga -->` fence the captures use — `TODO`.

Raising the numerator means capturing more pages, never editing a reference to match.

`evals/validate-fixtures.py` checks every value the cases assert against `tokens.json`. Run it
after any re-harvest: an eval asserting a stale value teaches the skill a false rule, which is
worse than having no eval.

**Any fabrication fails a suite outright**, regardless of detection score.

## Where a design is checked twice — on purpose

`dga-design-review` pass 6 checks accessibility *in the design*; `dga-a11y` checks it *in the
running code*; `dga-code-reviewer` checks what is visible *statically in the source*. Different
artefacts, different failure modes, same rules. That is the only intentional overlap.

## Known gaps — what this kit does NOT cover

Stated plainly so no skill implies coverage it lacks.

| Gap | Impact | Fix |
|---|---|---|
| **Digital Transformation Measurement Indicator** | `dga-launch-gate` §6 incomplete | Harvest — published outside design.dga.gov.sa |
| **Digital Experience Maturity Indicator** | same | same |
| **Assessment Criteria *checklist file*** | The scoring page is captured (`harvest/raw/2026-08-27-section-sweep.md`); the downloadable checklist is a separate file | `Download Checklist` on `/AssessmentCriteria` |
| **Responsive radius & spacing values** | Per-breakpoint tokens can't be resolved; treating them as constants is wrong on two of three breakpoints | PC 1.0 Foundations Figma variable collections |
| ~~**Dark theme values**~~ | **Closed 2026-08-27** — all **402** are in the public CSS bundle; the 67 text/background roles are in `tokens.json` as `role.dark` and audited by `check-contrast.mjs --theme dark`. 🚩 DGA's selector `[data-theme=dark] :root` can never match, so its dark theme is inert. **We do not ship it either** — see the row below | Remaining 340 non-role declarations are uncaptured in **both** themes — see `role.dark.$comment` |
| **Dark theme, shippable** | `tokens.css` deliberately emits **no** dark rule. Correcting DGA's selector would activate 1.05:1 pairings for anyone already using `data-theme="dark"`, and the five `*-light` status surfaces have no dark tint anywhere in DGA's output — so it cannot be made safe without inventing values | An entity that wants dark mode owns the remediation and records it in `dga-brand-overlay` |
| **Mobile UI Kit** (6 components) | Names confirmed from `/designing-for-mobile` 2026-08-27; **no specs** — that page is a Figma download landing page | Figma-only |
| **Arabic-language version of the site** | Arabic terminology for `content.md`. The toggle is reachable and renders; only the terminology harvest is outstanding | The `العربية` toggle |
| **Storybook** | Component demos | Marked "soon" by DGA — not available yet |
| **Designer sign-off** | Values are exact; the *interpretation* is unverified | A DGA-literate designer reads the references |

## Disputed and unverified claims

Recorded rather than quietly resolved, per the kit's own cite-or-omit rule.

| Claim | Status |
|---|---|
| **How many places DGA itself states an RTL rule.** This file previously said "6 references across the whole system". Nothing in the kit enumerates them, so the number cannot be checked from its own files, and a review of the derived skills named four (Quote, Steps, Buttons, Pagination). The 16 ⚠️ **RTL** callouts in `components.md` are the kit's *derived* guidance, which is a different count and must not be conflated with DGA's own statements. | **`TODO(verify)`** — settle by re-reading the live site and listing the pages. Until then no skill may cite a number. |
| Three colour values disputed against an independent extraction | Carried as `$meta.$disputed` in `tokens.json`; see `harvest/CROSSREF-SECOND-EXTRACTION.md` |
| **How many components DGA ships.** `/about-platforms-code` publishes a **33+** counter. `/guidelines/components/` enumerates **50** routes. | Recorded, not reconciled. This kit cites **50** — the enumerable count. The counter is stale marketing copy. |
| **When 1.0.0 and 1.0.2 shipped.** `/updates/roadmap` dates them Feb 2024 and Sep 2024; `/updates/change-log` dates the same versions 20 Feb **2025** and 1 Sep **2025**. | Cite the change log — the more specific record. |

## Where DGA itself is silent

No skill invents a rule here. Each says DGA is silent and names its fallback.

Numeral policy · Hijri calendar · Arabic body typeface · motion tokens (durations and easings —
though `prefers-reduced-motion` **is** required in three places) · terminology glossary ·
Arabic tone of voice · **Card accessibility** (DGA's section is Accordion's, pasted in) ·
**Menu accessibility** (no section exists at all) · Table ARIA roles · carousel pause control
(WCAG 2.1 AA 2.2.2 requires one — apply WCAG) · colour-blind-safe chart palettes · dark-mode
usage guidance · accessibility-statement page.

## Where DGA's own tokens fail WCAG

Not a gap in this kit — a fact about the source, and the reason `check-contrast.mjs` exists.
`text.secondary` (#dba102) is a DGA token **designated for text** that measures 2.30:1 on white
and fails AA at every size. Three `text.*-light` tokens are dark-surface only despite the naming.
Run `node skills/dga-design-system/assets/check-contrast.mjs` for the current list.
