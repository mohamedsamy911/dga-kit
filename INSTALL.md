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

### Install the six Codex agents separately

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

The repository supplies all six native TOML definitions in [`codex-agents/`](codex-agents/).
They are generated from the Claude Markdown definitions, not maintained as a second set of
rules. No Claude installation or automatic migration is required.

**Prerequisites:** install and enable the 11 skills through the Codex plugin above, and have
**Node 18+ and Git**. No `npm install`, no Python, and no clone of your own — but Git must be on
PATH, because npm resolves a `github:` spec by cloning this repository for you. Without it `npx`
fails with an ENOENT from git. The same command works on Windows, macOS, Linux and WSL.

**Everything Codex can take, in one command:**

```bash
npx github:mohamedsamy911/dga-kit --codex
```

That copies the six agents into `~/.codex/agents/` **and** runs `codex plugin marketplace add`
/ `codex plugin add` for the skills. If the `codex` CLI is not callable it installs the agents,
says so, and prints the two commands — it does not write Codex's `config.toml` by hand.

**Agents into one project instead** (the TOMLs land in that project's `.codex/agents/` and can be
committed with it; each teammate still needs the skills in their own Codex session):

```bash
npx github:mohamedsamy911/dga-kit --codex --agents --project .
```

**Skills only:**

```bash
npx github:mohamedsamy911/dga-kit --codex --skills
```

The destination is `~/.codex/agents/`, or `CODEX_HOME/agents/` if `CODEX_HOME` is set to an
absolute path. The installer prints the full destination. `--project` ignores `CODEX_HOME`.

Add `--dry-run` to either to see the plan without writing anything.

**Then start a new Codex session in the target project** and explicitly request a named agent,
for example: *"Use the dga-code-reviewer subagent to review this change. Do not edit files."*
Check that Codex actually launches that named role and can read the installed DGA skills.
File installation and TOML validation alone do not prove runtime discovery on your Codex version.
**Installing the agents changes nothing else.** Copying the six TOML files does not touch
`config.toml`, permissions, models or plugin settings.

⚠️ **Installing the Codex *skills* does.** `--codex --skills` (and the default run) invokes
`codex plugin marketplace add` and `codex plugin add` on your behalf, and Codex registers the
plugin in `~/.codex/config.toml` under `[plugins."dga-kit@dga-kit"]`. That is the supported way
and the only one — Codex serves plugin skills from its own cache plus that registration, not from
a directory anything else can write. The installer does not edit `config.toml` itself; Codex
does. Use `--codex --agents` if you want the file copy and no configuration change, or
`--dry-run` to see the exact commands first.

**Safety and updates.** Two guarantees hold for **both** tools: linked paths — symlinks,
dangling symlinks and Windows junctions — are refused, on the path and on every parent, and
files are created exclusively so a link planted mid-install cannot be followed. The Claude
manifest is checked before any file is copied, so a run that cannot record what it installs
writes nothing at all.

For **Codex agents** specifically, all six source files and every destination conflict are
checked before copying, and any different file — including a migrated or customized agent —
aborts the whole install rather than replacing it. Claude's rule is different, and the table
below is the one to read.

⚠️ **The two tools have deliberately different rules.** Read the row for the one you mean:

| | Codex agents | Claude skills & agents |
|---|---|---|
| An existing file that **differs** | **Always refused.** The install aborts; nothing is written. | Skipped with a note, unless `--force`. |
| `--force` | **No effect.** There is no override — a differing Codex agent is never overwritten. | Overwrites, and adopts a `dga-*` path this kit did not record. Each is printed as `OVERWRITE`. |
| How to update a changed file | Move yours aside, then rerun. | `--force`, or move yours aside and rerun. |
| `--uninstall` | Removes only a **byte-identical** copy. An edited agent is kept and reported. | Removes a path only if it is in the manifest **and** on the fixed allowlist. |

`--uninstall` obeys the same `--claude` / `--codex` / `--skills` / `--agents` selectors as an
install, and preserves the manifest entries it was told to leave.

Uninstall does **not** remove the Codex skills plugin: that is Codex's to manage, with
`codex plugin remove dga-kit@dga-kit`. Updating or uninstalling the skills plugin does **not**
update or remove the separately copied agents. An interrupted copy can leave a partial install;
update or remove the separately copied agents. An interrupted copy can leave a partial install;
inspect the printed destination before retrying.

**Format and conversion.** OpenAI documents native custom agents as one TOML file per role in
the personal or project agent directory, requiring `name`, `description` and
`developer_instructions`. This kit also sets `sandbox_mode = "read-only"` for the code reviewer,
compliance auditor and frontend architect. These are defaults; Codex's parent-session runtime
permissions still apply. No agent pins a model or reasoning effort, and Claude `tools` lists
are not copied as unsupported Codex fields. See the
[official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
(retrieved 2026-08-31).

The complete Markdown body is preserved after a short Codex-specific skill-lookup preamble.
That preamble resolves references through the installed skill's `SKILL.md` location instead of
assuming the skills live beside the agent files. Optional external skills, such as `design`,
are not bundled. These definitions remain unofficial DGA guidance, not compliance certification.

**Maintainers:** edit `agents/*.md`, then regenerate and check (Python 3.11+ and PyYAML):

```bash
python evals/build-codex-agents.py
python evals/build-codex-agents.py --check
python evals/test-codex-agents.py
```

Never hand-edit `codex-agents/*.toml`. CI checks source/output parity and runs the installer
regressions in scratch directories on Windows, macOS and Linux.

### `interface.capabilities`

See [its own section below](#interfacecapabilities--settled-as-far-as-it-can-be) — kept in one
place so the two copies cannot drift apart.

### The manual route

§2 and §3 below are **Claude Code layouts** — the installer writes to
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

So this manifest declares `["Instructions"]` **by convention, not by specification**. The Codex
plugin registers skills only, and `"Instructions"` is the label the installed ponytail plugin
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

**Any platform** — Windows, macOS, Linux or WSL, same command:

```bash
npx github:mohamedsamy911/dga-kit --claude
```

Flags: `--force` overwrites an existing install (and adopts one this kit did not record) ·
`--uninstall` removes only what it installed · `--clean-legacy` removes pre-0.5 paths after you
type DELETE · `--dry-run` prints the plan and writes nothing.

The installer verifies that every relative cross-reference resolves in the installed layout and
reports any that don't — it exits non-zero if any is broken.
the flat `skills/` layout is required — **don't nest them**.

## Naming — why everything is `dga-` prefixed

Both skills and agents are prefixed so nothing in this kit can collide with an agent or skill of
your own. If you already have a `frontend-dev` or a `code-reviewer`, it is untouched.

## Ownership — how the installer decides what it may delete

This section covers the **Claude installers**. The separate Codex-agent installer never deletes
or overwrites files; see [its safety and update instructions above](#install-the-six-codex-agents-separately).

The prefix is not the safeguard; a manifest is. Every path the installer creates is recorded in
`~/.claude/.dga-kit-manifest`, and **it will only ever delete a path listed there**.

| Situation | What happens |
|---|---|
| A skill directory exists that the manifest does not claim | **Skipped, untouched.** Re-run with `--force` to adopt it — that is the upgrade path from a pre-0.5.1 install, and each adoption is printed as `OVERWRITE`. |
| `--uninstall` with no manifest | **Refuses to run.** It will not delete by name. |
| `--uninstall` with a manifest | Removes a path only if it is **both** listed in the manifest **and** matches the fixed allowlist (`skills/dga-*` from the shipped list, or `agents/dga-*.md`). |
| A manifest entry outside that allowlist | **Refused and reported.** The manifest is editable text, so it is treated as a record, not an authority — a corrupted one can under-delete, never delete something unrelated. |
| Pre-0.5 leftovers (`dga-chakra`, `rga-brand`, `agents/_shared/`) | **Never deleted automatically.** Reported as notes. `--clean-legacy` lists each path and requires you to type `DELETE`. |

This matters because `rga-brand` is a plausible name for a skill of your own. Versions before
0.5.1 deleted it by name during a normal install. They no longer do.

## What gets installed

| | |
|---|---|
| **11 skills** | `dga-design-system` · `dga-ui-adapter` · `dga-react` · `dga-rtl-i18n` · `dga-design-review` · `dga-mockup` · `dga-handoff` · `dga-a11y` · `dga-launch-gate` · `dga-tokens-sync` · `dga-brand-overlay` |
| **6 agents** | `dga-designer` · `dga-frontend-architect` · `dga-frontend-dev` · `dga-code-reviewer` · `dga-compliance-auditor` · `dga-content-writer` |

Each agent is self-contained — no shared include files, nothing written outside its own file.
Claude uses `agents/*.md`; Codex uses the generated `codex-agents/*.toml` through the separate
installation step above. Installing the Codex plugin alone still installs only the skills.

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
