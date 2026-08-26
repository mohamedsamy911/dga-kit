#!/usr/bin/env node
// Generates tokens.css and tailwind-preset.js from tokens.json.
// Re-run after any DGA re-harvest — see skills/dga-tokens-sync/SKILL.md
// Usage: node generate-tokens.mjs
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const t = JSON.parse(readFileSync(join(here, 'tokens.json'), 'utf8'))
const banner = `/* GENERATED FROM tokens.json — DO NOT EDIT BY HAND.
   Source: ${t.$meta.source} (Platforms Code, National Design System of Saudi Arabia)
   Retrieved: ${t.$meta.retrieved} | Regenerate: node generate-tokens.mjs */\n`

// $-prefixed keys are annotations ($source, $verify, $note) - never token values.
// Every loop below must honour this or annotations leak into the generated output.
const skip = k => k.startsWith('$')
const kebab = s => String(s).replace(/\./g, '-')

/* ---------- CSS ---------- */
const L = []
L.push(banner)
L.push(':root {')
L.push('  /* --- colour primitives --- */')
for (const [fam, ramp] of Object.entries(t.color)) {
  if (skip(fam)) continue
  if (fam === 'base') { for (const [k, v] of Object.entries(ramp)) L.push(`  --dga-color-base-${k}: ${v};`); continue }
  L.push(`  /* ${fam} */`)
  for (const [step, hex] of Object.entries(ramp)) if (!skip(step)) L.push(`  --dga-color-${fam}-${step}: ${hex};`)
}
L.push('')
L.push('  /* --- semantic roles (reference these, not the primitives) --- */')
for (const [group, roles] of Object.entries(t.role)) {
  if (skip(group)) continue
  L.push(`  /* ${group} */`)
  for (const [role, hex] of Object.entries(roles)) if (!skip(role)) L.push(`  --dga-${group}-${kebab(role)}: ${hex};`)
}
L.push('')
L.push('  /* --- spacing (numeric, 4px base) --- */')
for (const [k, v] of Object.entries(t.space.numeric)) if (!skip(k)) L.push(`  --dga-space-${kebab(k)}: ${v};`)
L.push('  /* --- spacing (named) --- */')
for (const [k, v] of Object.entries(t.space.named)) if (!skip(k)) L.push(`  --dga-space-${k}: ${v};`)
L.push('')
L.push('  /* --- radius --- */')
for (const [k, v] of Object.entries(t.radius)) if (!skip(k)) L.push(`  --dga-radius-${k}: ${v};`)
L.push('')
L.push('  /* --- width --- */')
for (const [k, v] of Object.entries(t.width)) if (!skip(k)) L.push(`  --dga-width-${k}: ${v};`)
L.push('')
L.push('  /* --- container --- */')
for (const [k, v] of Object.entries(t.container)) if (!skip(k)) L.push(`  --dga-container-${k}: ${v};`)
L.push('')
L.push('  /* --- elevation --- */')
for (const [k, v] of Object.entries(t.shadow)) if (!skip(k)) L.push(`  --dga-shadow-${k}: ${v};`)
L.push('')
L.push('  /* --- typography: IBM Plex Sans. Arabic face TODO(verify) with DGA --- */')
L.push(`  --dga-font-sans: "IBM Plex Sans", system-ui, sans-serif;`)
for (const [name, v] of Object.entries(t.typography.scale)) {
  if (skip(name)) continue
  L.push(`  --dga-text-${name}-size: ${v.size};`)
  L.push(`  --dga-text-${name}-line: ${v.lineHeight};`)
  if (v.tracking) L.push(`  --dga-text-${name}-tracking: ${v.tracking};`)
}
L.push('}')
L.push('')
L.push('/* Arabic is a connected script — letter-spacing breaks the joins.')
L.push('   DGA applies -2% tracking to Display 2xl..md; it must never reach Arabic text. */')
L.push(':root:lang(ar), [lang="ar"], [dir="rtl"] { letter-spacing: normal !important; }')
L.push('')
L.push('/* TODO(harvest): dark theme values exist in the PC 1.0 Figma variable collections')
L.push('   but are not exposed as CSS variables on the public site. Do not invent them. */')
writeFileSync(join(here, 'tokens.css'), L.join('\n') + '\n')

/* ---------- Tailwind ---------- */
const colors = {}
for (const [fam, ramp] of Object.entries(t.color)) {
  if (skip(fam)) continue
  colors[fam] = {}
  for (const [step, hex] of Object.entries(ramp)) if (!skip(step)) colors[fam][step] = hex
}
for (const [group, roles] of Object.entries(t.role)) {
  if (skip(group)) continue
  colors[group] = {}
  for (const [role, hex] of Object.entries(roles)) if (!skip(role)) colors[group][kebab(role)] = hex
}
const spacing = {}
for (const [k, v] of Object.entries(t.space.numeric)) if (!skip(k)) spacing[k] = v
for (const [k, v] of Object.entries(t.space.named)) if (!skip(k)) spacing[k] = v
const radius = {}; for (const [k, v] of Object.entries(t.radius)) if (!skip(k)) radius[k] = v
const shadow = {}; for (const [k, v] of Object.entries(t.shadow)) if (!skip(k)) shadow[k] = v
const fontSize = {}
for (const [n, v] of Object.entries(t.typography.scale)) if (!skip(n)) fontSize[n] = [v.size, { lineHeight: v.lineHeight, ...(v.tracking ? { letterSpacing: v.tracking } : {}) }]

const preset = `// GENERATED FROM tokens.json — DO NOT EDIT BY HAND.
// Source: ${t.$meta.source} | Retrieved: ${t.$meta.retrieved}
// Regenerate: node generate-tokens.mjs
//
// Breakpoints follow DGA: Mobile 0-599 | Tablet 600-959 | Desktop 960-1279 | XL 1280+
// Use LOGICAL utilities only (ms-/me-/ps-/pe-/start-/end-), never ml-/mr-/left-/right-.
export default {
  theme: {
    screens: { sm: '600px', md: '960px', lg: '1280px' },
    extend: {
      colors: ${JSON.stringify(colors, null, 6).replace(/\n/g, '\n    ')},
      spacing: ${JSON.stringify(spacing, null, 6).replace(/\n/g, '\n    ')},
      borderRadius: ${JSON.stringify(radius, null, 6).replace(/\n/g, '\n    ')},
      boxShadow: ${JSON.stringify(shadow, null, 6).replace(/\n/g, '\n    ')},
      fontSize: ${JSON.stringify(fontSize, null, 6).replace(/\n/g, '\n    ')},
      maxWidth: { paragraph: '${t.container['paragraph-max-width']}', container: '${t.container['max-width-desktop']}' },
      fontFamily: { sans: ['IBM Plex Sans', 'system-ui', 'sans-serif'] },
    },
  },
}
`
writeFileSync(join(here, 'tailwind-preset.js'), preset)
console.log('wrote tokens.css and tailwind-preset.js')
