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

The repository also ships `.codex-plugin/plugin.json` alongside the Claude manifest, and an
[AGENTS.md](AGENTS.md) at the root. `AGENTS.md` is read by Codex and other agentic tools when
working **in this repository** — it carries the contributor contract (what may not be hand-edited,
what must be re-run before committing), not DGA guidance.

⚠️ The `.codex-plugin/plugin.json` schema has not been verified against a published Codex plugin
specification. If Codex rejects it, that manifest is the thing to correct — the skills themselves
are plain Markdown and work regardless of how they are loaded.

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

That runs the contrast checker's self-check. `node ... check-contrast.mjs` on its own prints the
DGA token pairings that fail WCAG AA; add `--ci` to make it exit non-zero, and put it in your
pipeline.

## Caveats

- **These skills are documentation, not code.** They have been run in Claude Code but the
  *interpretation* of DGA's rules has not been signed off by a DGA-literate designer. Values are
  exact; readings of them may not be. Corrections with a citation are the most useful thing you
  can contribute.
- A local (non-plugin) install lives on one machine only — it is not synced to your Anthropic
  account and won't appear in cloud sessions. For a team, use the plugin or the per-project
  install.
