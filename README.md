# dga-kit

**Saudi DGA "Platforms Code" guidance, as skills and agents for Claude Code and Codex.**

If you build for a `.gov.sa` platform, you have to satisfy the National Design System of Saudi
Arabia — [design.dga.gov.sa](https://design.dga.gov.sa/). It is a **scored** requirement: the
entity is assessed against the Digital Transformation and Digital Experience Maturity indicators.
Most teams find that out late, from an assessor.

This kit puts the rules where the work happens, so compliance is checked on every screen and
every component instead of remembered at the end.

**Works with any UI library** — Tailwind, MUI, Chakra, shadcn/Radix, Ant Design, Bootstrap, a Vue
or Angular kit, plain CSS, or DGA's own React package.

## Before you install — read this

> **This is an unofficial project.** It is **not affiliated with, endorsed by, or certified by**
> the Digital Government Authority. "Platforms Code" and "DGA" are theirs, not mine; this kit is
> one reading of their **publicly published** material, and it can be wrong.
>
> **It cannot make your platform compliant, and it is not evidence of compliance.** Use it to
> find issues faster and to know what to ask — then **verify anything that matters directly with
> DGA at DS-DGA@dga.gov.sa.**
>
> The interpretation has **not been signed off by a DGA-literate designer**. Token values are
> exact; what they mean is a reading. [COVERAGE.md](COVERAGE.md) lists every known gap and
> unverified claim, including where DGA's own published pages are defective.

## Try the showcase

[**Live demo: وصل · Wasl**](https://mohamedsamy911.github.io/dga-kit/) ·
[English](https://mohamedsamy911.github.io/dga-kit/?lang=en) ·
[Source and local setup](showcase/README.md)

An Arabic-first, bilingual fictional service portal built with the kit: explore services,
complete a simulated request, and try keyboard navigation and accessibility controls.
**Not a government service or evidence of compliance.** Use fictional details only; requests
stay in memory and disappear on refresh. The demo runs independently of Claude Code and Codex.

## Install

**One command. Everything, for whatever you have installed.**

```bash
npx github:mohamedsamy911/dga-kit
```

It detects Claude Code and Codex on your machine and installs the **11 skills and 6 agents** for
each.

**Prerequisites: Node 18+ and Git.** Git is not optional — npm resolves a `github:` spec by
cloning, so without it `npx` fails with an ENOENT from git rather than anything useful. Nothing
is published to npm, and there is no `npm install` step: `npx` fetches this repository and runs
it.

Anything it cannot do, it names and tells you how to finish — it never half-installs and calls it
done. A file you have edited is never overwritten **unless you pass `--force`** — and on the
Codex side not even then, because a differing agent is always refused. `--uninstall`
removes only what the installer wrote.

Narrow it with one flag from each axis:

| | |
|---|---|
| `--claude` · `--codex` | one tool instead of both |
| `--skills` · `--agents` | one kind instead of both |
| `--claude --skills` | a single cell — any combination works |
| `--project .` | Codex agents into this project's `.codex/agents/`, not your home |
| `--dry-run` | print the plan, write nothing |
| `--uninstall` | remove only what it installed |
| `--help` | the full list |

Then restart Claude Code, and start a new Codex session.

> **One step is not a file copy.** Codex serves plugin *skills* from its own cache plus
> `config.toml`, not from a directory, so the installer runs `codex plugin marketplace add` and
> `codex plugin add` for you. If the `codex` CLI is not on your PATH it says so and prints the two
> commands rather than guessing at Codex's internal layout. Codex *agents* are a plain file copy,
> because its plugin manifest has no top-level `agents` field — which is why they need their own
> step at all.

<details>
<summary>Installing Claude Code through the plugin marketplace instead</summary>

```bash
/plugin marketplace add mohamedsamy911/dga-kit
```

```bash
/plugin install dga-kit@dga-kit
```

</details>

## What you get

**11 skills** — invoked automatically when the work matches, or by name.

| Skill | Use it for |
|---|---|
| `dga-design-system` | The rules. Foundations, 50 components, 19 templates, content, tokens. Everything else reads from it. |
| `dga-ui-adapter` | **Building UI on any library.** Token wiring, all 50 components mapped, the compliance build list. |
| `dga-react` | Building on DGA's own `platformscode-new-react` package. |
| `dga-rtl-i18n` | Arabic-first RTL, bidi text, Arabic typography, Hijri dates, numerals, i18n wiring. |
| `dga-design-review` | Auditing a design against DGA. Seven passes, severity rubric, verdict. |
| `dga-mockup` | Producing a compliant screen or wireframe, Arabic-first. |
| `dga-handoff` | Turning an approved design into a developer spec. |
| `dga-a11y` | Auditing a running app against DGA's per-component ARIA and WCAG 2.1 AA. |
| `dga-launch-gate` | Everything beyond design: registration, the transparency mandate, required pages, Open Data. |
| `dga-tokens-sync` | Re-harvesting DGA's tokens and diffing them against this repo. |
| `dga-brand-overlay` | Your entity's brand on top of DGA, and the decisions DGA leaves open. |

**6 agents, in both formats** — ask for one by name, or let Claude pick. In Codex, install them
separately as above and explicitly ask for delegation to the named subagent.

| Agent | Does |
|---|---|
| `dga-designer` | Frames the problem, designs the full state matrix, writes the copy, produces a handoff. |
| `dga-frontend-architect` | The eight decisions before code exists: token ownership, UI library, the compliance backlog, RTL strategy, routing, state. Read-only. |
| `dga-frontend-dev` | Builds features from a spec on your stack, DGA-compliant and Arabic-first. |
| `dga-code-reviewer` | Reviews for correctness, security, DGA compliance and WCAG AA. Read-only. |
| `dga-compliance-auditor` | Pre-launch go/no-go with evidence per item. Read-only. |
| `dga-content-writer` | Arabic-first bilingual UI copy, against DGA's prescribed strings. |

## Try it

```bash
node skills/dga-design-system/assets/check-contrast.mjs
```

That runs WCAG contrast over DGA's own token pairings, **both themes**, and reports **20
failures** — 5 in light, 15 in dark. Add `--theme light` for the light-only run.

The five light ones all come from a single token: `text.secondary` (#dba102) measures **2.30:1 on
white** and fails AA at every size, large included. It is a real token, designated for text, so
the name invites the mistake and reviewers defer to it.

That is the kind of thing this kit exists to catch. ⚠️ **`--ci` cannot go green on stock DGA
tokens** — `text.secondary` fails permanently, and no change to *your* code alters that, because
the script only ever reads DGA's table. Run it as a committed artefact (`--json`) and gate your
build on a grep over your own source. The 15 dark failures are worse and are covered below.

```bash
python3 harvest/sources.py --check
```

That asks DGA whether anything has changed since this kit was built. On a quiet week it answers
in about a second and downloads nothing.

## The one rule

**Cite or omit.** Every reference file names the DGA page set it was gathered from and the date
it was retrieved. Component and foundation rules cite an exact page URL; cross-cutting references
(brand, content, mobile) name the page set, because DGA publishes no single page for them.
Where DGA is silent, a skill says so and names its fallback — WCAG 2.1 AA, or a stated project
default. Nothing is invented.

**This is auditable, and it is not yet per-rule.** A handful of rules carry the page set rather
than the individual URL. Where a claim matters to you, check it against DGA directly and
[open an issue](https://github.com/mohamedsamy911/dga-kit/issues) if it does not hold — that is the most useful contribution you can
make to this kit.

A compliance tool that is confidently wrong is worse than no tool at all. So the kit also states,
out loud, [where DGA itself is silent or self-contradictory](COVERAGE.md#where-dga-itself-is-silent)
— including two component pages that are defective at source.

## Status, honestly

Token values were **extracted from the live site's CSS custom properties**, not transcribed, on
2026-08-26. `tokens.json` carries **303** values a project consumes, plus **67** dark values held
for audit only. DGA's stylesheet declares **1,126** custom properties — 1,065 on `:root`, 402
under the dark selector, 61 elsewhere.

**That gap is now reconciled, and the earlier explanation of it was wrong.** This kit used to
explain the difference away as aliasing:

```text
The rest are aliases and per-component role vars resolving to values already held.
```

[`harvest/reconcile-tokens.py`](harvest/reconcile-tokens.py) settled it declaration by
declaration against the live stylesheet: **412 resolve to values `tokens.json` does not hold.**
Of those, **246 are the generic ramp** — the upstream Untitled-UI palette DGA ships in CSS but
does not publish as a Platforms Code colour, a deliberate exclusion that had simply never been
*stated*. Another **12 are gradients** whose every colour component the kit already holds: what
is missing there is the gradient *definition*, not a value. The remaining **154 go to triage**:
129 DGA-namespaced values the kit does not hold, plus 25 whose family is unrecognised and are
left for review rather than quietly excluded. That covers the entire `--alpha-*` transparency
scale, the `--colors-alpha-*` primitives behind it, and the `--button-*`, `--link-*`,
`--notification-*` and `--tag-*` role sets. Every one is listed in
[harvest/RECONCILIATION.md](harvest/RECONCILIATION.md).

The system is "Platforms Code", published version **1.0.3** (released 4 Nov 2025, per
`/updates/change-log`). The nav badge and footer still read "Version 1.0" and the Figma files
are still named `PC 1.0 …` — those are chrome and filenames, not the version. The harvest postdates 1.0.3, so the values are current.

| | |
|---|---|
| Harvest — 5 foundations, 50 components, **all 19 templates**, **303 token values** read from 1,052 CSS custom properties | ✅ Complete |
| **Assessment Criteria** — the rubric a platform is actually scored against | ✅ Captured |
| 11 skills, 6 agents | ✅ |
| Contrast checker, self-tested — light **and dark** | ✅ |
| **Freshness monitoring** — weekly, review-gated | ✅ See below |
| **Codex plugin install path** | ✅ Verified 2026-08-28 — skills only; passes Codex's own `validate_plugin.py` |
| **Codex-native agents** | Six generated TOML definitions; separate installer with offline safety/parity checks. Confirm runtime discovery in your Codex session. |
| **Designer sign-off** | ⚠️ **Outstanding** — values are exact, interpretation unverified |
| **Figma-only values** (responsive radius/spacing, mobile kit specs) | ❌ Not public. Omitted, not guessed. |

**Dark theme: found, and broken upstream.** This kit used to list dark values as Figma-only. They
are not — DGA ships **402 dark declarations** in its public CSS. But they sit under the selector
`[data-theme=dark] :root`, which can never match, because `:root` is `<html>` and a descendant
combinator needs an ancestor it does not have. Verified in the live page: zero elements matched.
**DGA ships a complete dark theme that cannot turn on.**

The values are carried in `tokens.json` for audit, and deliberately **not** generated into
`tokens.css` — correcting the selector would activate it for anyone already using
`data-theme="dark"` (Chakra v3 does, out of the box), and it cannot be made safe from DGA's own
values: five `*-light` status surfaces have no dark tint anywhere, so white text on them measures
**1.05:1**. Run `check-contrast.mjs --theme dark` for the full list.

See [COVERAGE.md](COVERAGE.md) for what is and is not covered, and
[harvest/CAPTURE-LOG.md](harvest/CAPTURE-LOG.md) for the evidence trail.

## Staying current

DGA ships roughly four releases a year, and a compliance kit that quietly goes stale is worse
than none. Two directions are watched, because they fail differently:

**Is DGA still saying what we recorded?** A weekly GitHub Action diffs the live site against a
recorded baseline — build hashes, the route table and release list read out of DGA's own JS
bundle, `text.secondary`, the dark selector, sitemap and robots. It writes
[harvest/FRESHNESS.md](harvest/FRESHNESS.md) and opens one rolling issue when something needs a
decision.

**Are we still saying what DGA said?** That is the failure this repo has actually had — invalid
CSS shipped from a token unit, a template count asserted at 19 when the harvest held 17, and a
launch-gate quote that dropped DGA's word *"typically"*, turning "typically cannot proceed to
deployment" into an unconditional block. No amount of watching DGA catches those.
`evals/check-quote-fidelity.py` compares the DGA quotes it *can* — those whose source page has
been captured — against that captured text, and fails on a quote that reproduces a capture
without matching it. It found two real defects on its first run. Be clear about its reach: only
**2 DGA pages are captured**, so 14 of 92 blockquotes are checkable and the other 78 are
**unverifiable, not verified**. A quote fenced as DGA's own words with no capture behind it fails
the run.

**Nothing accepts itself.** The sentinel never rewrites its baseline; the deep harvest writes
nothing without an explicit `--accept`; the Action has `contents: read` and cannot commit. A
finding stays open until a human updates the guidance. And `evals/test-automation.py` tests the
monitoring itself against six scenarios — a new version, a changed token, a renamed template, a
blocked page, a contradiction — because a monitor that has silently stopped working looks exactly
like a quiet week.

## Layout

```
skills/     the 11 skills; dga-design-system is the source of truth the rest read
agents/     the 6 Claude Markdown agents — source of truth for both formats
codex-agents/  generated native Codex TOML agents — installed separately
bin/dga-kit.mjs  the one installer (npx); leaves what it did not write alone, except --force
                 (adopts an unclaimed dga-* path) and --clean-legacy (deletes pre-0.5 paths
                 after you type DELETE)
harvest/    the evidence behind every rule, and the monitoring that keeps it honest
              raw/                curated captures, with <!-- dga --> marking DGA's own words
              CAPTURE-LOG.md      what was captured, from where, when
              sources.py          the source contract + the Tier A sentinel (--check)
              source-inventory.json  every watched URL, its owning references, the counts contract
              deep.py             Tier B: browser-captured page text (--capture / --accept)
              snapshots/          machine-owned page text, for diffing only
              FRESHNESS.md        generated: last check, what moved, review pending?
              reconcile-tokens.py    every DGA declaration vs every value we carry
              RECONCILIATION.md      generated: every DGA value we do NOT carry
evals/      23 eval cases across two suites, run by `claude plugin eval`:
              <suite>/cases/*.md        the cases, in markdown — the source a human reviews
              build-evals-json.py       generates skills/<skill>/evals/evals.json from them
              build-codex-agents.py      generates native Codex agents from agents/*.md
              test-codex-agents.py       conversion and safe-install regressions
              validate-fixtures.py      the kit against its own tokens, evidence and prose
              check-quote-fidelity.py   the DGA quotes a capture covers (14 of 92 today)
              test-automation.py        whether the monitoring detects what it claims to
showcase/   fictional Arabic/English React demo; separate dependencies, tests and build
.github/    plugin CI, the weekly freshness sentinel, and showcase Pages deployment
```

## Prior and parallel work

[`Sara-Saraireh/dga-platforms-code-claude-skill`](https://github.com/Sara-Saraireh/dga-platforms-code-claude-skill)
is an independent Claude Code skill for the same standard, MIT-licensed, and it extracted the
colour tokens from the same DGA page two months before this kit did.

The two extractions were compared: **48 of 51 shared colour steps are character-identical**,
which is stronger evidence for both sets of numbers than either repo could produce alone. Three
values disagree and are recorded as open in
[harvest/CROSSREF-SECOND-EXTRACTION.md](harvest/CROSSREF-SECOND-EXTRACTION.md) rather than
quietly resolved in this kit's favour.

If you want one focused skill rather than eleven, look there first.

## Contributing

The most useful contributions are **corrections with a citation**. If a rule here does not match
what DGA publishes, open an issue with the URL and what it says. Second most useful: token
re-harvests when DGA updates (`dga-tokens-sync` does the diff).

For demo changes, see [showcase setup and checks](showcase/README.md) and the
[Pages publishing guide](showcase/docs/PUBLISHING.md). Keep its dependencies separate from
the root package, preserve the fictional-demo disclosure, and test the production `/dga-kit/`
path in both languages before publishing.

**Reporting a problem:** see [SECURITY.md](SECURITY.md). A factual error in a compliance rule is
treated with the same priority as a security bug, because a platform shipping on a wrong rule
fails an assessment it believed it had passed.

**Trademarks.** "Digital Government Authority", "DGA" and "Platforms Code" belong to their
owners. They are used here descriptively, to say what this kit is about. No affiliation or
endorsement is claimed or implied — see the notice at the top of this file.

## Licence

[MIT](LICENSE) — the kit's own text and code. The DGA rules it cites belong to the Digital
Government Authority and are quoted here under their published guidance, not relicensed.
