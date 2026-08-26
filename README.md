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
| `dga-design-system` | The rules. Foundations, 50 components, 18 of 19 templates, content, tokens. Everything else reads from it. |
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

Token values were **extracted from the live site's CSS custom properties**, not transcribed —
1,052 of them, on 2026-08-26. The system is "Platforms Code", site Version 1.0, design kits PC 1.0.

| | |
|---|---|
| Harvest — 5 foundations, 50 components, 1,052 tokens | ✅ Complete |
| Templates — **18 of 19** | ⚠️ Hajj not yet harvested ([gap list](COVERAGE.md#known-gaps--what-this-kit-does-not-cover)) |
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

**Reporting a problem:** see [SECURITY.md](SECURITY.md). A factual error in a compliance rule is
treated with the same priority as a security bug, because a platform shipping on a wrong rule
fails an assessment it believed it had passed.

**Trademarks.** "Digital Government Authority", "DGA" and "Platforms Code" belong to their
owners. They are used here descriptively, to say what this kit is about. No affiliation or
endorsement is claimed or implied — see the notice at the top of this file.

## Licence

[MIT](LICENSE) — the kit's own text and code. The DGA rules it cites belong to the Digital
Government Authority and are quoted here under their published guidance, not relicensed.
