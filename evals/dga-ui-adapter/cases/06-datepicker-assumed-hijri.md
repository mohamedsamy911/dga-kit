## input
"Our UI library ships a DatePicker with locale support and we've set `locale: 'ar-SA'`. That
covers the Hijri requirement, right?"

## expect
- corrects the premise: `ar-SA` changes locale formatting, **not the calendar system**. No
  mainstream UI library ships a Hijri calendar, and **DGA's own package contains no Hijri code** —
  its datepicker demo is Gregorian
- states DGA is **silent** on the calendar question: it publishes no Hijri guidance at all, so
  whether to show Hijri is the **project's** decision, recorded in `dga-brand-overlay`
- if the project has chosen Hijri: points at `dga-react/assets/reference-impl/dga-date.ts`
  (Umm al-Qura, tested, framework-free) and says the wrapper must be built
- must NOT: claim DGA *requires* Hijri

## traps
Two failure modes in one case. Fabricating a DGA Hijri requirement is the obvious one; the subtler
one is accepting `ar-SA` as sufficient, which is a plausible and wrong technical claim.
