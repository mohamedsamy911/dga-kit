## input
A Tailwind config extends the DGA display scale and a developer applies it to a bilingual page:

```html
<h1 class="text-display-lg tracking-tight">الخدمات الرقمية</h1>
```

## expect
- finds: DGA's display scale already carries **-0.02em tracking** (design spec says −2%; CSS
  `letter-spacing` does not accept percentages), and `tracking-tight` compounds it.
  Arabic is a **connected script** — letter-spacing breaks the joins and renders the word as
  detached glyphs
- fix: scope tracking to Latin, or zero it under `[dir="rtl"]`
- must NOT: describe this as a stylistic preference or a "may look better" note. It is kit
  guidance, not a DGA rule — DGA says nothing about tracking Arabic — but where a browser applies
  the tracking it breaks the joins, making Arabic text wrong rather than ugly
- must NOT: call it a DGA rule

## traps
Nothing errors, nothing fails a build, and it looks correct to a reviewer who does not read
Arabic. Severity is as much the test here as detection.
