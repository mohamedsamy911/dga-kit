# Security and contact

## Reporting a problem

**Email:** mohamedadel74@gmail.com — put `dga-kit` in the subject.
For anything non-sensitive, open an issue instead: https://github.com/mohamedsamy911/dga-kit/issues

Expect an acknowledgement within a week. This is a volunteer-maintained project with no SLA; if
something is urgent for a live government platform, do not wait on this repository — verify
directly with DGA at DS-DGA@dga.gov.sa.

## What counts as a security issue here

This kit ships **documentation, JSON/CSS token files, Node scripts, Python tooling and two
installer scripts**. Nothing here is a runtime you deploy. Two things it *does* do, which an
earlier version of this file wrongly denied:

- **It makes outbound network calls.** `harvest/sources.py` and `harvest/deep.py` fetch
  `design.dga.gov.sa` — the shell, the CSS and JS bundles (~19 MB on a deploy), `sitemap.xml` and
  `robots.txt`. Only when you run them, or via the weekly GitHub Action.
- **It has one optional dependency.** `harvest/deep.py --playwright` imports Playwright, which you
  must install yourself and which downloads a Chromium build. The `--capture` path — the tested
  one — needs nothing beyond the standard library.

What the installers place in `~/.claude` is mostly inert Markdown (33 files) plus a little JSON —
but **not only** that. The skill directories also carry `.mjs`, `.js`, `.ts`, `.mts` and `.css`
assets, including two runnable Node scripts: `check-contrast.mjs` and `generate-tokens.mjs`.

**None of it executes on its own.** Installing runs nothing; the scripts run only when you invoke
them, and both read `tokens.json` and write only inside the kit's own `assets/`. But "inert
Markdown and JSON" was wrong, and if you are reviewing what lands on your machine, review those
files too. The harvest and eval tooling is **not** installed; it stays in the repo.

| Area | Why it matters |
|---|---|
| **The installers** | They write to and delete from `~/.claude`. A path-handling bug could remove files the kit did not install. Report immediately. |
| **`harvest/sources.py`, `harvest/deep.py`** | Outbound HTTP to DGA, and they write `source-inventory.json`, `FRESHNESS.md` and `snapshots/`. Capture files are **untrusted input**: their keys become paths, so a traversal here is a real finding. Report it. |
| **`harvest/deep.py --playwright`** | Runs a headless browser against a live site. Untested by CI, and the widest surface in the repo. |
| **`check-contrast.mjs` / `generate-tokens.mjs`** | They read `tokens.json` and write into the kit's own `assets/`. They take no network input. |
| **Token or rule values** | Not a security issue, but a **correctness** one — see below. |

Both installers only delete paths recorded in `~/.claude/.dga-kit-manifest`, and refuse to
uninstall without it. If you find a way to make either delete something it did not install,
that is a security bug and I want to hear about it before it is public.

## Incorrect compliance guidance

A wrong rule in a compliance tool can cause real harm — a platform ships believing it is
compliant and fails an assessment. **Report factual errors as issues, with the DGA page URL and
what it actually says.** Corrections with a citation are the most valuable contribution this
project can receive, and they are treated with the same priority as bugs.

Known-unverified areas are listed in [COVERAGE.md](COVERAGE.md). Nothing there is hidden.

## What this project will not do

- It will never ask for credentials, tokens, or platform access.
- It makes no network requests at runtime.
- It will not claim DGA endorsement, certification, or approval, because it has none.

## Scope of the guidance

This is an **unofficial** reading of publicly published DGA material. It is not a compliance
certification and cannot make your platform compliant. Treat every rule as a prompt to verify,
not as an authority. Where the stakes are high, confirm with DGA directly.
