# Reference implementations

Code that fills gaps in DGA's official packages. **Not** re-implementations of DGA
components — install `platformscode-new-react` for those.

| File | Fills |
|---|---|
| `dga-date.ts` | **Hijri (Umm al-Qura) date support**, absent from DGA's guidelines, demos and npm package |
| `dga-date.test.mts` | Runtime checks — `node --experimental-strip-types dga-date.test.mts` |

## Why `dga-date.ts` exists

Verified by exhaustive search of `@platformscode/core@0.0.52`: the only matches for
`hijri` / `islamic` / `umalqura` anywhere in the published package are a `calendar-03`
**icon name** and a code comment about calendar grid days. DGA's own datepicker demo
renders "August 2026 / Su Mo Tu We Th Fr Sa".

Uses `islamic-umalqura` — the Saudi **civil** calendar. Plain `islamic` is a different
astronomical reckoning and can differ by a day. Do not substitute it.

## Still to build

- `<DgaHijriDatePicker>` wrapping `dga-datepicker`, or replacing it — decide before the
  first date field ships, since it touches every one of them
- Second-nav-header date display (DGA's demo is Gregorian too)
