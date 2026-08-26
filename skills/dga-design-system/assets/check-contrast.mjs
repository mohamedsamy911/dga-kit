#!/usr/bin/env node
/**
 * WCAG 2.1 contrast check over DGA's own semantic token pairings.
 *
 *   node check-contrast.mjs            # report every text role x light background
 *   node check-contrast.mjs --ci       # exit 1 if any pairing fails AA
 *   node check-contrast.mjs --json     # machine-readable
 *
 * Reads tokens.json, so it stays correct across a re-harvest. This is the check behind
 * references/CONTRAST-AUDIT.md and rule 2 of dga-ui-adapter — DGA publishes a text role that
 * fails AA on its own backgrounds, and no build step catches that on its own.
 *
 * SCOPE — read before wiring this into CI:
 *   • It audits DGA's OWN published role x background table. It never reads your source, so
 *     nothing you write can change its exit code.
 *   • It does not score the pairings your theme composes (colorPalette fg-on-muted, hover
 *     states, text over a brand fill). That is where AA breaks in a real build.
 *   • --ci therefore cannot go green on stock DGA tokens: text.secondary fails, permanently.
 *     Run it as a committed artefact (--json); gate your build on a grep over your own source.
 *   • The -light / oncolor-* / *disabled* roles are marked `expected` below: they are
 *     dark-surface tokens, NOT failures, and are excluded from the verdict on purpose.
 *
 * Thresholds: AA normal 4.5, AA large 3.0 (>=18.66px bold or >=24px regular).
 */
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const t = JSON.parse(readFileSync(join(here, 'tokens.json'), 'utf8'))

/** #rgb | #rrggbb | #rrggbbaa -> [r,g,b], alpha composited over `over`. */
export function parseHex(hex, over = [255, 255, 255]) {
  let h = hex.trim().replace('#', '')
  if (h.length === 3) h = h.split('').map((c) => c + c).join('')
  if (h.length !== 6 && h.length !== 8) throw new Error(`not a hex colour: ${hex}`)
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16))
  if (h.length === 6) return [r, g, b]
  const a = parseInt(h.slice(6, 8), 16) / 255
  return [r, g, b].map((c, i) => Math.round(c * a + over[i] * (1 - a)))
}

/** WCAG 2.x relative luminance. */
export function luminance([r, g, b]) {
  const f = (c) => {
    const s = c / 255
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4
  }
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
}

/** Contrast ratio, 1..21. Order-independent. */
export function ratio(fg, bg) {
  const bgRgb = parseHex(bg)
  const a = luminance(parseHex(fg, bgRgb))
  const b = luminance(bgRgb)
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)
}

const round = (n) => Math.round(n * 100) / 100

// Backgrounds a body page actually uses. Surface roles only - not the solid brand fills, which
// are paired with the oncolor-* text roles instead.
const SURFACES = ['white', 'body', 'card', 'menu', 'brand-light']

const results = []
for (const [role, fg] of Object.entries(t.role.text)) {
  if (role.startsWith('$')) continue
  for (const surface of SURFACES) {
    const bg = t.role.background[surface]
    if (!bg) continue
    const r = round(ratio(fg, bg))
    results.push({
      text: `text.${role}`, fg,
      background: `background.${surface}`, bg,
      ratio: r,
      aaNormal: r >= 4.5,
      aaLarge: r >= 3,
      // A dark-surface token failing on a light surface is expected, not a defect.
      expected: role.endsWith('-light') || role.startsWith('oncolor') || role.includes('disabled'),
    })
  }
}

const fails = results.filter((x) => !x.aaLarge && !x.expected)
const largeOnly = results.filter((x) => x.aaLarge && !x.aaNormal && !x.expected)
const marginal = results.filter((x) => x.aaNormal && x.ratio < 5 && !x.expected)

if (process.argv.includes('--json')) {
  console.log(JSON.stringify({ results, fails, largeOnly, marginal }, null, 2))
} else {
  const line = (x) => `  ${x.text.padEnd(28)} ${x.fg.padEnd(10)} on ${x.background.padEnd(24)} ${String(x.ratio).padStart(6)}:1`
  console.log(`DGA contrast check - ${t.$meta.systemName}`)
  console.log(`source ${t.$meta.source} retrieved ${t.$meta.retrieved}\n`)

  console.log(`FAIL - below AA at every size (${fails.length})`)
  fails.length ? fails.forEach((x) => console.log(line(x))) : console.log('  none')

  console.log(`\nLARGE TEXT ONLY - >=3:1 but <4.5:1 (${largeOnly.length})`)
  largeOnly.length ? largeOnly.forEach((x) => console.log(line(x))) : console.log('  none')

  console.log(`\nMARGINAL - passes AA by <0.5. Any opacity breaks these (${marginal.length})`)
  marginal.length ? marginal.forEach((x) => console.log(line(x))) : console.log('  none')

  console.log(`\n${results.length} pairings checked. ${results.filter((x) => x.expected).length} dark-surface/oncolor/disabled roles excluded from the verdict.`)
  console.log(`Those are dark-surface tokens, NOT failures - do not delete them from a theme.`)
  if (fails.length) {
    const roles = [...new Set(fails.map((x) => x.text))]
    const one = roles.length === 1
    console.log(`\n${one ? 'This is a real DGA token' : 'These are real DGA tokens'} designated for text: ${roles.join(', ')}.`)
    console.log(`Do not use ${one ? 'it' : 'them'} on a light surface at any size. secondary-gold.800`)
    console.log(`(#945c01) is the first gold step that clears AA on white.`)
  }
}

if (process.argv.includes('--ci') && fails.length) process.exit(1)

// --- self-check: node check-contrast.mjs --test ---
if (process.argv.includes('--test')) {
  const assert = (c, m) => { if (!c) { console.error('FAIL ' + m); process.exit(1) } }
  assert(round(ratio('#000000', '#ffffff')) === 21, 'black on white is 21:1')
  assert(round(ratio('#ffffff', '#ffffff')) === 1, 'white on white is 1:1')
  assert(round(ratio('#ffffff', '#000000')) === 21, 'ratio is order-independent')
  assert(round(ratio('#777777', '#ffffff')) === 4.48, '#777 on white is 4.48:1 (known value)')
  assert(round(ratio('#dba102', '#ffffff')) === 2.3, 'DGA text.secondary on white is 2.30:1')
  // #ffffffcc (oncolor-secondary) composited over white must resolve to white
  assert(round(ratio('#ffffffcc', '#ffffff')) === 1, 'alpha is composited, not ignored')
  assert(parseHex('#fff').join() === '255,255,255', 'shorthand hex expands')
  assert(fails.every((x) => !x.expected), 'expected-fail roles never reach the verdict')
  console.log('self-check passed')
}
