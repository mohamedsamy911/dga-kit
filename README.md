# dga-kit

**Saudi DGA "Platforms Code" compliance, as Claude Code skills and agents.**

If you build for a `.gov.sa` platform, you have to satisfy the National Design System of Saudi
Arabia — [design.dga.gov.sa](https://design.dga.gov.sa/). It is a **scored** requirement: the
entity is assessed against the Digital Transformation and Digital Experience Maturity indicators.
Most teams find that out late, from an assessor.

This kit puts the rules where the work happens, so compliance is checked on every screen and
every component instead of remembered at the end.

**Works with any UI library** — Tailwind, MUI, Chakra, shadcn/Radix, Ant Design, Bootstrap, a Vue
or Angular kit, plain CSS, or DGA's own React package.

## Install

```bash
/plugin marketplace add mohamedsamy911/dga-kit
```

```bash
/plugin install dga-kit@dga-kit
```

Then restart Claude Code. Prefer per-project or global copies without the plugin system? See
[INSTALL.md](INSTALL.md).

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

**6 agents** — ask for one by name, or let Claude pick.

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

That runs WCAG contrast over DGA's own token pairings. It reports five failures — because DGA
publishes a text token, `text.secondary` (#dba102), that measures **2.30:1 on white** and fails
AA at every size, large included. It is a real token, designated for text, so the name invites
the mistake and reviewers defer to it.

That is the kind of thing this kit exists to catch. Wire the script into CI with `--ci`.

## The one rule

**Cite or omit.** Every DGA rule in `references/` carries its source URL and the date it was
retrieved. Where DGA is silent, a skill says so and names its fallback — WCAG 2.1 AA, or a stated
project default. Nothing is invented.

A compliance tool that is confidently wrong is worse than no tool at all. So the kit also states,
out loud, [where DGA itself is silent or self-contradictory](COVERAGE.md#where-dga-itself-is-silent)
— including two component pages that are defective at source.

## Status, honestly

Token values were **extracted from the live site's CSS custom properties**, not transcribed —
1,052 of them, on 2026-08-26. The system is "Platforms Code", site Version 1.0, design kits PC 1.0.

| | |
|---|---|
| Harvest — 5 foundations, 50 components, 19 templates, 1,052 tokens | ✅ Complete |
| 11 skills, written and DGA-grounded | ✅ |
| 6 agents | ✅ |
| Contrast checker, self-tested | ✅ |
| **Designer sign-off** | ⚠️ **Outstanding** — values are exact, interpretation unverified |
| **Figma-only values** (dark theme, responsive radius/spacing, mobile kit) | ❌ Not public. Omitted, not guessed. |

See [COVERAGE.md](COVERAGE.md) for what is and is not covered, and
[harvest/CAPTURE-LOG.md](harvest/CAPTURE-LOG.md) for the evidence trail.

## Layout

```
skills/     the 11 skills; dga-design-system is the source of truth the rest read
agents/     the 6 agents
harvest/    raw captures + CAPTURE-LOG.md — the evidence behind every rule
evals/      23 eval cases across two suites, plus a fixture validator
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

Not affiliated with or endorsed by the Digital Government Authority. Platforms Code is DGA's;
this kit is an unofficial reading of it. When it matters, verify with DS-DGA@dga.gov.sa.

## Licence

[MIT](LICENSE) — the kit's own text and code. The DGA rules it cites belong to the Digital
Government Authority and are quoted here under their published guidance, not relicensed.
