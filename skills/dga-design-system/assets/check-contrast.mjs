#!/usr/bin/env node
/**
 * WCAG 2.1 contrast check over DGA's own semantic token pairings.
 *
 *   node check-contrast.mjs               # both themes, every text role x surface
 *   node check-contrast.mjs --theme dark  # one theme only (light | dark)
 *   node check-contrast.mjs --ci          # exit 1 if any pairing fails AA, either theme
 *   node check-contrast.mjs --json        # machine-readable
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
 *   • That exclusion is LIGHT-ONLY for the -light roles. On the dark theme they are the
 *     intended roles, so a failure there is real and must reach the verdict.
 *
 * DARK THEME - read this before acting on the dark numbers:
 *   DGA publishes 402 dark declarations under `[data-theme=dark] :root`, a selector that can
 *   never match (:root is <html>; a descendant combinator needs an ancestor it does not
 *   have). So today no DGA platform renders dark at all. These pairings describe what WOULD
 *   ship if the selector were corrected - and three are worse than anything in light.
 *   See tokens.json role.dark.$verify.
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

/** Audit one theme's text roles against that same theme's surfaces. */
function audit(theme) {
  const roles = theme === 'dark' ? t.role.dark : t.role
  const out = []
  for (const [role, fg] of Object.entries(roles.text)) {
    if (role.startsWith('$')) continue
    for (const surface of SURFACES) {
      const bg = roles.background[surface]
      if (!bg) continue
      const r = round(ratio(fg, bg))
      out.push({
        theme,
        text: `text.${role}`, fg,
        background: `background.${surface}`, bg,
        ratio: r,
        aaNormal: r >= 4.5,
        aaLarge: r >= 3,
        // A dark-surface token failing on a LIGHT surface is expected, not a defect. On dark it
        // is the intended role, so the same failure is real and must reach the verdict.
        expected: (theme === 'light' && role.endsWith('-light')) ||
                  role.startsWith('oncolor') || role.includes('disabled'),
      })
    }
  }
  return out
}

const themeArg = process.argv[process.argv.indexOf('--theme') + 1]
const THEMES = process.argv.includes('--theme') && ['light', 'dark'].includes(themeArg)
  ? [themeArg] : ['light', 'dark']

const results = THEMES.flatMap(audit)
const fails = results.filter((x) => !x.aaLarge && !x.expected)
const largeOnly = results.filter((x) => x.aaLarge && !x.aaNormal && !x.expected)
const marginal = results.filter((x) => x.aaNormal && x.ratio < 5 && !x.expected)
const byTheme = (arr, th) => arr.filter((x) => x.theme === th)

if (process.argv.includes('--json')) {
  console.log(JSON.stringify({ results, fails, largeOnly, marginal }, null, 2))
} else {
  const line = (x) => `  ${THEMES.length > 1 ? x.theme.padEnd(6) : ''}${x.text.padEnd(28)} ${x.fg.padEnd(10)} on ${x.background.padEnd(24)} ${String(x.ratio).padStart(6)}:1`
  console.log(`DGA contrast check - ${t.$meta.systemName}`)
  console.log(`source ${t.$meta.source} retrieved ${t.$meta.retrieved}\n`)

  console.log(`FAIL - below AA at every size (${fails.length})`)
  fails.length ? fails.forEach((x) => console.log(line(x))) : console.log('  none')

  console.log(`\nLARGE TEXT ONLY - >=3:1 but <4.5:1 (${largeOnly.length})`)
  largeOnly.length ? largeOnly.forEach((x) => console.log(line(x))) : console.log('  none')

  console.log(`\nMARGINAL - passes AA by <0.5. Any opacity breaks these (${marginal.length})`)
  marginal.length ? marginal.forEach((x) => console.log(line(x))) : console.log('  none')

  console.log(`\n${results.length} pairings checked across ${THEMES.join(' + ')}. ${results.filter((x) => x.expected).length} oncolor/disabled/light-on-light roles excluded from the verdict.`)
  console.log(`Those are dark-surface tokens, NOT failures - do not delete them from a theme.`)

  const lightFails = byTheme(fails, 'light')
  if (lightFails.length) {
    const roles = [...new Set(lightFails.map((x) => x.text))]
    const one = roles.length === 1
    console.log(`\nLIGHT - ${one ? 'this is a real DGA token' : 'these are real DGA tokens'} designated for text: ${roles.join(', ')}.`)
    console.log(`Do not use ${one ? 'it' : 'them'} on a light surface at any size. secondary-gold.800`)
    console.log(`(#945c01) is the first gold step that clears AA on white.`)
  }
  if (byTheme(fails, 'dark').length) {
    console.log(`\nDARK - the dark theme cannot activate today: DGA ships [data-theme=dark] :root,`)
    console.log(`which never matches. If that selector is corrected, the failures above ship.`)
    console.log(`Worst first: the five *-light status surfaces are NOT remapped by dark, so white`)
    console.log(`text lands on a near-white background at ~1.05:1. text.error (#b42318) is`)
    console.log(`unreadable on every dark surface. Read tokens.json role.dark.$verify first.`)
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
  // --- dark theme regressions this file exists to keep visible ---
  const d = t.role.dark
  assert(d && d.text && d.background, 'tokens.json carries role.dark')
  assert(round(ratio(d.text.secondary, d.background.body)) === 7.64,
    'the gold that fails on light passes at 7.64:1 on dark - the light finding is not absolute')
  assert(round(ratio(d.text.error, d.background.body)) === 2.68,
    'dark text.error is 2.68:1 on the dark body - fails AA at every size')
  assert(round(ratio(d.text.default, d.background['brand-light'])) < 1.1,
    'dark does not remap the *-light surfaces, so white text on them is ~1.05:1')
  assert(d.background['brand-light'] === t.role.background['brand-light'],
    'background.brand-light is carried at its LIGHT value - that is the defect, not a typo')
  assert(byTheme(fails, 'dark').length > 0, 'the dark pass reaches the verdict')
  console.log('self-check passed')
}
