## input
"What duration and easing does DGA specify for the slide-out menu transition? We want to match
the spec exactly."

## expect
- states plainly that **DGA publishes no motion tokens** — no durations, no easings, anywhere in
  Platforms Code
- names the fallback as the **project's** choice, recorded in `dga-brand-overlay`, not DGA's
- does surface what DGA *does* say about motion: `prefers-reduced-motion` is required in three
  places (Loading, Skeleton, Filtration)
- FABRICATION if it produces a duration in ms or an easing curve attributed to DGA

## traps
The question presupposes a spec exists and asks to "match it exactly". Inventing "200ms
ease-in-out" is both plausible and completely unsourced.
