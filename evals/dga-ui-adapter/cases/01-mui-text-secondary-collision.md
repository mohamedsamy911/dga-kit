## input
A team wires the DGA tokens into a MUI theme for a `.gov.sa` portal:

```ts
palette: {
  text: { primary: t.role.text.default, secondary: t.role.text.secondary },
  background: { default: t.role.background.body, paper: t.role.background.card },
}
```

They ask whether the theme is DGA-compliant.

## expect
- finds: `t.role.text.secondary` is DGA's gold **#dba102** and measures **2.30:1 on white** —
  below the 4.5:1 small-text threshold *and* the 3:1 large-text one
- names the mechanism: **MUI's `text.secondary` is a muted grey; DGA's is gold.** Mapping
  name-to-name looks obviously correct and ships an AA failure on every muted caption in the app
- fix names: `t.role.text['secondary-paragraph']` (#6c727e)
- points at `check-contrast.mjs` as the enforcement, not a code review
- must NOT: accept it because the token is genuinely DGA's

## traps
Both sides of the mapping are named `text.secondary`. This is the single highest-value finding
in the skill and the one a reviewer is most likely to skim past.
