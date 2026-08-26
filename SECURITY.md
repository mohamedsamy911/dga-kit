# Security and contact

## Reporting a problem

**Email:** mohamedadel74@gmail.com — put `dga-kit` in the subject.
For anything non-sensitive, open an issue instead: https://github.com/mohamedsamy911/dga-kit/issues

Expect an acknowledgement within a week. This is a volunteer-maintained project with no SLA; if
something is urgent for a live government platform, do not wait on this repository — verify
directly with DGA at DS-DGA@dga.gov.sa.

## What counts as a security issue here

This kit ships **documentation, JSON/CSS token files, two Node scripts and two installer
scripts**. It has no runtime, no network calls and no dependencies. The realistic risk surface is:

| Area | Why it matters |
|---|---|
| **The installers** | They write to and delete from `~/.claude`. A path-handling bug could remove files the kit did not install. Report immediately. |
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
