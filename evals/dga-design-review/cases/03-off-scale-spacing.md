## input
Card grid with 20px gaps between cards, 34px section padding, and 720px content width.

## expect
- 20px: **compliant** — `2xl` is 20px on DGA's scale
- 34px: **Major** — not on the scale; nearest steps are 32px (`4xl`) and 40px (`5xl`)
- 720px: **compliant** — matches `paragraph-max-width`
- must NOT flag 20px

## traps
20px looks off-scale to anyone assuming a pure 4/8px system, but DGA's named scale includes
it. Flagging it is a false positive.
