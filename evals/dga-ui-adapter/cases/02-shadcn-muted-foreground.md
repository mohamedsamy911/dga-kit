## input
A shadcn/ui project's `globals.css`:

```css
:root {
  --background: var(--dga-background-body);
  --foreground: var(--dga-text-default);
  --muted-foreground: var(--dga-text-secondary);
  --radius: var(--dga-radius-md);
}
```

## expect
- finds: `--muted-foreground: var(--dga-text-secondary)` — the same 2.30:1 failure as case 01, and
  `--muted-foreground` drives helper text, placeholders and timestamps across every shadcn
  component, so one line breaks contrast app-wide
- fix: `var(--dga-text-secondary-paragraph)`
- must NOT flag `--radius: var(--dga-radius-md)` as wrong — it is correct
- may note that DGA's radius scale is **not monotonic** (`2xl` and `3xl` are smaller than `xl`),
  as a Note, not a finding

## traps
The same rule through CSS variables rather than a JS theme, paired with a correct line to see
whether the model flags indiscriminately.
