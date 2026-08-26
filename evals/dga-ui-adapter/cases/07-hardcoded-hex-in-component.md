## input
The project has a fully wired DGA theme. A new component ships with:

```tsx
<div style={{ backgroundColor: '#f9fafb', borderRadius: 8 }}>
```

The developer points out that `#f9fafb` **is** the correct DGA value for `background.body`.

## expect
- still a finding: the value is right and the **reference** is wrong. A literal hex cannot follow
  the theme, so it survives a dark-theme rollout, a re-harvest and a brand overlay by silently
  going stale
- notes DGA documents dark values for every semantic role, so a hardcoded light value is a
  guaranteed dark-mode bug the day that lands
- fix: reference the semantic role, and the same for `borderRadius: 8` -> the radius token
- must NOT: accept "but it's the correct value" as closing the issue

## traps
The developer is factually right about the value. The rule is about the reference, not the colour,
and a model that only diffs hex values against `tokens.json` will pass this through.
