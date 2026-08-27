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
python evals/validate-fixtures.py                              # must print "All fixtures valid"
node skills/dga-design-system/assets/check-contrast.mjs --test  # must print "self-check passed"
```

`validate-fixtures.py` is the guard for everything below. If it fails, the change is wrong — do
not "fix" the assertion to make it pass without first proving the assertion was the error.

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

**3 · `$`-prefixed keys are annotations, never token values.** `$source`, `$verify`, `$note`,
`$meta`. **Every loop in a generator must skip them** or they leak into output as
`--dga-width-$source: [object Object]`. This has already happened once.

**4 · Suspect values go in `$verify`, in the data.** Not in prose a consumer of `tokens.json` will
never read. `status` must come from the vocabulary in `$meta.$conventions`, and anything marked
`disputed` must also be written up in `harvest/` — both are enforced.

**5 · Nothing in `skills/` may reference outside `skills/`.** Only `skills/` and `agents/` are
installed; `harvest/`, `evals/` and `COVERAGE.md` are not. A `../../harvest/…` link resolves in
this repo and dangles for every user. Enforced by the *installed layout* check.

**6 · Eval fixtures must not contradict the guidance they test.** Case 12 shipped four times with
a defect a reviewer then correctly reported, scoring a right answer as a false positive. Where a
fixture asserts a number or a code pattern, assert it against the source of truth in
`validate-fixtures.py` rather than trusting prose in two places.

**7 · `check-contrast.mjs --ci` exits 1 by design.** DGA publishes a text token (`text.secondary`,
#dba102, 2.30:1) that fails AA. The script audits **DGA's own** table and never reads project
source, so it cannot be a green gate and is not a substitute for checking a real codebase.

**8 · The installers may only ever delete what they installed.** A path is removed only if it is
both recorded in `~/.claude/.dga-kit-manifest` **and** matches the fixed allowlist. The manifest is
editable text, so it is a record, not an authority. Never reintroduce deletion by name — an
earlier version deleted `rga-brand`, a plausible name for a user's own skill.

## Layout

```
skills/     11 skills; dga-design-system is the source of truth the rest read
agents/     6 agents, each self-contained (no shared includes)
harvest/    the evidence trail — capture log and cross-references
evals/      23 cases across two suites, plus validate-fixtures.py
```

Skills reference each other as siblings (`../dga-design-system/...`), so the flat layout is
required.

## Changing DGA rules

Re-harvesting is `skills/dga-tokens-sync/SKILL.md` — follow it rather than improvising. It covers
re-stamping per-section `$source` dates (only for pages you actually re-read), recording what you
could not settle as `$verify`, and re-running the contrast check and fixtures.

## Tone

Reference files are read by engineers under deadline pressure. State the rule, the reason it
matters, and the concrete fix. Flag the traps that pass a build and a code review — those are the
kit's whole reason to exist. Do not pad.
