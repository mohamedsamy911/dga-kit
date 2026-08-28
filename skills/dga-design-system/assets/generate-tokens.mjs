#!/usr/bin/env node
// Generates tokens.css and tailwind-preset.js from tokens.json.
// Re-run after any DGA re-harvest — see skills/dga-tokens-sync/SKILL.md
// Usage: node generate-tokens.mjs
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const t = JSON.parse(readFileSync(join(here, 'tokens.json'), 'utf8'))
// Light and dark were harvested on different dates by different methods (light from the live
// :root, dark from the CSS bundle). One date on the banner would be wrong for half the file.
const darkRetrieved = t.role?.dark?.$source?.retrieved
const banner = `/* GENERATED FROM tokens.json — DO NOT EDIT BY HAND.
   Source: ${t.$meta.source} (Platforms Code, National Design System of Saudi Arabia)
   Light values retrieved: ${t.$meta.retrieved}${darkRetrieved ? `
   Dark values retrieved:  ${darkRetrieved} (held in tokens.json, not emitted here — see below)` : ''}
   Regenerate: node generate-tokens.mjs */\n`

// $-prefixed keys are annotations ($source, $verify, $note) - never token values.
// Every loop below must honour this or annotations leak into the generated output.
const skip = k => k.startsWith('$')
const kebab = s => String(s).replace(/\./g, '-')
// DGA publishes display tracking as a percentage (-2%). CSS letter-spacing accepts <length>
// or normal only - percentages were proposed in css-text-4 and never shipped, so a browser
// drops the declaration silently. tokens.json keeps DGA's published value so a re-harvest
// diffs clean; the conversion to em happens here, at the boundary.
const em = v => (typeof v === 'string' && v.endsWith('%')) ? `${parseFloat(v) / 100}em` : v

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
  // `dark` is a whole theme, not a role group - it gets its own selector below.
  if (skip(group) || group === 'dark') continue
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
  if (v.tracking) L.push(`  --dga-text-${name}-tracking: ${em(v.tracking)};`)
}
L.push('}')
L.push('')
L.push('/* Arabic is a connected script — letter-spacing breaks the joins.')
L.push('   DGA\'s design spec says -2% tracking on Display 2xl..md; CSS letter-spacing does not')
L.push('   accept percentages (proposed in css-text-4, never shipped), so the em equivalent')
L.push('   -0.02em is used. It must never reach Arabic text. */')
L.push(':root:lang(ar), [lang="ar"], [dir="rtl"] { letter-spacing: normal !important; }')
L.push('')
// --- dark theme: DELIBERATELY NOT EMITTED ------------------------------------
// The 402 harvested dark values live in tokens.json under `role.dark` and are audited by
// `check-contrast.mjs --theme dark`. They are NOT written into this stylesheet, and that is a
// safety decision, not an oversight:
//
//   1. DGA publishes them under `[data-theme=dark] :root`, which can never match (:root is
//      <html>; a descendant combinator needs an ancestor it does not have). So on a real DGA
//      platform the dark theme is INERT - and inert is safe.
//   2. Emitting the corrected selector `:root[data-theme="dark"]` would make it live. Any
//      consumer already using `data-theme="dark"` - Chakra v3 does, out of the box - would
//      silently activate it. That turns a harmless upstream bug into a live accessibility
//      regression in someone else's product.
//   3. It cannot be made safe from DGA's own values. `text.error` has a cited substitute
//      (red.300 #fca19b, which DGA itself uses for notification.text-error in dark) and so does
//      `text.primary` (sa-flag.300 #88d8ad). But the five `*-light` status surfaces have NONE:
//      every dark variant DGA publishes for them - under notification-, tag- and featuredicons-
//      - still resolves to the same near-white value. White text on them is 1.05:1. Inventing a
//      dark tint would break `cite or omit`.
//
// So: values retained for audit, stylesheet stays safe. An entity that wants dark mode owns the
// remediation and records it in dga-brand-overlay. See tokens.json role.dark.$verify.
L.push('/* Dark theme is NOT emitted here, on purpose.')
L.push('   DGA publishes 402 dark values under `[data-theme=dark] :root` - a selector that can')
L.push('   never match, so upstream the theme is inert. Emitting a corrected selector would')
L.push('   activate it for anyone already using data-theme="dark" (Chakra v3 does), and it')
L.push('   cannot be made safe: five *-light status surfaces have no dark tint anywhere in')
L.push('   DGA\'s output, so white text on them measures 1.05:1.')
L.push('   Values: tokens.json role.dark. Audit: node check-contrast.mjs --theme dark. */')
writeFileSync(join(here, 'tokens.css'), L.join('\n') + '\n')

/* ---------- Tailwind ---------- */
const colors = {}
for (const [fam, ramp] of Object.entries(t.color)) {
  if (skip(fam)) continue
  colors[fam] = {}
  for (const [step, hex] of Object.entries(ramp)) if (!skip(step)) colors[fam][step] = hex
}
for (const [group, roles] of Object.entries(t.role)) {
  // The dark group is excluded from BOTH generated outputs, deliberately - see the dark-theme
  // block below. It is NOT emitted to tokens.css, and no `darkMode` strategy is set here.
  //
  // This comment used to claim the opposite ("dark ships as CSS custom properties in tokens.css
  // instead; `darkMode` below points Tailwind at the same attribute"), which described neither
  // output and read as an instruction to wire dark up. Acting on it would activate DGA's
  // unactivatable dark theme, including five status surfaces that measure 1.05:1.
  if (skip(group) || group === 'dark') continue
  colors[group] = {}
  for (const [role, hex] of Object.entries(roles)) if (!skip(role)) colors[group][kebab(role)] = hex
}
const spacing = {}
for (const [k, v] of Object.entries(t.space.numeric)) if (!skip(k)) spacing[k] = v
for (const [k, v] of Object.entries(t.space.named)) if (!skip(k)) spacing[k] = v
const radius = {}; for (const [k, v] of Object.entries(t.radius)) if (!skip(k)) radius[k] = v
const shadow = {}; for (const [k, v] of Object.entries(t.shadow)) if (!skip(k)) shadow[k] = v
const fontSize = {}
for (const [n, v] of Object.entries(t.typography.scale)) if (!skip(n)) fontSize[n] = [v.size, { lineHeight: v.lineHeight, ...(v.tracking ? { letterSpacing: em(v.tracking) } : {}) }]

const preset = `// GENERATED FROM tokens.json — DO NOT EDIT BY HAND.
// Source: ${t.$meta.source} | Light values retrieved: ${t.$meta.retrieved}${darkRetrieved ? ` | dark ${darkRetrieved}, not shipped` : ''}
// Regenerate: node generate-tokens.mjs
//
// Breakpoints follow DGA: Mobile 0-599 | Tablet 600-959 | Desktop 960-1279 | XL 1280+
// Use LOGICAL utilities only (ms-/me-/ps-/pe-/start-/end-), never ml-/mr-/left-/right-.
export default {
  // No darkMode strategy is set, on purpose. This preset ships no dark colours (see the
  // dark-theme note in generate-tokens.mjs), and setting darkMode to 'selector' here would
  // silently switch a consumer's dark: utilities away from the prefers-color-scheme default
  // they expect - a behaviour change in return for colours we do not provide.
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
