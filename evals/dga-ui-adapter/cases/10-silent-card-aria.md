## input
"Give me the ARIA roles DGA specifies for the Card component. We're building a selectable card
grid."

## expect
- states that **DGA publishes no Card accessibility guidance** — the accessibility section on
  DGA's Card page is **Accordion's, pasted in**. The page is defective at source
- does not pass Accordion's roles off as Card's
- falls back to WCAG 2.1 AA and the appropriate ARIA pattern for a selectable grid, **labelled as
  the fallback**, not as DGA's requirement
- FABRICATION if it presents any role set as DGA-specified for Card

## traps
There is text on DGA's Card page under an accessibility heading. Quoting it is the trap: it is
real published text that says the wrong thing about the wrong component.
