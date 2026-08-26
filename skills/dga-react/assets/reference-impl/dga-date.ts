/**
 * Hijri + Gregorian date formatting for a DGA-compliant project.
 *
 * WHY THIS EXISTS: DGA's Platforms Code has no Hijri support anywhere — not in the
 * datepicker guideline, not in its live demo ("August 2026 / Su Mo Tu..."), and not in
 * the official npm package (verified by exhaustive search of @platformscode/core).
 * For a Saudi government service that gap has to be filled by the consuming project.
 *
 * Built on the platform Intl API — no date library. `islamic-umalqura` is the Saudi
 * CIVIL calendar; plain `islamic` is a different (astronomical) reckoning and can differ
 * by a day. Do not substitute it.
 *
 * NUMERALS: DGA states no policy on Arabic-Indic (٠١٢٣) vs Western (0123). The project
 * decision is recorded in skills/dga-brand-overlay/SKILL.md. `numerals` defaults to 'latn'
 * because reference numbers, IDs and anything a user may copy into another system must
 * stay Western — see formatting rules in dga-rtl-i18n/references/formats.md.
 */

export type Calendar = 'hijri' | 'gregorian'
export type Numerals = 'latn' | 'arab'
export type Locale = 'ar' | 'en'

export interface DateFormatOptions {
  locale?: Locale
  numerals?: Numerals
  /** Intl dateStyle, or pass `fields` for finer control */
  dateStyle?: 'full' | 'long' | 'medium' | 'short'
  fields?: Intl.DateTimeFormatOptions
}

const CALENDAR_ID: Record<Calendar, string> = {
  hijri: 'islamic-umalqura',
  gregorian: 'gregory',
}

function buildLocale(locale: Locale, calendar: Calendar, numerals: Numerals): string {
  const base = locale === 'ar' ? 'ar-SA' : 'en-SA'
  return `${base}-u-ca-${CALENDAR_ID[calendar]}-nu-${numerals}`
}

/** Format a date in a single calendar. */
export function formatDate(
  date: Date,
  calendar: Calendar,
  { locale = 'ar', numerals = 'latn', dateStyle = 'long', fields }: DateFormatOptions = {},
): string {
  const opts: Intl.DateTimeFormatOptions = fields ?? { dateStyle }
  return new Intl.DateTimeFormat(buildLocale(locale, calendar, numerals), opts).format(date)
}

export const formatHijri = (d: Date, o?: DateFormatOptions) => formatDate(d, 'hijri', o)
export const formatGregorian = (d: Date, o?: DateFormatOptions) => formatDate(d, 'gregorian', o)

/**
 * Both calendars in one string — the common pattern on Saudi government services.
 * Order puts Hijri first for `ar`, Gregorian first for `en`.
 *
 * NOTE: Intl already emits the era marker ("هـ" / "AH") for islamic-umalqura. Do not
 * append your own — an earlier version of this file did and produced "1448 هـ هـ".
 */
export function formatDual(date: Date, o: DateFormatOptions = {}): string {
  const locale = o.locale ?? 'ar'
  const h = formatHijri(date, o)   // already carries هـ / AH
  const g = formatGregorian(date, o)
  return locale === 'ar' ? `${h} (${g})` : `${g} (${h})`
}

/** Extract Hijri year/month/day as numbers — useful for a custom calendar grid. */
export function toHijriParts(date: Date): { year: number; month: number; day: number } {
  const parts = new Intl.DateTimeFormat('en-u-ca-islamic-umalqura-nu-latn', {
    year: 'numeric', month: 'numeric', day: 'numeric',
  }).formatToParts(date)
  const get = (t: string) => Number(parts.find(p => p.type === t)?.value.replace(/[^\d]/g, ''))
  return { year: get('year'), month: get('month'), day: get('day') }
}

/** Number of days in a given Hijri month — Umm al-Qura months are 29 or 30, not fixed. */
export function hijriMonthLength(hYear: number, hMonth: number): number {
  const start = hijriToGregorian(hYear, hMonth, 1)
  const next = hMonth === 12 ? hijriToGregorian(hYear + 1, 1, 1) : hijriToGregorian(hYear, hMonth + 1, 1)
  return Math.round((next.getTime() - start.getTime()) / 86_400_000)
}

/**
 * Hijri → Gregorian. Intl only formats one way, so this searches for the Gregorian date
 * whose Hijri parts match. Bounded and fast (a few iterations).
 */
export function hijriToGregorian(hYear: number, hMonth: number, hDay: number): Date {
  // Rough anchor: Hijri epoch 622-07-16 CE, mean year ~354.367 days.
  // Normalised to UTC midnight so the result round-trips exactly against a UTC-midnight input.
  const days = Math.floor((hYear - 1) * 354.367 + (hMonth - 1) * 29.53 + (hDay - 1))
  const anchor = Date.UTC(622, 6, 16) + days * 86_400_000
  const approx = Math.floor(anchor / 86_400_000) * 86_400_000
  for (let delta = 0; delta <= 5; delta++) {
    for (const sign of [0, -1, 1]) {
      const probe = new Date(approx + sign * delta * 86_400_000)
      const p = toHijriParts(probe)
      if (p.year === hYear && p.month === hMonth && p.day === hDay) return probe
    }
  }
  throw new RangeError(`No Gregorian date matches Hijri ${hYear}-${hMonth}-${hDay}`)
}

/** Arabic month names for a custom picker header. */
export function hijriMonthNames(locale: Locale = 'ar'): string[] {
  const f = new Intl.DateTimeFormat(`${locale === 'ar' ? 'ar-SA' : 'en'}-u-ca-islamic-umalqura`, { month: 'long' })
  return Array.from({ length: 12 }, (_, i) => f.format(hijriToGregorian(1447, i + 1, 1)))
}
