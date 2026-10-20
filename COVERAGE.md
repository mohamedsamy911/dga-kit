# Coverage map

Every area of design.dga.gov.sa, and which skill owns it. One owner per area: normative rules
live once, in `dga-design-system/references/`, and every other skill cites rather than restates.

**One documented exception.** A handful of values are used on literally every screen — the four
breakpoint bands, the named spacing scale, the container and paragraph widths — and sending a
reviewer to another file for four numbers makes a worse skill. Those are restated in
`dga-design-review`, `dga-mockup` and `dga-ui-adapter` prose **on purpose**. The duplication is
deliberate; going unguarded was not, so `evals/validate-fixtures.py` now re-derives each restated
figure from `tokens.json` and fails on any copy that drifts. Prose is what the model actually
reads, so a stale copy outranks the correct token — see
[Guarding against our own drift](#guarding-against-our-own-drift). **Nothing else is duplicated:**
add a rule to `references/` and cite it.

## DGA source → owning skill

> **Evidence, 2026-10-18.** After DGA's 2026 update (re-harvested 2026-10-08), the full English
> text of every component, template and guidance page — taken verbatim from DGA's live bundle —
> was compared with the kit by two independent reviewers, and every resulting change was confirmed
> on the rendered page (`harvest/raw/2026-10-18-reread.md`). DGA's text table also holds strings
> its pages never display; those were not used. Those passages could not see the code samples,
> which live outside that table. All 50 component Code tabs were read on 2026-10-19 instead
> (`harvest/raw/2026-10-19-code-samples.md`). The live demos' rendered semantics were inspected the
> same day (`harvest/raw/2026-10-19-live-demo-semantics.md`); their visuals are still not compared.

| DGA area | Pages | Extracted into | Owned by |
|---|---|---|---|
| Foundations — colour | 1 | `foundations.md`, `tokens.json`, `CONTRAST-AUDIT.md` | `dga-design-system` |
| Foundations — typography | 1 | `foundations.md` | `dga-design-system` |
| Foundations — layout & spacing | 1 | `foundations.md`, `tokens.json` | `dga-design-system` |
| Foundations — elevation | 1 | `foundations.md`, `tokens.json` | `dga-design-system` |
| Foundations — iconography | 1 | `foundations.md` | `dga-design-system` |
| Components | **50** | `components.md` | `dga-design-system` |
| Templates | **21** routed (20 in DGA's nav; National Day 95 left it 2026-10-08) | `patterns.md` | `dga-design-system` |
| Accessibility (per-component + Accessibility Ease) | 51 | `accessibility.md` | `dga-a11y` |
| Design tokens (`/thoughts/designToken`) | 1 | `foundations.md` §Token architecture | `dga-tokens-sync` |
| Local & global standards | 1 | `foundations.md` §Compliance context | `dga-launch-gate` |
| Transparency mandate (About the Entity, e-Participation) | 2 | `patterns.md` | `dga-launch-gate` |
| Brand & identity (logos, seasonal, Saudi Font) | across templates | `brand.md` | `dga-brand-overlay` |
| Content & language | across templates | `content.md` | `dga-design-system` |
| RTL — where DGA's guidance names a direction | Explicit: Quote, Steps, Buttons. Written RTL-first: Search, FAQs and Sitemap templates. Enumerated 2026-10-19 | `dga-rtl-i18n/SKILL.md`, `components.md`, `patterns.md` | `dga-rtl-i18n` |
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
| **dga-design-system** | The rules. Foundations, 50 components, 21 templates, content, tokens. Read by everything else. | Judge a design, write code, or run anything |
| **dga-design-review** | Auditing a *design* against DGA. Seven fixed passes, severity rubric, verdict. | Audit code, or produce designs |
| **dga-mockup** | *Producing* compliant screens from DGA templates, Arabic-first | Review its own output — that's design-review's job |
| **dga-handoff** | The design→dev seam. Component inventory, token map, state matrix, bilingual copy | Design or build |
| **dga-react** | Code, **when the project uses DGA's own `platformscode-new-react`** — the gap layer over it | Apply to a project on any other UI library; that is `dga-ui-adapter` |
| **dga-ui-adapter** | Code, **on every other UI library** — wiring DGA tokens into your theme, 50 component mappings, the build list | Teach you your own UI library |
| **dga-rtl-i18n** | Arabic-first mechanics. Mirroring, bidi, Arabic typography, Intl formats, next-intl | Component specs |
| **dga-a11y** | Auditing *running code* against DGA's per-component ARIA + WCAG 2.2 AA | Review static designs |
| **dga-launch-gate** | Everything beyond design: registration, transparency mandate, required pages, Open Data, measurement indicators | Design or accessibility detail |
| **dga-tokens-sync** | Re-harvesting tokens and diffing them | Anything at build time |
| **dga-brand-overlay** | One entity's overlay, and the project's open decisions (numerals, calendar, mirroring) | Override anything DGA fixes |

## Two code skills, one active at a time

`dga-react` and `dga-ui-adapter` never both apply. Which one depends on the project's UI library:

| Project uses | Use | Because |
|---|---|---|
| `platformscode-new-react` | `dga-react` | DGA's own **123** components are available as the reference implementation. The skill is the gap layer over them. |
| **Anything else** — Tailwind, MUI, Chakra, shadcn/Radix, Ant, Bootstrap, Vue/Angular kits, plain CSS | `dga-ui-adapter` | None of DGA's components are available, so every spec must be re-expressed and *"does this match DGA"* becomes a judgement rather than a diff. |

## Agents

The six roles ship as Claude Markdown in `agents/` and generated Codex TOML in `codex-agents/`.
The Codex skills plugin does not register agents: run the
[separate installer](INSTALL.md#install-the-six-codex-agents-separately). Generation preserves
each role's body and adds only Codex skill lookup instructions and read-only sandbox defaults
for the three non-writing roles. No new DGA coverage is implied by the second format.

| Agent | Lane | Writes files? |
|---|---|---|
| `dga-designer` | Problem framing → state matrix → copy → handoff | Yes |
| `dga-frontend-architect` | Structural decisions before code exists | **No** |
| `dga-frontend-dev` | Implementation from a spec | Yes |
| `dga-code-reviewer` | Correctness, security, DGA, WCAG AA | **No** |
| `dga-compliance-auditor` | Pre-launch go/no-go with evidence | **No** |
| `dga-content-writer` | Arabic-first bilingual interface copy | Yes |

## Which model the agents run on

**None of the six pins a model.** They inherit whatever the session is set to, which is your
choice to make and not this kit's — an earlier version pinned `model: opus` on five of them,
which silently overrode a user who had deliberately selected a cheaper model and billed them
accordingly. A plugin should not do that.

The recommendation, so it is an informed choice rather than a default: run
`dga-code-reviewer` and `dga-compliance-auditor` on the strongest model you have access to.
Both produce a **verdict** on work that is going to be scored, and a missed Blocker there costs
an assessment, not a review cycle. The rest degrade gracefully.

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
| `sitemap.xml` is fetchable but **stale** — 34 components and 16 templates against the real 50 and 19 (21 routed since 2026-10-08) | A lower-bound signal only. Never a count. Its template set is exactly the Sep 2024 release. |

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

The file also pins the **counts as a contract** (50 components, 21 templates, 5 foundations,
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

The SPA bundle is a static asset, and it **contains the router table** — all 50 component slugs,
21 templates, 5 foundations, 6 Thoughts — and names the small chunk that carries the release list.
So the counts contract and *"has DGA released?"* are answerable by `curl` after all. The sentinel
reads the router table rather than nav links: on 2026-10-08 DGA dropped a still-served page from
its nav, and a link reader reported it removed. Only page **prose** needs
a browser.

The bundles are ~19 MB, too heavy to pull for nothing, so `--check` fetches the 4 KB shell first
and reads the Vite build hashes out of it. Unchanged hashes mean DGA has not deployed and there is
nothing a deep read could find, so it stops there — **about a second**. A deploy triggers the full
read, about five.

| What it detects | How |
|---|---|
| DGA deployed | Vite build hash on the CSS or JS asset |
| A new release, or a release dropped | the version list in DGA's `releases-<hash>.js` chunk |
| A route added, removed or renamed | router-table diff against the baseline |
| A page leaving or joining the nav | nav links vs the router table, diffed against the baseline |
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
| `.github/workflows/dga-freshness.yml` | Mondays 06:00 UTC, or manual | Runs the sentinel, uploads a current `FRESHNESS.md` only after a completed check, opens **one rolling issue** when review is pending |
| `.github/workflows/ci.yml` | push + PR | The offline checks: fixtures, quote fidelity, contrast self-test, generated-file drift, installer, manifests |

Two properties of the sentinel workflow are load-bearing and asserted by the eval suite:

- **`permissions: contents: read`.** It cannot commit. A workflow able to write the repo could
  accept its own findings, which would silently close the review gate everything else defers to.
  `--baseline` is a human step, run locally, after the guidance has been updated.
- **Exit 1 is a result, not a failure.** The job stays green and the issue carries the signal;
  only exit >1 — a sentinel that could not complete — fails the build. Conflating the two either
  turns every real DGA change into a red build people learn to ignore, or hides a broken check
  behind an expected red.

Transient GET timeouts and connection resets get at most three attempts, with 5-second and
10-second pauses. HTTP, DNS and certificate errors fail immediately; TLS validation is unchanged.
Exhausted retries still return exit 2. A failed check means **freshness is unknown**, not that DGA
changed or that the recorded guidance is current. Its artifact contains only `sentinel.log`
(stdout and stderr), never the previously committed `FRESHNESS.md`. Inspect the failing URL and
network error before rerunning; retries cannot repair a persistently unreachable source.

**That was the situation from 2026-08-31 to 2026-10-18.** GitHub-hosted runners could not reach
`design.dga.gov.sa`, which answers only from Saudi Arabia: every run failed at the sentinel step
with exit 2, a TCP 443 timeout before TLS. Since 2026-10-18 the workflow runs through an
authenticated forward proxy in Saudi Arabia, admitted only from GitHub Actions' IP ranges
(`harvest/KSA-PROXY.md`). A self-hosted runner was rejected, because it is a security risk for a
public repository. First completed hosted run:
[39164824587](https://github.com/mohamedsamy911/dga-kit/actions/runs/39164824587), exit 0.
History:
[`harvest/diagnostics/2026-08-31-freshness-timeout.md`](harvest/diagnostics/2026-08-31-freshness-timeout.md).

The issue has a full lifecycle, not just an open:

| Sentinel | Workflow does |
|---|---|
| exit 1, no open issue | opens one, labelled `dga-freshness` |
| exit 1, issue already open | **comments** on it — a fresh issue every Monday for the same unread finding is how a queue stops being read |
| exit 0, issue open | **comments and closes** it: the baseline now matches, so the finding was accepted or reverted upstream |
| exit 0, no issue | nothing |
| exit >1, or the sentinel never ran | fails the job, reports an incomplete check, leaves review issues unchanged |

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
watches **us** — it compares the DGA quotes a capture actually covers (66 of 160 blockquotes
today; the rest are *unverifiable*, not verified) against the captured page text in
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

It also guards two things the quote checker structurally cannot, because neither is a quote:

**The token count contract.** `tokens.json` carries **345** values, plus **67** dark held for
audit only, out of the **1,126** custom properties DGA's stylesheet declares. The prose used to
convert one number into the other:

```text
"1,052 design tokens"
"All 1,052 DGA values are already extracted and machine-readable"
```

— which promised a developer wiring a theme roughly 3.5× what the file holds.
`$meta.carriedValues` is now asserted to be the real leaf count, every doc that sizes the token
set must quote it, and no file anywhere may describe the 1,052 read as a count of tokens shipped.
**That "aliases" explanation was itself wrong, and is retracted.**
`harvest/reconcile-tokens.py` reconciled the gap declaration by declaration against the live
stylesheet (build `CYyqM6kT`, re-run 2026-10-18): **293 resolve to values `tokens.json` does not
hold** — **246 the generic ramp** DGA ships but does not publish as a Platforms Code colour,
**12 gradients** whose components are all already carried, 26 under DGA's inert dark selector,
and 9 excluded by name with evidence. That leaves **0 DGA-namespaced** and **0 left to triage**:
the transparency scale, the real gap, is carried as `color.alpha`. Every figure is recorded in `$meta.$reconciliation` and
every declaration is listed in `harvest/RECONCILIATION.md`.

Three lessons worth keeping. The unstated exclusion was the actual defect on the generic ramp —
dropping it is right, *not saying so* is what made the count look like a contradiction. The
reconciliation only works because it compares **resolved values, not names**: DGA declares its
roles as `var()` chains, so a name diff reports a gap ten times larger and is useless. And
resolution has to honour the **cascade and the theme scope** — DGA redeclares 393 light names,
so a first-match resolver reported `--background-black` as an uncarried `#000000` when the
effective value is the already-carried `#161616`. That bug alone inflated the gap by 104
declarations, and the exclusion rule that replaced it has to be an **evidenced list**, because
one that infers "not semantic, therefore decorative" hides real gaps behind a plausible label.

**Values restated in prose.** The breakpoint bands, spacing steps and paragraph width are
re-derived from `tokens.json` and compared against every markdown copy. The first version of the
breakpoint check listed the expected bands as literal regex alternatives, so a drifted band:

```text
Tablet 600–899
```

simply failed to match and the check went green on a real regression. Every guard here is
mutation-tested: change the value, confirm the run turns red, revert.

Both scans skip fenced code blocks, so this section can quote the defects it describes without
tripping the guard that forbids them.

**Any fabrication fails a suite outright**, regardless of detection score.

## Where a design is checked twice — on purpose

`dga-design-review` pass 6 checks accessibility *in the design*; `dga-a11y` checks it *in the
running code*; `dga-code-reviewer` checks what is visible *statically in the source*. Different
artefacts, different failure modes, same rules. That is the only intentional overlap.

## Known gaps — what this kit does NOT cover

Stated plainly so no skill implies coverage it lacks.

| Gap | Impact | Fix |
|---|---|---|
| **Measurement criteria — Digital Transformation (Qiyas) and Digital Experience Maturity Index** | Both public reports are captured (2026-10-19, `harvest/raw/2026-10-19-measurement-indicators.md`), so `dga-launch-gate` §6 says what each measures. Their item-level criteria are not public — Qiyas's 95 criteria live in DGA's measurement system, DXMI's detailed reports go to owning entities — so the gate records both as *not assessed by this kit* and never issues PASS | The entity's own results; nothing public to harvest |
| ~~**Assessment Criteria *checklist file***~~ | **Closed 2026-10-19** — all 56 items, Arabic and English, in `harvest/raw/2026-10-19-assessment-checklist.md` and `dga-launch-gate/references/assessment-checklist.md`; the workbook's hash is checked on every freshness run | — |
| **DGA documents on dga.gov.sa** (registration controls DGA-1-2-2-106, accessibility guideline DGA-1-2-4-203, the measurement reports) | Captured 2026-10-19 from copies the owner downloaded. dga.gov.sa challenges automated clients, so no sentinel watches them | Re-download by hand; compare against the sha256 in each raw capture |
| **Component token names: light theme only, and 104 not linked to a kit token** | Since 0.10.0, DGA's 379 component token names (21 families: `--button-*`, `--link-*`, `--tag-*`, `--form-*`, ...) ship in `component-roles.json`/`.css`, generated from build `CYyqM6kT` by `harvest/build-component-roles.py`. 275 link to a kit token through DGA's own alias chain. 104 are literals: they point into the Untitled-UI ramps the kit does not carry, or into names like `--colors-primary-sa-flag-600-primary` with no kit counterpart. They are never matched by value alone. Dark is not emitted. Triage closed 2026-10-18: DGA's transparency scale is carried as `color.alpha` (42 values).  26 dark declarations are excluded by policy and 9 by name, with evidence. The 12 `--gradient-*` declarations: every colour in them is carried; the gradient definition is not. **A skill must not tell a caller a value is absent from DGA because it is absent from `tokens.json`.** Full list in the reconciliation report | Regenerate with `python harvest/build-component-roles.py` after each DGA deploy. The 104 literals link only if DGA publishes the ramps they point into, or names for them the kit carries |
| **The upstream Untitled-UI generic ramp** (246 declarations) | *Deliberately excluded*, not missing: blue, cyan, fuchsia, indigo, moss, orange, pink, purple, red, teal, violet, yellow and seven separate grey ramps. DGA ships them in CSS but does not publish them as Platforms Code colours. The exclusion list is **explicit, name by name** — an inferred "not semantic, therefore decorative" rule wrongly swept up `--colors-border-primary`, `--colors-text-primary` and the `--colors-alpha-*` primitives, and a wrong exclusion hides a real gap | None — but never quote these as DGA colours |
| ~~**Responsive radius & spacing values**~~ | **Closed 2026-10-19** — DGA's Figma Foundations file: radius is the same at every size; 39 spacing and 36 type values change per mode (`references/responsive-tokens.md`). `component-roles.css` now emits DGA's per-mode spacing | — |
| ~~**Dark theme values**~~ | **Closed 2026-08-27** — all **402** are in the public CSS bundle; the 67 text/background roles are in `tokens.json` as `role.dark` and audited by `check-contrast.mjs --theme dark`. 🚩 DGA's selector `[data-theme=dark] :root` can never match, so its dark theme is inert. **We do not ship it either** — see the row below | Remaining 340 non-role declarations are uncaptured in **both** themes — see `role.dark.$comment` |
| **Dark theme, shippable** | `tokens.css` deliberately emits **no** dark rule. Correcting DGA's selector would activate 1.05:1 pairings for anyone already using `data-theme="dark"`, and the five `*-light` status surfaces have no dark value in DGA's CSS. DGA's Figma dark theme defines them and the other hazards (read 2026-10-19), but it differs from the CSS in 80 roles, so picking it is a theme decision | An entity that wants dark mode owns the remediation and records it in `dga-brand-overlay` |
| ~~**Mobile UI Kit**~~ | **Read 2026-10-20** from DGA's Figma *Mobile Components* file: 57 component sets, structure and sizes in `mobile.md`. Behaviour was not captured: neither the Figma files nor the guideline pages reviewed specify it | Figma |
| **Arabic-language version of the site** | Arabic terminology for `content.md`. The toggle is reachable and renders; only the terminology harvest is outstanding | The `العربية` toggle |
| **Storybook** | Component demos | Marked "soon" by DGA — not available yet |
| **Designer sign-off** | Values are exact; the *interpretation* is unverified | A DGA-literate designer reads the references |

## Disputed and unverified claims

Recorded rather than quietly resolved, per the kit's own cite-or-omit rule.

| Claim | Status |
|---|---|
| ~~**How many places DGA itself states an RTL rule.**~~ This file once said "6 references across the whole system" without listing them. | **Closed 2026-10-19** — every string in the live site build was searched for direction words in English and Arabic, and each hit was checked on the rendered page (`harvest/raw/2026-10-19-rtl-statements.md`). Skills cite the pages, still never a total: the list holds for one DGA build. |
| Three colour values disputed against an independent extraction | **Explained 2026-10-19** — `neutral.500`/`950`: DGA's CSS and its Figma Foundations file differ by one unit, as 20 other primitives do; the June read matches Figma. Kit keeps the rendered CSS values. `info.50` reads blue in the live build. Kept in `$meta.$disputed` as a record; see `harvest/raw/2026-10-19-figma-foundations.md` |
| **How many components DGA ships.** `/about-platforms-code` publishes a **33+** counter. `/guidelines/components/` enumerates **50** routes. | Recorded, not reconciled. This kit cites **50** — the enumerable count. The counter is stale marketing copy. |
| **When 1.0.0 and 1.0.2 shipped.** `/updates/roadmap` dates them Feb 2024 and Sep 2024; `/updates/change-log` dates the same versions 20 Feb **2025** and 1 Sep **2025**. | Cite the change log — the more specific record. |

## Where DGA itself is silent

No skill invents a rule here. Each says DGA is silent and names its fallback.

Numeral policy · Hijri calendar · motion tokens (durations and easings —
though `prefers-reduced-motion` **is** required in three places) · terminology glossary ·
Arabic tone of voice · **Card accessibility** (DGA's section is Accordion's, pasted in) ·
**Menu accessibility** (no section exists at all) · Table ARIA roles · carousel pause control
(WCAG 2.2 AA 2.2.2 requires one — apply WCAG) · colour-blind-safe chart palettes · dark-mode
usage guidance · accessibility-statement page.

## Where DGA's own tokens fail WCAG

Not a gap in this kit — a fact about the source, and the reason `check-contrast.mjs` exists.
`text.secondary` (#dba102) is a DGA token **designated for text** that measures 2.30:1 on white
and fails AA at every size. Three `text.*-light` tokens are dark-surface only despite the naming.
Run `node skills/dga-design-system/assets/check-contrast.mjs` for the current list.
