# Installing dga-kit

Three ways. Pick one.

## 1 · As a plugin — recommended

```bash
/plugin marketplace add <your-org>/dga-kit
```

```bash
/plugin install dga-kit@dga-kit
```

Restart Claude Code. All 11 skills and 6 agents load together, update with the repo, and
uninstall cleanly with `/plugin uninstall dga-kit`.

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
your own. If you already have a `frontend-dev` or a `code-reviewer`, it is untouched. Nothing
here overwrites anything you did not install from here.

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
