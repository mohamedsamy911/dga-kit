# Report template

```markdown
# DGA design review — {screen name}

**Reviewed:** {date} · **Locale:** {ar / en / both} · **Breakpoint:** {…}
**Source:** {file or URL} · **DGA version:** {from dga-version.md}

## Verdict

**{Ready for development | Not ready — N blockers}**

{One or two sentences. What is the shape of the problem, not a list — the list is below.}

| Blocker | Major | Minor | Note |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

## Findings

### B1 · {Short title}   <!-- illustrative example below — not a real DGA value -->
**Severity:** Blocker · **Pass:** Colour & contrast · **Instances:** 3

**What:** Body text `#7A8A82` on `#F5F7F4` measures 3.1:1. WCAG 2.1 AA requires 4.5:1 for text
under 18.66px.

**Rule:** {DGA rule and its source URL} · WCAG 2.1 AA 1.4.3 Contrast (Minimum)

**Fix:** Use `{token}` (`#…`), which measures {…}:1 on this background.

---

### M1 · {Short title}
…

## Verified clean

Passes run with no findings — say so explicitly, so the designer knows what was actually
checked rather than assuming silence means skipped.

- Layout & grid
- Typography

## Could not verify

- {Anything the artefact didn't let you check, and what you'd need to check it}
```

## Notes on using it

- Prefix IDs by severity (`B1`, `M2`, `N1`) so they stay stable and referenceable across
  review rounds — "B1 is fixed" is a sentence someone can say in a standup.
- **Verified clean** is not padding. A review that lists only problems leaves the designer
  unable to tell a passed check from a skipped one.
- **Could not verify** is what keeps the report honest. Anything you couldn't measure goes
  here, never into a confident finding.
