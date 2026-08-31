# AGENTS.md — working on dga-kit

Instructions for any coding agent (Codex, Claude Code, or otherwise) making changes **to this
repository**. This is not DGA guidance; it is the contract for editing the kit safely.

For what the kit *is*, read [README.md](README.md). For what it does and does not cover,
[COVERAGE.md](COVERAGE.md).

## The one rule this project lives or dies by

**Cite or omit.** Every rule in `skills/*/references/` names the DGA page set it came from and the
date it was retrieved. Where DGA is silent, say so and name the fallback (usually WCAG 2.1 AA).

**Never invent a DGA rule to fill a gap.** A compliance tool that is confidently wrong is worse
than no tool — a team ships believing it is compliant and fails an assessment. If you cannot cite
it, do not write it.

The same applies to coverage claims. State what the harvest actually holds — all 19 templates as
of 2026-08-27 — and never round a partial harvest up.

## Before you commit

```bash
python evals/validate-fixtures.py                # "All fixtures valid against tokens.json"
python evals/test-automation.py                  # "All automation scenarios detected correctly"
python evals/check-quote-fidelity.py --ci        # must exit 0
python evals/build-evals-json.py --check          # "evals.json is current for both suites"
python evals/build-codex-agents.py --check         # six native agents match their Markdown sources
python evals/test-codex-agents.py                 # conversion and isolated installer regressions
python harvest/reconcile-tokens.py --test         # "reconcile self-check passed" (offline)
node skills/dga-design-system/assets/check-contrast.mjs --test   # "self-check passed"
node skills/dga-design-system/assets/generate-tokens.mjs          # then `git diff` must be empty
node bin/dga-kit.mjs --test                       # "installer self-check passed"; leaves no temp dirs
node bin/dga-kit.mjs --dry-run                    # installer parses and plans; writes nothing
```

**The freshness sentinel's exit codes are a contract.** `harvest/sources.py --check` returns
`0` no change, `1` a finding a human must review, `2` the sentinel could not complete. The weekly
workflow keeps the job green on `1` and fails it on `>1`. Python exits `1` on any unhandled
exception, so every new failure path must be routed through `check_main()` and return `2` — a
broken monitor that reports `1` files a review issue weekly while knowing nothing.

**Before a release, also run Codex's own plugin validator.** It ships with a Codex installation,
so CI cannot rely on it — CI reports SKIPPED when absent rather than passing quietly. Three
documents claim this repo passes it, which makes it a claim someone has to actually check:

```bash
python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

This list must match `.github/workflows/ci.yml`. It drifted once — the file named two gates while
CI ran six — so a contributor running "the gates" was checking a third of what the pipeline
checked. `validate-fixtures.py` enforces the match.

`validate-fixtures.py` is the guard for everything below. If it fails, the change is wrong — do
not "fix" the assertion to make it pass without first proving the assertion was the error.

**A guard that cannot fail is worse than no guard.** Every check added here has been *break-tested*:
the thing it guards is deliberately broken, and the check must fail — and fail on that alone. This
repo has shipped three checks that passed while verifying nothing (a `grep | wc -l` under
`set -euo pipefail`, a vacuous status-vocabulary assertion, and a stale-claim detector that matched
no real sentence). Prove the new check fails before trusting it to pass.

## Invariants that are easy to break

**1 · `tokens.json` is the harvest, not a working file.** Values are verbatim from
design.dga.gov.sa. Do **not** "correct" one because it looks wrong.

The live example: DGA publishes display tracking as `-2%`, and CSS `letter-spacing` does not
accept percentages — every browser drops it. The fix is **not** to edit `tokens.json`; it keeps
`-2%` so a re-harvest diffs clean. `generate-tokens.mjs` converts to `-0.02em` at the boundary.
Fixtures assert both halves.

**2 · Never hand-edit generated files.** `tokens.css` and `tailwind-preset.js` are outputs. Change
`tokens.json` or the generator, then:

```bash
node skills/dga-design-system/assets/generate-tokens.mjs
```

A hand-edit is silently reverted by the next contributor who regenerates.

The same rule applies to `codex-agents/*.toml`: edit `agents/*.md`, then run
`python evals/build-codex-agents.py` (Python 3.11+ and PyYAML). The Markdown body and description
must survive conversion intact. Only the Codex skill-lookup preamble and read-only sandbox
defaults are added; do not copy Claude tool names or pin models/reasoning effort.

**3 · `$`-prefixed keys are annotations, never token values.** `$source`, `$verify`, `$note`,
`$meta`. **Every loop in a generator must skip them** or they leak into output as
`--dga-width-$source: [object Object]`. This has already happened once.

**4 · Suspect values go in `$verify`, in the data.** Not in prose a consumer of `tokens.json` will
never read. `status` must come from the vocabulary in `$meta.$conventions`, and anything marked
`disputed` must also be written up in `harvest/` — both are enforced.

**5 · Nothing in `skills/` may reference outside `skills/`.** Only runtime skills and agent
definitions are installed; `harvest/`, `evals/` and `COVERAGE.md` are not. A `../../harvest/…`
link resolves in this repo and dangles for every user. Enforced by the *installed layout* check.

**6 · Eval fixtures must not contradict the guidance they test.** Case 12 shipped four times with
a defect a reviewer then correctly reported, scoring a right answer as a false positive. Where a
fixture asserts a number or a code pattern, assert it against the source of truth in
`validate-fixtures.py` rather than trusting prose in two places.

**7 · `check-contrast.mjs --ci` exits 1 by design.** DGA publishes a text token (`text.secondary`,
#dba102, 2.30:1) that fails AA. The script audits **DGA's own** table and never reads project
source, so it cannot be a green gate and is not a substitute for checking a real codebase.

**8 · The installers may only ever delete what they installed.** For the Claude installers, a
path is removed only if it is both recorded in `~/.claude/.dga-kit-manifest` **and** matches the
fixed allowlist. The manifest is editable text, so it is a record, not an authority. Never
reintroduce deletion by name — an earlier version deleted `rga-brand`, a plausible name for a
user's own skill.

`bin/dga-kit.mjs` leaves anything it did not write alone, with two announced exceptions: `--force`
adopts and overwrites an unclaimed `dga-*` path, and `--clean-legacy` deletes pre-0.5 paths after
you type DELETE. It takes an explicit project
or user scope, preflights every file, and refuses conflicting or linked destinations. Test it
in scratch directories, never by modifying the maintainer's real Codex profile.

## Layout

```
skills/     11 skills; dga-design-system is the source of truth the rest read
agents/     6 Claude Markdown agents, each self-contained (source of truth)
codex-agents/  6 generated native Codex TOML agents, installed separately
harvest/    the evidence trail — capture log and cross-references
evals/      23 cases across two suites, plus validate-fixtures.py
showcase/   standalone fictional Arabic/English demo; separate dependencies and Pages build
```

Skills reference each other as siblings (`../dga-design-system/...`), so the flat layout is
required.

For showcase changes, also follow `showcase/AGENTS.md` and run the build, theme guard, and
production-path browser tests documented in `showcase/README.md`. Those additional gates live
in `.github/workflows/showcase-pages.yml`; they do not replace the kit gates above. Never add
showcase dependencies to the root installer package or publish anything except `showcase/dist`.

## Changing DGA rules

Re-harvesting is `skills/dga-tokens-sync/SKILL.md` — follow it rather than improvising. It covers
re-stamping per-section `$source` dates (only for pages you actually re-read), recording what you
could not settle as `$verify`, and re-running the contrast check and fixtures.

## Tone

Reference files are read by engineers under deadline pressure. State the rule, the reason it
matters, and the concrete fix. Flag the traps that pass a build and a code review — those are the
kit's whole reason to exist. Do not pad.
