/**
 * Smoke tests for dga-date.ts.  Run:  node --experimental-strip-types dga-date.test.mts
 *
 * These exist because the first version of this file shipped two bugs that only a
 * runtime check catches: a duplicated era marker ("1448 هـ هـ" — Intl already emits it)
 * and a hijriToGregorian that returned the right calendar date but not a normalised
 * UTC-midnight timestamp, so round-trips failed equality.
 */
import * as m from './dga-date.ts'

let fail = 0
const check = (name: string, got: unknown, want: unknown) => {
  const ok = got === want
  if (!ok) fail++
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : `\n      got  ${got}\n      want ${want}`}`)
}

const d = new Date(Date.UTC(2026, 7, 26))

check('no duplicate era (ar)', /هـ.*هـ/.test(m.formatDual(d, { locale: 'ar' })), false)
check('no duplicate era (en)', /AH.*AH/.test(m.formatDual(d, { locale: 'en' })), false)

let rtFail = 0, n = 0
for (let i = 0; i < 365; i += 11) {
  const src = new Date(Date.UTC(2026, 0, 1) + i * 86_400_000)
  const p = m.toHijriParts(src)
  if (m.hijriToGregorian(p.year, p.month, p.day).getTime() !== src.getTime()) rtFail++
  n++
}
check(`round-trip exact over ${n} dates`, rtFail, 0)

const bad: string[] = []
for (let mth = 1; mth <= 12; mth++) {
  const L = m.hijriMonthLength(1448, mth)
  if (L !== 29 && L !== 30) bad.push(`${mth}:${L}`)
}
check('all 1448 months are 29 or 30 days', bad.join(','), '')

check('numerals latn by default', /\d/.test(m.formatHijri(d)), true)
check('numerals arab opt-in', /[٠-٩]/.test(m.formatHijri(d, { numerals: 'arab' })), true)
check('umm al-qura, not plain islamic', m.toHijriParts(d).year, 1448)

console.log(fail ? `\n${fail} FAILING` : '\nAll checks passed')
if (fail) process.exit(1)
