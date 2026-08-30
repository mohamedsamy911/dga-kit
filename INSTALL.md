# Installing dga-kit

Three ways. Pick one.

## 1 · As a plugin — recommended

```bash
/plugin marketplace add mohamedsamy911/dga-kit
```

```bash
/plugin install dga-kit@dga-kit
```

Restart Claude Code. All 11 skills and 6 agents load together, update with the repo, and
uninstall cleanly with `/plugin uninstall dga-kit`.

## 1b · With OpenAI Codex

```bash
codex plugin marketplace add mohamedsamy911/dga-kit
```

```bash
codex plugin add dga-kit@dga-kit
```

That installs the **11 skills**. It does not install the agents — see below.

**How this was established.** Codex publishes its own plugin contract locally, in the
`plugin-creator` system skill that ships with the CLI
(`~/.codex/skills/.system/plugin-creator/`). The manifest lives at `.codex-plugin/plugin.json`,
and the repository's copy **passes Codex's own validator**:

```
$ python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
Plugin validation passed
```

The catalogue Codex installs *from* is `.agents/plugins/marketplace.json` at the repository root —
`codex plugin add` installs from a configured marketplace, never from a bare plugin manifest. This
kit ships one, with a `url` source pointing back at this repository on `master`. The same shape is
used by [ponytail](https://github.com/DietrichGebert/ponytail), which is installed and working as a
Codex git marketplace.

> ⚠️ **`"skills": "./skills/"` resolves from the plugin root — do not change it to `"../skills/"`.**
> Confirmed four ways: Codex's spec, its `validate_plugin.py` (which requires the normalised value
> `skills`), its scaffold generator, and ponytail's installed manifest. An external review once
> recommended `"../skills/"`; it would resolve outside the repository and fail validation.
> `evals/validate-fixtures.py` pins it.

### What Codex does NOT install: the 6 agents

`codex plugin add` installs this kit's **11 skills**. It does **not** register the six Markdown
files in the repository-root `agents/` directory as Codex agents: Codex's plugin manifest has no
top-level `agents` field — `validate_plugin.py` rejects unknown keys — and this kit declares only
`"skills": "./skills/"`.

> ⚠️ **Do not read that as "Codex has no `agents/` concept."** It does, and this kit uses it —
> just for something else. A *skill* may carry `agents/openai.yaml`, which Codex's own validator
> reads at `skill_root / "agents" / "openai.yaml"`, for **UI metadata and invocation policy**:
> display name, description, brand colour, starter prompt. All 11 skills here ship one. That is a
> different thing from a repository-root `agents/` folder holding agent definitions, and an
> earlier version of this page conflated the two.

**Why the agents cannot be promised.** Codex can import Claude Code agents — its own selector
reads *"Migrate subagents from `~/.claude/agents` to `~/.codex/agents`"*, and
`external-agent-import-sync-enabled` appears in `config.toml`. On the machine where this was
tested, five of this kit's six agents had been converted to TOML that way. **Five of six is the
point:** `dga-frontend-architect` was missing, and no local log or specification explains what
performed the conversion. It also reads from `~/.claude/agents`, not from the installed plugin —
so it is a Codex feature that may run, not an install path this kit controls.

**Converting an agent by hand.** Codex agents are TOML — in `~/.codex/agents/` for your machine,
or `.codex/agents/` for a single project. Each of this kit's agents is Markdown with YAML front
matter (`name`, `description`) and a Markdown body. The mapping is direct — front matter `name`
and `description` become TOML keys, and the entire Markdown body becomes
`developer_instructions`:

```toml
# ~/.codex/agents/dga-designer.toml
name = "dga-designer"
description = "Principal-level product designer for Saudi government platforms. Arabic-first."
developer_instructions = """
<the whole Markdown body of agents/dga-designer.md, verbatim>
"""
```

Verify it was picked up with:

```bash
codex agents
```

**This is a supported Codex feature, and it is documented.** An earlier version of this page said
no published specification for the agent TOML format existed and that the field set should be
treated as observed rather than documented. That was wrong, and it understated what you can rely
on. OpenAI documents custom agents at
[learn.chatgpt.com/docs/agent-configuration/subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
(retrieved 2026-08-31): standalone TOML files in `~/.codex/agents/` for personal agents or
`.codex/agents/` for project-scoped ones, one agent per file. `name`, `description` and
`developer_instructions` are the **required** fields — exactly the three above — and `model`,
`model_reasoning_effort`, `sandbox_mode`, `mcp_servers` and `skills.config` are optional, along
with other `config.toml` keys.

Two details worth knowing before you convert anything:

- **`name` is the source of truth, not the filename.** Matching the two is the simplest
  convention, but Codex identifies the agent by the field.
- **`.codex/agents/` works per project.** If you want these agents on one repo rather than your
  whole machine, put the TOML there and commit it — this page's `~/.codex/agents/` examples are
  the personal-scope case.

⚠️ **What remains unsupported is shipping them through this plugin**, not writing them by hand.
Codex's plugin manifest has no top-level `agents` field, so `codex plugin add dga-kit@dga-kit`
installs the 11 skills and nothing else. Converting an agent is a supported thing you do
yourself; it is not something the install does for you.

### `interface.capabilities`

See [its own section below](#interfacecapabilities--settled-as-far-as-it-can-be) — kept in one
place so the two copies cannot drift apart.

### The manual route

§2 and §3 below are **Claude Code layouts** — `install-skills.sh` and `install-skills.ps1` write to
`~/.claude/skills` and `~/.claude/agents`, and §2 is `.claude/` inside your project. Codex does not
read those directories. The skills themselves are plain Markdown with YAML front matter and no
Claude-specific syntax, so you can copy `skills/` anywhere a tool will read it.

The repository also ships `.codex-plugin/plugin.json` alongside the Claude manifest, and an
[AGENTS.md](AGENTS.md) at the root. `AGENTS.md` is read by Codex and other agentic tools when
working **in this repository** — it carries the contributor contract (what may not be hand-edited,
what must be re-run before committing), not DGA guidance.

**What the manifest looks like, and why.** Paths in it resolve from the **plugin root** — the
directory containing `.codex-plugin/` — not from the manifest file itself. So `"skills":
"./skills/"` points at `<repo>/skills/`, which is where they are. This matches
[ponytail](https://github.com/DietrichGebert/ponytail), a published dual-target plugin whose
`.codex-plugin/plugin.json` uses the same `"./skills/"` form with its skills at the repo root.

> ⚠️ **Rewriting that to `"../skills/"` breaks it** — it would resolve outside the repository.
> An external review recommended exactly that change, reasoning that the path is relative to the
> manifest. It is not. The same review recommended adding `skills`/`agents` keys to
> `.claude-plugin/plugin.json` and changing the marketplace `source`; both would also break
> loading, because Claude Code discovers `skills/` and `agents/` by convention from the plugin
> root. `evals/validate-fixtures.py` now pins all three so the "fix" cannot land by accident.

### `interface.capabilities` — settled as far as it can be

**It is presentation metadata, not a permission or loading gate.** That much is established:
Codex's own specification calls `interface` an *"Interface/UX metadata block for plugin
presentation"*, component loading is declared separately through the top-level `skills`, `hooks`,
`mcpServers` and `apps` fields, and nothing in the installed CLI dispatches on these labels.

**There is no published vocabulary.** Codex's validator accepts any array of non-empty strings;
its scaffold generates an empty array. No enumeration exists in the specification, the validator,
the runtime, or the official OpenAI documentation searched on 2026-08-28.

So this manifest declares `["Instructions"]` **by convention, not by specification**. dga-kit
ships skills and nothing else, and `"Instructions"` is the label the installed ponytail plugin
uses for exactly that component — reserving `"Lifecycle hooks"` for its separate hooks component.
Every OpenAI-authored plugin instead draws from `{Interactive, Read, Write}`, which describes
connector-style plugins rather than instruction packages.

An earlier version declared `["Skills"]`, a label that appears in no specification, no OpenAI
plugin, and no third-party plugin on the machine this was tested on.

If you have documentation that establishes a real vocabulary,
[open an issue](https://github.com/mohamedsamy911/dga-kit/issues); that is a genuinely useful
contribution.

## 2 · Per-project — versioned with your code

Copy or submodule `skills/` into the project as `.claude/skills/`, and `agents/` as
`.claude/agents/`. Preferable when the team wants the kit pinned alongside the code and updated
through review rather than each person installing their own copy.

## 3 · Globally, without the plugin system

Copies the skills into `~/.claude/skills` and the agents into `~/.claude/agents`, so they load in
every project.

**Windows (PowerShell), from inside this folder:**

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1
```

**macOS / Linux / WSL:**

```bash
./install-skills.sh
```

Flags: `-Force` / `--force` overwrites an existing install · `-Uninstall` / `--uninstall` removes
everything it installed.

Both installers verify that every relative cross-reference resolves in the installed layout and
report any that don't. Skills reference each other as siblings (`../dga-design-system/...`), so
the flat `skills/` layout is required — **don't nest them**.

## Naming — why everything is `dga-` prefixed

Both skills and agents are prefixed so nothing in this kit can collide with an agent or skill of
your own. If you already have a `frontend-dev` or a `code-reviewer`, it is untouched.

## Ownership — how the installer decides what it may delete

The prefix is not the safeguard; a manifest is. Every path the installer creates is recorded in
`~/.claude/.dga-kit-manifest`, and **it will only ever delete a path listed there**.

| Situation | What happens |
|---|---|
| A skill directory exists that the manifest does not claim | **Skipped, untouched.** Re-run with `--force` / `-Force` to adopt it — that is the upgrade path from a pre-0.5.1 install, and each adoption is printed as `OVERWRITE`. |
| `--uninstall` with no manifest | **Refuses to run.** It will not delete by name. |
| `--uninstall` with a manifest | Removes a path only if it is **both** listed in the manifest **and** matches the fixed allowlist (`skills/dga-*` from the shipped list, or `agents/dga-*.md`). |
| A manifest entry outside that allowlist | **Refused and reported.** The manifest is editable text, so it is treated as a record, not an authority — a corrupted one can under-delete, never delete something unrelated. |
| Pre-0.5 leftovers (`dga-chakra`, `rga-brand`, `agents/_shared/`) | **Never deleted automatically.** Reported as notes. `--clean-legacy` / `-CleanLegacy` lists each path and requires you to type `DELETE`. |

This matters because `rga-brand` is a plausible name for a skill of your own. Versions before
0.5.1 deleted it by name during a normal install. They no longer do.

## What gets installed

| | |
|---|---|
| **11 skills** | `dga-design-system` · `dga-ui-adapter` · `dga-react` · `dga-rtl-i18n` · `dga-design-review` · `dga-mockup` · `dga-handoff` · `dga-a11y` · `dga-launch-gate` · `dga-tokens-sync` · `dga-brand-overlay` |
| **6 agents** | `dga-designer` · `dga-frontend-architect` · `dga-frontend-dev` · `dga-code-reviewer` · `dga-compliance-auditor` · `dga-content-writer` |

Each agent is self-contained — no shared include files, nothing written outside its own file.

**Adding DGA awareness to an agent of your own** is one line in its markdown:

```markdown
Building for any `.gov.sa` platform? Invoke the `dga-ui-adapter` skill before writing UI, and
`dga-design-system` for what DGA actually requires. Compliance is scored, not stylistic.
```

## Not installed

`evals/`, `harvest/` and `COVERAGE.md` stay in the repo — audit trail and test suite, not runtime
material. The one exception is `harvest/CAPTURE-LOG.md`, which ships inside
`dga-design-system/references/capture-log.md` so the evidence travels with the rules.

## Verify it worked

Ask Claude *"what DGA skills do I have?"*, or run the one piece of the kit that executes:

```bash
node skills/dga-design-system/assets/check-contrast.mjs --test
```

That runs the contrast checker's self-check — the maths against known values — and is the one
thing here safe to gate a build on. `node ... check-contrast.mjs` on its own prints the DGA token
pairings that fail WCAG AA (20: 5 light, 15 dark).

> ⚠️ **Do not put `--ci` in your pipeline as a gate.** It exits non-zero on stock DGA tokens and
> always will: `text.secondary` fails AA on DGA's own backgrounds, and the script never reads your
> source, so nothing you write can turn it green. A gate that can only ever be red gets muted, and
> then it is not a gate. Commit `--json` output as an artefact and diff it; gate on a grep over your
pipeline.

## Caveats

- **These skills are documentation, not code.** They have been run in Claude Code but the
  *interpretation* of DGA's rules has not been signed off by a DGA-literate designer. Values are
  exact; readings of them may not be. Corrections with a citation are the most useful thing you
  can contribute.
- A local (non-plugin) install lives on one machine only — it is not synced to your Anthropic
  account and won't appear in cloud sessions. For a team, use the plugin or the per-project
  install.
